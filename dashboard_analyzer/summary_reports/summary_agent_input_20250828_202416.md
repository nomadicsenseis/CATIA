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
[{'period': 1, 'date_range': '2025-08-15 to 2025-08-21', 'ai_interpretation': '📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**\n\n**Nodos analizados:** 5 (Global, Global/LH, Global/LH/Economy, Global/SH/Business, Global/SH/Business/IB)\n\n---\n\n## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA\n\n# 🏢 **PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)**\n\n## **A. Economy Short Haul:**\n\n❌ **NO EXISTE SEPARACIÓN POR COMPAÑÍAS**\n- Solo existe el nodo padre **Global/SH** sin desglose por Economy\n- No hay nodos **Economy SH/IB** ni **Economy SH/YW** disponibles\n- **Razón de ausencia:** La segmentación disponible no incluye cabina Economy en Short Haul a nivel de compañía\n\n## **B. Business Short Haul:**\n\n✅ **EXISTE SOLO NODO Business SH/IB**\n- **Nodo disponible:** Global/SH/Business/IB (anomalía -8.05 pts)\n- **Nodo faltante:** Global/SH/Business/YW \n- **Razón de ausencia:** Likely insufficient sample size para YW Business en Short Haul durante el período analizado\n\n## **🎯 DIAGNÓSTICO CONCLUSIVO:**\n\n**Para Business Short Haul:** **IMPOSIBLE DETERMINAR** si la causa es específica de compañía IB o general a la cabina, ya que solo existe evidencia del nodo IB. La anomalía negativa de -8.05 pts en Business SH/IB no puede ser comparada con YW por ausencia de datos.\n\n**Implicación:** El análisis de causas debe proceder asumiendo que los hallazgos en Business SH/IB podrían ser representativos de toda la cabina Business Short Haul, con la limitación de no poder validar si es un problema específico de la compañía Iberia.\n\n---\n\n## 💺 DIAGNÓSTICO A NIVEL DE CABINA\n\n# ✈️ **PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)**\n\n## **A. Short Haul - Análisis de Cabinas:**\n\n### **Nodos Disponibles:**\n- **Global/SH/Business/IB:** Anomalía -8.05 pts\n- **Economy SH:** ❌ No disponible (sin nodos separados)\n\n### **Análisis de Patrón:**\n**IMPOSIBLE DETERMINAR CONVERGENCIA/DIVERGENCIA** debido a la ausencia del nodo Economy SH. Solo disponemos de Business SH/IB que muestra:\n- Drivers negativos dominantes: Journey preparation support (-3.958 SHAP) y Check-in (-2.658 SHAP)\n- Causa principal: **Deterioro en touchpoints digitales**, no operativa\n\n## **B. Long Haul - Análisis de Cabinas:**\n\n### **Nodos Disponibles:**\n- **Global/LH:** Anomalía +10.94 pts\n- **Global/LH/Economy:** Anomalía +12.58 pts\n- **Business LH y Premium LH:** ❌ No disponibles\n\n### **Análisis de Patrón:**\n**CONVERGENCIA COMPLETA ENTRE NODOS LH DISPONIBLES:**\n\n**Drivers Principales Convergentes:**\n- **Punctuality:** LH general (+6.457 SHAP) vs LH/Economy (+7.208 SHAP)\n- **Boarding:** LH general (+1.578 SHAP) vs LH/Economy (+1.725 SHAP)\n- **Arrivals Experience:** LH general (+1.494 SHAP) vs LH/Economy (+1.593 SHAP)\n\n**Evidencia Operativa Convergente:**\n- **Reducción incidentes:** LH general (-45.3%) vs LH/Economy (-45.3%)\n- **Mejora OTP15:** Ambos nodos +2.2 puntos (78.1% → 80.35%)\n- **Rutas críticas:** MAD-MIA, MAD-MEX, GUA-MAD consistentes en ambos\n\n## **🎯 DIAGNÓSTICO CONCLUSIVO:**\n\n**Short Haul:** **ANÁLISIS INCOMPLETO** - No es posible determinar si el patrón es común al radio debido a la ausencia de Economy SH.\n\n**Long Haul:** **CAUSA COMÚN AL RADIO** - Perfecta convergencia entre nodos disponibles (LH general y LH/Economy) en drivers SHAP, evidencia operativa y rutas afectadas. La mejora operativa sistémica en puntualidad y boarding impacta homogéneamente a todas las cabinas Long Haul analizadas.\n\n---\n\n## 🌎 DIAGNÓSTICO GLOBAL POR RADIO\n\n# 🌍 **PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL**\n\n## **A. Comparación Entre Radios:**\n\n### **Ambos Radios Afectados con Patrones Divergentes:**\n\n**Long Haul: ANOMALÍA POSITIVA DOMINANTE**\n- **Global/LH:** +10.94 pts | **Global/LH/Economy:** +12.58 pts\n- **Driver principal:** Punctuality (+6.457 a +7.208 SHAP)\n- **Evidencia operativa:** Reducción incidentes -45.3%, mejora OTP15 +2.2 pts\n\n**Short Haul: ANOMALÍA NEGATIVA ESPECÍFICA**\n- **Global/SH/Business/IB:** -8.05 pts\n- **Driver principal:** Journey preparation support (-3.958 SHAP) y Check-in (-2.658 SHAP)\n- **Evidencia operativa:** Mejora NCS (-38.9% incidentes) pero deterioro experiencia digital\n\n### **Divergencia Crítica en Drivers:**\n- **LH:** Causas **operativas** (puntualidad, boarding, arrivals)\n- **SH:** Causas de **producto/experiencia digital** (journey prep, check-in)\n\n## **B. Coherencia con Nodo Global:**\n\n### **Global Refleja Dominancia Long Haul:**\n- **Global:** +5.10 pts (anomalía positiva neta)\n- **Patrón Global:** Punctuality (+3.365 SHAP) como driver dominante\n- **Evidencia operativa Global:** Reducción total incidentes -33.1%\n\n### **Interpretación de Agregación:**\nEl nodo Global muestra **efecto neto positivo** donde:\n- La **mejora operativa masiva en Long Haul** (+10.94 a +12.58 pts) \n- **Compensa y supera** el deterioro digital en Short Haul Business (-8.05 pts)\n- Resultado: Anomalía global positiva moderada (+5.10 pts)\n\n## **🎯 DIAGNÓSTICO CONCLUSIVO:**\n\n**CAUSAS MIXTAS CON DOMINANCIA LONG HAUL** - Los dos radios presentan patrones causales completamente divergentes: Long Haul experimenta una mejora operativa sistémica excepcional (drivers operativos positivos) mientras Short Haul sufre deterioro en experiencia digital (drivers de producto negativos). El nodo Global refleja la dominancia cuantitativa del impacto positivo Long Haul, generando una anomalía global neta positiva (+5.10 pts) que enmascara pero no elimina los problemas específicos de Short Haul.\n\n---\n\n## 📋 ANÁLISIS DE CAUSAS DETALLADO\n\n# 🔍 **PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS**\n\n## **CAUSA 1: MEJORA OPERATIVA SISTÉMICA EN LONG HAUL**\n\n### **A. NATURALEZA DE LA CAUSA:**\n**Hipótesis:** Implementación exitosa de mejoras operativas integrales que optimizaron simultáneamente la puntualidad, procesos de boarding y experiencia de llegadas, generando un efecto multiplicador en la satisfacción del cliente durante vuelos de largo radio.\n\n### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**\n\n**Segmento más grande afectado:** **Global/LH** (afecta a todos los subsegmentos Long Haul)\n\n**Output Causal Detallado:**\n- **Anomalía:** +10.94 pts (17.75 vs 6.80 NPS baseline)\n- **Driver dominante:** Punctuality (SHAP +6.457, satisfacción +5.79 pts)\n- **Drivers secundarios:** Boarding (+1.578 SHAP), Arrivals Experience (+1.494 SHAP), Journey Preparation Support (+1.265 SHAP)\n- **Factor negativo:** IB Plus Loyalty Program (-0.909 SHAP)\n\n**Métricas Operativas Clave:**\n- **Mejora OTP15:** +2.2 puntos (78.1% → 80.35%)\n- **Reducción total incidentes NCS:** -45.3% (223 → 122 incidentes)\n- **Reducción retrasos:** -34.5% (110 → 72 incidentes)\n- **Reducción otras incidencias:** -67.0% (88 → 29 incidentes)\n\n**Rutas Críticas Involucradas:**\n- **GUA-MAD:** NPS 40.7 (27 pax) - Punctuality CSAT 81.9%\n- **MAD-MIA:** NPS 35.0 (103 pax) - Punctuality CSAT 78.6%\n- **MAD-MEX:** NPS 25.1 - Arrivals CSAT 80.6%\n- **Total pasajeros analizados:** 795\n\n**Validación Cualitativa:** 3,000 análisis de verbatims sobre boarding confirman mejoras percibidas.\n\n---\n\n## **CAUSA 2: DETERIORO EN EXPERIENCIA DIGITAL SHORT HAUL BUSINESS**\n\n### **A. NATURALEZA DE LA CAUSA:**\n**Hipótesis:** Fallas sistémicas en touchpoints digitales pre-vuelo (journey preparation y check-in) que impactaron desproporcionadamente al segmento Business Short Haul, donde las expectativas de servicio digital son más altas y la tolerancia a problemas es menor.\n\n### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**\n\n**Segmento más grande afectado:** **Global/SH/Business/IB** (único nodo disponible, representa el patrón Business SH)\n\n**Output Causal Detallado:**\n- **Anomalía:** -8.05 pts (28.95 vs 37.0 NPS baseline)\n- **Drivers negativos críticos:** Journey preparation support (-3.958 SHAP), Check-in (-2.658 SHAP), Punctuality (-2.319 SHAP)\n- **Driver positivo compensatorio:** Wi-Fi (+3.690 SHAP)\n- **Impacto combinado touchpoints digitales:** -6.616 SHAP\n\n**Métricas Operativas Contradictorias:**\n- **Mejora NCS:** -38.9% incidentes totales (262 → 160)\n- **OTP15:** Deterioro marginal -0.3 pts (88.18% → 87.89%)\n- **Load Factor:** Aumento +1.5 pts (73.48% → 74.98%)\n- **Mishandling:** Aumento +4.5 incidentes\n\n**Rutas Críticas Involucradas:**\n- **ARN-MAD:** NPS -33.3 (3 pax) - Check-in CSAT 66.7%\n- **LIN-MAD:** NPS -10.0 (10 pax) - Wi-Fi 100% pero otros factores deteriorados\n- **EAS-MAD:** NPS 0.0 (7 pax) - Check-in problemático 71.4%\n- **MAD-VCE:** NPS 77.8 (9 pax) - Wi-Fi 100% (valida SHAP positivo)\n\n**Validación Cualitativa:** 302 análisis de verbatims sobre boarding confirman problemas específicos en procesos.\n\n**Reactividad Diferencial:** Fleet (166.0 pts spread) y Residence Region (156.6 pts spread) muestran máxima sensibilidad al deterioro.\n\n---\n\n## **🎯 SÍNTESIS DE ALCANCE:**\n\n- **CAUSA 1** afecta a **todo el ecosistema Long Haul** (Global/LH y Global/LH/Economy con patrones idénticos)\n- **CAUSA 2** afecta específicamente a **Business Short Haul** (evidencia solo en IB, pero patrón likely extensible a toda la cabina)\n\n---\n\n## 📋 SÍNTESIS EJECUTIVA FINAL\n\n📈 SÍNTESIS EJECUTIVA:\n\nDurante la semana del 15 al 21 de agosto de 2025, Iberia experimentó un patrón dual de evolución del NPS caracterizado por una mejora excepcional en Long Haul contrastada con deterioro específico en Business Short Haul. A nivel global, el NPS mejoró 5.10 puntos (de 15.99 a 21.09), impulsado principalmente por una mejora operativa sistémica en vuelos de largo radio que elevó el NPS de Long Haul en 10.94 puntos (de 6.80 a 17.75), con Economy Long Haul liderando con una subida de 12.58 puntos (de 3.08 a 15.66). Esta mejora se sustentó en la optimización de la puntualidad (SHAP +6.457 a +7.208), procesos de boarding y experiencia de llegadas, respaldada por una reducción del 45.3% en incidentes operativos y una mejora de 2.2 puntos en OTP15. Simultáneamente, Business Short Haul experimentó un deterioro de 8.05 puntos (de 37.0 a 28.95 NPS), causado por fallas en touchpoints digitales pre-vuelo, específicamente journey preparation support (SHAP -3.958) y check-in (SHAP -2.658), a pesar de mejoras operativas generales.\n\nLas rutas más beneficiadas se concentraron en América Latina, destacando GUA-MAD (NPS 40.7), MAD-MIA (NPS 35.0) y MAD-MEX (NPS 31.5), mientras que las rutas europeas Short Haul como ARN-MAD (NPS -33.3) y LIN-MAD (NPS -10.0) experimentaron los mayores deterioros. Los clientes más reactivos a estos cambios fueron aquellos segmentados por región de residencia (spreads de hasta 125.5 puntos) y tipo de flota (spreads de hasta 166.0 puntos), evidenciando sensibilidades diferenciadas según mercado geográfico y configuración de aeronave.\n\n**ECONOMY SH: Desempeño Estable**\nLa cabina Economy de Short Haul mantuvo desempeño estable durante la semana del 15 al 21 de agosto, sin datos específicos disponibles para análisis detallado. No se detectaron cambios significativos a nivel semanal, sugiriendo niveles consistentes de satisfacción en este segmento.\n\n**BUSINESS SH: Deterioro en Experiencia Digital**\nEl segmento Business de Short Haul experimentó un deterioro significativo de 8.05 puntos, registrando un NPS de 28.95 (versus 37.0 la semana anterior). Esta evolución se explica principalmente por fallas sistémicas en journey preparation support (SHAP -3.958) y procesos de check-in (SHAP -2.658), parcialmente compensadas por mejoras en Wi-Fi (SHAP +3.690), siendo especialmente visible en rutas como ARN-MAD (NPS -33.3) y LIN-MAD (NPS -10.0), y entre perfiles diferenciados por tipo de flota y región de residencia.\n\n**ECONOMY LH: Mejora Operativa Excepcional**\nLa cabina Economy de Long Haul lideró las mejoras con una subida de 12.58 puntos, registrando un NPS de 15.66 (versus 3.08 la semana anterior). La causa principal fue una mejora operativa sistémica centrada en puntualidad (SHAP +7.208), complementada por optimización en boarding (+1.725 SHAP) y arrivals experience (+1.593 SHAP), respaldada por una reducción del 45.3% en incidentes operativos. Esta mejora se reflejó especialmente en rutas como MAD-MIA (NPS 40.0), MAD-MEX (NPS 32.5) y GUA-MAD (NPS 44.0), mientras que los perfiles más reactivos incluyen segmentación por región de residencia y tipo de flota.\n\n**BUSINESS LH: Desempeño Estable**\nLa cabina Business de Long Haul mantuvo desempeño estable durante la semana analizada, sin datos específicos disponibles para análisis detallado. No se detectaron cambios significativos a nivel semanal, manteniendo niveles consistentes de satisfacción.\n\n**PREMIUM LH: Desempeño Estable**\nEl segmento Premium de Long Haul mantuvo desempeño estable durante la semana del 15 al 21 de agosto, sin variaciones significativas detectadas a nivel semanal. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción.\n\n---\n\n✅ **ANÁLISIS COMPLETADO**\n\n- **Nodos procesados:** 5\n- **Pasos de análisis:** 5\n- **Metodología:** Análisis conversacional paso a paso\n- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado\n\n*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*'}]

**ANÁLISIS DIARIO SINGLE:**
📅 2025-08-21 to 2025-08-21:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 11 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH, Global/SH/Business, Global/SH/Business/IB, Global/SH/Business/YW, Global/SH/Economy, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. Economy Short Haul:**

**NODOS IDENTIFICADOS:**
✅ **Economy SH/YW existe**: Global/SH/Economy/YW  
❌ **Economy SH/IB NO existe**: Sin nodo específico en el árbol

**ANÁLISIS DEL NODO EXISTENTE (SH/Economy/YW):**
- **Anomalía**: +20.37 puntos (positiva excepcional)
- **Drivers principales**: Mishandling crítico +9.1pts, Load Factor elevado +2.8pts, OTP deteriorado -1.1pts
- **Evidencia operativa**: 23 incidentes NCS, ruta MAD-XRY como epicentro (NPS 28.6)
- **Segmentos más afectados**: Others CodeShare (NPS -60.0), Business travelers (NPS 0.0)

**DIAGNÓSTICO ECONOMY SH**: **Causa específica de YW** - Solo YW presenta anomalía con problemas operativos localizados, mientras que IB no registra anomalía significativa en Economy SH.

---

## **B. Business Short Haul:**

**NODOS IDENTIFICADOS:**
✅ **Business SH/IB existe**: Global/SH/Business/IB  
✅ **Business SH/YW existe**: Global/SH/Business/YW

**ANÁLISIS COMPARATIVO:**

| Métrica | SH/Business/IB | SH/Business/YW | Convergencia |
|---------|----------------|----------------|--------------|
| **Anomalía NPS** | -4.23 pts | -22.57 pts | ❌ **DIVERGEN** |
| **Mishandling** | 29.2% (+11.5pts) | 25.7% (+9.1pts) | ✅ **CONVERGEN** |
| **OTP15** | 87.9% (-0.4pts) | 81.7% (-1.1pts) | ⚠️ **PARCIAL** |
| **Flota crítica** | A320neo (NPS 11.1) | No especificado | ❌ **DIVERGEN** |
| **Ruta crítica** | No identificada | LCG-MAD (NPS -33.3) | ❌ **DIVERGEN** |
| **Incidentes NCS** | 23 (82.6% retrasos) | 23 (82.6% retrasos) | ✅ **CONVERGEN** |

**DIAGNÓSTICO BUSINESS SH**: **Causa común de cabina con manifestaciones específicas por compañía** - Ambas compañías comparten los mismos drivers operativos críticos (Mishandling elevado, deterioro OTP, mismo patrón de incidentes), pero IB concentra problemas en flota A320neo mientras YW los concentra geográficamente en ruta LCG-MAD.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. Short Haul - Análisis de Cabinas:**

**COMPARACIÓN ECONOMY SH vs BUSINESS SH:**

| Factor | Economy SH | Business SH | Convergencia |
|--------|------------|-------------|--------------|
| **Dirección anomalía** | +11.33 pts (POSITIVA) | -4.23 pts IB / -22.57 pts YW (NEGATIVAS) | ❌ **DIVERGEN COMPLETAMENTE** |
| **Mishandling impact** | 28.3% (+10.9pts) | 29.2% IB / 25.7% YW | ✅ **CONVERGEN** |
| **OTP15 deterioro** | 84.4% (-0.8pts) | 87.9% IB / 81.7% YW | ✅ **CONVERGEN** |
| **Incidentes NCS** | 23 (82.6% retrasos) | 23 (82.6% retrasos) | ✅ **CONVERGEN** |
| **Reactividad cliente** | Compensación por segmentos | Devastación total Business/Work | ❌ **REACTIVIDAD DIFERENCIAL EXTREMA** |

**PATRÓN DE CONSISTENCIA IB/YW:**
- **IB**: Economy sin anomalía vs Business -4.23pts
- **YW**: Economy +20.37pts vs Business -22.57pts
- **Conclusión**: Patrón divergente inconsistente entre compañías

**DIAGNÓSTICO SHORT HAUL**: **Causa operativa común con reactividad específica de cabina** - Mismos drivers operativos críticos (Mishandling 28.3%, deterioro OTP, 23 incidentes) pero Economy muestra "efecto compensación" mientras Business sufre impacto directo devastador.

---

## **B. Long Haul - Análisis de Cabinas:**

**COMPARACIÓN ECONOMY LH vs BUSINESS LH vs PREMIUM LH:**

| Factor | Economy LH | Business LH | Premium LH | Convergencia |
|--------|------------|-------------|------------|--------------|
| **Dirección anomalía** | +19.4 pts (POSITIVA) | +23.17 pts (POSITIVA) | +7.97 pts (POSITIVA) | ✅ **CONVERGEN DIRECCIONALMENTE** |
| **Mishandling impact** | 28.3% (+10.9pts) | 28.3% (+10.9pts) | 28.3% (+10.9pts) | ✅ **CONVERGEN TOTALMENTE** |
| **OTP15 deterioro** | 80.3% (-1.5pts) | 80.3% (-1.4pts) | 80.3% (-1.4pts) | ✅ **CONVERGEN TOTALMENTE** |
| **Load Factor presión** | 93.2% (+3.1pts) | 88.2% vs 92.3% | 92.4% (+2.3pts) | ✅ **CONVERGEN** |
| **Incidentes NCS** | 16 (68.7% retrasos) | 16 (68.7% retrasos) | 16 (68.7% retrasos) | ✅ **CONVERGEN TOTALMENTE** |
| **Patrón reactividad** | Segmentos polarizados | Business/Work NPS 0.0 devastado | Fleet polarización (A333 vs A350) | ⚠️ **REACTIVIDAD DIFERENCIAL MODERADA** |

**PROGRESIÓN LÓGICA DE REACTIVIDAD:**
- **Economy LH**: Mayor compensación (+19.4pts) - Segmentos Leisure resilientes
- **Business LH**: Máxima compensación (+23.17pts) - Pero colapso total en Business/Work (0.0)  
- **Premium LH**: Menor compensación (+7.97pts) - Polarización extrema por flota

**DIAGNÓSTICO LONG HAUL**: **Causa completamente común al radio** - Convergencia total en drivers operativos (Mishandling 28.3%, OTP 80.3%, mismo patrón de incidentes) con progresión lógica de reactividad: todas las cabinas muestran anomalías positivas por "efecto compensación matemática" pero con sensibilidades diferenciadas por perfil de cliente.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. Comparación Entre Radios:**

**ESTADO DE AFECTACIÓN:**
✅ **Short Haul AFECTADO**: Anomalías mixtas (Economy +11.33pts, Business negativas)  
✅ **Long Haul AFECTADO**: Anomalías positivas generalizadas (+7.97 a +23.17pts)  
✅ **AMBOS RADIOS impactados simultáneamente**

**CONVERGENCIA EN DRIVERS PRINCIPALES:**

| Driver Operativo | Short Haul | Long Haul | Convergencia |
|------------------|------------|-----------|--------------|
| **Mishandling** | 28.3% (+10.9pts) | 28.3% (+10.9pts) | ✅ **IDÉNTICO** |
| **OTP15 deterioro** | 84.4% (-0.8pts) | 80.3% (-1.4pts) | ✅ **CONVERGENTE** |
| **Load Factor presión** | 87.1% - 93.2% | 88.2% - 93.2% | ✅ **CONVERGENTE** |
| **Incidentes NCS** | 23 (82.6% retrasos) | 16 (68.7% retrasos) | ✅ **PATRÓN SIMILAR** |
| **Misconex** | Estable 0.9% | Estable 0.9% | ✅ **CONVERGENTE** |

**EVIDENCIA OPERATIVA CONSISTENTE:**
- **Mishandling crítico idéntico** (28.3%) en ambos radios
- **Deterioro puntualidad** proporcional al radio (SH -0.8pts, LH -1.4pts)
- **Patrón dominante de retrasos** en incidentes NCS
- **Sobrecarga operativa** por Load Factor elevado

---

## **B. Coherencia con Nodo Global:**

**COMPARACIÓN GLOBAL vs RADIOS:**

| Métrica | Global | Short Haul | Long Haul | Coherencia |
|---------|--------|------------|-----------|------------|
| **Anomalía NPS** | -13.5 pts (NEGATIVA) | +11.01 pts (POSITIVA) | +19.26 pts (POSITIVA) | ❌ **INCOHERENTE** |
| **Mishandling** | 28.3% (+10.9pts) | 28.3% (+10.9pts) | 28.3% (+10.9pts) | ✅ **PERFECTA** |
| **Incidentes totales** | 328 incidentes | 23 incidentes | 16 incidentes | ✅ **AGREGACIÓN LÓGICA** |
| **Impacto Business** | Business -25.2pts vs Leisure | Business devastado | Business/Work NPS 0.0 | ✅ **CONSISTENTE** |

**EXPLICACIÓN DE LA APARENTE INCOHERENCIA:**
El nodo Global muestra **-13.5 pts** mientras SH y LH muestran anomalías positivas debido a:

1. **Efecto de agregación ponderada**: El Global incluye volúmenes y segmentos no visibles en los subnodos
2. **Impacto diferencial por perfil**: Los segmentos Business/Work más críticos tienen mayor peso en Global
3. **328 incidentes totales**: Magnitud superior a la suma de SH (23) + LH (16), sugiriendo impactos adicionales

---

## **DIAGNÓSTICO GLOBAL:**

**Causa global homogénea con efectos compensatorios por radio** - Ambos radios Short Haul y Long Haul convergen completamente en los mismos drivers operativos críticos (Mishandling 28.3%, deterioro OTP, sobrecarga Load Factor, patrón dominante de retrasos), pero manifiestan diferentes efectos compensatorios matemáticos a nivel de cabina que enmascaran la severidad real del problema operativo, mientras que el nodo Global refleja el impacto agregado real de -13.5 puntos al ponderar correctamente todos los segmentos afectados.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA 1: COLAPSO CRÍTICO DEL SISTEMA DE HANDLING DE EQUIPAJES**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis**: Falla sistémica en los procesos de manejo de equipajes que generó un incremento del 62% en mishandling (28.3% vs 17.4% promedio), probablemente causada por la convergencia de alta ocupación operativa, fallos en sistemas automatizados de clasificación, y/o problemas de coordinación en conexiones internacionales.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO**: **Global** (nivel más amplio de impacto)

**OUTPUT CAUSAL DETALLADO**:
- **NPS Impact**: -13.5 puntos vs baseline (32.4 vs 18.8)
- **Mishandling**: 28.3% vs 17.4% promedio (+10.9pts, +62% incremento)
- **Incidentes validados**: 328 incidentes totales, con casos críticos como "35 equipajes en tierra procedentes de IB124/LIM"
- **Rutas más afectadas**: LIM (Lima) como epicentro cascada, MAD-MVD, LCG-MAD, MAD-XRY

**ALCANCE DE SUBSEGMENTOS AFECTADOS**:
Esta causa afecta **TODOS los subsegmentos** bajo el nodo Global:
- **Long Haul**: Economy (+19.4pts aparente pero con Business/Work devastado), Business (+23.17pts con colapso 0.0 en Business/Work), Premium (+7.97pts con A333 crítico -25.0)
- **Short Haul**: Economy (+11.33pts con Others CodeShare -60.0), Business (IB -4.23pts, YW -22.57pts)

**MÉTRICAS CLAVE**:
- **Flota más afectada**: A33ACMI (NPS -52.9), A333 (NPS -25.0 a -20.0), A332 (NPS -12.5 a 6.2)
- **Perfiles críticos**: Business/Work (NPS 0.0 múltiples segmentos), Others CodeShare (NPS -60.0 a -26.7)
- **Verbatims**: No disponibles (limitación crítica del análisis)

---

## **CAUSA 2: DETERIORO SISTEMÁTICO DE PUNTUALIDAD OPERATIVA**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis**: Efecto cascada de retrasos generado por la combinación de sobrecarga operativa (Load Factor >90% en múltiples segmentos), problemas de control de tráfico aéreo (ATC), y complicaciones en rotación de aeronaves que crearon un "efecto dominó" temporal a lo largo del día.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO**: **Global** (impacto sistémico completo)

**OUTPUT CAUSAL DETALLADO**:
- **OTP15 degradado**: 83.9% vs 84.8% promedio (-0.9pts) a nivel Global
- **Variación por radio**: SH 84.4% (-0.8pts), LH 80.3% (-1.4pts)
- **Incidentes dominantes**: 82.6% de incidentes NCS fueron retrasos (19/23 en SH, proporción similar en LH)
- **Load Factor crítico**: Múltiples segmentos >90% (LH Economy 93.2%, LH Premium 92.4%)

**ALCANCE DE SUBSEGMENTOS AFECTADOS**:
Esta causa afecta **TODOS los subsegmentos** bajo el nodo Global con impacto diferenciado:
- **Mayor sensibilidad**: Segmentos Business/Work (NPS 0.0 recurrente)
- **Menor sensibilidad**: Segmentos Leisure (mantienen NPS positivos)
- **Concentración geográfica**: Rutas específicas como LCG-MAD (NPS -33.3)

**MÉTRICAS CLAVE**:
- **Incidentes totales**: 328 incidentes con patrón dominante de retrasos
- **Casos críticos**: Problemas ATC, rotación aeronaves, carga combustible
- **Rutas identificadas**: MAD-MVD, LCG-MAD, MAD-XRY como epicentros
- **Verbatims**: No disponibles (limitación del análisis)

---

## **CAUSA 3: SOBRECARGA OPERATIVA POR ALTA OCUPACIÓN**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis**: La convergencia de Load Factor elevado (87-93% según segmento) con capacidad operativa limitada creó un "cuello de botella sistémico" que amplificó exponencialmente el impacto de cualquier disrupción menor, convirtiendo problemas rutinarios en crisis de servicio al cliente.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO**: **Global** (presión sistémica completa)

**OUTPUT CAUSAL DETALLADO**:
- **Load Factor elevado**: 88.6% vs 87.5% promedio (+1.1pts) Global
- **Picos críticos por segmento**: LH Economy 93.2% (+3.1pts), LH Premium 92.4% (+2.3pts)
- **Efecto multiplicador**: Alta ocupación + problemas operativos = impacto desproporcionado
- **Capacidad de recuperación limitada**: Sin margen para absorber disrupciones

**ALCANCE DE SUBSEGMENTOS AFECTADOS**:
Esta causa actúa como **AMPLIFICADOR** en todos los subsegmentos bajo Global:
- **Segmentos premium más vulnerables**: Menor tolerancia a sobrecarga
- **Operaciones ACMI más expuestas**: A33ACMI con NPS -52.9
- **Rutas internacionales críticas**: Mayor complejidad operativa bajo presión

**MÉTRICAS CLAVE**:
- **Correlación directa**: Load Factor >90% correlaciona con NPS más bajos
- **Impacto diferencial**: Business/Work devastados vs Leisure resilientes
- **Flota específica**: A320neo, A33ACMI como más vulnerables bajo presión
- **Verbatims**: No disponibles (limitación crítica para validar percepción de hacinamiento)

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 21 de agosto de 2025 registró una crisis operativa severa que generó un impacto NPS heterogéneo según el segmento, con el nivel Global experimentando una caída crítica de -13.5 puntos (de 32.4 a 18.9), mientras paradójicamente los subsegmentos Long Haul mostraron mejoras aparentes: Economy LH subió +19.4 puntos (de 10.5 a 29.9), Business LH aumentó +23.17 puntos (de 22.28 a 45.45) y Premium LH creció +7.97 puntos (de 22.28 a 45.45). En Short Haul, Economy registró una mejora de +11.33 puntos (de 21.18 a 32.52), mientras Business mostró deterioros diferenciados: IB cayó -4.23 puntos y YW se desplomó -22.57 puntos (de 60.07 a 37.5). Las causas principales fueron el colapso crítico del sistema de handling de equipajes con un incremento del 62% en mishandling (28.3% vs 17.4% promedio), deterioro sistemático de puntualidad operativa (OTP15 de 83.9% vs 84.8% baseline) validado por 328 incidentes totales donde dominaron los retrasos, y sobrecarga operativa por alta ocupación (Load Factor hasta 93.2% en algunos segmentos) que amplificó exponencialmente cualquier disrupción menor.

Las rutas más afectadas incluyen MAD-MVD con NPS de 30.8, LCG-MAD con NPS devastador de -33.3, MAD-XRY como epicentro de problemas (NPS 28.6), y el caso crítico de Lima (LIM) con el incidente de "35 equipajes en tierra procedentes de IB124/LIM". Los grupos de clientes más reactivos fueron consistentemente los viajeros Business/Work que experimentaron NPS de 0.0 en múltiples segmentos, contrastando dramáticamente con viajeros Leisure que mantuvieron satisfacción alta (NPS 34-54 según segmento), operaciones CodeShare "Others" con NPS devastador de -60.0, flota A33ACMI con NPS crítico de -52.9, y clientes de regiones Asia y América Norte que mostraron mayor sensibilidad a las disrupciones operativas.

**ECONOMY SH: Mejora Aparente con Crisis Operativa Subyacente**
La cabina Economy de SH experimentó una mejora aparente de +11.33 puntos, pasando de un NPS de 21.18 a 32.52 el 21 de agosto, pero el análisis revela que esta subida enmascara una crisis operativa severa con problemas críticos de mishandling (+9.1 puntos vs promedio, alcanzando 25.7%) y deterioro de puntualidad (OTP15 de 81.7% vs 82.8% promedio), validados por 23 incidentes NCS donde el 82.6% fueron retrasos. Esta aparente mejora se explica por compensación estadística donde segmentos resilientes (Leisure con NPS 42.0) compensaron matemáticamente los impactos devastadores en otros perfiles, especialmente evidentes en la ruta MAD-XRY donde todos los pasajeros fueron detractores (NPS 0.0), mientras que los perfiles más reactivos incluyen viajeros Business/Work (NPS 0.0), operaciones CodeShare "Others" (NPS -60.0) y clientes de América Norte (NPS -9.1).

**BUSINESS SH: Deterioro Diferenciado por Compañía**
El segmento Business de SH mostró deterioros diferenciados, con IB registrando una caída de -4.23 puntos y YW experimentando un desplome crítico de -22.57 puntos (de 60.07 a 37.5) el 21 de agosto. Esta evolución se explica principalmente por problemas operativos convergentes de mishandling crítico (29.2% en IB, 25.7% en YW vs promedios de 17.7% y 16.6% respectivamente) y deterioro de puntualidad, siendo especialmente visible en rutas como LCG-MAD (NPS -33.3 para YW) y concentrado en flota A320neo para IB (NPS 11.1), mientras que los perfiles más reactivos son consistentemente los viajeros Business/Work que alcanzaron NPS de 0.0 en ambas compañías, contrastando con viajeros Leisure que mantuvieron satisfacción moderada.

**ECONOMY LH: Compensación Matemática con Problemas Operativos**
La cabina Economy de LH registró una mejora aparente de +19.4 puntos, pasando de un NPS de 10.5 a 29.9 el 21 de agosto, pero esta subida resulta de una compensación matemática que enmascara problemas operativos severos incluyendo mishandling crítico de 28.3% (+10.9 puntos vs promedio), sobrecarga operativa con Load Factor de 93.2% (+3.1 puntos) y deterioro de puntualidad (OTP15 de 80.3% vs 81.8% promedio), validados por 16 incidentes NCS donde el 68.7% fueron retrasos. Esta aparente mejora se concentró especialmente en segmentos resilientes que compensaron los impactos devastadores en otros perfiles, siendo especialmente visible en rutas como MAD-MVD (NPS 30.8), mientras que los perfiles más reactivos incluyen viajeros Business/Work que experimentaron colapso total (NPS -23.1), clientes de regiones Asia (NPS -100.0) y operaciones con flota A332 (NPS 6.2).

**BUSINESS LH: Mejora Aparente con Colapso Segmentado**
La cabina Business de LH mostró una mejora aparente de +23.17 puntos, pasando de un NPS de 22.28 a 45.45 el 21 de agosto, pero esta subida enmascara un colapso total en viajeros Business/Work que alcanzaron NPS de 0.0 (5 encuestas) mientras viajeros Leisure mantuvieron satisfacción alta (NPS 53.6 con 28 encuestas). Los drivers principales fueron los mismos problemas operativos críticos de mishandling (28.3% vs 17.4% promedio) y deterioro de puntualidad (OTP15 de 80.3% vs 81.8%), impactando especialmente a clientes de España (NPS 30.8) vs América Sur (NPS 85.7) y concentrándose en flota A332 (NPS 28.6) vs A350 (NPS 77.8), mientras que los perfiles más reactivos son exclusivamente los viajeros Business/Work que sufrieron devastación completa por las disrupciones operativas.

**PREMIUM LH: Polarización Extrema por Flota**
El segmento Premium de LH experimentó una mejora moderada de +7.97 puntos, pasando de un NPS de 32.0 a 40.0 el 21 de agosto, resultado de una polarización extrema entre flotas donde A350 next alcanzó excelencia (NPS 75.0 con 8 encuestas) que compensó matemáticamente los graves problemas del A333 (NPS -25.0 con 4 encuestas). Las causas dominantes fueron los problemas operativos críticos de mishandling (28.3% vs 17.4% promedio), sobrecarga por Load Factor elevado (92.4% vs 90.1%) y deterioro de puntualidad (OTP15 de 80.3% vs 81.8%), especialmente evidentes en operaciones A333 que concentraron los problemas de equipaje correlacionados con el incidente crítico IB124/LIM, mientras que los perfiles más reactivos incluyen viajeros Business (NPS 25.0 vs Leisure 45.5) y operaciones geográficas específicas donde España mostró desempeño moderado (NPS 50.0) vs América Centro y Sur con experiencia perfecta (NPS 100.0).

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 11
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-20 to 2025-08-20:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 8 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/LH/Premium, Global/SH, Global/SH/Business, Global/SH/Business/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. Economy Short Haul:**

**NODOS IDENTIFICADOS:**
- ❌ **Economy SH/IB**: No existe nodo separado en el árbol
- ✅ **Economy SH/YW**: No existe nodo específico, pero SH/Business/YW sí está presente

**DIAGNÓSTICO**: No se puede realizar análisis comparativo Economy SH por compañías ya que **no existen nodos separados IB vs YW** para este segmento en el árbol de anomalías.

---

## **B. Business Short Haul:**

**NODOS IDENTIFICADOS:**
- ❌ **Business SH/IB**: No existe nodo separado en el árbol  
- ✅ **Business SH/YW**: Existe como Global/SH/Business/YW con análisis completo

**EVIDENCIA DEL NODO YW:**
- **Anomalía**: -35.07 puntos NPS (46.2 vs 14.93 baseline)
- **Drivers principales**: Mishandling crítico (+9.1pts), deterioro OTP15 (-1.1pts)
- **Flota específica**: ATR con NPS 33.3 vs CRJ con 53.8
- **Ruta crítica**: CMN-MAD operada con ATR

**DIAGNÓSTICO**: **Causa específica de YW en Business Short Haul** - Solo existe evidencia para YW, sugiriendo que los problemas operativos (mishandling crítico, flota ATR, ruta CMN-MAD) fueron exclusivos de las operaciones de Air Nostrum, no de Iberia mainline.

---

## **CONCLUSIÓN DIAGNÓSTICA:**

**Short Haul Business**: Los problemas del 20 de agosto fueron **específicos de Air Nostrum (YW)**, concentrados en operaciones ATR y rutas como CMN-MAD, sin evidencia de impacto similar en operaciones Iberia mainline.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. Short Haul - Análisis de Cabinas:**

### **NODOS DISPONIBLES:**
- ✅ **Global/SH**: NPS 28.86 (-7.59 pts anomalía)
- ✅ **Global/SH/Business**: NPS 39.58 (+16.82 pts anomalía positiva)
- ✅ **Global/SH/Business/YW**: NPS 46.2 (-35.07 pts anomalía)

### **PATRONES IDENTIFICADOS:**

**DRIVERS OPERATIVOS CONVERGENTES:**
- **Mishandling crítico**: 28.3% vs 17.4% (+10.9pts) - **Común a todo SH**
- **Deterioro OTP**: 84.4% vs 85.3% (-0.8pts) - **Común a todo SH**
- **Incidente específico**: IB424/BCN con 47 equipajes sin cargar - **Común a todo SH**

**REACTIVIDAD DIVERGENTE POR CABINA:**
- **SH General**: Impacto negativo moderado (-7.59pts)
- **SH/Business**: Paradoja de anomalía positiva (+16.82pts) a pesar de problemas operativos
- **SH/Business/YW**: Impacto severo (-35.07pts) concentrado en flota ATR

**DIAGNÓSTICO SH**: **Causa operativa común con reactividad específica por cabina** - Mismos problemas operativos (mishandling, puntualidad) afectaron todo Short Haul, pero Business mostró menor sensibilidad mientras que YW absorbió el impacto más severo.

---

## **B. Long Haul - Análisis de Cabinas:**

### **NODOS DISPONIBLES:**
- ✅ **Global/LH**: NPS 26.67 (+13.38 pts anomalía positiva)
- ✅ **Global/LH/Economy**: NPS 26.8 (-16.3 pts anomalía)
- ✅ **Global/LH/Business**: NPS 37.93 (-15.65 pts anomalía)
- ✅ **Global/LH/Premium**: NPS 5.88 (-26.15 pts anomalía)

### **PATRONES IDENTIFICADOS:**

**DRIVERS OPERATIVOS CONVERGENTES:**
- **Mishandling crítico**: 28.3% vs 17.4% (+10.9pts) - **Común a todo LH**
- **Load Factor elevado**: 92.4% vs 90.1% (+2.3pts) - **Común a todo LH**
- **Deterioro OTP15**: 80.3% vs 81.8% (-1.4pts) - **Común a todo LH**

**REACTIVIDAD PROGRESIVA POR CLASE:**
- **LH General**: Anomalía positiva (+13.38pts) por efecto matemático
- **Economy**: Impacto negativo moderado (-16.3pts)
- **Business**: Impacto negativo similar (-15.65pts)
- **Premium**: Impacto más severo (-26.15pts) - **Mayor sensibilidad**

**CONCENTRACIÓN EN FLOTAS ESPECÍFICAS:**
- **A321XLR**: NPS -42.9 (Economy más afectada)
- **A33ACMI/A333**: Problemas concentrados en Business/Premium

**DIAGNÓSTICO LH**: **Causa operativa común con progresión inversa de reactividad** - Mismos problemas operativos afectaron todo Long Haul, pero Premium mostró mayor sensibilidad (-26.15pts) que Economy (-16.3pts), con Business en posición intermedia (-15.65pts).

---

## **CONCLUSIÓN DIAGNÓSTICA:**

**Short Haul**: Causa operativa común (mishandling, OTP) con **reactividad específica por operador** (YW más vulnerable que IB).

**Long Haul**: Causa operativa común (mishandling, flotas específicas) con **progresión inversa de sensibilidad** (Premium > Business > Economy), donde clientes de mayor valor mostraron mayor reactividad a los problemas operativos.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. Comparación Entre Radios:**

### **ESTADO DE AMBOS RADIOS:**
- ✅ **Short Haul afectado**: NPS 28.86 (-7.59 pts anomalía negativa)
- ✅ **Long Haul afectado**: NPS 26.67 (+13.38 pts anomalía positiva paradójica)

### **CONVERGENCIA EN DRIVERS PRINCIPALES:**

**DRIVERS OPERATIVOS IDÉNTICOS:**
- **Mishandling crítico**: 28.3% vs 17.4% (+10.9pts) - **Común a ambos radios**
- **Deterioro OTP**: SH 84.4% vs LH 80.3% (ambos por debajo del baseline)
- **Incidentes NCS**: 22 incidentes SH + 10 incidentes LH = **32 incidentes totales**
- **Causa externa común**: Climatología adversa en MXP afectando ambos radios

**VALORES SHAP CONSISTENTES:**
- **Mishandling**: Factor más impactante en ambos radios (+10.9pts)
- **Load Factor**: SH 87.1% vs LH 92.4% (ambos elevados)
- **Evidencia operativa**: Incidente IB424/BCN común, problemas de flota específicos

**DIAGNÓSTICO ENTRE RADIOS**: **Causa operativa global homogénea** - Ambos radios convergieron completamente en drivers principales (mishandling crítico, deterioro OTP, incidentes masivos) con la misma causa raíz operativa.

---

## **B. Coherencia con Nodo Global:**

### **ANÁLISIS DE COHERENCIA:**

**NODO GLOBAL:**
- **NPS**: 28.16 (+9.32 pts anomalía positiva)
- **Drivers**: Mishandling 28.3% (+10.9pts), mismos factores operativos

**PATRÓN DE AGREGACIÓN:**
- **SH**: -7.59 pts (negativo)
- **LH**: +13.38 pts (positivo paradójico)
- **Global**: +9.32 pts (positivo resultante)

**EFECTO MATEMÁTICO IDENTIFICADO:**
El Global **NO refleja normalidad** sino una **compensación matemática** donde:
- Los problemas operativos fueron **idénticos y severos** en ambos radios
- La anomalía positiva en LH (+13.38) **compensó** la negativa en SH (-7.59)
- El resultado Global (+9.32) **enmascara** la severidad real de los problemas operativos

**CONCENTRACIÓN GEOGRÁFICA REVELADA:**
- **Epicentro**: 7 pasajeros africanos ruta ALC-MAD
- **Impacto desproporcionado**: Evento ultra-localizado afectó métricas globales
- **281 incidentes concentrados** en ALC-MAD validando la causa común

**DIAGNÓSTICO GLOBAL**: **El nodo Global enmascara causas operativas severas** - Los mismos problemas operativos críticos (mishandling +10.9pts, incidentes masivos) afectaron ambos radios, pero efectos matemáticos compensatorios en el agregado Global (+9.32pts) ocultan la magnitud real de la crisis operativa del 20 de agosto.

---

## **CONCLUSIÓN DIAGNÓSTICA:**

**Alcance**: **Causa operativa global homogénea con efectos compensatorios** - Crisis operativa sistémica (mishandling crítico, climatología adversa, incidentes masivos) afectó tanto Short Haul como Long Haul con drivers idénticos, pero el nodo Global presenta una anomalía positiva engañosa que enmascara la severidad real de los problemas operativos concentrados geográficamente en rutas específicas como ALC-MAD.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA 1: CRISIS DE MISHANDLING CRÍTICO**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis**: Colapso sistémico en los procesos de manejo de equipaje que alcanzó niveles críticos (+62% vs promedio), causando experiencias devastadoras generalizadas que impactaron directamente la percepción de calidad del servicio y confianza del cliente.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO**: **Global** (todos los clientes de la compañía)

**OUTPUT CAUSAL DETALLADO:**
- **Métrica crítica**: 28.3% vs 17.4% baseline (+10.9 puntos porcentuales)
- **Magnitud del deterioro**: +62% incremento vs promedio
- **NPS Global**: 28.16 (+9.32 pts anomalía paradójica)
- **Incidente específico documentado**: Vuelo IB424/BCN con 47 equipajes sin cargar

**ALCANCE CONFIRMADO**: Esta causa afecta **todos los subsegmentos** identificados:
- Global/LH (mishandling 28.3%)
- Global/LH/Economy (mishandling crítico como driver principal)
- Global/LH/Business (mishandling crítico como driver principal)  
- Global/LH/Premium (mishandling crítico como factor más impactante)
- Global/SH (mishandling 28.3%)
- Global/SH/Business (mishandling crítico documentado)
- Global/SH/Business/YW (mishandling +9.1pts vs promedio)

**RUTAS ESPECÍFICAS INVOLUCRADAS**: ALC-MAD (epicentro con 281 incidentes), BCN (vuelo IB424), CMN-MAD

**VERBATIMS**: No disponibles para el período analizado

---

## **CAUSA 2: PROBLEMAS OPERATIVOS CONCENTRADOS EN FLOTAS ESPECÍFICAS**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis**: Fallos técnicos y operativos concentrados en tipos específicos de aeronaves (A321XLR, A33ACMI, ATR) que crearon experiencias diferenciadas severas, generando dispersión extrema en la satisfacción según el tipo de flota asignada al pasajero.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO**: **Global/LH** (Long Haul completo)

**OUTPUT CAUSAL DETALLADO:**
- **A321XLR**: NPS -42.9 (n=14) - Devastadoramente afectada
- **A350 C**: NPS 0.0 (n=9) - Severamente comprometida  
- **A33ACMI**: NPS -19.2 (n=26) - Operaciones subcontratadas deficientes
- **Dispersión máxima**: 88.1 puntos entre flotas (A321XLR vs A350 estándar)
- **NPS LH**: 26.67 (+13.38 pts anomalía positiva por efecto matemático)

**ALCANCE CONFIRMADO**: Esta causa afecta **todos los subsegmentos Long Haul**:
- Global/LH/Economy (A321XLR como epicentro con NPS -42.9)
- Global/LH/Business (A33ACMI/A333 problemáticas)
- Global/LH/Premium (A350 next vs otras flotas con 12.5 pts spread)

**FLOTAS ESPECÍFICAS CRÍTICAS**:
- **A321XLR**: Problemas severos concentrados
- **A33ACMI**: Operaciones subcontratadas deficientes  
- **ATR** (Short Haul): Ruta CMN-MAD específicamente problemática

**RUTAS INVOLUCRADAS**: ALC-MAD, MAD-MIA, CCS-MAD, CMN-MAD

---

## **CAUSA 3: DETERIORO SISTÉMICO DE PUNTUALIDAD (OTP)**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis**: Cascada de retrasos y cancelaciones iniciada por factores externos (climatología adversa en MXP) que generó un efecto dominó operativo, deteriorando la experiencia del cliente a través de tiempos de espera, reprogramaciones y conexiones perdidas.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO**: **Global** (impacto sistémico)

**OUTPUT CAUSAL DETALLADO:**
- **OTP15 Global**: Deterioro generalizado vs baseline
- **Short Haul**: 84.4% vs 85.3% (-0.8 pts)
- **Long Haul**: 80.3% vs 81.8% (-1.4 pts)  
- **Incidentes NCS totales**: 32 incidentes (22 SH + 10 LH)
- **Distribución**: 64% retrasos, 27% cancelaciones
- **Causa externa**: Climatología adversa en MXP

**ALCANCE CONFIRMADO**: Esta causa afecta **todos los subsegmentos** operativos:
- Todos los nodos Global, LH y SH muestran deterioro OTP
- 20 retrasos documentados + 8 cancelaciones
- Efecto cascada en conexiones y reprogramaciones

**FACTOR EXTERNO**: Regulaciones de tráfico aéreo por climatología adversa en MXP

**RUTAS CRÍTICAS**: Operaciones con conexiones en MXP y hubs principales

---

## **CAUSA 4: SOBRECARGA OPERATIVA (LOAD FACTOR ELEVADO)**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis**: Alta ocupación de vuelos que amplificó el impacto de otros problemas operativos, reduciendo la flexibilidad para gestionar incidencias y creando mayor presión en servicios de ground handling y atención al cliente.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**SEGMENTO MÁS GRANDE AFECTADO**: **Global/LH** (mayor impacto documentado)

**OUTPUT CAUSAL DETALLADO:**
- **Load Factor LH**: 92.4% vs 90.1% baseline (+2.3 pts)
- **Impacto en NPS**: Factor secundario pero amplificador
- **Correlación**: Alta ocupación + problemas operativos = experiencia degradada
- **Economy LH**: 93.2% vs 90.1% (+3.1 pts) - Más severo
- **Business LH**: 88.2% vs 92.3% (-4.1 pts paradójico)

**ALCANCE CONFIRMADO**: Afecta principalmente **segmentos Long Haul**:
- Global/LH/Economy (93.2% ocupación crítica)
- Menor impacto en Business (ocupación paradójicamente menor)

**EFECTO AMPLIFICADOR**: La alta ocupación redujo la capacidad de reubicación y gestión de incidencias, amplificando el impacto del mishandling y retrasos.

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 20 de agosto de 2025 presentó un patrón complejo de variaciones en NPS caracterizado por una paradoja aparente: mientras el nivel Global registró una mejora de 9.32 puntos (alcanzando un NPS de 28.16), los segmentos individuales experimentaron deterioros significativos. El segmento Long Haul mostró una subida aparente de 13.38 puntos (NPS de 26.67), pero esta mejora enmascara caídas severas en sus cabinas: Economy LH cayó 16.3 puntos (NPS de 26.8), Business LH descendió 15.65 puntos (NPS de 37.93), y Premium LH sufrió la mayor caída con 26.15 puntos (NPS de 5.88). En Short Haul, el segmento general bajó 7.59 puntos (NPS de 28.86), mientras que Business SH mostró una subida paradójica de 16.82 puntos (NPS de 39.58), aunque su subsegmento YW experimentó una caída severa de 35.07 puntos (NPS de 46.2). Las causas principales se concentraron en una crisis operativa sistémica liderada por problemas críticos de mishandling (28.3% vs 17.4% promedio), deterioro generalizado de puntualidad, y fallos específicos en flotas como A321XLR (NPS -42.9) y A33ACMI (NPS -19.2), amplificados por factores externos como climatología adversa en MXP que generó 32 incidentes operativos documentados.

Las rutas más impactadas incluyeron ALC-MAD como epicentro absoluto con 281 incidentes concentrados y 7 pasajeros africanos que registraron NPS de -14.3, MAD-MIA con NPS de 25.0, CMN-MAD operada con flota ATR mostrando NPS de -33.3, y BOG-MAD con NPS de 0.0. Los grupos de clientes más reactivos fueron los pasajeros internacionales, especialmente de América del Norte (NPS -50.0 en Premium), África (NPS -14.3), y Oriente Medio (NPS -40.0), contrastando dramáticamente con clientes domésticos españoles que mantuvieron NPS positivos (+42.6). La segmentación por propósito de viaje reveló que los pasajeros Leisure absorbieron el 90% del impacto negativo, mientras que los viajeros de negocios mostraron mayor resistencia a las disrupciones operativas.

**ECONOMY SH: Estabilidad Semanal**
La cabina Economy de Short Haul mantuvo desempeño estable durante esta semana. No se detectaron cambios significativos a nivel de cabina individual, manteniendo niveles consistentes de satisfacción en este segmento.

**BUSINESS SH: Paradoja Operativa con Impacto Selectivo**
El segmento Business de Short Haul registró una subida aparente de 16.82 puntos (NPS de 39.58) que enmascara problemas operativos severos. Esta paradoja se explica principalmente por la concentración del impacto en operaciones específicas de Air Nostrum (YW), donde el mishandling crítico (+9.1 puntos vs promedio) y el deterioro de puntualidad (-1.1 puntos OTP15) afectaron especialmente la flota ATR en rutas como CMN-MAD, mientras que las operaciones mainline de Iberia mantuvieron mejor desempeño relativo.

**ECONOMY LH: Crisis Operativa Concentrada en Flotas Específicas**
La cabina Economy de Long Haul experimentó un deterioro significativo de 16.3 puntos, registrando un NPS de 26.8. La causa principal fue una crisis operativa concentrada en la flota A321XLR que alcanzó un NPS devastador de -42.9, complementada por problemas sistémicos de mishandling (+10.9 puntos) y sobrecarga operativa con Load Factor del 93.2%. Este deterioro se reflejó especialmente en rutas transatlánticas como MAD-MIA, mientras que los perfiles más reactivos incluyen pasajeros de ocio que representaron el 90% del volumen afectado.

**BUSINESS LH: Impacto Severo en Operaciones Subcontratadas**
La cabina Business de Long Haul registró una caída de 15.65 puntos (NPS de 37.93) durante el período analizado. Los drivers principales fueron el colapso del mishandling (incremento del 62% vs promedio) y problemas concentrados en flotas A33ACMI y A333, impactando especialmente las rutas con operaciones subcontratadas y entre perfiles de pasajeros Leisure que mostraron mayor sensibilidad a las disrupciones operativas.

**PREMIUM LH: Mayor Sensibilidad a Crisis Operativa**
El segmento Premium de Long Haul sufrió la caída más severa con 26.15 puntos de deterioro, alcanzando un NPS de 5.88. Las causas dominantes fueron los mismos problemas operativos sistémicos pero con mayor reactividad del segmento, especialmente evidentes en rutas como BOG-MAD y entre pasajeros de América del Norte que registraron NPS de -50.0, confirmando la mayor sensibilidad de este segmento premium a las fallas operativas.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 8
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-19 to 2025-08-19:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 9 (Global, Global/LH/Business, Global/LH/Premium, Global/SH, Global/SH/Business, Global/SH/Business/IB, Global/SH/Business/YW, Global/SH/Economy, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. ECONOMY SHORT HAUL**

### **Nodos Identificados:**
- ✅ **Economy SH/YW**: Global/SH/Economy/YW (NPS +21.3 pts, anomalía positiva)
- ❌ **Economy SH/IB**: No existe nodo separado

### **Análisis de Ausencia:**
El nodo Economy SH/IB no aparece como anomalía separada, sugiriendo que:
- Los problemas operativos del 19/08 no generaron una desviación suficiente en IB Economy para ser detectada como anomalía
- El impacto se concentró específicamente en el segmento YW o la metodología de detección no capturó la anomalía IB

---

## **B. BUSINESS SHORT HAUL**

### **Nodos Identificados:**
- ✅ **Business SH/IB**: Global/SH/Business/IB (NPS -7.63 pts, anomalía negativa)
- ✅ **Business SH/YW**: Global/SH/Business/YW (NPS +51.7 pts, anomalía positiva)

### **Análisis Comparativo:**

| **Aspecto** | **Business SH/IB** | **Business SH/YW** | **Divergencia** |
|-------------|-------------------|-------------------|-----------------|
| **Dirección Anomalía** | Negativa (-7.63 pts) | Positiva (+51.7 pts) | ⚠️ **OPUESTA** |
| **Causa Principal** | Mishandling crítico (29.2%) + Incidente IB424/BCN | Mishandling (25.7%) pero muestra pequeña | **Diferentes niveles** |
| **Muestra** | 26 encuestas | 9 encuestas | **Representatividad distinta** |
| **Segmento Afectado** | Business/Work devastado (-33.3) | 100% Leisure | **Perfiles opuestos** |
| **Flota** | A320 más afectada (-16.7) | 100% CRJ | **Flotas diferentes** |

---

## **🎯 DIAGNÓSTICOS FINALES**

### **Economy Short Haul:**
**"Causa específica de compañía YW"** - Solo YW presenta anomalía detectable, sugiriendo que los problemas operativos del 19/08 impactaron de manera diferencial entre compañías en el segmento Economy.

### **Business Short Haul:**
**"Causa específica de compañía con impactos opuestos"** - IB y YW muestran patrones completamente divergentes (negativo vs positivo), diferentes causas operativas (Mishandling severo vs muestra estadísticamente frágil), y afectación de perfiles de cliente distintos, confirmando causas específicas por compañía dentro de la misma cabina Business.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. SHORT HAUL - ANÁLISIS DE CABINAS**

### **Comparación Economy SH vs Business SH:**

| **Aspecto** | **Economy SH** | **Business SH** | **Convergencia/Divergencia** |
|-------------|----------------|-----------------|------------------------------|
| **Dirección General** | Positiva (+7.6 pts) | Negativa (-11.52 pts) | 🔴 **DIVERGENTE** |
| **Causa Operativa** | Mishandling crítico (28.3%) | Mishandling crítico (28.3%) | ✅ **CONVERGENTE** |
| **Reactividad** | Paradoja: problemas operativos → NPS positivo | Directa: problemas operativos → NPS negativo | 🔴 **DIVERGENTE** |
| **Segmentación Interna** | España resiliente (+42.1) vs América Norte afectada (-18.2) | Business/Work devastado (-33.3) vs Leisure protegido (+40.6) | 🔴 **PATRONES DISTINTOS** |

### **Análisis por Compañía:**
- **IB**: Economy (sin anomalía) vs Business (-7.63) → **Reactividad diferencial**
- **YW**: Economy (+21.3) vs Business (+51.7) → **Ambas positivas pero Business estadísticamente frágil**

### **Reactividad Diferencial Identificada:**
- **Economy SH**: Actúa como "amortiguador" - mismos problemas operativos generan paradoja positiva
- **Business SH**: Altamente reactiva - problemas operativos impactan directamente y severamente

---

## **B. LONG HAUL - ANÁLISIS DE CABINAS**

### **Comparación Economy LH vs Business LH vs Premium LH:**

| **Aspecto** | **Economy LH** | **Business LH** | **Premium LH** | **Patrón** |
|-------------|----------------|-----------------|----------------|------------|
| **Dirección Anomalía** | No detectada | Negativa (-0.058 pts) | Negativa (-20.49 pts) | 📈 **PROGRESIÓN LÓGICA** |
| **Causa Operativa** | Mishandling 28.3% | Mishandling 28.3% | Mishandling 28.3% | ✅ **CONVERGENTE** |
| **Reactividad** | Sin anomalía | Mínima | Severa | 📈 **ESCALADA POR CLASE** |
| **Flota Afectada** | - | A330 crisis total | A350/A333 problemas | ✅ **CONVERGENTE** |
| **Perfil Impactado** | - | Business/Work (NPS 0.0) | Business/Work (NPS 0.0) | ✅ **CONVERGENTE** |

### **Progresión de Reactividad Identificada:**
1. **Economy LH**: Sin anomalía detectada - máxima resistencia
2. **Business LH**: Anomalía mínima (-0.058) - resistencia moderada  
3. **Premium LH**: Anomalía severa (-20.49) - máxima sensibilidad

### **Patrón de Amortiguación:**
- **Economy LH** actúa como amortiguador total ante la crisis operativa
- **Business/Premium LH** muestran sensibilidad progresiva según clase de servicio

---

## **🎯 DIAGNÓSTICOS FINALES**

### **Short Haul:**
**"Causa común de radio con reactividad diferencial extrema por cabina"** - Ambas cabinas experimentaron la misma crisis operativa (Mishandling 28.3%), pero Economy SH actuó como amortiguador generando paradójicamente NPS positivo, mientras Business SH mostró alta reactividad con impacto negativo directo.

### **Long Haul:**
**"Causa común de radio con escalada progresiva de sensibilidad por clase"** - Las tres cabinas experimentaron la misma crisis operativa sistémica, pero mostraron una progresión lógica de reactividad: Economy LH (sin impacto) → Business LH (impacto mínimo) → Premium LH (impacto severo), confirmando que la clase de servicio determina la sensibilidad a disrupciones operativas.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. COMPARACIÓN ENTRE RADIOS**

### **Afectación por Radio:**

| **Aspecto** | **Short Haul** | **Long Haul** | **Convergencia** |
|-------------|----------------|---------------|------------------|
| **Anomalías Detectadas** | ✅ Economy (+7.6) y Business (-11.52) | ✅ Business (-0.058) y Premium (-20.49) | ✅ **AMBOS AFECTADOS** |
| **Causa Operativa Principal** | Mishandling 28.3% vs 17.4% (+10.9 pts) | Mishandling 28.3% vs 17.4% (+10.9 pts) | ✅ **CONVERGENTE** |
| **Driver Secundario** | OTP15 deterioro (-0.8 pts) | OTP15 deterioro (-1.4 pts) | ✅ **CONVERGENTE** |
| **Incidentes NCS** | 20 incidentes (13 retrasos + 6 cancelaciones) | 22 incidentes (12 retrasos + 8 cancelaciones) | ✅ **CONSISTENTE** |
| **Flota Afectada** | A350 (-100.0), 32S (-27.8), A33ACMI (-22.2) | A330 crisis total (A333: 0.0, A332: -25.0) | ✅ **CONVERGENTE AIRBUS** |

### **Evidencia Operativa Específica:**
- **Incidente Común Validado**: IB424/BCN con 47 equipajes sin cargar afecta ambos radios
- **Patrón Geográfico**: Rutas críticas en ambos radios (ATH-MAD en SH, LIM-MAD en LH)
- **Valores SHAP**: Mishandling como driver principal consistente entre radios

---

## **B. COHERENCIA CON NODO GLOBAL**

### **Análisis del Nodo Global:**

| **Métrica** | **Global** | **Patrón SH+LH** | **Coherencia** |
|-------------|------------|------------------|----------------|
| **Anomalía Detectada** | +5.62 pts (FALSA POSITIVA) | SH: mixto, LH: negativo | ❌ **INCOHERENTE** |
| **Mishandling** | 28.3% (+10.9 pts) | Consistente en ambos radios | ✅ **COHERENTE** |
| **Incidentes Totales** | 329 incidentes | SH: 20 + LH: 22 = 42 vs 329 | ❌ **DISCREPANCIA MASIVA** |
| **Rutas Críticas** | IAD-MAD (-33.3), Oriente Medio (-50.0) | ATH-MAD, LIM-MAD | ✅ **PATRÓN GEOGRÁFICO** |

### **Contradicción Fundamental Identificada:**
- **Global reporta anomalía positiva (+5.62)** mientras **evidencia operativa muestra crisis severa**
- **329 incidentes totales vs 42 reportados** en análisis por radio sugiere **subreportación sistémica**

---

## **C. MANIFESTACIÓN EN NIVEL GLOBAL**

### **Efecto de Compensación Detectado:**
1. **SH Economy** (+7.6) compensa parcialmente **LH Premium** (-20.49)
2. **Mercado doméstico español resiliente** (NPS 41.6) compensa **rutas internacionales críticas**
3. **Flotas estables** (CRJ +41.4) compensan **flotas Airbus problemáticas**

### **Anomalías Enmascaradas:**
- **Segmentos críticos** (Oriente Medio -50.0, Asia -33.3) quedan diluidos en agregación
- **Crisis específicas de flota** (A350: -100.0 en SH) no se reflejan en Global
- **Problemas de alianzas** (AA: -50.0, LATAM: -27.3) invisibles en nivel Global

---

## **🎯 DIAGNÓSTICO FINAL**

### **Alcance de las Causas:**
**"Causa global homogénea con efectos compensatorios que enmascaran la crisis real"** 

**Explicación Detallada:**
- **Ambos radios experimentaron la misma crisis operativa sistémica** (Mishandling 28.3%, deterioro OTP15, incidentes masivos de equipaje)
- **Los drivers principales convergen completamente** entre SH y LH (Mishandling, flota Airbus, rutas específicas)
- **El nodo Global muestra una falsa anomalía positiva** debido a efectos compensatorios donde segmentos resilientes (mercado doméstico español, flotas regionales, clientes Leisure) enmascaran crisis severas en segmentos específicos
- **La discrepancia de 329 vs 42 incidentes** confirma que el Global captura la magnitud real de la crisis que no se refleja completamente en el análisis por radio

**Implicación Crítica:** La crisis del 19/08/2025 fue sistémica y global, pero el algoritmo de detección falló al identificarla como mejora debido a la composición heterogénea de la base de clientes que permitió compensaciones estadísticas.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA 1: CRISIS DE MISHANDLING SISTÉMICA**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Falla operativa masiva en el sistema de manejo de equipajes que se extendió por toda la red, afectando desproporcionalmente a flotas Airbus y rutas internacionales específicas. El incremento de +10.9 puntos en Mishandling (28.3% vs 17.4%) representa una crisis operativa que cascadeó hacia múltiples aspectos de la experiencia del cliente.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **Global** (nivel más amplio)

**Output Causal Detallado:**
- **Mishandling crítico:** 28.3% vs 17.4% baseline (+10.9 pts) - El driver más significativo
- **329 incidentes operativos totales** - Volumen extraordinario para un solo día
- **Incidente específico validado:** 47 equipajes sin cargar del vuelo IB424/BCN → efecto cascada
- **Correlación directa:** Mishandling crítico ↔ 329 incidentes operativos

**Subsegmentos afectados bajo este nodo:**
- Global/SH/Economy: Paradoja operativa (problemas severos, NPS positivo por compensación)
- Global/SH/Business: Impacto directo negativo (-11.52 pts)
- Global/LH/Business: Crisis específica A330 (NPS 0.0 en Business/Work)
- Global/LH/Premium: Devastación severa (-20.49 pts)

**Métricas clave:**
- **NPS Global:** +5.62 pts (anomalía falsa)
- **Rutas críticas:** IAD-MAD (-33.3), ATH-MAD (-18.2), LIM-MAD (impacto severo)
- **Flotas más afectadas:** A350 (-100.0 en SH), A330 (crisis total en LH)
- **Verbatims:** No disponibles (sistema colapsado durante crisis)

---

## **CAUSA 2: FALLA SISTÉMICA DE FLOTA AIRBUS**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Problemas técnicos, de mantenimiento o de configuración específicos de la familia Airbus que generaron disrupciones operativas concentradas. La dispersión extrema entre flotas (125-141 puntos de diferencia) sugiere problemas sistémicos en aeronaves Airbus vs Boeing/regionales.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **Global/SH** (mayor volumen de operaciones Airbus)

**Output Causal Detallado:**
- **Dispersión extrema por flota:** 141.4 puntos entre mejor y peor performance
- **A350 colapso total:** NPS -100.0 (3 surveys) - 100% detractores
- **A330 crisis sistémica:** A333 (NPS 0.0), A332 (NPS -25.0), A33ACMI (NPS -22.2)
- **Contraste con flotas estables:** CRJ (NPS 41.4), A321 performance aceptable

**Subsegmentos afectados bajo este nodo:**
- Global/SH/Economy: A350, 32S, A33ACMI con performance crítica
- Global/SH/Business: A320 más afectada (-16.7) vs CRJ mejor (66.7)
- Global/LH/Business: Crisis exclusiva A330 vs A350 funcionamiento normal
- Global/LH/Premium: A350/A333 problemáticas vs flotas alternativas

**Métricas clave:**
- **Flotas críticas:** A350 (-100.0), A333 (0.0), A332 (-25.0), 32S (-27.8)
- **Flotas estables:** CRJ (41.4), A321 (performance superior)
- **Rutas específicas:** Correlación entre flotas Airbus y rutas internacionales problemáticas
- **Load Factor paradójico:** Mayor problemas con menor ocupación en algunos casos

---

## **CAUSA 3: DETERIORO DE PUNTUALIDAD Y EFECTO CASCADA**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Los problemas iniciales de equipaje y flota generaron un efecto dominó de retrasos que se propagó por la red, creando pérdidas de conexión masivas y reprogramaciones que amplificaron exponencialmente el impacto en la experiencia del cliente.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **Global** (impacto sistémico en toda la red)

**Output Causal Detallado:**
- **OTP15 deteriorado:** 83.9% vs 84.8% baseline (-0.9 pts)
- **110 retrasos masivos** como principal disruptor operativo
- **42 cancelaciones** con impacto severo en experiencia
- **Efecto cascada documentado:** "24 pérdidas de conexión, 3 cancelaciones, 1 reprogramación, 12 cambios de equipo"

**Subsegmentos afectados bajo este nodo:**
- Todos los subsegmentos experimentaron deterioro de puntualidad
- Impacto diferencial: Premium y Business más sensibles a retrasos
- Economy mostró mayor resistencia al deterioro de puntualidad

**Métricas clave:**
- **Incidentes específicos:** IB379 MAD-SJU (+1h15min), IB2623 como epicentro (3 incidentes)
- **Load Factor crítico:** 88.6% vs 87.5% - Sobrecarga operativa
- **Rutas de conexión:** Pérdidas masivas de conexión amplificaron problemas
- **Impacto geográfico:** América Norte correlaciona con rutas de conexión críticas

---

## **CAUSA 4: IMPACTO DIFERENCIAL POR PERFIL DE CLIENTE**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** La misma crisis operativa generó reacciones completamente diferentes según el perfil del cliente, donde viajeros Business/Work mostraron extrema sensibilidad mientras viajeros Leisure y mercado doméstico español actuaron como amortiguadores, creando efectos compensatorios que enmascararon la severidad real de la crisis.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **Global/SH** (mayor diversidad de perfiles)

**Output Causal Detallado:**
- **Dispersión extrema por propósito:** Business/Work devastado vs Leisure resiliente
- **Mercado doméstico protegido:** España NPS 41.6 vs rutas internacionales críticas
- **Codeshares severamente afectados:** AA (-50.0), LATAM (-27.3) vs IB relativamente estable
- **Efecto compensación:** Segmentos resilientes enmascararon crisis en Global

**Subsegmentos afectados bajo este nodo:**
- Global/SH/Business: Business/Work (-33.3) vs Leisure (30.4) - 63.8 pts diferencia
- Global/LH/Business: Business/Work (NPS 0.0) - colapso total
- Global/LH/Premium: Business/Work (NPS 0.0) - devastación completa
- Todos los segmentos Economy: Mayor resistencia general

**Métricas clave:**
- **Segmentos críticos:** Oriente Medio (-50.0), Asia (-33.3), América Norte (impacto variable)
- **Segmentos protegidos:** España (41.6), Europa (performance superior), Leisure (resistencia)
- **Alianzas comprometidas:** AA y LATAM con performance crítica
- **Paradoja estadística:** Crisis real enmascarada por composición de muestra favorable

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 19 de agosto de 2025 se produjo una crisis operativa sistémica que generó patrones complejos y contradictorios en el NPS. A nivel global se detectó una aparente mejora de +5.62 puntos (pasando de 18.84 a 24.46), pero esta anomalía positiva enmascara una realidad operativa devastadora caracterizada por un incremento crítico del mishandling al 28.3% (+10.9 puntos vs baseline) y 329 incidentes operativos. Las anomalías reales se concentraron en segmentos específicos: el Premium LH experimentó la caída más severa con -20.49 puntos (de 32.03 a 11.54), el Business SH registró un deterioro de -11.52 puntos (de 22.77 a 11.25), mientras que paradójicamente el Economy SH mostró una mejora de +7.6 puntos (de 21.2 a 28.8) y el Business SH/YW una subida aparente de +51.7 puntos (de 14.93 a 66.67). La causa principal fue una falla sistémica de manejo de equipajes documentada en el incidente IB424/BCN donde 47 equipajes no fueron cargados, complementada por problemas específicos de la flota Airbus (A350 con NPS -100.0, A330 en crisis total) y un efecto cascada de 110 retrasos que generaron 24 pérdidas de conexión masivas.

Las rutas más críticas incluyeron IAD-MAD con NPS -33.3, ATH-MAD con -18.2, y LIM-MAD severamente impactada, mientras que los grupos más reactivos fueron los viajeros Business/Work que experimentaron un colapso total (NPS 0.0) en múltiples segmentos premium, contrastando con la resistencia mostrada por viajeros Leisure y el mercado doméstico español que mantuvo NPS de 41.6 puntos.

**ECONOMY SH: Crisis Operativa Enmascarada**
La cabina Economy de SH experimentó una mejora aparente durante el 19 de agosto de 2025, registrando un NPS de 28.8 puntos con una subida de +7.6 puntos respecto al baseline de 21.2. Esta paradoja se explica por un efecto de compensación estadística donde el mercado doméstico español (NPS 41.6) y las flotas regionales estables (CRJ con 41.4) enmascararon los severos problemas operativos que afectaron desproporcionalmente a segmentos específicos como los codeshares de American Airlines (NPS -50.0) y las rutas internacionales. La causa subyacente fue el mismo incremento crítico de mishandling (28.3%) y deterioro de puntualidad que impactó toda la red, pero la composición favorable de la muestra generó la ilusión de mejora mientras segmentos minoritarios sufrían devastación.

**BUSINESS SH: Devastación Diferencial por Compañía**
El segmento Business de SH mostró patrones divergentes entre compañías, con IB registrando un deterioro de -7.63 puntos (de 30.70 a 23.08) mientras YW aparentemente mejoró +51.7 puntos (de 14.93 a 66.67). La caída en IB se explica principalmente por el impacto directo del mishandling crítico (29.2%) y los incidentes específicos como el IB424/BCN, siendo especialmente devastador para viajeros Business/Work que alcanzaron NPS -33.3, contrastando con la resistencia de viajeros Leisure (NPS 30.4). La aparente mejora en YW se basa en una muestra estadísticamente frágil de solo 9 encuestas, concentradas en el mercado español y flota CRJ, lo que cuestiona la validez de esta anomalía positiva.

**ECONOMY LH: Estabilidad Operativa**
La cabina Economy de LH mantuvo desempeño estable durante el 19 de agosto de 2025, sin detectarse anomalías significativas a pesar de la crisis operativa sistémica. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción y actuando como el segmento más resiliente ante las disrupciones operativas que devastaron otras cabinas.

**BUSINESS LH: Crisis Específica de Flota A330**
La cabina Business de LH registró un deterioro mínimo de -0.058 puntos (de 22.28 a 22.22) durante el 19 de agosto, pero esta cifra enmascara una crisis operativa específica de la flota Airbus A330. Los drivers principales fueron la falla sistémica de las aeronaves A330 (A333 con NPS 0.0, A332 con -25.0, A33ACMI con -50.0) contrastando con el funcionamiento normal de la flota A350 (NPS 75.0), impactando devastadoramente a los viajeros Business/Work que experimentaron un colapso total (NPS 0.0) mientras los clientes Leisure mantuvieron cierta resistencia (NPS 25.8).

**PREMIUM LH: Devastación Completa del Segmento de Élite**
El segmento Premium de LH experimentó la caída más severa con -20.49 puntos de deterioro (de 32.03 a 11.54) durante el 19 de agosto. Las causas dominantes fueron la crisis multifacética que combinó mishandling crítico (28.3%), sobrecarga operativa (Load Factor 92.4%) y el colapso específico de la ruta LIM-MAD, especialmente evidentes en el impacto devastador sobre clientes americanos de negocios (América Norte NPS -33.3, América Sur NPS 0.0) y la falla específica de las flotas A350 en este segmento, mientras que los problemas sistémicos de captura de feedback (ausencia total de verbatims) sugieren que la crisis fue tan severa que colapsó los sistemas de recolección de experiencia del cliente.

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

**Nodos analizados:** 6 (Global, Global/LH/Business, Global/LH/Premium, Global/SH/Business, Global/SH/Business/IB, Global/SH/Economy/IB)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. Economy Short Haul:**

**Nodos disponibles:** Solo existe **Global/SH/Economy/IB**
**Ausencia:** No existe nodo Economy SH/YW

**Razón de ausencia:** El análisis indica que YW no operó vuelos Economy Short Haul el 18 de agosto de 2025, o su volumen de respuestas NPS fue insuficiente para generar un nodo separado.

## **B. Business Short Haul:**

**Nodos disponibles:** Solo existe **Global/SH/Business/IB**  
**Ausencia:** No existe nodo Business SH/YW

**Razón de ausencia:** Similar a Economy, YW no tuvo operación significativa en Business Short Haul el 18 de agosto, o el volumen de encuestas NPS fue insuficiente para análisis separado.

---

## **DIAGNÓSTICO FINAL:**

**Economy Short Haul:** **Causa específica de Iberia** - No hay comparación posible con YW por ausencia operativa, pero los problemas identificados (FCO-MAD, mishandling 29.2%, flota A33ACMI) son específicos de la operación IB.

**Business Short Haul:** **Causa específica de Iberia** - Los problemas operativos (condiciones meteorológicas FNC→FAO, 32 incidentes NCS, mishandling 29.2%) afectaron exclusivamente la operación IB sin contraparte YW para comparación.

**Conclusión:** Las anomalías del 18 de agosto en Short Haul son **específicas de la operación Iberia**, sin evidencia de problemas compartidos a nivel de cabina general debido a la ausencia operativa de YW en ambos segmentos.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. Short Haul - Análisis de Cabinas:**

### **Comparación Economy SH vs Business SH (ambos IB):**

**PATRONES CONVERGENTES IDENTIFICADOS:**
- **Causa operativa común**: Ambas cabinas afectadas por la misma crisis meteorológica (FNC→FAO, 32 incidentes NCS)
- **Driver principal compartido**: Mishandling crítico (29.2% vs 17.7% baseline) impacta ambas cabinas
- **Concentración geográfica**: Problemas focalizados en rutas específicas (FCO-MAD en Economy, LHR-MAD en Business)

**DIVERGENCIAS CRÍTICAS EN REACTIVIDAD:**
- **Economy SH/IB**: NPS cayó -2.22 pts (impacto moderado)
- **Business SH/IB**: NPS cayó -9.3 pts (impacto severo - **4x mayor**)
- **Paradoja de clase**: Los clientes Business, que deberían estar más protegidos, resultaron **más vulnerables** a las disrupciones

---

## **B. Long Haul - Análisis de Cabinas:**

### **Comparación Economy LH vs Business LH vs Premium LH:**

**PATRONES COMPLETAMENTE DIVERGENTES:**
- **Economy LH**: No aparece en el análisis (sin anomalías detectadas)
- **Business LH**: NPS cayó -5.04 pts por problemas específicos (codeshare AA, flota A333)
- **Premium LH**: NPS subió +31.6 pts por efecto selectividad premium

**PROGRESIÓN INVERSA DE REACTIVIDAD:**
- **Premium LH**: Completamente aislado de problemas operativos (+31.6 pts)
- **Business LH**: Impacto moderado y focalizado (-5.04 pts)
- **Economy LH**: Sin impacto detectable (ausente del análisis)

---

## **DIAGNÓSTICO FINAL:**

**Short Haul:** **Causa común de radio con reactividad diferencial crítica** - Ambas cabinas comparten la misma causa operativa (crisis meteorológica), pero Business SH mostró **4x mayor vulnerabilidad** que Economy SH, contradiciendo la lógica esperada de protección por clase de servicio.

**Long Haul:** **Causas completamente específicas de cabina** - Cada cabina tuvo drivers únicos y completamente independientes: Premium beneficiado por selectividad, Business afectado por codeshare/flota específica, y Economy sin impacto. No hay patrón común de radio.

**Conclusión:** Las anomalías muestran **comportamientos opuestos por radio**: SH con causa común pero reactividad paradójica, LH con causas completamente segmentadas por cabina.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. Comparación Entre Radios:**

### **Afectación por Radio:**
**Ambos radios afectados** pero con **patrones causales completamente divergentes**

### **Análisis de Convergencia/Divergencia:**

**SHORT HAUL:**
- **Driver principal**: Crisis meteorológica (FNC→FAO) + Mishandling crítico (29.2%)
- **Patrón**: Causa operativa común, reactividad diferencial por cabina
- **Impacto**: Economy -2.22 pts, Business -9.3 pts

**LONG HAUL:**
- **Drivers principales**: Codeshare AA (-100.0), Flota A333 (-71.4), Selectividad Premium (+31.6)
- **Patrón**: Causas específicas y segmentadas por cabina
- **Impacto**: Business -5.04 pts, Premium +31.6 pts

**CONCLUSIÓN DE CONVERGENCIA:** **Divergencia total** - No hay drivers compartidos ni evidencia operativa común entre radios.

---

## **B. Coherencia con Nodo Global:**

### **Contradicción Crítica Identificada:**
- **Nodo Global**: NPS +2.68 pts (ANOMALÍA POSITIVA)
- **Evidencia operativa Global**: Deterioro severo (Mishandling +10.9 pts, OTP -0.9 pts, 297 incidentes)
- **Radios individuales**: Múltiples anomalías negativas significativas

### **Análisis de Coherencia:**
**INCOHERENCIA FUNDAMENTAL** - El Global muestra mejora mientras:
- SH/Business: -9.3 pts (impacto severo)
- LH/Business: -5.04 pts (impacto moderado)  
- SH/Economy: -2.22 pts (impacto leve)
- Solo LH/Premium: +31.6 pts (compensatorio)

### **Hipótesis de la Contradicción:**
El **efecto compensatorio de LH/Premium** (+31.6 pts con muestra selectiva de 10 respuestas) podría estar **artificialmente inflando** el resultado Global, enmascarando los problemas operativos reales documentados.

---

## **DIAGNÓSTICO FINAL:**

**Causas mixtas con contradicción sistémica** - Los radios Short Haul y Long Haul experimentaron **causas completamente independientes y no relacionadas** (meteorológica vs codeshare/flota), pero el nodo Global presenta una **contradicción fundamental** al mostrar mejora (+2.68 pts) mientras la evidencia operativa documenta deterioro severo generalizado. Esta incoherencia sugiere un **posible fallo en la medición o agregación de datos NPS** que requiere investigación urgente antes de considerar válida la anomalía Global positiva.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA 1: CRISIS METEOROLÓGICA OPERATIVA**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Condiciones meteorológicas adversas (vientos fuertes en FNC) generaron una cascada operativa masiva que desencadenó fallas sistémicas en manejo de equipajes, cancelaciones y cambios de aeronave, impactando desproporcionadamente a clientes según su perfil de tolerancia a disrupciones.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **Global/SH/Business** (29 respuestas)

**Output causal detallado:**
- **NPS impacto:** +9.99 pts (paradójicamente positivo durante crisis)
- **Incidentes operativos:** 32 totales (22 cancelaciones, 5 retrasos, 5 cambios aeronave)
- **Trigger inicial:** Desvío FNC→FAO por vientos fuertes → regreso forzado MAD
- **Métricas operativas críticas:**
  - Mishandling: 28.3% vs 17.4% (+10.9 pts deterioro)
  - OTP15: 84.4% vs 85.3% (-0.8 pts)
  - Load Factor: 68.8% vs 73.6% (-4.8 pts por cancelaciones)

**Subsegmentos afectados:** Global/SH/Business/IB (NPS -9.3 pts), Global/SH/Economy/IB (NPS -2.22 pts)

**Rutas involucradas:** FCO-MAD (epicentro con NPS 0.0), LHR-MAD

**Impacto diferencial identificado:**
- CodeShare American Airlines: NPS -66.7 (crisis catastrófica)
- CodeShare Iberia: NPS 38.0 (gestión más efectiva)
- Business/Work: NPS 71.4 (alta resiliencia)
- Leisure: NPS 20.5 (más vulnerable)

---

## **CAUSA 2: FALLAS ESPECÍFICAS DE CODESHARE Y FLOTA**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Problemas operativos concentrados en acuerdos de codeshare con American Airlines y aeronaves específicas (A333) generaron experiencias catastróficas localizadas, mientras el resto de la operación mantuvo estándares normales o superiores.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento más grande afectado:** **Global/LH/Business** (29 respuestas)

**Output causal detallado:**
- **NPS impacto:** -5.04 pts (17.24 vs 22.28 baseline)
- **Dispersión crítica:** 142.9 pts entre regiones (problema muy localizado)
- **Fallas específicas identificadas:**
  - American Airlines CodeShare: NPS -100.0 (n=3) - Falla total
  - Flota Airbus A333: NPS -71.4 (n=7) - Problemas técnicos/confort
  - América del Norte: NPS -100.0 (n=3) - Impacto devastador

**Subsegmentos afectados:** Todos los subsegmentos bajo Global/LH/Business

**Métricas operativas correlacionadas:**
- Mishandling: 28.3% vs 17.4% (+10.9 pts)
- OTP15: 80.3% vs 81.8% (-1.4 pts)  
- Incidentes NCS: 33 total (16 cancelaciones, 7 retrasos, 7 aircraft changes)

**Contraste positivo identificado:**
- A350 next: NPS +66.7 (flota funcionando bien)
- España: NPS +42.9 (mercado resiliente)
- Rutas directas EZE-MAD: NPS +100.0

---

## **CAUSA 3: EFECTO SELECTIVIDAD PREMIUM**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** La muestra ultra-selectiva de clientes premium (solo 10 respuestas) combinada con estándares operativos superiores de CodeShare Iberia y protección efectiva ante disrupciones masivas generó una anomalía positiva artificial no representativa de la operación general.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento afectado:** **Global/LH/Premium** (10 respuestas)

**Output causal detallado:**
- **NPS impacto:** +31.6 pts (63.6 vs 32.0 baseline) - Anomalía positiva significativa
- **Perfil ultra-específico:**
  - 100% clientes Leisure (ocio)
  - 100% vuelos CodeShare Iberia
  - Concentrado en América Centro
- **Diferenciación operativa:**
  - CodeShare IB: NPS 80.0 pts (excepcional)
  - A350 next: NPS 60.0 vs A350 estándar 50.0
  - Ausencia total de incidentes NCS en este segmento

**Subsegmentos afectados:** Único segmento (sin subsegmentación)

**Contexto operativo:** Mientras el día presentó 33 incidentes totales y deterioro generalizado, este segmento permaneció completamente aislado de las disrupciones, creando el "efecto burbuja premium" que explica la anomalía positiva.

---

## **CAUSA 4: CONTRADICCIÓN SISTÉMICA DE DATOS**

### **A. NATURALEZA DE LA CAUSA:**
**Hipótesis:** Fallo sistémico en la medición, procesamiento o agregación de datos NPS que genera una contradicción fundamental entre la mejora reportada a nivel Global y el deterioro operativo documentado en todas las métricas clave.

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE:**

**Segmento afectado:** **Global** (nivel más amplio)

**Output causal detallado:**
- **Contradicción fundamental:**
  - NPS Global: +2.68 pts (MEJORA reportada)
  - Evidencia operativa: Deterioro severo generalizado
- **Métricas operativas que contradicen:**
  - Mishandling: 28.3% vs 17.4% (+62% deterioro)
  - Load Factor: 88.6% vs 87.5% (+1.1 pts sobrecarga)
  - OTP: 83.9% vs 84.8% (-0.9 pts deterioro)
  - Incidentes NCS: 297 total documentados

**Subsegmentos afectados:** Potencialmente todos los segmentos bajo Global

**Limitaciones críticas identificadas:**
- Ausencia de verbatims (posible pérdida de datos)
- Inconsistencias en datos NCS por rutas (0 vs 297 total)
- Desfase temporal potencial entre incidentes y respuestas NPS

**Recomendación crítica:** Investigación urgente de la metodología de cálculo NPS antes de considerar válida esta anomalía.

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 18 de agosto de 2025 presentó un patrón complejo de variaciones en NPS caracterizado por una contradicción fundamental a nivel global y comportamientos divergentes por radio. A nivel agregado, el NPS global mostró una mejora aparente de +2.68 puntos (21.52 vs 18.84), sin embargo, esta evolución positiva contradice completamente la evidencia operativa que documenta un deterioro severo generalizado con 297 incidentes, mishandling del 28.3% (+10.9 puntos vs promedio) y caída en puntualidad. Esta contradicción sugiere un posible fallo sistémico en la medición NPS que requiere investigación urgente. En Short Haul, una crisis meteorológica originada por vientos fuertes en FNC que forzó desvíos a FAO y regresos a MAD desencadenó una cascada operativa de 32 incidentes que impactó diferenciadamente: Economy SH/IB experimentó un deterioro moderado de -2.22 puntos (21.15 vs 23.37), mientras Business SH/IB sufrió una caída más severa de -9.3 puntos (40.0 vs 30.7), paradójicamente mostrando mayor vulnerabilidad que Economy. En Long Haul, el patrón fue completamente segmentado: Business LH cayó -5.04 puntos (17.24 vs 22.28) por fallas específicas en codeshare con American Airlines (NPS -100.0) y problemas con flota A333 (NPS -71.4), mientras Premium LH experimentó una mejora excepcional de +31.6 puntos (63.6 vs 32.0) debido a un efecto de selectividad premium con solo 10 respuestas de clientes ultra-específicos protegidos de las disrupciones.

Las rutas más críticas incluyeron FCO-MAD como epicentro de la crisis con NPS 0.0 (100% detractores), mientras que en Long Haul las rutas hacia América del Norte registraron impactos devastadores (NPS -100.0). Los grupos de clientes más reactivos fueron los pasajeros de codeshare con American Airlines (NPS -66.7), residentes de América del Norte (NPS -100.0 en múltiples segmentos), y usuarios de flota A333 (NPS -71.4), contrastando con la alta resiliencia mostrada por clientes Business/Work (NPS 71.4) y la protección efectiva de clientes premium en vuelos CodeShare Iberia (NPS 80.0).

**ECONOMY SH: Crisis Meteorológica con Impacto Moderado**
La cabina Economy de SH experimentó un deterioro moderado durante el 18 de agosto de 2025, registrando un NPS de 21.15 con una caída de -2.22 puntos respecto al baseline de 23.37. La causa principal fue la crisis meteorológica que generó desvíos FNC→FAO y una cascada operativa de cancelaciones masivas (22 de 32 incidentes), complementada por un deterioro crítico en mishandling que alcanzó 29.2% (+11.5 puntos vs promedio). Este deterioro se concentró especialmente en la ruta FCO-MAD que registró NPS 0.0 con 25 pasajeros completamente detractores, mientras que los perfiles más reactivos incluyeron residentes de América del Norte (NPS 0.0) y usuarios de flota A33ACMI (NPS -37.9).

**BUSINESS SH: Vulnerabilidad Paradójica ante Crisis Operativa**
El segmento Business de SH mostró una vulnerabilidad paradójicamente mayor que Economy, registrando un NPS de 40.0 el 18 de agosto con una caída significativa de -9.3 puntos vs el baseline de 30.7. Esta evolución se explica principalmente por la misma crisis meteorológica que afectó a Economy pero con impacto amplificado, siendo especialmente visible en rutas como LHR-MAD y entre perfiles leisure (NPS 29.6) que mostraron mayor sensibilidad a disrupciones que los clientes Business/Work (NPS 75.0), revelando una segmentación crítica dentro de la propia cabina Business.

**ECONOMY LH: Desempeño Estable**
La cabina Economy de LH mantuvo desempeño estable durante el 18 de agosto de 2025, sin detectarse anomalías significativas que requirieran análisis específico. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción mientras otras cabinas experimentaban variaciones importantes.

**BUSINESS LH: Fallas Específicas de Codeshare y Flota**
La cabina Business de LH experimentó un deterioro focalizado durante el 18 de agosto, registrando un NPS de 17.24 con una caída de -5.04 puntos respecto al período anterior de 22.28. Los drivers principales fueron fallas catastróficas en codeshare con American Airlines (NPS -100.0) y problemas específicos con flota A333 (NPS -71.4), impactando especialmente las rutas hacia América del Norte y perfiles de pasajeros norteamericanos, mientras que el resto de la operación con CodeShare Iberia y flota A350 next mantuvo performance superior.

**PREMIUM LH: Efecto Selectividad con Mejora Excepcional**
El segmento Premium de LH experimentó una mejora excepcional durante el 18 de agosto, registrando un NPS de 63.6 con +31.6 puntos de mejora vs el baseline de 32.0. Las causas dominantes fueron un efecto de selectividad premium con muestra ultra-específica de solo 10 clientes leisure en vuelos CodeShare Iberia, especialmente evidentes en rutas de América Centro y entre perfiles protegidos de las disrupciones operativas que afectaron otros segmentos, creando una "burbuja premium" con estándares operativos superiores.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 6
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-17 to 2025-08-17:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 10 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/SH, Global/SH/Business, Global/SH/Business/YW, Global/SH/Economy, Global/SH/Economy/IB, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 **DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)**

## **A. ECONOMY SHORT HAUL**

**NODOS DISPONIBLES:**
✅ **Economy SH/IB** - Presente con análisis completo  
✅ **Economy SH/YW** - Presente con análisis completo

**COMPARACIÓN DE PATRONES:**

| **Aspecto** | **IB** | **YW** | **Convergencia** |
|-------------|--------|--------|------------------|
| **Driver Principal** | Mishandling +11.5pts (29.2% vs 17.7%) | Mishandling +9.1pts (25.7% vs 16.6%) | ✅ **IDÉNTICO** |
| **Magnitud NPS** | -13.1 puntos (10.3 vs 23.4) | -20.9 puntos (-3.1 vs 17.8) | ⚠️ Diferente intensidad |
| **Epicentro Operativo** | Hub Madrid (99 pérdidas conexión) | Hub Madrid (99 pérdidas conexión) | ✅ **IDÉNTICO** |
| **Incidentes NCS** | 47 incidentes totales | 47 incidentes totales | ✅ **IDÉNTICO** |
| **Rutas Críticas** | MAD-VCE (-7.1) | MAD-XRY (-50.0) | ⚠️ Diferentes rutas afectadas |

**DIAGNÓSTICO ECONOMY SH:** **Causa común de cabina** - Ambas compañías convergen en el driver principal (crisis de Mishandling centrada en Madrid) y evidencia operativa idéntica, con diferencias solo en intensidad y rutas específicas afectadas.

---

## **B. BUSINESS SHORT HAUL**

**NODOS DISPONIBLES:**
✅ **Business SH** - Presente (análisis general)  
✅ **Business SH/YW** - Presente con análisis específico  
❌ **Business SH/IB** - **NO DISPONIBLE**

**ANÁLISIS DEL NODO DISPONIBLE:**
- **Business SH/YW:** Anomalía -32.17 puntos con Mishandling +9.1pts como driver principal
- **Business SH general:** Anomalía -11.5 puntos con mismo patrón operativo (Madrid epicentro)

**RAZÓN DE AUSENCIA Business SH/IB:** Probablemente insuficiente volumen de respuestas NPS en el segmento Business/IB para generar análisis estadísticamente significativo el 17 de agosto de 2025.

**DIAGNÓSTICO BUSINESS SH:** **Causa común de cabina** - El único nodo específico disponible (YW) muestra el mismo driver principal (Mishandling crítico centrado en Madrid) que el análisis general de Business SH, indicando patrón operativo común independiente de la compañía.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ **DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)**

## **A. SHORT HAUL - ANÁLISIS DE CABINAS**

**NODOS DISPONIBLES:**
✅ **Economy SH** - Anomalía -15.5 puntos  
✅ **Business SH** - Anomalía -11.5 puntos

**COMPARACIÓN DE PATRONES:**

| **Aspecto** | **Economy SH** | **Business SH** | **Convergencia** |
|-------------|----------------|-----------------|------------------|
| **Driver Principal** | Mishandling +10.9pts (28.3% vs 17.4%) | Mishandling +10.9pts (28.3% vs 17.4%) | ✅ **IDÉNTICO** |
| **Epicentro Operativo** | Madrid Hub (99 pérdidas conexión) | Madrid Hub (99 pérdidas conexión) | ✅ **IDÉNTICO** |
| **Incidentes NCS** | 47 incidentes totales | 47 incidentes totales | ✅ **IDÉNTICO** |
| **Factores Secundarios** | OTP15 deterioro, Load Factor alto | OTP15 deterioro, Load Factor bajo | ⚠️ Load Factor diverge |
| **Reactividad NPS** | -15.5 puntos (mayor impacto) | -11.5 puntos (menor impacto) | ⚠️ **DIFERENCIAL** |

**ANÁLISIS DE REACTIVIDAD:**
- **Economy SH:** Mayor vulnerabilidad (-15.5pts) ante crisis operativa
- **Business SH:** Menor reactividad (-11.5pts) pero mismo driver causal
- **Patrón consistente IB/YW:** Ambas compañías muestran mayor impacto en Economy vs Business

**DIAGNÓSTICO SHORT HAUL:** **Causa común de radio con reactividad diferencial por cabina** - Misma causa operativa (crisis Mishandling en Madrid) afecta ambas cabinas, pero Economy muestra mayor sensibilidad al deterioro del servicio que Business.

---

## **B. LONG HAUL - ANÁLISIS DE CABINAS**

**NODOS DISPONIBLES:**
✅ **Economy LH** - Anomalía -4.4 puntos  
✅ **Business LH** - Anomalía -0.54 puntos  
❌ **Premium LH** - **NO DISPONIBLE**

**COMPARACIÓN DE PATRONES:**

| **Aspecto** | **Economy LH** | **Business LH** | **Convergencia** |
|-------------|----------------|-----------------|------------------|
| **Driver Principal** | Mishandling +10.9pts (28.3% vs 17.4%) | Mishandling +10.9pts (28.3% vs 17.4%) | ✅ **IDÉNTICO** |
| **Epicentro Operativo** | Madrid Hub (99 pérdidas conexión) | Madrid Hub (99 pérdidas conexión) | ✅ **IDÉNTICO** |
| **Incidentes NCS** | 51 incidentes totales | 51 incidentes totales | ✅ **IDÉNTICO** |
| **Load Factor** | 93.2% (sobrecarga crítica) | 88.2% (menor presión) | ⚠️ Diferente presión operativa |
| **Reactividad NPS** | -4.4 puntos (impacto significativo) | -0.54 puntos (impacto mínimo) | ⚠️ **ALTAMENTE DIFERENCIAL** |

**PROGRESIÓN DE REACTIVIDAD:**
- **Economy LH:** Alta sensibilidad (-4.4pts) a crisis operativa
- **Business LH:** Muy baja reactividad (-0.54pts) - "amortiguador" ante problemas
- **Ratio de impacto:** Economy 8x más reactiva que Business ante misma causa

**RAZÓN AUSENCIA Premium LH:** Probablemente volumen insuficiente de respuestas NPS en Premium el 17 de agosto de 2025.

**DIAGNÓSTICO LONG HAUL:** **Causa común de radio con reactividad altamente diferencial por cabina** - Idéntica causa operativa (crisis Mishandling en Madrid) genera impacto masivamente desproporcionado: Economy altamente vulnerable vs Business actuando como "amortiguador" con mínima reactividad.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 **DIAGNÓSTICO A NIVEL RADIO Y GLOBAL**

## **A. COMPARACIÓN ENTRE RADIOS**

**RADIOS AFECTADOS:**
✅ **Short Haul** - Anomalía severa identificada  
✅ **Long Haul** - Anomalía moderada identificada

**ANÁLISIS COMPARATIVO:**

| **Aspecto** | **Short Haul** | **Long Haul** | **Convergencia** |
|-------------|----------------|---------------|------------------|
| **Driver Principal** | Mishandling +10.9pts (28.3% vs 17.4%) | Mishandling +10.9pts (28.3% vs 17.4%) | ✅ **IDÉNTICO** |
| **Epicentro Operativo** | Madrid Hub (99 pérdidas conexión) | Madrid Hub (99 pérdidas conexión) | ✅ **IDÉNTICO** |
| **Incidentes NCS** | 47 incidentes | 51 incidentes | ✅ **CONSISTENTE** |
| **Factores Secundarios** | OTP15 deterioro, Load Factor variable | OTP15 deterioro, Load Factor alto | ✅ **CONVERGENTE** |
| **Magnitud Impacto** | -15.5pts Economy, -11.5pts Business | -4.4pts Economy, -0.54pts Business | ⚠️ **SH MÁS SEVERO** |

**PATRÓN IDENTIFICADO:**
- **Causa operativa idéntica:** Crisis Mishandling centrada en Madrid afecta ambos radios
- **Intensidad diferencial:** Short Haul sufre impacto 3-4x mayor que Long Haul
- **Evidencia convergente:** Mismos incidentes NCS y deterioro operativo

---

## **B. COHERENCIA CON NODO GLOBAL**

**ANÁLISIS DE AGREGACIÓN:**

| **Métrica** | **Global** | **Agregación SH+LH** | **Coherencia** |
|-------------|------------|---------------------|----------------|
| **Anomalía NPS** | -11.39 puntos (7.45 vs 18.84) | SH dominante + LH moderado | ✅ **COHERENTE** |
| **Driver Principal** | Mishandling +10.9pts (28.3% vs 17.4%) | Idéntico en ambos radios | ✅ **PERFECTA** |
| **Epicentro** | Madrid Hub crisis | Madrid Hub en ambos | ✅ **CONFIRMADA** |
| **Incidentes NCS** | 587 incidentes totales | 47+51 = 98 documentados | ✅ **CONSISTENTE** |
| **Ruta Crítica** | MAD-XRY (NPS -63.6) | Confirma epicentro Madrid | ✅ **VALIDADA** |

**EFECTO DE AGREGACIÓN:**
- **No hay cancelación:** Ambos radios contribuyen negativamente al Global
- **Amplificación coherente:** Global (-11.39) refleja combinación ponderada de SH (más severo) + LH (moderado)
- **Evidencia unificada:** Todos los nodos convergen en la misma narrativa operativa

---

## **🎯 DIAGNÓSTICO FINAL**

**ALCANCE DE LAS CAUSAS:** **Causa global homogénea con intensidad diferencial por radio** - La crisis operativa del 17 de agosto (Mishandling crítico centrado en Madrid) afectó simultáneamente Short Haul y Long Haul con idénticos drivers causales y evidencia operativa, pero Short Haul experimentó 3-4x mayor impacto debido a su mayor vulnerabilidad a disrupciones de conexiones en hub, manifestándose coherentemente en el nodo Global como una anomalía severa (-11.39 puntos) que refleja la combinación ponderada de ambos radios sin efectos compensatorios.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 **ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS**

## **CAUSA PRINCIPAL: CRISIS DE MISHANDLING DE EQUIPAJES**

### **A. NATURALEZA DE LA CAUSA**

**HIPÓTESIS CAUSAL:** El 17 de agosto de 2025 experimentó una cascada operativa iniciada por disrupciones masivas en el hub de Madrid (41 cambios de equipo + condiciones meteorológicas adversas) que generó 99 pérdidas de conexión, desencadenando un colapso sistémico en el manejo de equipajes. La naturaleza hub-and-spoke de la operación amplificó exponencialmente el impacto: cada conexión perdida generó múltiples casos de equipajes desconectados, creando un efecto dominó que saturó los sistemas de handling y elevó la tasa de mishandling de 17.4% (promedio) a 28.3% (+62% de incremento).

---

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE**

**SEGMENTO MÁS GRANDE AFECTADO:** **Global** (1,036 surveys totales)

**OUTPUT CAUSAL DETALLADO:**
- **Driver Principal:** Mishandling disparado a 28.3% vs 17.4% baseline (+10.9 puntos)
- **Magnitud NPS:** Caída crítica de -11.39 puntos (7.45 vs 18.84 baseline)
- **Epicentro Operativo:** Hub Madrid con 99 pérdidas de conexión masivas
- **Incidentes Validadores:** 587 incidentes NCS totales, incluyendo 30 específicos de equipaje

**ALCANCE COMPLETO:** Esta causa afecta a **TODOS los subsegmentos** bajo el nodo Global:
- ✅ Global/LH (Long Haul): -3.25 puntos NPS
- ✅ Global/LH/Economy: -4.4 puntos NPS  
- ✅ Global/LH/Business: -0.54 puntos NPS
- ✅ Global/SH (Short Haul): -14.96 puntos NPS
- ✅ Global/SH/Economy: -15.5 puntos NPS
- ✅ Global/SH/Business: -11.5 puntos NPS
- ✅ Global/SH/Economy/IB: -13.1 puntos NPS
- ✅ Global/SH/Economy/YW: -20.9 puntos NPS
- ✅ Global/SH/Business/YW: -32.17 puntos NPS

**MÉTRICAS CLAVE CONSOLIDADAS:**

| **Indicador** | **Valor Crítico** | **Impacto** |
|---------------|-------------------|-------------|
| **Mishandling Rate** | 28.3% vs 17.4% (+10.9pts) | **CRÍTICO** |
| **Pérdidas Conexión MAD** | 99 casos documentados | **MASIVO** |
| **Cambios de Equipo** | 41 cambios reportados | **DISRUPTIVO** |
| **OTP15** | 83.9% vs 84.8% (-0.9pts) | **DETERIORADO** |
| **Load Factor** | 88.6% vs 87.5% (+1.1pts) | **SOBRECARGA** |
| **Incidentes NCS** | 587 totales (30 equipaje específicos) | **VALIDADO** |

**RUTAS CRÍTICAS INVOLUCRADAS:**
- **MAD-XRY (Madrid-Jerez):** NPS catastrófico -63.6 (11 respuestas)
- **LYS-MAD:** NPS -66.7 (3 respuestas)
- **MAD-SCQ:** NPS -50.0 (4 respuestas)
- **BOG-MAD:** NPS 3.8 (26 respuestas) - Extraordinariamente bajo
- **MAD-VCE:** NPS -7.1

**SEGMENTOS MÁS DEVASTADOS:**
- **ORIENTE MEDIO:** NPS -100.0 (6 surveys) - Impacto total
- **Codeshare VY (Vueling):** NPS -64.3 (14 surveys) - Colapso operativo
- **Flota A321XLR:** NPS -20.0 - Equipos específicos afectados
- **Europa:** NPS -21.4 vs +25.5 América Centro
- **Business Travelers:** Más sensibles que Leisure a disrupciones

**VERBATIMS REPRESENTATIVOS:** 
⚠️ **LIMITACIÓN CRÍTICA:** No hay verbatims disponibles para el período analizado, lo que representa una pérdida significativa de la dimensión emocional y percepción específica del cliente durante la crisis.

---

### **CONCLUSIÓN CAUSAL**

La **Crisis de Mishandling del 17 de agosto de 2025** representa una anomalía operativa excepcional donde factores meteorológicos y técnicos convergieron para crear una "tormenta perfecta" centrada en Madrid. El efecto cascada generado por 99 pérdidas de conexión saturó completamente los sistemas de handling, elevando el mishandling un 62% sobre el promedio y causando la caída de NPS más significativa del período analizado (-11.39 puntos globales). 

**El impacto fue geográficamente concentrado pero demográficamente diferencial:** mientras los clientes domésticos españoles mostraron mayor resistencia, los viajeros internacionales (especialmente de Oriente Medio y conexiones europeas) experimentaron un colapso total de la experiencia de servicio, validando la hipótesis de que las disrupciones de hub afectan desproporcionalmente a los segmentos de mayor valor y complejidad operativa.

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 17 de agosto de 2025 registró una caída crítica del NPS global de 11.39 puntos, pasando de 18.84 a 7.45, causada por una crisis operativa sistémica centrada en el hub de Madrid. Los segmentos más devastados fueron Short Haul Economy con una caída de 15.5 puntos (de 21.18 a 5.68) y Short Haul Business con un deterioro de 11.5 puntos (de 22.28 a 10.78), mientras que Long Haul mostró mayor resistencia con Economy cayendo 4.4 puntos (de 10.46 a 6.06) y Business apenas 0.54 puntos (de 22.28 a 21.74). La causa principal identificada fue un incremento crítico del mishandling de equipajes que se disparó de 17.4% a 28.3% (+10.9 puntos), desencadenado por 99 pérdidas de conexión masivas en Madrid, 41 cambios de equipo y deterioro generalizado de la puntualidad (OTP15 cayó a 83.9% vs 84.8% promedio). Esta crisis operativa se validó con 587 incidentes NCS documentados, incluyendo 166 retrasos, 38 cancelaciones y 30 problemas específicos de equipaje.

Las rutas más severamente impactadas fueron MAD-XRY con un NPS catastrófico de -63.6 puntos, LYS-MAD con -66.7 puntos y MAD-SCQ con -50.0 puntos, todas confirmando Madrid como epicentro de la crisis. Los grupos de clientes más reactivos incluyeron viajeros de Oriente Medio (NPS -100.0), pasajeros de codeshare Vueling (NPS -64.3), clientes europeos (NPS -21.4 vs +25.5 en América Centro) y usuarios de flota A321XLR (NPS -20.0), mientras que los clientes españoles domésticos mostraron mayor resistencia con NPS +16.1, evidenciando que las disrupciones de hub afectan desproporcionalmente a segmentos internacionales y de conexión.

**ECONOMY SH: Crisis Operativa Severa**
La cabina Economy de Short Haul experimentó el mayor deterioro del día, registrando un NPS de 5.68 el 17 de agosto con una caída de 15.5 puntos respecto al baseline de 21.18. La causa principal fue la crisis de mishandling que se disparó a 28.3% (+10.9 puntos vs promedio), amplificada por la sobrecarga operativa con Load Factor de 93.2% y el colapso del hub Madrid que generó 99 pérdidas de conexión masivas. Esta crisis se reflejó especialmente en rutas como MAD-XRY (NPS -50.0) y se concentró en segmentos vulnerables como clientes de Oriente Medio (NPS -100.0), flota A321XLR (NPS -20.0) y codeshares AA (NPS -18.8), mientras que los perfiles más reactivos incluyen residentes europeos y viajeros corporativos que sufrieron el impacto más severo de las disrupciones de conexiones.

**BUSINESS SH: Impacto Moderado con Misma Causa**
El segmento Business de Short Haul mostró mayor resistencia pero no escapó a la crisis, registrando un NPS de 10.78 el 17 de agosto con una caída de 11.5 puntos vs el baseline de 22.28. Esta evolución se explica principalmente por el mismo driver de mishandling crítico (28.3%) y las disrupciones masivas en Madrid, siendo especialmente visible en la ruta MAD-SCQ (NPS -50.0) y entre perfiles de viajeros corporativos que, aunque menos reactivos que Economy, experimentaron un deterioro significativo debido a su mayor sensibilidad a pérdidas de conexiones y retrasos operativos.

**ECONOMY LH: Resistencia Relativa con Impacto Focalizado**
La cabina Economy de Long Haul mostró mayor resistencia a la crisis, registrando un NPS de 6.06 el 17 de agosto con una caída de 4.4 puntos respecto al baseline de 10.46. La causa principal fue el mismo mishandling crítico (28.3%) y las disrupciones de Madrid, pero con menor intensidad debido a la menor dependencia de conexiones de hub. Esta deterioro se reflejó especialmente en rutas como BOG-MAD (NPS 3.8) y se concentró en segmentos específicos como viajeros corporativos europeos y usuarios de flota A321XLR, mientras que los perfiles más reactivos incluyen business travelers y residentes europeos que mantuvieron mayor sensibilidad a las disrupciones operativas.

**BUSINESS LH: Máxima Resistencia Operativa**
La cabina Business de Long Haul demostró la mayor resistencia a la crisis operativa, registrando un NPS de 21.74 el 17 de agosto con una caída mínima de 0.54 puntos vs el baseline de 22.28. Los drivers principales fueron los mismos factores operativos (mishandling y disrupciones Madrid), pero esta cabina actuó como "amortiguador" ante los problemas, impactando mínimamente las rutas y perfiles, confirmando que los clientes Business de largo radio mantienen mayor tolerancia a disrupciones operativas gracias a servicios diferenciados y expectativas distintas.

**PREMIUM LH: Estabilidad Semanal**
El segmento Premium de Long Haul mantuvo desempeño estable durante esta semana. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción sin anomalías reportadas en el análisis del árbol de NPS.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 10
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-16 to 2025-08-16:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 8 (Global, Global/LH/Premium, Global/SH, Global/SH/Business, Global/SH/Business/IB, Global/SH/Business/YW, Global/SH/Economy, Global/SH/Economy/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 PASO 1: DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. ECONOMY SHORT HAUL**

### **Nodos Identificados:**
✅ **Economy SH/YW existe** - Global/SH/Economy/YW (NPS: 4.35, caída -13.48 pts)
❌ **Economy SH/IB NO existe** - No hay nodo separado en el árbol

### **Razón de Ausencia Economy SH/IB:**
El nodo Economy SH/IB no aparece como anomalía separada, sugiriendo que **IB Economy mantuvo performance dentro de rangos normales** mientras que **YW Economy experimentó deterioro significativo**.

---

## **B. BUSINESS SHORT HAUL**

### **Nodos Identificados:**
✅ **Business SH/IB existe** - Global/SH/Business/IB (NPS: -6.5, caída -37.15 pts)
✅ **Business SH/YW existe** - Global/SH/Business/YW (NPS: -16.7, caída -31.6 pts)

### **Análisis Comparativo:**

| Dimensión | Business SH/IB | Business SH/YW | Convergencia |
|-----------|----------------|----------------|--------------|
| **Causa Raíz** | Huelga BOD + Mishandling | Huelga BOD + Mishandling | ✅ **IDÉNTICA** |
| **Driver Principal** | Mishandling +11.5pts | Mishandling +9.1pts | ✅ **CONVERGENTE** |
| **Incidentes NCS** | 57 incidentes totales | 57 incidentes totales | ✅ **IDÉNTICA** |
| **Rutas Afectadas** | LHR-MAD (NPS 0.0) | MAD-VGO (NPS -40.0) | 🔄 **DIFERENTES** |
| **Impacto Geográfico** | Españoles más afectados | Europeos más afectados | 🔄 **DIFERENTES** |

---

## **📋 DIAGNÓSTICOS POR CABINA:**

### **Economy Short Haul:**
**"La causa es específica de compañía YW - IB Economy no presenta anomalía mientras YW Economy sufre deterioro significativo por la misma crisis operativa."**

### **Business Short Haul:**
**"La causa es común a ambas compañías - IB y YW Business convergen en causa raíz (huelga BOD), driver principal (Mishandling) y evidencia operativa, con diferencias solo en manifestación geográfica específica."**

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ PASO 2: DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. SHORT HAUL - ANÁLISIS DE CABINAS**

### **Nodos Disponibles:**
- **Economy SH**: Global/SH/Economy/YW (NPS: 4.35, caída -13.48 pts)
- **Business SH**: Global/SH/Business/IB (NPS: -6.5, caída -37.15 pts) + Global/SH/Business/YW (NPS: -16.7, caída -31.6 pts)

### **Análisis Comparativo Short Haul:**

| Dimensión | Economy SH | Business SH | Convergencia |
|-----------|------------|-------------|--------------|
| **Causa Raíz** | Huelga BOD + Mishandling | Huelga BOD + Mishandling | ✅ **CONVERGENTE** |
| **Driver Principal** | Mishandling +9.1pts | Mishandling +11.5pts (IB) / +9.1pts (YW) | ✅ **CONVERGENTE** |
| **Magnitud Impacto** | -13.48 pts | -37.15 pts (IB) / -31.6 pts (YW) | 🔴 **DIVERGENTE** |
| **Incidentes NCS** | 57 incidentes | 57 incidentes | ✅ **CONVERGENTE** |
| **Reactividad** | Moderada | **EXTREMA** (Business/Work -100.0 NPS) | 🔴 **DIVERGENTE** |

### **Patrón de Reactividad:**
- **Economy**: Resistencia relativa (-13.48 pts)
- **Business**: **Devastación total** (-37.15 pts IB, -31.6 pts YW)
- **Diferencial**: Business muestra **2.3x mayor sensibilidad** a la misma crisis operativa

---

## **B. LONG HAUL - ANÁLISIS DE CABINAS**

### **Nodos Disponibles:**
- **Premium LH**: Global/LH/Premium (NPS: 16.7, caída -15.4 pts)

### **Limitación Crítica:**
❌ **Economy LH y Business LH NO aparecen como nodos separados** en el árbol de anomalías

### **Análisis Disponible Long Haul:**
- **Premium LH**: Misma causa raíz (Mishandling +10.9pts), misma crisis operativa (huelga BOD)
- **Reactividad**: -15.4 pts, intermedia entre Economy SH (-13.48) y Business SH (-31.6 a -37.15)
- **Patrón de flota**: Concentrado en A350 con problemas específicos (NPS -12.5)

---

## **📋 DIAGNÓSTICOS POR RADIO:**

### **Short Haul:**
**"La causa es común al radio (huelga BOD + Mishandling) pero con reactividad específica por cabina - Business SH muestra sensibilidad extrema (2.3x mayor impacto) mientras Economy SH presenta resistencia relativa a la misma crisis operativa."**

### **Long Haul:**
**"Análisis limitado por disponibilidad de datos - Solo Premium LH visible como anomalía, sugiriendo que Economy LH y Business LH mantuvieron performance dentro de rangos normales o que Premium LH fue desproporcionadamente afectado por problemas específicos de flota A350."**

### **Patrón Transversal Identificado:**
**Progresión lógica de reactividad: Economy (más resistente) < Premium < Business (más vulnerable) - Los clientes premium muestran mayor sensibilidad a disrupciones operativas.**

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 PASO 3: DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. COMPARACIÓN ENTRE RADIOS**

### **Afectación por Radio:**
✅ **Short Haul AFECTADO** - Múltiples nodos con anomalías severas
✅ **Long Haul AFECTADO** - Nodo Premium LH con anomalía significativa

### **Análisis Comparativo Entre Radios:**

| Dimensión | Short Haul | Long Haul | Convergencia |
|-----------|------------|-----------|--------------|
| **Causa Raíz** | Huelga BOD + Mishandling | Mishandling + Sobrecarga A350 | ✅ **CONVERGENTE** |
| **Driver Principal** | Mishandling +9.1/+11.5pts | Mishandling +10.9pts | ✅ **CONVERGENTE** |
| **Incidentes NCS** | 57 incidentes totales | 38 incidentes específicos | ✅ **CONVERGENTE** |
| **Magnitud Promedio** | -13.48 a -37.15 pts | -15.4 pts | ✅ **SIMILAR RANGO** |
| **Flotas Afectadas** | CRJ, A320 variants | A350, A350 next | 🔄 **ESPECÍFICAS** |
| **Manifestación** | Huelga BOD directa | Efecto cascada + sobrecarga | 🔄 **DIFERENTE** |

### **Patrón de Propagación:**
```
HUELGA BOD → CRISIS SISTÉMICA → IMPACTO DUAL
     ↓              ↓                ↓
Short Haul:    Long Haul:       Global:
Directo        Cascada          Agregado
```

---

## **B. COHERENCIA CON NODO GLOBAL**

### **Validación Agregada:**
- **Global NPS**: 14.29 (caída -4.55 pts)
- **Drivers Global**: Mishandling +10.9pts (idéntico a LH), 658 incidentes totales
- **Evidencia Operativa**: Misma causa raíz (huelga BOD) permea todos los niveles

### **Coherencia Matemática:**
| Nivel | Impacto | Peso Relativo | Contribución Global |
|-------|---------|---------------|-------------------|
| **SH Economy** | -13.48 pts | Alto volumen | Impacto moderado |
| **SH Business** | -31.6 a -37.15 pts | Bajo volumen | Impacto concentrado |
| **LH Premium** | -15.4 pts | Volumen medio | Impacto medio |
| **GLOBAL** | **-4.55 pts** | **Total** | **Agregación coherente** |

### **Análisis de Amplificación/Atenuación:**
- **Global ATENÚA** los impactos individuales por efecto de promediado
- **Segmentos no afectados** (Economy LH, Business LH sin anomalía) actúan como **amortiguadores**
- **Dispersión extrema** documentada (hasta 180 puntos entre perfiles) se normaliza en agregado

---

## **📋 DIAGNÓSTICO DE ALCANCE:**

### **Naturaleza de la Causa:**
**"La causa es GLOBAL HOMOGÉNEA con manifestaciones específicas por radio - La huelga de BOD generó una crisis sistémica que afectó tanto Short Haul (impacto directo) como Long Haul (efecto cascada), convergiendo en el mismo driver principal (Mishandling +10.9pts) y evidencia operativa consistente (658 incidentes NCS totales)."**

### **Manifestación en Nodo Global:**
**"El nodo Global refleja una agregación coherente y atenuada de los impactos por radio - La caída moderada de -4.55 pts resulta del promediado entre segmentos severamente afectados (Business SH hasta -37.15 pts) y segmentos que actuaron como amortiguadores, manteniendo la misma causa raíz operativa (huelga BOD + Mishandling crítico) en todos los niveles."**

### **Patrón Sistémico Identificado:**
**Crisis operativa externa única → Propagación sistémica diferenciada → Impacto global atenuado pero homogéneo en causa raíz**

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 PASO 4: ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA ÚNICA IDENTIFICADA: CRISIS OPERATIVA SISTÉMICA POR HUELGA DE HANDLING**

---

## **A. NATURALEZA DE LA CAUSA**

### **Hipótesis Causal:**
La **huelga de Aviapartner en el aeropuerto de Bordeaux (BOD)** el 16 de agosto de 2025 desencadenó una **crisis operativa sistémica** que se propagó a través de toda la red de Iberia mediante un efecto cascada. El evento externo generó:

1. **Cancelaciones directas** (vuelos MAD-BOD-MAD)
2. **Redistribución forzada de flota** (especialmente A350)
3. **Sobrecarga del sistema de handling** en otros aeropuertos
4. **Deterioro masivo del mishandling** (+10.9 puntos vs baseline)
5. **Impacto diferencial por sensibilidad del segmento** (Business > Premium > Economy)

La naturaleza externa e impredecible del evento explica por qué afectó simultáneamente múltiples métricas operativas y generó dispersiones extremas entre perfiles de cliente.

---

## **B. EVIDENCIA CONSOLIDADA Y ALCANCE**

### **Segmento Más Grande Afectado: GLOBAL**
**Justificación:** El nodo Global representa el universo completo de clientes impactados y contiene la evidencia más comprehensiva de la crisis sistémica.

### **Output Causal Detallado - Nodo Global:**

#### **📊 Impacto Cuantificado:**
- **NPS**: 14.29 (caída de -4.55 puntos vs baseline 18.84)
- **Surveys**: Muestra robusta estadísticamente significativa
- **Magnitud**: Crisis operativa documentada y verificable

#### **🎯 Drivers Operativos Críticos:**
| Métrica | Día Anomalía | Promedio 7d | Desviación | Clasificación |
|---------|--------------|-------------|------------|---------------|
| **Mishandling** | 28.3% | 17.4% | **+10.9pts** | 🔴 **CRÍTICO** |
| **Load Factor** | 88.6% | 87.5% | +1.1pts | 🟡 Moderado |
| **OTP15** | 83.9% | 84.8% | -0.9pts | 🟡 Moderado |
| **Misconex** | 0.9% | 0.9% | Sin cambio | ⚪ Neutro |

#### **🚨 Incidentes Operativos (NCS):**
- **658 incidentes totales** - Volumen excepcional
- **Distribución específica:**
  - 200 retrasos (30% del total)
  - 94 cancelaciones
  - 105 pérdidas de conexión en Madrid (hub principal)
  - 26 cambios de equipo
  - 18 problemas específicos de equipaje

#### **✈️ Flotas y Rutas Críticas:**
- **Flotas problemáticas:** A33ACMI (NPS -26.0), A350 C (NPS -13.3)
- **Ruta más afectada:** LIS-MAD (NPS -44.4, n=9)
- **Epicentro operativo:** Madrid como hub principal con mayor concentración de disrupciones

#### **👥 Impacto Diferencial por Perfil:**
- **Business**: NPS 4.3 - Más severamente afectado
- **Leisure**: NPS 14.9 - Impacto moderado  
- **Gap crítico**: 10.6 puntos - Clientes premium sufrieron desproporcionadamente
- **Regiones:** ASIA más afectada (NPS -30.0), AFRICA menos afectada (NPS 85.7)
- **CodeShare problemático:** BA y QR (ambos NPS -33.3) vs IB propia (NPS 17.4)

### **🌐 Alcance de Afectación:**
**Esta causa afecta TODOS los subsegmentos bajo el nodo Global, incluyendo:**
- ✅ Global/SH/Economy/YW (caída -13.48 pts)
- ✅ Global/SH/Business/IB (caída -37.15 pts) 
- ✅ Global/SH/Business/YW (caída -31.6 pts)
- ✅ Global/LH/Premium (caída -15.4 pts)

### **📋 Métricas Clave Consolidadas:**
- **Causa raíz confirmada:** Huelga Aviapartner BOD
- **Driver principal:** Mishandling +10.9pts (factor más impactante)
- **Evidencia operativa:** 658 incidentes NCS + vuelos específicos cancelados
- **Propagación:** Efecto cascada desde BOD → Madrid hub → Red completa
- **Gestión de crisis:** Comunicación proactiva IB Conecta implementada

### **⚠️ Limitaciones Identificadas:**
- **Sin verbatims disponibles:** Falta perspectiva cualitativa del cliente para este período
- **Cobertura de rutas:** Datos granulares limitados en algunas herramientas
- **Impacto en análisis:** Sin insights específicos sobre percepción emocional, pero evidencia operativa es robusta y convergente

---

## **🎯 SÍNTESIS CAUSAL FINAL**

**La huelga de handling Aviapartner en BOD el 16/08/2025 generó una crisis operativa sistémica que se propagó por toda la red de Iberia, manifestándose principalmente a través del deterioro crítico del mishandling (+10.9pts) y afectando diferencialmente a todos los segmentos según su sensibilidad operativa, con impacto más severo en clientes Business y rutas premium.**

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 16 de agosto de 2025 registró una caída generalizada del NPS a nivel global, pasando de 18.84 a 14.29 puntos (-4.55 puntos), causada por una huelga del proveedor de handling Aviapartner en el aeropuerto de Bordeaux que desencadenó una crisis operativa sistémica. Esta disrupción externa afectó de manera diferencial a múltiples segmentos: el segmento Global/SH experimentó una caída de -8.02 puntos (de 21.27 a 13.26), mientras que Global/LH/Premium registró una reducción de -15.4 puntos (de 32.0 a 16.7). La causa principal se materializó a través del deterioro crítico del mishandling, que aumentó 10.9 puntos porcentuales hasta alcanzar 28.3% versus el promedio de 17.4%, generando 658 incidentes operativos totales que incluyeron 200 retrasos, 94 cancelaciones y 105 pérdidas de conexión concentradas en el hub de Madrid.

Las rutas más impactadas incluyeron LIS-MAD con un NPS de -44.4 puntos y LHR-MAD que registró 0.0 puntos de NPS, evidenciando la concentración del impacto en conexiones internacionales hacia Madrid. Los clientes Business mostraron la mayor reactividad a la crisis operativa, especialmente los viajeros por motivos de trabajo que alcanzaron un NPS de -100.0 puntos, mientras que los pasajeros de CodeShare con LATAM y British Airways experimentaron NPS de -80.0 y -33.3 puntos respectivamente, contrastando con la operación propia de Iberia que mantuvo un NPS de 17.4 puntos.

**ECONOMY SH: Impacto Moderado por Crisis Operativa Externa**
La cabina Economy de Short Haul experimentó un deterioro significativo el 16 de agosto de 2025, con el segmento YW registrando un NPS de 4.35 puntos (caída de -13.48 puntos respecto al baseline de 17.83). La causa principal fue la huelga de handling en Bordeaux que elevó el mishandling en 9.1 puntos porcentuales hasta 25.7%, complementada por el deterioro de la puntualidad (OTP15 bajó 1.1 puntos) y la sobrecarga operativa evidenciada en 57 incidentes totales. Esta caída se reflejó especialmente en rutas como MAD-PNA con un NPS de -27.3 puntos, mientras que los perfiles más reactivos incluyeron clientes europeos (NPS -40.0) y pasajeros de CodeShare con LATAM (NPS -100.0) y American Airlines (NPS -60.0).

**BUSINESS SH: Crisis Devastadora en Segmento Premium**
El segmento Business de Short Haul sufrió el impacto más severo, con caídas dramáticas en ambas compañías: IB registró un NPS de -6.5 puntos (deterioro de -37.15 puntos) y YW alcanzó -16.7 puntos (caída de -31.6 puntos). Esta evolución se explica principalmente por el mismo deterioro del mishandling que afectó críticamenete a los clientes premium, siendo especialmente visible en rutas como LHR-MAD (NPS 0.0) para IB y MAD-VGO (NPS -40.0) para YW, y entre perfiles de viajeros de negocios que mostraron una sensibilidad extrema con NPS de -100.0 puntos, evidenciando cero tolerancia a las disrupciones operativas.

**ECONOMY LH: Desempeño Estable**
La cabina Economy de Long Haul mantuvo desempeño estable durante el 16 de agosto de 2025, sin registrar anomalías significativas que requirieran análisis específico. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción a pesar de la crisis operativa que afectó otros segmentos.

**BUSINESS LH: Desempeño Estable**
La cabina Business de Long Haul mantuvo desempeño estable el 16 de agosto de 2025, sin mostrar variaciones significativas respecto al período anterior. No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción y actuando como segmento amortiguador ante la crisis operativa sistémica.

**PREMIUM LH: Impacto Específico por Problemas de Flota**
El segmento Premium de Long Haul experimentó un deterioro de -15.4 puntos el 16 de agosto, pasando de un NPS baseline de 32.0 a 16.7 puntos. Las causas dominantes fueron el mismo incremento crítico del mishandling (+10.9 puntos porcentuales) y la sobrecarga operativa específica de la flota A350, especialmente evidentes en el caso específico de 35 equipajes no cargados en la ruta GUA/SAL, y entre perfiles de clientes que volaron en A350 estándar (NPS -12.5) versus A350 next que preservó mejor la experiencia (NPS 75.0).

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 8
- **Pasos de análisis:** 5
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
🚨 Anomalías detectadas: daily_analysis

📅 2025-08-15 to 2025-08-15:
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** 6 (Global, Global/LH, Global/LH/Business, Global/LH/Economy, Global/SH/Business/IB, Global/SH/Business/YW)

---

## 📊 DIAGNÓSTICO A NIVEL DE EMPRESA

# 🏢 DIAGNÓSTICO A NIVEL COMPAÑÍA (IB/YW)

## **A. ECONOMY SHORT HAUL**

**❌ NODOS NO DISPONIBLES**
- **Economy SH/IB**: No existe en el árbol de datos
- **Economy SH/YW**: No existe en el árbol de datos

**Razón de ausencia**: Los datos proporcionados solo incluyen nodos de Long Haul Economy (Global/LH/Economy) sin separación por compañías, ya que en Long Haul no aplica la distinción IB/YW.

---

## **B. BUSINESS SHORT HAUL**

**✅ AMBOS NODOS DISPONIBLES**

### **Business SH/IB (Global/SH/Business/IB)**
- **NPS**: +53.57 (+22.87 pts anomalía positiva)
- **Driver principal**: Mishandling crítico (29.2% vs 17.7% baseline, +11.5pts)
- **Patrón**: Paradoja operativa - deterioro severo sin impacto negativo
- **Concentración**: Ruta MAD-MXP, 4 pasajeros afectados
- **Evidencia**: Resiliencia del sistema, impacto localizado compensado

### **Business SH/YW (Global/SH/Business/YW)**
- **NPS**: 0.0 (-14.9 pts anomalía negativa)
- **Driver principal**: Mishandling crítico (25.7% vs 16.6% baseline, +55% incremento)
- **Patrón**: Deterioro operativo localizado severo
- **Concentración**: Ruta FRA-MAD exclusivamente
- **Evidencia**: Impacto desproporcionado en clientes españoles

---

## **🎯 DIAGNÓSTICO FINAL**

### **Economy Short Haul**: 
**NO EVALUABLE** - Datos no disponibles para ambas compañías.

### **Business Short Haul**: 
**CAUSA ESPECÍFICA DE COMPAÑÍA** - IB y YW divergen significativamente en drivers, rutas afectadas (MAD-MXP vs FRA-MAD), magnitud del impacto (positivo vs negativo) y patrones de respuesta del cliente, indicando problemas operativos diferenciados por compañía específica.

---

## 💺 DIAGNÓSTICO A NIVEL DE CABINA

# ✈️ DIAGNÓSTICO A NIVEL DE CABINA (Economy/Business/Premium)

## **A. SHORT HAUL - ANÁLISIS DE CABINAS**

### **Cabinas Disponibles:**
- **Business SH/IB**: Anomalía positiva (+22.87 pts)
- **Business SH/YW**: Anomalía negativa (-14.9 pts)
- **Economy SH**: ❌ No disponible en datos

### **Análisis de Patrones:**

**🔍 DRIVERS OPERATIVOS CONVERGENTES:**
- **Ambas compañías Business SH**: Mishandling crítico como driver principal
  - IB: 29.2% vs 17.7% baseline (+11.5pts)
  - YW: 25.7% vs 16.6% baseline (+55% incremento)
- **Patrón común**: Deterioro severo en gestión de equipajes

**🔄 RESPUESTA DIVERGENTE:**
- **IB**: Impacto **positivo** (+22.87) - Resiliencia y compensación
- **YW**: Impacto **negativo** (-14.9) - Penalización severa
- **Diferencia**: 37.77 puntos entre compañías con el mismo driver

**📍 CONCENTRACIÓN GEOGRÁFICA DIFERENCIADA:**
- **IB**: Problemas en MAD-MXP (volumen limitado, 4 pasajeros)
- **YW**: Problemas en FRA-MAD (impacto en clientes españoles)

---

## **B. LONG HAUL - ANÁLISIS DE CABINAS**

### **Cabinas Disponibles:**
- **Economy LH**: Anomalía negativa (-6.98 pts)
- **Business LH**: Anomalía negativa (-5.1 pts)
- **Premium LH**: ❌ No disponible en datos

### **Análisis de Patrones:**

**🔍 DRIVERS OPERATIVOS CONVERGENTES:**
- **Ambas cabinas LH**: Mishandling crítico como driver principal
  - Economy: 28.3% vs baseline (+10.9pts)
  - Business: 28.3% vs baseline (+10.9pts)
- **Patrón idéntico**: Mismo deterioro operativo base

**📊 REACTIVIDAD DIFERENCIAL MÍNIMA:**
- **Economy LH**: -6.98 pts (más sensible)
- **Business LH**: -5.1 pts (menos sensible)
- **Diferencia**: Solo 1.88 puntos entre cabinas

**🎯 CONCENTRACIÓN GEOGRÁFICA COMÚN:**
- **Ambas cabinas**: Problemas concentrados en rutas específicas (BOG-MAD, BOS-MAD)
- **Patrón compartido**: "Deterioro silencioso" sin feedback formal

---

## **🎯 DIAGNÓSTICO FINAL**

### **Short Haul**: 
**CAUSA COMÚN DE RADIO CON REACTIVIDAD DIFERENCIAL EXTREMA** - Ambas compañías Business SH comparten el mismo driver operativo crítico (Mishandling), pero muestran respuestas completamente opuestas (+22.87 vs -14.9), indicando que la causa operativa es común al radio pero la capacidad de gestión/compensación es específica de cada compañía.

### **Long Haul**: 
**CAUSA COMÚN DE RADIO CON REACTIVIDAD HOMOGÉNEA** - Economy y Business LH convergen completamente en drivers operativos (Mishandling crítico), patrones geográficos y magnitud de impacto (diferencia mínima de 1.88 pts), indicando una causa operativa sistémica que afecta uniformemente a todas las cabinas del radio.

---

## 🌎 DIAGNÓSTICO GLOBAL POR RADIO

# 🌍 DIAGNÓSTICO A NIVEL RADIO Y GLOBAL

## **A. COMPARACIÓN ENTRE RADIOS**

### **Estado de Afectación:**
- **Short Haul**: ✅ AFECTADO - Anomalías significativas en Business (+22.87 IB, -14.9 YW)
- **Long Haul**: ✅ AFECTADO - Anomalías negativas consistentes (-6.2 general, -6.98 Economy, -5.1 Business)
- **Conclusión**: **AMBOS RADIOS AFECTADOS**

### **Convergencia de Drivers:**

**🔍 DRIVER PRINCIPAL IDÉNTICO:**
- **Short Haul**: Mishandling crítico (IB: +11.5pts, YW: +55% incremento)
- **Long Haul**: Mishandling crítico (+10.9pts consistente)
- **Convergencia**: **TOTAL** - Mismo driver operativo principal

**📊 VALORES SHAP Y EVIDENCIA:**
- **Magnitud similar**: Deterioro de Mishandling entre +10.9 a +11.5pts en ambos radios
- **Patrón operativo**: OTP deteriorado y Load Factor variable en ambos
- **Evidencia**: "Deterioro silencioso" sin feedback formal en ambos radios

### **Diferencias Clave:**
- **Short Haul**: Reactividad **extremadamente divergente** entre compañías (±37.77pts spread)
- **Long Haul**: Reactividad **homogénea** entre cabinas (1.88pts spread)

---

## **B. COHERENCIA CON NODO GLOBAL**

### **Impacto Agregado:**
- **Nodo Global**: **Anomalía POSITIVA** (+2.30 pts, NPS 21.14 vs 18.84 esperado)
- **Radios individuales**: Ambos con anomalías **mayoritariamente negativas**

### **Patrón de Compensación Identificado:**

**🎭 EFECTOS QUE SE CANCELAN:**
- **Long Haul**: Impacto negativo consistente (-6.2pts)
- **Short Haul**: Impactos opuestos que se compensan (+22.87 IB vs -14.9 YW)
- **Resultado Global**: Los impactos positivos de SH/IB compensan parcialmente los negativos de LH y SH/YW

### **Coherencia Operativa:**
- **Global confirma**: Mishandling crítico (28.3% vs 17.4% baseline, +10.9pts)
- **Global confirma**: "Deterioro silencioso" (0 incidentes NCS, 0 verbatims)
- **Global confirma**: Concentración geográfica (MAD-NCE como ruta crítica)

---

## **🎯 DIAGNÓSTICO FINAL**

**CAUSA GLOBAL HOMOGÉNEA CON EFECTOS COMPENSATORIOS** - Ambos radios convergen completamente en el mismo driver operativo crítico (Mishandling +10.9 a +11.5pts) y evidencia operativa, pero Short Haul muestra capacidad diferencial de compensación por compañía (IB resiliente, YW vulnerable) mientras Long Haul presenta reactividad homogénea. El nodo Global refleja esta dinámica compleja donde una causa operativa sistémica genera impactos heterogéneos que se compensan parcialmente, resultando en una anomalía global positiva que enmascara problemas operativos severos subyacentes.

---

## 📋 ANÁLISIS DE CAUSAS DETALLADO

# 🔍 ANÁLISIS PROFUNDO DE CAUSAS IDENTIFICADAS

## **CAUSA PRINCIPAL IDENTIFICADA: DETERIORO CRÍTICO DEL MISHANDLING**

---

### **A. NATURALEZA DE LA CAUSA**

**Hipótesis Causal**: El 15 de agosto de 2025 se produjo un **colapso sistémico en la gestión de equipajes** que afectó globalmente las operaciones, incrementando el mishandling entre 55% y 65% sobre los niveles baseline. Esta causa operativa fundamental generó un patrón de "deterioro silencioso" donde los problemas impactaron severamente la percepción del cliente sin traducirse en quejas formales masivas, debido a la concentración geográfica específica y la naturaleza implícita de las expectativas sobre equipajes.

---

### **B. EVIDENCIA CONSOLIDADA Y ALCANCE**

### **SEGMENTO MÁS GRANDE AFECTADO: GLOBAL**
*Representa la totalidad de la operación con 861 encuestas*

#### **📊 OUTPUT CAUSAL DETALLADO**

**Anomalía NPS**: +2.30 puntos (NPS 21.14 vs 18.84 esperado)
- **Paradoja aparente**: Anomalía positiva global con problemas operativos severos

**Driver Operativo Principal**:
- **Mishandling**: 28.3% vs 17.4% baseline (**+10.9 puntos**, +62% incremento)
- **Factor más crítico identificado** en el análisis

**Drivers Operativos Secundarios**:
- **Load Factor**: 88.6% vs 87.5% baseline (+1.1pts) - Sobrecarga operativa
- **OTP15**: 83.9% vs 84.8% baseline (-0.9pts) - Deterioro en puntualidad
- **Misconex**: 0.9% (estable) - No contribuyente

#### **🎯 ALCANCE DE AFECTACIÓN**

**TODOS LOS SUBSEGMENTOS CONFIRMADOS AFECTADOS**:

1. **Long Haul Global**: Mishandling 28.3% (+10.9pts)
   - Economy LH: Impacto -6.98 pts
   - Business LH: Impacto -5.1 pts

2. **Short Haul Business**:
   - IB: Mishandling 29.2% (+11.5pts) - Impacto compensado +22.87 pts
   - YW: Mishandling 25.7% (+55% incremento) - Impacto severo -14.9 pts

#### **🗺️ CONCENTRACIÓN GEOGRÁFICA**

**Rutas Críticas Identificadas**:
- **MAD-NCE**: NPS -40.0 (n=5) - Impacto devastador
- **BOG-MAD**: NPS -5.6 (Economy LH, n=18)
- **BOS-MAD**: NPS 0.0 (LH general, n=8)
- **MAD-MXP**: NPS compensado (Business SH/IB, n=4)
- **FRA-MAD**: NPS 33.3 pero impacto negativo en YW (n=3)

#### **📈 MÉTRICAS CLAVE CONSOLIDADAS**

**Volumen Total**: 861 encuestas
**Distribución Segmental**:
- Leisure: 812 encuestas (94.3%) - NPS +22.3
- Business: 49 encuestas (5.7%) - NPS +2.0

**Dispersión Máxima por Dimensión**:
- Fleet: 73.1 puntos de spread
- Residence Region: 70.0 puntos de spread
- CodeShare: 65.4 puntos de spread

#### **🔇 PATRÓN DE FEEDBACK**

**Característica "Silenciosa"**:
- **❌ Cero incidentes NCS reportados** - Sin escalamientos formales
- **❌ Cero verbatims disponibles** - Sin feedback cualitativo
- **✅ Impacto real en NPS** - Los problemas afectaron la percepción

#### **🎭 EXPLICACIÓN DE LA PARADOJA GLOBAL**

**Mecanismo de Compensación**:
1. **Problemas severos localizados** (MAD-NCE, rutas específicas)
2. **Operación mayoritaria estable** (94.3% Leisure con NPS +22.3)
3. **Capacidad diferencial de gestión** (IB resiliente vs YW vulnerable)
4. **Resultado neto positivo** que enmascara problemas operativos críticos

---

### **🎯 CONCLUSIÓN CAUSAL**

El **deterioro crítico del Mishandling** del 15 de agosto de 2025 representa una causa operativa **sistémica y global** que afectó uniformemente a todos los segmentos (+10.9 a +11.5pts de incremento), pero se manifestó de forma **heterogénea** debido a diferencias en:
- Capacidad de gestión por compañía (IB vs YW)
- Concentración geográfica específica por ruta
- Perfil y expectativas del cliente por segmento

Esta causa explica completamente el patrón paradójico observado donde problemas operativos severos coexisten con métricas NPS globales aparentemente positivas.

---

## 📋 SÍNTESIS EJECUTIVA FINAL

📈 SÍNTESIS EJECUTIVA:

El 15 de agosto de 2025 se registró un patrón complejo de evolución del NPS caracterizado por un deterioro operativo sistémico en la gestión de equipajes que afectó de manera heterogénea los diferentes segmentos. A nivel global, el NPS experimentó una mejora aparente de 2.30 puntos (de 18.84 a 21.14), enmascarando problemas operativos severos donde el mishandling se incrementó dramáticamente del 17.4% al 28.3% baseline. Esta paradoja se explica por el impacto concentrado geográficamente y la capacidad diferencial de compensación entre segmentos. El segmento Long Haul mostró deterioros consistentes, con Economy LH cayendo 6.98 puntos hasta un NPS de 3.48 y Business LH descendiendo 5.1 puntos hasta 17.1, ambos impactados por el mismo driver operativo. En contraste, Short Haul Business mostró comportamientos extremadamente divergentes: mientras IB experimentó una mejora de 22.87 puntos alcanzando un NPS de 53.57 a pesar del deterioro operativo, YW sufrió una caída crítica de 14.9 puntos hasta un NPS de 0.0, evidenciando capacidades de gestión operativa radicalmente diferentes entre compañías.

Las rutas más afectadas se concentraron en conexiones específicas con Madrid como hub central: MAD-NCE registró el impacto más severo con un NPS de -40.0, mientras que BOG-MAD (NPS -5.6), BOS-MAD (NPS 0.0) y FRA-MAD (NPS 33.3 pero con impacto negativo en clientes específicos) completaron el patrón de deterioro localizado. Los grupos de clientes más reactivos incluyeron viajeros de negocio europeos, particularmente aquellos en rutas operadas por flota A333 y A332, junto con clientes españoles en rutas internacionales que mostraron mayor sensibilidad al deterioro operativo, penalizando severamente la experiencia sin generar feedback formal a través de canales tradicionales como incidentes NCS o verbatims.

**ECONOMY SH: Desempeño Estable Semanal**
La cabina Economy de Short Haul mantuvo desempeño estable durante la semana del 15 de agosto, sin datos específicos disponibles en el análisis del árbol de anomalías. No se detectaron cambios significativos a nivel semanal, manteniendo niveles consistentes de satisfacción en este segmento.

**BUSINESS SH: Divergencia Operativa Extrema Entre Compañías**
El segmento Business de Short Haul experimentó la mayor dispersión de resultados del análisis, con IB registrando una mejora excepcional de 22.87 puntos hasta un NPS de 53.57, mientras YW sufrió un deterioro crítico de 14.9 puntos cayendo hasta un NPS de 0.0. Esta evolución contrastante se explica principalmente por el mismo driver operativo - deterioro crítico del mishandling (IB: +11.5pts, YW: +55% incremento) - pero con capacidades de compensación radicalmente diferentes. La divergencia fue especialmente visible en rutas como MAD-MXP (donde IB logró mantener experiencia positiva a pesar de problemas operativos) versus FRA-MAD (donde YW no pudo mitigar el impacto en clientes españoles), evidenciando que los perfiles más reactivos incluyen viajeros de negocio europeos con alta sensibilidad a problemas de equipajes.

**ECONOMY LH: Deterioro Silencioso Generalizado**
La cabina Economy de Long Haul experimentó un deterioro significativo de 6.98 puntos, cayendo hasta un NPS de 3.48 el 15 de agosto. La causa principal fue el colapso en la gestión de equipajes (mishandling incrementando 10.9 puntos hasta 28.3%) combinado con sobrecarga operativa (Load Factor 93.2%) y deterioro en puntualidad, creando una "tormenta perfecta" operativa sin generar feedback formal. Este deterioro se reflejó especialmente en rutas como BOG-MAD (NPS -5.6) que concentró el 100% del impacto negativo, mientras que los perfiles más reactivos incluyeron viajeros de negocio europeos (NPS -35.0) y usuarios de flota A333 (NPS -60.0), demostrando mayor vulnerabilidad a problemas operativos que otros segmentos demográficos.

**BUSINESS LH: Impacto Operativo con Experiencias Polarizadas**
La cabina Business de Long Haul registró un deterioro de 5.1 puntos hasta un NPS de 17.1 el 15 de agosto, caracterizado por experiencias extremadamente polarizadas dentro del mismo segmento premium. Los drivers principales fueron el mismo deterioro crítico del mishandling (+10.9 puntos) y problemas de puntualidad, pero con impactos diferenciales severos por geografía y flota. Esta evolución impactó especialmente las rutas con conexiones europeas donde clientes de EUROPA mostraron NPS de -37.5 versus AMERICA CENTRO con NPS 100.0, mientras que los perfiles más reactivos incluyeron pasajeros Leisure en flota A332 (NPS -37.5) contrastando dramáticamente con viajeros Business/Work que mantuvieron NPS 66.7, evidenciando que las expectativas y tolerancia varían significativamente incluso dentro del segmento premium.

**PREMIUM LH: Desempeño Estable Semanal**
El segmento Premium de Long Haul mantuvo desempeño estable durante la semana del 15 de agosto, sin datos específicos disponibles en el análisis del árbol de anomalías. No se detectaron cambios significativos a nivel semanal, manteniendo niveles consistentes de satisfacción en este segmento premium.

---

✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** 6
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