# Implementation Plan: Interactive Geographic Heatmap Visualization System

**Branch**: `001-heatmap-visualization` | **Date**: 2025-12-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-heatmap-visualization/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an interactive web application that visualizes geographic distribution of user data through heatmaps on a Taiwan map. The system loads CSV data containing grid coordinates (gx/gy), converts them to latitude/longitude, and displays time-based heatmap visualizations with automatic hourly cycling. Users can filter by month, select different duration metrics, manually control time periods, and view demographic breakdowns. The application will be packaged as a standalone Windows executable with Vue.js frontend and FastAPI backend.

## Technical Context

**Language/Version**:
- Frontend: JavaScript/TypeScript with Vue.js 3.x
- Backend: Python 3.9+ (conda environment "fapi")

**Primary Dependencies**:
- Frontend: Vue 3 (Composition API), OpenLayers 9.x (mapping), Apache ECharts 5.x (charting), Proj4 (coordinate projection)
- Backend: FastAPI, Pandas 2.x, NumPy 1.26.x, Numba (JIT compilation for coordinate conversion)

**Storage**: File-based (CSV data from data/data.csv, no persistent database needed)

**Testing**:
- Backend: pytest for API contracts and coordinate conversion functions
- Frontend: Vitest (recommended for Vite-based Vue 3 projects)

**Target Platform**:
- Development: Cross-platform (Windows/Mac/Linux)
- Production: Windows executable (single .exe file)

**Project Type**: Web application (Vue.js frontend + FastAPI backend)

**Performance Goals**:
- API response time <500ms (per SC-004, SC-006)
- Visualization rendering <1s (per SC-003)
- Initial load <3s (per constitution principle V)
- Support datasets with 100k+ data points (per constitution)

**Constraints**:
- Must work offline (standalone executable)
- Must convert gx/gy coordinates using TWD97 transformation
- Auto-cycling must be precise (3-second intervals per FR-005)
- RWD: 320px mobile to 4K desktop (per FR-017)

**Scale/Scope**:
- Data: ~2,881 rows in data/data.csv (actual count from research; 4 months × 24 hours × varying locations)
- Endpoints: 3 primary API endpoints (heatmap, demographics, metadata) + health check
- UI Components: 9 Vue components (map, tooltip, 4 controls, 2 charts, 1 dashboard view)
- Coordinate conversion: Mathematical transformation using TWD97 TM2 (no external API calls)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Frontend-Backend Separation ✅

**Status**: PASS

- Frontend (Vue.js) handles UI/UX, user interactions, visualization rendering
- Backend (FastAPI) handles data processing, CSV parsing, coordinate conversion, business logic
- Communication via RESTful API with documented contracts
- No business logic in frontend; no UI rendering in backend

**Evidence**: Spec clearly separates concerns - map rendering and charts in frontend (FR-003, FR-012, FR-013), data processing and coordinate conversion in backend (FR-001, FR-002).

### II. Data-Driven Visualization ✅

**Status**: PASS

- Raw CSV processing in FastAPI backend
- Frontend receives structured JSON for rendering
- No CSV parsing in frontend
- Coordinate conversion (gx/gy → lat/lng) happens server-side

**Evidence**: FR-001 (backend loads CSV), FR-002 (backend converts coordinates). Frontend only consumes processed data for visualization.

### III. Standalone Executable Packaging ✅

**Status**: PASS

- Backend packaged using PyInstaller
- Frontend bundled as static assets
- Single .exe launches embedded web server and opens browser
- No external dependencies for end users

**Evidence**: User requirement explicitly states "最後打包成exe成行檔" (finally package as exe executable). Matches constitution principle III exactly.

### IV. Interactive User Experience ✅

**Status**: PASS

- Heatmap supports interactive exploration (FR-003, FR-004)
- Filtering by month, hour, metric (FR-006, FR-007, FR-008)
- Real-time updates via auto-cycling and manual controls (FR-005, FR-009, FR-010, FR-011)
- Responsive design (FR-017) for different screen sizes

**Evidence**: All interactive requirements align with constitution principle IV. User stories 2-6 focus on interactive filtering and exploration.

### V. Performance & Responsiveness ✅

**Status**: PASS

- Initial load target: <3s (constitution) - not explicitly in spec but assumed
- Visualization rendering: <1s (SC-003)
- Backend API responses: <500ms (SC-004, SC-006)
- Dataset support: 100k data points (constitution) - spec has ~50k rows

**Evidence**: Success criteria SC-003, SC-004, SC-006 directly address performance. Scale matches constitution requirements.

### Technology Stack Constraints ✅

**Status**: PASS

**Mandatory Technologies Met**:
- ✅ Frontend: Vue.js 3.x with Composition API (specified in user input)
- ✅ Backend: FastAPI with Python 3.9+ (specified in user input, conda env "fapi")
- ✅ Data Processing: Pandas for data manipulation (CSV processing)
- ✅ Visualization: Apache ECharts (modern charting library with native Chinese support)
- ✅ Packaging: PyInstaller for EXE generation (as per constitution)

**Prohibited Patterns Avoided**:
- ✅ No SSR - frontend is SPA
- ✅ No database engines - file-based CSV storage
- ✅ No heavyweight frameworks beyond specified stack
- ✅ Using Vue 3 Composition API (not deprecated Options API)

**Evidence**: Technical context matches all mandatory technologies. No violations of prohibited patterns.

### Quality Standards ✅

**Status**: PASS (to be implemented)

**Code Organization**: Plan will specify backend/ and frontend/ directories as per constitution
**Testing Requirements**: Backend API contracts and data processing functions will have tests (pytest)
**Documentation Requirements**:
- API documentation via FastAPI automatic OpenAPI/Swagger
- README with build and packaging instructions (to be created)
- User guide for packaged application (to be created)
- Data format specification (to be created)

**Evidence**: Constitution requirements will be met during implementation. No conflicts identified.

### Summary

**Overall Status**: ✅ PASS - All constitution principles satisfied

No violations requiring justification. Feature aligns perfectly with established architectural principles and technology constraints. Ready to proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── data.py            # Data query endpoints
│   │   │   ├── coordinates.py     # Coordinate conversion endpoints
│   │   │   └── demographics.py    # Demographic statistics endpoints
│   │   └── models/
│   │       ├── request.py         # API request schemas
│   │       └── response.py        # API response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_loader.py         # CSV loading and caching
│   │   ├── coordinate_converter.py # gx/gy ↔ lat/lng conversion
│   │   ├── heatmap_aggregator.py  # Aggregate data for heatmap
│   │   └── demographic_calculator.py # Calculate percentages
│   ├── models/
│   │   ├── __init__.py
│   │   └── location_data.py       # Data models for location points
│   └── utils/
│       ├── __init__.py
│       └── config.py               # Configuration and constants
├── tests/
│   ├── test_api_contracts.py      # API contract tests
│   ├── test_coordinate_converter.py # Coordinate conversion tests
│   ├── test_data_loader.py        # Data loading tests
│   └── test_demographic_calculator.py # Demographic calculation tests
├── requirements.txt                # Python dependencies
└── build_exe.py                    # PyInstaller build script

frontend/
├── src/
│   ├── main.js                     # Vue app entry point
│   ├── App.vue                     # Root component
│   ├── components/
│   │   ├── map/
│   │   │   ├── HeatmapMap.vue      # Main map component with heatmap
│   │   │   └── MapTooltip.vue      # Hover tooltip component
│   │   ├── controls/
│   │   │   ├── MonthSelector.vue   # Month selection dropdown
│   │   │   ├── MetricSelector.vue  # Duration metric selector
│   │   │   ├── TimelineSlider.vue  # Hour selection slider
│   │   │   └── PlaybackControls.vue # Play/pause/reset buttons
│   │   └── charts/
│   │       ├── GenderChart.vue     # Gender distribution chart
│   │       └── AgeChart.vue        # Age distribution chart
│   ├── views/
│   │   └── Dashboard.vue           # Main dashboard view
│   ├── services/
│   │   ├── api.js                  # API client
│   │   └── dataService.js          # Data fetching and caching
│   ├── composables/
│   │   ├── useHeatmapData.js       # Heatmap data management
│   │   ├── useAutoplay.js          # Auto-cycling logic
│   │   └── useDemographics.js      # Demographic data management
│   └── assets/
│       └── styles/                 # CSS/SCSS files
├── public/
│   └── index.html
├── package.json
└── vite.config.js                  # Vite bundler configuration

data/
├── data.csv                        # Source data file
└── gxgy_transfer.ipynb            # Reference: coordinate conversion formula

docs/
├── user-guide.md                   # End-user documentation
├── data-format.md                  # CSV schema documentation
└── build-instructions.md           # Development and packaging guide

README.md                           # Project overview and setup
```

**Structure Decision**: Selected Option 2 (Web application) as this is a Vue.js frontend + FastAPI backend project. The structure follows the constitution's code organization requirements with clear separation between `backend/` and `frontend/` directories. PyInstaller will bundle the backend as an executable that serves the frontend static assets.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All requirements align with constitution principles.

---

## Implementation Summary

### Phase 0: Research ✅ COMPLETED

All technical decisions have been resolved through comprehensive research:

1. **Mapping Library**: OpenLayers 9.x
   - Offline capability for standalone executable
   - Native TWD97 coordinate system support
   - Excellent heatmap performance (100k+ points)

2. **Charting Library**: Apache ECharts 5.x
   - Native Chinese language support
   - Official Vue 3 integration (vue-echarts)
   - Canvas-based rendering for real-time updates

3. **Coordinate Conversion**: Numba JIT + LRU Caching
   - ~260,000 conversions/second performance
   - <10MB memory footprint
   - Inverse TM2 transformation (gx/gy → lat/lng)

4. **Data Caching**: Pandas DataFrame + Dictionary Lookup
   - 1-3ms query performance (O(1) lookup)
   - ~5MB memory usage
   - 1000+ requests/second capacity

5. **Packaging**: PyInstaller Single-File Executable
   - 40-60MB target size (with UPX compression)
   - Embedded frontend + backend + data
   - Auto-launch browser on startup

**Artifacts Generated:**
- [research.md](./research.md) - Detailed technology research and decisions

### Phase 1: Design ✅ COMPLETED

Data models and API contracts have been defined:

1. **Data Model**: 5 core entities documented
   - Location Data Point (with demographics)
   - Time Period (month + hour)
   - Heatmap Layer Data
   - Demographic Summary
   - All relationships and validation rules defined

2. **API Contracts**: OpenAPI 3.0 specification
   - 3 primary endpoints: `/api/heatmap`, `/api/demographics`, `/api/metadata`
   - Complete request/response schemas
   - Chinese labels for demographic categories
   - Error handling specifications

3. **Development Guide**: Quickstart documentation
   - Backend setup (conda environment)
   - Frontend setup (npm)
   - Testing procedures
   - Troubleshooting guide

**Artifacts Generated:**
- [data-model.md](./data-model.md) - Entity definitions and relationships
- [contracts/openapi.yaml](./contracts/openapi.yaml) - API specification
- [quickstart.md](./quickstart.md) - Developer onboarding guide

### Phase 2: Task Planning (Next Step)

Use `/speckit.tasks` command to generate implementation task breakdown:
- Backend: Data loader, coordinate converter, API endpoints
- Frontend: Map component, charts, controls, auto-cycling
- Integration: API client, state management
- Testing: Unit tests, API contract tests
- Packaging: Build scripts, executable generation

### Ready for Implementation

**Verification Checklist:**
- ✅ All NEEDS CLARIFICATION items resolved
- ✅ Constitution compliance verified
- ✅ Technology stack finalized
- ✅ Data models documented
- ✅ API contracts defined
- ✅ Project structure specified
- ✅ Development guide created

**Next Command**: `/speckit.tasks` to generate detailed implementation tasks

---

## Key Technical Specifications

### Backend Stack
```
Python 3.9+
├── FastAPI 0.104.1          # Web framework
├── Uvicorn 0.24.0           # ASGI server
├── Pandas 2.1.3             # Data processing
├── NumPy 1.26.2             # Numerical operations
├── Numba 0.58.1             # JIT compilation
└── PyInstaller 6.2.0        # Executable packaging
```

### Frontend Stack
```
Vue.js 3.4.0
├── OpenLayers 9.0.0         # Mapping library
├── ECharts 5.4.0            # Charting library
├── vue-echarts 6.6.0        # Vue wrapper for ECharts
├── Proj4 2.11.0             # Coordinate projection
└── Vite 5.x                 # Build tool
```

### Data Flow
```
CSV File (data.csv)
    ↓
Backend: Load & Convert (gx/gy → lat/lng)
    ↓
In-Memory Cache (Pandas DataFrame)
    ↓
API Endpoints (FastAPI)
    ↓
Frontend: Visualization (OpenLayers + ECharts)
```

### Performance Targets (from Research)
- **Startup**: 1-2 seconds (data loading + conversion)
- **API Response**: 1-5ms (with caching)
- **Heatmap Render**: <1s (per SC-003)
- **Demographic Update**: <500ms (per SC-006)
- **Memory Usage**: ~5MB (data cache)
- **Executable Size**: 40-60MB (compressed)

### API Endpoints Overview
| Endpoint | Method | Purpose | Cache |
|----------|--------|---------|-------|
| `/api/heatmap` | GET | Location data for map | O(1) lookup |
| `/api/demographics` | GET | Gender/age statistics | LRU cached |
| `/api/metadata` | GET | Available options | Static |
| `/health` | GET | Server status | N/A |

### Component Hierarchy (Frontend)
```
App.vue
└── Dashboard.vue
    ├── HeatmapMap.vue
    │   └── MapTooltip.vue
    ├── MonthSelector.vue
    ├── MetricSelector.vue
    ├── TimelineSlider.vue
    ├── PlaybackControls.vue
    ├── GenderChart.vue
    └── AgeChart.vue
```

---

**Plan Status**: ✅ COMPLETE - Ready for task generation and implementation
**Last Updated**: 2025-12-15
**Next Step**: Run `/speckit.tasks` to create detailed implementation tasks
