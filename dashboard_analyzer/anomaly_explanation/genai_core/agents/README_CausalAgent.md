# 🔍 CausalExplanationAgent - Documentación Completa

## 📋 **DESCRIPCIÓN GENERAL**

El `CausalExplanationAgent` es el agente responsable de **investigar anomalías en un segmento específico** mediante el análisis de múltiples fuentes de datos operativos y de experiencia del cliente. Forma parte del sistema de análisis de anomalías y proporciona explicaciones causales detalladas.

---

## 🎯 **MODOS DE OPERACIÓN**

### **📊 COMPARATIVE MODE** 
- **Propósito:** Comparar el período actual con un período de referencia
- **Enfoque:** Cambios relativos y diferencias entre períodos
- **Herramienta inicial:** `explanatory_drivers_tool`
- **Comparación:** Dinámico según `causal_filter` (L7d, LM, vs Sel. Period)

### **📈 SINGLE MODE**
- **Propósito:** Analizar un período específico de forma aislada
- **Enfoque:** Valores absolutos con análisis de correlación
- **Herramienta inicial:** `operative_data_tool`
- **Comparación:** Solo para análisis de correlación con NPS

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

#### **Single Mode:**
```python
async def _operative_data_tool_single_period(node_path, start_date, end_date)
```
- **Función:** Valores absolutos + análisis de correlación con NPS
- **Output:** Valores absolutos + correlación (ej: "OTP = 85%, correlaciona con caída NPS")
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

### **4. 💬 VERBATIMS_TOOL**

#### **Comparative Mode:**
```python
async def _verbatims_tool(node_path, start_date, end_date)
```
- **Función:** Compara temas de verbatims entre períodos
- **Output:** Cambios en sentimientos y temas principales

#### **Single Mode:**
```python
async def _verbatims_tool_single_period(node_path, start_date, end_date)
```
- **Función:** Análisis temático del período específico
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

## 🔄 **FLUJO DE INVESTIGACIÓN**

### **Comparative Mode:**
```
1. explanatory_drivers_tool → Identifica drivers principales
2. operative_data_tool → Analiza métricas operativas
3. ncs_tool → Revisa incidentes
4. routes_tool → Examina rutas afectadas
5. verbatims_tool → Analiza feedback
6. customer_profile_tool → Identifica perfiles reactivos
```

### **Single Mode:**
```
1. operative_data_tool → Valores absolutos + correlación
2. ncs_tool → Incidentes del período
3. routes_tool → NPS por rutas
4. verbatims_tool → Temas del período
5. customer_profile_tool → Perfiles por NPS
```

---

## ⚙️ **CONFIGURACIÓN**

### **Parámetros Principales:**
- **`study_mode`**: `"comparative"` | `"single"`
- **`causal_filter`**: `"vs L7d"` | `"vs LM"` | `"vs Sel. Period"` | `None`
- **`node_path`**: Segmento a analizar (ej: "Global/LH/Economy")
- **`detection_mode`**: `"mean"` | `"vslast"` | `"target"`

### **Criterios de Terminación:**
- Causa tangible clara identificada
- Segmento de clientes afectado determinado
- Todas las fuentes de datos relevantes agotadas
- Máximo de iteraciones alcanzado (5)
- Errores de herramientas previenen investigación adicional

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