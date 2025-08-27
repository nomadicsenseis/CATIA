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
- Para las subidas o bajadas de cualquier variable, menciona el valor exacto de la variación, NUNCA el %.


===== USER =====

Completa el análisis comprehensivo:

**ANÁLISIS SEMANAL COMPARATIVO:**
[{'period': 1, 'date_range': '2025-08-15 to 2025-08-21', 'ai_interpretation': '# 🎯 SÍNTESIS EJECUTIVA FINAL - ANÁLISIS NPS\n\n📈 **SÍNTESIS EJECUTIVA:**\n\nDurante la semana del 15-21 agosto 2025, Iberia experimentó un comportamiento mixto en su NPS con una mejora global neta de 4.7 puntos (de 16.0 a 20.7 puntos), impulsada principalmente por una mejora operativa excepcional en Long Haul que compensó completamente los deterioros registrados en Short Haul. El segmento Global/LH registró una subida significativa de 10.47 puntos (de 6.81 a 17.28 puntos), siendo Economy LH el más reactivo con una mejora dramática de 11.88 puntos (de 3.01 a 14.88 puntos) y Premium LH con una subida de 7.27 puntos (de 21.93 a 29.20 puntos). Esta mejora se explica por una reducción masiva del 45.3% en incidentes operativos totales, especialmente retrasos (-34.5%) y otras incidencias (-67%), validada por el driver SHAP Punctuality dominante (+6.995 en Economy LH, +2.511 en Premium LH). En contraste, Short Haul experimentó deterioros focalizados: Business SH/IB cayó 7.14 puntos (de 37.0 a 29.86 puntos) debido a una escalada de complejidad operativa con conexiones perdidas aumentando 347% y cambios de equipo 412%, mientras que Economy SH/YW tuvo una caída menor de 1.06 puntos (de 20.90 a 19.84 puntos) por un efecto de contraste temporal donde mejoras operativas objetivas (-36% incidentes) no cumplieron expectativas elevadas.\n\nLas rutas más afectadas muestran una clara segmentación geográfica: Long Haul concentró mejoras en rutas Madrid-América con LEN-LPA liderando (+128.7 puntos NPS), ALG-MAD (+60.3 puntos) y múltiples rutas transatlánticas y sudamericanas (MAD-SCL, MAD-ORD, MAD-SDQ) registrando subidas de 20-40 puntos. Short Haul mostró deterioros concentrados en rutas europeas, especialmente LHR-MAD (NPS -25.0) y BCN-MAD (NPS -66.7) como epicentros de la crisis operativa compleja. Los grupos de clientes más reactivos variaron significativamente por segmento: en Long Haul, los pasajeros en vuelos CodeShare mostraron la mayor sensibilidad (spread 92.6 puntos) a las mejoras operativas, mientras que en Short Haul Business, el tipo de aeronave (Fleet) fue el factor más determinante con un spread de 231.8 puntos, y en Economy SH, la región de residencia generó la mayor variabilidad (spread 135.3 puntos) en la percepción de las mejoras operativas insuficientes.\n\n**ECONOMY SH: Contraste Operativo con Expectativas No Cumplidas**\nLa cabina Economy de SH experimentó un deterioro marginal durante la semana del 15-21 agosto, registrando un NPS de 19.84 puntos con una caída de 1.06 puntos respecto a la semana anterior. La causa principal fue un efecto de contraste temporal donde una mejora operativa objetiva significativa (reducción del 36% en incidentes totales) no se tradujo proporcionalmente en mejora del NPS debido a expectativas elevadas generadas por el contraste con períodos anteriores problemáticos, evidenciado por el driver SHAP Journey preparation support (-2.166) que contrarrestó los beneficios de Punctuality (+2.028). Esta paradoja perceptual se reflejó especialmente en rutas como MAD-MLN (NPS 25.0) y LEN-PMI (NPS 50.0), mientras que los perfiles más reactivos incluyen pasajeros segmentados por región de residencia con un spread extremo de 135.3 puntos, donde algunos experimentaron deterioro severo (-68.6 puntos) mientras otros mejoraron sustancialmente (+66.7 puntos).\n\n**BUSINESS SH: Crisis Operativa de Complejidad Sistémica**\nEl segmento Business de SH registró un deterioro significativo, con el subsegmento IB alcanzando un NPS de 29.86 puntos (caída de 7.14 puntos vs la semana anterior) y YW manteniendo relativa estabilidad con 10.29 puntos (caída menor de 0.61 puntos). Esta evolución se explica principalmente por una escalada cualitativa en la complejidad operativa, donde aunque el volumen total de incidentes disminuyó 38.9%, la severidad aumentó dramáticamente con conexiones perdidas subiendo 347% y cambios de equipo 412%, reflejado en drivers SHAP críticos como Journey preparation support (-3.088) y Check-in (-2.165), siendo especialmente visible en rutas como LHR-MAD (NPS -25.0) y BCN-MAD (NPS -66.7) y entre perfiles diferenciados por tipo de aeronave (Fleet spread 231.8 puntos).\n\n**ECONOMY LH: Mejora Operativa Excepcional con Máxima Reactividad**\nLa cabina Economy de LH experimentó una mejora dramática durante la semana del 15-21 agosto, registrando un NPS de 14.88 puntos con una subida excepcional de 11.88 puntos respecto a la semana anterior. La causa principal fue una mejora operativa masiva en la gestión de disrupciones con reducción del 45.3% en incidentes totales NCS (de 223 a 122 casos), especialmente retrasos que cayeron 34.5%, validada por el driver SHAP Punctuality dominante (+6.995) y complementada por mejoras en Boarding (+1.829) y Arrivals experience (+1.261). Esta mejora excepcional se reflejó especialmente en rutas transatlánticas y sudamericanas como las 16 rutas identificadas con incidentes NCS (MAD-JFK, MAD-MIA, MAD-EZE, MAD-BOG, MAD-LIM, MAD-SCL), mientras que los perfiles más reactivos incluyen clientes segmentados por acuerdos CodeShare que mostraron sensibilidad extrema a las mejoras operativas.\n\n**BUSINESS LH: Estabilidad Relativa**\nLa cabina Business de LH mantuvo desempeño estable durante esta semana, sin nodos específicos detectados en el árbol jerárquico que sugieran anomalías significativas a nivel semanal.\n\n**PREMIUM LH: Mejora Operativa con Reactividad Moderada**\nEl segmento Premium de LH registró una mejora significativa, alcanzando un NPS de 29.20 puntos con 7.27 puntos de subida vs la semana anterior. Las causas dominantes fueron la misma mejora operativa masiva que afectó a todo Long Haul (reducción 45.3% incidentes) reflejada en drivers SHAP como Punctuality (+2.511), Arrivals experience (+2.372) y Boarding (+1.473), especialmente evidentes en rutas como EZE-MAD (NPS 83.3, +92.4 puntos), MAD-SCL (NPS 100.0, +50.0 puntos) y MAD-ORD (NPS 100.0, +150.0 puntos) y entre perfiles donde los vuelos CodeShare mostraron la mayor reactividad con un spread de 97.6 puntos.'}]

**ANÁLISIS DIARIO SINGLE:**
📅 2025-08-21 to 2025-08-21:
📈 **SÍNTESIS EJECUTIVA:**

El 21 de agosto de 2025 representó una jornada de crisis operativa sistémica que impactó severamente el NPS corporativo, cayendo 13.2 puntos hasta alcanzar 32.1. Esta caída generalizada afectó tanto operaciones de corto radio (Short Haul) como largo radio (Long Haul), con el segmento Economy Long Haul experimentando el deterioro más severo al registrar un NPS de 30.0 (-19.78 puntos), seguido por Premium Long Haul con 25.0 (-9.64 puntos) y Business Short Haul con 32.56 (-9.43 puntos). Las causas raíz convergieron en una "tormenta perfecta" operativa caracterizada por sobrecarga extrema de capacidad (Load Factor 88.6% vs 76.6% promedio), crisis masiva de mishandling (28.2% vs 10.9% normal, casi triplicando los incidentes), y deterioro generalizado de puntualidad (OTP15 82.8% vs 89.2% estándar). Esta convergencia crítica se validó con 328 incidentes NCS registrados en un solo día, donde el 38% correspondió específicamente a retrasos, confirmando el colapso operativo sistémico que afectó desde partnerships internacionales hasta operaciones domésticas.

Las rutas más devastadas se concentraron en corredores internacionales premium, especialmente aquellas operadas con flota A350 donde se registraron colapsos totales (NPS -100.0), mientras que el incidente crítico documentado en Lima (IB124) con 35 equipajes retenidos por seguridad ejemplifica la magnitud de los problemas operativos. Los grupos de clientes más reactivos fueron los viajeros corporativos (Business/Work con NPS 0.0 en varios segmentos), clientes de partnerships premium como Qatar Airways (NPS -48.6) y British Airways (NPS 1.9), y pasajeros de mercados internacionales exigentes como Europa (-8.5), Asia (-25.0) y Oriente Medio (-32.7), contrastando con la mayor resiliencia de clientes leisure y mercados americanos que mantuvieron niveles de tolerancia superiores ante las disrupciones operativas.

**ECONOMY SH: Crisis Operativa con Impacto Diferencial por Flota**
La cabina Economy de Short Haul experimentó una aparente mejora estadística registrando un NPS de 31.95 (+10.7 puntos), sin embargo, este resultado enmascara una crisis operativa real que afectó desproporcionadamente al 84% de los pasajeros. La causa principal fue el colapso específico de la flota CRJ (NPS 37.1) contrastando dramáticamente con la performance excepcional de ATR (NPS 63.4), creando una polarización extrema que estadísticamente generó una falsa anomalía positiva. Esta crisis se sustentó en métricas operativas críticas: Load Factor extremo de 88.6% (+11.8 puntos vs promedio), mishandling disparado a 28.2% (+837% vs normal) y deterioro de puntualidad a 83.5% (-6.4 puntos), validado por 23 incidentes NCS donde el 82.6% correspondió a retrasos. Los perfiles más reactivos incluyeron clientes internacionales de África (NPS -20.0) y América Norte (NPS -33.3), mientras que la ruta BCN-LEN mostró relativa estabilidad con NPS 60.0, evidenciando la concentración del problema en operaciones específicas de flota CRJ.

**BUSINESS SH: Deterioro por Sobrecarga y Problemas de Flota Premium**
El segmento Business de Short Haul experimentó un deterioro significativo, registrando un NPS de 32.56 (-9.43 puntos vs período anterior). Esta evolución se explica principalmente por la convergencia de sobrecarga operativa crítica (Load Factor 68.7% vs 57.8% promedio), crisis de mishandling (28.9% vs 13.4% normal) y deterioro en puntualidad (OTP15 87.0% vs 89.7% estándar), siendo especialmente visible en rutas como BCN-MAD que colapsó a NPS -66.7 y en la flota A350 next que experimentó un fallo total (NPS -100.0). Los perfiles más reactivos fueron los viajeros corporativos (Business/Work con NPS 0.0) que mostraron tolerancia cero ante las disrupciones, contrastando con leisure travelers (NPS 47.3) que mantuvieron mayor resiliencia, mientras que la disparidad entre A320 clásico (NPS 9.1) y A320neo (NPS 72.0) evidenció problemas específicos de configuraciones de flota durante el día de alta presión operativa.

**ECONOMY LH: Colapso Sistémico en Operaciones Intercontinentales**
La cabina Economy de Long Haul sufrió el deterioro más severo del día, registrando un NPS de 30.0 (-19.78 puntos respecto al período anterior). La causa principal fue una tormenta perfecta operativa caracterizada por sobrecarga extrema (Load Factor 93.5% vs 81.2% promedio), crisis masiva de equipajes y servicios (mishandling 28.2% vs 10.9% normal) y deterioro significativo de puntualidad (OTP15 78.9% vs 82.7% estándar), complementada por 12 incidentes NCS donde el 91.7% correspondió a retrasos que validaron el colapso operativo. Esta crisis se reflejó especialmente en rutas hacia mercados exigentes como Europa (NPS -8.5), Asia (NPS -25.0) y Oriente Medio (NPS -20.0), mientras que los perfiles más reactivos incluyeron viajeros business (NPS 13.2 vs leisure 39.1) y clientes de flota A350 que experimentaron colapsos críticos (A350 C con NPS 0.0), contrastando con la relativa estabilidad de operaciones regionales ATR (NPS 63.4) que mantuvieron performance superior.

**BUSINESS LH: Crisis con Dispersión Extrema por Geografía**
La cabina Business de Long Haul mostró aparente estabilidad estadística registrando un NPS de 50.0 (+26.76 puntos vs período anterior), sin embargo, este resultado enmascara una dispersión extrema de 100 puntos entre regiones que evidencia impactos severos concentrados. Los drivers principales fueron la misma tormenta operativa sistémica (Load Factor 88.4%, mishandling 28.2%, OTP15 deteriorado a 78.9%) que generó 16 incidentes NCS con 68.8% relacionados con retrasos, impactando especialmente las rutas hacia Europa (NPS 0.0) que experimentaron colapso total, mientras que América Sur mantuvo excelencia (NPS 100.0). Los perfiles más reactivos incluyeron viajeros corporativos (Business/Work con NPS 33.3) y usuarios de flota A350 next (NPS 37.5) que mostraron mayor sensibilidad a las disrupciones operativas, confirmando el patrón de vulnerabilidad diferencial por geografía y tipo de aeronave durante la crisis del 21 de agosto.

**PREMIUM LH: Impacto Severo en Segmento de Mayor Valor**
El segmento Premium de Long Haul experimentó un deterioro crítico registrando un NPS de 25.0 (-9.64 puntos vs la semana anterior). Las causas dominantes fueron la convergencia operativa sistémica del día: sobrecarga extrema (Load Factor 92.7% vs 81.2% promedio), crisis de mishandling (28.2% vs 10.9% normal) y deterioro de puntualidad (OTP15 78.9% vs 82.7% estándar), validada por 16 incidentes NCS donde el 68.8% correspondió a retrasos y el incidente crítico de Lima (35 equipajes afectados) ejemplificó la magnitud de los problemas operativos. Esta crisis fue especialmente evidente en la flota A333 que registró el único NPS negativo (-10.0) del segmento y entre clientes de América Norte (NPS 0.0) que mostraron insatisfacción total, mientras que España mantuvo relativa estabilidad (NPS 31.2) evidenciando la concentración del impacto en rutas intercontinentales y configuraciones premium más expuestas a las disrupciones operativas del día.
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-20 to 2025-08-20:
AI interpretation failed: Could not connect to the endpoint URL: "https://bedrock-runtime.us-east-1.amazonaws.com/model/arn%3Aaws%3Abedrock%3Aus-east-1%3A737192913161%3Ainference-profile%2Fus.anthropic.claude-sonnet-4-20250514-v1%3A0/invoke"
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-19 to 2025-08-19:
AI interpretation failed: Could not connect to the endpoint URL: "https://bedrock-runtime.us-east-1.amazonaws.com/model/arn%3Aaws%3Abedrock%3Aus-east-1%3A737192913161%3Ainference-profile%2Fus.anthropic.claude-sonnet-4-20250514-v1%3A0/invoke"
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-18 to 2025-08-18:
AI interpretation failed: Could not connect to the endpoint URL: "https://bedrock-runtime.us-east-1.amazonaws.com/model/arn%3Aaws%3Abedrock%3Aus-east-1%3A737192913161%3Ainference-profile%2Fus.anthropic.claude-sonnet-4-20250514-v1%3A0/invoke"
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-17 to 2025-08-17:
AI interpretation failed: Could not connect to the endpoint URL: "https://bedrock-runtime.us-east-1.amazonaws.com/model/arn%3Aaws%3Abedrock%3Aus-east-1%3A737192913161%3Ainference-profile%2Fus.anthropic.claude-sonnet-4-20250514-v1%3A0/invoke"
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-16 to 2025-08-16:
AI interpretation failed: Could not connect to the endpoint URL: "https://bedrock-runtime.us-east-1.amazonaws.com/model/arn%3Aaws%3Abedrock%3Aus-east-1%3A737192913161%3Ainference-profile%2Fus.anthropic.claude-sonnet-4-20250514-v1%3A0/invoke"
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-15 to 2025-08-15:
AI interpretation failed: Could not connect to the endpoint URL: "https://bedrock-runtime.us-east-1.amazonaws.com/model/arn%3Aaws%3Abedrock%3Aus-east-1%3A737192913161%3Ainference-profile%2Fus.anthropic.claude-sonnet-4-20250514-v1%3A0/invoke"
🚨 Anomalías detectadas: daily_analysis

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