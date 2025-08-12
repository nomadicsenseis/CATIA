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
[{'period': 1, 'date_range': '2025-08-01 to 2025-08-07', 'ai_interpretation': '📈 SÍNTESIS EJECUTIVA:\n\nDurante la semana del 1 al 7 de agosto de 2025, se identificaron patrones divergentes significativos en la experiencia del cliente que evidencian una dualidad operativa crítica en la red. Mientras el segmento Business Short Haul de Vueling experimentó una mejora excepcional de 12.1 puntos (pasando de un NPS baseline de 3.2 a 15.3), las cabinas premium de Long Haul sufrieron deterioros severos: Business LH cayó 8.3 puntos (de 29.2 a 21.0) y Premium LH se desplomó 19.2 puntos (de 40.0 a 20.8). Esta dualidad se explica por dos causas operativas independientes: una mejora específica en los procesos de Vueling que benefició únicamente a sus pasajeros Business en rutas cortas, y un deterioro operativo sistémico que afectó toda la red Long Haul con impacto proporcional a las expectativas de servicio de cada segmento.\n\nLos grupos de clientes más reactivos fueron claramente los pasajeros Premium de Long Haul, quienes mostraron la mayor sensibilidad al deterioro operativo, seguidos por Business LH, mientras que Economy LH demostró mayor resistencia manteniendo variaciones dentro de rangos normales. La especificidad geográfica y por compañía de las mejoras (exclusivamente Vueling Short Haul Business) contrasta con la naturaleza sistémica de los problemas en Long Haul, sugiriendo causas operativas completamente diferentes que requieren estrategias de intervención diferenciadas por radio y tipo de cliente.\n\n**ECONOMY SH: Estabilidad Operativa Mantenida**\n\nLa cabina Economy de Short Haul mantuvo desempeño estable durante la semana del 1 de agosto, registrando un NPS de 22.7 con una variación de apenas 0.9 puntos respecto al período anterior. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción tanto en Iberia (22.9, +0.8 puntos) como en Vueling (22.2, +1.1 puntos), lo que evidencia una operación estable y convergente entre ambas compañías en este segmento.\n\n**BUSINESS SH: Mejora Excepcional Específica de Vueling**\n\nEl segmento Business de Short Haul mostró un comportamiento divergente notable, registrando un NPS agregado de 24.3 con una mejora de 3.7 puntos vs el período anterior. Esta evolución se explica exclusivamente por una mejora extraordinaria en Vueling Business (+12.1 puntos, alcanzando un NPS de 15.3 desde un baseline de 3.2), mientras que Iberia Business mantuvo estabilidad (29.5, -1.5 puntos). La especificidad de esta mejora en Vueling sugiere la implementación exitosa de iniciativas operativas o de servicio particulares de esta compañía.\n\n**ECONOMY LH: Resistencia Relativa al Deterioro Sistémico**\n\nLa cabina Economy de Long Haul mantuvo desempeño relativamente estable, registrando un NPS de 12.0 con una variación de -2.6 puntos respecto al período anterior. No se detectaron cambios significativos que constituyeran anomalías, manteniendo niveles de resistencia ante el deterioro operativo que afectó más severamente a las cabinas premium del mismo radio.\n\n**BUSINESS LH: Deterioro Operativo Significativo**\n\nLa cabina Business de Long Haul experimentó un deterioro notable, registrando un NPS de 21.0 con una caída de 8.3 puntos vs el período anterior. Esta degradación forma parte del patrón sistémico que afectó toda la red Long Haul, siendo especialmente visible en los segmentos con mayores expectativas de servicio, aunque sin alcanzar la severidad observada en Premium.\n\n**PREMIUM LH: Impacto Severo del Deterioro Sistémico**\n\nEl segmento Premium de Long Haul sufrió el mayor impacto, registrando un NPS de 20.8 con una caída severa de 19.2 puntos vs el período anterior. Esta degradación extrema evidencia la máxima reactividad de los pasajeros premium ante problemas operativos sistémicos, confirmando que este segmento actúa como el indicador más sensible de la calidad operativa en rutas largas.'}]

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