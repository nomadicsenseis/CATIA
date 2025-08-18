===== SYSTEM =====

Eres un experto analista ejecutivo especializado en completar análisis de NPS comprehensivos.

⚠️ **CRÍTICO - NO INVENTES DATOS:**
Si hay algún dato que te falta, NO lo supongas ni inventes. En su lugar, indica claramente que ese dato específico no está disponible. Por ejemplo: "El análisis diario para Economy LH no está disponible" o "Los datos de rutas para el día 25 no están incluidos en el análisis".

⚠️ **IMPORTANTE - SI HAY DATOS DIARIOS, ÚSALOS:**
Si se te proporciona análisis diario en la sección "ANÁLISIS DIARIO SINGLE", DEBES usarlo e integrarlo en el resumen. NO digas que "no está disponible" si los datos están presentes en el input.

TU FUNCIÓN:
- Tomar la síntesis ejecutiva del interpreter semanal TAL COMO ESTÁ
- INTEGRAR el detalle diario del interpreter DENTRO de cada sección correspondiente de la síntesis semanal
- Identificar días especialmente reseñables en el detalle diario
- Crear un resumen fluido y ejecutivo

IMPORTANTE:
- NO incluyas recomendaciones adicionales
- NO uses títulos como "Integración del análisis diario" o similares
- El análisis diario debe fluir naturalmente como un párrafo adicional
- Identifica días especialmente reseñables en el detalle diario
- Haz el texto fluido y ejecutivo, no técnico
- Solo incluye días que tengan análisis relevantes (con caídas/subidas o datos significativos)
- Para cabinas/radio sin incidencias: comenta solo su NPS del período y el del período de comparación
- NO hables de "anomalias". Habla de "caídas" o "subidas" de NPS.
- SI hay datos diarios en el input, ÚSALOS. NO digas que "no están disponibles" si están presentes.

ANCLAJE DE SECCIONES (case-insensitive):
- Global (los 2 primeros párrafos de la síntesis)
- Economy SH
- Business SH
- Economy LH
- Business LH
- Premium LH

INTEGRACIÓN POR SECCIÓN:
- Tras cada bloque semanal anterior, añade exactamente un párrafo narrativo con los días reseñables en orden cronológico (28-jul → 03-ago si existen).
- Incluye cuando estén disponibles: NPS actual, baseline y diferencia; métricas clave (p.ej., % mishandling, nº cambios de aeronave, reprogramaciones, reubicaciones) y rutas/destinos citados.
- Si el bloque semanal indica "sin datos", REDACTA como: "Se mantiene estable a nivel semanal; pueden existir oscilaciones diarias que se detallan a continuación" y añade igualmente el párrafo diario si hay datos.
- No modifiques, no reordenes ni resumas el texto semanal. No alteres sus cifras ni redondeos.

ESTILO Y LÉXICO:
- Estilo ejecutivo, fluido y conciso. No técnico.
- Usa "subidas/bajadas", "mejoras/deterioros". Evita "anomalía/s".
- Máximo 1-2 frases por día; prioriza 28, 29, 30, 31 de julio; 1, 2, 3 de agosto.
- No inventes cifras. Si no hay NPS exacto en el diario, describe el evento y su dirección (subida/bajada) sin números.


===== USER =====

Completa el análisis comprehensivo:

**ANÁLISIS SEMANAL COMPARATIVO:**
[{'period': 1, 'date_range': '2025-08-01 to 2025-08-07', 'ai_interpretation': '📈 SÍNTESIS EJECUTIVA:\n\nDurante la semana del 1 al 7 de agosto de 2025, el NPS global de Iberia experimentó una ligera caída de 0.78 puntos, pasando de 20.51 a 19.73 puntos. Esta evolución refleja principalmente una crisis operativa sistémica en Long Haul que afectó todas las cabinas con diferentes intensidades, mientras que Short Haul mostró patrones divergentes por compañía. La causa principal fue un colapso masivo en la gestión de conexiones (+97% pérdidas de conexión, +150% cambios de equipo) que impactó especialmente las operaciones Long Haul, evidenciado por el deterioro del 63.3% en incidentes operativos totales y una caída del 6.7% en puntualidad real (OTP15). Paralelamente, Short Haul Business experimentó una divergencia extrema entre compañías: Iberia sufrió deterioro en servicios auxiliares (+120% otras incidencias, especialmente lounge) mientras Vueling logró mejoras operativas significativas (-40.1% conexiones perdidas, +20.24 puntos en satisfacción de puntualidad).\n\nLas rutas más afectadas se concentraron en el corredor Madrid-Latinoamérica, destacando MAD-SCL con el NPS más crítico de 12.5 puntos (16 pasajeros) y MAD-MIA con 37.5 puntos (8 pasajeros), ambas mostrando la mayor vulnerabilidad operativa. Los grupos de clientes más reactivos fueron los residentes de regiones específicas con spreads de hasta 130.9 puntos de variabilidad, seguidos por los clientes de operaciones codeshare que mostraron sensibilidad extrema con rangos de hasta 104 puntos entre el mejor y peor desempeño.\n\n**ECONOMY SH: Desempeño Estable**\nLa cabina Economy de Short Haul mantuvo desempeño estable durante la semana del 1 al 7 de agosto, sin registrar anomalías significativas en su NPS semanal. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción y operando dentro de parámetros normales sin impactos detectables de las disrupciones que afectaron otros segmentos.\n\n**BUSINESS SH: Divergencia Extrema por Compañía**\nEl segmento Business de Short Haul experimentó la mayor divergencia operativa del período, con Iberia registrando una caída de 3.22 puntos (de 31.07 a 27.85) mientras Vueling logró una mejora excepcional de 9.94 puntos (de 3.20 a 13.14). Esta evolución opuesta se explica principalmente por el deterioro de servicios de lounge en Iberia (SHAP -0.503, satisfacción -10.77%) contrastado con mejoras masivas en puntualidad de Vueling (SHAP +12.823, satisfacción +20.24%), siendo especialmente visible en las 17 rutas Long Haul gestionadas por Vueling y entre perfiles de flota que mostraron la máxima reactividad con spreads de hasta 143.3 puntos.\n\n**ECONOMY LH: Compensación Heroica Parcialmente Exitosa**\nLa cabina Economy de Long Haul experimentó una caída moderada de 2.26 puntos, pasando de un NPS de 14.55 a 12.28 durante la semana del 1 al 7 de agosto. La causa principal fue una crisis operativa severa con deterioro del 34-97% en múltiples métricas (pérdidas de conexión +97%, incidentes +34%), pero compensada heroicamente por mejoras excepcionales en experiencia de llegada (SHAP +3.496, satisfacción +6.32 puntos) y soporte de preparación de viaje (+8.38 puntos). Esta compensación se reflejó especialmente en rutas como MAD-UIO (NPS 100.0, +65.2 puntos) y MAD-SDQ (NPS 66.7, +39.6 puntos), mientras que los perfiles más reactivos incluyen clientes codeshare con spreads de 73.6 puntos de variabilidad.\n\n**BUSINESS LH: Compensación Fallida con Colapso de Conexiones**\nLa cabina Business de Long Haul registró una caída significativa de 6.61 puntos, deteriorándose de 29.24 a 22.63 durante el período analizado. Los drivers principales fueron el colapso masivo de conexiones (SHAP -4.178, correlacionado con +97% pérdidas de conexión reales) y el deterioro del programa de lealtad IB Plus (SHAP -4.592, satisfacción -24.29%), parcialmente compensados por mejoras en preparación de viaje (SHAP +13.232) y cambios de aeronave (SHAP +9.525 por downgauging). Esta crisis impactó especialmente las rutas MAD-SCL (NPS 12.5) y MAD-MIA (NPS 37.5), siendo los residentes regionales los perfiles más vulnerables con spreads extremos de 130.9 puntos de reactividad.\n\n**PREMIUM LH: Deterioro Severo por Expectativas No Cumplidas**\nEl segmento Premium de Long Haul sufrió la mayor caída del período con 19.75 puntos de deterioro, pasando de 40.00 a 20.25 durante la semana del 1 al 7 de agosto. Las causas dominantes fueron el deterioro operativo multifactorial (+86.7% incidentes diversos, +58.3% retrasos, -6.7% puntualidad real) combinado con deterioro secundario de producto (aircraft interior -15.76%, food & beverage -13.80%), parcialmente compensado por mejoras en experiencia de llegada (SHAP +10.002) debido a la reducción del 50% en cancelaciones. Este impacto fue especialmente evidente en la red atlántica de alto impacto, particularmente MAD-SCL (NPS 12.5) y rutas Barcelona-Sudamérica con limitaciones técnicas, siendo los perfiles de flota los más reactivos con spreads de 9.0 puntos según tipo de aeronave utilizada.'}]

**ANÁLISIS DIARIO SINGLE:**


TAREA:
1. Copia la síntesis ejecutiva del interpreter semanal TAL COMO ESTÁ
2. Para cada sección (Párrafo 1, Párrafo 2, y cada sección de cabina/radio):
   - Mantén el contenido semanal TAL COMO ESTÁ
   - Añade DESPUÉS un párrafo adicional con el detalle diario correspondiente
   - Integra de forma fluida y natural, sin títulos ni separadores
   - El análisis diario debe fluir naturalmente después del análisis semanal
3. Orden de integración: Global (párrafos 1 y 2), luego Economy SH, Business SH, Economy LH, Business LH, Premium LH
4. Identifica días especialmente reseñables en el detalle diario (en orden cronológico)
5. NO cambies la síntesis ejecutiva del interpreter semanal (ni cifras ni redondeos)
6. NO añadas recomendaciones adicionales
7. Haz el texto fluido y ejecutivo, no técnico, evitando la palabra "anomalía"
8. Solo incluye días que tengan análisis relevantes (con caídas/subidas o datos significativos)
9. Para cabinas/radio con "sin datos": REDACTA como estabilidad semanal y añade, si existen, las oscilaciones diarias relevantes a continuación
10. **CRÍTICO**: Si hay datos en "ANÁLISIS DIARIO SINGLE", DEBES usarlos. NO digas que "no están disponibles" si están presentes en el input.