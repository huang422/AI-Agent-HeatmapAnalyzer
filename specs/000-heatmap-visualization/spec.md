# Feature Specification: Interactive Geographic Heatmap Visualization System

**Feature Branch**: `001-heatmap-visualization`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User description: "建立互動式網頁呈現資料分析視覺化專案，前端使用vue，後端用fastapi，最後打包成exe成行檔"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Geographic Distribution of Users (Priority: P1)

Users need to visualize the geographic distribution of people across different locations using a heatmap that shows user density at specific coordinates and time periods.

**Why this priority**: This is the core value of the application - enabling users to see where people are concentrated geographically. Without this, the application has no purpose.

**Independent Test**: Can be fully tested by loading the application and verifying that a map displays with heatmap overlay showing user density data from the CSV file, and delivers immediate visual insight into geographic distribution patterns.

**Acceptance Scenarios**:

1. **Given** the application is launched, **When** the user opens the interface, **Then** a map is displayed with heatmap visualization showing user density across all coordinates
2. **Given** the heatmap is displayed, **When** the user hovers over any location, **Then** a tooltip displays the number of users at that specific location
3. **Given** the application loads data, **When** coordinate conversion from gx/gy to latitude/longitude completes, **Then** all locations are accurately positioned on the map

---

### User Story 2 - View Time-Based Changes in User Distribution (Priority: P2)

Users need to see how user distribution changes across different hours of the day, with automatic cycling through time periods to reveal temporal patterns.

**Why this priority**: Understanding temporal patterns is critical for business decisions but requires the basic map visualization to exist first.

**Independent Test**: Can be tested by observing the heatmap automatically cycle through 24 hourly time periods (0-23) every 3 seconds, showing how user density changes throughout the day.

**Acceptance Scenarios**:

1. **Given** the map is displayed, **When** the application starts, **Then** the heatmap automatically cycles through hours 0-23, updating every 3 seconds
2. **Given** the time is cycling, **When** each new hour displays, **Then** the heatmap intensity updates to reflect user density for that specific hour
3. **Given** cycling is active, **When** the current hour changes, **Then** a clear indication shows which hour (0-23) is currently displayed

---

### User Story 3 - Filter Data by Month (Priority: P2)

Users need to select specific months to analyze seasonal patterns in user distribution across the available time periods (December 2024, February 2025, May 2025, August 2025).

**Why this priority**: Seasonal analysis is valuable but depends on having the basic visualization working first. Equal priority to hourly cycling.

**Independent Test**: Can be tested by selecting each month option and verifying that the heatmap displays only data from the selected month.

**Acceptance Scenarios**:

1. **Given** the map is displayed, **When** the user selects "December 2024", **Then** the heatmap shows only data from month 202412
2. **Given** the user has selected a month, **When** the user switches to a different month, **Then** the heatmap updates immediately to show the new month's data
3. **Given** multiple months exist, **When** the user cycles through all months, **Then** the heatmap accurately reflects each month's unique distribution patterns

---

### User Story 4 - Select Different Metrics for Visualization (Priority: P2)

Users need to choose between different user duration categories to analyze how long people stay in each location.

**Why this priority**: Different duration metrics provide different business insights but all depend on the core heatmap functionality.

**Independent Test**: Can be tested by selecting each metric option (total users, under 10 minutes, 10-30 minutes, over 30 minutes) and verifying the heatmap updates to show the selected metric.

**Acceptance Scenarios**:

1. **Given** the default view shows total users, **When** the user selects "under 10 minutes", **Then** the heatmap updates to show only users who stayed less than 10 minutes
2. **Given** the user has selected a duration metric, **When** hovering over locations, **Then** the tooltip shows the user count for the selected metric category
3. **Given** any metric is selected, **When** switching to a different metric, **Then** the heatmap intensity recalculates based on the new metric values

---

### User Story 5 - Manually Control Time Period (Priority: P3)

Users need to manually select specific hours using a timeline slider to examine particular time periods in detail, pausing the automatic cycling.

**Why this priority**: Manual control enhances analysis but is not essential for initial insights. Users can still gain value from automatic cycling.

**Independent Test**: Can be tested by dragging the timeline slider to any hour (0-23) and verifying that the heatmap stops auto-cycling and displays data for the selected hour.

**Acceptance Scenarios**:

1. **Given** automatic cycling is active, **When** the user drags the timeline slider to hour 14, **Then** auto-cycling stops and the heatmap displays data for hour 14
2. **Given** the user has manually selected an hour, **When** the user clicks "Start Auto-Play" button, **Then** automatic cycling resumes from the current hour
3. **Given** the user is viewing a specific hour, **When** the user clicks "Reset" button, **Then** the view returns to default settings and auto-cycling restarts from hour 0

---

### User Story 6 - View Demographic Breakdown (Priority: P3)

Users need to see demographic statistics (gender and age distribution) for the currently selected time period and month to understand who is present at each location.

**Why this priority**: Demographic insights add valuable context but users can gain initial value from geographic and temporal patterns alone.

**Independent Test**: Can be tested by selecting different months and hours, then verifying that gender and age distribution charts update to show percentage breakdowns for the selected time period.

**Acceptance Scenarios**:

1. **Given** a specific month and hour are selected, **When** the selection changes, **Then** gender distribution chart updates showing percentages for 男性 (Male) and 女性 (Female)
2. **Given** a specific month and hour are selected, **When** the selection changes, **Then** age distribution chart updates showing percentages across nine age groups (19歲以下 through 55-59歲)
3. **Given** demographic charts are displayed, **When** values are shown, **Then** all percentages are calculated from the selected month/hour data and sum to 100%
4. **Given** demographic data exists, **When** users interact with the charts, **Then** clear labels in Chinese display for each demographic category

---

### Edge Cases

- What happens when a coordinate (gx, gy) cannot be converted to valid latitude/longitude? System should skip invalid coordinates and log warnings without crashing.
- What happens when a specific month/hour combination has zero users at all locations? Heatmap should display with zero intensity (no heat) for that time period.
- What happens when the CSV file is missing required columns? System should validate data structure on load and display clear error message indicating which columns are missing.
- What happens when user hovers over a location with no data? Tooltip should display "No data" or "0 users" instead of showing nothing.
- What happens when the user rapidly switches between months or hours? System should debounce updates or queue them to prevent visual glitching.
- What happens when demographic data contains invalid or null values? System should calculate percentages only from valid data and indicate when data is incomplete.
- What happens when all demographic values for a time period are zero? Charts should display "No data available" message.
- What happens on mobile devices with small screens? Responsive design should adjust layout with map on top, controls below, and charts stacked vertically.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load and parse CSV data from data/data.csv containing columns: month, gx, gy, hour, avg_total_users, avg_users_under_10min, avg_users_10_30min, avg_users_over_30min, sex_1, sex_2, age_1 through age_9
- **FR-002**: System MUST convert grid coordinates (gx, gy) to geographic coordinates (latitude, longitude) using the inverse transformation of the geo2tm2 function found in gxgy_transfer.ipynb
- **FR-003**: System MUST render an interactive map with heatmap overlay showing user density at each coordinate
- **FR-004**: System MUST display a tooltip showing user count when hovering over any heatmap location
- **FR-005**: System MUST automatically cycle through hours 0-23 with a 3-second interval between transitions
- **FR-006**: System MUST provide month selection control with four options: 202412, 202502, 202505, 202508
- **FR-007**: System MUST provide metric selection control with four options: avg_total_users, avg_users_under_10min, avg_users_10_30min, avg_users_over_30min
- **FR-008**: System MUST provide a timeline slider control below the map allowing manual hour selection from 0-23
- **FR-009**: System MUST pause automatic cycling when user manually selects a month, metric, or hour
- **FR-010**: System MUST provide "Start Auto-Play" or "Resume" button to restart automatic hour cycling
- **FR-011**: System MUST provide "Reset" button to return to default state (first month, total users metric, hour 0, auto-cycling enabled)
- **FR-012**: System MUST display gender distribution chart showing percentages for sex_1 (男性/Male) and sex_2 (女性/Female)
- **FR-013**: System MUST display age distribution chart showing percentages for nine age groups with Chinese labels
- **FR-014**: System MUST update demographic charts whenever month or hour selection changes
- **FR-015**: System MUST calculate all demographic percentages from the selected month/hour filtered data
- **FR-016**: System MUST display Chinese labels for all demographic categories as specified
- **FR-017**: System MUST implement responsive web design (RWD) ensuring usability on desktop, tablet, and mobile devices
- **FR-018**: System MUST maintain smooth visual transitions when updating heatmap data
- **FR-019**: System MUST clearly indicate current selections (month, metric, hour) in the user interface
- **FR-020**: System MUST handle missing or invalid data gracefully without crashing

### Key Entities

- **Location Data Point**: Represents user activity at a specific grid location, containing: month identifier, grid coordinates (gx, gy), geographic coordinates (latitude, longitude derived), hour (0-23), user count metrics by duration, demographic breakdowns by gender and age
- **Time Period**: Represents a specific combination of month and hour for data filtering and visualization
- **Heatmap Layer**: Represents the visual intensity map overlaid on the geographic map, with intensity values derived from the selected metric at each location
- **Demographic Distribution**: Represents percentage breakdowns of users by gender (2 categories) and age (9 categories) for a given time period

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can identify high-density user locations within 5 seconds of opening the application
- **SC-002**: Users can understand temporal patterns by watching the automatic hourly cycle complete within 72 seconds (24 hours × 3 seconds)
- **SC-003**: Users can switch between months and see updated visualizations within 1 second
- **SC-004**: Users can select any specific hour and view its data within 500 milliseconds
- **SC-005**: The application displays correctly on screens ranging from 320px mobile width to 4K desktop resolution
- **SC-006**: Demographic charts update to reflect selected time period within 500 milliseconds
- **SC-007**: All coordinate conversions from gx/gy to latitude/longitude maintain positioning accuracy within 50 meters
- **SC-008**: Users can successfully interact with all controls (month selector, metric selector, timeline slider, play/reset buttons) without confusion
- **SC-009**: The heatmap visualization accurately represents relative user density differences across all locations
- **SC-010**: 95% of users can identify the highest density location and time period within 2 minutes of using the application

## Assumptions

- Data in data/data.csv is complete and follows the expected schema with all required columns
- The gx/gy coordinate system uses TWD97 (Taiwan Datum 1997) with the parameters specified in gxgy_transfer.ipynb
- All gx/gy coordinates in the dataset fall within valid Taiwan geographic boundaries
- Users have modern web browsers with JavaScript enabled
- The fapi conda environment includes necessary Python packages for FastAPI backend operations
- Executable packaging will target Windows operating systems
- Month values 202412, 202502, 202505, 202508 represent December 2024, February 2025, May 2025, and August 2025 respectively
- Hour values 0-23 represent 24-hour clock format
- Demographic age groups cover the range 19歲以下 (under 19) through 55-59歲, with ages 60+ grouped as "other"
- Auto-cycling interval of 3 seconds provides sufficient time for users to observe each hour's pattern
- The application will be used primarily for business analysis and planning purposes

## Out of Scope

- Real-time data updates or live data streaming
- User authentication or access control
- Data editing or modification capabilities
- Export of visualizations to image or PDF formats
- Historical comparison views showing multiple months simultaneously
- Predictive analytics or forecasting features
- Integration with external mapping services beyond the chosen mapping library
- Multi-language support beyond Chinese labels for demographics
- Customization of color schemes or visual themes
- Administrative interface for data management
- Mobile native applications (iOS/Android)
- Deployment to web servers or cloud platforms
