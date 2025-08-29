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
[{'period': 1, 'date_range': '2025-08-18 to 2025-08-24', 'ai_interpretation': '📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**\n\n**Nodos analizados:** 10 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH, Global/SH/Business, Global/SH/Business/YW, Global/SH/Economy, Global/SH/Economy/YW)\n\n---\n\n## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA\n\n# 🏢 PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)\n\n## **A. Economy Short Haul:**\n\n**Nodos identificados:**\n- ✅ **Global/SH/Economy/YW** existe (NPS: 33.21, Anomalía: +19.20 puntos)\n- ❌ **Global/SH/Economy/IB** NO existe en los datos\n\n**Razón de ausencia:** No se detectó anomalía significativa en el segmento Economy SH/IB durante el período analizado, por lo que no se generó nodo de análisis.\n\n**Diagnóstico:** **Causa específica de compañía YW** - La anomalía positiva está localizada únicamente en Vueling, no es un patrón generalizado de la cabina Economy Short Haul.\n\n---\n\n## **B. Business Short Haul:**\n\n**Nodos identificados:**\n- ✅ **Global/SH/Business/YW** existe (NPS: 39.81, Anomalía: +44.0 puntos)\n- ❌ **Global/SH/Business/IB** NO existe en los datos\n\n**Razón de ausencia:** No se detectó anomalía significativa en el segmento Business SH/IB durante el período analizado, por lo que no se generó nodo de análisis.\n\n**Diagnóstico:** **Causa específica de compañía YW** - La anomalía positiva está localizada únicamente en Vueling, no es un patrón generalizado de la cabina Business Short Haul.\n\n---\n\n## **CONCLUSIÓN DIAGNÓSTICA:**\n\nLas anomalías NPS positivas en Short Haul están **específicamente concentradas en Vueling (YW)**, tanto en Economy como en Business. Iberia (IB) no presenta anomalías detectables en ninguna de estas cabinas durante el mismo período, lo que confirma que las causas operativas y de experiencia identificadas son particulares de la operación de Vueling.\n\n---\n\n## 💺 DIAGNÓSTICO A NIVEL DE CABINA\n\n# ✈️ PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)\n\n## **A. Short Haul - Análisis de Cabinas:**\n\n### **Patrones Identificados:**\n\n**Economy SH/YW:**\n- Anomalía: +19.20 puntos NPS\n- Driver dominante: Punctuality (SHAP: +11.105)\n- Causa: Mejora operativa masiva (-59.6% incidentes)\n\n**Business SH/YW:**\n- Anomalía: +44.0 puntos NPS  \n- Driver dominante: Punctuality (SHAP: +16.286)\n- Causa: Misma mejora operativa (-53% incidentes)\n\n### **Convergencia Operativa con Reactividad Diferencial:**\n- **Causa común**: Ambas cabinas reaccionan a la **misma transición operativa** (crisis sistémica → normalización)\n- **Reactividad diferencial**: Business SH muestra **mayor sensibilidad** (+44.0 vs +19.20 puntos) a las mejoras de puntualidad\n- **Drivers convergentes**: Punctuality como factor dominante en ambas, con valores SHAP proporcionales\n\n**Diagnóstico SH:** **Causa común de radio con reactividad diferencial por cabina** - La mejora operativa de Vueling afecta ambas cabinas, pero Business muestra mayor sensibilidad a los cambios de puntualidad.\n\n---\n\n## **B. Long Haul - Análisis de Cabinas:**\n\n### **Patrones Identificados:**\n\n**Economy LH:**\n- Anomalía: +13.3 puntos NPS\n- Driver dominante: Punctuality (SHAP: +8.765)\n- Causa: Reducción masiva de incidentes (-56.1%)\n\n**Business LH:**\n- Anomalía: +17.1 puntos NPS\n- Driver dominante: Punctuality (SHAP: +6.475)\n- Causa: Misma reducción de incidentes (-56.1%)\n\n**Premium LH:**\n- Anomalía: **-8.07 puntos NPS** (única negativa)\n- Drivers negativos: Boarding (SHAP: -7.482), Cabin Crew (SHAP: -5.622)\n- Contradicción: Mejora operativa pero deterioro en servicio específico\n\n### **Divergencia Crítica en Premium:**\n- **Economy y Business LH**: Convergencia total en causa operativa y reactividad positiva\n- **Premium LH**: **Divergencia completa** - misma mejora operativa genera resultado negativo por problemas específicos de servicio\n\n**Diagnóstico LH:** **Causa específica de cabina Premium** - Mientras Economy y Business reaccionan positivamente a las mejoras operativas, Premium experimenta deterioro por factores específicos de servicio (boarding, cabin crew) que superan el beneficio operativo.\n\n---\n\n## **CONCLUSIÓN DIAGNÓSTICA:**\n\n- **Short Haul**: Causa común de radio con reactividad proporcional por nivel de servicio\n- **Long Haul**: Causa común operativa, pero Premium presenta factores específicos negativos que invierten el impacto\n\n---\n\n## 🌎 DIAGNÓSTICO GLOBAL POR RADIO\n\n# 🌍 PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL\n\n## **A. Comparación Entre Radios:**\n\n### **Anomalías Detectadas:**\n- **Short Haul**: +11.9 puntos NPS (solo YW afectado)\n- **Long Haul**: +12.6 puntos NPS (todas las compañías)\n\n### **Convergencia en Drivers Principales:**\n\n**Driver Dominante Común:**\n- **SH**: Punctuality (SHAP: +6.655)\n- **LH**: Punctuality (SHAP: +7.970)\n\n**Evidencia Operativa Convergente:**\n- **SH**: Reducción -59.6% incidentes totales\n- **LH**: Reducción -50% incidentes NCS (276 → 138)\n\n**Valores SHAP Consistentes:**\n- Ambos radios muestran Punctuality como driver dominante con valores SHAP similares (~7 puntos)\n- Arrivals Experience como driver secundario en ambos radios\n- Boarding como driver terciario compartido\n\n---\n\n## **B. Coherencia con Nodo Global:**\n\n### **Agregación Coherente:**\n- **Global**: +11.93 puntos NPS\n- **Promedio ponderado**: SH (+11.9) + LH (+12.6) = coherente con Global (+11.93)\n\n### **Drivers Globales vs Radios:**\n- **Global**: Punctuality (SHAP: +7.095) - **convergente** con ambos radios\n- **Global**: Arrivals Experience (SHAP: +1.710) - **convergente** con ambos radios\n- **Global**: Boarding (SHAP: +1.321) - **convergente** con ambos radios\n\n### **Evidencia Operativa Global:**\n- **OTP15**: +0.7 puntos mejora - **consistente** con mejoras en ambos radios\n- **Cancelaciones**: +140% incremento - **refleja** la suma de incidentes de ambos radios\n- **Patrón temporal**: Crisis sistémica → normalización - **común** a ambos radios\n\n---\n\n## **CONCLUSIÓN DIAGNÓSTICA:**\n\n**Causa global homogénea** - Ambos radios (SH y LH) convergen completamente en el mismo patrón causal: mejora operativa masiva en puntualidad tras resolución de crisis sistémicas. El nodo Global refleja perfectamente la agregación de estos patrones convergentes, con drivers SHAP, evidencia operativa y magnitudes de anomalía totalmente coherentes entre los tres niveles de análisis.\n\nLa única excepción es Premium LH, que representa una divergencia específica de cabina dentro del patrón global homogéneo.\n\n---\n\n## 📋 ANÁLISIS DE CAUSAS DETALLADO\n\n# 🔍 PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS\n\n## **CAUSA PRINCIPAL IDENTIFICADA: RECUPERACIÓN OPERATIVA SISTÉMICA**\n\n### **A. NATURALEZA DE LA CAUSA:**\n\n**Hipótesis Causal:** Transición operativa fundamental desde un período de crisis sistémicas múltiples (cierre MEX por inundaciones, ceniza volcánica, temperaturas extremas, pérdidas de conexión masivas) hacia un período de normalización operativa con solo disrupciones meteorológicas localizadas y manejables. Esta mejora operativa masiva generó una percepción diferencial positiva en los pasajeros, especialmente en aspectos de puntualidad y experiencia de llegadas.\n\n---\n\n### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**\n\n**Segmento más amplio afectado:** **GLOBAL** (abarca todos los subsegmentos)\n\n**Output causal detallado del segmento Global:**\n- **NPS Actual:** 26.56 puntos\n- **NPS Baseline:** 14.63 puntos  \n- **Anomalía:** +11.93 puntos\n- **Driver Dominante:** PUNCTUALITY (SHAP: +7.095)\n- **Diferencia de satisfacción:** +10.07 puntos vs período comparativo\n\n**Subsegmentos afectados:** Esta causa impacta a **TODOS** los subsegmentos bajo el nodo Global:\n- Global/LH (+12.6 puntos)\n- Global/LH/Economy (+13.3 puntos)\n- Global/LH/Business (+17.1 puntos)\n- Global/SH (+11.9 puntos - solo YW)\n- Global/SH/Economy/YW (+19.20 puntos)\n- Global/SH/Business/YW (+44.0 puntos)\n\n**Excepción:** Global/LH/Premium (-8.07 puntos) presenta patrón invertido por factores específicos de servicio.\n\n---\n\n### **MÉTRICAS CLAVE CONSOLIDADAS:**\n\n**Indicadores Operativos:**\n- **Reducción total de incidentes:** -50% a -59.6% según radio\n- **OTP15:** Mejora +0.7 a +2.2 puntos\n- **Cancelaciones:** Reducción -38.1% a -52.4%\n- **Retrasos:** Reducción -47.6% a -53.5%\n- **Otras incidencias:** Reducción -68.2% a -73.7%\n- **Desvíos:** Reducción -80% a -100%\n\n**Rutas Involucradas (muestra representativa):**\n- **Long Haul:** BOG-MAD, LIM-MAD, MAD-MIA, MAD-MEX, GYE-MAD\n- **Short Haul:** MAD-NCE, CDT-MAD, MAD-TIA, MAD-ZRH, BCN-MAD\n- **Patrón geográfico:** Predominio rutas América-Europa y conexiones Madrid\n\n**Drivers SHAP Convergentes:**\n- **Punctuality:** +6.655 a +16.286 (driver dominante en todos los segmentos)\n- **Arrivals Experience:** +1.574 a +7.024 (driver secundario)\n- **Boarding:** +1.167 a +2.949 (driver terciario)\n\n**Verbatims Representativos:**\n- **4,604 análisis sobre BOARDING** en SH confirmando mejoras percibidas\n- **1,425 análisis específicos sobre BOARDING** en Economy SH/YW\n- **461 comentarios sobre BOARDING** en Business SH/YW\n- **288 análisis sobre BOARDING** en Business LH\n\n**Reactividad Diferencial por Perfil:**\n- **CodeShare:** Mayor reactividad (spreads 65-233 puntos)\n- **Residence Region:** Alta reactividad (spreads 33-106 puntos)\n- **Fleet:** Reactividad moderada (spreads 15-150 puntos)\n- **Business/Leisure:** Reactividad uniforme (spreads 7-29 puntos)\n\n---\n\n### **CONCLUSIÓN CAUSAL:**\n\nLa recuperación operativa sistémica constituye una **causa global homogénea** que explica las anomalías NPS positivas en prácticamente todos los segmentos analizados. La mejora masiva en puntualidad, tras resolver crisis operativas excepcionales, generó un impacto diferencial positivo que se amplifica según el nivel de servicio (Business > Economy) y muestra mayor reactividad en perfiles específicos (CodeShare, regiones geográficas particulares).\n\n---\n\n## 📋 SÍNTESIS EJECUTIVA FINAL\n\n📈 SÍNTESIS EJECUTIVA:\n\nDurante la semana del 18 al 24 de agosto de 2025, el Grupo IAG experimentó una mejora generalizada del NPS impulsada por una recuperación operativa excepcional tras resolver crisis sistémicas de la semana anterior. A nivel global, el NPS subió 11.93 puntos (de 14.63 a 26.56), con Long Haul liderando la mejora al pasar de 9.2 a 21.8 puntos (+12.6) y Short Haul registrando una subida de 11.9 puntos (de 16.9 a 28.9). Esta mejora se explica por la transición desde un período de crisis múltiples (cierre del aeropuerto de México por inundaciones, ceniza volcánica, temperaturas extremas) hacia condiciones operativas normalizadas, evidenciado por una reducción del 50-60% en incidentes totales, mejoras en OTP15 de hasta 2.2 puntos y la eliminación completa de desvíos. El driver dominante fue Punctuality (SHAP +7.095 a nivel global), complementado por mejoras en Arrivals Experience y Boarding, validado por más de 7,000 análisis de verbatims que confirman la percepción positiva de los clientes.\n\nLas rutas más beneficiadas se concentraron en conexiones América-Europa, destacando BOG-MAD con una subida de 51.3 puntos NPS, LIM-MAD (+36.2 puntos) y MAD-MIA, mientras que en Short Haul sobresalieron CDT-MAD (+77.3 puntos) y MAD-NCE (+60.6 puntos). Los perfiles de clientes más reactivos fueron los pasajeros de CodeShare (spreads de hasta 233 puntos) y ciertas regiones de residencia (spreads de 33-106 puntos), mientras que la segmentación Business/Leisure mostró reactividad más uniforme.\n\n**ECONOMY SH: Mejora Operativa Concentrada en Vueling**\nLa cabina Economy de Short Haul experimentó una mejora sustancial durante la semana del 18-24 agosto, impulsada exclusivamente por Vueling que registró un NPS de 33.21 (mejora de 19.20 puntos vs semana anterior), mientras Iberia mantuvo niveles estables sin anomalías detectables. La causa principal fue la recuperación operativa masiva de Vueling con una reducción del 59.6% en incidentes totales (de 265 a 107), liderada por Punctuality como driver dominante (SHAP +11.105) y complementada por mejoras en Arrivals Experience (+2.572) y Boarding (+2.369), validadas por 1,425 análisis de verbatims. Esta mejora se reflejó especialmente en rutas como CDT-MAD (NPS 55.6, +77.3 puntos vs L7d) y MAD-NCE (NPS 16.7, +53.3 puntos), mientras que los perfiles más reactivos fueron CodeShare (spread 113.8 puntos) y diferentes regiones de residencia (spread 76.7 puntos).\n\n**BUSINESS SH: Recuperación Excepcional en Vueling**\nEl segmento Business de Short Haul mostró la mejora más dramática del período, registrando un NPS de 39.81 (subida de 44.0 puntos vs semana anterior), concentrada exclusivamente en Vueling mientras Iberia mantuvo desempeño estable. Esta evolución se explica principalmente por la transición de crisis sistémica a normalización operativa, con Punctuality como driver dominante (SHAP +16.286), seguido por Arrivals Experience (+7.024) y Boarding (+0.256), respaldado por una reducción del 53% en incidentes operativos y validado por 140 análisis de verbatims sobre boarding. El impacto fue especialmente visible en rutas como FRA-MAD (NPS 60.0), MAD-MUC (NPS 66.7) y BIO-MAD (NPS 50.0), siendo los perfiles CodeShare (spread 140.0 puntos) y Residence Region (spread 106.4 puntos) los más reactivos a esta mejora operativa.\n\n**ECONOMY LH: Recuperación Post-Crisis Sistémica**\nLa cabina Economy de Long Haul experimentó una mejora significativa durante la semana del 18-24 agosto, registrando un NPS de 20.0 (subida de 13.3 puntos respecto a la semana anterior). La causa principal fue la recuperación operativa excepcional tras resolver eventos catastróficos únicos como el cierre de México por inundación y pérdidas masivas de conexión, evidenciada por una reducción del 56.1% en incidentes totales y liderada por Punctuality como driver dominante (SHAP +8.765), complementada por mejoras en Arrivals Experience (+2.326) y Boarding (+1.542). Esta mejora se reflejó especialmente en rutas como BOG-MAD (NPS 57.4, +51.3 puntos vs L7d), LIM-MAD (NPS 5.7, +36.2 puntos) y MAD-MIA (NPS 26.8), mientras que los perfiles más reactivos incluyeron CodeShare (spread 74.4 puntos) y diferentes regiones de residencia (spread 62.4 puntos).\n\n**BUSINESS LH: Normalización Operativa Exitosa**\nLa cabina Business de Long Haul registró una mejora sólida durante el período analizado, alcanzando un NPS de 35.2 (subida de 17.1 puntos vs la semana anterior). Los drivers principales fueron Punctuality (SHAP +6.475) validado por la reducción de 49 retrasos (-47.6%), Aircraft Interior (+2.947) y Arrivals Experience (+2.085), impactando especialmente las rutas transatlánticas como MAD-MEX (NPS 56.2, +56.2 puntos), JFK-MAD (NPS 45.5, +112.1 puntos) y LAX-MAD (NPS 100.0, +50.0 puntos), con los perfiles Fleet (spread 150.8 puntos) y Residence Region (spread 57.5 puntos) mostrando la mayor reactividad a la eliminación de disrupciones por inundación en México.\n\n**PREMIUM LH: Deterioro por Problemas de Servicio Específicos**\nEl segmento Premium de Long Haul experimentó un deterioro durante la semana del 18-24 agosto, registrando un NPS de 20.0 (caída de 8.07 puntos vs la semana anterior), contrastando con la mejora operativa general. Las causas dominantes fueron el deterioro crítico en Boarding (SHAP -7.482, -2.30 puntos de satisfacción) y Cabin Crew (SHAP -5.622, -2.27 puntos), que superaron el impacto positivo de Punctuality (+9.570), especialmente evidentes en rutas latinoamericanas como MAD-SCL y EZE-MAD, con los perfiles CodeShare (spread 233.3 puntos) y Residence Region (spread 72.9 puntos) mostrando la mayor reactividad a estas deficiencias específicas de servicio premium.\n\n---\n\n✅ **ANÁLISIS COMPLETADO**\n\n- **Nodos procesados:** 10\n- **Pasos de análisis:** 5\n- **Metodología:** Análisis conversacional paso a paso\n- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado\n\n*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*'}]

**ANÁLISIS DIARIO SINGLE:**
📅 2025-08-24 to 2025-08-24:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 11 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH/Business, Global/SH/Business/IB, Global/SH/Business/YW, Global/SH/Economy, Global/SH/Economy/IB, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. Economy Short Haul:**

**NODOS IDENTIFICADOS:**
- ✅ **Global/SH/Economy/IB** - Anomalía: -7.84 puntos NPS
- ✅ **Global/SH/Economy/YW** - Anomalía: -12.63 puntos NPS

**ANÁLISIS COMPARATIVO:**

### **Drivers Principales:**
- **IB**: Mishandling 29.2% (+11.5pts vs baseline) | Codeshare crisis (LATAM -100.0, BA 0.0)
- **YW**: Mishandling 25.7% (+9.1pts vs baseline) | Problemas técnicos masivos (5 de 12 incidentes)

### **Valores SHAP y Evidencia Operativa:**
- **IB**: Problemas concentrados en **codeshare** y flota **A33ACMI/A321**
- **YW**: Problemas concentrados en **incidentes técnicos** y **cambios de aircraft** (3 cambios)

### **Patrones Diferenciados:**
- **IB**: Crisis específica en **partnerships** (dispersión 121.4 puntos entre códigos)
- **YW**: Crisis en **operaciones técnicas** (cambio de rueda desde MAD, 155 conexiones afectadas)

**📊 DIAGNÓSTICO:** **Causa específica de compañía** - IB y YW muestran drivers y patrones operativos claramente diferenciados dentro de Economy SH.

---

## **B. Business Short Haul:**

**NODOS IDENTIFICADOS:**
- ✅ **Global/SH/Business/IB** - Anomalía: -12.4 puntos NPS  
- ✅ **Global/SH/Business/YW** - Anomalía: -16.28 puntos NPS

**ANÁLISIS COMPARATIVO:**

### **Drivers Principales:**
- **IB**: Mishandling 29.2% (+11.5pts) | Problemas concentrados en **perfiles específicos** (A350 C, ASIA, BA CodeShare)
- **YW**: Mishandling 25.7% (+9.1pts) | **Operación extremadamente limitada** (solo 7-8 encuestas vs volúmenes normales)

### **Valores SHAP y Evidencia Operativa:**
- **IB**: Impacto **concentrado por perfil** (A350 C: -100.0 NPS, ASIA: -100.0 NPS)
- **YW**: **Crisis sistémica** con operación defensiva (posibles cancelaciones masivas)

### **Patrones Diferenciados:**
- **IB**: Problemas de **calidad específica** en segmentos premium (Load Factor bajo: 75.0% vs 81.0%)
- **YW**: **Disrupción operativa masiva** con volumen crítico bajo indicando cancelaciones

**📊 DIAGNÓSTICO:** **Causa específica de compañía** - IB y YW exhiben patrones operativos fundamentalmente diferentes: IB con problemas de calidad concentrados vs YW con crisis sistémica y operación defensiva.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. Short Haul - Análisis de Cabinas:**

### **CONVERGENCIA EN CAUSA RAÍZ:**
- **Economy SH**: Mishandling crítico (IB: 29.2%, YW: 25.7%) + problemas técnicos
- **Business SH**: Mishandling crítico (IB: 29.2%, YW: 25.7%) + problemas técnicos

### **DIVERGENCIA EN REACTIVIDAD:**

**Economy SH:**
- **IB**: -7.84 puntos | Impacto moderado con resistencia relativa
- **YW**: -12.63 puntos | Impacto severo con mayor sensibilidad

**Business SH:**
- **IB**: -12.4 puntos | Impacto concentrado en perfiles específicos (A350 C: -100.0)
- **YW**: -16.28 puntos | Colapso sistémico con operación defensiva

### **PATRÓN DE CONSISTENCIA ENTRE COMPAÑÍAS:**
- ✅ **Consistente**: En ambas compañías, **Business es más reactivo** que Economy ante los mismos problemas operativos
- ✅ **Consistente**: YW muestra **mayor vulnerabilidad** que IB en ambas cabinas

**📊 DIAGNÓSTICO SH:** **Causa común de radio con reactividad diferencial por cabina** - Misma causa operativa (mishandling + problemas técnicos) pero Business SH muestra sistemáticamente mayor sensibilidad que Economy SH en ambas compañías.

---

## **B. Long Haul - Análisis de Cabinas:**

### **CONVERGENCIA EN CAUSA RAÍZ:**
- **Economy LH**: Mishandling 28.3% (+10.9pts) + problemas flota A33ACMI
- **Business LH**: Mishandling 28.3% (+10.9pts) + problemas técnicos específicos
- **Premium LH**: Mishandling 28.3% (+10.9pts) + fallas A350 en MAD-SCL

### **PROGRESIÓN LÓGICA DE REACTIVIDAD:**

| Cabina | Anomalía NPS | Reactividad | Patrón |
|--------|--------------|-------------|---------|
| **Economy LH** | -8.63 pts | **Moderada** | Resistencia relativa |
| **Business LH** | -9.08 pts | **Alta** | Baja tolerancia a disrupciones |
| **Premium LH** | **-51.08 pts** | **EXTREMA** | Colapso total ante problemas |

### **ANÁLISIS DE AMORTIGUACIÓN:**
- **Economy LH**: Actúa como **amortiguador relativo** - mismo problema operativo, menor impacto
- **Premium LH**: Actúa como **amplificador** - problemas específicos (A350 MAD-SCL) generan colapso desproporcionado

### **EVIDENCIA DE PROGRESIÓN:**
- ✅ **Escalada lógica**: Economy → Business → Premium en sensibilidad
- ✅ **Mismo driver**: Mishandling 28.3% afecta a todas las cabinas
- ✅ **Impacto diferencial**: Premium colapsa (-51.08) mientras Economy resiste (-8.63)

**📊 DIAGNÓSTICO LH:** **Causa común de radio con progresión lógica de reactividad por cabina** - Misma causa operativa crítica (mishandling + problemas técnicos) pero con escalada sistemática de sensibilidad: Economy (resistente) → Business (sensible) → Premium (extremadamente vulnerable).

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. Comparación Entre Radios:**

### **AFECTACIÓN CONFIRMADA:**
- ✅ **Short Haul afectado**: Economy (-1.22 a -12.63 pts) | Business (-12.4 a -16.28 pts)
- ✅ **Long Haul afectado**: Economy (-8.63 pts) | Business (-9.08 pts) | Premium (-51.08 pts)

### **CONVERGENCIA EN DRIVERS PRINCIPALES:**

**Drivers Comunes Identificados:**
- **Mishandling crítico**: SH (25.7-29.2%) vs LH (28.3%) - **Convergencia total**
- **Problemas técnicos**: SH (cambios aircraft, rueda MAD) vs LH (A350, A33ACMI) - **Convergencia operativa**
- **Incidentes masivos**: SH (12 incidentes YW) vs LH (116 incidentes) - **Escalada proporcional**

### **CONSISTENCIA EN VALORES SHAP Y EVIDENCIA:**

| Radio | Factor Crítico | Impacto Operativo | Evidencia NCS |
|-------|----------------|-------------------|---------------|
| **SH** | Mishandling 25.7-29.2% | Cambios aircraft, problemas técnicos | 12 incidentes |
| **LH** | Mishandling 28.3% | A350/A33ACMI, vuelo IB266 | 116 incidentes |

**✅ CONVERGENCIA CONFIRMADA**: Misma causa raíz operativa con manifestación escalada por complejidad del radio.

---

## **B. Coherencia con Nodo Global:**

### **IMPACTO AGREGADO DEL GLOBAL:**
- **Global NPS**: -3.34 puntos (21.13 vs 24.47 baseline)
- **Composición**: Reflejo coherente de SH + LH ponderado por volumen

### **VALIDACIÓN DE COHERENCIA:**

**Drivers Globales vs Radios:**
- **Mishandling Global**: 28.3% vs 17.4% (+10.9pts) ✅ **Coherente con ambos radios**
- **Incidentes Global**: 116 NCS ✅ **Suma coherente** (SH: 12 + LH: ~104)
- **OTP Global**: 83.9% vs 84.8% ✅ **Refleja deterioro en ambos radios**

### **PATRÓN DE AMPLIFICACIÓN:**

**Global NO atenúa - AMPLIFICA selectivamente:**
- **Flota A33ACMI**: Global (-57.9) = LH severity
- **CodeShare LATAM**: Global (-54.5) = SH severity  
- **Vuelo IB266**: Global (155 conexiones) = LH cascade effect

### **EVIDENCIA DE AGREGACIÓN COHERENTE:**
- ✅ **Sin efectos compensatorios**: No hay normalidad en Global mientras radios sufren
- ✅ **Amplificación selectiva**: Global refleja los peores impactos de cada radio
- ✅ **Dispersión extrema**: Global muestra spreads máximos (CodeShare: 104.5pts, Fleet: 101.8pts)

---

## **📊 DIAGNÓSTICO FINAL:**

**Causa global homogénea con manifestación escalada por complejidad operativa** - Ambos radios (SH y LH) convergen completamente en la misma causa raíz (mishandling crítico 28.3% + problemas técnicos masivos), pero LH muestra mayor severidad por complejidad operativa (116 vs 12 incidentes), mientras el Global amplifica selectivamente los peores impactos de cada radio sin efectos compensatorios, confirmando una crisis operativa sistémica del 24 de agosto de 2025.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA PRINCIPAL: CRISIS DE MISHANDLING EXTREMO**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Colapso sistémico en los procesos de manejo de equipajes causado por una cascada de problemas técnicos que saturó la capacidad operativa de handling, generando una experiencia degradada masiva que impactó desproporcionadamente según el perfil y expectativas del cliente.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Global (Nodo Padre)
- **Alcance total:** Todos los subsegmentos bajo Global experimentaron esta causa
- **Impacto:** -3.34 puntos NPS (21.13 vs 24.47 baseline)

**OUTPUT CAUSAL DETALLADO:**
```
MISHANDLING CRÍTICO: 28.3% vs 17.4% promedio (+10.9 puntos - +62% incremento)
↓
CASCADA OPERATIVA INICIADA POR:
• Problemas técnicos masivos (cambio de rueda desde MAD)
• 116 incidentes NCS totales
• Vuelo crítico IB266 (SDQ-MAD): 155 conexiones afectadas
• 3 cambios de aeronave forzados
↓
IMPACTO DIFERENCIAL POR PERFIL:
• Premium LH: -51.08 pts (extrema sensibilidad)
• Business: -9.08 a -16.28 pts (alta sensibilidad)  
• Economy: -1.22 a -12.63 pts (sensibilidad moderada)
```

**MÉTRICAS CLAVE CONSOLIDADAS:**
- **Indicadores Operativos:** Mishandling 28.3% (+10.9pts), OTP 83.9% (-0.9pts), Load Factor 88.6% (+1.1pts)
- **NPS por Segmento:** Premium LH (-51.08), Business LH (-9.08), Economy LH (-8.63)
- **Rutas Críticas:** MAD-SCL (NPS -33.3), LIN-MAD (NPS -25.0), DSS-MAD (NPS 14.3)
- **Verbatims:** No disponibles (limitación crítica del análisis)

**SUBSEGMENTOS AFECTADOS CONFIRMADOS:**
✅ Global/LH (Economy/Business/Premium) ✅ Global/SH (Economy/Business) ✅ Todas las compañías (IB/YW) ✅ Todas las flotas (especialmente A33ACMI, A350) ✅ Todos los mercados geográficos (con variación de intensidad)

---

## **CAUSA SECUNDARIA: PROBLEMAS TÉCNICOS ESPECÍFICOS DE FLOTA**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Fallas técnicas concentradas en flotas específicas (A350, A33ACMI) que requirieron cambios de aeronave y generaron retrasos masivos, amplificando el impacto del mishandling y creando un efecto dominó en conexiones y rutas intercontinentales.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Global/LH (Long Haul completo)
- **Alcance:** Todos los subsegmentos LH (Economy/Business/Premium)
- **Impacto:** Economy LH (-8.63), Business LH (-9.08), Premium LH (-51.08)

**OUTPUT CAUSAL DETALLADO:**
```
PROBLEMAS TÉCNICOS CRÍTICOS:
• A33ACMI: NPS -91.7 (12 surveys) - Colapso total
• A350: Problemas en MAD-SCL, NPS -28.6 a -100.0
• Cambio de rueda desde MAD → Efecto cascada
↓
IMPACTO OPERATIVO ESPECÍFICO:
• Vuelo IB264 (OPO-MAD): Reprogramado 4h 55min
• 155 conexiones perdidas en cascada
• 2 problemas técnicos + 2 cambios de aircraft
↓
CONCENTRACIÓN GEOGRÁFICA:
• MAD-SCL: Ruta epicentro (NPS -33.3)
• América del Sur: Región más afectada (NPS -25.0 a -20.0)
• Mercados premium intercontinentales colapsaron
```

**MÉTRICAS CLAVE CONSOLIDADAS:**
- **Flotas Críticas:** A33ACMI (NPS -91.7), A350 C (NPS -100.0), A350 next (NPS -28.6)
- **Incidentes Técnicos:** 6 incidentes específicos, 155 conexiones afectadas
- **Rutas Impactadas:** MAD-SCL (NPS -33.3), OPO-MAD (problemas técnicos documentados)
- **Mercados:** ASIA (NPS -100.0), América del Sur (NPS -25.0)

**SUBSEGMENTOS AFECTADOS CONFIRMADOS:**
✅ Global/LH/Economy ✅ Global/LH/Business ✅ Global/LH/Premium ✅ Flotas A350/A33ACMI ✅ Rutas intercontinentales ✅ CodeShare críticos (BA, LATAM)

---

## **CAUSA TERCIARIA: CRISIS ESPECÍFICA DE CODESHARE**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Los problemas operativos afectaron desproporcionadamente las operaciones de código compartido, donde los estándares de servicio y procesos de coordinación entre aerolíneas se vieron comprometidos, generando experiencias extremadamente negativas en partnerships críticos.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Global/SH/Economy (Mayor volumen de operaciones codeshare)
- **Alcance:** Todos los subsegmentos SH con operaciones codeshare
- **Impacto:** Economy SH/IB (-7.84), con dispersión extrema en codeshare

**OUTPUT CAUSAL DETALLADO:**
```
COLAPSO CODESHARE CRÍTICO:
• LATAM: NPS -100.0 (6 surveys) - Experiencia devastadora total
• British Airways: NPS -25.0 a -66.7 - Partnership comprometido
• Dispersión extrema: 121.4 puntos entre códigos (IB vs LATAM)
↓
PROBLEMAS DE COORDINACIÓN:
• Procesos de handling compartido colapsaron
• Estándares de servicio no mantenidos
• Comunicación cliente deteriorada en partnerships
↓
IMPACTO REPUTACIONAL:
• Daño a relaciones comerciales críticas
• Experiencia inconsistente entre códigos
• Amplificación del problema operativo base
```

**MÉTRICAS CLAVE CONSOLIDADAS:**
- **CodeShare Críticos:** LATAM (-100.0), BA (-25.0 a -66.7), AA (-13.3)
- **Dispersión:** 104.5 puntos en Global, 121.4 puntos en SH/Economy/IB
- **Contraste:** IB directo (NPS 21.4-25.4) vs CodeShare (NPS -100.0 a 0.0)
- **Volumen:** Concentrado en operaciones SH Economy (mayor muestra)

**SUBSEGMENTOS AFECTADOS CONFIRMADOS:**
✅ Global/SH/Economy/IB ✅ Global/SH/Business/IB ✅ Global/LH (partnerships intercontinentales) ✅ Todas las rutas con operaciones codeshare ✅ Mercados internacionales dependientes de partnerships

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 24 de agosto de 2025 experimentó una caída generalizada del NPS a nivel global, deteriorándose de 24.47 a 21.13 puntos (-3.34 puntos), causada por una crisis operativa multidimensional centrada en problemas críticos de manejo de equipajes que alcanzaron el 28.3% versus un promedio de 17.4%. Esta crisis se manifestó de manera diferenciada según el radio y clase de servicio: en Long Haul, Premium colapsó dramáticamente de 28.87 a -22.22 puntos (-51.08 puntos) debido a fallas técnicas específicas en la flota A350 operando la ruta MAD-SCL, mientras que Business LH cayó de 35.39 a 26.32 puntos (-9.08 puntos) por problemas concentrados en conexiones desde América del Sur, y Economy LH se deterioró de 19.16 a 10.53 puntos (-8.63 puntos) por la crisis en operaciones ACMI del A333. En Short Haul, las caídas fueron más moderadas pero igualmente significativas: Economy SH registró descensos entre -1.22 y -12.63 puntos según la compañía, mientras que Business SH experimentó deterioros de -12.4 a -16.28 puntos, ambos impulsados por los mismos problemas de mishandling y una cascada de 116 incidentes operativos que incluyeron cambios masivos de aeronave y problemas técnicos críticos.

Las rutas más severamente afectadas fueron MAD-SCL con un NPS de -33.3 puntos en Premium, LIN-MAD con -25.0 puntos, y las conexiones desde América del Sur que registraron NPS de -25.0 puntos, mientras que los grupos de clientes más reactivos fueron los pasajeros Premium de largo radio (especialmente en flota A350), clientes asiáticos que experimentaron NPS de -100.0 puntos, y usuarios de operaciones codeshare con LATAM (-100.0 NPS) y British Airways (-25.0 a -66.7 NPS), evidenciando que los segmentos de mayor expectativa y las operaciones de partnership fueron desproporcionadamente vulnerables a la crisis operativa del día.

**ECONOMY SH: Crisis Operativa Diferenciada por Compañía**
La cabina Economy de SH experimentó un deterioro significativo durante el 24 de agosto de 2025, con IB registrando un NPS de 16.09 (caída de -7.84 puntos) y YW alcanzando 50.0 puntos (deterioro de -12.63 puntos respecto al baseline). La causa principal fue una crisis de mishandling que alcanzó el 29.2% en IB y 25.7% en YW, muy por encima de los promedios de 17.7% y 16.6% respectivamente, complementada por problemas específicos de codeshare en IB (LATAM con NPS -100.0 y BA con NPS 0.0) y una cascada de incidentes técnicos en YW que incluyó 5 problemas técnicos críticos y cambios masivos de aeronave. Este deterioro se reflejó especialmente en rutas como DUS-MAD con NPS 14.3 y la concentración de problemas en Europa (NPS -8.9 en IB), mientras que los perfiles más reactivos incluyen las operaciones codeshare, la flota A33ACMI (NPS -40.0), y los viajeros de negocio que mostraron mayor sensibilidad a las disrupciones operativas.

**BUSINESS SH: Colapso Concentrado en Perfiles Premium**
El segmento Business de SH experimentó un deterioro severo, con IB registrando un NPS de 19.0 (caída de -12.4 puntos) y YW alcanzando 50.0 puntos (deterioro de -16.28 puntos vs el período anterior). Esta evolución se explica principalmente por el mismo factor de mishandling crítico (29.2% en IB, 25.7% en YW) que afectó desproporcionadamente a los clientes de mayor expectativa, siendo especialmente visible en perfiles específicos como A350 C (NPS -100.0), clientes asiáticos (NPS -100.0), y operaciones codeshare con BA (NPS -66.7), mientras que YW experimentó una crisis sistémica con operación extremadamente limitada que sugiere cancelaciones masivas defensivas ante la magnitud de los problemas técnicos.

**ECONOMY LH: Crisis ACMI y Problemas Técnicos Masivos**
La cabina Economy de LH experimentó un deterioro significativo durante el 24 de agosto de 2025, registrando un NPS de 10.53 (caída de -8.63 puntos) respecto a la semana anterior. La causa principal fue una crisis operativa centrada en problemas críticos de la flota A33ACMI que registró un NPS devastador de -91.7 puntos con prácticamente todos los clientes convertidos en detractores extremos, complementada por un incremento alarmante del mishandling al 28.3% versus el 17.4% promedio y múltiples incidentes técnicos que incluyeron el vuelo crítico IB266 con 155 conexiones afectadas. Este deterioro se reflejó especialmente en rutas como MAD-SCL con NPS 0.0 y BOS-MAD también con NPS 0.0, mientras que los perfiles más reactivos incluyen los clientes business/work (NPS 0.0 con 13 encuestas) y los mercados geográficos de Europa (NPS -36.8) y América Norte (NPS -15.4).

**BUSINESS LH: Cascada de Problemas en Conexiones Sudamericanas**
La cabina Business de LH experimentó un deterioro notable, registrando un NPS de 26.32 (caída de -9.08 puntos) respecto al período anterior. Los drivers principales fueron el mismo factor crítico de mishandling del 28.3% y una cascada de problemas operativos iniciada por fallas técnicas que requirieron cambios de rueda desde MAD y generaron reprogramaciones de hasta 4 horas 55 minutos, impactando especialmente las rutas de conexión desde América del Sur donde el NPS colapsó a -25.0 puntos, mientras que España mantuvo un desempeño positivo con NPS +54.5, y los perfiles más reactivos fueron los pasajeros de conexiones internacionales largas que mostraron mayor vulnerabilidad a las disrupciones operativas masivas del día.

**PREMIUM LH: Colapso Total por Fallas Técnicas A350**
El segmento Premium de LH experimentó un colapso dramático durante el 24 de agosto de 2025, registrando un NPS de -22.22 (deterioro de -51.08 puntos) vs la semana anterior. Las causas dominantes fueron una combinación letal de mishandling extremo del 28.3% y fallas técnicas críticas concentradas en la flota A350 que operaba la ruta estratégica MAD-SCL, donde el NPS colapsó a -33.3 puntos, especialmente evidentes en esta ruta intercontinental premium y entre clientes de ocio del segmento premium que demostraron ser extremadamente vulnerables a las disrupciones técnicas, convirtiendo prácticamente toda la experiencia A350 en detractores con NPS de -28.6 puntos y generando un impacto desproporcionado que explica la magnitud excepcional de esta anomalía.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 11
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-23 to 2025-08-23:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 8 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH/Business/IB, Global/SH/Economy, Global/SH/Economy/IB)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. ECONOMY SHORT HAUL**

**Nodos identificados:**
- ✅ **Global/SH/Economy** (existe)
- ✅ **Global/SH/Economy/IB** (existe)
- ❌ **Global/SH/Economy/YW** (NO existe)

**Análisis disponible:** Solo tenemos datos del nodo Global/SH/Economy/IB, que muestra:
- Anomalía negativa: -7.94 puntos NPS
- Driver principal: Crisis de equipajes (Mishandling 29.2% vs 17.7% +11.5pts)
- Incidente específico: 165 equipajes retenidos en BCN

**Diagnóstico Economy SH:** **Análisis incompleto por ausencia del nodo YW** - No es posible determinar si la causa es específica de IB o común a la cabina SH Economy, ya que falta la evidencia comparativa de Vueling.

---

## **B. BUSINESS SHORT HAUL**

**Nodos identificados:**
- ✅ **Global/SH/Business** (no existe como nodo separado en los datos)
- ✅ **Global/SH/Business/IB** (existe)
- ❌ **Global/SH/Business/YW** (NO existe)

**Análisis disponible:** Solo tenemos datos del nodo Global/SH/Business/IB, que muestra:
- Anomalía negativa: -2.4 puntos NPS
- Driver principal: Crisis de equipajes (Mishandling 29.2% vs 17.7% +11.5pts)
- Impacto concentrado: Clientes Business españoles (NPS 0.0)
- Mismo incidente: 165 equipajes retenidos en BCN

**Diagnóstico Business SH:** **Análisis incompleto por ausencia del nodo YW** - No es posible determinar si la causa es específica de IB o común a la cabina SH Business, ya que falta la evidencia comparativa de Vueling.

---

## **CONCLUSIÓN DEL PASO 1**

**Limitación crítica identificada:** La ausencia sistemática de nodos YW (Vueling) en ambas cabinas Short Haul impide realizar el diagnóstico comparativo requerido. Ambos nodos IB muestran el mismo driver principal (crisis de equipajes en BCN), pero sin la contraparte YW no podemos confirmar si es una causa específica de Iberia o afectó a toda la operación Short Haul del grupo.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ **PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)**

## **A. SHORT HAUL - ANÁLISIS DE CABINAS**

### **Comparación Economy SH vs Business SH:**

**PATRONES CONVERGENTES IDENTIFICADOS:**
- **Driver común**: Ambas cabinas afectadas por la **misma crisis de equipajes** (Mishandling 29.2% vs 17.7% baseline)
- **Incidente idéntico**: 165 equipajes retenidos en BCN impacta ambas cabinas
- **Rutas críticas compartidas**: BCN-MAD como epicentro en ambos segmentos
- **Evidencia operativa**: Mismos 25 incidentes NCS afectan ambas cabinas

**REACTIVIDAD DIFERENCIAL DETECTADA:**
- **Economy SH/IB**: Anomalía -7.94 puntos (mayor impacto)
- **Business SH/IB**: Anomalía -2.4 puntos (menor impacto)
- **Sensibilidad**: Economy mostró **3.3x mayor reactividad** al mismo problema operativo

**Diagnóstico Short Haul:** **Causa común al radio con reactividad diferencial por cabina** - Ambas cabinas sufren la misma crisis operativa (equipajes BCN), pero Economy muestra mayor sensibilidad al impacto que Business.

---

## **B. LONG HAUL - ANÁLISIS DE CABINAS**

### **Comparación Economy LH vs Business LH vs Premium LH:**

**PARADOJA OPERATIVA COMÚN:**
- **Patrón convergente**: Las tres cabinas muestran **anomalías POSITIVAS** pese a problemas operativos severos:
  - **Economy LH**: +8.72 puntos NPS
  - **Business LH**: +19.6 puntos NPS  
  - **Premium LH**: -3.87 puntos NPS (única negativa)

**DRIVERS OPERATIVOS COMPARTIDOS:**
- **Mishandling crítico**: 28.3% vs 17.4% baseline (común a las tres)
- **27 incidentes NCS**: Afectan toda la operación LH
- **Load Factor elevado**: Sobrecarga operativa sistémica

**REACTIVIDAD INVERSA DETECTADA:**
- **Premium LH**: Única cabina que reacciona **negativamente** (-3.87 pts) a los problemas operativos
- **Economy/Business LH**: Muestran **mejoras paradójicas** pese a la crisis operativa
- **Progresión lógica**: A mayor nivel de servicio, mayor sensibilidad a problemas operativos

**Diagnóstico Long Haul:** **Causa común al radio con reactividad inversa por nivel de servicio** - Todas las cabinas sufren la misma crisis operativa masiva (270 incidentes, mishandling crítico), pero Premium muestra la única reacción negativa esperada, mientras Economy y Business presentan anomalías positivas paradójicas.

---

## **CONCLUSIÓN DEL PASO 2**

**Short Haul**: Causa operativa común (crisis equipajes BCN) con impacto proporcional al nivel de servicio.

**Long Haul**: Causa operativa común (crisis sistémica masiva) con reactividad inversa - solo Premium reacciona negativamente como sería esperado, sugiriendo factores compensatorios no identificados en Economy y Business.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 **PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL**

## **A. COMPARACIÓN ENTRE RADIOS**

### **Afectación de Ambos Radios Confirmada:**
- ✅ **Short Haul**: Anomalías negativas (-7.94 Economy, -2.4 Business)
- ✅ **Long Haul**: Anomalías mixtas (+8.72 Economy, +19.6 Business, -3.87 Premium)

### **Convergencia Parcial en Drivers:**

**DRIVERS COMPARTIDOS:**
- **Crisis de equipajes**: Mishandling crítico en ambos radios (28.3-29.2% vs baselines 17.4-17.7%)
- **Incidente BCN**: 165 equipajes retenidos impacta ambos radios
- **Deterioro puntualidad**: OTP15 degradado en ambos (80.3% SH, 83.9% LH vs baselines)

**DRIVERS DIVERGENTES:**
- **Magnitud de incidentes**: SH (25 incidentes) vs LH (270 incidentes) - **10.8x diferencia**
- **Load Factor**: SH (impacto menor) vs LH (sobrecarga crítica 92.4%)
- **Complejidad operativa**: SH (problemas localizados) vs LH (crisis sistémica masiva)

---

## **B. COHERENCIA CON NODO GLOBAL**

### **Paradoja Global Identificada:**

**NODO GLOBAL**: Anomalía positiva +7.32 puntos NPS
**RADIOS CONSTITUYENTES**:
- Short Haul: Anomalías negativas (impacto negativo neto)
- Long Haul: Anomalías mayoritariamente positivas (Economy +8.72, Business +19.6)

### **Análisis de Coherencia:**

**✅ COHERENCIA OPERATIVA**: El Global refleja correctamente los **270 incidentes masivos** y **crisis de equipajes sistémica**

**❌ INCOHERENCIA NPS**: El Global (+7.32) no refleja el **impacto negativo de Short Haul** pero sí amplifica las **anomalías positivas paradójicas de Long Haul**

**EFECTO DOMINANTE**: Long Haul domina estadísticamente el resultado Global, enmascarando los problemas reales de Short Haul

---

## **CONCLUSIÓN DEL PASO 3**

**Diagnóstico de Alcance:** **Causas globales con manifestación asimétrica por radio** - Ambos radios sufren la misma crisis operativa sistémica (equipajes, incidentes masivos, puntualidad), pero Long Haul presenta anomalías positivas paradójicas que dominan el resultado Global, ocultando el impacto negativo real y esperado en Short Haul.

**Implicación Crítica:** El nodo Global (+7.32) presenta una **falsa señal positiva** que enmascara problemas operativos severos, siendo dominado por las anomalías paradójicas de Long Haul mientras ignora el deterioro real capturado en Short Haul.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 **PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS**

## **CAUSA 1: CRISIS SISTÉMICA DE EQUIPAJES**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Falla operativa crítica en el manejo de equipajes que generó un efecto cascada desde Barcelona hacia toda la red, afectando tanto la operación doméstica como las conexiones internacionales. La limitación de peso en BCN desencadenó retenciones masivas que impactaron rotaciones de aeronaves y conexiones posteriores.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Global/SH/Economy (alcance más amplio de clientes)

**OUTPUT CAUSAL DETALLADO:**
- **NPS Impact:** -7.04 puntos (32.40 vs 25.36 baseline)
- **Driver Principal:** Mishandling 28.3% vs 17.4% promedio (+10.9 puntos - aumento del 62%)
- **Incidente Específico:** 165 equipajes retenidos en BCN por limitación de peso
- **Cascada Operativa:** 25 incidentes reportados, 8 retrasos, 6 cancelaciones

**SUBSEGMENTOS AFECTADOS:** Esta causa afecta a todos los nodos bajo Global, incluyendo:
- Global/SH/Economy/IB (impacto -7.94 puntos)
- Global/SH/Business/IB (impacto -2.4 puntos)
- Global/LH/Economy (paradójicamente +8.72 puntos)
- Global/LH/Business (paradójicamente +19.6 puntos)
- Global/LH/Premium (impacto -3.87 puntos - única reacción negativa esperada en LH)

**MÉTRICAS CLAVE:**
- **Rutas Críticas:** BCN-MAD (epicentro), DBV-MAD, HAM-MAD, MAD-EZE (efecto cascada)
- **Flota Afectada:** A33ACMI (-16.7 NPS), A320neo, A350 C (NPS -30.0 en LH)
- **Perfil Impacto:** CodeShare AA (-75.0 NPS), LATAM (-16.7 NPS)
- **Geografía:** Madrid como hub amplificador de problemas upstream

---

## **CAUSA 2: SOBRECARGA OPERATIVA SISTÉMICA**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Operación al límite de capacidad que amplificó todos los demás problemas operativos. El Load Factor elevado creó un efecto dominó donde cualquier disrupción (como la crisis de equipajes) se magnificó por la falta de flexibilidad operativa para absorber problemas.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Global/LH (mayor complejidad operativa)

**OUTPUT CAUSAL DETALLADO:**
- **Load Factor Crítico:** 88.6% vs 87.5% promedio (mayor ocupación)
- **270 Incidentes Masivos:** Día excepcionalmente problemático
- **OTP15 Deteriorado:** 83.9% vs 84.8% promedio (peor puntualidad)
- **Rotaciones Comprometidas:** Cambios de aeronave, retrasos extremos hasta 3h55min

**SUBSEGMENTOS AFECTADOS:** Esta causa afecta a toda la operación Global, manifestándose diferentemente:
- Short Haul: Amplifica problemas locales (BCN-MAD)
- Long Haul: Crea crisis sistémica masiva (270 incidentes)
- Premium: Única cabina que reacciona negativamente como esperado

**MÉTRICAS CLAVE:**
- **Incidentes Totales:** 270 (vs operación normal)
- **Conexiones Perdidas:** 82 incidentes específicos
- **Cambios Equipo:** 44 incidentes
- **Vuelo Más Crítico:** IB0355 (2 incidentes)

---

## **CAUSA 3: VULNERABILIDAD DE OPERACIONES EXTERNAS**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Las operaciones CodeShare y ACMI mostraron mayor vulnerabilidad a las disrupciones operativas, sugiriendo menor control de calidad o protocolos de contingencia menos efectivos en operaciones no directamente controladas por Iberia.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Global/SH/Economy/IB (donde se concentran más CodeShare)

**OUTPUT CAUSAL DETALLADO:**
- **American Airlines CodeShare:** NPS -75.0 (devastador)
- **LATAM CodeShare:** NPS -16.7 (severo)
- **Flota A33ACMI:** NPS -16.7 (problemas específicos)
- **Dispersión CodeShare:** 117.9 puntos (indica problemas específicos de socios)

**SUBSEGMENTOS AFECTADOS:** Esta causa se manifiesta en múltiples nodos:
- Global/SH/Economy/IB: CodeShare AA/LATAM críticos
- Global/LH/Business: CodeShare QR (-33.3 NPS)
- Global/LH: A350 C devastada (-30.0 NPS en Business, -6.7 en general)

**MÉTRICAS CLAVE:**
- **CodeShare Críticos:** AA, LATAM, QR con NPS negativos severos
- **Flota Externa:** A33ACMI, A350 C con problemas específicos
- **Diferencial Control:** Operación propia vs externa muestra gaps significativos

---

## **SÍNTESIS CAUSAL**

Las tres causas identificadas operaron simultáneamente el 23 de agosto de 2025, creando una **tormenta perfecta operativa** donde:

1. **Crisis de equipajes** (causa primaria) desencadenó problemas cascada
2. **Sobrecarga operativa** (causa amplificadora) magnificó todos los impactos  
3. **Vulnerabilidad externa** (causa estructural) concentró el daño en operaciones menos controladas

El resultado fue una **paradoja de NPS Global positivo** que enmascaró problemas operativos severos, dominado por anomalías positivas inexplicadas en Long Haul que contrastan con el impacto negativo esperado y confirmado en Short Haul.

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 **SÍNTESIS EJECUTIVA:**

El 23 de agosto de 2025 presentó una paradoja crítica en el comportamiento del NPS, donde el segmento Global registró una mejora aparente de +7.32 puntos (alcanzando 31.79 vs baseline 24.47), pero esta subida enmascaró una crisis operativa severa con 270 incidentes documentados. La anomalía se explica por tres causas principales: una crisis sistémica de equipajes originada por la retención de 165 equipajes en Barcelona por limitación de peso, una sobrecarga operativa generalizada con Load Factor crítico del 88.6%, y vulnerabilidades específicas en operaciones CodeShare y flotas externas. Estas causas generaron impactos diferenciados donde Long Haul mostró subidas paradójicas de NPS (+8.72 puntos en Economy LH alcanzando 27.88, y +19.6 puntos en Business LH llegando a 55.0) que contrastan completamente con la evidencia operativa, mientras que Short Haul experimentó las caídas esperadas (-7.04 puntos en Economy SH bajando a 32.40, y -2.4 puntos en Business SH descendiendo a 29.0) y Premium LH fue la única cabina de largo radio que reaccionó negativamente como era previsible (-3.87 puntos cayendo a 25.0).

Las rutas más críticas incluyen BCN-MAD como epicentro del problema de equipajes, MAD-EZE y DBV-MAD afectadas por efectos cascada, y MAD-UIO con NPS devastador de 0.0. Los grupos más reactivos fueron los clientes de CodeShare (American Airlines con NPS -75.0, LATAM -16.7), pasajeros de flota A350 C (NPS -30.0 en Business), viajeros corporativos españoles, y operaciones ACMI que mostraron mayor vulnerabilidad a las disrupciones operativas que las operaciones directas de Iberia.

**ECONOMY SH: Crisis de Equipajes Impacta Severamente**
La cabina Economy de Short Haul experimentó un deterioro significativo durante el 23 de agosto de 2025, registrando una caída de -7.04 puntos que llevó el NPS de 39.44 a 32.40. La causa principal fue la crisis de equipajes con un Mishandling crítico del 28.3% (vs 17.4% promedio), desencadenada por la retención de 165 equipajes en Barcelona por limitación de peso, complementada por 25 incidentes operativos que incluyeron 8 retrasos y 6 cancelaciones. Este deterioro se reflejó especialmente en rutas como MAD-TIA (NPS 0.0), DBV-MAD (NPS 14.3) y BCN-MAD (NPS 42.9), mientras que los perfiles más reactivos incluyen clientes de CodeShare American Airlines (NPS -25.0), flota A33ACMI (NPS -16.7) y pasajeros de América del Norte.

**BUSINESS SH: Impacto Moderado por Segmentación**
El segmento Business de Short Haul mostró una caída más contenida de -2.4 puntos, registrando un NPS de 29.0 vs 31.4 del período anterior. Esta evolución se explica principalmente por la misma crisis de equipajes (Mishandling 29.2% vs 17.7% promedio) pero con menor reactividad que Economy, siendo especialmente visible en rutas como BCN-MAD (NPS 0.0) y MAD-PRG (NPS 0.0), y entre perfiles de viajeros corporativos españoles que mostraron mayor sensibilidad (NPS 0.0) comparado con clientes de leisure europeos.

**ECONOMY LH: Subida Paradójica Inexplicada**
La cabina Economy de Long Haul experimentó una mejora paradójica de +8.72 puntos, registrando un NPS de 27.88 vs baseline 19.16, contradiciendo completamente la evidencia operativa de 270 incidentes masivos y Mishandling del 28.3%. Esta subida anómala carece de explicación lógica dado el contexto de crisis operativa severa, sugiriendo factores compensatorios no identificados o sesgos en la recolección de feedback que requieren investigación adicional para entender cómo problemas operativos tan severos coexistieron con percepciones aparentemente positivas.

**BUSINESS LH: Mejora Excepcional Contra Evidencia**
La cabina Business de Long Haul registró una subida extraordinaria de +19.6 puntos, alcanzando un NPS de 55.0 vs 35.4 del período anterior, representando la mayor paradoja del análisis. Los drivers aparentes contradicen totalmente esta mejora, con 27 incidentes operativos, problemas severos en flota A350 C (NPS -100.0 con todos detractores), y deterioro generalizado en métricas operativas, haciendo esta subida completamente inexplicable y sugiriendo la necesidad de auditar la metodología de captura de NPS para este segmento específico.

**PREMIUM LH: Única Reacción Coherente**
El segmento Premium de Long Haul mostró la única reacción coherente con la evidencia operativa, registrando una caída de -3.87 puntos que llevó el NPS de 28.87 a 25.0. Las causas dominantes fueron la crisis de equipajes (Mishandling 28.3%), sobrecarga operativa (Load Factor 92.4%) y 27 incidentes documentados, especialmente evidentes en rutas como EZE-MAD (NPS 0.0) y entre perfiles de flota A333 (NPS -66.7) y pasajeros de América del Norte, confirmando que los clientes Premium mantienen mayor sensibilidad a las disrupciones operativas.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 8
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-22 to 2025-08-22:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 7 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH/Economy/IB, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. Economy Short Haul:**

**✅ AMBOS NODOS PRESENTES:**
- **Global/SH/Economy/IB**: Analizado
- **Global/SH/Economy/YW**: Analizado

**COMPARACIÓN DE PATRONES:**

| **Dimensión** | **IB** | **YW** | **Convergencia** |
|---------------|---------|---------|------------------|
| **Driver Principal** | Mishandling +11.5pts (29.2%) | Mishandling +9.1pts (25.7%) | ✅ **CONVERGENTE** |
| **NPS Impact** | -2.53 pts (deterioro) | +12.6 pts (mejora) | ❌ **DIVERGENTE** |
| **Incidentes NCS** | 15 incidentes técnicos/equipaje | 15 incidentes técnicos/equipaje | ✅ **CONVERGENTE** |
| **OTP Deterioro** | -0.4pts (87.9%) | -1.1pts (81.7%) | ✅ **CONVERGENTE** |
| **Load Factor** | Estable (90.1%) | Elevado +2.8pts (86.3%) | ⚠️ **PARCIALMENTE DIVERGENTE** |

**🔍 DIAGNÓSTICO ECONOMY SH:**
**Causa COMÚN de cabina con inconsistencias de datos**. Ambas compañías muestran el mismo driver operativo crítico (mishandling elevado) y patrones de incidentes idénticos, pero YW presenta una anomalía positiva inexplicable que sugiere problemas de calidad de datos más que diferencias operativas reales.

---

## **B. Business Short Haul:**

**❌ NODOS NO DISPONIBLES:**
- **Global/SH/Business/IB**: No existe en el árbol
- **Global/SH/Business/YW**: No existe en el árbol

**RAZÓN DE AUSENCIA:**
Los nodos Business Short Haul no aparecen en el análisis, lo que indica que:
1. No se detectaron anomalías significativas a este nivel de granularidad
2. El volumen de respuestas pudo ser insuficiente para análisis estadísticamente válido
3. Las anomalías se concentraron principalmente en segmentos Economy SH y Long Haul

---

## **📋 CONCLUSIÓN PASO 1:**

**Economy Short Haul**: **CAUSA COMÚN DE CABINA** - Ambas compañías (IB/YW) convergen en drivers operativos principales (mishandling crítico, incidentes técnicos, deterioro OTP), sugiriendo problemas sistémicos a nivel de cabina más que diferencias específicas por compañía.

**Business Short Haul**: **NO APLICA** - Sin nodos disponibles para comparación.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. Short Haul - Análisis de Cabinas:**

**📊 CABINAS DISPONIBLES:**
- **Economy SH**: ✅ Disponible (IB y YW analizados)
- **Business SH**: ❌ No disponible (sin nodos detectados)

**🔍 ANÁLISIS DE CONVERGENCIA:**
**NO APLICABLE** - Con solo Economy SH disponible, no es posible realizar comparación entre cabinas para determinar patrones convergentes o divergentes a nivel de radio Short Haul.

**📈 HALLAZGO RELEVANTE:**
La **ausencia completa de nodos Business SH** sugiere que:
1. Los problemas operativos del 22-08-2025 impactaron principalmente a Economy
2. Business SH mantuvo niveles de satisfacción dentro de rangos normales
3. La reactividad diferencial se concentró en segmentos Economy

---

## **B. Long Haul - Análisis de Cabinas:**

**📊 CABINAS DISPONIBLES:**
- **Economy LH**: ✅ Disponible 
- **Business LH**: ✅ Disponible
- **Premium LH**: ✅ Disponible

**🔍 ANÁLISIS DE CONVERGENCIA:**

| **Dimensión** | **Economy LH** | **Business LH** | **Premium LH** | **Convergencia** |
|---------------|----------------|-----------------|----------------|------------------|
| **Driver Principal** | Mishandling +10.9pts | Mishandling +10.9pts | Mishandling +10.9pts | ✅ **TOTAL** |
| **Incidentes NCS** | 16 incidentes técnicos | 16 incidentes técnicos | 16 incidentes técnicos | ✅ **TOTAL** |
| **OTP Deterioro** | -1.4pts (80.3%) | -1.4pts (80.3%) | -1.4pts (80.3%) | ✅ **TOTAL** |
| **Load Factor** | +3.1pts (93.2%) | +2.3pts (92.4%) | +2.3pts (92.4%) | ✅ **CONVERGENTE** |
| **NPS Impact** | -6.72pts | +12.76pts | -8.9pts | ❌ **DIVERGENTE** |

**📈 PROGRESIÓN DE REACTIVIDAD:**

| **Cabina** | **Reactividad** | **Patrón** |
|------------|-----------------|------------|
| **Business LH** | **INVERSA** (+12.76pts) | Anomalía positiva inexplicable |
| **Economy LH** | **ALTA** (-6.72pts) | Reacción esperada a problemas |
| **Premium LH** | **MUY ALTA** (-8.9pts) | Mayor sensibilidad a disrupciones |

**🎯 HALLAZGOS CRÍTICOS:**

1. **CAUSA OPERATIVA COMÚN**: Las tres cabinas LH comparten exactamente los mismos drivers operativos (mishandling +10.9pts, 16 incidentes técnicos, deterioro OTP)

2. **REACTIVIDAD DIFERENCIAL EXTREMA**: Mismas causas operativas generan respuestas completamente opuestas:
   - **Premium**: Mayor sensibilidad (-8.9pts) - Lógico para segmento premium
   - **Economy**: Sensibilidad moderada (-6.72pts) - Esperado
   - **Business**: Reacción inversa (+12.76pts) - **ANOMALÍA INEXPLICABLE**

3. **INCONSISTENCIA DE DATOS**: Business LH muestra mejora de NPS a pesar de problemas operativos idénticos, sugiriendo error metodológico o de datos

---

## **📋 CONCLUSIÓN PASO 2:**

**Short Haul**: **NO DETERMINABLE** - Solo Economy SH disponible impide análisis comparativo de cabinas.

**Long Haul**: **CAUSA COMÚN DE RADIO con REACTIVIDAD DIFERENCIAL ANÓMALA** - Las tres cabinas convergen completamente en drivers operativos (mishandling crítico, incidentes técnicos), pero divergen inexplicablemente en impacto NPS, con Business LH mostrando una anomalía positiva que contradice la lógica operativa y sugiere problemas de calidad de datos más que diferencias reales de experiencia del cliente.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. Comparación Entre Radios:**

**📊 ESTADO DE AFECTACIÓN:**
- **Short Haul**: ✅ AFECTADO (Economy SH con anomalías detectadas)
- **Long Haul**: ✅ AFECTADO (Economy, Business, Premium LH con anomalías detectadas)
- **Conclusión**: **AMBOS RADIOS AFECTADOS**

**🔍 CONVERGENCIA DE DRIVERS PRINCIPALES:**

| **Driver Operativo** | **Short Haul** | **Long Haul** | **Convergencia** |
|---------------------|-----------------|---------------|------------------|
| **Mishandling** | +9.1 a +11.5pts | +10.9pts | ✅ **TOTAL CONVERGENCIA** |
| **Incidentes Técnicos** | 15 incidentes | 16 incidentes | ✅ **CONVERGENCIA** |
| **OTP Deterioro** | -0.4 a -1.1pts | -1.4pts | ✅ **CONVERGENCIA** |
| **Load Factor** | +2.8pts (variable) | +2.3 a +3.1pts | ✅ **CONVERGENCIA** |
| **Causa Externa** | Huelga controladores Argentina | Huelga controladores Argentina | ✅ **IDÉNTICA** |

**🎯 EVIDENCIA OPERATIVA CONSISTENTE:**
- **Mishandling crítico**: Ambos radios muestran incrementos de ~10 puntos
- **Problemas técnicos**: Patrones idénticos de incidentes (cambios aeronave, fallas técnicas)
- **Factor externo común**: Huelga de controladores en Argentina afectó ambos radios
- **Operaciones ACMI**: Problemas con Titan Air impactaron ambos segmentos

---

## **B. Coherencia con Nodo Global:**

**📈 ANÁLISIS DE COHERENCIA:**

| **Aspecto** | **Nodo Global** | **Agregado SH+LH** | **Coherencia** |
|-------------|-----------------|-------------------|----------------|
| **NPS Impact** | +1.05pts (25.52 vs 24.47) | Mixto (negativo LH, mixto SH) | ⚠️ **INCOHERENTE** |
| **Driver Principal** | Mishandling +10.9pts (28.3%) | Mishandling ~10pts ambos radios | ✅ **COHERENTE** |
| **Incidentes** | 130 incidentes totales | 15-16 por segmento | ✅ **COHERENTE** |
| **Causa Externa** | Huelga controladores Argentina | Misma causa ambos radios | ✅ **COHERENTE** |

**🔍 PARADOJA GLOBAL IDENTIFICADA:**
El nodo Global muestra **anomalía positiva (+1.05pts)** mientras múltiples subnodos muestran deterioro, lo que indica:

1. **EFECTO COMPENSATORIO**: Segmentos no analizados (posiblemente Premium Business o rutas específicas) compensaron los impactos negativos
2. **PROBLEMA DE BASELINE**: La comparación baseline pudo estar sesgada por problemas similares en período previo
3. **GESTIÓN DE CRISIS EFECTIVA**: Los 130 incidentes gestionados proactivamente mitigaron el impacto final

**📊 MANIFESTACIÓN EN GLOBAL:**
- **ATENÚA PATRONES INDIVIDUALES**: El Global modera los impactos negativos observados en subnodos
- **REFLEJA GESTIÓN OPERATIVA**: La anomalía positiva sugiere que la respuesta organizacional fue efectiva
- **INDICA POLARIZACIÓN**: Alta reactividad (64.4pts) confirma experiencias muy heterogéneas

---

## **📋 CONCLUSIÓN PASO 3:**

**CAUSA GLOBAL HOMOGÉNEA con GESTIÓN DIFERENCIAL EFECTIVA** - Ambos radios (SH y LH) convergen completamente en drivers operativos principales (mishandling crítico +~10pts, incidentes técnicos masivos, huelga controladores Argentina), confirmando una causa raíz común de alcance global. Sin embargo, el nodo Global muestra anomalía positiva (+1.05pts) que atenúa los impactos negativos individuales, indicando que la gestión proactiva de los 130 incidentes y posibles efectos compensatorios de segmentos no analizados mitigaron exitosamente el impacto agregado final, transformando una crisis operativa potencialmente devastadora en una mejora relativa del NPS.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA 1: CRISIS MASIVA DE MISHANDLING**

### A. NATURALEZA DE LA CAUSA:
**Hipótesis:** Colapso sistémico en la gestión de equipajes causado por la convergencia de sobrecarga operativa, problemas técnicos de aeronaves y disrupciones externas que saturaron la capacidad de handling, generando una cascada de fallos que impactó desproporcionadamente la experiencia del cliente.

### B. EVIDENCIA CONSOLIDADA Y ALCANCE:

**🎯 SEGMENTO MÁS GRANDE AFECTADO:** **Global** (Nodo padre que engloba toda la operación)

**📊 OUTPUT CAUSAL DETALLADO:**
- **Magnitud del impacto:** Mishandling 28.3% vs 17.4% baseline (+10.9 puntos)
- **NPS resultante:** +1.05pts (paradójico debido a gestión de crisis)
- **Alcance operativo:** 130 incidentes totales gestionados
- **Reactividad:** 64.4 puntos (experiencias altamente polarizadas)

**🌍 SUBSEGMENTOS AFECTADOS:**
- **Global/LH:** Mishandling +10.9pts → NPS -4.43pts
- **Global/LH/Economy:** Mishandling +10.9pts → NPS -6.72pts  
- **Global/LH/Premium:** Mishandling +10.9pts → NPS -8.9pts
- **Global/SH/Economy/IB:** Mishandling +11.5pts → NPS -2.53pts
- **Global/SH/Economy/YW:** Mishandling +9.1pts → NPS +12.6pts (anomalía de datos)

**📈 MÉTRICAS CLAVE:**
- **Indicador principal:** 28.3% mishandling (vs 17.4% normal)
- **Correlación:** Perfecta entre nivel de mishandling y deterioro NPS
- **Gestión de crisis:** 130 incidentes proactivamente gestionados
- **Impacto diferencial:** Premium (-8.9pts) > Economy (-6.72pts) por mayor sensibilidad

---

## **CAUSA 2: DISRUPCIONES TÉCNICAS MASIVAS DE FLOTA**

### A. NATURALEZA DE LA CAUSA:
**Hipótesis:** Fallas técnicas concentradas en tipos específicos de aeronaves (especialmente A350 y operaciones ACMI con Titan Air) que generaron cambios de equipo, reprogramaciones y efectos dominó operativos, impactando particularmente rutas de largo radio y segmentos premium con mayor sensibilidad a disrupciones.

### B. EVIDENCIA CONSOLIDADA Y ALCANCE:

**🎯 SEGMENTO MÁS GRANDE AFECTADO:** **Global/LH** (Long Haul concentra el impacto técnico)

**📊 OUTPUT CAUSAL DETALLADO:**
- **Incidentes técnicos:** 16 eventos confirmados
- **NPS resultante:** -4.43pts (de 21.57 a 17.14)
- **Tipos de incidentes:** 3 technical_issues + 2 aircraft_change + problemas ACMI
- **Ruta epicentro:** MAD-ORD con A330-300 ACMI (Titan Air)

**🌍 SUBSEGMENTOS AFECTADOS:**
- **Global/LH/Economy:** 16 incidentes → NPS -6.72pts
- **Global/LH/Business:** 16 incidentes → NPS +12.76pts (anomalía)
- **Global/LH/Premium:** 16 incidentes → NPS -8.9pts (mayor sensibilidad)

**📈 MÉTRICAS CLAVE:**
- **Flota crítica:** A350 next (NPS 7.1), A33ACMI (NPS 16.7)
- **Ruta específica:** MAD-ORD NPS 16.7 (6 respuestas)
- **Operador problema:** Titan Air ACMI con regreso a MAD por fallas técnicas
- **Impacto geográfico:** América Norte NPS 0.0 (28 surveys)
- **Load Factor:** 92.4% (sobrecarga que amplificó problemas técnicos)

---

## **CAUSA 3: HUELGA DE CONTROLADORES AÉREOS EN ARGENTINA**

### A. NATURALEZA DE LA CAUSA:
**Hipótesis:** Disrupción externa que generó retrasos masivos (+25 minutos), pérdidas de conexión y efecto dominó en la red de vuelos, particularmente impactando rutas LATAM y operaciones con conexiones en Argentina, con efectos que se propagaron a través de la red global.

### B. EVIDENCIA CONSOLIDADA Y ALCANCE:

**🎯 SEGMENTO MÁS GRANDE AFECTADO:** **Global** (Impacto de red con efectos sistémicos)

**📊 OUTPUT CAUSAL DETALLADO:**
- **Vuelos afectados:** IB108/EZE-MAD como epicentro
- **Efecto cascada:** 4 cambios de equipo + 2 reprogramaciones
- **Pérdidas de conexión:** 31 casos gestionados
- **Retrasos:** 37 incidentes (28% del total de incidentes)

**🌍 SUBSEGMENTOS AFECTADOS:**
- **CodeShare LATAM:** NPS -33.3 (15 surveys) - Impacto directo
- **Global/LH/Economy:** Conexiones perdidas impactan mishandling
- **Global/SH/Economy:** Efectos de red por reprogramaciones

**📈 MÉTRICAS CLAVE:**
- **Retraso específico:** +25 minutos en vuelos Argentina
- **OTP deterioro:** -0.9pts global (83.9% vs 84.8%)
- **Misconex:** 31 pérdidas de conexión gestionadas
- **Correlación perfecta:** Entre pérdidas conexión y incremento mishandling
- **Regiones afectadas:** ORIENTE MEDIO (-50.0), ASIA (-33.3) por efectos de red

---

## **CAUSA 4: SOBRECARGA OPERATIVA SISTÉMICA**

### A. NATURALEZA DE LA CAUSA:
**Hipótesis:** Saturación de la capacidad operativa evidenciada por Load Factors elevados que, combinada con las disrupciones técnicas y externas, creó un cuello de botella sistémico que amplificó todos los demás problemas y redujo la capacidad de recuperación operativa.

### B. EVIDENCIA CONSOLIDADA Y ALCANCE:

**🎯 SEGMENTO MÁS GRANDE AFECTADO:** **Global/LH/Economy** (Mayor volumen y sensibilidad a sobrecarga)

**📊 OUTPUT CAUSAL DETALLADO:**
- **Load Factor:** 93.2% vs 90.1% baseline (+3.1pts)
- **NPS resultante:** -6.72pts 
- **Amplificación:** Sobrecarga + mishandling + técnicos = tormenta perfecta

**🌍 SUBSEGMENTOS AFECTADOS:**
- **Global/LH/Premium:** 92.4% Load Factor → NPS -8.9pts
- **Global/SH/Economy/YW:** 86.3% Load Factor → problemas operativos
- **Global/SH/Economy/IB:** 90.1% Load Factor estable pero con otros impactos

**📈 MÉTRICAS CLAVE:**
- **Sobrecarga crítica:** 93.2% en Economy LH (límite operativo)
- **Correlación:** Load Factor alto + problemas técnicos = impacto exponencial
- **Capacidad saturada:** Menor flexibilidad para gestionar disrupciones
- **Efecto multiplicador:** Cada problema adicional tuvo impacto desproporcionado

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El análisis del 22 de agosto de 2025 revela un patrón complejo de disrupciones operativas que generaron impactos heterogéneos en la satisfacción del cliente. A nivel global, la compañía experimentó una mejora paradójica de +1.05 puntos (NPS 25.52 vs 24.47 baseline), resultado de una gestión proactiva de crisis que mitigó el impacto de 130 incidentes operativos. Sin embargo, esta mejora agregada oculta deterioros significativos en segmentos específicos: Long Haul registró una caída de -4.43 puntos (NPS 17.14 vs 21.57), mientras que Short Haul Economy mostró comportamientos divergentes entre compañías, con IB cayendo -2.53 puntos (NPS 21.40 vs 23.93) y YW presentando una mejora inexplicable de +12.6 puntos (NPS 40.2 vs 27.6). Las causas identificadas incluyen una crisis masiva de mishandling que alcanzó el 28.3% (+10.9 puntos sobre el promedio), disrupciones técnicas concentradas en flota A350 y operaciones ACMI con Titan Air, y los efectos en cascada de la huelga de controladores aéreos en Argentina que generó pérdidas de conexión y retrasos sistémicos.

Las rutas más afectadas se concentraron en operaciones transatlánticas, particularmente MAD-ORD con un NPS devastador de 16.7, JFK-MAD con NPS de 10.0, y MAD-ZRH registrando 16.7 puntos. Los grupos de clientes más reactivos fueron los viajeros de negocios, que experimentaron caídas dramáticas (Business/Work con NPS -14.3), y los pasajeros de CodeShare LATAM (NPS -33.3), mientras que los viajeros Leisure mantuvieron mayor resiliencia con NPS positivos. Geográficamente, las regiones más impactadas fueron América Norte (NPS 0.0), Oriente Medio (-50.0) y Asia (-33.3), evidenciando cómo las disrupciones localizadas se propagaron a través de la red global de conexiones.

**ECONOMY SH: Impacto Operativo Diferenciado por Compañía**
La cabina Economy de Short Haul mostró comportamientos divergentes durante el 22 de agosto, con IB registrando un NPS de 21.40 (deterioro de -2.53 puntos respecto al baseline) mientras YW presentó un NPS de 40.2 (mejora aparente de +12.6 puntos). La causa principal del deterioro en IB fue el incremento crítico de mishandling al 29.2% (+11.5 puntos sobre el promedio), complementado por 15 incidentes operativos que incluyeron problemas técnicos y cambios de aeronave. Esta degradación se reflejó especialmente en la ruta MAD-ZRH con NPS de 16.7, mientras que los perfiles más reactivos incluyeron viajeros de negocios (NPS 0.0 vs Leisure 23.1) y pasajeros de CodeShare LATAM (NPS -100.0). La mejora reportada en YW presenta inconsistencias con la evidencia operativa disponible, sugiriendo problemas de calidad de datos más que una mejora real de la experiencia.

**BUSINESS SH: Desempeño Estable**
El segmento Business de Short Haul mantuvo desempeño estable durante el 22 de agosto de 2025. No se detectaron anomalías significativas a este nivel de granularidad, manteniendo niveles consistentes de satisfacción que no requirieron análisis detallado de causas específicas.

**ECONOMY LH: Deterioro por Tormenta Perfecta Operativa**
La cabina Economy de Long Haul experimentó un deterioro significativo durante el 22 de agosto, registrando un NPS de 12.44 (caída de -6.72 puntos respecto al baseline de 19.16). La causa principal fue una convergencia de problemas operativos críticos: mishandling disparado al 28.3% (+10.9 puntos), sobrecarga operativa con Load Factor del 93.2% (+3.1 puntos) y 16 incidentes técnicos que incluyeron fallas de aeronaves y cambios de equipo. Esta degradación se reflejó especialmente en rutas transatlánticas como JFK-MAD con NPS catastrófico de 10.0, mientras que los perfiles más reactivos incluyeron viajeros de negocios (NPS -14.3) y pasajeros de América Norte (NPS 0.0), contrastando con la mayor resiliencia de viajeros Leisure (NPS 14.5) y destinos de América Centro (NPS 35.5).

**BUSINESS LH: Anomalía Positiva Inexplicable**
La cabina Business de Long Haul registró un NPS de 48.15 durante el 22 de agosto (mejora aparente de +12.76 puntos respecto al baseline de 35.39). Esta evolución resulta paradójica dado que el segmento experimentó los mismos problemas operativos críticos que afectaron otras cabinas: mishandling del 28.3%, 16 incidentes técnicos y deterioro en puntualidad. Los datos sugieren una inconsistencia metodológica más que una mejora real, especialmente considerando que los viajeros Business suelen ser más sensibles a disrupciones operativas, no menos.

**PREMIUM LH: Alta Sensibilidad a Disrupciones Técnicas**
El segmento Premium de Long Haul experimentó un deterioro de -8.9 puntos durante el 22 de agosto, registrando un NPS de 20.0 vs el baseline de 28.9. Las causas dominantes fueron problemas técnicos concentrados en flota A350 next (NPS 7.1) que generaron cambios de aeronave y disrupciones en cascada, amplificados por el mishandling crítico del 28.3% y sobrecarga operativa. Esta degradación fue especialmente evidente en rutas América Centro/Norte (NPS -25.0) y entre viajeros Leisure (NPS 9.5), mientras que los pasajeros Business mantuvieron mayor tolerancia (NPS 75.0), evidenciando patrones de reactividad diferencial dentro del segmento premium.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 7
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-21 to 2025-08-21:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 9 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH/Business, Global/SH/Business/IB, Global/SH/Economy, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. ECONOMY SHORT HAUL**

### **Nodos Disponibles:**
- ✅ **Economy SH/YW**: Existe (Global/SH/Economy/YW)
- ❌ **Economy SH/IB**: No existe en los datos

### **Análisis de Cobertura:**
El nodo Economy SH/YW muestra que dentro de sus 175 surveys totales, **IB representa el 94.3% del volumen** (165 respuestas vs 5 de "Others" y 5 de VY). Esto indica que **la anomalía en Economy SH está dominada por operaciones IB**, no por diferencias entre compañías.

### **Drivers Principales Economy SH/YW:**
- **Mishandling crítico**: +9.1 pts (25.7% vs 16.6%)
- **Sobrecarga operativa**: Load Factor 86.3% vs 83.6% (+2.8 pts)
- **Deterioro puntualidad**: OTP 81.7% vs 82.8% (-1.1 pts)

---

## **B. BUSINESS SHORT HAUL**

### **Nodos Disponibles:**
- ✅ **Business SH/IB**: Existe (Global/SH/Business/IB)
- ❌ **Business SH/YW**: No existe en los datos

### **Análisis de Cobertura:**
El nodo Business SH/IB representa la **totalidad del segmento Business Short Haul**, con 32 surveys y concentración en flota A320neo (18 surveys, 56% del volumen).

### **Drivers Principales Business SH/IB:**
- **Mishandling crítico**: +11.5 pts (29.2% vs 17.7%)
- **Concentración en flota A320neo**: NPS 11.1 vs A319 NPS 100.0
- **Deterioro puntualidad**: OTP15 87.9% vs 88.3% (-0.4 pts)

---

## **🎯 DIAGNÓSTICO FINAL**

### **Economy Short Haul:**
**CAUSA GENERAL DE CABINA** - No hay evidencia de diferenciación por compañía ya que IB domina completamente el volumen (94.3%) y los drivers operativos (mishandling, load factor, puntualidad) son sistémicos a toda la operación Short Haul.

### **Business Short Haul:**
**CAUSA GENERAL DE CABINA** - La anomalía se concentra en operaciones IB que representan la totalidad del segmento, con drivers operativos (mishandling crítico, problemas de flota A320neo) que son sistémicos a la operación Business Short Haul, no específicos de compañía.

**CONCLUSIÓN NIVEL COMPAÑÍA:** Las causas son **comunes a la cabina padre** en ambos casos, no específicas de diferenciación IB vs YW.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. SHORT HAUL - ANÁLISIS DE CABINAS**

### **Patrones Identificados por Cabina:**

**Economy SH:**
- **NPS**: +10.6 pts (anomalía aparentemente positiva)
- **Driver principal**: Mishandling +9.1 pts (25.7% vs 16.6%)
- **Factores secundarios**: Load Factor +2.8 pts, OTP -1.1 pts
- **Reactividad**: Paradoja - mejora NPS pese a deterioro operativo

**Business SH:**
- **NPS**: -4.96 pts (anomalía negativa clara)
- **Driver principal**: Mishandling +11.5 pts (29.2% vs 17.7%) - **MÁS SEVERO**
- **Factor diferencial**: Concentración flota A320neo (NPS 11.1 vs A319 100.0)
- **Reactividad**: **ALTA** - respuesta negativa directa a problemas operativos

### **Análisis de Convergencia:**
- **Driver común**: Mishandling crítico en ambas cabinas (+9.1 vs +11.5 pts)
- **Patrón divergente**: **Business SH muestra mayor reactividad** al mismo problema operativo
- **Factor diferencial**: Business concentra problemas en flota específica (A320neo)

---

## **B. LONG HAUL - ANÁLISIS DE CABINAS**

### **Patrones Identificados por Cabina:**

**Economy LH:**
- **NPS**: -10.74 pts (caída significativa)
- **Driver principal**: Mishandling +10.9 pts (28.3% vs 17.4%)
- **Concentración**: MAD-MVD (NPS 30.8)
- **Reactividad**: **ALTA** - impacto severo por problemas operativos

**Business LH:**
- **NPS**: -10.06 pts (caída similar a Economy)
- **Driver principal**: Mishandling +10.9 pts (mismo nivel que Economy)
- **Segmentación crítica**: Business/Work NPS 0.0 (insatisfacción total)
- **Reactividad**: **EXTREMA** - segmento más exigente devastado

**Premium LH:**
- **NPS**: +11.1 pts (anomalía aparentemente positiva)
- **Driver paradójico**: Mismo mishandling +10.9 pts pero NPS mejora
- **Factor protector**: Dominancia A350 next (NPS 75.0) vs A333 (NPS -25.0)
- **Reactividad**: **BAJA** - protegida por mix de flota favorable

### **Análisis de Convergencia:**
- **Driver común**: Mishandling +10.9 pts **idéntico** en las tres cabinas
- **Progresión de reactividad**: Premium (protegida) < Economy (alta) ≈ Business (extrema)
- **Factor diferencial**: **Premium actúa como amortiguador** por composición de flota

---

## **🎯 DIAGNÓSTICO FINAL**

### **Short Haul:**
**CAUSA COMÚN DE RADIO CON REACTIVIDAD DIFERENCIAL** - Ambas cabinas comparten el mismo driver operativo (mishandling crítico), pero Business SH muestra mayor sensibilidad (-4.96 pts vs +10.6 pts aparente en Economy), especialmente concentrada en flota A320neo.

### **Long Haul:**
**CAUSA COMÚN DE RADIO CON AMORTIGUADOR DIFERENCIAL** - Las tres cabinas comparten idénticamente el mismo driver (mishandling +10.9 pts), pero Premium LH actúa como amortiguador (+11.1 pts) debido a mix favorable de flota A350 next, mientras Economy y Business muestran impacto severo similar (-10.74 y -10.06 pts respectivamente).

**CONCLUSIÓN NIVEL CABINA:** En ambos radios, la **causa es común** (mishandling crítico), pero existe **reactividad diferencial** donde las cabinas premium muestran mayor resistencia por factores protectores (flota, mix de clientes).

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. COMPARACIÓN ENTRE RADIOS**

### **Estado de Afectación:**
- ✅ **Short Haul**: AFECTADO - Anomalías en ambas cabinas
- ✅ **Long Haul**: AFECTADO - Anomalías en todas las cabinas
- **Conclusión**: **AMBOS RADIOS IMPACTADOS**

### **Convergencia de Drivers Principales:**

**Short Haul:**
- **Mishandling**: +9.1 a +11.5 pts (según cabina)
- **Load Factor**: Elevado (+2.8 pts Economy)
- **Puntualidad**: Deterioro (-1.1 a -0.4 pts)

**Long Haul:**
- **Mishandling**: +10.9 pts (**IDÉNTICO** en todas las cabinas LH)
- **Load Factor**: Elevado (+2.3 a +3.1 pts según cabina)
- **Puntualidad**: Deterioro (-1.4 pts)

### **Consistencia de Evidencia Operativa:**
- **Convergencia total**: Mishandling crítico como driver dominante en ambos radios
- **Valores similares**: SH (+9.1 a +11.5 pts) vs LH (+10.9 pts)
- **Factores secundarios**: Load Factor elevado y deterioro puntualidad **consistentes**

---

## **B. COHERENCIA CON NODO GLOBAL**

### **Manifestación en Global:**
- **NPS Global**: +7.9 pts (aparente anomalía positiva)
- **Drivers Globales**: Mishandling +10.9 pts, Load Factor +1.1 pts, OTP -0.9 pts
- **Incidentes totales**: 328 incidentes (125 retrasos)

### **Análisis de Coherencia:**

**PARADOJA DETECTADA:**
- **Nivel Global**: Aparente mejora (+7.9 pts NPS)
- **Nivel Radios**: Deterioro evidente en SH y LH por mismos drivers
- **Evidencia operativa**: **328 incidentes críticos** contradicen mejora aparente

### **Patrón de Agregación:**
El nodo Global **NO refleja** coherentemente el impacto de los radios individuales:
- **SH**: Patrones mixtos (Economy aparente mejora, Business deterioro)
- **LH**: Deterioro generalizado excepto Premium (efecto amortiguador)
- **Global**: Resultado agregado que **enmascara** la severidad real del problema operativo

---

## **🎯 DIAGNÓSTICO FINAL**

### **Alcance de las Causas:**
**CAUSA GLOBAL HOMOGÉNEA CON ENMASCARAMIENTO AGREGADO** - Ambos radios (SH y LH) convergen completamente en el mismo driver principal (mishandling crítico +9-11 pts) y factores secundarios idénticos (load factor elevado, deterioro puntualidad), confirmando una causa operativa sistémica que afectó toda la operación el 21 de agosto de 2025.

### **Manifestación Global:**
El nodo Global presenta una **paradoja de agregación** donde la aparente anomalía positiva (+7.9 pts) **contradice** la evidencia operativa masiva (328 incidentes, mishandling +10.9 pts) y el deterioro documentado en múltiples segmentos, sugiriendo efectos de compensación estadística que enmascaran la severidad real del problema operativo sistémico.

**CONCLUSIÓN NIVEL RADIO:** Las causas son **globales y homogéneas** entre radios, pero el nivel agregado Global sufre de **enmascaramiento** que oculta la magnitud real del impacto operativo del día.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA PRINCIPAL: COLAPSO CRÍTICO DEL SISTEMA DE MANEJO DE EQUIPAJES**

### **A. NATURALEZA DE LA CAUSA**

**Hipótesis Causal:**
El 21 de agosto de 2025 experimentó un **fallo sistémico en las operaciones de handling de equipajes** que se manifestó como un incremento del **62-66% en mishandling** respecto al baseline. Este colapso operativo se propagó a través de toda la red, afectando tanto operaciones Short Haul como Long Haul, generando un efecto cascada que deterioró múltiples aspectos de la experiencia del cliente (retrasos, conexiones perdidas, insatisfacción).

---

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE**

#### **Segmento Más Grande Afectado: GLOBAL**
- **Volumen**: 731 surveys totales
- **NPS Impact**: Aparente +7.9 pts (enmascarado por efectos estadísticos)
- **Realidad operativa**: Deterioro severo sistémico

#### **Output Causal Detallado - Segmento Global:**

**MÉTRICAS OPERATIVAS CRÍTICAS:**
- **Mishandling**: 28.3% vs 17.4% baseline (**+10.9 pts, +62% incremento**)
- **Load Factor**: 88.6% vs 87.5% baseline (+1.1 pts - sobrecarga operativa)
- **OTP15**: 83.9% vs 84.8% baseline (-0.9 pts - deterioro puntualidad)
- **Incidentes NCS**: **328 incidentes totales** (125 retrasos, 38% del total)

**PROPAGACIÓN SISTÉMICA CONFIRMADA:**
Esta causa afecta **TODOS los subsegmentos** bajo el nodo Global:

**Short Haul:**
- Economy SH: Mishandling +9.1 pts (25.7% vs 16.6%)
- Business SH: Mishandling +11.5 pts (29.2% vs 17.7%) - **MÁS SEVERO**

**Long Haul:**
- Economy LH: Mishandling +10.9 pts (28.3% vs 17.4%)
- Business LH: Mishandling +10.9 pts (idéntico)
- Premium LH: Mishandling +10.9 pts (mismo nivel, pero amortiguado por flota)

#### **Rutas Críticas Identificadas:**
- **MAD-MVD** (Long Haul): NPS 30.8 - Concentración del impacto
- **MAD-PNA** (Short Haul): NPS 0.0 - Experiencia unánimemente negativa
- **MAD-XRY** (Short Haul Economy): NPS 28.6 - Deterioro severo

#### **Incidente Específico Documentado:**
- **Vuelo IB124/LIM**: **35 equipajes retenidos** por medidas de seguridad
- **Correlación**: Este incidente específico ejemplifica el colapso sistémico del handling

#### **Limitación Crítica - Verbatims:**
**❌ AUSENCIA TOTAL** de feedback cualitativo para el 21 de agosto de 2025, lo que impide:
- Validar percepción directa sobre los 328 incidentes
- Entender contexto emocional de la crisis
- Correlacionar problemas específicos con quejas de clientes

---

### **IMPACTO DIFERENCIAL POR PERFIL:**

**Segmentos Más Devastados:**
- **Clientes ASIA** (Global): NPS -50.0 (4 surveys)
- **Business/Work travelers** (múltiples segmentos): NPS 0.0 a -23.1
- **CodeShare "Others"**: NPS -26.7 a -66.7 (experiencia catastrófica)
- **Flota A33ACMI**: NPS -7.9 a -56.2 (problemas operativos concentrados)

**Factores Agravantes:**
- **Alta ocupación**: Load Factor 88-93% según segmento (sobrecarga operativa)
- **Concentración en flotas específicas**: A320neo, A332, A33ACMI más afectadas
- **Rutas intercontinentales**: Mayor impacto en conexiones de larga distancia

---

### **EXPLICACIÓN CAUSAL CONSOLIDADA:**

El **colapso del sistema de handling de equipajes** del 21 de agosto de 2025 representa una **falla operativa sistémica** que afectó uniformemente toda la red de Iberia. El incremento del 62-66% en mishandling generó un **efecto dominó** que se propagó através de:

1. **Retrasos masivos** (125 incidentes de 328 totales)
2. **Sobrecarga operativa** por alta ocupación
3. **Deterioro en puntualidad** por efectos cascada
4. **Impacto diferencial severo** en segmentos de alto valor (Business, clientes internacionales)

La **ausencia total de verbatims** sugiere que la crisis fue tan severa que impidió la captura normal del feedback de clientes, evidenciando una **falla en la gestión de crisis** además del problema operativo fundamental.

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El análisis del 21 de agosto de 2025 revela un patrón complejo donde aparentes mejoras en el NPS Global (+7.9 puntos, alcanzando 32.36 vs baseline 24.47) enmascaran un deterioro operativo severo que impactó diferencialmente los segmentos. Los nodos Long Haul experimentaron caídas significativas, con Economy LH descendiendo 10.74 puntos (de 40.64 a 29.90) y Business LH cayendo 10.06 puntos (de 55.51 a 45.45), mientras Premium LH mostró una mejora paradójica de 11.1 puntos (de 28.9 a 40.0). En Short Haul, Economy registró una aparente mejora de 10.6 puntos (de 27.6 a 38.2) y Business experimentó un deterioro de 4.96 puntos (de 31.43 a 26.47). La causa raíz identificada fue un colapso crítico del sistema de manejo de equipajes, con mishandling disparándose entre 9.1 y 11.5 puntos por encima del baseline (alcanzando 25.7%-29.2% vs 16.6%-17.7% promedio), complementado por sobrecarga operativa (load factors de 86.3%-93.2%) y deterioro en puntualidad. Esta crisis se evidenció en 328 incidentes operativos totales, incluyendo 125 retrasos y casos específicos como 35 equipajes retenidos en el vuelo IB124/LIM.

Las rutas más afectadas incluyen MAD-MVD con un NPS devastador de 30.8, MAD-PNA con experiencia unánimemente negativa (NPS 0.0), y MAD-XRY registrando 28.6 puntos. Los grupos más reactivos fueron viajeros de negocios (Business/Work alcanzando NPS 0.0 en múltiples segmentos), clientes asiáticos (NPS -50.0 a -100.0), operaciones de codeshare "Others" (NPS -26.7 a -66.7), y pasajeros en flotas A33ACMI y A320neo, que concentraron el mayor impacto negativo. La paradójica mejora en Premium LH se explica por un efecto protector de la flota A350 next (NPS 75.0) que compensó los problemas operativos, mientras que la ausencia total de verbatims para este día crítico sugiere que la crisis fue tan severa que impidió la captura normal del feedback de clientes.

**ECONOMY SH: Mejora Aparente con Deterioro Operativo Subyacente**
La cabina Economy de Short Haul experimentó una mejora aparente de 10.6 puntos, pasando de un NPS de 27.6 a 38.2 el 21 de agosto de 2025. Sin embargo, esta mejora contradice el deterioro operativo severo evidenciado por mishandling crítico (+9.1 puntos, alcanzando 25.7% vs 16.6% baseline), sobrecarga operativa (load factor 86.3% vs 83.6%) y deterioro en puntualidad (OTP 81.7% vs 82.8%). Esta paradoja se concentró especialmente en la ruta MAD-XRY con NPS 28.6, mientras que los perfiles más reactivos incluyeron clientes de América Norte (NPS -9.1) y operaciones de codeshare "Others" (NPS -60.0), sugiriendo que la mejora agregada enmascara problemas específicos en segmentos críticos.

**BUSINESS SH: Deterioro por Crisis Operativa Concentrada**
El segmento Business de Short Haul registró un deterioro de 4.96 puntos, descendiendo de un NPS de 31.43 a 26.47 el 21 de agosto. Esta evolución se explica principalmente por mishandling explosivo (+11.5 puntos, alcanzando 29.2% vs 17.7% baseline) y concentración de problemas en flota A320neo (NPS crítico 11.1 vs A319 con NPS perfecto 100.0), siendo especialmente visible en rutas como MAD-VCE y entre perfiles Business/Work que alcanzaron insatisfacción total (NPS 0.0).

**ECONOMY LH: Caída Severa por Problemas Sistémicos**
La cabina Economy de Long Haul experimentó un deterioro significativo de 10.74 puntos, descendiendo de un NPS de 40.64 a 29.90 el 21 de agosto de 2025. La causa principal fue el colapso del sistema de handling de equipajes (mishandling +10.9 puntos, alcanzando 28.3% vs 17.4% baseline), complementado por alta ocupación (load factor 93.2% vs 90.1%) y deterioro en puntualidad (OTP 80.3% vs 81.8%). Esta caída se reflejó especialmente en rutas como MAD-MVD con NPS 30.8, mientras que los perfiles más reactivos incluyeron viajeros de negocios (NPS -23.1), clientes asiáticos (NPS -100.0) y pasajeros en flota A332 (NPS 6.2).

**BUSINESS LH: Impacto Crítico en Segmento Premium**
La cabina Business de Long Haul registró una caída de 10.06 puntos, descendiendo de un NPS de 55.51 a 45.45 el 21 de agosto. Los drivers principales fueron mishandling crítico idéntico al de Economy (+10.9 puntos) y deterioro en puntualidad, impactando especialmente las rutas intercontinentales como LAX-MAD y entre perfiles Business/Work que experimentaron insatisfacción total (NPS 0.0), evidenciando la mayor sensibilidad de este segmento a fallos operativos.

**PREMIUM LH: Mejora Paradójica por Efecto Protector de Flota**
El segmento Premium de Long Haul mostró una mejora paradójica de 11.1 puntos, pasando de un NPS de 28.9 a 40.0 el 21 de agosto, a pesar del mismo deterioro operativo (mishandling +10.9 puntos). Las causas dominantes fueron el efecto protector de la flota A350 next (NPS 75.0 con 8 surveys) que compensó los problemas de la flota A333 (NPS -25.0), especialmente evidentes en rutas como BOG-MAD y entre clientes de América Centro/Sur que registraron satisfacción perfecta (NPS 100.0).

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 9
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-20 to 2025-08-20:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 6 (Global, Global/LH/Economy, Global/LH/Premium, Global/SH/Business, Global/SH/Business/YW, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 **PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)**

## **A. Economy Short Haul:**

**ESTADO DE NODOS:**
- ✅ **Economy SH/YW existe**: Global/SH/Economy/YW (NPS: 23.89, anomalía -3.71 pts)
- ❌ **Economy SH/IB NO existe**: No hay nodo separado para IB en Economy SH

**RAZÓN DE LA AUSENCIA**: El nodo IB Economy SH probablemente no alcanzó el umbral mínimo de anomalía o volumen de datos para ser incluido en el análisis automatizado.

## **B. Business Short Haul:**

**ESTADO DE NODOS:**
- ✅ **Business SH/YW existe**: Global/SH/Business/YW (NPS: 33.7, anomalía -16.28 pts)
- ❌ **Business SH/IB NO existe**: No hay nodo separado para IB en Business SH

**RAZÓN DE LA AUSENCIA**: Similar al caso Economy, el nodo IB Business SH no presenta anomalías significativas o suficiente volumen para análisis separado.

## **DIAGNÓSTICO CONCLUSIVO:**

**Economy Short Haul**: **Causa específica de YW** - Solo Vueling presenta anomalía significativa (-3.71 pts), mientras que Iberia mantiene performance normal.

**Business Short Haul**: **Causa específica de YW** - Solo Vueling presenta anomalía crítica (-16.28 pts), mientras que Iberia mantiene performance normal.

**IMPLICACIÓN ESTRATÉGICA**: Los problemas operativos del 20 de agosto de 2025 afectaron desproporcionadamente a Vueling (YW) en ambas cabinas Short Haul, mientras que Iberia (IB) mantuvo operaciones estables en estos segmentos.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ **PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)**

## **A. Short Haul - Análisis de Cabinas:**

**PATRONES IDENTIFICADOS:**
- **Economy SH/YW**: Anomalía moderada (-3.71 pts) | Driver principal: Mishandling 25.7% (+9.1 pts)
- **Business SH/YW**: Anomalía severa (-16.28 pts) | Driver principal: Mishandling 25.7% (+9.1 pts)

**ANÁLISIS DE CONVERGENCIA/DIVERGENCIA:**
- ✅ **Driver operativo común**: Ambas cabinas comparten el mismo factor causal (Mishandling crítico 25.7%)
- ⚠️ **Reactividad diferencial**: Business muestra **4.4x mayor sensibilidad** (-16.28 vs -3.71 pts) ante el mismo problema operativo
- 📍 **Concentración geográfica similar**: Ambas afectadas en rutas específicas (LIS-MAD para Economy, CMN-MAD para Business)

**DIAGNÓSTICO SH**: **Causa común de radio con reactividad diferencial por cabina** - El mismo problema operativo (crisis de equipaje) genera impacto desproporcionadamente mayor en Business por expectativas de servicio superiores.

## **B. Long Haul - Análisis de Cabinas:**

**PATRONES IDENTIFICADOS:**
- **Economy LH**: Anomalía **POSITIVA** (+7.6 pts) | Gestión excepcional de crisis
- **Premium LH**: Anomalía **NEGATIVA** (-22.98 pts) | Colapso operativo crítico

**ANÁLISIS DE CONVERGENCIA/DIVERGENCIA:**
- ❌ **Patrones completamente opuestos**: Economy mejora mientras Premium colapsa
- 🔄 **Drivers operativos idénticos**: Ambas enfrentan Mishandling 28.3% (+10.9 pts), Load Factor elevado, OTP deteriorado
- 📊 **Reactividad inversa**: Mismo contexto operativo genera experiencias diametralmente opuestas

**FACTORES EXPLICATIVOS:**
- **Economy LH**: Gestión excepcional de expectativas + comunicación efectiva durante crisis
- **Premium LH**: Expectativas elevadas no satisfechas + concentración en rutas críticas (BOG-MAD)

**DIAGNÓSTICO LH**: **Causa común de radio con reactividad inversa por cabina** - Idénticos problemas operativos generan experiencias opuestas: Economy convierte la adversidad en fortaleza mientras Premium sufre colapso por expectativas no cumplidas.

## **SÍNTESIS GENERAL:**
Ambos radios muestran **causas operativas comunes** pero **reactividades diferenciales extremas** por tipo de cabina, confirmando que el perfil del cliente y sus expectativas son factores críticos en la percepción final de la experiencia.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 **PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL**

## **A. Comparación Entre Radios:**

**ESTADO DE AFECTACIÓN:**
- ✅ **Short Haul afectado**: Anomalías negativas en Economy (-3.71 pts) y Business (-16.28 pts)
- ✅ **Long Haul afectado**: Anomalías mixtas - Economy positiva (+7.6 pts) y Premium negativa (-22.98 pts)

**CONVERGENCIA DE DRIVERS:**
- ✅ **Driver principal común**: **Mishandling crítico** domina en ambos radios
  - **SH**: 25.7% (+9.1 pts vs baseline)
  - **LH**: 28.3% (+10.9 pts vs baseline)
- ✅ **Drivers secundarios consistentes**: OTP deteriorado y Load Factor elevado en ambos
- ✅ **Evidencia operativa convergente**: Incidentes masivos de equipaje (IB424/BCN con 47 equipajes sin cargar)

## **B. Coherencia con Nodo Global:**

**ANÁLISIS DE COHERENCIA:**
- **Global NPS**: 28.16 pts (anomalía -3.69 pts)
- **Agregación lógica**: El Global refleja el **promedio ponderado** de efectos mixtos:
  - Impactos negativos SH + Premium LH
  - Compensación parcial por Economy LH excepcional (+7.6 pts)
- **Amplificación de evidencia**: Global reporta **281 incidentes totales** vs incidentes específicos por radio, confirmando escala masiva del problema

**MANIFESTACIÓN EN GLOBAL:**
- ✅ **Drivers consistentes**: Mishandling 28.3% como factor dominante
- ✅ **Evidencia amplificada**: 281 incidentes vs 22 (SH) confirma alcance sistémico
- ✅ **Impacto neto coherente**: -3.69 pts refleja compensación entre radios

## **DIAGNÓSTICO FINAL:**

**Causa global homogénea con manifestaciones diferenciales** - El 20 de agosto de 2025 experimentó una **crisis operativa sistémica de equipaje** que afectó toda la red (281 incidentes), pero se manifestó de forma diferente según el perfil del cliente: Short Haul mostró impacto negativo uniforme, mientras Long Haul evidenció reactividad inversa (Economy resiliente vs Premium colapsado), resultando en un impacto global neto moderado (-3.69 pts) que enmascara la severidad real de los problemas operativos subyacentes.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 **PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS**

## **CAUSA PRINCIPAL IDENTIFICADA: CRISIS OPERATIVA SISTÉMICA DE EQUIPAJE**

### **A. NATURALEZA DE LA CAUSA:**

**Hipótesis Causal**: El 20 de agosto de 2025 se produjo un **colapso operativo en cadena** iniciado por condiciones meteorológicas adversas en MXP (Milán) que generó regulaciones de tráfico aéreo, desencadenando un efecto dominó que saturó los sistemas de manejo de equipaje a nivel de red. La combinación de **alta ocupación** (Load Factor elevado) + **disrupciones operativas masivas** (281 incidentes) + **capacidad limitada de recovery** resultó en una incapacidad sistémica para gestionar el equipaje de los pasajeros, manifestándose como el driver más crítico de deterioro del NPS.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO**: **Global** (toda la operación)

#### **OUTPUT CAUSAL DETALLADO - NODO GLOBAL:**

**📊 MÉTRICAS OPERATIVAS CRÍTICAS:**
- **Mishandling**: 28.3% vs 17.4% baseline (**+10.9 pts** - incremento del 62%)
- **Load Factor**: 88.6% vs 87.5% baseline (+1.1 pts - sobrecarga operativa)
- **OTP15**: 83.9% vs 84.8% baseline (-0.9 pts - deterioro puntualidad)
- **NPS Impacto**: 28.16 vs 24.47 baseline (**-3.69 pts**)

**🚨 EVIDENCIA OPERATIVA MASIVA:**
- **281 incidentes totales** documentados en NCS
- **92 retrasos** (32.7%) + **34 cancelaciones** (12.1%)
- **25 vuelos específicamente afectados**
- **Incidente crítico**: Vuelo IB424/BCN con **47 equipajes sin cargar**
- **4 problemas técnicos** en flotas específicas

**🌍 RUTAS Y FLOTAS CRÍTICAS:**
- **A321XLR**: NPS -42.9 (n=14) - Extremadamente crítico
- **A33ACMI**: NPS -9.5 (n=42) - Problemas ACMI
- **BOG-MAD**: Epicentro en Premium LH
- **LIS-MAD**: Crítico en Economy SH/YW
- **CMN-MAD**: Crítico en Business SH/YW

**📈 ALCANCE CONFIRMADO:**
Esta causa afecta **TODOS los subsegmentos** bajo el nodo Global:
- ✅ **Short Haul Economy/Business YW**: Impacto negativo directo
- ✅ **Long Haul Economy**: Impacto positivo (gestión excepcional de crisis)
- ✅ **Long Haul Premium**: Impacto negativo severo
- ✅ **Mercados internacionales**: Oriente Medio (-28.6), África (-14.3)
- ✅ **CodeShare partnerships**: Qatar Airways (-33.3), Others (-37.5)

**⚠️ LIMITACIÓN CRÍTICA:**
- **Verbatims no disponibles**: Sin feedback cualitativo directo de los clientes para validar la percepción emocional del impacto del equipaje

**🎯 PATRÓN DE MANIFESTACIÓN:**
La misma causa operativa (crisis de equipaje) se manifiesta de forma **diferencial según el perfil del cliente**:
- **Economy LH**: Convierte adversidad en experiencia positiva (+7.6 pts)
- **Premium LH**: Colapso total por expectativas no cumplidas (-22.98 pts)  
- **Business SH**: Mayor sensibilidad que Economy SH (-16.28 vs -3.71 pts)
- **Mercados internacionales**: Más vulnerables que domésticos

**CONCLUSIÓN CAUSAL**: Una crisis operativa de equipaje sistémica, iniciada por factores meteorológicos externos y amplificada por alta ocupación, generó el mayor impacto diferencial en NPS según las expectativas específicas de cada segmento de clientes.

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 20 de agosto de 2025 se caracterizó por una crisis operativa sistémica de equipaje que generó impactos diferenciados en el NPS según el perfil del cliente. A nivel global, el NPS experimentó una caída de 3.69 puntos, pasando de 24.47 a 28.16 puntos, causada principalmente por un incremento crítico del 62% en mishandling (28.3% vs 17.4% baseline) desencadenado por condiciones meteorológicas adversas en MXP que generaron regulaciones de tráfico aéreo y 281 incidentes operativos masivos. Esta crisis se manifestó de forma paradójica: mientras Economy Long Haul logró una mejora excepcional de 7.6 puntos (pasando de 19.2 a 26.8 puntos) mediante una gestión de crisis ejemplar, Premium Long Haul sufrió un colapso severo con una caída de 22.98 puntos (de 28.87 a 5.88 puntos), y Short Haul mostró deterioros moderados en Vueling con Economy cayendo 3.71 puntos (de 27.60 a 23.89) y Business experimentando una caída más severa de 16.28 puntos (de 50.0 a 33.7).

Las rutas más críticas incluyeron BOG-MAD como epicentro del colapso en Premium, LIS-MAD con un NPS catastrófico de -12.5 para Economy SH, y CMN-MAD registrando -33.3 puntos en Business SH. Los grupos más reactivos fueron los viajeros de negocios internacionales, especialmente de América del Norte (NPS -50.0 en Premium y -37.5 en Economy YW), mientras que los clientes leisure de América Centro mostraron la mayor resiliencia con un NPS excepcional de +63.0 puntos, evidenciando que las expectativas del cliente y el propósito de viaje determinaron la percepción final ante la misma crisis operativa.

**ECONOMY SH: Crisis de Equipaje Moderadamente Gestionada**
La cabina Economy de Short Haul en Vueling experimentó un deterioro moderado durante el 20 de agosto, registrando un NPS de 23.89 puntos con una caída de 3.71 puntos respecto al baseline de 27.60. La causa principal fue la crisis sistémica de equipaje con un mishandling del 25.7% (+9.1 puntos vs baseline), complementada por sobrecarga operativa con Load Factor del 86.3% y deterioro en puntualidad (OTP15 81.7%). Este deterioro se reflejó especialmente en la ruta LIS-MAD con un NPS catastrófico de -12.5 puntos, mientras que los perfiles más reactivos incluyeron viajeros de negocios internacionales de América del Norte (NPS -37.5) y África (NPS -25.0), contrastando con la mayor resistencia de pasajeros españoles (NPS +43.2).

**BUSINESS SH: Impacto Severo por Expectativas Elevadas**
El segmento Business de Short Haul en Vueling sufrió un deterioro severo, registrando un NPS de 33.7 puntos con una caída crítica de 16.28 puntos vs el baseline de 50.0. Esta evolución se explica principalmente por el mismo mishandling crítico del 25.7% que afectó a Economy, pero con una reactividad 4.4 veces mayor debido a expectativas de servicio superiores, siendo especialmente visible en la ruta CMN-MAD con un NPS de -33.3 puntos operada por flota ATR, y entre perfiles de clientes internacionales que mostraron menor tolerancia a las disrupciones operativas comparado con clientes españoles (NPS 66.7).

**ECONOMY LH: Gestión Excepcional de Crisis**
La cabina Economy de Long Haul logró una mejora excepcional durante el 20 de agosto, registrando un NPS de 26.8 puntos con una subida extraordinaria de 7.6 puntos respecto al baseline de 19.2. La causa principal fue una gestión de crisis ejemplar que convirtió adversidades operativas (mishandling 28.3%, Load Factor 93.2%) en experiencias positivas mediante comunicación efectiva y protocolos de recuperación superiores. Esta mejora se reflejó especialmente en rutas como MAD-MIA con NPS de 25.0 puntos y fue liderada por pasajeros de América Centro con un NPS excepcional de +63.0 puntos, mientras que los perfiles más beneficiados fueron viajeros leisure que mostraron mayor adaptabilidad a las disrupciones comparado con viajeros business.

**BUSINESS LH: Estabilidad Operativa Mantenida**
La cabina Business de Long Haul mantuvo desempeño estable durante el período analizado. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción sin anomalías reportadas en el árbol de análisis.

**PREMIUM LH: Colapso por Expectativas No Cumplidas**
El segmento Premium de Long Haul experimentó un colapso severo durante el 20 de agosto, registrando un NPS de 5.88 puntos con una caída devastadora de 22.98 puntos vs el baseline de 28.87. Las causas dominantes fueron el mismo mishandling crítico del 28.3% y sobrecarga operativa (Load Factor 92.4%) que afectó otras cabinas, pero amplificadas por expectativas premium no satisfechas, especialmente evidentes en la ruta BOG-MAD con NPS 0.0 puntos y entre viajeros de América del Norte (NPS -50.0) y pasajeros leisure premium que mostraron la mayor vulnerabilidad ante disrupciones operativas, contrastando con la relativa resistencia de América Sur (NPS +33.3).

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 6
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-19 to 2025-08-19:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 9 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH/Business/IB, Global/SH/Business/YW, Global/SH/Economy/IB, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW) - SHORT HAUL

## **A. ECONOMY SHORT HAUL**

**NODOS IDENTIFICADOS:**
- ✅ **Economy SH/IB** (Global/SH/Economy/IB): Anomalía -0.46 pts
- ✅ **Economy SH/YW** (Global/SH/Economy/YW): Anomalía +11.5 pts

**ANÁLISIS COMPARATIVO:**

### **Drivers Principales:**
- **IB**: Mishandling 29.2% (+11.5pts), OTP15 87.9% (-0.4pts)
- **YW**: Mishandling 25.7% (+9.1pts), OTP15 81.7% (-1.1pts)

### **Evidencia Operativa:**
- **IB**: 20 incidentes NCS, epicentro en flotas largo radio (A350, A33ACMI)
- **YW**: 20 incidentes NCS, mismo patrón operativo pero impacto diferencial por segmentación

### **Patrón Divergente Crítico:**
- **IB**: Impacto negativo concentrado en rutas internacionales y CodeShare partners
- **YW**: Impacto positivo por segmentación favorable (clientes nacionales/leisure resilientes)

**DIAGNÓSTICO:** **Causa común operativa con impacto diferencial por composición de clientela** - Ambas compañías experimentaron la misma crisis operativa (mishandling +9-11pts) pero YW mostró mayor resiliencia debido a su perfil de cliente predominantemente nacional/leisure.

---

## **B. BUSINESS SHORT HAUL**

**NODOS IDENTIFICADOS:**
- ✅ **Business SH/IB** (Global/SH/Business/IB): Anomalía -8.35 pts
- ✅ **Business SH/YW** (Global/SH/Business/YW): Anomalía -32.95 pts

**ANÁLISIS COMPARATIVO:**

### **Drivers Principales:**
- **IB**: Mishandling 29.2% (+11.5pts), OTP15 87.9% (-0.4pts)
- **YW**: Mishandling 25.7% (+9.1pts), OTP15 81.7% (-1.1pts)

### **Evidencia Operativa:**
- **IB**: 20 incidentes NCS, polarización extrema Business/Work (-33.3) vs Leisure (+30.4)
- **YW**: 20 incidentes NCS, mismos incidentes críticos (IB424/BCN, IB379 MAD-SJU)

### **Patrón Convergente:**
- Ambas compañías muestran **identical drivers operativos**
- **Misma evidencia de incidentes** (47 equipajes IB424, retraso IB379)
- **Impacto diferencial explicado por volumen de muestra** (IB: 26 surveys vs YW: 9 surveys)

**DIAGNÓSTICO:** **Causa común operativa de cabina** - Tanto IB como YW experimentaron la misma crisis operativa con drivers idénticos; las diferencias en magnitud del NPS se explican por tamaños de muestra y composición específica de respondientes, no por causas operativas distintas.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. SHORT HAUL - ANÁLISIS DE CABINAS**

**NODOS ANALIZADOS:**
- Economy SH: IB (-0.46 pts) / YW (+11.5 pts)
- Business SH: IB (-8.35 pts) / YW (-32.95 pts)

### **Patrones de Convergencia/Divergencia:**

**DRIVERS OPERATIVOS:**
- **Convergencia total**: Ambas cabinas muestran **identical drivers** (Mishandling +9-11pts, OTP15 deteriorado)
- **Misma evidencia**: 20 incidentes NCS idénticos (IB424/BCN, IB379 MAD-SJU)
- **Consistencia entre compañías**: El patrón operativo es uniforme IB/YW en ambas cabinas

**REACTIVIDAD DIFERENCIAL CRÍTICA:**
- **Economy SH**: Mayor **resiliencia** - YW logra anomalía positiva (+11.5) a pesar de crisis operativa
- **Business SH**: Mayor **sensibilidad** - Ambas compañías muestran caídas severas (IB: -8.35, YW: -32.95)

**PATRÓN IDENTIFICADO:**
Economy mostró **amortiguación** ante problemas operativos (especialmente YW con clientela leisure/nacional), mientras Business amplificó el impacto negativamente.

**DIAGNÓSTICO SHORT HAUL:** **Causa operativa común al radio con reactividad diferencial por cabina** - La crisis operativa (mishandling +10pts) afectó uniformemente ambas cabinas, pero Economy actuó como "amortiguador" mientras Business amplificó el impacto negativo debido a expectativas más altas.

---

## **B. LONG HAUL - ANÁLISIS DE CABINAS**

**NODOS ANALIZADOS:**
- Economy LH: -4.87 pts
- Business LH: -13.17 pts  
- Premium LH: -17.3 pts

### **Patrones de Convergencia/Divergencia:**

**DRIVERS OPERATIVOS CONVERGENTES:**
- **Mishandling crítico**: 28.3% (+10.9pts) - **Idéntico** en las tres cabinas
- **OTP15 deteriorado**: 80.3-83.9% - **Consistente** degradación
- **Load Factor elevado**: 88-93% - **Presión operativa común**
- **Evidencia NCS**: 22 incidentes **idénticos** (LAX-MAD epicentro)

**PROGRESIÓN LÓGICA DE REACTIVIDAD:**
```
Economy LH (-4.87) < Business LH (-13.17) < Premium LH (-17.3)
```

**ESCALADA POR EXPECTATIVAS:**
- **Economy**: Impacto moderado, mayor tolerancia a disrupciones
- **Business**: Impacto severo, expectativas de confiabilidad altas
- **Premium**: Impacto máximo, tolerancia cero a problemas operativos

**EPICENTRO COMÚN IDENTIFICADO:**
- **LAX-MAD (A321XLR)**: NPS 0.0 - Concentración absoluta del problema
- **Flota específica**: A350 C, A33ACMI consistentemente problemáticas
- **Mishandling transatlántico**: Impacto amplificado en rutas de larga distancia

**DIAGNÓSTICO LONG HAUL:** **Causa operativa común al radio con escalada progresiva por nivel de servicio** - La crisis operativa (mishandling +10.9pts, epicentro LAX-MAD) impactó uniformemente las tres cabinas, pero con intensidad creciente según el nivel de expectativas: Economy mostró resistencia, Business sufrió impacto severo, y Premium experimentó el colapso máximo.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. COMPARACIÓN ENTRE RADIOS**

### **AFECTACIÓN SIMULTÁNEA CONFIRMADA:**
- ✅ **Short Haul afectado**: Economy (-0.46 a +11.5), Business (-8.35 a -32.95)
- ✅ **Long Haul afectado**: Economy (-4.87), Business (-13.17), Premium (-17.3)

### **CONVERGENCIA DE DRIVERS PRINCIPALES:**

**MISHANDLING - DRIVER UNIVERSAL:**
- **Short Haul**: 25.7-29.2% (+9.1 a +11.5pts vs baseline)
- **Long Haul**: 28.3% (+10.9pts vs baseline)
- **Convergencia perfecta**: **~+10pts en ambos radios**

**PUNTUALIDAD - PATRÓN CONSISTENTE:**
- **Short Haul**: OTP15 81.7-87.9% (-0.4 a -1.1pts)
- **Long Haul**: OTP15 80.3-83.9% (-0.9 a -1.4pts)
- **Degradación uniforme**: **~-1pt en ambos radios**

**EVIDENCIA OPERATIVA CONVERGENTE:**
- **Incidentes NCS idénticos**: 20-22 eventos en ambos radios
- **Casos críticos compartidos**: IB424/BCN (47 equipajes), IB379 MAD-SJU (+1h15min)
- **Load Factor elevado**: 75-93% presión operativa común

---

## **B. COHERENCIA CON NODO GLOBAL**

### **AGREGACIÓN COHERENTE CONFIRMADA:**

**NODO GLOBAL: -0.002 pts** (prácticamente estable)

**EXPLICACIÓN DE LA APARENTE ESTABILIDAD:**
```
Short Haul: Impactos mixtos (Economy +11.5 compensa Business -32.95)
Long Haul: Impactos negativos uniformes (-4.87 a -17.3)
Resultado: Compensación parcial = Global casi neutro (-0.002)
```

**VALIDACIÓN CRUZADA:**
- **Drivers Global**: Mishandling 28.3% (+10.9pts) - **Idéntico** a ambos radios
- **Incidentes Global**: 329 eventos NCS - **Suma coherente** de ambos radios
- **Patrones geográficos**: IAD-MAD, LAX-MAD - **Consistentes** con análisis por radio

### **ENMASCARAMIENTO CRÍTICO IDENTIFICADO:**
El nodo Global (-0.002 pts) **enmascara una crisis operativa severa** debido a efectos compensatorios:
- **Segmentos resilientes** (Economy SH/YW +11.5) compensan
- **Segmentos devastados** (Premium LH -17.3, Business SH/YW -32.95)

---

## **🎯 DIAGNÓSTICO FINAL**

**CAUSA GLOBAL HOMOGÉNEA CONFIRMADA** - Ambos radios (Short Haul y Long Haul) experimentaron la **misma crisis operativa** con drivers idénticos (Mishandling +10pts, OTP15 -1pt, incidentes masivos), pero el nodo Global (-0.002 pts) enmascara la severidad real debido a efectos compensatorios entre segmentos con diferente reactividad a disrupciones operativas.

**IMPLICACIÓN CRÍTICA:** La estabilidad aparente del NPS Global oculta una **crisis operativa sistémica** que requiere atención inmediata, ya que afectó uniformemente toda la operación con impactos severos en segmentos premium y de negocio.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA 1: CRISIS MASIVA DE MISHANDLING**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Colapso sistémico en los procesos de manejo de equipaje y servicios operativos terrestres, probablemente causado por sobrecarga operativa, fallas en sistemas de handling, o problemas de coordinación entre aeropuertos hub y destinos internacionales. El incremento del 62% en mishandling sugiere un evento operativo específico o acumulación de fallas sistémicas.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Global (Nodo padre - todos los clientes)

**OUTPUT CAUSAL DETALLADO:**
- **Magnitud del impacto:** Mishandling disparado a 28.3% vs 17.4% promedio (+10.9 puntos, +62% incremento)
- **NPS resultante:** 24.463 (caída marginal -0.002 que enmascara impactos severos por segmento)
- **Alcance:** 329 incidentes operativos totales validados por NCS

**SUBSEGMENTOS AFECTADOS (cascada completa):**
- **Long Haul:** 28.3% mishandling - Impacto severo en todas las cabinas
- **Short Haul:** 25.7-29.2% mishandling - Impacto diferencial por compañía
- **Todas las cabinas:** Economy, Business, Premium experimentaron el mismo driver

**MÉTRICAS CLAVE CONSOLIDADAS:**
- **Indicadores operativos:** 
  - Mishandling: 28.3% (+10.9pts)
  - 110 retrasos documentados
  - 42 cancelaciones
  - 24 pérdidas de conexión
- **Rutas críticas involucradas:**
  - LAX-MAD (A321XLR): NPS 0.0 - Epicentro absoluto
  - IAD-MAD: NPS -33.3 - Ruta más problemática
  - EZE-MAD: Impacto en Business LH
- **Incidentes específicos validados:**
  - IB424/BCN: 47 equipajes sin cargar
  - IB2623: Vuelo más impactado (3 incidentes)

**VERBATIMS:** No disponibles (consistente con crisis operativa severa)

---

## **CAUSA 2: DETERIORO GENERALIZADO DE PUNTUALIDAD**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Efecto dominó operativo donde los problemas iniciales de mishandling generaron retrasos en cadena, cancelaciones reactivas y reprogramaciones masivas. La degradación de OTP15 en 0.9-1.4 puntos sugiere un colapso temporal del sistema de operaciones que se propagó a través de la red de vuelos.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Global (Nodo padre - toda la operación)

**OUTPUT CAUSAL DETALLADO:**
- **Magnitud del impacto:** OTP15 deteriorado a 83.9% vs 84.8% promedio (-0.9 puntos)
- **Correlación:** Directa con 110 retrasos documentados que explican completamente el deterioro
- **Efecto cascada:** Impacto propagado desde problemas de equipaje hacia toda la operación

**SUBSEGMENTOS AFECTADOS:**
- **Long Haul:** OTP15 80.3-83.9% (-0.9 a -1.4pts)
- **Short Haul:** OTP15 81.7-87.9% (-0.4 a -1.1pts)
- **Patrón consistente:** Degradación uniforme en todos los radios y cabinas

**MÉTRICAS CLAVE CONSOLIDADAS:**
- **Indicadores operativos:**
  - 110 incidentes de retrasos (33% del total de incidentes)
  - 42 cancelaciones (13% del total)
  - OTP15 global: 83.9% (-0.9pts)
- **Casos críticos documentados:**
  - IB379 MAD-SJU: Reprogramado +1h15min
  - Emergencia médica con desvío a MIA
  - Efecto dominó en conexiones intercontinentales

---

## **CAUSA 3: SOBRECARGA OPERATIVA POR ALTA OCUPACIÓN**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Load Factor elevado (88.6-93.2%) generó presión extrema en recursos operativos, personal de tierra y sistemas de handling, actuando como catalizador que amplificó otros problemas operativos. La alta ocupación redujo la flexibilidad operativa para gestionar disrupciones y recuperarse de incidentes.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO:** Long Haul (donde el impacto fue más severo)

**OUTPUT CAUSAL DETALLADO:**
- **Magnitud del impacto:** Load Factor 88.6-93.2% vs 87.5-90.1% promedio (+1.1 a +3.1 puntos)
- **Correlación:** Directa con problemas de mishandling y deterioro de servicios
- **Amplificación:** Factor que convirtió problemas menores en crisis sistémica

**SUBSEGMENTOS AFECTADOS:**
- **Long Haul Business:** 92.4% LF - Presión máxima en servicios premium
- **Long Haul Premium:** 92.4% LF - Expectativas altas con recursos limitados
- **Short Haul:** 75.0-86.3% LF - Menor presión pero aún problemático

**MÉTRICAS CLAVE CONSOLIDADAS:**
- **Indicadores operativos:**
  - Load Factor promedio: 88.6% (+1.1pts vs baseline)
  - Picos críticos: 93.2% en Economy LH
  - Correlación directa con flotas problemáticas (A350 C, A33ACMI)
- **Rutas de alta ocupación afectadas:**
  - LAX-MAD: 100% de pasajeros detractores
  - Rutas transatlánticas: Mayor impacto percibido
- **Flotas bajo presión:**
  - A321XLR: NPS 0.0 (sobrecarga operativa)
  - A350 C: NPS -28.6 (recursos limitados)

**EFECTO MULTIPLICADOR CONFIRMADO:** La alta ocupación no causó directamente la anomalía, pero amplificó exponencialmente el impacto de problemas de mishandling y puntualidad, especialmente en segmentos premium con expectativas elevadas.

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 19 de agosto de 2025 reveló una crisis operativa sistémica que impactó diferencialmente a los segmentos de Iberia, con el NPS global manteniéndose aparentemente estable en 24.463 (-0.002 puntos) pero enmascarando severas disrupciones subyacentes. La causa raíz fue un colapso masivo en el manejo de equipaje (mishandling disparado a 28.3% vs 17.4% promedio, +10.9 puntos) acompañado de deterioro generalizado en puntualidad (OTP15 reducido a 83.9% vs 84.8%, -0.9 puntos) y sobrecarga operativa por alta ocupación (Load Factor 88.6% vs 87.5%, +1.1 puntos). Estos problemas se materializaron a través de 329 incidentes operativos documentados, incluyendo 110 retrasos, 42 cancelaciones y casos críticos como 47 equipajes sin cargar del vuelo IB424/BCN y la reprogramación del IB379 MAD-SJU con +1h15min de retraso. La evidencia operativa fue validada por 22 incidentes NCS en Long Haul y 20 en Short Haul, confirmando el alcance sistémico de la crisis.

Las rutas más devastadas fueron LAX-MAD con un NPS de 0.0 (100% detractores en A321XLR), IAD-MAD con -33.3 puntos, y EZE-MAD que impactó severamente el segmento Business. Los grupos de clientes más reactivos fueron los viajeros de negocio internacionales, especialmente en América Norte (-33.3 NPS en Global/Premium) y Oriente Medio (-50.0 NPS), mientras que los clientes de ocio domésticos mostraron mayor resiliencia. Las flotas A350 C, A33ACMI y 32S concentraron los problemas más severos, con dispersiones de hasta 125 puntos entre aeronaves, evidenciando vulnerabilidades operativas específicas por tipo de flota.

**ECONOMY SH: Impacto Operativo Diferencial por Compañía**
La cabina Economy de Short Haul experimentó un comportamiento divergente entre compañías durante el 19 de agosto, con Iberia registrando una caída marginal a NPS 23.48 (-0.46 puntos) mientras Vueling logró una mejora significativa a NPS 39.1 (+11.5 puntos). La causa principal fue la misma crisis operativa de mishandling (29.2% en IB vs 25.7% en YW) y deterioro de puntualidad, pero el impacto diferencial se explica por la composición de clientela: Iberia sufrió más en rutas internacionales y operaciones codeshare (American Airlines -25.0, British Airways 0.0), mientras Vueling se benefició de su base de clientes predominantemente nacional y de ocio, más resilientes a disrupciones. Las flotas de largo radio (A350, A33ACMI) mostraron las mayores caídas con dispersiones de hasta 141 puntos, mientras que rutas como BIO-MAD registraron NPS de 0.0-25.0 puntos.

**BUSINESS SH: Crisis Amplificada por Expectativas Premium**
El segmento Business de Short Haul sufrió el impacto más severo, con Iberia cayendo a NPS 23.08 (-8.35 puntos) y Vueling colapsando a NPS 33.72 (-32.95 puntos). Esta evolución se explica principalmente por la extrema sensibilidad de los clientes de negocio ante la crisis operativa de mishandling (+11.5 puntos) y puntualidad deteriorada, siendo especialmente visible la polarización entre viajeros Business/Work (NPS -33.3) versus Leisure (NPS +30.4). Los 20 incidentes operativos documentados, incluyendo el caso crítico de 47 equipajes sin cargar y múltiples reprogramaciones, impactaron desproporcionadamente a este segmento premium que mantiene expectativas de confiabilidad absoluta.

**ECONOMY LH: Deterioro Moderado con Concentración Geográfica**
La cabina Economy de Long Haul registró una caída a NPS 14.3 (-4.87 puntos) el 19 de agosto, reflejando un impacto moderado pero significativo de la crisis operativa sistémica. La causa principal fue el mishandling crítico (28.3% vs 17.4% promedio, +10.9 puntos) combinado con deterioro de puntualidad (OTP15 80.3% vs 81.8%, -1.4 puntos) y sobrecarga operativa (Load Factor 93.2% vs 90.1%, +3.1 puntos). Esta degradación se manifestó especialmente en la ruta MAD-NRT con NPS 14.3 y mostró un patrón diferencial extremo por flota: mientras A350 next mantuvo un sólido NPS de 53.1, las flotas A321XLR (-25.0) y A350 C (-40.0) experimentaron colapsos severos, evidenciando vulnerabilidades operativas específicas por tipo de aeronave.

**BUSINESS LH: Impacto Severo en Segmento Premium**
La cabina Business de Long Haul experimentó una caída significativa a NPS 22.22 (-13.17 puntos) durante el 19 de agosto, resultado directo de la tormenta perfecta operativa que concentró múltiples fallas en un segmento de alta expectativa. Los drivers principales fueron el mishandling crítico (28.3% vs 17.4%, +10.9 puntos) y deterioro de puntualidad (OTP15 80.3% vs 81.8%, -1.4 puntos), impactando especialmente la ruta EZE-MAD y generando una dispersión récord de 125 puntos entre flotas. La flota A33ACMI registró un catastrófico NPS de -50.0 (4 surveys) contrastando dramáticamente con el excelente desempeño del A350 (NPS 75.0), mientras que la concentración geográfica mostró América Centro con -50.0 versus América Sur con 62.5 puntos.

**PREMIUM LH: Colapso Máximo por Expectativas Elevadas**
El segmento Premium de Long Haul sufrió la caída más severa registrando NPS 11.5 (-17.3 puntos) el 19 de agosto, representando el impacto máximo de la crisis operativa sistémica. Las causas dominantes fueron el mishandling crítico (28.3% vs 17.4%, +10.9 puntos) actuando como factor principal, complementado por Load Factor elevado (92.4% vs 90.1%, +2.3 puntos) y deterioro de puntualidad (OTP15 80.3% vs 81.8%, -1.4 puntos), especialmente evidentes en la ruta LIM-MAD (NPS 60.0) y entre clientes americanos que mostraron la mayor reactividad con NPS -33.3 versus europeos con +33.3, confirmando que los viajeros de negocio internacionales son el perfil más sensible a disrupciones operativas en el segmento premium.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 9
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-18 to 2025-08-18:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 11 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH, Global/SH/Business/IB, Global/SH/Business/YW, Global/SH/Economy, Global/SH/Economy/IB, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 **PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)**

## **A. Economy Short Haul:**

### **Nodos Identificados:**
✅ **Economy SH/IB**: Presente - NPS -2.78 puntos  
✅ **Economy SH/YW**: Presente - NPS -6.05 puntos

### **Análisis Comparativo de Drivers:**

| **Factor** | **SH/Economy/IB** | **SH/Economy/YW** | **Divergencia** |
|------------|-------------------|-------------------|-----------------|
| **Mishandling** | 29.2% vs 17.7% (+11.5pts) | 25.7% vs 16.6% (+9.1pts) | Similar magnitud |
| **OTP15** | 87.9% vs 88.3% (-0.4pts) | 81.7% vs 82.8% (-1.1pts) | YW más afectado |
| **Load Factor** | 90.1% (estable) | 86.3% vs 83.6% (+2.8pts) | Patrones diferentes |
| **Incidentes NCS** | 32 incidentes totales | 32 incidentes totales | Idéntico |

### **Evidencia Operativa:**
- **Común**: Ambas compañías reportan exactamente **32 incidentes NCS** con predominio de cancelaciones (22)
- **Común**: Desvío meteorológico FNC→FAO→MAD como evento desencadenante
- **Diferencial**: IB muestra impacto concentrado en FCO-MAD (NPS 0.0), YW en BRU-MAD

**🎯 DIAGNÓSTICO ECONOMY SH:** **Causa común de cabina** - Ambas compañías muestran el mismo patrón operativo (mishandling crítico, 32 incidentes idénticos) con variaciones menores en manifestación geográfica.

---

## **B. Business Short Haul:**

### **Nodos Identificados:**
✅ **Business SH/IB**: Presente - NPS +8.6 puntos (anomalía positiva)  
✅ **Business SH/YW**: Presente - NPS -11.98 puntos (anomalía negativa)

### **Análisis Comparativo de Drivers:**

| **Factor** | **SH/Business/IB** | **SH/Business/YW** | **Divergencia** |
|------------|-------------------|-------------------|-----------------|
| **Mishandling** | 29.2% vs 17.7% (+11.5pts) | 25.7% vs 16.6% (+9.1pts) | Similar deterioro |
| **OTP15** | 87.9% vs 88.3% (-0.4pts) | 81.7% vs 82.8% (-1.1pts) | YW más deteriorado |
| **Incidentes NCS** | 32 incidentes totales | 32 incidentes totales | Idéntico |
| **Dirección NPS** | **POSITIVA (+8.6)** | **NEGATIVA (-11.98)** | **OPUESTA** |

### **Evidencia Operativa Diferencial:**
- **IB**: Dispersión regional extrema (86.7 pts) con compensación estadística - América Norte devastada (-33.3) pero otras regiones excepcionales (+53.3)
- **YW**: Impacto diferenciado por propósito (Leisure NPS 5.9 vs Business 66.7) sin compensación regional

**🎯 DIAGNÓSTICO BUSINESS SH:** **Causa específica de compañía** - Mismo deterioro operativo base pero **direcciones opuestas en NPS** debido a diferentes mecanismos de compensación y perfiles de cliente afectados.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ **PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)**

## **A. Short Haul - Análisis de Cabinas:**

### **Patrones Operativos Base:**
| **Cabina** | **Mishandling** | **OTP15** | **Incidentes NCS** | **Magnitud NPS** |
|------------|-----------------|-----------|-------------------|------------------|
| **Economy SH** | +9.1 a +11.5pts | -0.4 a -1.1pts | 32 idénticos | -2.78 a -6.05 |
| **Business SH** | +9.1 a +11.5pts | -0.4 a -1.1pts | 32 idénticos | +8.6 a -11.98 |

### **Análisis de Convergencia/Divergencia:**

#### **Factores Convergentes:**
- **Mismo deterioro operativo**: Ambas cabinas experimentan mishandling crítico (+9-11pts) y problemas de puntualidad
- **Mismo volumen de incidentes**: 32 NCS con patrón idéntico de cancelaciones (22)
- **Mismo evento desencadenante**: Condiciones meteorológicas adversas FNC

#### **Factores Divergentes Críticos:**
- **Dirección del impacto**: Economy consistentemente negativa (-2.78 a -6.05) vs Business con direcciones opuestas (+8.6 IB, -11.98 YW)
- **Reactividad diferencial**: Business muestra **mayor volatilidad** (rango 20.58 pts) vs Economy (rango 3.27 pts)
- **Mecanismos de compensación**: Business IB logra compensación regional, Economy no

#### **Consistencia Entre Compañías:**
- **Economy**: Patrón consistente IB/YW - ambas negativas con misma causa raíz
- **Business**: Patrón **inconsistente** IB/YW - direcciones opuestas con misma base operativa

**🎯 DIAGNÓSTICO SHORT HAUL:** **Causa común de radio con reactividad específica de cabina** - El deterioro operativo es idéntico, pero Business muestra mayor sensibilidad y capacidad de compensación regional que Economy.

---

## **B. Long Haul - Análisis de Cabinas:**

### **Patrones Operativos Base:**
| **Cabina** | **Mishandling** | **OTP15** | **Load Factor** | **Magnitud NPS** |
|------------|-----------------|-----------|-----------------|------------------|
| **Economy LH** | 28.3% (+10.9pts) | 80.3% (-1.4pts) | 93.2% (+3.1pts) | -2.4 puntos |
| **Business LH** | 28.3% (+10.9pts) | 80.3% (-1.4pts) | 92.4% (+2.3pts) | -18.1 puntos |
| **Premium LH** | 28.3% (+10.9pts) | 80.3% (-1.4pts) | 92.4% (+2.3pts) | -34.77 puntos |

### **Análisis de Progresión de Reactividad:**

#### **Convergencia Operativa Total:**
- **Métricas idénticas**: Las tres cabinas reportan exactamente los mismos valores operativos
- **Mismo evento desencadenante**: Crisis operativa con 297 incidentes totales
- **Misma causa raíz**: Mishandling crítico como factor dominante

#### **Progresión Lógica de Impacto:**
```
Economy LH:  -2.4 puntos  (Línea base de impacto)
Business LH: -18.1 puntos (7.5x más reactivo)
Premium LH:  -34.77 puntos (14.5x más reactivo)
```

#### **Reactividad Diferencial por Expectativas:**
- **Economy**: Tolerancia base a problemas operativos
- **Business**: **Mayor sensibilidad** debido a expectativas de servicio premium
- **Premium**: **Máxima reactividad** - expectativas más altas generan mayor insatisfacción ante mismos problemas

#### **Patrón de Amortiguación:**
- **Economy actúa como amortiguador**: Menor reactividad absorbe mejor el impacto operativo
- **Premium amplifica el impacto**: Mayor sensibilidad convierte problemas operativos en crisis de satisfacción

**🎯 DIAGNÓSTICO LONG HAUL:** **Causa común de radio con progresión lógica de reactividad por cabina** - Deterioro operativo idéntico pero impacto exponencialmente mayor conforme aumenta la clase de servicio debido a expectativas diferenciadas del cliente.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 **PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL**

## **A. Comparación Entre Radios:**

### **Estado de Afectación:**
✅ **Ambos radios afectados** - Short Haul (-3.4 a -6.05 pts) y Long Haul (-2.4 a -34.77 pts)

### **Convergencia de Drivers Principales:**

| **Driver** | **Short Haul** | **Long Haul** | **Convergencia** |
|------------|----------------|---------------|------------------|
| **Mishandling** | +9.1 a +11.5pts | +10.9pts | ✅ **IDÉNTICA** |
| **OTP15** | -0.4 a -1.1pts | -1.4pts | ✅ **CONVERGENTE** |
| **Load Factor** | +0.9 a +2.8pts | +2.3 a +3.1pts | ✅ **CONVERGENTE** |
| **Incidentes NCS** | 32-33 incidentes | 297 incidentes | ⚠️ **ESCALAS DIFERENTES** |

### **Evidencia Operativa Consistente:**
- **Evento desencadenante común**: Condiciones meteorológicas adversas (desvío FNC→FAO→MAD)
- **Patrón de cascada idéntico**: Meteorología → Cancelaciones → Mishandling → Deterioro NPS
- **Mismo día crítico**: 18 de agosto como "tormenta perfecta operativa"
- **Causa raíz compartida**: Crisis de mishandling como factor dominante en ambos radios

**🔍 CONVERGENCIA CONFIRMADA:** Ambos radios muestran **drivers idénticos** con diferencias solo en escala operativa (SH: 32 incidentes, LH: 297 incidentes).

---

## **B. Coherencia con Nodo Global:**

### **Análisis de Agregación:**

| **Nivel** | **NPS Impacto** | **Mishandling** | **Patrón** |
|-----------|-----------------|-----------------|------------|
| **Global** | -2.94 puntos | 28.3% (+10.9pts) | Agregado coherente |
| **SH Range** | -3.4 a -6.05 pts | +9.1 a +11.5pts | Contribuye al Global |
| **LH Range** | -2.4 a -34.77 pts | +10.9pts | Contribuye al Global |

### **Validación de Coherencia:**

#### **✅ Coherencia Confirmada:**
- **Global NPS (-2.94)** refleja promedio ponderado entre SH y LH
- **Global Mishandling (28.3%)** es consistente con valores de ambos radios
- **Mismo evento desencadenante**: Desvío meteorológico FNC reportado en todos los niveles
- **297 incidentes Global** incluye los 32-33 de SH como subconjunto

#### **📊 Patrón de Agregación:**
- **No hay efectos compensatorios**: Ambos radios negativos se suman al Global negativo
- **No hay normalidad enmascarada**: Global refleja fielmente el deterioro de sus componentes
- **Amplificación coherente**: Global no atenúa sino que refleja la magnitud real del problema

#### **🔗 Evidencia Operativa Global:**
- **297 incidentes totales** con 82 cancelaciones confirman escala masiva
- **Mishandling crítico (28.3%)** como factor unificador entre todos los niveles
- **Impacto geográfico consistente**: FNC-MAD (-50.0) como epicentro identificado en múltiples niveles

---

## **🎯 DIAGNÓSTICO FINAL:**

**Causa global homogénea confirmada** - Las condiciones meteorológicas adversas del 18 de agosto generaron una crisis operativa sistémica que afectó uniformemente ambos radios con los mismos drivers (mishandling crítico, deterioro de puntualidad, sobrecarga operativa), manifestándose coherentemente desde el nivel Global hasta los segmentos más granulares sin efectos compensatorios o patrones divergentes.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 **PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS**

## **CAUSA 1: CRISIS DE MISHANDLING CRÍTICO**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** El deterioro masivo en la gestión de equipajes (+10.9 puntos, alcanzando 28.3% vs 17.4% promedio) representa la traducción directa de la sobrecarga operativa en experiencia tangible del cliente. Cuando los sistemas de handling colapsan por volumen excesivo y disrupciones, el cliente experimenta inmediatamente la pérdida, retraso o daño de su equipaje, generando insatisfacción inmediata y medible.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **GLOBAL** (todos los clientes)

**Output causal detallado:**
- **Magnitud del deterioro:** 28.3% vs 17.4% baseline (+10.9 puntos, +62% incremento)
- **Correlación directa con NPS:** Factor más crítico identificado en todos los niveles de análisis
- **Validación operativa:** 5 incidentes específicos de equipaje dentro de los 297 totales

**Alcance confirmado:** Esta causa afecta a **todos los subsegmentos** bajo el nodo Global:
- Short Haul: +9.1 a +11.5 puntos de deterioro
- Long Haul: +10.9 puntos de deterioro  
- Todas las cabinas (Economy, Business, Premium)
- Ambas compañías (IB, YW)

**Métricas clave:**
- **Indicador operativo:** Mishandling 28.3% (peor día de la semana)
- **Impacto NPS:** Factor dominante en caída de -2.94 puntos Global
- **Rutas específicas:** FNC-MAD (-50.0 NPS) como epicentro
- **Verbatims:** No disponibles para el período

---

## **CAUSA 2: CASCADA DE DISRUPCIONES METEOROLÓGICAS**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Las condiciones meteorológicas adversas en Funchal actuaron como evento desencadenante de una cascada operativa sistémica. Un solo desvío (FNC→FAO→MAD) generó efectos dominó que colapsaron múltiples aspectos de la operación, desde cancelaciones masivas hasta cambios de aeronave, creando una "tormenta perfecta" operativa que amplificó exponencialmente el impacto en la experiencia del cliente.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **GLOBAL** (toda la red operativa)

**Output causal detallado:**
- **Evento desencadenante:** Desvío vuelo IB048 por vientos fuertes en FNC
- **Escalada documentada:** 297 incidentes totales con 82 cancelaciones
- **Efecto cascada:** Meteorología → Cancelaciones → Sobrecarga → Mishandling → NPS

**Alcance confirmado:** Esta causa afecta a **todos los subsegmentos** bajo el nodo Global:
- **297 incidentes operativos totales** distribuidos en toda la red
- **82 cancelaciones** impactando múltiples rutas y conexiones
- **22 cambios de avión** afectando diferentes flotas
- **76 pérdidas de conexión** impactando clientes en tránsito

**Métricas clave:**
- **Indicador operativo:** 297 incidentes NCS (volumen extraordinario)
- **Impacto NPS:** Correlación directa con deterioro -2.94 puntos
- **Rutas específicas:** FNC-MAD como epicentro (-50.0 NPS), MAD-MEX (16.7 NPS)
- **Casos emblemáticos:** IB048 desvío FNC→FAO→MAD, IB0559 (3 incidentes)
- **Verbatims:** No disponibles para el período

---

## **CAUSA 3: SOBRECARGA OPERATIVA CRÍTICA**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** El incremento del Load Factor (88.6% vs 87.5% promedio) combinado con las disrupciones generó una sobrecarga sistémica donde la capacidad operativa fue superada por la demanda real. Las cancelaciones concentraron pasajeros en vuelos restantes, creando densidades críticas que deterioraron la calidad del servicio y amplificaron el impacto de otros problemas operativos.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **GLOBAL** (toda la operación)

**Output causal detallado:**
- **Load Factor crítico:** 88.6% vs 87.5% baseline (+1.1 puntos)
- **Concentración por cancelaciones:** 82 cancelaciones redistribuyeron pasajeros
- **Amplificación de problemas:** Mayor densidad = mayor impacto de mishandling y retrasos

**Alcance confirmado:** Esta causa afecta a **todos los subsegmentos** bajo el nodo Global:
- Long Haul: 92.4% a 93.2% (sobrecarga crítica)
- Short Haul: 86.3% a 90.1% (sobrecarga moderada)
- Todas las cabinas experimentando mayor densidad

**Métricas clave:**
- **Indicador operativo:** Load Factor 88.6% (pico semanal)
- **Impacto NPS:** Factor contributivo a deterioro -2.94 puntos
- **Correlación:** Mayor ocupación correlaciona con peor experiencia
- **Efecto multiplicador:** Amplifica impacto de mishandling y retrasos
- **Verbatims:** No disponibles para el período

---

## **CAUSA 4: DETERIORO DE PUNTUALIDAD SISTÉMICO**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** La caída del OTP15 (83.9% vs 84.8% promedio) refleja la incapacidad del sistema para mantener horarios programados bajo presión operativa extrema. Los retrasos generan frustración inmediata en clientes sensibles al tiempo, especialmente en segmentos Business, y crean efectos cascada que deterioran conexiones y experiencias posteriores.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **GLOBAL** (toda la red de vuelos)

**Output causal detallado:**
- **OTP15 deteriorado:** 83.9% vs 84.8% baseline (-0.9 puntos)
- **Validación operativa:** 50 retrasos confirmados dentro de 297 incidentes
- **Impacto diferencial:** Mayor sensibilidad en segmentos Business y Premium

**Alcance confirmado:** Esta causa afecta a **todos los subsegmentos** bajo el nodo Global:
- Short Haul: -0.4 a -1.1 puntos de deterioro OTP
- Long Haul: -1.4 puntos de deterioro OTP
- Especial impacto en Business (-18.1 pts) y Premium (-34.77 pts)

**Métricas clave:**
- **Indicador operativo:** OTP15 83.9% (deterioro semanal)
- **Impacto NPS:** Factor contributivo especialmente en cabinas premium
- **Retrasos confirmados:** 50 incidentes específicos de retrasos
- **Sensibilidad diferencial:** Business/Premium más reactivos que Economy
- **Verbatims:** No disponibles para el período

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 18 de agosto de 2025 registró una caída generalizada del NPS debido a una crisis operativa desencadenada por condiciones meteorológicas adversas en Funchal. El impacto global fue de -2.94 puntos (21.52 vs 24.47 baseline), siendo el peor día operativo de la semana. Las causas principales fueron el deterioro crítico del mishandling que se disparó al 28.3% vs 17.4% promedio (+10.9 puntos), validado por 297 incidentes operativos totales incluyendo 82 cancelaciones y el desvío emblemático del vuelo IB048 por vientos fuertes. Esta crisis se amplificó por la sobrecarga operativa con Load Factor de 88.6% vs 87.5% promedio y el deterioro de puntualidad con OTP15 de 83.9% vs 84.8% baseline. Los segmentos más afectados muestran una progresión clara: Global/LH experimentó caídas de -2.4 puntos en Economy, -18.1 puntos en Business y -34.77 puntos en Premium, mientras que Global/SH registró deterioros de -3.4 puntos generales con variaciones por compañía de -2.78 puntos en IB y -6.05 puntos en YW para Economy.

Las rutas más impactadas incluyen FNC-MAD con un NPS devastador de -50.0, MAD-MEX con 16.7 puntos, FCO-MAD con 0.0 puntos y DSS-MAD con -33.3 puntos, todas correlacionadas con el epicentro meteorológico y sus efectos cascada. Los grupos de clientes más reactivos fueron los residentes de África (NPS -100.0) y Asia (NPS -71.4 a -80.0), la flota A33ACMI (NPS -23.4 a -37.9), los partners de codeshare LATAM (NPS -46.7) y American Airlines (NPS -44.4), y particularmente los viajeros de negocios que mostraron mayor sensibilidad con caídas de hasta -36.4 puntos vs leisure, evidenciando expectativas más altas ante disrupciones operativas.

**ECONOMY SH: Crisis Operativa con Impacto Diferencial por Compañía**
La cabina Economy de SH experimentó un deterioro significativo durante el 18 de agosto de 2025, con IB registrando un NPS de 21.15 (caída de -2.78 puntos) y YW mostrando mayor impacto con 21.55 (deterioro de -6.05 puntos). La causa principal fue la crisis de mishandling que alcanzó 25.7% a 29.2% vs promedios de 16.6% a 17.7%, complementada por 32 incidentes operativos idénticos en ambas compañías dominados por 22 cancelaciones masivas. Este deterioro se reflejó especialmente en rutas como FCO-MAD (NPS 0.0) para IB y BRU-MAD para YW, mientras que los perfiles más reactivos incluyen residentes de Asia (NPS -100.0 a -80.0), flota ATR (NPS 10.3) y operaciones de codeshare con partners específicos.

**BUSINESS SH: Divergencia Extrema Entre Compañías**
El segmento Business de SH mostró direcciones completamente opuestas, con IB registrando un NPS de 40.0 (mejora de +8.6 puntos) mientras YW experimentó 21.74 (caída de -11.98 puntos). Esta divergencia se explica principalmente por mecanismos de compensación regional diferentes: IB logró dispersión extrema de 86.7 puntos donde América Norte colapsó (-33.3) pero otras regiones compensaron (+53.3), mientras YW mostró impacto diferenciado por propósito de viaje con Leisure devastado (5.9) vs Business resiliente (66.7). El patrón fue especialmente visible en rutas como LHR-MAD (NPS 60.0) para IB y entre perfiles donde los viajeros de ocio mostraron 60.8 puntos menos tolerancia que business ante las mismas disrupciones operativas.

**ECONOMY LH: Impacto Moderado con Devastación en Segmentos Business**
La cabina Economy de LH experimentó un deterioro controlado, registrando un NPS de 16.8 (caída de -2.4 puntos) respecto al baseline de 19.2. La causa principal fue la tormenta perfecta operativa con mishandling crítico de 28.3% vs 17.4% promedio (+10.9 puntos), validada por 33 incidentes NCS con 16 cancelaciones y el caso emblemático IB048 desviado por vientos fuertes, complementada por sobrecarga operativa con Load Factor de 93.2% vs 90.1% promedio. Esta caída se reflejó especialmente en rutas como MAD-ORD (NPS -12.5) y entre segmentos de viajeros de negocios que mostraron NPS de -36.4 vs +20.1 de leisure, evidenciando que los problemas operativos impactan desproporcionadamente a clientes sensibles al tiempo con expectativas más altas.

**BUSINESS LH: Colapso Severo por Expectativas Premium**
La cabina Business de LH sufrió un deterioro severo, registrando un NPS de 17.2 (caída dramática de -18.1 puntos) vs baseline de 35.4. Los drivers principales fueron la crisis multifactorial que combinó mishandling crítico (+10.9 puntos), 33 incidentes operativos con predominio de cancelaciones, y problemas específicos de flota A333 (NPS -71.4) junto con colapso total de operaciones codeshare con American Airlines (NPS -100.0). El impacto fue especialmente evidente en rutas transatlánticas hacia América del Norte y entre clientes leisure (NPS 12.0) que mostraron menor tolerancia que business (50.0) a las disrupciones, reflejando que las expectativas premium amplifican la insatisfacción ante problemas operativos idénticos a los de Economy.

**PREMIUM LH: Devastación Máxima por Hipersensibilidad**
El segmento Premium de LH experimentó el colapso más severo, registrando un NPS de 28.87 (caída catastrófica de -34.77 puntos) vs baseline de 63.64. Las causas dominantes fueron la crisis de mishandling que alcanzó 28.3% (+10.9 puntos vs promedio) amplificada por las expectativas más altas del segmento, donde los mismos problemas operativos que afectaron a todas las cabinas generaron impacto exponencialmente mayor. La devastación fue especialmente evidente en operaciones con flota A350 tradicional (NPS 50) vs A350 next (60) y entre destinos de América Centro (NPS 50), demostrando que el segmento Premium actúa como amplificador de cualquier deficiencia operativa debido a la hipersensibilidad de clientes con expectativas de servicio excepcional.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 11
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
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