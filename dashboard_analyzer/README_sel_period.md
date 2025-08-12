# vs Sel. Period Filter Implementation

## Overview

This implementation adds support for the "vs Sel. Period" comparison filter in the NPS anomaly detection system. This filter allows you to compare current data against a specific selected period using the proper Power BI DAX logic with `Aux_Date_Master_Selected_Period`.

## What Changed

### 1. Updated DAX Query Logic

The system now uses the correct Power BI approach for "vs Sel. Period":

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

### 2. Updated PBI Collector Methods

The following methods in `pbi_collector.py` have been updated:

- `_get_explanatory_drivers_range_query()`
- `_get_routes_range_query()`
- `_get_customer_profile_range_query()`

### 3. Supported Query Types

The "vs Sel. Period" filter now works with:

- **Explanatory Drivers**: Shows satisfaction differences vs selected period
- **Customer Profile**: Shows customer segment analysis vs selected period  
- **Routes**: Shows route performance vs selected period

## How to Use

### Command Line Usage

```bash
# Basic usage with vs Sel. Period
python dashboard_analyzer/main.py --causal-filter-comparison "vs Sel. Period" --causal-comparison-dates 2023-12-01 2024-01-01

# With additional parameters
python dashboard_analyzer/main.py \
  --causal-filter-comparison "vs Sel. Period" \
  --causal-comparison-dates 2023-12-01 2024-01-01 \
  --segment "Global/SH" \
  --explanation-mode "agent"
```

### Parameters

- `--causal-filter-comparison "vs Sel. Period"`: Enables the vs Sel. Period filter
- `--causal-comparison-dates START_DATE END_DATE`: Sets the comparison period (YYYY-MM-DD format)

### Example Scenarios

#### 1. Compare Current Month vs December 2023
```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison "vs Sel. Period" \
  --causal-comparison-dates 2023-12-01 2024-01-01
```

#### 2. Compare Specific Segment vs Previous Year
```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison "vs Sel. Period" \
  --causal-comparison-dates 2023-01-01 2023-12-31 \
  --segment "Global/SH/Economy"
```

#### 3. Full Analysis with vs Sel. Period
```bash
python dashboard_analyzer/main.py \
  --mode "comprehensive" \
  --causal-filter-comparison "vs Sel. Period" \
  --causal-comparison-dates 2023-12-01 2024-01-01 \
  --segment "Global" \
  --explanation-mode "agent" \
  --clean
```

## Technical Details

### DAX Query Structure

The updated queries include:

1. **vs Sel. Period Filter**: `TREATAS({"vs Sel. Period"}, 'Filtro_Comparativa'[Filtro_Comparativa])`
2. **Selected Period Date Filter**: Uses `Aux_Date_Master_Selected_Period[Date_aux]`
3. **Date Range Logic**: `AND(>= START_DATE, < END_DATE)`

### Integration Points

- **main.py**: Argument parsing for `--causal-filter-comparison` and `--causal-comparison-dates`
- **pbi_collector.py**: Updated query generation methods
- **Query Templates**: Modified to support the new filter logic

## Testing

### Test Scripts

1. **Basic Query Generation**: `test_sel_period_queries.py`
2. **Integration Testing**: `test_sel_period_integration.py`

### Running Tests

```bash
# Test query generation
python dashboard_analyzer/test_sel_period_queries.py

# Test integration
python dashboard_analyzer/test_sel_period_integration.py
```

### Generated Files

The test scripts generate DAX files for inspection:
- `test_explanatory_drivers_sel_period.dax`
- `test_customer_profile_sel_period.dax`
- `test_routes_sel_period.dax`
- `integration_test_*.dax`

## Verification

### Power BI Testing

1. Copy the generated DAX queries
2. Paste into Power BI DAX Editor
3. Verify the queries execute correctly
4. Check that the vs Sel. Period logic works as expected

### System Testing

1. Run the main.py with vs Sel. Period parameters
2. Verify the analysis completes successfully
3. Check that the explanations reference the correct comparison period
4. Validate the data matches expectations

## Troubleshooting

### Common Issues

1. **Date Format**: Ensure dates are in YYYY-MM-DD format
2. **Power BI Connection**: Verify Power BI API credentials are set
3. **Query Errors**: Check generated DAX files for syntax issues

### Debug Mode

Enable debug mode for verbose output:

```bash
python dashboard_analyzer/main.py \
  --causal-filter-comparison "vs Sel. Period" \
  --causal-comparison-dates 2023-12-01 2024-01-01 \
  --debug
```

## Next Steps

1. **Test in Power BI**: Verify the DAX queries work correctly
2. **Validate Results**: Compare vs Sel. Period results with other filters
3. **Performance Testing**: Ensure the new logic doesn't impact performance
4. **Documentation**: Update user documentation with examples

## Files Modified

- `dashboard_analyzer/data_collection/pbi_collector.py`: Updated query methods
- `dashboard_analyzer/test_sel_period_queries.py`: Test script (new)
- `dashboard_analyzer/test_sel_period_integration.py`: Integration test (new)
- `dashboard_analyzer/README_sel_period.md`: This documentation (new) 