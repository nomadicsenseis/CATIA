# 🔍 CausalExplanationAgent - Documentación Completa

## 📋 **DESCRIPCIÓN GENERAL**

El `CausalExplanationAgent` es el agente responsable de **investigar anomalías en un segmento específico** mediante el análisis de múltiples fuentes de datos operativos y de experiencia del cliente. Forma parte del sistema de análisis de anomalías y proporciona explicaciones causales detalladas.

## 🆕 **ÚLTIMAS MEJORAS (Agosto 2025)**

### **✅ Arreglos Implementados:**
- **Modo Single Period completamente funcional** - Todas las herramientas ejecutándose correctamente
- **Autonomía total del agente** - Decisiones basadas en reflexiones, sin secuencias hardcodeadas
- **Chatbot fallback implementado** - Verbatims usa chatbot con fallback a PBI
- **Correlación operativa mejorada** - Mean anomaly detection con análisis de correlación
- **Robustez de collectors** - Manejo seguro de valores None y errores de sintaxis

### **🔧 Problemas Resueltos:**
- **Error replace() en PBI collector** - Solucionado manejo de None en modo single
- **Fallas en routes_tool** - Implementado _safe_clean_columns
- **Errores en customer_profile_tool** - Limpieza de columnas robusta
- **Flujo next_tool_code** - Implementado en modo single period
- **Errores de sintaxis** - Múltiples arreglos de indentación y lógica

---

## 🎯 **MODOS DE OPERACIÓN**

### **📊 COMPARATIVE MODE** 
- **Propósito:** Comparar el período actual con un período de referencia
- **Enfoque:** Cambios relativos y diferencias entre períodos
- **Herramienta inicial:** `explanatory_drivers_tool`
- **Comparación:** Dinámico según `causal_filter` (L7d, LM, vs Sel. Period)

### **📈 SINGLE MODE** 🆕 **(Completamente funcional)**
- **Propósito:** Analizar un período específico de forma aislada
- **Enfoque:** Valores absolutos con análisis de correlación
- **Herramienta inicial:** `operative_data_tool`
- **Comparación:** Solo para análisis de correlación con NPS
- **Estado:** ✅ **Todas las herramientas funcionando correctamente**
- **Autonomía:** ✅ **Agente decide flujo completo basado en reflexiones**

---

## 🛠️ **HERRAMIENTAS (TOOLS)**

### **1. 📊 OPERATIVE_DATA_TOOL**

#### **Comparative Mode:**
```python
async def _operative_data_tool(node_path, start_date, end_date, comparison_mode)
```
- **Función:** Compara métricas operativas entre períodos
- **Output:** Cambios relativos (ej: "OTP bajó 3 pts vs L7d")
- **Métricas:** Load Factor, OTP15_adjusted, Misconex, Mishandling

#### **Single Mode:** 🆕 **(Mejorado con Mean Anomaly Detection)**
```python
async def _operative_data_tool_single_period(node_path, start_date, end_date)
```
- **Función:** Valores absolutos + análisis de correlación con NPS usando mean anomaly detection
- **Output:** Valores absolutos + correlación (ej: "OTP = 85%, correlaciona con caída NPS")
- **Análisis mejorado:**
  - 📊 **Target Period**: 14 días que contienen la fecha NPS
  - 📊 **Baseline**: 173 períodos anteriores de 14 días cada uno
  - 📈 **Mean Calculation**: Media de cada métrica operativa vs baseline
  - ⚠️ **Correlaciones automáticas** con umbrales de significancia
- **Correlaciones:**
  - ✅ **OTP ↓**: Correlaciona con caída NPS (peor puntualidad)
  - ✅ **Misconex/Mishandling ↑**: Correlaciona con caída NPS (más incidentes)
  - ✅ **Load Factor ↑**: Correlaciona con caída NPS (inversamente proporcional)

---

### **2. 📋 NCS_TOOL**

#### **Comparative Mode:**
```python
async def _ncs_tool(node_path, start_date, end_date)
```
- **Función:** Compara incidentes NCS entre períodos
- **Output:** Cambios en número de incidentes por tipo

#### **Single Mode:**
```python
async def _ncs_tool_single_period(node_path, start_date, end_date)
```
- **Función:** Cuenta absoluta de incidentes del período
- **Output:** Número absoluto de incidentes por tipo

---

### **3. ✈️ ROUTES_TOOL**

#### **Comparative Mode:**
```python
async def _routes_tool(node_path, start_date, end_date, min_surveys, anomaly_type)
```
- **Función:** Compara NPS por rutas entre períodos
- **Output:** Cambios NPS por ruta vs período de referencia

#### **Single Mode:**
```python
async def _routes_tool_single_period(node_path, start_date, end_date, min_surveys, anomaly_type)
```
- **Función:** Valores NPS absolutos por ruta del período
- **Output:** NPS absoluto por ruta (ej: "MAD-BCN: NPS 65.2")

---

### **4. 💬 VERBATIMS_TOOL** 🆕 **(Con Chatbot Integration)**

#### **Comparative Mode:**
```python
async def _verbatims_tool(node_path, start_date, end_date)
```
- **Función:** Compara temas de verbatims entre períodos
- **Output:** Cambios en sentimientos y temas principales

#### **Single Mode:** 🆕 **(Chatbot con Fallback)**
```python
async def _verbatims_tool_single_period(node_path, start_date, end_date)
```
- **Función:** Análisis temático del período específico con integración chatbot
- **Implementación mejorada:**
  - 🤖 **Primero intenta chatbot** - Conexión HTTP a `https://nps.chatbot.iberia.es/api/verbatims`
  - 🔐 **Autenticación JWT** - Usa `chatbot_jwt_token` para autenticación
  - 📊 **Fallback a PBI** - Si chatbot falla, usa Power BI collector
  - ⚠️ **Manejo robusto** - Gestiona errores de red, timeouts, tokens expirados
- **Output:** Sentimientos y temas del período sin comparación

---

### **5. 👥 CUSTOMER_PROFILE_TOOL**

#### **Comparative Mode:**
```python
async def _customer_profile_tool(node_path, start_date, end_date, min_surveys, profile_dimension, mode="comparative")
```
- **Función:** Reactividad por perfil vs `causal_filter`
- **Output:** NPS_diff por segmento (ej: "Business: +2.3 vs L7d")
- **Dimensiones:** Business/Leisure, Fleet, Residence region, Codeshare

#### **Single Mode:**
```python
async def _customer_profile_tool(node_path, start_date, end_date, min_surveys, profile_dimension, mode="single")
```
- **Función:** Valores NPS absolutos por perfil del período
- **Output:** NPS absoluto por segmento (ej: "Business: NPS 67.2")

---

### **6. 🔬 EXPLANATORY_DRIVERS_TOOL** *(Solo Comparative)*
```python
async def _explanatory_drivers_tool(node_path, start_date, end_date, min_surveys)
```
- **Función:** Análisis de drivers explicativos con SHAP values
- **Output:** Factores que explican cambios en NPS
- **Nota:** Solo disponible en modo comparative

---

## 📝 **ESTRUCTURA DE PROMPTS**

### **📁 Archivo:** `causal_explanation.yaml`

```yaml
comparative_prompts:
  system_prompt: "Sistema para análisis comparativo..."
  input_template: "Analiza anomalía comparando {period} vs {comparison_filter}..."
  reflection_prompt: "Reflexiona sobre {tool_name} comparando períodos..."
  synthesis_prompt: "Sintetiza hallazgos comparativos..."

single_prompts:
  system_prompt: "Sistema para análisis de período único..."
  input_template: "Analiza período {period} con valores absolutos..."
  reflection_prompt: "Reflexiona sobre {tool_name} para período específico..."
  synthesis_prompt: "Sintetiza hallazgos del período..."

tools_prompts:
  operative_data_tool:
    comparative: "Analiza cambios en métricas operativas..."
    single: "Analiza métricas operativas con correlación NPS..."
  ncs_tool:
    comparative: "Compara incidentes NCS entre períodos..."
    single: "Analiza incidentes NCS del período..."
  # ... (resto de tools)
```

---

## 🔄 **FLUJO DE INVESTIGACIÓN** 🆕 **(Autónomo)**

### **Comparative Mode:**
```
1. explanatory_drivers_tool → Identifica drivers principales
2. operative_data_tool → Analiza métricas operativas
3. ncs_tool → Revisa incidentes
4. routes_tool → Examina rutas afectadas
5. verbatims_tool → Analiza feedback
6. customer_profile_tool → Identifica perfiles reactivos
```

### **Single Mode:** 🆕 **(Flujo autónomo, no hardcodeado)**
```
🤖 Agente decide herramienta inicial (operative_data_tool)
├── 📊 operative_data_tool → Valores absolutos + correlación mean anomaly
├── 📋 ncs_tool → Incidentes del período
├── ✈️ routes_tool → NPS por rutas
├── 💬 verbatims_tool → Temas del período (chatbot + fallback)
├── 👥 customer_profile_tool → Perfiles por NPS
└── 🧠 Reflexión → Decide si continuar o terminar

✅ El agente evalúa cada resultado y decide la siguiente herramienta
✅ No hay secuencia fija - completamente adaptativo
✅ Termina cuando identifica causa tangible + perfiles afectados
```

---

## ⚙️ **CONFIGURACIÓN**

### **Parámetros Principales:**
- **`study_mode`**: `"comparative"` | `"single"`
- **`causal_filter`**: `"vs L7d"` | `"vs LM"` | `"vs Sel. Period"` | `None`
- **`node_path`**: Segmento a analizar (ej: "Global/LH/Economy")
- **`detection_mode`**: `"mean"` | `"vslast"` | `"target"`

### **Criterios de Terminación:** 🆕 **(Decisión autónoma del agente)**
- 🤖 **El agente decide terminar** cuando considera que tiene suficiente evidencia
- 📊 **Causa tangible clara identificada** - Métricas operativas correlacionadas
- 👥 **Segmento de clientes afectado determinado** - Perfiles reactivos identificados
- 🔄 **Todas las fuentes de datos relevantes agotadas** - Herramientas ejecutadas según necesidad
- 📝 **Reflexión concluyente** - Agente indica "TERMINAR" o "END"
- ⚠️ **Máximo de iteraciones alcanzado** (5) - Límite de seguridad
- ❌ **Errores de herramientas previenen investigación adicional**

---

## 📊 **ANÁLISIS DE CORRELACIÓN (Single Mode)**

### **Métricas y Correlaciones Esperadas:**
| Métrica | Correlación con ↓NPS | Lógica |
|---------|-------------------|--------|
| **OTP15_adjusted ↓** | ✅ Positiva | Peor puntualidad |
| **Misconex ↑** | ✅ Positiva | Más conexiones perdidas |
| **Mishandling ↑** | ✅ Positiva | Más incidentes equipaje |
| **Load_Factor ↑** | ✅ Positiva | Mayor ocupación, peor experiencia |

### **Umbrales de Significancia:**
- **Load_Factor**: 3.0 pts
- **OTP15_adjusted**: 3.0 pts  
- **Misconex**: 1.0 pts
- **Mishandling**: 0.5 pts

---

## 🎯 **OBJETIVOS POR MODO**

### **Comparative Mode:**
1. **Cambios Identificados**: Qué cambió entre períodos
2. **Factores Explicativos**: Drivers con SHAP values
3. **Segmentos Afectados**: Rutas y perfiles más reactivos

### **Single Mode:**
1. **Causa Tangible**: Factores con valores absolutos
2. **Rutas Afectadas**: Rutas específicas con problemas
3. **Reactividad**: Perfiles más sensibles del período

---

## 📈 **EJEMPLOS DE OUTPUT**

### **Comparative Mode:**
```
📊 DATOS OPERATIVOS - CAMBIOS vs L7d:
• Load_Factor: 78.5% → 75.2% (-3.3pts) ⚠️
• OTP15_adjusted: 85.4% → 82.1% (-3.3pts) ⚠️

👥 CUSTOMER PROFILE - NPS IMPACT vs L7d:
• Business: NPS_diff +2.3 vs L7d (156 surveys)
• Leisure: NPS_diff -5.1 vs L7d (234 surveys)
```

### **Single Mode:**
```
📊 DATOS OPERATIVOS - ANÁLISIS CORRELACIÓN:
• Load_Factor: 78.5% (media: 75.2%, ↑3.3pts) ⚠️
✅ Load_Factor: Correlaciona con caída NPS (mayor ocupación, peor experiencia)

👥 CUSTOMER PROFILE - ABSOLUTE NPS VALUES:
• Business: NPS 67.2 (156 surveys)
• Leisure: NPS 52.8 (234 surveys)
```

---

## 🔧 **MÉTODOS PRINCIPALES**

### **Investigación:**
- `explain_anomaly()` - Punto de entrada principal
- `_investigate_anomaly_with_comparison()` - Modo comparative
- `_investigate_anomaly_single_period()` - Modo single

### **Ejecución de Tools:**
- `_execute_tool_unified()` - Dispatcher unificado
- `_execute_tool_comparative()` - Tools comparative
- `_execute_tool_single_period()` - Tools single

### **Prompts:**
- `_get_system_prompt(mode)` - Prompt de sistema por modo
- `_get_input_template(mode)` - Template inicial por modo
- `_get_tool_prompt(tool_name, mode)` - Prompts específicos de tools
- `_get_reflection_prompt(mode)` - Prompts de reflexión
- `_get_synthesis_prompt(mode)` - Prompts de síntesis

---

## 🔧 **MEJORAS TÉCNICAS IMPLEMENTADAS**

### **🛠️ Robustez de Collectors:**
- **`_safe_clean_columns()`**: Manejo seguro de valores `None` en limpieza de columnas
- **PBI Collector**: Solución de error `replace()` con `None` values en modo single
- **Chatbot Integration**: Conexión HTTP robusta con fallback a PBI
- **Error Handling**: Gestión completa de timeouts, tokens expirados, errores de red

### **🤖 Autonomía del Agente:**
- **Flujo `next_tool_code`**: Implementado en modo single period
- **Decisiones basadas en reflexiones**: No hay secuencias hardcodeadas
- **Message History**: Reflexiones correctamente almacenadas para síntesis
- **Parseo robusto**: Manejo de respuestas LLM con formato estructurado

### **📊 Análisis Mejorado:**
- **Mean Anomaly Detection**: Análisis de correlación con períodos baseline
- **Target vs Baseline**: Comparación automática con umbrales de significancia
- **Correlaciones automáticas**: Identificación de métricas que explican NPS
- **Debug logging**: Logs detallados para troubleshooting

### **🔄 Integración de Herramientas:**
- **Unified execution**: `_execute_tool_unified()` maneja todos los modos
- **Modo single period**: Todas las herramientas funcionando correctamente
- **Fallback mechanisms**: Recuperación automática de fallos
- **Data validation**: Verificación de datos antes del análisis

---

## ⚡ **PERFORMANCE**

### **Timeouts:**
- **Tool execution**: 300s por tool
- **LLM calls**: 300s por llamada
- **Reflection**: 240s para reflexiones

### **Límites:**
- **Max iterations**: 5
- **Prompt size**: 30KB para reflexiones
- **Tree data size**: Configurable via `max_tree_data_size`

---

## 🔍 **DEBUGGING**

### **Logging Levels:**
- `INFO`: Flujo principal de investigación
- `DEBUG`: Parámetros detallados de tools
- `ERROR`: Errores en tools y LLM calls

### **Variables de Seguimiento:**
- `self.collected_data`: Datos recopilados por tool
- `self.tracker`: Contexto de herramientas
- `message_history`: Historial de conversación

---

## 📚 **DEPENDENCIAS**

### **Collectors:**
- `PBIDataCollector`: Datos operativos y rutas
- `NCSDataCollector`: Incidentes NCS  
- `ChatbotVerbatimsCollector`: Verbatims de clientes

### **LLM:**
- Compatible con OpenAI GPT-4, Claude Sonnet, etc.
- Configuración via `LLMType` enum

---

*Última actualización: Enero 2025* 