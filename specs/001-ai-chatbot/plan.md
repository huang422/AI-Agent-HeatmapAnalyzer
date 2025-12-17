# Implementation Plan: AI Chatbot Sidebar for Heatmap Data Analysis

**Branch**: `001-ai-chatbot` | **Date**: 2025-12-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot/spec.md`

## Summary

Add a collapsible AI chatbot sidebar to the right side of the Store Heatmap web application that enables users to query and analyze heatmap data through natural language conversation. The chatbot integrates with Ollama running qwen2.5:7b model locally on NVIDIA RTX 4080 (12GB) to provide intelligent analysis of demographic and time-based patterns in the data. The system converts currently displayed heatmap data (filtered by month, hour, day type) to JSON format with converted coordinates (TWD97 → WGS84) and passes this context to the AI model for accurate, data-driven responses in Traditional Chinese.

**Technical Approach**: Extend existing Vue 3 + FastAPI architecture with new backend API endpoints (`/api/chat/*`) that interface with local Ollama service, new frontend composable (`useChatbot.js`) for state management, and a responsive sidebar component (`ChatSidebar.vue`) that integrates seamlessly with existing dashboard without affecting current functionality. Reuse existing data caching (`data_loader.py`) and coordinate conversion (`coordinate_converter.py`) services to prepare JSON context for AI analysis.

## Technical Context

**Language/Version**:
- Backend: Python 3.9+ (existing)
- Frontend: JavaScript ES6+ with Vue 3 Composition API (existing)

**Primary Dependencies**:
- Backend: FastAPI 0.104+ (existing), Pandas 2.0+ (existing), Ollama Python client 0.1.0+ (NEW), Numba (existing for coordinate conversion)
- Frontend: Vue 3.3+ (existing), Axios 1.6+ (existing), Vite 4.5+ (existing)

**Storage**:
- Primary: In-memory data cache (Pandas DataFrame) loaded from CSV at startup (existing)
- Chat History: Frontend reactive state (Vue ref), session-only (no persistence)
- No new database required

**Testing**:
- Backend: pytest for unit/integration tests (existing pattern)
- Frontend: Vitest for component tests (existing tooling)
- Manual E2E testing for chatbot interaction flows

**Target Platform**:
- Development: Windows/Linux desktop with Vite dev server (frontend) + FastAPI dev server (backend)
- Production: PyInstaller bundled Windows .exe serving SPA as static files (existing deployment pattern)

**Project Type**: Web application (frontend + backend separation maintained)

**Performance Goals**:
- AI response time: <5 seconds (P95) for typical queries
- Chatbot UI open/close: <300ms animation duration
- Data context preparation: <100ms (reuse cached data)
- No degradation to existing heatmap/chart rendering performance

**Constraints**:
- GPU memory: <8GB VRAM usage by qwen2.5:7b model (12GB available)
- Network: localhost-only communication between frontend/backend/Ollama
- Backward compatibility: All existing features MUST remain fully functional
- Offline operation: Ollama runs locally, no external API calls

**Scale/Scope**:
- Data volume: ~2,881 records (existing dataset size)
- JSON context size per query: ~500KB-1MB (filtered subset)
- Chat history: Up to 10 message pairs (20 messages total) passed to AI for context
- Concurrent users: Single user (desktop application)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Frontend-Backend Separation ✅ PASS

**Compliance**:
- Frontend (`ChatSidebar.vue`, `useChatbot.js`) handles UI, user interactions, message display
- Backend (`/api/chat/*` endpoints) handles Ollama integration, data context preparation, business logic
- Communication via RESTful API (`POST /api/chat/message`, `GET /api/chat/health`)
- No AI model logic in frontend; no UI rendering in backend

**Justification**: Design maintains clear separation consistent with existing architecture.

### II. Data-Driven Visualization ✅ PASS

**Compliance**:
- Backend prepares data context (JSON with coordinates, demographics, time filters)
- Frontend receives structured chat response messages for rendering
- No raw data processing in chatbot frontend component
- Reuses existing backend data processing pipeline (`DataCache`, coordinate converter)

**Justification**: Chatbot responses driven by backend-prepared data context, consistent with existing data flow.

### III. Standalone Executable Packaging ✅ PASS (with external dependency)

**Compliance**:
- Backend chatbot routes packaged in existing PyInstaller .exe
- Frontend chatbot component bundled as static assets
- Single EXE launches web server serving chatbot-enabled SPA

**External Dependency**:
- Ollama must be installed separately (cannot bundle in .exe)
- Documented in README with clear setup instructions

**Justification**: Ollama is a system-level service (like GPU drivers) that users install once. Bundling would increase .exe size by ~500MB and complicate updates. This is acceptable for AI features requiring local ML infrastructure.

### IV. Interactive User Experience ✅ PASS

**Compliance**:
- Chatbot provides interactive Q&A about heatmap data
- Users can filter/explore via natural language queries
- Responsive design (desktop sidebar, mobile overlay)
- Real-time AI responses with loading indicators

**Justification**: Extends interactivity beyond visual filters to conversational data exploration.

### V. Performance & Responsiveness ✅ PASS

**Compliance**:
- AI response target: <5s (P95), meets requirement for responsive feel
- Chatbot UI animations: <300ms, maintains snappy interaction
- Existing visualization performance unchanged (no impact on heatmap/charts)
- Data context preparation reuses cached data (<100ms overhead)

**Justification**: Performance targets aligned with desktop application expectations. AI latency (2-5s) is acceptable for analytical queries (not real-time data entry).

### Technology Stack Constraints ✅ PASS (one addition)

**Compliance**:
- Frontend: Vue 3 Composition API (existing) ✅
- Backend: FastAPI with Python 3.9+ (existing) ✅
- Data Processing: Pandas (existing) ✅
- Packaging: PyInstaller (existing) ✅
- **NEW**: Ollama Python client for AI integration

**Justification**: Ollama client is a lightweight HTTP wrapper (~50KB) for interfacing with locally-running Ollama service. Does not introduce heavyweight frameworks. Necessary for AI chatbot requirement. Aligns with "modern tools" allowed in constitution for new capabilities.

### Quality Standards ✅ PASS

**Compliance**:
- Code in `backend/src/api/routes/chat.py`, `backend/src/services/ollama_service.py`, `frontend/src/components/chat/ChatSidebar.vue`
- API contracts in `specs/001-ai-chatbot/contracts/chat-api.yaml`
- Tests: Backend contract tests for new endpoints, frontend component tests optional
- Documentation: README updated with Ollama setup, API auto-documented via FastAPI

**Justification**: Follows existing project structure and quality standards.

### **FINAL VERDICT: ✅ ALL GATES PASSED**

Minor note: Ollama as external dependency is justified (see Section III). No constitution violations requiring complexity tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot/
├── spec.md              # Feature specification (already created)
├── plan.md              # This file
├── research.md          # Phase 0: Ollama integration patterns, system prompt design
├── data-model.md        # Phase 1: Chat message, data context, AI service status entities
├── quickstart.md        # Phase 1: Developer setup guide for Ollama + chatbot
├── contracts/           # Phase 1: OpenAPI schema for /api/chat/* endpoints
│   └── chat-api.yaml
└── checklists/
    └── requirements.md  # Validation checklist (already created)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── routes/
│   │       ├── data.py           # Existing heatmap API
│   │       ├── demographics.py   # Existing demographics API
│   │       └── chat.py           # NEW: Chat endpoints
│   ├── services/
│   │   ├── data_loader.py        # Existing data caching
│   │   ├── coordinate_converter.py # Existing TWD97→WGS84
│   │   ├── ollama_service.py     # NEW: Ollama client wrapper
│   │   └── data_exporter.py      # NEW: JSON context builder
│   ├── models/
│   │   └── location_data.py      # Existing data models
│   └── utils/
│       └── config.py             # Existing config (add OLLAMA_HOST)
└── tests/
    ├── integration/
    │   └── test_chat_api.py      # NEW: Chat endpoint tests
    └── unit/
        ├── test_ollama_service.py # NEW: Ollama service tests
        └── test_data_exporter.py  # NEW: Data export tests

frontend/
├── src/
│   ├── components/
│   │   ├── map/                  # Existing: HeatmapMap, MapTooltip
│   │   ├── charts/               # Existing: GenderChart, AgeChart
│   │   ├── controls/             # Existing: TimelineSlider, etc.
│   │   └── chat/                 # NEW: Chat components directory
│   │       └── ChatSidebar.vue   # NEW: Main chatbot UI
│   ├── composables/
│   │   ├── useHeatmapData.js     # Existing data fetching
│   │   ├── useDemographics.js    # Existing demographics
│   │   ├── useAutoplay.js        # Existing autoplay logic
│   │   └── useChatbot.js         # NEW: Chat state management
│   ├── services/
│   │   ├── api.js                # Existing axios instance (reused)
│   │   └── dataService.js        # Existing data service
│   ├── views/
│   │   └── Dashboard.vue         # MODIFIED: Include ChatSidebar
│   └── assets/
│       └── styles/
│           └── main.css          # MODIFIED: Add chat color variables
└── tests/
    └── components/
        └── ChatSidebar.spec.js   # NEW: Component tests (optional)
```

**Structure Decision**: Web application structure maintained. New chatbot functionality added as:
- Backend: New routes (`chat.py`) and services (`ollama_service.py`, `data_exporter.py`) in existing directories
- Frontend: New component directory (`components/chat/`) and composable (`useChatbot.js`) following established patterns
- Minimal modifications to existing files (Dashboard.vue includes new component, main.py registers new router, main.css adds variables)

## Complexity Tracking

> **No violations detected. This section intentionally left empty.**

All constitution checks passed. Ollama as external dependency (Section III) is documented but not classified as a violation since the constitution allows system-level dependencies for new capabilities (analogous to GPU drivers for visualization).

---

# Phase 0: Research & Design Decisions

## Research Summary

### 1. Ollama Integration Architecture

**Decision**: Use Ollama Python client library (`ollama` package) as HTTP wrapper around Ollama REST API

**Rationale**:
- Official client simplifies API interaction (vs raw HTTP requests)
- Handles connection pooling, retries, error handling automatically
- Minimal dependency footprint (~50KB)
- Well-documented, actively maintained by Ollama team

**Alternatives Considered**:
- **Direct HTTP with `requests`**: More control but reinvents error handling, connection management. Rejected due to maintenance burden.
- **LangChain Ollama integration**: Too heavyweight (adds 10+ MB dependencies), unnecessary abstractions for simple chat use case. Rejected for bloat.
- **llama-cpp-python**: Requires compiling models, complex setup. Ollama already handles this. Rejected for complexity.

**Implementation Pattern**:
```python
# backend/src/services/ollama_service.py
from ollama import Client

class OllamaService:
    def __init__(self, host="http://localhost:11434", model="qwen2.5:7b"):
        self.client = Client(host=host)
        self.model = model

    def generate_response(self, user_message, data_context, history):
        messages = [
            {"role": "system", "content": build_system_prompt(data_context)},
            *history,
            {"role": "user", "content": user_message}
        ]
        response = self.client.chat(model=self.model, messages=messages)
        return response['message']['content']
```

**Health Check Strategy**: Poll Ollama `/api/tags` endpoint on FastAPI startup and periodically in chatbot UI to detect service availability.

---

### 2. System Prompt Engineering for Data Analysis

**Decision**: Use structured system prompt with JSON data context, explicit field descriptions, and Traditional Chinese instructions

**Rationale**:
- qwen2.5:7b performs better with clear structure and examples
- JSON data context provides precise numerical facts, preventing hallucination
- Explicit field mapping (e.g., "sex_1 = male %, sex_2 = female %") reduces misinterpretation
- Traditional Chinese instructions improve response quality for target audience

**Prompt Template Structure**:
```
你是專業的數據分析助理，專門分析台灣地區人流熱力圖數據。

當前數據上下文（JSON格式）：
{
  "month": 202412,
  "hour": 8,
  "day_type": "平日",
  "total_records": 124,
  "summary": {
    "total_users": 5234.5,
    "avg_sex_1": 31.8,  // 男性百分比
    "avg_sex_2": 68.2,  // 女性百分比
    "top_locations": [...]
  }
}

欄位說明：
- lat/lon: WGS84經緯度座標
- avg_total_users: 該地點總平均使用者數
- sex_1/sex_2: 性別百分比（男性/女性）
- age_1~age_9: 年齡層百分比（<19歲, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-59, 60+）

回答規則：
1. 僅基於提供的數據回答，不得臆測
2. 提及地點時包含經緯度座標
3. 使用具體數字佐證分析
4. 保持簡潔專業的語氣
```

**Context Size Management**: Pass only filtered data (current month/hour/day_type) to keep context under 8K tokens. For "compare across time" queries (P3), use aggregated summaries instead of full records.

**Testing Strategy**: Build test question set covering P1-P3 user stories, manually verify accuracy against known data, iterate on prompt wording.

---

### 3. Data Context Preparation Strategy

**Decision**: Reuse existing `DataCache` and coordinate converter, create new `DataExporter` service to build JSON context on-demand per request

**Rationale**:
- `DataCache` already filters data by (month, hour, day_type) with O(1) lookup
- Coordinate conversion already performed at cache initialization (lat/lng columns exist)
- Incremental approach: Export only needed fields (23 fields from spec) vs full DataFrame
- On-demand generation avoids pre-computing/storing JSON for all 96 time combinations

**Data Flow**:
1. User asks question in chatbot
2. Frontend sends: `{ message, context: { month, hour, day_type }, history }`
3. Backend `data_exporter.export_to_json(month, hour, day_type)`:
   - Fetches from `DataCache.lookup_dict[(month, hour, day_type)]`
   - Selects 23 required columns (including pre-converted lat/lng)
   - Converts to list of dicts via `df.to_dict('records')`
   - Calculates summary statistics (total_users, avg_sex_*, top_locations)
4. Backend builds system prompt with JSON context
5. Ollama generates response

**Performance**: DataFrame filtering + to_dict is <100ms for typical ~200 records per filter. Negligible overhead vs AI inference (2-5s).

**Alternative Rejected**: Pre-generate all 96 JSONs at startup. Rejected because:
- Wastes memory (~50MB for all combinations)
- 90% of combinations never queried in typical session
- Cache invalidation complexity if data reloads

---

### 4. Frontend State Management Pattern

**Decision**: Create new composable `useChatbot.js` following existing pattern (`useHeatmapData`, `useDemographics`)

**Rationale**:
- Consistent with Vue 3 Composition API patterns in project
- Reactive state (`messages`, `isThinking`, `isConnected`) isolated from global scope
- Reuses existing `apiClient` (axios instance) for HTTP calls
- Enables future multi-instance chat (e.g., multiple chat windows) if needed

**State Structure**:
```javascript
// useChatbot.js
const messages = ref([
  { id: 1, role: 'system', content: '歡迎...', timestamp: Date.now() }
])
const isThinking = ref(false)
const isConnected = ref(false)

const sendMessage = async (userMessage) => {
  const context = getCurrentContext() // from useHeatmapData
  const response = await apiClient.post('/api/chat/message', {
    message: userMessage,
    context,
    history: messages.value.slice(-10)
  })
  messages.value.push(response.data)
}
```

**Context Integration**: `useChatbot` imports `useHeatmapData` to access `currentMonth`, `currentHour`, `currentDayType`. This creates one-way dependency (chat depends on heatmap state) but avoids circular deps.

**Alternative Rejected**: Global Pinia store. Rejected because:
- Project doesn't use Pinia currently (would introduce new dependency)
- Chatbot state is feature-specific, not truly global
- Composable pattern sufficient for this scale

---

### 5. Responsive UI Design Strategy

**Decision**: Desktop = 350px fixed-width sidebar pushing main content left; Mobile = full-screen overlay with backdrop

**Rationale**:
- Desktop users benefit from side-by-side view (map + chat)
- Mobile screen too narrow for split view (375px width - 350px sidebar = 25px map unusable)
- Overlay pattern familiar to mobile users (similar to menus, modals)
- CSS transitions provide smooth slide-in/fade-in animations

**Breakpoints** (matching existing project):
- Desktop: ≥1024px → sidebar width 350px, main content `width: calc(100% - 350px)`
- Tablet: 768-1023px → sidebar width 320px (slightly narrower)
- Mobile: <768px → sidebar width 100vw, `position: fixed`, backdrop overlay

**Animation Timing**:
- Slide transition: `transform: translateX(0)` with `transition: 300ms ease-in-out`
- Backdrop fade: `opacity: 0.5` with `transition: 200ms ease`

**Z-index Layers** (avoid conflicts):
- Map controls: z-index 10 (existing)
- Tooltips: z-index 50 (existing)
- Chat sidebar: z-index 100 (above map, below modals)
- Chat backdrop: z-index 99 (behind sidebar)

**Alternative Rejected**: Bottom drawer on mobile. Rejected because:
- Harder to read long AI responses (limited height)
- Requires different component logic for mobile vs desktop
- Overlay pattern simpler to implement and maintain

---

### 6. Error Handling & Graceful Degradation

**Decision**: Multi-layered error handling with user-friendly messages at each point of failure

**Error Scenarios & Handling**:

| Scenario | Detection | User Feedback | Recovery |
|----------|-----------|---------------|----------|
| Ollama not running | `/api/chat/health` returns 503 | "⚠ AI 服務離線" status badge, disable input | Auto-retry health check every 30s |
| Model not loaded | Ollama client throws error | "模型未載入，請執行 ollama pull qwen2.5:7b" | Manual user action required |
| Network timeout | Axios timeout (30s) | "回應超時，請重試" with retry button | User clicks retry, resends same message |
| GPU OOM | Ollama returns 500 | "GPU 記憶體不足，請重啟 Ollama" | Manual Ollama restart |
| Empty data context | `DataExporter` returns 0 records | AI prompt includes "無數據可分析" flag | AI responds "當前條件下無可用數據" |
| Rapid requests | Backend detects concurrent request | 429 "請等待當前問題處理完成" | Frontend disables send button while `isThinking=true` |

**Logging Strategy**:
- Backend: Log Ollama errors to console with full stack trace (for debugging)
- Frontend: Log API errors to console.error (for developer tools)
- User-facing messages: Plain Traditional Chinese, no technical jargon

**Alternative Rejected**: Silent failures with generic "錯誤" message. Rejected because:
- Users can't self-diagnose (e.g., forgot to start Ollama)
- Increases support burden
- Poor UX for edge cases that will definitely occur

---

### 7. Testing Strategy

**Backend Testing**:
- **Unit Tests** (`test_ollama_service.py`):
  - Mock Ollama client responses
  - Test system prompt building logic
  - Test error handling (connection refused, timeout, invalid response)
- **Unit Tests** (`test_data_exporter.py`):
  - Test JSON export with sample DataCache
  - Verify coordinate conversion preserved
  - Test empty data handling
- **Integration Tests** (`test_chat_api.py`):
  - Test `/api/chat/message` with mock Ollama
  - Verify request validation (max length, required fields)
  - Test timeout behavior

**Frontend Testing**:
- **Component Tests** (`ChatSidebar.spec.js`) - OPTIONAL for MVP:
  - Test open/close behavior
  - Test message rendering
  - Test send button disable state
- **Manual E2E Testing** - REQUIRED:
  - Test all P1 acceptance scenarios (open, ask, close, loading indicator)
  - Test responsive design at 3 breakpoints (1920px, 768px, 375px)
  - Test existing features while chatbot open (playback, filters, charts)
  - Test error states (Ollama offline, timeout, no data)

**Rationale**: Focus testing on backend business logic (data export, Ollama integration) where bugs have highest impact. Frontend component tests optional since ChatSidebar is presentational with simple state (messages array). Manual E2E testing more efficient for UI verification in MVP phase.

---

# Phase 1: Data Models & API Contracts

## Data Model Specification

### Entity: ChatMessage

**Purpose**: Represents a single message in the conversation history

**Fields**:
- `id` (integer): Unique message identifier, auto-generated timestamp-based ID
- `role` (enum): Message sender type
  - Values: `"user"`, `"assistant"`, `"system"`
  - Validation: Must be one of the three values
- `content` (string): Message text content
  - Validation: Non-empty, max 10,000 characters (AI responses can be longer than user input)
- `timestamp` (integer): Unix timestamp in milliseconds when message was created
  - Validation: Positive integer, auto-generated on creation

**Relationships**:
- Part of conversation history (ordered list)
- No persistent storage (session-only in frontend state)

**State Transitions**: Immutable once created (messages not edited or deleted in MVP)

**Example**:
```json
{
  "id": 1734480123456,
  "role": "user",
  "content": "哪個時段最繁忙？",
  "timestamp": 1734480123456
}
```

---

### Entity: DataContext

**Purpose**: Encapsulates heatmap data and filter conditions passed to AI for analysis

**Fields**:
- `month` (integer): YYYYMM format (e.g., 202412)
  - Validation: Must exist in available months from DataCache metadata
- `hour` (integer): Hour of day (0-23)
  - Validation: 0 ≤ hour ≤ 23
- `day_type` (string): Day classification
  - Values: `"平日"` (weekday) or `"假日"` (weekend/holiday)
  - Validation: Must be one of the two values
- `data` (array of HeatmapDataRecord): Filtered data records
  - Validation: Can be empty array (no data for filter combination)
- `summary` (object): Pre-computed statistics for AI context
  - Fields:
    - `total_records` (integer): Number of data points
    - `total_users` (float): Sum of avg_total_users across all records
    - `avg_sex_1` (float): Average male percentage
    - `avg_sex_2` (float): Average female percentage
    - `top_locations` (array): Top 5 locations by total_users with lat/lon

**Relationships**:
- Contains multiple HeatmapDataRecord entities
- Generated on-demand per chat request by DataExporter
- Embedded in AI system prompt

**Validation Rules**:
- If `data` is empty, `summary.total_records` must be 0
- All summary averages computed only if `total_records > 0`

**Example**:
```json
{
  "month": 202412,
  "hour": 8,
  "day_type": "平日",
  "data": [ /* array of HeatmapDataRecord */ ],
  "summary": {
    "total_records": 124,
    "total_users": 5234.5,
    "avg_sex_1": 31.8,
    "avg_sex_2": 68.2,
    "top_locations": [
      {"lat": 25.033, "lon": 121.543, "total_users": 145.2}
    ]
  }
}
```

---

### Entity: HeatmapDataRecord

**Purpose**: Single data point representing people flow at a specific location and time

**Fields** (23 fields as specified):
- `month` (integer): YYYYMM format
- `gx` (integer): TWD97 TM2 grid X coordinate
- `gy` (integer): TWD97 TM2 grid Y coordinate
- `lat` (float): WGS84 latitude (converted from gx/gy)
  - Validation: 21.0 ≤ lat ≤ 26.0 (Taiwan bounds)
- `lon` (float): WGS84 longitude (converted from gx/gy)
  - Validation: 119.0 ≤ lon ≤ 122.0 (Taiwan bounds)
- `hour` (integer): 0-23
- `day_type` (string): "平日" or "假日"
- `avg_total_users` (float): Total average user count
  - Validation: ≥ 0
- `avg_users_under_10min` (float): Users with <10 min dwell time
  - Validation: ≥ 0
- `avg_users_10_30min` (float): Users with 10-30 min dwell time
  - Validation: ≥ 0
- `avg_users_over_30min` (float): Users with >30 min dwell time
  - Validation: ≥ 0
- `sex_1` (float): Male percentage (0-100)
  - Validation: 0 ≤ sex_1 ≤ 100
- `sex_2` (float): Female percentage (0-100)
  - Validation: 0 ≤ sex_2 ≤ 100, sex_1 + sex_2 ≈ 100
- `age_1` through `age_9` (float): Age group percentages (0-100)
  - age_1: <19, age_2: 20-24, age_3: 25-29, age_4: 30-34, age_5: 35-39, age_6: 40-44, age_7: 45-49, age_8: 50-59, age_9: 60+
  - Validation: Each 0 ≤ age_X ≤ 100
- `age_other` (float): Unclassified age percentage (0-100)
  - Validation: Sum of all age percentages ≈ 100

**Relationships**:
- Source: Loaded from CSV via DataCache
- Coordinate conversion applied via existing `coordinate_converter.py`
- Many records aggregated into one DataContext per chat request

**Example**:
```json
{
  "month": 202412,
  "gx": 7165,
  "gy": 7152,
  "lat": 25.033311,
  "lon": 121.543653,
  "hour": 8,
  "day_type": "平日",
  "avg_total_users": 45.2,
  "avg_users_under_10min": 12.3,
  "avg_users_10_30min": 18.7,
  "avg_users_over_30min": 14.2,
  "sex_1": 31.8,
  "sex_2": 68.2,
  "age_1": 1.2,
  "age_2": 5.4,
  "age_3": 18.7,
  "age_4": 24.1,
  "age_5": 16.8,
  "age_6": 12.3,
  "age_7": 10.9,
  "age_8": 7.6,
  "age_9": 2.5,
  "age_other": 0.5
}
```

---

### Entity: AIServiceStatus

**Purpose**: Represents current state of Ollama service connection and model availability

**Fields**:
- `status` (enum): Connection state
  - Values: `"connected"`, `"disconnected"`, `"error"`
- `model_loaded` (boolean): Whether qwen2.5:7b model is available
- `ollama_version` (string, optional): Ollama version string (e.g., "0.1.17")
- `available_models` (array of strings, optional): List of loaded models
- `error_message` (string, optional): Human-readable error if status is "error"
- `last_checked` (integer): Unix timestamp of last health check

**Relationships**:
- Queried by frontend via `/api/chat/health` endpoint
- Determines chatbot UI state (enabled/disabled input, status indicator color)

**State Transitions**:
- `disconnected` → `connected`: When Ollama service starts
- `connected` → `disconnected`: When Ollama stops or network unreachable
- `connected` → `error`: When API returns unexpected error
- Any state → `connected`: After successful health check

**Example**:
```json
{
  "status": "connected",
  "model_loaded": true,
  "ollama_version": "0.1.17",
  "available_models": ["qwen2.5:7b", "llama2:7b"],
  "error_message": null,
  "last_checked": 1734480200000
}
```

---

## API Contract: Chat Endpoints

### POST /api/chat/message

**Purpose**: Send user message and receive AI-generated response based on current heatmap data context

**Request**:
```yaml
method: POST
path: /api/chat/message
headers:
  Content-Type: application/json
body:
  type: object
  required: [message, context]
  properties:
    message:
      type: string
      minLength: 1
      maxLength: 500
      description: User's question in Traditional Chinese
    context:
      type: object
      required: [month, hour, day_type]
      properties:
        month:
          type: integer
          description: YYYYMM format (e.g., 202412)
        hour:
          type: integer
          minimum: 0
          maximum: 23
        day_type:
          type: string
          enum: ["平日", "假日"]
    history:
      type: array
      items:
        type: object
        properties:
          role:
            type: string
            enum: [user, assistant, system]
          content:
            type: string
          timestamp:
            type: integer
      maxItems: 20
      description: Recent conversation history (last 10 message pairs)
```

**Success Response (200)**:
```yaml
body:
  type: object
  properties:
    response:
      type: string
      description: AI-generated answer in Traditional Chinese
    timestamp:
      type: integer
      description: Unix timestamp of response generation
    model:
      type: string
      description: Model used (e.g., "qwen2.5:7b")
    tokens_used:
      type: integer
      description: Approximate token count for inference
```

**Error Responses**:
- **400 Bad Request**: Invalid request body (missing fields, validation failure)
  ```json
  {"detail": "Message length exceeds 500 characters"}
  ```
- **503 Service Unavailable**: Ollama service not running or model not loaded
  ```json
  {"detail": "Ollama service is not available. Please start Ollama and ensure qwen2.5:7b is pulled."}
  ```
- **500 Internal Server Error**: Model inference failed or unexpected error
  ```json
  {"detail": "Failed to generate response: <error details>"}
  ```

**Example**:
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "哪個時段最繁忙？",
    "context": {
      "month": 202412,
      "hour": 8,
      "day_type": "平日"
    },
    "history": []
  }'

# Response:
{
  "response": "根據12月平日早上8點的數據，此時段總使用者數為5234.5人...",
  "timestamp": 1734480123456,
  "model": "qwen2.5:7b",
  "tokens_used": 245
}
```

---

### GET /api/chat/health

**Purpose**: Check Ollama service availability and model status

**Request**:
```yaml
method: GET
path: /api/chat/health
headers: {}
```

**Success Response (200)**:
```yaml
body:
  type: object
  properties:
    status:
      type: string
      enum: [ok, degraded]
      description: Overall service status
    ollama_status:
      type: string
      enum: [connected, disconnected, error]
    model:
      type: string
      description: Expected model name
    model_loaded:
      type: boolean
      description: Whether qwen2.5:7b is available
    gpu_available:
      type: boolean
      nullable: true
      description: GPU acceleration status (true if model loaded)
    error:
      type: string
      nullable: true
      description: Error message if any
    timestamp:
      type: string
      format: date-time
      description: ISO 8601 timestamp of health check
```

**Example**:
```bash
curl http://localhost:8000/api/chat/health

# Ollama running:
{
  "status": "ok",
  "ollama_status": "connected",
  "model": "qwen2.5:7b",
  "model_loaded": true,
  "gpu_available": true,
  "error": null,
  "timestamp": "2025-12-17T10:30:00Z"
}

# Ollama offline:
{
  "status": "degraded",
  "ollama_status": "disconnected",
  "model": "qwen2.5:7b",
  "model_loaded": false,
  "gpu_available": null,
  "error": "Cannot connect to Ollama at http://localhost:11434",
  "timestamp": "2025-12-17T10:30:00Z"
}
```

---

### GET /api/chat/context

**Purpose**: Retrieve current data context for debugging/testing (optional endpoint)

**Request**:
```yaml
method: GET
path: /api/chat/context
query parameters:
  month:
    type: integer
    required: false
  hour:
    type: integer
    required: false
    minimum: 0
    maximum: 23
  day_type:
    type: string
    required: false
    enum: ["平日", "假日"]
```

**Success Response (200)**:
```yaml
body:
  type: object
  properties:
    metadata:
      type: object
      properties:
        total_records:
          type: integer
        query:
          type: object
          description: Filter parameters used
    sample_data:
      type: array
      items:
        $ref: '#/components/schemas/HeatmapDataRecord'
      maxItems: 50
      description: First 50 records (or all if fewer)
    note:
      type: string
      description: Informational message if data truncated
```

**Example**:
```bash
curl http://localhost:8000/api/chat/context?month=202412&hour=8&day_type=平日

{
  "metadata": {
    "total_records": 124,
    "query": {
      "month": 202412,
      "hour": 8,
      "day_type": "平日"
    }
  },
  "sample_data": [ /* first 50 HeatmapDataRecord objects */ ],
  "note": "Showing 50 of 124 records"
}
```

---

## Developer Quickstart Guide

### Prerequisites

1. **Python 3.9+** with pip installed
2. **Node.js 18+** with npm installed
3. **NVIDIA GPU** with CUDA-capable driver (525.60.13+)
4. **Ollama** installed (version 0.1.0+)

### First-Time Setup

#### 1. Install Ollama

**Linux**:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows**:
Download installer from https://ollama.com/download/windows

**Verify Installation**:
```bash
ollama --version
# Expected: ollama version 0.1.17 (or higher)
```

#### 2. Pull qwen2.5:7b Model

```bash
ollama pull qwen2.5:7b
# This downloads ~4.7GB model to ~/.ollama/models/
# First-time download takes 5-15 minutes depending on connection speed
```

**Verify Model**:
```bash
ollama list
# Expected output:
# NAME              ID           SIZE    MODIFIED
# qwen2.5:7b        abc123...    4.7 GB  2 minutes ago
```

#### 3. Start Ollama Service

**Linux/Mac**:
```bash
ollama serve
# Starts server on http://localhost:11434
# Keep this terminal open while developing
```

**Windows**:
Ollama runs as background service automatically. Check status:
```powershell
curl http://localhost:11434/api/tags
# Should return JSON list of models
```

#### 4. Clone and Setup Project

```bash
cd /path/to/store_heatmap
git checkout 001-ai-chatbot  # Switch to feature branch

# Backend setup
cd backend
pip install -r requirements.txt  # Includes new 'ollama' package

# Frontend setup
cd ../frontend
npm install  # No new packages (reuses existing Vue/Axios)
```

#### 5. Verify Ollama Integration

**Test Python client**:
```bash
cd backend
python -c "
from ollama import Client
client = Client()
response = client.chat(model='qwen2.5:7b', messages=[
    {'role': 'user', 'content': '你好'}
])
print(response['message']['content'])
"
# Expected: Traditional Chinese greeting response
```

### Running in Development

**Terminal 1 - Ollama** (if not auto-started):
```bash
ollama serve
```

**Terminal 2 - Backend**:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
# Watches for changes, auto-reloads
```

**Terminal 3 - Frontend**:
```bash
cd frontend
npm run dev
# Vite dev server on http://localhost:5173
# Proxies /api to backend:8000
```

**Access Application**:
Open browser to http://localhost:5173

### Testing Chatbot

1. Click 🤖 button on right side of screen
2. Chatbot sidebar should slide in
3. Status indicator should show "● 已連線" (green)
4. Type test question: "哪個時段最繁忙？"
5. Verify AI responds with data-driven answer in ~2-5 seconds

**Troubleshooting**:

| Issue | Cause | Solution |
|-------|-------|----------|
| Status shows "⚠ 離線" | Ollama not running | Run `ollama serve` or restart Ollama Windows service |
| "Model not found" error | qwen2.5:7b not pulled | Run `ollama pull qwen2.5:7b` |
| Timeout after 30s | GPU busy or model slow | Check `nvidia-smi` for GPU usage, close other GPU apps |
| Console error "ECONNREFUSED" | Backend not started | Start FastAPI with `uvicorn src.main:app --reload` |

### Code Locations

**New Backend Files**:
- `backend/src/api/routes/chat.py` - Chat API endpoints
- `backend/src/services/ollama_service.py` - Ollama client wrapper
- `backend/src/services/data_exporter.py` - JSON context builder

**New Frontend Files**:
- `frontend/src/components/chat/ChatSidebar.vue` - Chatbot UI
- `frontend/src/composables/useChatbot.js` - Chat state management

**Modified Files**:
- `backend/src/main.py` - Registers chat router
- `frontend/src/views/Dashboard.vue` - Includes ChatSidebar component
- `frontend/src/assets/styles/main.css` - Chat color variables

### Running Tests

**Backend Tests**:
```bash
cd backend
pytest tests/unit/test_ollama_service.py -v
pytest tests/unit/test_data_exporter.py -v
pytest tests/integration/test_chat_api.py -v
```

**Frontend Tests** (optional):
```bash
cd frontend
npm run test -- ChatSidebar.spec.js
```

### Packaging for Distribution

Build standalone .exe (existing process, chatbot bundled automatically):
```bash
cd backend
pyinstaller --onefile --add-data "../frontend/dist:frontend/dist" src/main.py
# Output: dist/main.exe

# Users must install Ollama separately (documented in README)
```

---

## Next Steps

After Phase 1 completion:

1. **Run `/speckit.tasks`** to generate detailed implementation tasks from this plan
2. **Review contracts** in `contracts/chat-api.yaml` with frontend/backend developers
3. **Set up test environment** with Ollama running and model pulled
4. **Begin implementation** following task order (backend services → API routes → frontend composable → UI component)
5. **Iterate on system prompt** based on test query results

**Estimated Implementation Time**: 2-3 days for P1 features (basic conversation + UI), 1-2 days for P2-P3 (demographics, time patterns)
