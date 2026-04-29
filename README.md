# Logistics Global Performance & Sales Goals Dashboard

## Visualización Principal
![Dashboard de Performance Global](assets/EXPO01.png)

## Escenario de Negocio
La Dirección Comercial requería monitorear el cumplimiento de objetivos de ventas por Booking (bkg) y volumen (CBM) a nivel regional, sucursal, puerto de carga, puerto de descarga y agente en tiempo real. Anteriormente, el proceso carecía de estandarización y cada oficina regional medía sus indicadores de forma trimestral. Este dashboard centraliza la operación global, permitiendo a las áreas comerciales identificar rápidamente el estado de cumplimiento para ejecutar acciones correctivas.

## Stack Tecnológico
* **Herramienta de BI:** Power BI Desktop.
* **Modelado:** Esquema de Constelación (Fact Constellation) con dimensiones conformadas.
* **Seguridad:** Implementación de Row-Level Security (RLS) dinámico por región de usuario.
* **ETL:** Power Query y Python (Pandas) para normalización de estructuras dispares.
* **Orquestación:** Apache Airflow.
* **Lenguajes:** DAX, SQL (Oracle), Python.

## Desafíos Técnicos Resueltos
* **Resolución de asimetría de granularidad temporal:** Diseño de un modelo capaz de cruzar transacciones operativas diarias (ventas/bookings) con metas comerciales, evitando la duplicación de valores en las agregaciones. Estos objetivos fueron definidos tanto a nivel semanal como mensual, cruzando variables de Oficina, Región, POD, POL y Agente.
* **Exposición de datos nulos (Puntos ciegos):** Implementación de lógica DAX avanzada y configuración de interacciones visuales para anular el comportamiento nativo que oculta nodos sin ventas. Esto fuerza la visualización de agencias o puertos con presupuesto asignado pero rendimiento operativo nulo.
* **Control de jerarquías dinámicas:** Desarrollo de cálculos que detectan el contexto de filtro activo (Nivel Global, Región, Puerto o Agente) para reasignar y calcular los presupuestos matemáticamente sin corromper los subtotales de la matriz.

## Impacto y Resultados
* **Visibilidad operativa inmediata:** Identificación instantánea del rendimiento de cada oficina, eliminando el procesamiento manual de múltiples hojas de cálculo y reduciendo los tiempos de latencia en la toma de decisiones.
* **Integridad de datos:** Alineación exacta entre los sistemas transaccionales y los objetivos comerciales mediante la corrección estructural de las bases de origen, garantizando KPIs de cumplimiento auditables.
* **Consolidación de herramientas analíticas:** Arquitectura escalable que centraliza el análisis de múltiples unidades de negocio (Exportación, Importación, Marítimo, Aéreo) en un único modelo semántico interactivo.

---

## Arquitectura de Datos y Modelo
El núcleo del proyecto es un Esquema de Constelación que permite resolver el filtrado eficiente entre múltiples tablas de hechos de diferente nivel de agregación.

![Modelo de Datos - Constellation Schema](assets/EXPO2.png)

### Capa de Ingeniería (ETL & SQL)
El flujo de datos se sostiene sobre la siguiente estructura:
* **Extracción (SQL):** Utilización de consultas optimizadas en Oracle para preprocesar los datos desde el origen y reducir la carga de procesamiento en el motor de Power BI. *(Ref: `assets/DWH_EXPORT_SALES.sql`)*.
* **Automatización (Python):** Gestión y validación de integridad de los archivos regionales antes de la ingesta mediante scripts, asegurando la inexistencia de valores nulos en campos de facturación clave. *(Ref: `assets/DWH_EXPORT_SALES.py`)*.

---
*Nota: Este repositorio documenta la arquitectura y desarrollo de un proyecto real implementado en producción. Para cumplir con las políticas de privacidad y acuerdos de confidencialidad (NDA), todos los datos financieros, volúmenes operativos y nombres de entidades han sido estrictamente alterados y anonimizados.*
