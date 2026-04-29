# Logistics Global Performance & Sales Goals Dashboard

## 📊 Visualización Principal
![Dashboard de Performance Global](assets/EXPO01.png)

## 📌 Escenario de Negocio
La dirección de logística global requería monitorear el cumplimiento de objetivos de ventas y volumen (CBM) por región y sucursal en tiempo real. Este dashboard centraliza la operación de múltiples nodos para identificar desviaciones críticas en el presupuesto anual y optimizar la toma de decisiones.

## 🛠️ Stack Tecnológico
* **Herramienta de BI:** Power BI Desktop.
* **Modelado:** Esquema en estrella (Star Schema).
* **ETL:** Power Query y Python (Pandas) para normalización.
* **Orquestación:** Apache Airflow.
* **Lenguajes:** DAX, SQL (Oracle), Python.

## 🚀 Desafíos Técnicos Resueltos

1. **Cálculo de Cumplimiento Dinámico:** Lógica DAX avanzada para comparar `Booking vs Goals` gestionando múltiples zonas horarias y monedas.
2. **Optimización del Modelo:** Reducción de latencia mediante jerarquización de dimensiones y optimización de tipos de datos.
3. **Anonimización:** Escalado aleatorio de métricas para proteger datos sensibles sin alterar las tendencias y correlaciones.

---

## 🏗️ Arquitectura de Datos y Modelo
El núcleo del proyecto es un **Esquema en Estrella** que permite un filtrado eficiente y escalabilidad.

![Modelo de Datos - Star Schema](assets/EXPO2.png)

### Capa de Ingeniería (ETL & SQL)
El flujo de datos se sostiene sobre una estructura robusta:

* **Extracción (SQL):** Se utilizan consultas optimizadas en Oracle para pre-procesar los datos y reducir la carga en el motor de Power BI. Ver archivo: `assets/DWH_EXPORT_SALES.sql`.
* **Automatización (Python):** El script `assets/DWH_EXPORT_SALES.py` gestiona la validación de integridad de los archivos regionales antes de la ingesta, asegurando que no existan nulos en campos de facturación clave.

---

## 💡 Impacto y Resultados
* **Eficiencia:** Reducción del tiempo de consolidación de reportes de 3 días a actualización automática inmediata.
* **Gobierno de Datos:** Implementación de una "versión única de la verdad" para todas las sucursales globales.
* **Accionabilidad:** Identificación inmediata de nodos con bajo rendimiento mediante KPIs de cumplimiento visuales.

---
