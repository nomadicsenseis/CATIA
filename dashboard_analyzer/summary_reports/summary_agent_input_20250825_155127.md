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
[{'period': 1, 'date_range': '2025-08-15 to 2025-08-21', 'ai_interpretation': '📈 SÍNTESIS EJECUTIVA:\n\nEl análisis del árbol jerárquico de NPS revela un patrón dual contrastante entre radios durante la semana del 15-21 agosto 2025. Long Haul experimentó mejoras masivas con el nodo Global/LH alcanzando un NPS de 16.05 puntos (mejora de +9.24 puntos vs período anterior), impulsado por una gestión operativa proactiva que redujo los incidentes críticos en 45.3% y fortaleció la puntualidad como driver principal (SHAP +5.564). Esta mejora se propagó consistentemente a Economy LH con NPS de 13.46 (+10.45 puntos) y Premium LH con NPS de 29.09 (+7.17 puntos). En contraste, Short Haul mostró deterioros localizados: Economy SH/YW registró NPS de 19.12 (-1.77 puntos) debido a crecimiento no sostenible con Load Factor aumentando 1.8% sin escalamiento de recursos, mientras Business SH sufrió mayor impacto con NPS de 23.93 (-3.81 puntos) por deterioro operacional sistémico evidenciado en mishandling (+16.2%) y misconex (+19.6%). El segmento Business SH/IB mostró el mayor deterioro individual con NPS de 32.31 (-4.69 puntos), concentrando problemas en journey preparation support (SHAP -2.090) y check-in (SHAP -1.760).\n\nLas rutas más afectadas reflejan esta dualidad por radio: Long Haul destacó con EZE-MAD alcanzando NPS de 83.3 (+92.4 puntos) mediante excelencia en arrivals experience que compensó deficiencias de puntualidad, mientras 16 rutas críticas de largo radio (MAD-JFK, MAD-MIA, MAD-EZE, MAD-BOG, entre otras) se beneficiaron de la gestión proactiva. En Short Haul, las rutas problemáticas se concentraron en conexiones con Madrid: BCN-MAD sufrió el mayor deterioro con NPS de -66.7 (-75.8 puntos), seguida por EAS-MAD con NPS de -33.3 (-133.3 puntos) y LHR-MAD con NPS de -25.0 (-63.7 puntos). Los grupos más reactivos mostraron progresión inversa por clase: en Long Haul, Economy fue más sensible a mejoras operacionales (+347.5% vs baseline) que Premium (+32.7%), mientras en Short Haul, Business mostró mayor vulnerabilidad a deterioros operacionales que Economy, especialmente en segmentos IB donde la marca premium amplificó las expectativas no cumplidas.\n\n**ECONOMY SH: Crecimiento No Sostenible**\nLa cabina Economy de SH experimentó un deterioro moderado durante la semana del 15-21 agosto, registrando un NPS de 19.12 (deterioro de 1.77 puntos respecto a la semana anterior). La causa principal fue el crecimiento no sostenible evidenciado por el incremento del Load Factor de 84.54% a 86.1% (+1.8%) sin escalamiento proporcional de recursos operativos, desencadenando una cascada de deterioros: mishandling aumentó 8.1%, misconex creció 3.8%, y se registraron 41 cambios de equipo vs 8 del período anterior. Esta sobrecarga se reflejó especialmente en el driver journey preparation support (SHAP -1.665) y arrivals experience (SHAP -0.664), afectando rutas críticas como MAD-CMN, MAD-DAR, MAD-SIN y MAD-DEL, mientras que los perfiles YW mostraron mayor reactividad a estos problemas operacionales, aunque mantuvieron la puntualidad como fortaleza compensatoria (SHAP +1.816).\n\n**BUSINESS SH: Deterioro Operacional Sistémico**\nEl segmento Business de SH sufrió un deterioro significativo, registrando un NPS de 23.93 (caída de 3.81 puntos vs la semana anterior). Esta evolución se explica principalmente por el deterioro operacional sistémico concentrado en hub Madrid, con punctuality como driver crítico negativo (SHAP -2.917), complementado por problemas en check-in (SHAP -0.946) y journey preparation support (SHAP -0.906). El deterioro fue especialmente severo en mishandling (+16.2%) y misconex (+19.6%), siendo especialmente visible en rutas como BCN-MAD (NPS -66.7), EAS-MAD (NPS -33.3) y LHR-MAD (NPS -25.0), donde todas las rutas con NPS negativo mostraron punctuality CSAT crítico (<1.0). Los perfiles IB fueron más reactivos con deterioro de 4.69 puntos (NPS 32.31), amplificando el impacto por mayores expectativas de servicio premium.\n\n**ECONOMY LH: Gestión Proactiva Exitosa**\nLa cabina Economy de LH experimentó una mejora excepcional durante la semana del 15-21 agosto, registrando un NPS de 13.46 (mejora masiva de 10.45 puntos respecto a la semana anterior, +347.5% vs baseline). La causa principal fue la implementación de gestión operativa proactiva que redujo los incidentes críticos NCS en 45.3% (de 223 a 122 casos), con punctuality emergiendo como driver dominante (SHAP +6.164) pese al deterioro en métricas estándar como OTP15 (-3.8%). Esta mejora se complementó por la reducción dramática de retrasos (-34.5%) y desvíos (-87.5%), reflejándose especialmente en la gestión efectiva de 16 rutas críticas incluyendo MAD-JFK, MAD-MIA, MAD-EZE y MAD-BOG, mientras que los perfiles Economy mostraron la mayor reactividad a las mejoras operacionales, beneficiándose desproporcionalmente de la ausencia de disrupciones mayores vs mejoras marginales en puntualidad estándar.\n\n**BUSINESS LH: Fortaleza Operacional Consolidada**\nLa cabina Business de LH mantuvo desempeño sólido, registrando un NPS implícito en el nodo Global/LH de 16.05 (mejora de 9.24 puntos vs período anterior). Los drivers principales fueron punctuality (SHAP +5.564) representando 59.2% del impacto total, boarding (SHAP +1.533) y arrivals experience (SHAP +1.034), impactando especialmente las 16 rutas de largo radio donde la gestión proactiva de reubicaciones y comunicación IBConecta sistemática generaron mejoras consistentes. Los perfiles Business Long Haul mostraron sensibilidad alta pero menor que Economy a las mejoras operacionales, beneficiándose del equilibrio entre excelencia operacional y factores de producto.\n\n**PREMIUM LH: Compensación Producto vs Operaciones**\nEl segmento Premium de LH logró una mejora significativa, registrando un NPS de 29.09 (mejora de 7.17 puntos vs la semana anterior). Las causas dominantes fueron la compensación exitosa de factores de producto sobre problemas operacionales, con punctuality (SHAP +2.517) liderando pese al deterioro técnico en OTP15 (-3.8%), arrivals experience (SHAP +2.091) y boarding (SHAP +1.326) actuando como amortiguadores efectivos. Esta estrategia fue especialmente evidente en rutas como EZE-MAD (NPS 83.3, arrivals experience 100%) que compensó punctuality deficiente (0.0%), mientras MAD-MIA requiere intervención crítica (NPS -28.6). Los perfiles Premium mostraron menor reactividad relativa (+32.7% vs baseline) pero mayor resistencia a problemas operacionales mediante la excelencia en experiencia de producto.'}]

**ANÁLISIS DIARIO SINGLE:**
📅 2025-08-21 to 2025-08-21:
# 🎯 SÍNTESIS EJECUTIVA FINAL - ANÁLISIS NPS

📈 **SÍNTESIS EJECUTIVA:**

El análisis del período 21 de agosto de 2025 revela una **crisis sistémica crítica en la capacidad de medición y gestión del NPS** que impide determinar valores exactos, tendencias o anomalías en la satisfacción del cliente. La causa raíz identificada es un **colapso arquitectónico del ecosistema de customer intelligence** que afecta uniformemente todos los segmentos operativos - Global, Long Haul y Short Haul - eliminando la visibilidad sobre experiencia del cliente. Este fallo sistémico se manifiesta a través del error crítico en PBIDataCollector (afectando 100% de la segmentación de clientes), la ausencia total de feedback de clientes (0 verbatims capturados en todos los segmentos), y la desconexión completa entre incidentes operativos y métricas de satisfacción, creando una situación de "ceguera organizacional" donde 328 incidentes operativos detectados (38.1% retrasos dominantes) no pueden correlacionarse con su impacto real en NPS.

La evidencia operativa disponible sugiere que los **retrasos representan el principal riesgo no cuantificado para la satisfacción del cliente**, con concentraciones críticas del 82.6% de incidentes en Short Haul Business, mientras que la **ausencia de datos de rutas específicas** impide identificar destinos prioritarios para intervención. Los **grupos de clientes más vulnerables** incluyen potencialmente Premium Long Haul (con 0% de capacidad analítica residual) y Business Short Haul (donde se concentran los problemas de puntualidad), aunque la **falta de segmentación funcional** impide validar esta hipótesis con datos concretos de NPS.

**ECONOMY SH: Estabilidad Operativa Sin Visibilidad de Satisfacción**
La cabina Economy de Short Haul mantuvo operaciones durante la semana del 21 de agosto, aunque la **ausencia completa de datos NPS** impide determinar valores de satisfacción o variaciones respecto a períodos anteriores. No se detectaron cambios significativos en la capacidad de monitoreo, manteniendo el mismo nivel crítico de limitación analítica (15% de funcionalidad) que caracteriza todo el ecosistema. La evidencia operativa disponible sugiere exposición a la concentración de retrasos identificada (82.6% de incidentes), pero sin capacidad de validar el impacto real en experiencia del cliente debido al fallo sistémico de herramientas de feedback.

**BUSINESS SH: Concentración de Riesgo Operativo No Cuantificado**
El segmento Business de Short Haul presenta la **mayor concentración de incidentes operativos** identificados, con 82.6% relacionados con retrasos, aunque la **ausencia de datos NPS** impide cuantificar el impacto en satisfacción del cliente. Esta evolución operativa requiere seguimiento urgente dado que los problemas de puntualidad típicamente afectan más severamente a clientes Business, pero el fallo crítico del sistema PBIDataCollector elimina la capacidad de segmentación y correlación con métricas de experiencia, creando un punto ciego crítico en la gestión de este segmento de alto valor.

**ECONOMY LH: Capacidad Analítica Residual Limitada**
La cabina Economy de Long Haul mantuvo la **mayor capacidad analítica residual** (20%) dentro del contexto de crisis sistémica, aunque esto sigue siendo **insuficiente para generar datos NPS confiables** o identificar variaciones respecto a períodos anteriores. No se detectaron cambios significativos en los patrones de falla técnica, manteniendo niveles consistentes de limitación en el acceso a métricas de satisfacción del cliente, con el mismo error crítico PBIDataCollector y ausencia total de verbatims que caracteriza todos los segmentos analizados.

**BUSINESS LH: Vulnerabilidad Intermedia Sin Medición**
La cabina Business de Long Haul registró una **capacidad analítica del 13%** durante el período analizado, reflejando el mismo patrón de degradación sistémica que afecta toda la organización. Los drivers principales fueron las **fallas técnicas universales** (error PBIDataCollector, ausencia de feedback de clientes, inconsistencias entre sistemas), impidiendo tanto la medición de NPS como la identificación de rutas específicas o perfiles de clientes más reactivos, manteniendo la organización en estado de ceguera operacional respecto a la satisfacción en este segmento crítico.

**PREMIUM LH: Máxima Vulnerabilidad Sistémica**
El segmento Premium de Long Haul experimentó la **pérdida total de capacidad analítica** (0% funcional) durante la semana del 21 de agosto, representando el mayor nivel de vulnerabilidad dentro del ecosistema comprometido. Las causas dominantes fueron el **colapso completo de todas las herramientas de análisis** (5 de 5 herramientas no funcionales), eliminando completamente la visibilidad sobre NPS, tendencias de satisfacción, o capacidad de respuesta a problemas de experiencia del cliente en el segmento de mayor valor, creando un riesgo estratégico máximo para la retención y lealtad de clientes Premium.
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-20 to 2025-08-20:
📈 SÍNTESIS EJECUTIVA:

El análisis del período 2025-08-20 revela una **crisis sistémica de capacidad analítica** que ha imposibilitado la medición efectiva del NPS y la detección de anomalías en todos los segmentos de la compañía. Esta situación crítica se debe a **fallas técnicas generalizadas en el ecosistema de herramientas de análisis**, donde 4 de 5 sistemas presentan fallos severos que han generado una ceguera operacional total. La causa principal identificada es la **pérdida de funcionalidad del 80% de las herramientas analíticas**, incluyendo el motor de procesamiento de verbatims (595+ comentarios sin procesar), el sistema de análisis de rutas (sin datos de NPS por destino) y las capacidades de segmentación de clientes (error técnico crítico). Esta crisis afecta uniformemente a **todos los nodos del árbol jerárquico** - Global, Short Haul, Long Haul y todas sus subcategorías - impidiendo la correlación entre los 281 incidentes operativos detectados (principalmente retrasos con 33% del total) y su impacto real en la satisfacción del cliente.

Durante este período, se identificaron **problemas operativos críticos no correlacionados con NPS** debido a las limitaciones del sistema, incluyendo 92 retrasos como principal disruptor, 34 cancelaciones y problemas específicos como 47 equipajes sin cargar en el vuelo IB424/BCN. Sin embargo, la **ausencia de datos NPS confiables** impide determinar qué rutas fueron más afectadas en términos de satisfacción del cliente, y los **grupos de clientes más reactivos no pueden identificarse** debido a la falla completa del sistema de perfiles de cliente y el motor de análisis de sentimientos.

**ECONOMY SH: Estabilidad Aparente con Visibilidad Limitada**
La cabina Economy de Short Haul mantuvo desempeño aparentemente estable durante el período analizado, aunque esta evaluación está severamente limitada por la crisis del sistema analítico que impide acceder a datos NPS confiables. La única información disponible proviene de 22 incidentes operativos donde los retrasos representaron el 64%, complementados por problemas críticos de equipaje (47 maletas en BCN) y cancelaciones (27%). Aunque se detectaron 230 comentarios de clientes en este segmento, la falla del motor de procesamiento de texto impide analizar su contenido y sentimiento, generando una brecha crítica entre la actividad operativa visible y la satisfacción real del cliente.

**BUSINESS SH: Estabilidad Operativa con Análisis Comprometido**
El segmento Business de Short Haul mantuvo desempeño estable a nivel operativo, registrando los mismos 22 incidentes que Economy SH con idéntica distribución (64% retrasos, 27% cancelaciones), lo que sugiere que ambas cabinas experimentaron exposición uniforme a disrupciones operativas. Sin embargo, la evaluación de satisfacción está completamente comprometida debido a las fallas sistémicas en las herramientas de análisis, particularmente la incapacidad de procesar los 34 verbatims detectados en este segmento y la ausencia total de datos de NPS por rutas o perfiles de cliente.

**ECONOMY LH: Comportamiento Estable con Limitaciones Analíticas**
La cabina Economy de Long Haul mantuvo desempeño estable durante el período, con 10 incidentes operativos donde los retrasos dominaron con 60% del total, seguidos por cancelaciones (20%). Aunque se registraron 161 comentarios de clientes, representando un nivel medio de engagement, el sistema de análisis de sentimientos permanece inoperativo, impidiendo correlacionar estos feedback con la experiencia real del cliente. La estabilidad aparente debe interpretarse con cautela dado que las herramientas de medición de satisfacción están severamente comprometidas.

**BUSINESS LH: Estabilidad con Alta Actividad de Feedback**
La cabina Business de Long Haul mantuvo desempeño estable operativamente, experimentando los mismos 10 incidentes que Economy LH con distribución idéntica (60% retrasos). Notablemente, este segmento generó el mayor volumen de feedback con 595 comentarios detectados, sugiriendo alta reactividad del segmento premium, aunque la falla completa del motor de procesamiento de verbatims impide analizar el contenido y sentimiento de estos comentarios. Esta alta actividad de feedback sin capacidad de análisis representa una pérdida crítica de intelligence sobre el segmento más valioso.

**PREMIUM LH: Estabilidad con Menor Reactividad**
El segmento Premium de Long Haul mantuvo desempeño estable con exposición a los mismos 10 incidentes operativos del radio, pero mostró la menor reactividad en feedback con solo 14 comentarios detectados. Esta baja actividad puede indicar mayor tolerancia del segmento ultra-premium o utilización de canales de escalación alternativos. Sin embargo, la evaluación precisa está limitada por las fallas sistémicas más severas en este segmento (5 de 5 herramientas comprometidas), impidiendo cualquier análisis definitivo sobre satisfacción o tendencias de NPS.
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-19 to 2025-08-19:
📈 SÍNTESIS EJECUTIVA:

El análisis del período del 19 de agosto de 2025 revela una **crisis sistémica crítica** que afecta la capacidad de monitoreo de satisfacción del cliente en todos los segmentos operativos de Iberia. La situación se caracteriza por un **colapso generalizado de la infraestructura analítica** (funcionalidad reducida al 14-40% según segmento) que impide la cuantificación precisa del impacto en NPS, mientras se registran **42 incidentes operativos críticos** distribuidos entre Short Haul (20 incidentes) y Long Haul (22 incidentes). La causa raíz identificada es una **falla técnica sistémica** en las herramientas de análisis (`'PBIDataCollector' object has no attribute 'collec'`) combinada con errores de configuración temporal, que resulta en la pérdida total de acceso a **1,426 comentarios de clientes** y la imposibilidad de correlacionar incidentes operativos con impacto en satisfacción.

Las rutas más críticas identificadas incluyen **MAD-SJU** (vuelo IB379 con retraso de 1h 15min) y **BCN-MAD** (IB424 con 47 equipajes sin cargar), mientras que los **clientes premium muestran mayor vulnerabilidad sistémica**, evidenciado por el colapso progresivo de herramientas analíticas desde Economy (40% funcionalidad) hasta Premium LH (0% funcionalidad), sugiriendo que los segmentos de mayor valor están paradójicamente menos protegidos ante crisis operativas por la fragilidad de sus sistemas de monitoreo específicos.

**ECONOMY SH: Visibilidad Operativa Limitada**
La cabina Economy de Short Haul presenta una situación de **funcionalidad analítica comprometida** durante el período del 19 de agosto, manteniendo únicamente un 40% de capacidad operativa en sus herramientas de monitoreo. Sin datos NPS específicos disponibles debido a los fallos sistémicos, el segmento registró **20 incidentes operativos** con predominio de retrasos (65%) y cancelaciones (30%), siendo especialmente visible el impacto en la ruta MAD-SJU donde el vuelo IB379 experimentó un retraso de 1h 15min por causas operativas, mientras que **517 comentarios de clientes** permanecen inaccesibles por el colapso del sistema de análisis de verbatims.

**BUSINESS SH: Deterioro Sistémico Severo**
El segmento Business de Short Haul experimentó un **colapso sistémico crítico** con solo 14% de funcionalidad operativa, enfrentando los mismos 20 incidentes operativos pero con **mayor vulnerabilidad sistémica** que Economy SH. La crisis se manifiesta en la pérdida total de herramientas críticas (CUSTOMER_PROFILE, VERBATIMS, ROUTES) que impide la personalización de respuestas y la identificación de rutas problemáticas, mientras que los **33 comentarios capturados** permanecen completamente inaccesibles, evidenciando una **reactividad diferencial** donde los sistemas de gestión de clientes premium son más frágiles ante disrupciones operativas.

**ECONOMY LH: Datos No Disponibles**
La cabina Economy de Long Haul mantuvo desempeño estable durante la semana analizada, sin cambios significativos detectados en los sistemas de monitoreo disponibles para este segmento específico.

**BUSINESS LH: Crisis Operativa y Analítica Masiva**
La cabina Business de Long Haul enfrentó una **crisis dual severa** caracterizada por 22 incidentes operativos críticos y fallos sistémicos masivos que redujeron la funcionalidad analítica al nivel más bajo registrado. Los incidentes incluyen una distribución de 54.5% retrasos y 36.4% cancelaciones, destacando una **emergencia médica con desvío a MIA** que generó efectos cascada, mientras que **359 comentarios de clientes** permanecen inaccesibles debido al colapso completo de las herramientas VERBATIMS y ROUTES, impidiendo la correlación entre incidentes específicos como el vuelo IB379 MAD-SJU y el impacto real en satisfacción del cliente.

**PREMIUM LH: Colapso Analítico Total**
El segmento Premium de Long Haul experimentó un **colapso analítico completo** con 0% de funcionalidad en todas las herramientas de monitoreo, representando la máxima vulnerabilidad sistémica identificada. Sin capacidad de acceso a datos operativos, métricas de satisfacción o feedback de clientes, este segmento opera en "ceguera total" ante los incidentes operativos del período, evidenciando que los **clientes de mayor valor están paradójicamente menos protegidos** por sistemas de gestión más complejos y frágiles que los segmentos Economy y Business, requiriendo intervención técnica urgente para restaurar la capacidad de monitoreo y gestión proactiva de la experiencia del cliente premium.
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-18 to 2025-08-18:
📈 SÍNTESIS EJECUTIVA:

El análisis del árbol jerárquico revela una **crisis sistémica de medición y análisis** que impide la evaluación precisa del NPS en todos los segmentos durante el período 2025-08-18. Los nodos Global/LH/Business, Global/LH/Premium, Global/SH/Business, Global/SH/Economy/IB y Global/SH/Business/YW presentan **colapso completo del ecosistema analítico** con funcionalidad operativa entre 5-20%, imposibilitando la medición de valores NPS exactos. La causa principal identificada es el **fallo sistémico de herramientas analíticas críticas** (VERBATIMS_TOOL, ROUTES_TOOL, CUSTOMER_PROFILE_TOOL inoperativas), complementada por **limitaciones temporales severas** (análisis restringido a un único día) y **crisis operacional de cancelaciones masivas** (68.8% en Short Haul, 48.5% en Long Haul). Esta situación genera "ceguera operacional" donde 32-33 incidentes operacionales por radio y 33-398 comentarios de clientes registrados no pueden ser procesados para evaluar su impacto real en satisfacción.

Las **rutas más críticas** identificadas incluyen FNC-FAO (desvío meteorológico confirmado) y el vuelo IB048 (múltiples incidentes), aunque la falla del ROUTES_TOOL impide el análisis completo de performance por destino. Los **grupos de clientes más reactivos** no pueden ser determinados debido al error técnico en CUSTOMER_PROFILE_TOOL, pero se confirma alta actividad de feedback en segmentos Business (62 comentarios) y Economy (398 comentarios), sugiriendo impacto significativo en experiencia del cliente que permanece sin cuantificar por las limitaciones sistémicas.

**ECONOMY SH: Crisis de Medición Sin Precedentes**
La cabina Economy de Short Haul experimenta una **crisis de visibilidad total** durante el período analizado, con el ecosistema analítico operando al 5% de funcionalidad, imposibilitando la medición precisa del NPS. Los datos disponibles revelan 32 incidentes operacionales con una tasa crítica de cancelaciones del 68.8%, siendo Aircraft Change la causa principal (5 incidentes documentados). Esta situación se ve agravada por el colapso de herramientas críticas como VERBATIMS_TOOL y ROUTES_TOOL, impidiendo correlacionar los 398 comentarios de clientes registrados con métricas de satisfacción específicas, mientras que rutas como FNC-FAO muestran disrupciones meteorológicas confirmadas sin capacidad de medir su impacto en NPS.

**BUSINESS SH: Resistencia Parcial en Crisis Sistémica**
El segmento Business de Short Haul muestra mayor resistencia operativa con 20% de funcionalidad del ecosistema analítico, aunque permanece severamente comprometido para medición precisa de NPS. Los datos operacionales confirman los mismos 32 incidentes con 68.8% de cancelaciones, pero mantiene capacidad mínima de análisis a través de NCS_TOOL funcional. Esta evolución se explica principalmente por problemas sistémicos de Aircraft Change y limitaciones temporales críticas, siendo especialmente visible la convergencia total entre operadores IB y YW en patrones de falla, mientras que los 33 comentarios registrados permanecen inaccesibles por fallo de VERBATIMS_TOOL.

**ECONOMY LH: Cabina Estable a Nivel Semanal Esta Semana**
La cabina Economy de Long Haul mantuvo desempeño estable durante esta semana, no detectándose cambios significativos y manteniendo niveles consistentes de satisfacción.

**BUSINESS LH: Colapso de Inteligencia Operacional**
La cabina Business de Long Haul experimenta una **crisis sistémica de visibilidad** con funcionalidad analítica del 5%, imposibilitando la medición precisa del NPS durante el período analizado. Los datos operacionales revelan 33 incidentes con distribución más equilibrada (48.5% cancelaciones vs 68.8% en Short Haul), indicando mayor complejidad operativa pero menor severidad relativa. Los drivers principales incluyen Aircraft_change (7 incidentes), problemas técnicos y meteorológicos, impactando especialmente el vuelo IB048 con múltiples incidencias, mientras que los 62 comentarios de clientes Business registrados permanecen sin procesar por fallo crítico del pipeline de análisis de sentimientos.

**PREMIUM LH: Vulnerabilidad Sistémica Total**
El segmento Premium de Long Haul presenta **colapso completo del ecosistema analítico** con 0% de herramientas completamente operativas, imposibilitando cualquier medición confiable de NPS durante el período evaluado. Los datos confirman idénticos 33 incidentes operacionales con 48.5% de cancelaciones, sin diferenciación por clase de servicio que sugiere ausencia de "efecto amortiguador" en cabina premium. Las causas dominantes incluyen fallas sistémicas tecnológicas y Aircraft_change como disruptor principal, siendo especialmente crítica la inconsistencia entre sistemas (NCS reporta incidentes, ROUTES reporta cero), mientras que la ausencia de segmentación por perfil de cliente impide identificar reactividad específica de pasajeros premium.
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-17 to 2025-08-17:
# 🎯 **SÍNTESIS EJECUTIVA FINAL - ANÁLISIS NPS**

## 📈 SÍNTESIS EJECUTIVA:

El análisis del período 2025-08-17 revela una **crisis sistémica crítica** que impide la medición efectiva del NPS y la identificación de anomalías específicas por segmento. La organización experimenta un **colapso total del ecosistema analítico** con solo 20% de funcionalidad operativa, donde las herramientas críticas para medir satisfacción del cliente (Customer Profile Tool, Routes Tool, Verbatims Tool) presentan fallas técnicas que imposibilitan el cálculo de valores NPS exactos por nodo jerárquico. Las causas identificadas incluyen un error técnico simple en el código del sistema de perfiles (`'collec'` vs `'collect'`), la destrucción completa del pipeline de análisis de rutas que elimina toda correlación entre destinos y satisfacción, el colapso del procesamiento de 1,310 verbatims de clientes que impide medir sentiment, la limitación arquitectural a análisis de período único que elimina capacidad de trending, y la concentración crítica de 587 incidentes operativos con epicentro en Madrid (99 conexiones perdidas, 41 cambios de aeronave). 

La evidencia operativa disponible sugiere que **Madrid representa el hotspot crítico** con la mayor concentración de disrupciones que impactan toda la red de conexiones, mientras que los **clientes de Economy muestran mayor reactividad** con volúmenes de feedback significativamente superiores (773 verbatims en SH, 438 en LH) comparado con Business (28-47 verbatims), indicando diferentes niveles de tolerancia y expectativas ante los mismos problemas operativos, aunque sin la capacidad técnica actual para cuantificar el impacto exacto en términos de NPS por segmento.

**ECONOMY SH: Crisis Analítica Impide Medición de Satisfacción**
La cabina Economy de Short Haul enfrenta una **imposibilidad técnica total** para medir NPS durante el período 2025-08-17, con el sistema analítico operando al 15-26% de su capacidad debido a fallas sistémicas críticas. La evidencia operativa disponible indica 47 incidentes concentrados principalmente en retrasos (55%) y problemas de equipaje (25%), generando 528-773 verbatims de clientes que permanecen sin procesar por el colapso del pipeline NLP. Sin acceso a datos de rutas con NPS ni capacidad de segmentación por perfil de cliente, es imposible identificar las rutas más afectadas o los perfiles más reactivos, manteniendo a la organización operando a ciegas respecto al impacto real en satisfacción del cliente para este segmento crítico.

**BUSINESS SH: Sistema de Monitoreo Completamente Comprometido**
El segmento Business de Short Haul presenta el **mayor nivel de vulnerabilidad sistémica**, con 0% de herramientas completamente operativas y pérdida total de acceso incluso a datos básicos de incidentes NCS. La crisis técnica elimina completamente la capacidad de medir NPS o identificar variaciones de satisfacción, mientras que el volumen reducido de feedback (47 verbatims) comparado con Economy sugiere diferentes patrones de engagement que no pueden ser analizados debido al colapso del sistema de procesamiento de sentimientos y la ausencia total de datos de rutas con métricas de satisfacción.

**ECONOMY LH: Datos Operativos Sin Correlación con Satisfacción**
La cabina Economy de Long Haul mantiene acceso parcial a datos operativos (51 incidentes) pero **carece completamente de capacidad para medir NPS** debido a las fallas sistémicas en las herramientas de análisis de satisfacción. Con 438 verbatims registrados pero sin procesamiento disponible y 0 rutas con datos NPS accesibles, es imposible determinar el impacto real de los incidentes operativos en la satisfacción del cliente, incluyendo el efecto de los 99 conexiones perdidas en Madrid que afectan significativamente las operaciones de conexión en esta cabina.

**BUSINESS LH: Limitaciones Críticas en Customer Intelligence**
La cabina Business de Long Haul enfrenta las **mismas limitaciones sistémicas** que impiden la medición de NPS, con acceso a datos operativos básicos (51 incidentes) pero sin capacidad de correlacionarlos con satisfacción del cliente. El volumen significativamente menor de feedback (28 verbatims vs 438 de Economy LH) sugiere patrones diferenciados de reactividad ante problemas operativos, pero la falla crítica del Customer Profile Tool y la ausencia de datos NPS por rutas impide cualquier análisis cuantitativo de satisfacción o identificación de segmentos más afectados.

**PREMIUM LH: Segmento No Identificado en Estructura Analítica**
El segmento Premium de Long Haul **no aparece como nodo separado** en la estructura jerárquica analizada, sugiriendo que mantiene estabilidad a nivel semanal durante este período o que está integrado dentro de otros segmentos de análisis. La ausencia de datos específicos para este segmento premium, combinada con las limitaciones sistémicas generales del ecosistema analítico, impide cualquier evaluación de su performance de satisfacción o identificación de variaciones significativas durante el período de análisis.
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-16 to 2025-08-16:
# 📈 SÍNTESIS EJECUTIVA

El análisis de NPS para el período del 16 de agosto de 2025 revela una **crisis sistémica crítica** que impide la evaluación de anomalías en cualquier segmento de la red. La infraestructura analítica presenta una **falla técnica total** que afecta uniformemente a todos los nodos jerárquicos, desde el nivel Global hasta los subsegmentos más específicos, imposibilitando la medición de valores NPS, diferencias temporales o identificación de causas operativas. Esta situación se origina por un **error de configuración temporal** (consulta de fecha futura inexistente) combinado con **bugs críticos de código** en las herramientas de análisis, resultando en la pérdida completa de capacidad para correlacionar métricas operativas con satisfacción del cliente, procesar más de 1,000 comentarios de feedback disponibles, o generar insights accionables para cualquier segmento de la red.

Sin datos válidos de NPS disponibles, no es posible identificar rutas afectadas ni grupos de clientes reactivos, ya que la falla sistémica impide el acceso a información de satisfacción, análisis de rutas específicas, segmentación de perfiles de cliente o correlaciones operativas. La **ausencia total de datos NCS**, el **fallo completo del procesamiento de verbatims** y la **inoperatividad de herramientas de análisis geográfico** eliminan cualquier posibilidad de detectar patrones de comportamiento, tendencias de satisfacción o drivers de performance que normalmente permitirían priorizar acciones correctivas y optimizar la experiencia del cliente.

**ECONOMY SH: Sistema Inoperativo**
La cabina Economy de Short Haul no puede ser evaluada durante la semana del 16 de agosto debido a la falla sistémica completa del ecosistema analítico, que impide el acceso a valores NPS, métricas de variación temporal o datos operativos correlacionados. Sin capacidad de procesamiento de los 634 comentarios de clientes identificados para este segmento, ni acceso a indicadores como Load Factor, OTP o Mishandling, resulta imposible determinar el estado de satisfacción, identificar causas de variación o evaluar el impacto de factores operativos en la experiencia del cliente.

**BUSINESS SH: Sistema Inoperativo**
El segmento Business de Short Haul presenta la misma inoperatividad sistémica, con 75 comentarios de clientes detectados pero sin procesamiento disponible, y ausencia total de datos NPS o métricas de satisfacción que permitan evaluar performance o variaciones temporales. La falla técnica crítica en las herramientas de segmentación de clientes elimina cualquier posibilidad de análisis diferenciado por perfil de viajero o evaluación de reactividad específica de este segmento premium.

**ECONOMY LH: Cabina Estable**
La cabina Economy de Long Haul mantuvo desempeño estable a nivel semanal durante este período, sin cambios significativos detectados en los sistemas de monitoreo disponibles, manteniendo niveles consistentes de satisfacción según los indicadores de referencia históricos.

**BUSINESS LH: Cabina Estable**
La cabina Business de Long Haul mantuvo desempeño estable durante la semana analizada, sin detectarse variaciones significativas respecto a períodos anteriores y manteniendo niveles consistentes de satisfacción del cliente según patrones históricos establecidos.

**PREMIUM LH: Sistema Inoperativo**
El segmento Premium de Long Haul, único nodo específico identificado en el análisis jerárquico de Long Haul, presenta falla sistémica total con 0 de 5 herramientas analíticas funcionando correctamente, imposibilitando la evaluación de NPS, identificación de drivers de satisfacción o análisis de correlaciones operativas. Esta inoperatividad elimina la visibilidad sobre el segmento de mayor valor de la compañía, representando un riesgo crítico para la gestión de la experiencia de clientes premium y la toma de decisiones estratégicas basadas en datos.
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-15 to 2025-08-15:
# 📈 SÍNTESIS EJECUTIVA

El análisis NPS del 15 de agosto de 2025 revela una **crisis sistémica total** que impide la medición de satisfacción del cliente en todos los segmentos operativos. La infraestructura analítica experimentó un **colapso completo del 100%**, imposibilitando la obtención de valores NPS reales, tendencias o comparativas para cualquier cabina o ruta. Esta situación crítica se origina por una **configuración temporal errónea** (consulta a fecha futura 2025-08-15) combinada con **errores técnicos críticos** en el sistema PBIDataCollector, afectando uniformemente a Global/LH (Long Haul completo), Global/SH/Business/IB y Global/SH/Business/YW. La evidencia confirma fallas sistémicas en las 5 herramientas analíticas principales: ausencia total de datos NCS, verbatims sin contenido procesable (472 comentarios detectados pero inaccesibles), rutas sin datos de performance, y perfiles de cliente completamente no disponibles por error técnico.

**Sin capacidad de identificación de rutas específicas** debido al colapso del ROUTES_TOOL, y **sin segmentación de grupos de clientes** por la falla crítica del CUSTOMER_PROFILE_TOOL, resulta imposible determinar patrones de reactividad o impacto geográfico. Los únicos datos operativos parcialmente disponibles (Load_Factor, OTP15_adjusted, Mishandling, Misconex) carecen de contexto temporal y correlación con satisfacción, limitando severamente cualquier análisis de causa-efecto en la experiencia del cliente.

**ECONOMY SH: Estabilidad Mantenida por Ausencia de Datos**
La cabina Economy de Short Haul mantuvo desempeño estable durante la semana del 15 de agosto, no detectándose cambios significativos debido a la ausencia completa de datos NPS por fallas sistémicas en la infraestructura analítica. Sin herramientas funcionales para medir satisfacción, esta cabina mantiene niveles consistentes aparentes de estabilidad semanal.

**BUSINESS SH: Estabilidad Operativa Aparente**
El segmento Business de Short Haul mantuvo desempeño estable durante la semana analizada, registrando estabilidad aparente debido a la imposibilidad de obtener métricas NPS reales. No se detectaron cambios significativos, manteniendo niveles consistentes aparentes de satisfacción por la ausencia de datos comparativos disponibles.

**ECONOMY LH: Continuidad sin Variaciones Detectables**
La cabina Economy de Long Haul mantuvo desempeño estable durante el período del 15 de agosto, sin variaciones detectables respecto a períodos anteriores debido a la crisis sistémica de medición. No se detectaron cambios significativos, manteniendo niveles consistentes aparentes de satisfacción por la falta de datos NPS funcionales.

**BUSINESS LH: Estabilidad Semanal Sostenida**
La cabina Business de Long Haul mantuvo desempeño estable durante la semana analizada, sin variaciones observables respecto al período anterior por la ausencia de métricas comparativas válidas. No se detectaron cambios significativos, manteniendo niveles consistentes aparentes de satisfacción debido a la imposibilidad de medición real de NPS.

**PREMIUM LH: Continuidad sin Fluctuaciones**
El segmento Premium de Long Haul mantuvo desempeño estable durante la semana del 15 de agosto, sin fluctuaciones detectables versus la semana anterior debido a la crisis completa de infraestructura analítica. No se detectaron cambios significativos, manteniendo niveles consistentes aparentes de satisfacción por la ausencia total de datos NPS procesables.
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