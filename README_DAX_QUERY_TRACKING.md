# Sistema de Captura de Consultas DAX en el Agente Causal

## Descripción

Este sistema permite capturar y registrar todas las consultas DAX exactas que ejecuta el agente causal durante la investigación de anomalías NPS. Las consultas se incluyen en el archivo JSON de conversación para auditoría y análisis posterior.

## Características

### ✅ Funcionalidades Implementadas

1. **Captura Automática**: Todas las consultas DAX se capturan automáticamente durante la ejecución
2. **Metadatos Completos**: Cada consulta incluye parámetros, timestamps y contexto
3. **Integración con JSON**: Las consultas se exportan junto con la conversación
4. **Herramientas Cubiertas**: 
   - `operative_data_tool` - Consultas de datos operativos
   - `routes_tool` - Consultas de rutas y NPS
   - `customer_profile_tool` - Consultas de perfiles de cliente

### 📊 Estructura de Datos

Cada consulta DAX capturada incluye:

```json
{
  "tool_name": "operative_data_tool",
  "query": "DEFINE\n    VAR __DS0FilterTable = ...",
  "parameters": {
    "node_path": "Global",
    "target_date": "2025-06-16",
    "comparison_days": 14,
    "use_flexible": true,
    "cabins": ["Business", "Economy", "Premium EC"],
    "companies": ["IB", "YW"],
    "hauls": ["SH", "LH"]
  },
  "timestamp": "08:44:15",
  "iteration": 1
}
```

## Implementación Técnica

### 🔧 Modificaciones Realizadas

1. **CleanConversationTracker**: Agregado campo `dax_queries` para almacenar consultas
2. **Método `add_dax_query()`**: Registra consultas con metadatos completos
3. **Wrappers de Herramientas**: Interceptan consultas antes de ejecutarlas
4. **Exportación JSON**: Incluye consultas en el archivo de conversación

### 🛠️ Wrappers Implementados

- `_collect_operative_data_with_query_tracking()`: Captura consultas de datos operativos
- `_collect_routes_with_query_tracking()`: Captura consultas de rutas
- `_collect_customer_profile_with_query_tracking()`: Captura consultas de perfiles

## Uso

### Ejecución Normal

El sistema funciona automáticamente. No requiere cambios en el código de llamada:

```python
agent = CausalExplanationAgent()
result = await agent.investigate_anomaly(
    node_path="Global",
    start_date="2025-06-16",
    end_date="2025-06-16",
    anomaly_type="positive",
    anomaly_magnitude=10.07
)
```

### Acceso a Consultas

```python
# Obtener consultas capturadas
dax_queries = agent.tracker.dax_queries

# Cada consulta contiene:
for query in dax_queries:
    print(f"Herramienta: {query['tool_name']}")
    print(f"Consulta: {query['query']}")
    print(f"Parámetros: {query['parameters']}")
```

### Archivo JSON Exportado

El archivo JSON incluye una nueva sección `dax_queries`:

```json
{
  "metadata": { ... },
  "conversation_log": [ ... ],
  "clean_explanations": [ ... ],
  "dax_queries": [
    {
      "tool_name": "operative_data_tool",
      "query": "DEFINE\n...",
      "parameters": { ... },
      "timestamp": "08:44:15",
      "iteration": 1
    }
  ]
}
```

## Pruebas

### Script de Prueba

Ejecutar el script de prueba para verificar el funcionamiento:

```bash
python test_dax_query_tracking.py
```

### Verificación Manual

1. Ejecutar una investigación de anomalía
2. Verificar que se genera el archivo JSON
3. Comprobar que contiene la sección `dax_queries`
4. Validar que las consultas son correctas y completas

## Beneficios

### 🔍 Para Auditoría
- **Trazabilidad Completa**: Cada consulta DAX ejecutada queda registrada
- **Reproducibilidad**: Las consultas pueden ejecutarse independientemente
- **Debugging**: Fácil identificación de problemas en consultas específicas

### 📈 Para Análisis
- **Optimización**: Identificar consultas costosas o ineficientes
- **Patrones**: Analizar qué tipos de consultas se ejecutan más frecuentemente
- **Validación**: Verificar que los parámetros son correctos

### 🛡️ Para Compliance
- **Registro de Acceso**: Qué datos se consultaron y cuándo
- **Parámetros Exactos**: Filtros y condiciones aplicadas
- **Historial Completo**: Secuencia temporal de todas las consultas

## Limitaciones Actuales

- **NCS Tool**: No usa consultas DAX (lee archivos S3)
- **Verbatims Tool**: Usa chatbot collector, no consultas DAX directas
- **Herramientas Comparativas**: Solo implementado para modo single period

## Próximos Pasos

1. **Extensión a Modo Comparativo**: Implementar wrappers para análisis comparativo
2. **Más Herramientas**: Cubrir todas las herramientas que usan consultas DAX
3. **Métricas de Rendimiento**: Agregar tiempos de ejecución de consultas
4. **Validación de Consultas**: Verificar sintaxis DAX antes de ejecutar

## Archivos Modificados

- `dashboard_analyzer/anomaly_explanation/genai_core/agents/causal_explanation_agent.py`
  - Agregado campo `dax_queries` al tracker
  - Implementado método `add_dax_query()`
  - Creados wrappers para captura de consultas
  - Modificado método `export_conversation()`

## Archivos de Ejemplo

- `example_conversation_with_dax.json`: Ejemplo de JSON con consultas DAX
- `test_dax_query_tracking.py`: Script de prueba del sistema
- `README_DAX_QUERY_TRACKING.md`: Esta documentación
