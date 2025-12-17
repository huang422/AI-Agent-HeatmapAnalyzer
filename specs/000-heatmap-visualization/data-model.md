# Data Model: Interactive Geographic Heatmap Visualization System

**Feature**: 001-heatmap-visualization
**Date**: 2025-12-15
**Source**: Derived from [spec.md](./spec.md) Key Entities and data/data.csv structure

---

## Overview

This document defines the data structures used throughout the application. Models are described at a conceptual level, independent of implementation details.

---

## 1. Location Data Point

Represents user activity aggregated at a specific grid location (50m × 50m cell) for a specific month and hour.

### Attributes

| Attribute | Type | Description | Constraints | Source Column |
| --------- | ---- | ----------- | ----------- | ------------- |
| **month** | Integer | Month identifier in YYYYMM format | 202412, 202502, 202505, 202508 | month |
| **gx** | Integer | Grid X coordinate (TWD97 TM2 system) | 7000-8000 range | gx |
| **gy** | Integer | Grid Y coordinate (TWD97 TM2 system) | 0-8000 range | gy |
| **latitude** | Float | WGS84 latitude (derived from gx/gy) | 21.9-25.3° (Taiwan bounds) | *(computed)* |
| **longitude** | Float | WGS84 longitude (derived from gx/gy) | 118.0-122.1° (Taiwan bounds) | *(computed)* |
| **hour** | Integer | Hour of day (24-hour format) | 0-23 | hour |
| **day_type** | String | Weekday/Weekend classification | "假日" (holiday/weekend), "平日" (weekday) | day_type |
| **avg_total_users** | Float | Average total users at this location | ≥0 | avg_total_users |
| **avg_users_under_10min** | Float | Average users staying <10 minutes | ≥0 | avg_users_under_10min |
| **avg_users_10_30min** | Float | Average users staying 10-30 minutes | ≥0 | avg_users_10_30min |
| **avg_users_over_30min** | Float | Average users staying >30 minutes | ≥0 | avg_users_over_30min |

**Relationships:**
- Maps to exactly one Time Period (month + hour combination)
- Contains one Demographic Distribution

**Validation Rules:**
- month MUST be one of: 202412, 202502, 202505, 202508
- hour MUST be 0-23
- gx, gy MUST be within Taiwan grid bounds
- All avg_* fields MUST be non-negative
- Sum of duration fields ≤ avg_total_users (with small tolerance for rounding)

---

## 2. Demographic Distribution

Represents the demographic breakdown (gender and age) for users at a specific location and time.

### Gender Breakdown

| Attribute | Type | Description | Constraints | Source Column |
| --------- | ---- | ----------- | ----------- | ------------- |
| **sex_1** | Float | Percentage of male users | 0-100 | sex_1 |
| **sex_2** | Float | Percentage of female users | 0-100 | sex_2 |

**Validation**: sex_1 + sex_2 ≈ 100 (sum to 100% with tolerance for rounding)

### Age Breakdown

| Attribute | Type | Description | Constraints | Source Column |
| --------- | ---- | ----------- | ----------- | ------------- |
| **age_1** | Float | Percentage of users 19歲以下 (under 19) | 0-100 | age_1 |
| **age_2** | Float | Percentage of users 20-24歲 | 0-100 | age_2 |
| **age_3** | Float | Percentage of users 25-29歲 | 0-100 | age_3 |
| **age_4** | Float | Percentage of users 30-34歲 | 0-100 | age_4 |
| **age_5** | Float | Percentage of users 35-39歲 | 0-100 | age_5 |
| **age_6** | Float | Percentage of users 40-44歲 | 0-100 | age_6 |
| **age_7** | Float | Percentage of users 45-49歲 | 0-100 | age_7 |
| **age_8** | Float | Percentage of users 50-54歲 | 0-100 | age_8 |
| **age_9** | Float | Percentage of users 55-59歲 | 0-100 | age_9 |
| **age_other** | Float | Percentage of users 60+ (other ages) | 0-100 | age_other |

**Validation**: sum(age_1..age_9, age_other) ≈ 100

### Geographic Distribution (Additional Context)

The CSV also contains city-level distribution data for reference:

| Attribute Pattern | Description | Example |
| ----------------- | ----------- | ------- |
| **city_{name}** | Percentage from each city | city_taipei, city_kaohsiung |

*Note: City data is present but not currently used in primary visualization features*

**Relationships:**
- Belongs to exactly one Location Data Point

---

## 3. Time Period

Represents a specific combination of month and hour for data filtering.

### Attributes

| Attribute | Type | Description | Constraints |
| --------- | ---- | ----------- | ----------- |
| **month** | Integer | Month identifier | 202412, 202502, 202505, 202508 |
| **hour** | Integer | Hour of day | 0-23 |

**Relationships:**
- Associated with multiple Location Data Points

**Derived Properties:**
- **month_label**: Human-readable month name (e.g., "December 2024", "202412年12月")
- **hour_label**: Human-readable hour (e.g., "14:00", "下午2點")
- **unique_key**: Composite key "(month, hour)" for lookups

---

## 4. Heatmap Layer Data

Represents the processed data structure for rendering the heatmap visualization.

### Attributes

| Attribute | Type | Description | Constraints |
| --------- | ---- | ----------- | ----------- |
| **coordinates** | Array | Array of [latitude, longitude, weight] tuples | Non-empty |
| **month** | Integer | Current filter: month | One of 4 valid months |
| **hour** | Integer | Current filter: hour | 0-23 |
| **metric** | String | Current metric being visualized | One of 4 duration metrics |
| **min_weight** | Float | Minimum weight value in dataset | ≥0 |
| **max_weight** | Float | Maximum weight value in dataset | ≥min_weight |
| **total_points** | Integer | Number of data points | >0 |

**Relationships:**
- Aggregated from filtered Location Data Points

**Usage**: Frontend consumes this for map rendering

---

## 5. Demographic Summary

Represents aggregated demographic statistics for a specific time period.

### Attributes

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| **time_period** | Time Period | Month and hour for this summary |
| **total_users** | Float | Total user count across all locations |
| **gender_distribution** | Object | Weighted percentages by gender |
| **age_distribution** | Object | Weighted percentages by age group |

**gender_distribution structure:**
```json
{
  "male": 54.2,    // Weighted average of sex_1
  "female": 45.8    // Weighted average of sex_2
}
```

**age_distribution structure:**
```json
{
  "under_19": 2.1,
  "20_24": 6.8,
  "25_29": 9.3,
  "30_34": 8.2,
  "35_39": 7.5,
  "40_44": 8.1,
  "45_49": 10.2,
  "50_54": 11.4,
  "55_59": 12.3,
  "60_plus": 24.1
}
```

**Calculation Method:**
- Weighted average: (sum of location_metric × demographic_percentage) / total_metric
- Ensures demographics reflect actual user distribution, not equal-weighted location average

**Relationships:**
- Derived from multiple Location Data Points filtered by Time Period

---

## Data Relationships Diagram

```
┌─────────────────┐
│   Time Period   │
│  (month, hour)  │
└────────┬────────┘
         │ 1:N
         │
         ▼
┌────────────────────────┐
│  Location Data Point   │
│  (gx, gy, metrics)     │◄────── coordinates derived from (gx, gy)
└────────┬───────────────┘
         │ 1:1
         │
         ▼
┌────────────────────────┐
│ Demographic Distribution│
│  (sex_%, age_%)        │
└────────────────────────┘

         │
         │ aggregated to
         ▼
┌────────────────────────┐
│  Heatmap Layer Data    │
│  (for visualization)   │
└────────────────────────┘

         │
         │ summarized to
         ▼
┌────────────────────────┐
│  Demographic Summary   │
│  (weighted averages)   │
└────────────────────────┘
```

---

## Data Invariants

### Global Constraints

1. **Temporal Coverage**: Exactly 4 months × 24 hours = 96 unique time periods
2. **Spatial Coverage**: Variable number of (gx, gy) locations per time period (based on data collection)
3. **Percentage Totals**: All demographic percentages sum to ~100 (±1% tolerance for rounding)
4. **Duration Logic**: avg_users_under_10min + avg_users_10_30min + avg_users_over_30min ≤ avg_total_users
5. **Coordinate Bounds**: All lat/lng must fall within Taiwan geographic boundaries

### Data Quality Rules

1. **No Negative Values**: All user counts and percentages must be ≥0
2. **Coordinate Validity**: All (gx, gy) must successfully convert to valid (lat, lng)
3. **Time Period Validity**: No gaps in hourly data within a month (0-23 all present)
4. **Demographic Completeness**: If total_users > 0, demographic percentages must exist

---

## Example Data Instance

```json
{
  "location_data_point": {
    "month": 202412,
    "gx": 7165,
    "gy": 7152,
    "latitude": 25.033,
    "longitude": 121.544,
    "hour": 0,
    "day_type": "假日",
    "avg_total_users": 20.67,
    "avg_users_under_10min": 1.0,
    "avg_users_10_30min": 7.0,
    "avg_users_over_30min": 12.67,
    "demographics": {
      "gender": {
        "sex_1": 54.42,
        "sex_2": 45.58
      },
      "age": {
        "age_1": 1.43,
        "age_2": 3.49,
        "age_3": 6.68,
        "age_4": 6.59,
        "age_5": 11.90,
        "age_6": 4.84,
        "age_7": 11.92,
        "age_8": 8.46,
        "age_9": 17.43,
        "age_other": 27.27
      }
    }
  }
}
```

---

## Implementation Notes

### Backend Data Types (Python/Pandas)

```python
dtype_mapping = {
    'month': 'int32',
    'gx': 'int16',
    'gy': 'int16',
    'hour': 'int8',
    'day_type': 'category',
    'avg_total_users': 'float32',
    'avg_users_under_10min': 'float32',
    'avg_users_10_30min': 'float32',
    'avg_users_over_30min': 'float32',
    'sex_1': 'float32',
    'sex_2': 'float32',
    'age_1': 'float32',
    # ... other age columns
    'latitude': 'float64',   # Higher precision for coordinates
    'longitude': 'float64'
}
```

### Frontend Data Types (TypeScript Interfaces)

```typescript
interface LocationDataPoint {
  month: number;
  gx: number;
  gy: number;
  latitude: number;
  longitude: number;
  hour: number;
  avgTotalUsers: number;
  avgUsersUnder10min: number;
  avgUsers10_30min: number;
  avgUsersOver30min: number;
}

interface DemographicDistribution {
  gender: {
    male: number;    // sex_1
    female: number;  // sex_2
  };
  age: {
    under19: number;  // age_1
    age20_24: number; // age_2
    // ... other age groups
  };
}

interface HeatmapDataPoint {
  lat: number;
  lng: number;
  weight: number;
}
```

---

## Data Volume Estimates

Based on data/data.csv inspection:

| Metric | Value |
| ------ | ----- |
| Total Rows | ~2,881 |
| Unique (gx, gy) Locations | ~500-600 |
| Time Periods (month × hour) | 96 |
| Average Locations per Time Period | ~30 |
| CSV File Size | 584 KB |
| In-Memory Size (optimized) | ~4-5 MB |
| With lat/lng conversion | ~5-6 MB |

---

## Next Steps

This data model will be used to:
1. Define API request/response schemas in `/contracts`
2. Design database migrations (if needed - currently file-based)
3. Generate TypeScript interfaces for frontend
4. Validate data transformations in backend services
