# Importacion de librerias y modulos de Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime, timedelta
import logging
import pandas as pd
import oracledb
from azure.storage.blob import BlobServiceClient
from io import BytesIO

def run_etl_ventas():
    # Obtencion de credenciales desde el backend de Airflow para evitar hardcoding
    try:
        oracle_conn = BaseHook.get_connection('oracle_ventas_prod')
        azure_conn = BaseHook.get_connection('azure_datalake_prod')
    except Exception as e:
        logging.error("Las conexiones 'oracle_ventas_prod' o 'azure_datalake_prod' no estan configuradas en Airflow.")
        raise e

    # Asignacion de parametros de conexion Oracle
    oracle_user = oracle_conn.login
    oracle_password = oracle_conn.password
    oracle_host = oracle_conn.host
    oracle_port = oracle_conn.port
    
    # Asignacion de cadena de conexion Azure
    azure_conn_str = azure_conn.password 

    # Definicion de rutas y contenedores destino
    container_name = "datawarehouse"
    blob_name = "Producto/DWH_VENTAS.parquet"
    
    # Lista de esquemas/SIDs a iterar
    paises = [
        "ARGENTINA", "BRASIL", "BOLIVIA", "CHILE2", "COLOMBIA", "COSTARICA", 
        "ECUADOR", "GUATEMALA", "ORCL", "PARAGUAY", "PERU2", "VENEZUELA", 
        "URUGUAY", "IFS", "SALVADOR", "HONDURAS", "MEXICO", "NICARAGUA".....
    ]
    
    # Consulta SQL base
    query = "SELECT * FROM DWH_EXPO_SALES"
    df_list = []

    # Iteracion sobre cada pais para extraer datos de forma independiente
    for pais in paises:
        logging.info(f"Extrayendo datos de: {pais}")
        dsn = oracledb.makedsn(oracle_host, oracle_port, sid=pais)
        
        try:
            # Conexion usando context manager para garantizar el cierre
            with oracledb.connect(user=oracle_user, password=oracle_password, dsn=dsn) as conn:
                df = pd.read_sql(query, con=conn)
                if not df.empty:
                    df_list.append(df)
                    logging.info(f"{len(df)} registros extraidos de {pais}.")
                else:
                    logging.info(f"Sin registros en {pais}.")
        except oracledb.Error as e:
            # Propagacion del error para que Airflow registre el fallo de la tarea
            logging.error(f"Error critico en base de datos {pais}: {e}")
            raise 

    # Validacion de datos extraidos antes de procesar
    if not df_list:
        logging.warning("No se extrajeron datos. Cancelando subida a Azure.")
        return

    # Consolidacion de datos en memoria
    df_final = pd.concat(df_list, ignore_index=True)
    
    # Limpieza de caracteres especiales en columnas de texto
    string_cols = df_final.select_dtypes(include=['object']).columns
    df_final[string_cols] = df_final[string_cols].replace(r'\r|\n|,', '', regex=True)
    
    # Conversion a formato Parquet en memoria (Zero-Disk-I/O)
    parquet_buffer = BytesIO()
    df_final.to_parquet(parquet_buffer, engine='pyarrow', index=False)
    parquet_buffer.seek(0)
    
    # Carga del archivo al Data Lake
    logging.info("Iniciando transmision a Azure Blob Storage...")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(azure_conn_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        blob_client.upload_blob(parquet_buffer, overwrite=True)
        logging.info("Carga en Azure completada exitosamente.")
    except Exception as e:
        logging.error(f"Fallo en la comunicacion con Azure: {e}")
        raise 


# Configuracion de politicas de ejecucion y reintentos del DAG
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 27),
    'email_on_failure': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Declaracion del DAG e instanciacion de tareas
with DAG(
    dag_id='oracle_to_azure_ventas_diario',
    default_args=default_args,
    description='ETL in-memory de Oracle LATAM hacia Azure Data Lake',
    schedule_interval='0 3 * * *',
    catchup=False,
    tags=['core', 'ventas', 'ingesta'],
) as dag:

    tarea_extraccion_carga = PythonOperator(
        task_id='extraer_origen_cargar_datalake',
        python_callable=run_etl_ventas,
    )