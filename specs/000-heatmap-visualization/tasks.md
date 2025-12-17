# Tasks: Interactive Geographic Heatmap Visualization System

**Feature**: 001-heatmap-visualization
**Input**: Design documents from `/specs/001-heatmap-visualization/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with:
- Backend: `backend/src/`
- Frontend: `frontend/src/`
- Tests: `backend/tests/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETED

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure: backend/src/{api,services,models,utils}, backend/tests/
- [X] T002 Create frontend directory structure: frontend/src/{components/{map,controls,charts},views,services,composables,assets/styles}
- [X] T003 Initialize Python project with backend/requirements.txt (FastAPI, Pandas, NumPy, Numba, Uvicorn, pytest)
- [X] T004 Initialize Node.js project with frontend/package.json (Vue 3, OpenLayers, ECharts, vue-echarts, Proj4, Vite)
- [X] T005 [P] Create backend/.gitignore for Python artifacts
- [X] T006 [P] Create frontend/.gitignore for Node artifacts
- [X] T007 [P] Create docs/ directory structure: docs/{user-guide.md,data-format.md,build-instructions.md}
- [X] T008 Create README.md at repository root with project overview

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [X] T009 Implement coordinate converter service in backend/src/services/coordinate_converter.py with Numba JIT gx/gy→lat/lng conversion
- [X] T010 Implement data loader service in backend/src/services/data_loader.py with Pandas DataFrame initialization and CSV loading
- [X] T011 Create LocationData model in backend/src/models/location_data.py with all data point attributes
- [X] T012 Create configuration utilities in backend/src/utils/config.py (TWD97 parameters, grid constants, file paths)
- [X] T013 Initialize FastAPI app in backend/src/main.py with CORS middleware and static file serving
- [X] T014 Create API route structure: backend/src/api/routes/{data.py,demographics.py}
- [X] T015 Create API models: backend/src/api/models/{request.py,response.py} with Pydantic schemas matching OpenAPI spec

### Frontend Foundation

- [X] T016 Create Vue app entry in frontend/src/main.js with ECharts registration
- [X] T017 Create root component in frontend/src/App.vue with layout structure
- [X] T018 Create API client in frontend/src/services/api.js with axios instance for backend communication
- [X] T019 Configure Vite in frontend/vite.config.js with proxy to backend port 8000
- [X] T020 Setup Proj4 registration in frontend/src/services/proj4Config.js for TWD97 coordinate system
- [X] T021 Create base styles in frontend/src/assets/styles/main.css for responsive layout

### Testing Foundation

- [X] T022 [P] Setup pytest configuration in backend/pytest.ini
- [X] T023 [P] Create test for coordinate converter in backend/tests/test_coordinate_converter.py (round-trip verification)
- [ ] T024 [P] Create test for data loader in backend/tests/test_data_loader.py (CSV loading and caching)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Geographic Distribution (Priority: P1) 🎯 MVP

**Goal**: Display interactive map with heatmap showing user density from CSV data

**Independent Test**: Open application → Map displays with heatmap overlay → Hover shows tooltip with user counts

### Backend for US1

- [X] T025 [US1] Implement GET /api/heatmap endpoint in backend/src/api/routes/data.py (query params: month, hour, metric)
- [X] T026 [US1] Implement heatmap aggregator service (integrated in data_loader.py get_heatmap_data method)
- [X] T027 [US1] Create HeatmapResponse schema in backend/src/api/models/response.py matching OpenAPI spec
- [X] T028 [US1] Implement GET /api/metadata endpoint in backend/src/api/routes/data.py (return available months, hours, metrics)
- [X] T029 [US1] Add data validation and error handling for invalid month/hour combinations

### Frontend for US1

- [X] T030 [P] [US1] Create HeatmapMap component in frontend/src/components/map/HeatmapMap.vue with OpenLayers integration
- [X] T031 [P] [US1] Create MapTooltip component in frontend/src/components/map/MapTooltip.vue for hover display
- [X] T032 [US1] Create useHeatmapData composable in frontend/src/composables/useHeatmapData.js (fetch data, manage state)
- [X] T033 [US1] Create dataService in frontend/src/services/dataService.js (API calls with caching)
- [X] T034 [US1] Create Dashboard view in frontend/src/views/Dashboard.vue integrating HeatmapMap component
- [X] T035 [US1] Configure OpenLayers heatmap layer with blur=15, radius=8, gradient settings (integrated in HeatmapMap)
- [X] T036 [US1] Implement tooltip positioning logic to follow mouse cursor (integrated in HeatmapMap)

### Testing for US1

- [ ] T037 [P] [US1] API contract test in backend/tests/test_api_contracts.py for /api/heatmap endpoint
- [ ] T038 [P] [US1] API contract test in backend/tests/test_api_contracts.py for /api/metadata endpoint
- [ ] T039 [US1] Test heatmap aggregator in backend/tests/test_heatmap_aggregator.py (verify filtering and weight calculation)

**Checkpoint**: User Story 1 fully functional - can view geographic distribution with tooltip

---

## Phase 4: User Story 2 - View Time-Based Changes (Priority: P2)

**Goal**: Automatic cycling through 24 hours every 3 seconds showing temporal patterns

**Independent Test**: Watch heatmap auto-cycle through hours 0-23 → Verify 3-second intervals → Check hour indicator updates

### Backend for US2

- [ ] T040 [US2] Optimize heatmap endpoint response time for rapid sequential requests (<500ms per SC-004)

### Frontend for US2

- [X] T041 [US2] Create useAutoplay composable in frontend/src/composables/useAutoplay.js (setInterval logic, hour state)
- [X] T042 [US2] Create PlaybackControls component in frontend/src/components/controls/PlaybackControls.vue (play/pause/reset buttons)
- [X] T043 [US2] Integrate auto-cycling into Dashboard view with useAutoplay composable
- [X] T044 [US2] Display current hour indicator (0-23) prominently in Dashboard view
- [X] T045 [US2] Implement smooth heatmap transitions when hour changes (fade effect)
- [X] T046 [US2] Add play/pause state management to prevent multiple intervals

**Checkpoint**: Auto-cycling works independently - temporal patterns visible

---

## Phase 5: User Story 3 - Filter by Month (Priority: P2)

**Goal**: Allow users to select specific months (Dec 2024, Feb 2025, May 2025, Aug 2025)

**Independent Test**: Select each month option → Verify heatmap updates to show only that month's data

### Frontend for US3

- [X] T047 [US3] Create MonthSelector component in frontend/src/components/controls/MonthSelector.vue (dropdown with 4 month options)
- [X] T048 [US3] Add month state management to useHeatmapData composable
- [X] T049 [US3] Integrate MonthSelector into Dashboard view
- [X] T050 [US3] Update heatmap data fetch to include selected month parameter
- [X] T051 [US3] Display month labels in Chinese format (e.g., "2024年12月")
- [X] T052 [US3] Pause auto-cycling when user manually changes month (per FR-009)

**Checkpoint**: Month filtering works independently - seasonal patterns visible

---

## Phase 6: User Story 4 - Select Different Metrics (Priority: P2)

**Goal**: Choose between total users, <10min, 10-30min, >30min duration categories

**Independent Test**: Select each metric → Verify heatmap recalculates intensity → Tooltip shows metric-specific values

### Frontend for US4

- [X] T053 [US4] Create MetricSelector component in frontend/src/components/controls/MetricSelector.vue (4 metric options with Chinese labels)
- [X] T054 [US4] Add metric state management to useHeatmapData composable
- [X] T055 [US4] Integrate MetricSelector into Dashboard view
- [X] T056 [US4] Update heatmap data fetch to include selected metric parameter
- [X] T057 [US4] Display metric labels: "全部停留人數", "停留10分鐘以下", "停留10-30分鐘", "停留30分鐘以上"
- [X] T058 [US4] Update tooltip to show current metric's value
- [X] T059 [US4] Pause auto-cycling when user manually changes metric (per FR-009)

**Checkpoint**: Metric selection works independently - duration patterns visible

---

## Phase 7: User Story 5 - Manual Time Control (Priority: P3)

**Goal**: Timeline slider for manual hour selection, pausing auto-cycle

**Independent Test**: Drag slider to hour 14 → Auto-cycle stops → Heatmap shows hour 14 → Click play → Cycle resumes

### Frontend for US5

- [X] T060 [US5] Create TimelineSlider component in frontend/src/components/controls/TimelineSlider.vue (0-23 range slider)
- [X] T061 [US5] Integrate TimelineSlider into Dashboard view below map
- [X] T062 [US5] Connect slider to hour state in useAutoplay composable
- [X] T063 [US5] Implement auto-pause when slider is manually adjusted (per FR-009)
- [X] T064 [US5] Add visual feedback for slider interaction (active state)
- [X] T065 [US5] Connect "Reset" button in PlaybackControls to reset hour to 0 and restart auto-cycle (per FR-011)
- [X] T066 [US5] Connect "Start Auto-Play" button to resume cycling from current hour (per FR-010)

**Checkpoint**: Manual time control works independently - users can examine specific hours

---

## Phase 8: User Story 6 - View Demographic Breakdown (Priority: P3)

**Goal**: Display gender and age distribution charts for selected time period

**Independent Test**: Select different months/hours → Gender chart shows 男性/女性 percentages → Age chart shows 9 age groups

### Backend for US6

- [X] T067 [US6] Implement GET /api/demographics endpoint in backend/src/api/routes/demographics.py (query params: month, hour, metric)
- [X] T068 [US6] Implement demographic calculator service in backend/src/services/demographic_calculator.py (weighted percentage calculations)
- [X] T069 [US6] Create DemographicResponse schema in backend/src/api/models/response.py matching OpenAPI spec
- [X] T070 [US6] Add LRU caching to demographic calculations (functools.lru_cache, maxsize=128)

### Frontend for US6

- [X] T071 [P] [US6] Create GenderChart component in frontend/src/components/charts/GenderChart.vue (ECharts pie chart)
- [X] T072 [P] [US6] Create AgeChart component in frontend/src/components/charts/AgeChart.vue (ECharts bar chart)
- [X] T073 [US6] Create useDemographics composable in frontend/src/composables/useDemographics.js (fetch and manage demographic data)
- [X] T074 [US6] Integrate GenderChart and AgeChart into Dashboard view
- [X] T075 [US6] Configure gender chart with Chinese labels: "男性" (sex_1), "女性" (sex_2)
- [X] T076 [US6] Configure age chart with 9 Chinese labels: "19歲以下", "20-24歲", "25-29歲", "30-34歲", "35-39歲", "40-44歲", "45-49歲", "50-54歲", "55-59歲", "60歲以上"
- [X] T077 [US6] Update demographic charts whenever month or hour changes (per FR-014)
- [X] T078 [US6] Display "No data available" message when demographic values are zero

### Testing for US6

- [ ] T079 [P] [US6] API contract test in backend/tests/test_api_contracts.py for /api/demographics endpoint
- [ ] T080 [US6] Test demographic calculator in backend/tests/test_demographic_calculator.py (verify weighted averages sum to 100%)

**Checkpoint**: All user stories complete - demographic insights visible

---

## Phase 9: Cross-Cutting Concerns

**Purpose**: Responsive design, performance, error handling across all stories

- [ ] T081 [P] Implement responsive layout in Dashboard view (FR-017): mobile (320px+), tablet (768px+), desktop (1024px+)
- [ ] T082 [P] Add mobile-specific styles: map on top, controls stacked below, charts vertical
- [ ] T083 Implement error boundaries in frontend for graceful error handling (FR-020)
- [ ] T084 Add loading states and spinners for API calls
- [ ] T085 Implement debouncing for rapid filter changes (edge case from spec.md)
- [ ] T086 Add data validation error messages for missing CSV columns (edge case from spec.md)
- [ ] T087 Handle invalid coordinate conversion gracefully with logging (edge case from spec.md)
- [ ] T088 [P] Add /health endpoint in backend/src/main.py (per OpenAPI spec)
- [ ] T089 Optimize bundle size with tree-shaking (ECharts components, OpenLayers modules)
- [ ] T090 Test performance: visualization rendering <1s (SC-003), API responses <500ms (SC-004)

---

## Phase 10: Packaging & Documentation

**Purpose**: Build Windows executable and complete documentation

### Packaging

- [ ] T091 Build frontend production bundle: cd frontend && npm run build
- [ ] T092 Create PyInstaller spec file in backend/build_exe.spec with embedded frontend dist/
- [ ] T093 Create build script in backend/build_exe.py (automated PyInstaller execution)
- [ ] T094 Configure PyInstaller: bundle data/data.csv, exclude tkinter/matplotlib, enable UPX compression
- [ ] T095 Implement resource path resolution in backend/src/utils/config.py (sys._MEIPASS for PyInstaller)
- [ ] T096 Implement auto-launch browser in backend/src/main.py (find port 8000-8010, wait for server readiness)
- [ ] T097 Test executable: StoreHeatmap.exe starts, opens browser, all features work offline

### Documentation

- [ ] T098 [P] Write user guide in docs/user-guide.md (how to use the application)
- [ ] T099 [P] Write data format spec in docs/data-format.md (CSV schema documentation)
- [ ] T100 [P] Write build instructions in docs/build-instructions.md (development setup, packaging steps)
- [ ] T101 Update README.md with project description, setup instructions, technology stack
- [ ] T102 Verify quickstart.md instructions work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (P1) → US2 (P2) → US3 (P2) → US4 (P2) → US5 (P3) → US6 (P3)
  - Can work in parallel if team capacity allows
- **Cross-Cutting (Phase 9)**: Depends on core user stories (US1-US4 minimum)
- **Packaging (Phase 10)**: Depends on all desired features being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends only on Foundational - no other story dependencies
- **User Story 2 (P2)**: Depends on US1 (needs map and heatmap data) - integrates auto-cycling
- **User Story 3 (P2)**: Depends on US1 (needs map display) - adds month filtering
- **User Story 4 (P2)**: Depends on US1 (needs heatmap) - adds metric selection
- **User Story 5 (P3)**: Depends on US1, US2 (needs map and auto-cycling) - adds manual control
- **User Story 6 (P3)**: Depends on US1 (needs time period selection) - adds demographic charts

### Within Each User Story

- Backend endpoints before frontend API calls
- Composables before components
- Base components before integration into Dashboard
- Core functionality before edge case handling

### Parallel Opportunities

**Setup Phase:**
```bash
T005 [P] backend/.gitignore
T006 [P] frontend/.gitignore
T007 [P] docs/ structure
```

**Foundational Phase:**
```bash
T022 [P] pytest configuration
T023 [P] coordinate converter test
T024 [P] data loader test
```

**User Story 1:**
```bash
T030 [P] HeatmapMap component
T031 [P] MapTooltip component
T037 [P] /api/heatmap contract test
T038 [P] /api/metadata contract test
```

**User Story 6:**
```bash
T071 [P] GenderChart component
T072 [P] AgeChart component
T079 [P] /api/demographics contract test
```

**Cross-Cutting:**
```bash
T081 [P] Responsive layout
T082 [P] Mobile styles
T088 [P] /health endpoint
```

**Documentation:**
```bash
T098 [P] User guide
T099 [P] Data format spec
T100 [P] Build instructions
```

---

## Parallel Example: Foundational Phase

```bash
# All backend foundation services (sequential):
Task: T009 coordinate_converter.py
Task: T010 data_loader.py
Task: T011 location_data.py
Task: T012 config.py

# Then tests in parallel:
Task: T023 test_coordinate_converter.py
Task: T024 test_data_loader.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Open app → See heatmap → Hover for tooltip
5. Demo to stakeholders

### Incremental Delivery

1. Foundation → US1 → **MVP Demo** (geographic distribution)
2. Add US2 → **Demo** (temporal patterns via auto-cycling)
3. Add US3 + US4 → **Demo** (filtering by month and metric)
4. Add US5 → **Demo** (manual time control)
5. Add US6 → **Demo** (demographic insights)
6. Polish → Packaging → **Final Delivery** (Windows .exe)

### Parallel Team Strategy

With 2-3 developers after Foundational phase:

1. **Developer A**: US1 (P1 - blocking) → US5 (P3 - timeline slider)
2. **Developer B**: Wait for US1 → US2 (P2 - auto-cycling) → US3 (P2 - month filter)
3. **Developer C**: Wait for US1 → US4 (P2 - metric selection) → US6 (P3 - demographics)

Stories integrate independently into Dashboard view.

---

## Notes

- [P] tasks = different files, can run in parallel
- [Story] label (US1-US6) maps to user stories from spec.md
- Backend paths: `backend/src/`, Frontend paths: `frontend/src/`
- Each user story should be independently testable
- Stop at checkpoints to validate before proceeding
- Commit after each task or logical group
- Final target: Single Windows .exe (40-60MB, per research.md)
- Performance targets: <1s rendering (SC-003), <500ms API (SC-004)
