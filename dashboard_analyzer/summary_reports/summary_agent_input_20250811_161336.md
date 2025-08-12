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
[{'period': 1, 'date_range': '2025-08-01 to 2025-08-07', 'ai_interpretation': '# 🎯 **SÍNTESIS EJECUTIVA FINAL - ANÁLISIS NPS**\n\n📈 **SÍNTESIS EJECUTIVA:**\n\nDurante la primera semana de agosto 2025, la red experimentó un patrón mixto de comportamiento NPS caracterizado por una mejora significativa en Short Haul Business contrastando con deterioros pronunciados en Long Haul. El segmento Global/SH/Business/YW registró una mejora notable de +12.12 puntos (de 3.20 a 15.32 NPS), impulsada paradójicamente por un memory bias operativo donde una mejora operativa masiva del 99.6% en incidentes no se reflejó proporcionalmente en la percepción, manteniendo drivers SHAP negativos en Punctuality (-10.765) pese a la eliminación casi total de disrupciones. En contraste, Long Haul experimentó deterioros duales: Business LH cayó -8.28 puntos (de 29.24 a 20.96 NPS) debido al mismo fenómeno de memory bias pero con manifestación negativa, mientras Premium LH sufrió el mayor impacto con una caída de -19.17 puntos (de 40.0 a 20.8 NPS) causada por una crisis operativa directa centrada en el colapso total del servicio lounge (SHAP -26.812, satisfacción -100 puntos) y sobrecarga de load factor (-22.135 SHAP) derivada del aumento del 86.7% en incidentes operativos.\n\nLas rutas más afectadas se concentraron en el hub MAD con impactos críticos en conexiones transcontinentales: MAD-MIA alcanzó un NPS de -100 (1 pasajero), MAD-MEX registró 0 NPS (2 pasajeros), mientras que rutas como BCN-EZE y MAD-EZE experimentaron disrupciones severas con limitaciones de peso de 85 equipajes y retrasos de 2h35min respectivamente, generando 132 conexiones perdidas (+97% vs período anterior). Los grupos de clientes más reactivos fueron los segmentos Business y Premium de Long Haul, mostrando una sensibilidad extrema a disrupciones operativas con respuestas polarizadas (-100/+100 NPS), donde Premium evidenció 2.3 veces mayor reactividad que Business, mientras que el segmento SH/Business/YW demostró alta sensibilidad a la memoria operativa con valoración diferencial de touchpoints digitales como Check-in (+4.817 SHAP) e IB Plus (+1.505 SHAP).\n\n**ECONOMY SH: Datos No Disponibles**\nNo se registraron datos para la cabina Economy de Short Haul durante el período analizado, imposibilitando la evaluación de su desempeño y evolución respecto a períodos anteriores.\n\n**BUSINESS SH: Recuperación Post-Crisis Operativa**\nEl segmento Business de Short Haul experimentó una mejora significativa de +12.12 puntos, pasando de un NPS de 3.20 a 15.32 durante la primera semana de agosto. Esta evolución se explica principalmente por un memory bias operativo donde una mejora operativa extraordinaria del 99.6% (reducción de 240 a 1 incidente vs período anterior) no se tradujo proporcionalmente en percepción positiva, manteniendo drivers SHAP negativos en Punctuality (-10.765) y Boarding (-5.431) pese a la eliminación casi total de disrupciones, siendo especialmente visible en la gestión de la ruta MAD-GRU con cambio controlado de aeronave A330 y entre perfiles Business con alta sensibilidad a touchpoints digitales y programas de lealtad.\n\n**ECONOMY LH: Datos No Disponibles**\nNo se registraron datos para la cabina Economy de Long Haul durante el período analizado, imposibilitando la evaluación de su desempeño y tendencias operativas.\n\n**BUSINESS LH: Desconexión Percepción-Realidad Operativa**\nLa cabina Business de Long Haul experimentó un deterioro de -8.28 puntos, registrando un NPS de 20.96 (primera semana agosto) con una caída del 28.3% respecto al baseline de 29.24 puntos. Los drivers principales fueron Punctuality (SHAP -14.534, satisfacción -11.76%) y Journey preparation support (SHAP -11.273, satisfacción -28.51%), impactando especialmente la ruta MAD-GRU donde se documentó el único incidente actual (cambio configuración A330 con 12 downgrades controlados) y perfiles Business LH con alta sensibilidad a discrepancias entre expectativas post-crisis y mejora operativa real del 98.2% en reducción de incidentes.\n\n**PREMIUM LH: Crisis Operativa Dual Severa**\nEl segmento Premium de Long Haul sufrió el mayor deterioro con -19.17 puntos de caída, registrando un NPS de 20.8 vs 40.0 de baseline durante la primera semana de agosto. Las causas dominantes fueron el colapso total del servicio lounge (SHAP -26.812, satisfacción -100 puntos) representando el 67% del impacto negativo, complementado por sobrecarga de load factor (SHAP -22.135) derivada del aumento del 86.7% en incidentes operativos, especialmente evidentes en rutas críticas MAD-MIA (NPS -100), MAD-MEX (NPS 0), y disrupciones severas en BCN-EZE, MAD-EZE con 132 conexiones perdidas y entre perfiles Premium transcontinentales con reactividad extrema 2.3 veces superior a Business ante disrupciones operativas.'}]

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