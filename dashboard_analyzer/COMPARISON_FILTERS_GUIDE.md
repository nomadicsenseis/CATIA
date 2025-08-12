# Comparison Filters Guide

## Overview

The NPS anomaly detection system supports **9 different comparison filters** that can be selected from the main.py command line and passed to PBI queries as parameters by the causal agent. Each filter provides a different way to compare current performance against historical or target benchmarks.

## Available Comparison Filters

### Standard Filters (Power BI Built-in Logic)

These filters use Power BI's built-in comparison logic and don't require additional date parameters:

1. **`vs L7d`** - Last 7 days
2. **`vs L14D`** - Last 14 days  
3. **`vs L30D`** - Last 30 days
4. **`vs LM`** - Last month
5. **`vs LY`** - Last year
6. **`vs Y-2`** - Year -2
7. **`vs 2019`** - 2019 baseline
8. **`vs Target`** - Target comparison

### Custom Filter (Requires Date Parameters)

9. **`vs Sel. Period`** - Selected period (custom dates)

## How It Works

### 1. Command Line Selection

All filters can be selected from main.py:

```bash
# Standard filters (no dates needed)
python dashboard_analyzer/main.py --causal-filter-comparison 'vs LM'
python dashboard_analyzer/main.py --causal-filter-comparison 'vs LY'
python dashboard_analyzer/main.py --causal-filter-comparison 'vs Target'

# vs Sel. Period (requires dates)
python dashboard_analyzer/main.py --causal-filter-comparison 'vs Sel. Period' --causal-comparison-dates 2023-12-01 2024-01-01
```

### 2. Causal Agent Integration

The causal agent receives the comparison filter as a parameter:

```python
# In FlexibleAnomalyInterpreter
self.causal_filter = causal_filter  # e.g., "vs LM", "vs Sel. Period"
self.comparison_start_date = comparison_start_date  # For vs Sel. Period
self.comparison_end_date = comparison_end_date      # For vs Sel. Period
```

### 3. PBI Query Generation

Each filter generates different DAX queries:

#### Standard Filters (e.g., vs LM)
```dax
VAR __DS0FilterTable7 =
    TREATAS({"vs LM"}, 'Filtro_Comparativa'[Filtro_Comparativa])
```

#### vs Sel. Period
```dax
VAR __DS0FilterTable7 =
    TREATAS({"vs Sel. Period"}, 'Filtro_Comparativa'[Filtro_Comparativa])

VAR __DS0FilterTableSelPeriod =
    FILTER(
        KEEPFILTERS(VALUES('Aux_Date_Master_Selected_Period'[Date_aux])),
        AND(
            'Aux_Date_Master_Selected_Period'[Date_aux] >= DATE(2023, 12, 1),
            'Aux_Date_Master_Selected_Period'[Date_aux] < DATE(2024, 1, 1)
        ))
```

## Supported Query Types

All comparison filters work with these PBI query methods:

1. **Explanatory Drivers**: `collect_explanatory_drivers_for_date_range()`
2. **Routes**: `collect_routes_for_date_range()`
3. **Customer Profile**: `collect_customer_profile_for_date_range()`

## Practical Examples

### Example 1: Compare vs Last Month
```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison 'vs LM' \
  --segment 'Global/SH' \
  --explanation-mode 'agent'
```

**Use Case**: Compare current performance against the previous month to identify monthly trends.

### Example 2: Compare vs Last Year
```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison 'vs LY' \
  --segment 'Global/LH/Business' \
  --explanation-mode 'agent'
```

**Use Case**: Year-over-year comparison to identify annual trends and seasonal patterns.

### Example 3: Compare vs 2019 Baseline
```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison 'vs 2019' \
  --explanation-mode 'agent'
```

**Use Case**: Compare against pre-pandemic baseline to understand recovery and long-term trends.

### Example 4: Compare vs Target
```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison 'vs Target' \
  --anomaly-detection-mode 'target'
```

**Use Case**: Compare actual performance against business targets and goals.

### Example 5: Compare vs Custom Period
```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison 'vs Sel. Period' \
  --causal-comparison-dates 2023-12-01 2024-01-01 \
  --segment 'Global' \
  --explanation-mode 'agent'
```

**Use Case**: Compare against a specific period (e.g., December 2023) to understand performance changes.

## Technical Implementation

### PBI Collector Methods

Each method accepts the comparison filter:

```python
async def collect_explanatory_drivers_for_date_range(
    self, 
    node_path: str, 
    start_date: datetime, 
    end_date: datetime, 
    comparison_filter: str = "vs L7d",  # All filters supported
    comparison_start_date: datetime = None,  # For vs Sel. Period
    comparison_end_date: datetime = None     # For vs Sel. Period
) -> pd.DataFrame:
```

### Causal Agent Context

The causal agent receives the filter information for context:

```python
# For standard filters
causal_filter = "vs LM"  # Agent knows it's comparing vs last month

# For vs Sel. Period
causal_filter = "vs Sel. Period"
comparison_start_date = datetime(2023, 12, 1)
comparison_end_date = datetime(2024, 1, 1)
```

## DAX Query Differences

### Standard Filter (vs LM)
```dax
VAR __DS0FilterTable7 =
    TREATAS({"vs LM"}, 'Filtro_Comparativa'[Filtro_Comparativa])

-- Uses Power BI's built-in logic for last month
```

### vs Sel. Period
```dax
VAR __DS0FilterTable7 =
    TREATAS({"vs Sel. Period"}, 'Filtro_Comparativa'[Filtro_Comparativa])

VAR __DS0FilterTableSelPeriod =
    FILTER(
        KEEPFILTERS(VALUES('Aux_Date_Master_Selected_Period'[Date_aux])),
        AND(
            'Aux_Date_Master_Selected_Period'[Date_aux] >= DATE(2023, 12, 1),
            'Aux_Date_Master_Selected_Period'[Date_aux] < DATE(2024, 1, 1)
        ))

-- Uses custom date range with Aux_Date_Master_Selected_Period
```

## Best Practices

### When to Use Each Filter

1. **`vs L7d`**: Daily/weekly trend analysis
2. **`vs L14D`**: Bi-weekly performance comparison
3. **`vs L30D`**: Monthly trend analysis
4. **`vs LM`**: Month-over-month comparison
5. **`vs LY`**: Year-over-year analysis
6. **`vs Y-2`**: Long-term trend analysis
7. **`vs 2019`**: Pre-pandemic baseline comparison
8. **`vs Target`**: Performance vs business goals
9. **`vs Sel. Period`**: Custom period comparison

### Command Line Tips

```bash
# Always use quotes for filter names with spaces
--causal-filter-comparison 'vs Sel. Period'

# Use YYYY-MM-DD format for dates
--causal-comparison-dates 2023-12-01 2024-01-01

# Combine with other parameters
--causal-filter-comparison 'vs LM' --segment 'Global/SH' --explanation-mode 'agent'
```

## Testing

### Test All Filters
```bash
python dashboard_analyzer/test_all_comparison_filters.py
```

### Test vs Sel. Period
```bash
python dashboard_analyzer/test_sel_period_integration.py
```

### Generated Files
The test scripts generate DAX files for each filter:
- `test_vs_LM_explanatory_drivers.dax`
- `test_vs_LY_explanatory_drivers.dax`
- `test_vs_Sel._Period_explanatory_drivers.dax`
- etc.

## Troubleshooting

### Common Issues

1. **Date Format**: Ensure dates are YYYY-MM-DD format
2. **Filter Names**: Use exact filter names with proper spacing
3. **vs Sel. Period**: Always provide both start and end dates
4. **Power BI Connection**: Verify API credentials are set

### Debug Mode

Enable debug mode for verbose output:

```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison 'vs LM' \
  --debug
```

## Summary

The system provides comprehensive comparison filter support:

- ✅ **9 different filters** available
- ✅ **Standard filters** use Power BI built-in logic
- ✅ **vs Sel. Period** uses custom date range
- ✅ **Causal agent** receives filter context
- ✅ **PBI queries** generated with appropriate DAX
- ✅ **All query types** supported (explanatory drivers, routes, customer profile)

This gives you maximum flexibility to analyze NPS anomalies against different time periods and benchmarks! 