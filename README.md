# Logistics Global Performance & Sales Goals Dashboard

## 📌 Escenario de Negocio
La dirección de logística global necesitaba monitorear el cumplimiento de objetivos de ventas y volumen (CBM) por región y sucursal en tiempo real. Este dashboard centraliza la operación de múltiples nodos para identificar desviaciones críticas en el presupuesto anual.

## 🛠️ Stack Tecnológico
*   **Herramienta de BI:** Power BI Desktop.
*   **Modelado:** Esquema en estrella (Star Schema) con tablas de hechos de ventas y metas.
*   **ETL:** Power Query para la normalización de datos regionales y limpieza de inconsistencias.
*   **Lenguajes:** DAX (Medidas de inteligencia de tiempo y cumplimiento) y SQL para la extracción de datos.

## 🚀 Desafíos Técnicos Resueltos
1.  **Cálculo de Cumplimiento Dinámico:** Implementación de lógica DAX para comparar `Booking vs Goals` con filtros aplicados a múltiples zonas horarias y monedas.
2.  **Optimización del Modelo:** Reducción de la latencia en el filtrado mediante la correcta jerarquización de dimensiones (Sucursal -> Región).
3.  **Anonimización de Datos:** Proceso de escalado aleatorio de cifras para proteger la confidencialidad sin perder la integridad de las tendencias.

## 📈 Visualización del Proyecto
![Dashboard Principal](assets/dashboard_performance.png)

## 💡 Impacto
*   Reducción del tiempo de consolidación de reportes de 3 días a actualización automática.
*   Visibilidad inmediata de sucursales con bajo rendimiento (KPI de % Cumplimiento).
