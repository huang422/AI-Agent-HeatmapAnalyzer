# Tasks: AI Chatbot Sidebar for Heatmap Data Analysis

**Input**: Design documents from `/specs/001-ai-chatbot/`
**Prerequisites**: plan.md (tech stack, architecture), spec.md (user stories with priorities), contracts/chat-api.yaml (API specs)

**Tests**: Tests are OPTIONAL per plan.md ("Frontend component tests optional", "Backend unit/integration tests"). Manual E2E testing is REQUIRED for acceptance scenarios.

**Organization**: Tasks grouped by user story to enable independent implementation and testing. User Story 1 + User Story 4 form the MVP (P1 priorities).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/` (per plan.md structure)
- **Backend tests**: `backend/tests/unit/`, `backend/tests/integration/`
- **Frontend tests**: `frontend/tests/components/` (optional)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Environment setup and dependency installation for Ollama integration

- [ ] T001 Add `ollama>=0.1.0` to backend/requirements.txt
- [ ] T002 Install Ollama on development machine (manual: `curl -fsSL https://ollama.com/install.sh | sh`)
- [ ] T003 Pull qwen2.5:7b model (manual: `ollama pull qwen2.5:7b`)
- [ ] T004 Verify Ollama service running on localhost:11434 (manual: `ollama serve`)
- [ ] T005 Create frontend/src/components/chat/ directory for chat components
- [ ] T006 Create backend/tests/unit/ directory if not exists
- [ ] T007 Create backend/tests/integration/ directory if not exists

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend services that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 [P] Implement OllamaService class in backend/src/services/ollama_service.py with __init__, check_health, generate_response methods
- [ ] T009 [P] Implement DataExporter class in backend/src/services/data_exporter.py with export_to_json and get_context_summary methods
- [ ] T010 Add OLLAMA_HOST constant to backend/src/utils/config.py (default: http://localhost:11434)
- [ ] T011 Create Pydantic models in backend/src/api/models/chat.py (ChatMessage, ChatRequest, ChatResponse, HealthResponse)
- [ ] T012 Implement POST /api/chat/message endpoint in backend/src/api/routes/chat.py
- [ ] T013 Implement GET /api/chat/health endpoint in backend/src/api/routes/chat.py
- [ ] T014 Implement GET /api/chat/context endpoint in backend/src/api/routes/chat.py (optional debug endpoint)
- [ ] T015 Register chat router in backend/src/main.py with `app.include_router(chat.router)`
- [ ] T016 Add Ollama health check to startup_event in backend/src/main.py

**Checkpoint**: Backend foundation ready - frontend implementation can now begin in parallel with testing

---

## Phase 3: User Story 1 - Basic AI Conversation (Priority: P1) 🎯 MVP Component 1/2

**Goal**: Users can open chatbot sidebar, ask questions in natural language, and receive AI-powered analysis of current heatmap data

**Independent Test**:
1. Start Ollama service (`ollama serve`)
2. Start backend (`uvicorn src.main:app --reload`)
3. Start frontend (`npm run dev`)
4. Open http://localhost:5173
5. Click chatbot button (🤖)
6. Type "哪個時段最繁忙？" and press Enter
7. Verify AI responds with data-driven answer in ~2-5 seconds
8. Verify response mentions specific numbers from current filter context

### Implementation for User Story 1

- [ ] T017 [P] [US1] Create useChatbot composable in frontend/src/composables/useChatbot.js with messages, isThinking, isConnected state and sendMessage, checkHealth functions
- [ ] T018 [P] [US1] Create ChatSidebar.vue component in frontend/src/components/chat/ChatSidebar.vue with toggle button, message display, input field, and thinking indicator
- [ ] T019 [US1] Add chat color variables to frontend/src/assets/styles/main.css (--chat-bg, --chat-user-bg, --chat-ai-bg, --chat-border)
- [ ] T020 [US1] Implement getCurrentContext function in useChatbot.js to extract month/hour/day_type from useHeatmapData composable
- [ ] T021 [US1] Implement message sending logic in useChatbot.js calling POST /api/chat/message with context and history
- [ ] T022 [US1] Implement automatic scroll-to-bottom in ChatSidebar.vue when new message arrives
- [ ] T023 [US1] Implement AI response display with timestamp in ChatSidebar.vue
- [ ] T024 [US1] Add Traditional Chinese system prompt building in backend/src/services/ollama_service.py (include data context JSON, field descriptions, response rules)
- [ ] T025 [US1] Implement error handling in useChatbot.js for 503 (Ollama offline), 500 (inference failed), network timeout (30s)
- [ ] T026 [US1] Display user-friendly error messages in ChatSidebar.vue for AI service errors

**Checkpoint**: User Story 1 complete - users can have basic conversations with AI about heatmap data

---

## Phase 4: User Story 4 - Sidebar UI Interaction (Priority: P1) 🎯 MVP Component 2/2

**Goal**: Smooth chatbot open/close with responsive design that doesn't break existing features

**Independent Test**:
1. Open application at different screen sizes (1920px, 768px, 375px)
2. Click chatbot toggle button
3. Verify sidebar slides in smoothly (<300ms animation)
4. Verify main content resizes appropriately (desktop: calc(100% - 350px), mobile: overlay)
5. While chatbot open, test existing features: switch month, adjust timeline, view charts
6. Verify all existing features work normally
7. Click close button or outside chatbot
8. Verify sidebar collapses and main content returns to original width

### Implementation for User Story 4

- [ ] T027 [P] [US4] Implement open/close toggle logic in ChatSidebar.vue with isOpen state
- [ ] T028 [P] [US4] Add slide-in/slide-out CSS transitions in ChatSidebar.vue (transform: translateX, 300ms ease-in-out)
- [ ] T029 [P] [US4] Add responsive CSS breakpoints in ChatSidebar.vue (desktop ≥1024px: 350px sidebar, tablet 768-1023px: 320px, mobile <768px: 100vw overlay)
- [ ] T030 [P] [US4] Add z-index layers in ChatSidebar.vue (sidebar: 100, backdrop: 99) to avoid conflicts with map controls (z-index: 10) and tooltips (z-index: 50)
- [ ] T031 [US4] Include ChatSidebar component in frontend/src/views/Dashboard.vue
- [ ] T032 [US4] Add conditional margin-right to main content in Dashboard.vue when chatbot is open (desktop only)
- [ ] T033 [US4] Implement semi-transparent backdrop in ChatSidebar.vue for mobile overlay (opacity: 0.5, black background)
- [ ] T034 [US4] Implement click-outside-to-close logic in ChatSidebar.vue using backdrop click event
- [ ] T035 [US4] Implement unread message badge counter in ChatSidebar.vue toggle button (increments when message arrives while closed)
- [ ] T036 [US4] Add keyboard navigation support (Escape key to close, Enter to send) in ChatSidebar.vue
- [ ] T037 [US4] Add ARIA labels to chatbot toggle button and input field for accessibility

**Checkpoint**: MVP complete (User Story 1 + User Story 4) - fully functional chatbot with responsive UI

---

## Phase 5: User Story 2 - Demographic Analysis Queries (Priority: P2)

**Goal**: AI can analyze and answer demographic-specific questions about gender and age distribution

**Independent Test**:
1. Open chatbot sidebar
2. Ask "哪些區域女性使用者比例最高？"
3. Verify AI response includes:
   - Top 3 locations with highest sex_2 percentage
   - Latitude/longitude coordinates for each location
   - Actual sex_2 percentage values
4. Ask "哪個年齡層的人最多？"
5. Verify AI correctly identifies highest age group (age_1 through age_9) with percentage

### Implementation for User Story 2

- [ ] T038 [P] [US2] Enhance system prompt in backend/src/services/ollama_service.py with explicit age field mappings (age_1: <19, age_2: 20-24, etc.)
- [ ] T039 [P] [US2] Enhance system prompt in backend/src/services/ollama_service.py with explicit gender field mappings (sex_1: male %, sex_2: female %)
- [ ] T040 [US2] Add top_locations calculation to get_context_summary in backend/src/services/data_exporter.py (top 5 by avg_total_users with lat/lon)
- [ ] T041 [US2] Add age distribution aggregation to get_context_summary in backend/src/services/data_exporter.py (average age_1 through age_9)
- [ ] T042 [US2] Update system prompt template in backend/src/services/ollama_service.py to include top_locations and age distribution in JSON context
- [ ] T043 [US2] Test demographic queries manually (gender, age, location-specific) and verify AI responses match actual data

**Checkpoint**: User Story 2 complete - AI can accurately analyze demographics

---

## Phase 6: User Story 3 - Time-based Pattern Discovery (Priority: P3)

**Goal**: AI can compare data across different time conditions (weekday vs weekend, different hours)

**Independent Test**:
1. Open chatbot sidebar
2. Ask "平日和假日的使用者數差異大嗎？"
3. Verify AI response includes:
   - Total users for day_type='平日'
   - Total users for day_type='假日'
   - Percentage or absolute difference
4. Ask "一天中哪個小時最繁忙？"
5. Verify AI identifies hour (0-23) with highest avg_total_users sum

### Implementation for User Story 3

- [ ] T044 [US3] Enhance DataExporter.export_to_json in backend/src/services/data_exporter.py to support filtering by multiple conditions (for comparison queries)
- [ ] T045 [US3] Add cross-time comparison logic to system prompt in backend/src/services/ollama_service.py (instructions for comparing day_type='平日' vs '假日')
- [ ] T046 [US3] Add hourly aggregation to get_context_summary in backend/src/services/data_exporter.py (sum avg_total_users by hour)
- [ ] T047 [US3] Add dwell time pattern analysis to system prompt in backend/src/services/ollama_service.py (describe avg_users_under_10min vs 10_30min vs over_30min)
- [ ] T048 [US3] Test time-based comparison queries manually (weekday vs weekend, hour comparisons, dwell time) and verify AI responses

**Checkpoint**: User Story 3 complete - AI can analyze temporal patterns

---

## Phase 7: Testing & Quality Assurance (Optional Backend Tests)

**Purpose**: Add backend unit and integration tests (frontend tests remain optional per plan.md)

**Note**: These tests are OPTIONAL. Manual E2E testing is sufficient for MVP validation.

- [ ] T049 [P] Create test_ollama_service.py in backend/tests/unit/ with mock Ollama client to test check_health, generate_response, and error handling
- [ ] T050 [P] Create test_data_exporter.py in backend/tests/unit/ with sample DataCache to test export_to_json, get_context_summary, and coordinate preservation
- [ ] T051 [P] Create test_chat_api.py in backend/tests/integration/ to test POST /api/chat/message with mock Ollama (200, 400, 503, 500 responses)
- [ ] T052 [P] Create test_chat_api.py in backend/tests/integration/ to test GET /api/chat/health endpoint (connected and disconnected states)
- [ ] T053 [P] Create test_chat_api.py in backend/tests/integration/ to test GET /api/chat/context endpoint with filtering parameters

**Checkpoint**: Backend tests complete (if implemented)

---

## Phase 8: Edge Cases & Error Handling

**Purpose**: Handle all edge cases from spec.md to ensure robust user experience

- [ ] T054 [P] Implement 500-character message length limit in frontend/src/components/chat/ChatSidebar.vue with character counter display
- [ ] T055 [P] Implement rapid request prevention in frontend/src/composables/useChatbot.js (disable send button while isThinking=true)
- [ ] T056 [P] Add 30-second timeout to axios request in frontend/src/composables/useChatbot.js for /api/chat/message
- [ ] T057 [P] Display timeout error message in ChatSidebar.vue with retry button when request exceeds 30s
- [ ] T058 [US1] Add empty data check in backend/src/services/data_exporter.py (if total_records=0, include flag in context)
- [ ] T059 [US1] Update system prompt in backend/src/services/ollama_service.py to handle no-data case (respond "當前條件下無可用數據")
- [ ] T060 [US4] Implement health check polling in ChatSidebar.vue (check /api/chat/health every 30 seconds when offline)
- [ ] T061 [US4] Update connection status indicator in ChatSidebar.vue based on health check results (green "● 已連線" vs red "⚠ 離線")
- [ ] T062 Disable send button and input in ChatSidebar.vue when isConnected=false

**Checkpoint**: All edge cases handled per spec.md

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [ ] T063 [P] Update README.md with Ollama setup instructions (install, pull model, start service)
- [ ] T064 [P] Add system prompt optimization based on manual testing results (adjust wording, examples, constraints)
- [ ] T065 [P] Add example questions to ChatSidebar.vue welcome message ("你可以詢問：哪個時段最繁忙？ 年輕人主要在哪些區域活動？")
- [ ] T066 Code review and cleanup: remove console.log statements, add JSDoc comments to useChatbot.js
- [ ] T067 Verify existing heatmap/chart performance unchanged (manual test: measure render times before/after chatbot)
- [ ] T068 Run full manual E2E test suite covering all acceptance scenarios from spec.md
- [ ] T069 Test responsive design on actual devices (desktop 1920px, tablet 768px, mobile 375px)
- [ ] T070 Verify PyInstaller packaging still works (manual: build .exe, test chatbot functionality)

**Checkpoint**: Feature complete and polished

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (Ollama installed, dependencies added) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion - Core chatbot conversation
- **User Story 4 (Phase 4)**: Depends on Phase 2 completion - Can run in parallel with US1 (different files)
- **User Story 2 (Phase 5)**: Depends on Phase 2 + Phase 3 (enhances existing prompt) - Demographic analysis
- **User Story 3 (Phase 6)**: Depends on Phase 2 + Phase 3 (enhances existing prompt) - Time patterns
- **Testing (Phase 7)**: Optional - Can run in parallel with Phase 8
- **Edge Cases (Phase 8)**: Depends on Phase 3 + Phase 4 completion
- **Polish (Phase 9)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories, can run parallel with US1
- **User Story 2 (P2)**: Depends on User Story 1 (enhances same system prompt file) - Not truly independent but can be tested separately
- **User Story 3 (P3)**: Depends on User Story 1 (enhances same system prompt file) - Not truly independent but can be tested separately

### Within Each User Story

- User Story 1 & 4: Backend services → API endpoints → Frontend composable → UI component → Error handling
- User Story 2 & 3: Enhance existing services → Update prompt → Manual testing

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks except T004 can run in parallel (T001-T007 are independent setup steps; T004 requires T002-T003)

**Phase 2 (Foundational)**: T008 and T009 can run in parallel (different files), T011 can run parallel with both, T012-T014 can run in parallel after T011, T015-T016 sequential after T012-T014

**Phase 3 (US1) + Phase 4 (US4)**: Can run in parallel - different components
- US1 tasks: T017 and T018 can run in parallel, T019 can run parallel with both
- US4 tasks: T027-T030 can run in parallel, T031-T037 have some dependencies

**Phase 5 (US2)**: T038-T041 can run in parallel (different enhancements)

**Phase 6 (US3)**: T044-T047 can run in parallel (different enhancements)

**Phase 7 (Testing)**: All test file creation (T049-T053) can run in parallel

**Phase 8 (Edge Cases)**: T054-T057 can run in parallel, T058-T059 can run in parallel, T060-T062 sequential

**Phase 9 (Polish)**: T063-T065 can run in parallel

---

## Parallel Example: MVP (User Story 1 + User Story 4)

### After Phase 2 Foundational completes, launch in parallel:

**Team Member A - User Story 1 (Backend & State)**:
```bash
Task T017: "Create useChatbot composable in frontend/src/composables/useChatbot.js"
Task T024: "Add Traditional Chinese system prompt in backend/src/services/ollama_service.py"
```

**Team Member B - User Story 4 (UI & UX)**:
```bash
Task T027: "Implement open/close toggle logic in ChatSidebar.vue"
Task T028: "Add slide-in/slide-out CSS transitions in ChatSidebar.vue"
Task T029: "Add responsive CSS breakpoints in ChatSidebar.vue"
Task T030: "Add z-index layers in ChatSidebar.vue"
```

**Team Member A continues**:
```bash
Task T018: "Create ChatSidebar.vue component" (merges with Team B's work)
Task T020: "Implement getCurrentContext function in useChatbot.js"
Task T021: "Implement message sending logic in useChatbot.js"
```

**Team Member B continues**:
```bash
Task T031: "Include ChatSidebar component in Dashboard.vue"
Task T032: "Add conditional margin-right to main content in Dashboard.vue"
Task T033: "Implement semi-transparent backdrop for mobile"
```

Both converge for integration testing of MVP.

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 4 Only)

1. ✅ Complete Phase 1: Setup (Ollama installed, dependencies added)
2. ✅ Complete Phase 2: Foundational (Backend services and API endpoints ready)
3. ✅ Complete Phase 3: User Story 1 (Basic AI conversation works)
4. ✅ Complete Phase 4: User Story 4 (Responsive UI interaction works)
5. **STOP and VALIDATE**: Test both stories independently:
   - US1: Ask questions, verify AI responds with accurate data
   - US4: Open/close on desktop/tablet/mobile, verify existing features unaffected
6. Deploy/demo MVP if ready

**MVP Deliverable**: Users can open chatbot, ask basic questions, get AI-powered answers, close chatbot - all without breaking existing heatmap features.

### Incremental Delivery

1. Complete Setup (Phase 1) + Foundational (Phase 2) → **Foundation ready**
2. Add User Story 1 + User Story 4 → Test independently → **Deploy MVP!**
3. Add User Story 2 → Test demographic queries → **Deploy enhanced version**
4. Add User Story 3 → Test time comparisons → **Deploy full feature**
5. Add Edge Cases (Phase 8) → Test error scenarios → **Deploy production-ready**
6. Add Polish (Phase 9) → Final validation → **Deploy polished version**

Each phase adds value without breaking previous functionality.

### Parallel Team Strategy

With 2 developers:

1. **Both**: Complete Phase 1 + Phase 2 together (foundation)
2. Once Phase 2 done:
   - **Developer A**: User Story 1 (T017-T026) - Backend + state management
   - **Developer B**: User Story 4 (T027-T037) - UI/UX + responsiveness
3. **Both**: Integrate and test MVP
4. **Developer A**: User Story 2 (T038-T043) - Demographics
5. **Developer B**: User Story 3 (T044-T048) - Time patterns
6. **Both**: Edge cases + Polish

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label (US1, US2, US3, US4) maps task to specific user story for traceability
- User Story 1 + User Story 4 together form the MVP (both P1 priority)
- User Story 2 and 3 enhance the same system prompt (backend/src/services/ollama_service.py), so have sequential dependency
- Manual E2E testing is REQUIRED per plan.md; backend unit/integration tests are OPTIONAL
- Commit after completing each user story phase
- Stop at any checkpoint to validate story independently
- All file paths are absolute from repository root
- Traditional Chinese is the primary language for user-facing messages and AI responses

---

## Task Summary

- **Total Tasks**: 70
- **Setup (Phase 1)**: 7 tasks
- **Foundational (Phase 2)**: 9 tasks
- **User Story 1 (Phase 3)**: 10 tasks
- **User Story 4 (Phase 4)**: 11 tasks
- **User Story 2 (Phase 5)**: 6 tasks
- **User Story 3 (Phase 6)**: 5 tasks
- **Testing (Phase 7)**: 5 tasks (optional)
- **Edge Cases (Phase 8)**: 9 tasks
- **Polish (Phase 9)**: 8 tasks

**MVP Scope**: 37 tasks (Setup + Foundational + US1 + US4)
**Full Feature**: 70 tasks

**Parallel Opportunities**:
- Phase 2: 4 parallel groups
- Phase 3 + 4: Can run in parallel (21 tasks total, ~11 tasks per developer)
- Phase 7: All 5 tests in parallel
- Phase 8: 3 parallel groups
- Phase 9: 3 parallel tasks

**Estimated Effort** (per plan.md):
- MVP (US1 + US4): 2-3 days
- Demographics (US2): +1 day
- Time patterns (US3): +1 day
- Edge cases + Polish: +1 day
- **Total**: 5-6 days for complete feature
