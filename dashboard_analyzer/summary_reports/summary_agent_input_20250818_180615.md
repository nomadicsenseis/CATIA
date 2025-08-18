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
📈 SÍNTESIS EJECUTIVA:

El análisis del 8 de agosto de 2025 revela un patrón diferencial significativo en la respuesta de los segmentos ante disrupciones operativas concentradas en Short Haul. Los segmentos premium experimentaron mejoras excepcionales en satisfacción: Business LH alcanzó un NPS de 48.15 puntos (mejora de +23.17 puntos vs baseline de 24.98), Premium LH registró 40.0 puntos (+22.17 puntos vs baseline de 17.83), y Business SH/YW destacó con 29.41 puntos (+23.66 puntos vs baseline de 5.75). En contraste, Economy LH mostró un deterioro a 4.12 puntos (-2.9 puntos vs baseline de 7.02), mientras que Economy SH presentó comportamientos mixtos: IB con 17.59 puntos (-0.017 puntos vs baseline de 17.61) y YW con 32.54 puntos (+11.17 puntos vs baseline de 21.37). La causa principal identificada fueron 23 incidentes operacionales críticos en Short Haul, concentrados en problemas de puntualidad (69.6%-74% del total), incluyendo 10 retrasos, 6 cancelaciones y 1 desvío, que generaron respuestas diferenciadas según el nivel de servicio y marca.

La ruta MVD-MAD fue específicamente identificada con disrupciones operativas (+50 minutos de reprogramación), mientras que los grupos de clientes más reactivos mostraron un gradiente claro: los segmentos Business y Premium de ambas marcas demostraron alta resiliencia ante disrupciones, especialmente YW que convirtió las crisis operativas en experiencias valoradas positivamente, mientras que Economy IB mostró mayor sensibilidad a los problemas de puntualidad. La gestión proactiva documentada ("Clientes informados") actuó como factor compensatorio clave que explicó por qué las mismas disrupciones operativas generaron mejoras significativas en segmentos premium.

**ECONOMY SH: Reactividad Diferencial por Marca**
La cabina Economy de Short Haul mostró comportamientos contrastantes durante el 8 de agosto, con IB registrando un NPS de 17.59 puntos (deterioro mínimo de -0.017 puntos vs baseline de 17.61) mientras YW alcanzó 32.54 puntos (mejora significativa de +11.17 puntos vs baseline de 21.37). Esta divergencia se explica por la respuesta diferencial ante 23 incidentes operacionales críticos, donde YW demostró mayor resiliencia y valoración de la gestión proactiva de crisis, mientras IB mostró sensibilidad tradicional a disrupciones de puntualidad. Los perfiles más reactivos fueron los clientes YW Economy que convirtieron la transparencia comunicativa en experiencias positivas.

**BUSINESS SH: Resiliencia Premium Confirmada**
El segmento Business de Short Haul experimentó mejoras notables, registrando un NPS general de 34.21 puntos (mejora de +8.56 puntos vs baseline de 25.65), con YW alcanzando niveles excepcionales de 29.41 puntos (+23.66 puntos vs baseline de 5.75). Esta evolución se explica por la alta resiliencia del segmento premium ante las mismas 23 disrupciones operativas que afectaron Economy, donde la gestión proactiva y comunicación transparente fueron especialmente valoradas. Los frequent flyers Business YW demostraron ser el perfil más resiliente, convirtiendo disrupciones en oportunidades de experiencia diferenciada.

**ECONOMY LH: Datos Comprometidos por Error Técnico**
La cabina Economy de Long Haul mostró aparente deterioro registrando un NPS de 4.12 puntos (-2.9 puntos vs baseline de 7.02), sin embargo, este resultado corresponde a un falso positivo generado por consulta de datos en fecha futura sin información operativa real. No se detectaron cambios genuinos en este segmento, requiriendo corrección técnica del sistema de monitoreo antes de análisis válidos.

**BUSINESS LH: Anomalía Técnica sin Base Operativa**
La cabina Business de Long Haul registró aparentemente un NPS de 48.15 puntos (+23.17 puntos vs baseline de 24.98), pero este resultado representa un artefacto técnico por datos de fecha futura sin sustento operativo real. No se identificaron drivers operativos genuinos que expliquen esta variación, manteniendo este segmento como estable hasta corrección del sistema de datos.

**PREMIUM LH: Falso Positivo por Error Sistémico**
El segmento Premium de Long Haul mostró aparente mejora con un NPS de 40.0 puntos (+22.17 puntos vs baseline de 17.83), pero esta variación corresponde a un falso positivo generado por consulta en fecha futura sin datos operativos reales. No se detectaron cambios significativos genuinos en este segmento premium, manteniendo niveles estables hasta resolución de problemas técnicos del sistema.

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