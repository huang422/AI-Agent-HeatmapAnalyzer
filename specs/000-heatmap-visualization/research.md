# Research Findings: Interactive Geographic Heatmap Visualization System

**Feature**: 001-heatmap-visualization
**Date**: 2025-12-15
**Purpose**: Resolve all NEEDS CLARIFICATION items from Technical Context

---

## 1. Mapping Library Selection

### Decision: **OpenLayers**

### Rationale

OpenLayers is the optimal choice for this Taiwan-focused heatmap visualization application for these critical reasons:

1. **True Offline Capability**: Can use local tile sources (MBTiles, GeoTIFF, pre-downloaded tiles) with no mandatory external API calls - perfect for standalone .exe packaging
2. **Native TWD97/TM2 Support**: Built-in Proj4js integration with native support for Taiwan's TWD97 (EPSG:3826) coordinate system
3. **Excellent Heatmap Performance**: Built-in WebGL rendering handles 100k+ points smoothly; our ~2,881 data points well within limits
4. **No Licensing Restrictions**: Completely open source (BSD 2-Clause), free for commercial use in standalone applications
5. **Vue 3 Integration**: Framework-agnostic design works cleanly with Vue 3 Composition API through reactive composables

### Alternatives Considered

| Library | Pros | Cons | Verdict |
| ------- | ---- | ---- | ------- |
| **Leaflet.js** | Lightweight, excellent Vue3-Leaflet wrapper, simple API | Weaker TWD97 support, heatmap degrades beyond 10-20k points | Good for simpler projects but OpenLayers better handles coordinate systems |
| **Mapbox GL JS** | Excellent WebGL performance, beautiful styling | v2+ requires API key with restrictive licensing for offline use - dealbreaker | Licensing restrictions unsuitable for standalone app |
| **Google Maps** | Familiar API, rich features | Cannot work offline, requires constant connection, no TWD97 support | Completely unsuitable due to online-only requirement |

### Implementation Notes

**Required Packages:**
```json
{
  "ol": "^9.0.0",
  "proj4": "^2.11.0"
}
```

**Key Features to Use:**
- `Heatmap` layer with WebGL acceleration
- `Overlay` for hover tooltips
- Proj4 registration for TWD97 coordinate system
- Local tile sources bundled with executable
- Vector sources for data points

**Offline Map Tiles Strategy:**
- Download OpenStreetMap tiles for Taiwan region (zoom 7-15)
- Bundle tiles in exe resources folder (~200-500MB for comprehensive coverage)
- Alternative: Lightweight vector tiles from Taiwan GeoJSON (~5-20MB)

---

## 2. Charting Library Selection

### Decision: **Apache ECharts**

### Rationale

ECharts is the clear winner for demographic visualization in this Vue 3 application:

1. **Native Chinese Support**: Developed by Baidu with first-class Chinese language support - critical for labels like 男性/女性, 19歲以下, etc.
2. **Excellent Vue 3 Integration**: Official `vue-echarts` wrapper with full Composition API support via `<v-chart>` component
3. **Performance for Real-Time Updates**: Canvas-based rendering with built-in update optimization handles 3-second interval updates smoothly
4. **Desktop Application Ready**: Works perfectly in standalone desktop environments, no external dependencies, can be bundled entirely
5. **Rich Chart Types**: Built-in pie and bar charts with automatic percentage calculation support

### Alternatives Considered

| Library | Pros | Cons | Verdict |
| ------- | ---- | ---- | ------- |
| **Chart.js** | Lightweight, simple API | Chinese text requires manual configuration with rendering issues, limited customization | Good for simple Western apps, not ideal for Chinese text |
| **D3.js** | Maximum flexibility, powerful | Steep learning curve, no built-in Vue 3 integration, much larger bundle size | Overkill for standard bar/pie charts |
| **Recharts** | React-style declarative API | Designed for React not Vue, no official Vue support | Wrong framework |

### Implementation Notes

**Required Packages:**
```json
{
  "echarts": "^5.4.0",
  "vue-echarts": "^6.6.0"
}
```

**Vue 3 Integration Pattern:**
```vue
<script setup>
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'

// Register only needed components (tree-shaking)
use([CanvasRenderer, PieChart, BarChart, TitleComponent, TooltipComponent, LegendComponent])

const genderChartOption = computed(() => ({
  title: { text: '性別分布' },
  series: [{
    type: 'pie',
    data: [
      { value: demographicData.value.sex_1, name: '男性' },
      { value: demographicData.value.sex_2, name: '女性' }
    ]
  }]
}))
</script>

<template>
  <v-chart :option="genderChartOption" autoresize />
</template>
```

**Performance**: Bundle size ~300KB (minified, with required components only)

---

## 3. Coordinate Conversion Implementation

### Decision: **Hybrid NumPy Vectorization + Numba JIT + LRU Caching**

### Rationale

Based on analysis of data/gxgy_transfer.ipynb, the optimal approach combines:

1. **Numba JIT Compilation**: For the iterative tm2geo inverse transformation (~130x speedup over pure Python)
2. **LRU Caching**: For frequently accessed grid coordinates (common in heatmap scenarios)
3. **NumPy Vectorization**: For batch preprocessing operations

### Mathematical Background

**Forward Conversion (lat/lng → gx/gy):**
1. Convert to TM2 (Transverse Mercator 2-degree) coordinates using TWD97 parameters
2. Convert TM2 to grid indices with 50m cell size

**Inverse Conversion (gx/gy → lat/lng):**
1. Convert grid indices to TM2 coordinates (grid center)
2. Use iterative binary search to find footpoint latitude (converges in ~20 iterations)
3. Apply inverse formulas to calculate final lat/lng

**TWD97 Parameters:**
- Ellipsoid: WGS84 (a=6378137m, f=1/298.257222101)
- Central Meridian: 121.0°
- Scale Factor: 0.9999
- False Easting: 250000m
- Grid Origin: sw_lat=-32871.4054m, sw_lng=2422126.0017m
- Cell Size: 50m

### Performance Analysis

| Approach | Performance (50k conversions) | Memory | Complexity |
| -------- | ----------------------------- | ------ | ---------- |
| Pure Python | ~15-20 seconds | Low | Simple |
| NumPy only | ~5 seconds | Medium | Moderate |
| **Numba JIT** (chosen) | **~0.2 seconds** | Low | Moderate |
| C Extension | ~0.05 seconds | Low | High |
| Hybrid with cache | **~0.04 seconds** (80% hit rate) | Medium | Moderate |

**Expected Performance:**
- Single conversion: ~4 microseconds (~260,000 conversions/sec)
- 50k conversions (cold cache): ~200ms
- 50k conversions (80% cache hit): ~40ms
- Memory footprint: <10MB

### Implementation Notes

**Core Function Signature:**
```python
@lru_cache(maxsize=10000)
def grid_to_lat_lng(gx: int, gy: int) -> Tuple[float, float]:
    """Convert grid indices to lat/lng with LRU caching"""
    tm2_x = GRID_SW_LAT_OFFSET + (gx + 0.5) * GRID_CELL_SIZE
    tm2_y = GRID_SW_LNG_OFFSET + (gy + 0.5) * GRID_CELL_SIZE
    return _tm2geo_jit(tm2_x, tm2_y)

@jit(nopython=True)
def _tm2geo_jit(x: float, y: float) -> Tuple[float, float]:
    """Numba-optimized TM2 to lat/lng conversion"""
    # Iterative footpoint latitude calculation
    # ... implementation from notebook
```

**Testing Strategy:**
1. Round-trip verification: lat/lng → gx/gy → lat/lng (accuracy within 50m grid resolution ~0.0005°)
2. Known coordinates from notebook (5+ test cases from cells 4, 7)
3. Edge cases (Taiwan boundaries)
4. Performance benchmarks (50k target)

---

## 4. Data Caching Strategy

### Decision: **Hybrid Eager-Lazy Caching with In-Memory Pandas DataFrame**

### Rationale

The dataset is small (~2,881 rows, not 50k as initially estimated), making full in-memory caching optimal:

1. **Pandas DataFrame**: Provides excellent filtering, aggregations, and memory efficiency for this data size
2. **Eager Coordinate Conversion**: Convert all gx/gy → lat/lng on startup (one-time ~800ms cost)
3. **MultiIndex + Dictionary Lookup**: Pre-build (month, hour) → DataFrame slice dictionary for O(1) filtering
4. **Lazy Demographic Aggregation**: Calculate weighted percentages on-demand with LRU caching
5. **Optimized Data Types**: Use float32, int8, int16 instead of defaults to reduce memory by ~50%

### Memory Footprint

- Raw CSV: 584KB
- DataFrame in memory: ~2-3MB
- Lookup dictionary overhead: ~1MB
- Total: **~4-5MB** (well under 500MB limit, only 1% of budget)

### Performance Metrics

| Operation | Time | Notes |
| --------- | ---- | ----- |
| Initial load (startup) | 1-2s | One-time cost |
| Heatmap query | 1-3ms | O(1) lookup + JSON serialization |
| Demographics (cached) | 0.1ms | LRU cache hit |
| Demographics (uncached) | 5-10ms | Weighted aggregation |

**Expected capacity: 1000+ requests/second**

### Implementation Architecture

```python
class DataCache:
    def __init__(self):
        self.df = None  # Pandas DataFrame with MultiIndex
        self.lookup_dict = {}  # (month, hour) → DataFrame slice

    def initialize(self, csv_path: str):
        # 1. Load CSV
        self.df = pd.read_csv(csv_path)

        # 2. Convert gx/gy to lat/lng (EAGER)
        self.df[['lat', 'lng']] = self.df.apply(
            lambda row: pd.Series(gxgy_to_latlng(row['gx'], row['gy'])),
            axis=1
        )

        # 3. Optimize data types (float32, int8, int16)
        self._optimize_dtypes()

        # 4. Create MultiIndex and lookup dictionary
        self.df.set_index(['month', 'hour'], inplace=True)
        self._build_lookup_dict()

    def get_heatmap_data(self, month: int, hour: int) -> list:
        """O(1) lookup for heatmap data"""
        return self.lookup_dict[(month, hour)]

    @lru_cache(maxsize=128)
    def get_demographics(self, month: int, hour: int, metric: str) -> dict:
        """Cached weighted demographic aggregations"""
        # Calculate percentages from filtered data
```

### Alternatives Considered

| Approach | Pros | Cons | Verdict |
| -------- | ---- | ---- | ------- |
| Pure Dictionary | Simple | More memory, harder aggregations | Rejected |
| NumPy Arrays | Fast operations | Loses column names, poor JSON serialization | Rejected |
| SQLite in-memory | SQL flexibility | Overhead for this data size | Rejected - overkill |
| Redis/Memcached | Scalable | External dependency, serialization overhead | Rejected - unnecessary |
| **Pandas + Dict** (chosen) | **Best balance** | Slightly more complex | **Selected** |

---

## 5. PyInstaller Packaging Strategy

### Decision: **Single-File Executable with Embedded Assets**

### Rationale

Package FastAPI backend and Vue.js frontend as a single Windows executable:

1. **User Experience**: One `.exe` file - no installation, no configuration required
2. **Offline Operation**: All assets (frontend, data CSV, map tiles) bundled inside executable
3. **Security**: Tamper-proof - users can't accidentally modify files
4. **Professional**: Clean distribution with no visible folder structure

### Architecture

```
StoreHeatmap.exe (single file)
├── FastAPI backend (bundled Python)
├── Uvicorn server (embedded)
├── Vue.js frontend (static assets)
├── data/data.csv (bundled)
└── Map tiles (optional, can be external)
```

**Startup Sequence:**
1. Extract assets to temporary folder (sys._MEIPASS)
2. Find available port (8000-8010)
3. Start Uvicorn server on localhost:PORT
4. Wait for server readiness
5. Auto-open default browser to http://localhost:PORT

### Implementation Notes

**Resource Path Resolution:**
```python
def get_base_path():
    """Get base path for resources (works in dev and PyInstaller)"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)  # PyInstaller temp folder
    else:
        return Path(__file__).parent.parent.parent  # Development
```

**PyInstaller Spec File Key Settings:**
```python
datas = [
    ('dist/frontend', 'dist/frontend'),  # Vue build output
    ('data/data.csv', 'data'),           # CSV data
]

hiddenimports = [
    'uvicorn.logging',
    'uvicorn.loops.auto',
    'uvicorn.protocols.http.auto',
    # ... FastAPI dependencies
]

excludes = [
    'tkinter', 'matplotlib', 'PIL',  # Reduce size
]

exe = EXE(
    ...,
    upx=True,  # UPX compression (40-60% size reduction)
    console=True,  # Set False to hide console window
    name='StoreHeatmap',
)
```

**Size Optimization:**
- Without optimization: 80-120MB
- With UPX + excludes: **40-60MB** (target)
- Frontend assets: 2-5MB
- Data CSV: ~600KB

### Build Process

```bash
# 1. Build Vue.js frontend
cd frontend && npm run build

# 2. Build executable
cd backend
python build_exe.py  # Automated build script

# Output: backend/dist/StoreHeatmap.exe
```

### Browser Auto-Launch Strategy

```python
def wait_and_open_browser(url, timeout=30):
    """Wait for server readiness, then open browser"""
    import requests
    while time.time() - start < timeout:
        try:
            requests.get(url, timeout=1)
            webbrowser.open(url)
            return
        except:
            time.sleep(0.5)

# Launch in separate thread
threading.Thread(target=wait_and_open_browser, args=(url,), daemon=True).start()
```

### Alternatives Considered

| Approach | Pros | Cons | Verdict |
| -------- | ---- | ---- | ------- |
| **Single-file exe** (chosen) | Clean distribution, tamper-proof | Larger file, slower startup (~2-3s) | **Selected** - best UX |
| Exe + frontend folder | Smaller exe, easier frontend updates | User can break it, messy | Rejected - UX concerns |
| Electron + Python | Cross-platform, rich desktop features | 100+ MB, heavy resource usage | Rejected - overkill |
| Nuitka compilation | Smaller size, better performance | Longer compile, less FastAPI support | Could revisit if issues |

---

## Summary of Decisions

| Area | Decision | Key Benefits |
| ---- | -------- | ------------ |
| **Map Library** | OpenLayers | Offline capability, TWD97 support, no licensing issues |
| **Chart Library** | Apache ECharts | Native Chinese support, excellent Vue 3 integration |
| **Coordinate Conversion** | Numba JIT + LRU cache | 260k conversions/sec, <10MB memory |
| **Data Caching** | Pandas DataFrame + Dict lookup | 1-3ms queries, ~5MB memory, 1000+ req/s |
| **Packaging** | PyInstaller single-file | 40-60MB exe, one-click deployment |

---

## Next Phase: Data Model & Contracts

With all technical decisions resolved, we can proceed to Phase 1:
1. Define data models based on CSV schema and coordinate conversion
2. Design API contracts for heatmap, demographics, and metadata endpoints
3. Create development quickstart guide
4. Update agent context with selected technologies
