# Feature Specification: AI Chatbot Sidebar for Heatmap Data Analysis

**Feature Branch**: `001-ai-chatbot`
**Created**: 2025-12-17
**Status**: Draft
**Input**: User description: "1. Add collapsible AI agent chatbot on the right side of the web page, connecting to open-source model running on NVIDIA 4080 12GB, reading data to allow users to chat with AI and analyze data correctly. 2. Use ollama run qwen2.5:7b model. 3. Organize data into JSON file with only fields currently used in the project. Convert gx, gy to lat/lon using existing coordinate converter. JSON fields: month, gx, gy, lat, lon, hour, day_type, avg_total_users, avg_users_under_10min, avg_users_10_30min, avg_users_over_30min, sex_1, sex_2, age_1-9, age_other. 4. Preserve all existing frontend and backend functionality without breaking current features."

## User Scenarios & Testing

### User Story 1 - Basic AI Conversation (Priority: P1)

Users can open a chatbot sidebar on the right side of the page, ask questions about the heatmap data in natural language, and receive AI-powered analysis based on the currently displayed data context.

**Why this priority**: This is the core functionality that provides immediate user value. Users can query data insights through conversation without manually filtering and analyzing, significantly lowering the barrier to entry.

**Independent Test**: Can be fully tested by opening the chatbot, typing a question (e.g., "What time period has the most users?"), and receiving an AI response. This delivers immediate data insight value.

**Acceptance Scenarios**:

1. **Given** user is viewing the heatmap page, **When** clicking the AI chatbot button on the right side, **Then** the chatbot sidebar slides in from the right without blocking the main map area
2. **Given** chatbot is open, **When** user types "How many users are shown in the current time period?" and submits, **Then** AI responds with actual statistics based on the currently selected month, hour, and day type
3. **Given** user is chatting with AI, **When** clicking the close button or outside the chatbot area, **Then** the chatbot collapses and the map returns to original width
4. **Given** AI is processing a response, **When** user waits for the response, **Then** a clear "thinking" or loading indicator is displayed

---

### User Story 2 - Demographic Analysis Queries (Priority: P2)

Users can ask demographic-specific questions (gender, age distribution), and AI can analyze the data to provide insights such as "Which areas have higher female user percentages?" or "Where do young people mainly gather?"

**Why this priority**: This is an advanced analysis feature that enables users to deeply understand demographic distribution patterns, highly valuable for business decisions, but requires the basic conversation feature (P1) to work first.

**Independent Test**: Can be tested by asking "Where do 20-30 year old users mainly spend time?" to verify if AI can correctly parse age fields (age_2, age_3) and provide geographic location information.

**Acceptance Scenarios**:

1. **Given** chatbot is open with current data context, **When** user asks "What is the percentage of male and female users?", **Then** AI responds with sex_1 and sex_2 percentage statistics under current filter conditions
2. **Given** user wants to understand specific age group distribution, **When** typing "Which age group has the most people?", **Then** AI analyzes all age_1 through age_9 fields and reports the age group with highest percentage and its value
3. **Given** user asks about geographic distribution, **When** asking "What are the top three areas with highest female user percentage?", **Then** AI responds with latitude/longitude coordinates (lat, lon) and corresponding sex_2 percentages

---

### User Story 3 - Time-based Pattern Discovery (Priority: P3)

Users can ask about cross-time patterns such as "What's the difference between weekday and weekend traffic?" or "Which time of day is busiest?", and AI can compare data across different time conditions.

**Why this priority**: This is a more advanced analysis feature requiring comparison across multiple data slices. While valuable, it has lower priority compared to answering current data questions (P1, P2).

**Independent Test**: Can be tested by asking "Compare user traffic between 8 AM and 8 PM" to verify if AI can access different time period data and perform comparative analysis.

**Acceptance Scenarios**:

1. **Given** data contains multiple time period records, **When** user asks "Which hour has the highest total user count?", **Then** AI responds with the specific hour (0-23) and corresponding sum of avg_total_users
2. **Given** user wants to compare weekdays and weekends, **When** typing "Is there a big difference in user count between weekdays and weekends?", **Then** AI compares statistics for day_type='平日' and '假日' and provides insights
3. **Given** user asks about dwell time patterns, **When** asking "How long do most users stay?", **Then** AI analyzes the three fields avg_users_under_10min, avg_users_10_30min, avg_users_over_30min and reports the primary dwell time range

---

### User Story 4 - Sidebar UI Interaction (Priority: P1)

Users can smoothly open and close the chatbot, which works properly on different devices (desktop, tablet, mobile) without affecting existing map and chart functionality.

**Why this priority**: Basic UI functionality must be stable and reliable as it's the prerequisite for all other features. This is co-P1 with basic conversation because without stable UI, conversation features cannot be used.

**Independent Test**: Can be tested by opening/closing the chatbot at different screen sizes and verifying that the map, charts, timeline, and other existing features work normally.

**Acceptance Scenarios**:

1. **Given** user on desktop browser (width ≥1024px), **When** opening chatbot, **Then** chatbot width is 350px, main content area width reduces accordingly, map and charts adjust but remain usable
2. **Given** user on mobile browser (width <768px), **When** opening chatbot, **Then** chatbot displays as full-screen overlay with semi-transparent backdrop
3. **Given** chatbot is open, **When** user operates existing features (switch month, adjust timeline, view charts), **Then** all existing features work normally, unaffected by chatbot
4. **Given** chatbot is collapsed and new AI message arrives, **When** message is delivered, **Then** chatbot button displays unread message count badge

---

### Edge Cases

- **AI Service Offline**: When Ollama service is not running or model is not loaded, chatbot should display clear offline status indicator (e.g., "⚠ AI Service Offline") and disable message input to avoid user confusion
- **Overly Long Message Input**: When user types more than 500 characters, system should limit input or display character count warning to avoid sending oversized requests
- **AI Response Timeout**: When AI processing time exceeds 30 seconds, should display timeout error message and allow user to retry
- **No Data to Analyze**: When current filter conditions return no data (e.g., certain month/hour combination has no records), AI should clearly state "No data available under current conditions" rather than speculate
- **Rapid Successive Questions**: When user submits new question before previous one is answered, system should queue processing or prompt "Please wait for current question to complete"
- **GPU Memory Insufficient**: When GPU VRAM is insufficient to run model (though 12GB should be adequate for qwen2.5:7b), system should display appropriate error message and suggest restarting Ollama service
- **Missing Data Fields**: When some records lack specific fields (e.g., some locations have no age distribution data), AI should answer based on available data and note data limitations
- **Chatbot Conflicts with Existing UI Elements**: At certain screen sizes, chatbot may overlap with map controls, legends, or tooltips; should ensure z-index is set correctly to avoid blocking important information

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a collapsible chatbot UI component on the right side of the page, defaulting to collapsed state, expandable/collapsible via button or icon
- **FR-002**: Chatbot MUST integrate with locally-running Ollama service, using qwen2.5:7b model for natural language understanding and response generation
- **FR-003**: System MUST convert currently displayed heatmap data (filtered by user-selected month, hour, day type) to JSON format, including these fields: month, gx, gy, lat, lon, hour, day_type, avg_total_users, avg_users_under_10min, avg_users_10_30min, avg_users_over_30min, sex_1, sex_2, age_1 through age_9, age_other
- **FR-004**: System MUST use existing coordinate conversion program to convert gx, gy (TWD97 grid coordinates) to lat, lon (WGS84 latitude/longitude) during data conversion
- **FR-005**: AI MUST be able to read and analyze provided JSON data context, answering user questions based on actual data, without fabricating or speculating non-existent data
- **FR-006**: Users MUST be able to input natural language questions in Traditional Chinese in the chatbot, and AI MUST respond in Traditional Chinese
- **FR-007**: System MUST display loading or "thinking" visual indicator while AI processes questions, informing users the system is working
- **FR-008**: Chatbot MUST display conversation history including user messages and AI responses, automatically scrolling to latest message
- **FR-009**: System MUST detect Ollama service connection status and display connected/offline status indicator in chatbot
- **FR-010**: Opening and closing chatbot MUST NOT affect existing map, charts, timeline, filters, and all other existing functionality
- **FR-011**: System MUST provide responsive design for different screen sizes, displaying as sidebar (~350px) on desktop and full-screen overlay on mobile
- **FR-012**: System MUST limit user message input length per submission (recommended 500 characters max) to avoid oversized requests
- **FR-013**: System MUST set timeout mechanism for AI responses (recommended 30 seconds), displaying error message after timeout and allowing retry
- **FR-014**: System MUST clearly inform user when no data is available (no records under current filter conditions) rather than letting AI answer based on empty dataset
- **FR-015**: AI responses mentioning geographic locations MUST include latitude/longitude coordinates (lat, lon) for user location reference

### Key Entities

- **Chat Message**: Represents a conversation record containing role (user/assistant/system), content (text), and timestamp. Messages form conversation history in chronological order
- **Data Context**: Current heatmap display's filter conditions and corresponding data, including month, hour, day type, and all data records matching conditions (JSON format). This context is passed to AI model each time user asks a question
- **Heatmap Data Record**: Single geographic location's people flow statistics under specific time conditions, including coordinates (gx, gy, lat, lon), time information (month, hour, day_type), user counts (total and categorized by dwell time), and demographics (gender and age distribution)
- **AI Service Status**: Ollama service running status, including connection state (connected/disconnected), model loading status, and error messages (if any). Affects chatbot availability

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can open and close chatbot within 1 second, with smooth animations without stuttering
- **SC-002**: AI response time is less than 5 seconds in 95% of cases (for data analysis questions under current filter conditions)
- **SC-003**: AI response accuracy reaches 90% or above (based on test question set, verifying if AI responses match actual data)
- **SC-004**: Existing feature performance (map interaction, chart updates, timeline playback, filters) is not affected by chatbot functionality (performance degradation <10%)
- **SC-005**: Chatbot displays and operates normally on three screen sizes: desktop (≥1024px), tablet (768-1023px), mobile (<768px)
- **SC-006**: When Ollama service is offline, users see clear offline status prompt within 2 seconds, rather than continuous waiting or error messages
- **SC-007**: Users can ask at least 10 consecutive questions without refreshing the page, with conversation history correctly saved and displayed
- **SC-008**: Coordinate conversion accuracy reaches 100% (gx, gy to lat, lon conversion results match coordinates displayed on existing map)

## Assumptions

- **Assumption 1**: Ollama is installed on user's local environment, and qwen2.5:7b model has been successfully downloaded (via `ollama pull qwen2.5:7b`)
- **Assumption 2**: Ollama service runs on `localhost:11434` by default, unless user has custom configuration
- **Assumption 3**: User's NVIDIA RTX 4080 GPU (12GB VRAM) is sufficient to run qwen2.5:7b model without additional quantization or optimization
- **Assumption 4**: Users primarily converse in Traditional Chinese, and AI model (qwen2.5:7b) has good understanding and generation capabilities for Traditional Chinese
- **Assumption 5**: Existing project's coordinate conversion program (TWD97 gx/gy to WGS84 lat/lon) is verified correct and stable, can be directly reused
- **Assumption 6**: Users don't need conversation history to persist across sessions (clearing conversation records after closing webpage is acceptable)
- **Assumption 7**: Chatbot design language (colors, fonts, spacing) should be consistent with existing webpage style, using existing CSS variables and style system
- **Assumption 8**: As single-user desktop application (or local webpage), no need to consider multi-user concurrency or permission control
- **Assumption 9**: Data volume (~2,881 records) when converted to JSON is approximately 500KB-1MB, sufficient to pass to AI model as context in each request
- **Assumption 10**: Users have basic knowledge of using Ollama or can start Ollama service following documentation instructions

## Out of Scope

- **Voice Input/Output**: This phase does not support voice conversation features, limited to text input and responses only
- **Multi-language Support**: Only supports Traditional Chinese, does not include English or other language switching
- **Conversation History Export**: Does not provide functionality to export conversation records to PDF, TXT, or other formats
- **AI Actively Modifying Map State**: AI cannot directly control map filters or timeline (e.g., when user says "Show 8 AM map", AI only answers without automatically switching map state)
- **Advanced AI Features**: Does not include chart generation, predictive analysis, anomaly detection or other advanced analysis features, limited to descriptive statistics and data queries only
- **Conversation History Search**: Does not provide functionality to search past conversation records
- **Multi-model Switching**: Only supports qwen2.5:7b, does not provide option to switch to other Ollama models
- **Real-time Streaming Responses**: Initial version AI responses return complete text at once, does not include word-by-word streaming display (can be future enhancement)
- **User Authentication**: As local application, does not include login, permissions, or multi-user management features
- **Performance Monitoring Dashboard**: Does not provide real-time monitoring interface for technical metrics like GPU utilization, inference time, etc.

## Dependencies

- **Ollama**: Must be installed and running on local machine, version 0.1.0 or above recommended
- **qwen2.5:7b Model**: Must be pre-downloaded via `ollama pull qwen2.5:7b`
- **NVIDIA GPU Driver**: Requires CUDA-capable NVIDIA driver (recommended 525.60.13 or above) to enable GPU acceleration
- **Existing Coordinate Converter**: Depends on existing TWD97 to WGS84 coordinate conversion logic in project (located at backend/src/services/coordinate_converter.py)
- **Existing Data Loading Service**: Depends on existing data caching and filtering logic in project (located at backend/src/services/data_loader.py)
- **Existing Frontend Framework**: Uses project's existing Vue 3 Composition API, Axios, OpenLayers, ECharts and other frontend tech stack, without introducing new major frameworks

## Non-Functional Requirements

- **Performance**: AI response time should be within 5 seconds (P95), chatbot open/close animations should complete within 300 milliseconds
- **Reliability**: When Ollama service is abnormal, system should gracefully degrade (display error message but not crash), existing features unaffected
- **Compatibility**: Chatbot functionality should work normally on latest versions of mainstream browsers like Chrome, Firefox, Edge
- **Responsive Design**: UI must adapt to three main screen sizes: desktop (≥1024px), tablet (768-1023px), mobile (<768px)
- **Accessibility**: Chatbot should support keyboard navigation (Tab, Enter, Escape keys), buttons and input fields should have appropriate ARIA labels
- **Resource Usage**: GPU memory usage should be controlled within 8GB (reserving sufficient space for qwen2.5:7b), should not interfere with other GPU applications
- **Error Handling**: All API errors, network errors, timeout errors should have clear user-friendly messages (not technical error stacks)
- **Security**: User input should undergo basic validation (length limits, special character filtering) to avoid injection attacks or system abuse

## Risk Assessment

- **Risk 1 - Ollama Service Stability**: Ollama may fail to operate normally for various reasons (service crash, model loading failure, GPU driver issues). **Mitigation**: Implement health check mechanism, regularly detect Ollama status, provide clear error messages and restart guidance
- **Risk 2 - Poor AI Response Quality**: qwen2.5:7b may misunderstand certain questions or provide meaningless answers. **Mitigation**: Design clear system prompts, provide structured data context, conduct multiple rounds of testing and prompt optimization in early stages
- **Risk 3 - Breaking Existing Features**: Adding chatbot may cause CSS conflicts, JavaScript errors, or performance degradation. **Mitigation**: Use isolated CSS scopes (scoped styles), independent state management (composables), and conduct comprehensive regression testing
- **Risk 4 - Performance Bottleneck**: Passing large amounts of data (2,881 records) with each request may cause network latency or slow model inference. **Mitigation**: Only pass data subset under current filter conditions, implement caching mechanism to avoid repeated conversions
- **Risk 5 - GPU Memory Overflow**: Although 12GB VRAM is theoretically sufficient, other applications or system resources may cause OOM errors. **Mitigation**: Document best practices (close other GPU applications), provide diagnostic information when errors occur
- **Risk 6 - Overly High User Expectations**: Users may expect AI to perform functions beyond scope (e.g., prediction, anomaly detection, automatic map operations). **Mitigation**: Provide example questions in chatbot, clearly explain AI capability scope to avoid misleading

## Notes

- **Coordinate System**: Project uses TWD97 TM2 (Taiwan Geodetic Coordinate System) as internal coordinates, WGS84 (GPS coordinates) as display coordinates. Chatbot should uniformly use WGS84 latitude/longitude (lat, lon) to communicate with users, avoiding confusion
- **Data Update Frequency**: Current data is static CSV file, no real-time updates involved. AI analyzes data snapshot at load time; when users switch filter conditions, AI context should update synchronously
- **Model Selection Rationale**: qwen2.5:7b is an open-source model developed by Alibaba with good Traditional Chinese support; 7B parameters can run smoothly on RTX 4080 12GB, balancing performance and quality
- **Chatbot Position**: Right side chosen over left because most users are accustomed to right side as auxiliary panel (like chat, notifications), left side typically for main navigation
- **Data Privacy**: Since all data and models run locally, no cloud services or third-party APIs involved, ensuring data privacy and security
- **Future Expansion**: This specification focuses on core conversation features (P1-P3 user stories). Future considerations may include voice input, real-time streaming responses, conversation history export, AI proactive suggestions, etc.
