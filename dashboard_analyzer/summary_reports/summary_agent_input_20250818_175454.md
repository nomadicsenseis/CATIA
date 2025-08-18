===== SYSTEM =====

Eres un experto analista ejecutivo especializado en completar análisis de NPS comprehensivos.

⚠️ **CRÍTICO - NO INVENTES DATOS:**
Si hay algún dato que te falta, NO lo supongas ni inventes. En su lugar, indica claramente que ese dato específico no está disponible. Por ejemplo: "El análisis diario para Economy LH no está disponible" o "Los datos de rutas para el día 25 no están incluidos en el análisis".

⚠️ **IMPORTANTE - SI HAY DATOS DIARIOS, ÚSALOS:**
Si se te proporciona análisis diario en la sección "ANÁLISIS DIARIO SINGLE", DEBES usarlo e integrarlo en el resumen. NO digas que "no está disponible" si los datos están presentes en el input.

⚠️ **FORMATO DE NÚMEROS - UN DECIMAL:**
Todos los números, porcentajes, métricas y valores NPS deben mostrarse con exactamente UN decimal. Por ejemplo: 19.8 (no 19.75), -4.4 (no -4.39), 93.5% (no 93.53%), etc.

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
[{'period': 1, 'date_range': '2025-08-08 to 2025-08-14', 'ai_interpretation': '# 📈 SÍNTESIS EJECUTIVA\n\nDurante la semana del 8 al 14 de agosto de 2025, Iberia experimentó un deterioro generalizado del NPS causado por una crisis operativa meteorológica sistémica que afectó principalmente la puntualidad y los procesos de embarque. El NPS global cayó 4.38 puntos, pasando de 19.75 a 15.36, impulsado por eventos externos críticos como el cierre del aeropuerto de México por inundaciones y ceniza volcánica afectando la ruta NRT-MAD. Esta crisis se manifestó de manera diferencial según el nivel de servicio: Long Haul sufrió el mayor impacto con una caída de 8.35 puntos (de 14.33 a 5.98), mientras que Short Haul mostró mayor resistencia con un deterioro de 2.76 puntos (de 22.22 a 19.46). La evidencia operativa confirma esta causa con un aumento del 34% en mishandling de equipaje, incremento del 9.5% en retrasos y deterioro en métricas de puntualidad, validando perfectamente los drivers SHAP negativos identificados en punctuality (-2.467) y boarding (-1.034).\n\nLas rutas más afectadas se concentraron geográficamente en corredores Europa-Madrid y Latinoamérica-Madrid, con casos críticos como CDG-MAD (-40.0 puntos), FRA-MAD (-71.2 puntos), GIG-MAD (-15.7 puntos) y MAD-MEX (-23.0 puntos), todas vinculadas directamente a los incidentes meteorológicos y sus efectos cascada. Los grupos de clientes más reactivos fueron los pasajeros de Economy Long Haul, especialmente en rutas sudamericanas y centroamericanas, mientras que paradójicamente Business Long Haul demostró inmunidad operativa al convertir la crisis en mejora de experiencia gracias a servicios premium compensatorios.\n\n**ECONOMY SH: Crisis Operativa Europea con Compensación Doméstica**\nLa cabina Economy de Short Haul registró un NPS de 19.07 durante la semana del 8-14 de agosto, con un deterioro de 3.20 puntos respecto a la semana anterior. La causa principal fue una crisis operativa concentrada en rutas europeas principales, evidenciada por el aumento del 21.2% en retrasos (de 85 a 103 incidentes) que generó drivers SHAP negativos críticos en punctuality (-2.864) y boarding (-1.381). Esta caída se reflejó especialmente en rutas como BLQ-MAD (NPS -25.0, deterioro -86.4 puntos), FRA-MAD (NPS -25.0, deterioro -71.2 puntos) y CMN-MAD (NPS -50.0, deterioro -70.0 puntos), mientras que las rutas domésticas españolas actuaron como factor compensatorio con mejoras significativas en LCG-MAD (+32.8 puntos) y BCN-MAD (+23.9 puntos). Los perfiles más reactivos incluyen viajeros en rutas Europa Central y Mediterráneo, mostrando extrema sensibilidad a problemas de puntualidad con scores CSAT de 0.0-0.5.\n\n**BUSINESS SH: Divergencia Extrema por Compañía**\nEl segmento Business de Short Haul mostró una divergencia operativa extrema entre compañías, con IB registrando un NPS de 35.26 (mejora de 7.65 puntos) mientras YW colapsó a 1.16 (deterioro de 10.89 puntos) versus la semana anterior. Esta evolución se explica principalmente por la gestión diferencial de la misma crisis operativa: IB capitalizó la reducción del 28.1% en cancelaciones generando un driver SHAP positivo en journey preparation (+3.701), mientras YW sufrió fallos simultáneos en servicios críticos con drivers negativos en food & beverage (-1.921) y journey preparation (-1.893). El impacto fue especialmente visible en las mismas 24 rutas afectadas con hub Madrid como epicentro, donde IB optimizó la experiencia y YW experimentó colapso sistémico, evidenciando que los clientes Business Short Haul presentan extrema sensibilidad diferencial según la gestión operativa específica de cada compañía.\n\n**ECONOMY LH: Colapso Severo por Vulnerabilidad Intercontinental**\nLa cabina Economy de Long Haul experimentó el mayor deterioro de toda la red, registrando un NPS de 1.59 durante el período analizado con una caída severa de 11.15 puntos respecto a la semana anterior. La causa principal fue la crisis operativa meteorológica multifactorial que impactó desproporcionadamente este segmento debido a su exposición intercontinental, evidenciada por el driver SHAP punctuality más negativo de toda la red (-4.058) y validada por el aumento del 34% en mishandling y deterioro del 4.8% en puntualidad. Esta caída se reflejó especialmente en rutas como JFK-MAD (NPS -7.7, deterioro -31.7 puntos), MAD-MEX (NPS 28.6, deterioro -23.0 puntos) y LIM-MAD (NPS 0.0, deterioro -21.5 puntos), mientras que los perfiles más reactivos incluyen viajeros long-haul con alta sensibilidad a disrupciones sistémicas, especialmente aquellos con origen/destino Latinoamérica que representaron el 61.5% de la exposición geográfica.\n\n**BUSINESS LH: Inmunidad Operativa Paradójica**\nLa cabina Business de Long Haul demostró una paradoja operativa excepcional, registrando un NPS de 28.66 con una mejora de 7.12 puntos vs la semana anterior, a pesar de enfrentar la misma crisis operativa severa que afectó al resto de segmentos. Los drivers principales fueron journey preparation support (+3.330 SHAP), check-in (+2.510 SHAP) e IB Plus loyalty program (+1.616 SHAP), que compensaron completamente el deterioro operativo real del 34% en mishandling y 4.8% en puntualidad. Esta inmunidad operativa impactó las mismas rutas críticas donde otros segmentos colapsaron, evidenciando que los clientes Business Long Haul priorizan servicios premium sobre eficiencia operativa, con la única excepción del deterioro en food & beverage (-4.038 SHAP) como factor crítico de insatisfacción en la propuesta premium.\n\n**PREMIUM LH: Resistencia Moderada con Deterioro Controlado**\nEl segmento Premium de Long Haul registró un NPS de 20.62 durante la semana analizada con un deterioro controlado de 1.60 puntos vs la semana anterior. Las causas dominantes fueron punctuality (-2.225 SHAP), journey preparation support (-1.903 SHAP) y arrivals experience (-1.748 SHAP), todas vinculadas directamente a la crisis operativa meteorológica que incrementó los incidentes en 22.4% y el mishandling en 34%. Esta resistencia moderada fue especialmente evidente en las 23 rutas críticas afectadas, incluyendo corredores México-Europa y rutas Pacífico impactadas por ceniza volcánica, donde los clientes Premium mostraron mayor tolerancia que Economy pero menor inmunidad que Business, posicionándose como segmento intermedio en la progresión lógica de reactividad según nivel de servicio.'}]

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
11. **FORMATO DE NÚMEROS**: Todos los números, porcentajes, métricas y valores NPS deben mostrarse con exactamente UN decimal (ej: 19.8, -4.4, 93.5%)