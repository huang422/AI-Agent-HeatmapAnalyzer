# AI Agent Heatmap Analytics Web
# ---(Vue + FastAPI + LLM Agent)

> An interactive geospatial visualization platform for analyzing customer distribution patterns across Taiwan using real-time heatmap technology.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D.svg?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000?logo=ollama&logoColor=white)](https://ollama.com/)
[![Qwen](https://img.shields.io/badge/Qwen-3:14B-7C3AED)](https://github.com/QwenLM/Qwen)

## Project Overview

A full-stack web application that visualizes geographic user distribution data through interactive heatmaps on Taiwan's map. The system features automatic time-based cycling, multi-dimensional filtering, and comprehensive demographic analytics.

**Key Highlights:**
- **AI-Powered Assistant**: Local Ollama-based chatbot (Qwen 3:14B) for intelligent data analysis
- **High Performance**: Sub-500ms API response time with ~260,000 coordinate conversions/second
- **Rich Visualization**: Real-time heatmap updates with smooth transitions
- **Advanced Analytics**: Gender and age distribution charts
- **Auto-Playback**: Time-lapse visualization cycling through 24 hours (1-second intervals)
- **Multi-Filter System**: Month, hour, and duration metric filtering
- **Responsive Design**: From 320px mobile to 4K desktop

## Demo

![Application Screenshot](doc/images/img_1.png)

*Interactive heatmap visualization showing customer distribution patterns across Taiwan with real-time demographic analytics*

## Key Features

### Interactive Heatmap
- Grid-based density visualization using OpenLayers
- Smooth color transitions based on user density
- Real-time updates on filter changes

### Time-Based Analysis
- **Auto-cycling**: 1-second intervals through 24-hour timeline
- **Manual controls**: Play/pause/reset functionality
- **Timeline slider**: Direct hour selection with visual feedback

### Multi-Dimensional Filtering
- **Monthly Analysis**: 4 months of data (Dec 2024, Feb/May/Aug 2025)
- **Duration Metrics**:
  - Total users
  - Quick visits (<10 min)
  - Medium stays (10-30 min)
  - Long visits (>30 min)

### Demographic Insights
- **Gender Distribution**: Interactive pie chart
- **Age Groups**: 9 age brackets with percentage breakdown
- **ECharts Integration**: Smooth animations and responsive tooltips

### AI-Powered Data Assistant
- **Local LLM Integration**: Ollama with Qwen 3:14B model
- **Context-Aware Analysis**: Real-time data insights based on current filters
- **Natural Language Q&A**: Ask questions about heatmap patterns in Traditional Chinese
- **Smart Summaries**: Automatic statistics calculation and trend analysis
- **Conversation History**: Multi-turn dialogue with context retention

## Architecture

### Technology Stack

**Backend**
- **Framework**: FastAPI (Python 3.9+) - Modern, high-performance REST API
- **AI Integration**: Ollama - Local LLM inference (Qwen 3:14B model)
- **Data Processing**: Pandas + NumPy - Efficient data manipulation
- **Coordinate Conversion**: Numba JIT compilation for 260k+ conversions/sec
- **Server**: Uvicorn ASGI server with auto-reload

**Frontend**
- **Framework**: Vue.js 3 (Composition API) - Reactive UI components
- **Mapping**: OpenLayers 9 - Advanced geospatial visualization
- **Charts**: Apache ECharts 5 - Professional data visualization
- **Projection**: Proj4 - Coordinate system transformations
- **Build Tool**: Vite - Lightning-fast HMR and builds

**Data Pipeline**
- **Format**: CSV with TWD97 TM2 grid coordinates
- **Cache**: In-memory 5MB data cache for instant access
- **Conversion**: Custom Numba-accelerated coordinate transformer

### System Design

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Vue 3 SPA     │────▶│   FastAPI REST   │────▶│   Pandas Data   │
│   (Frontend)    │◀────│   (Backend)      │◀────│   (Processing)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │                         │
    OpenLayers              Uvicorn ASGI             Numba JIT
    ECharts 5               CORS Enabled          TWD97→WGS84
    Chat UI                 Ollama API            Data Export
                                │
                        ┌───────▼────────┐
                        │  Ollama Server │
                        │  (Qwen 3:14B)  │
                        └────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.9+ (conda environment recommended)
- Node.js 16.x or higher
- Git
- **Ollama** (for AI chat feature) - [Install from ollama.com](https://ollama.com)

### Development Setup

**1. Clone Repository**
```bash
git clone <repository-url>
cd store_heatmap
```

**2. Install and Start Ollama** (for AI chat feature)
```bash
# Install Ollama from https://ollama.com
# Then pull the Qwen model
ollama pull qwen3:14b

# Ollama will run on http://localhost:11434
```

**3. Backend Setup**
```bash
conda create -n fapi python=3.9 -y
conda activate fapi
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

**4. Frontend Setup** (new terminal)
```bash
cd frontend
npm install
npm run dev
```

**5. Access Application**
- Frontend: http://localhost:5173
- API Documentation: http://127.0.0.1:8000/docs
- Interactive API: http://127.0.0.1:8000/redoc
- Ollama API: http://localhost:11434

**Note**: AI chat feature requires Ollama to be running. If Ollama is not installed, the app will still work but the chatbot will be unavailable.

## Docker Deployment (Recommended)

### Quick Start with Docker

The easiest way to run the application with public internet access:

```bash
./start-docker.sh
```

This will:
- Build and start all services (Backend, Frontend, Ngrok)
- Display the local and public URLs
- Automatically expose your app to the internet via Ngrok

**Access Points:**
- Local Frontend: http://localhost
- Local API: http://localhost:8000/docs
- Public URL: Displayed in terminal (share with anyone!)
- Ngrok Dashboard: http://localhost:4040

**See [DOCKER.md](./docker-instruction/DOCKER.md) for detailed Docker deployment guide.**

## Production Deployment

### Building Windows Executable

Package into a **single standalone .exe** file:
- Python runtime + all dependencies
- Backend API (FastAPI + Uvicorn)
- Frontend UI (Vue 3 + OpenLayers + ECharts)
- Data file (data.csv)

**No installation required for end users!**

#### Build Steps

**1. Build Frontend**
```bash
cd frontend
npm run build
```

**2. Prepare Package**

Automated script:

```bash
./prepare_for_windows.sh
```

equired folders:
```bash
mkdir ~/store_heatmap_pack
cp -r backend ~/store_heatmap_pack/              # Backend source code
cp -r frontend/dist ~/store_heatmap_pack/frontend/  # Built frontend
cp -r data ~/store_heatmap_pack/                 # Data files
```

**3. Build on Windows**
```powershell
cd backend
pip install -r requirements.txt pyinstaller
python build_exe.py
```

**4. Result**
```
backend\dist\StoreHeatmap.exe  (~100-150 MB)
```

Double-click to run - browser opens automatically!

## 📁 Project Structure

```
store_heatmap/
├── backend/                    # Python FastAPI backend
│   ├── src/
│   │   ├── main.py            # Application entry point
│   │   ├── api/               # REST API routes and models
│   │   │   └── routes/
│   │   │       ├── data.py           # Heatmap data endpoints
│   │   │       ├── demographics.py   # Statistics endpoints
│   │   │       └── chat.py           # AI chatbot endpoints
│   │   ├── services/          # Business logic layer
│   │   │   ├── data_loader.py         # CSV data caching
│   │   │   ├── coordinate_converter.py # TWD97→WGS84
│   │   │   ├── data_exporter.py       # Data summarization
│   │   │   └── ollama_service.py      # AI integration
│   │   └── utils/             # Configuration
│   └── requirements.txt       # Dependencies
│
├── frontend/                   # Vue.js 3 frontend
│   ├── src/
│   │   ├── components/        # Vue components
│   │   │   ├── map/          # HeatmapMap
│   │   │   ├── charts/       # GenderChart, AgeChart
│   │   │   ├── controls/     # Playback controls
│   │   │   └── chat/         # AI Chatbot UI
│   │   ├── composables/      # Composition API logic
│   │   │   ├── useAutoplay.js   # 1-sec time cycling
│   │   │   └── useHeatmapData.js # API integration
│   │   └── services/         # API client
│   └── vite.config.js        # Build configuration
│
├── data/
│   └── data.csv              # TWD97 TM2 grid data
│
└── specs/                     # Technical documentation
```

## API Endpoints

**Data**
- `GET /api/heatmap` - Grid-based heatmap coordinates
  - Params: `month`, `hour`, `metric`
  - Returns: `[{lat, lng, value}]`

- `GET /api/demographics` - Gender/age statistics
  - Returns: Gender % + 9 age groups

**AI Chat**
- `POST /api/chat/message` - Send message to AI assistant
  - Body: `{message, context, history}`
  - Returns: AI response with analysis

- `GET /api/chat/health` - Check Ollama service status
  - Returns: Connection status and model info

- `GET /api/chat/context` - Get current data context
  - Params: `month`, `hour`, `day_type`
  - Returns: Data summary for debugging

**System**
- `GET /api/metadata` - Available filters
- `GET /health` - Health check
- `GET /docs` - Swagger UI

## ⚡ Performance

- **API Response**: <500ms average
- **Coordinate Conversion**: ~260,000/sec (Numba)
- **AI Response Time**: 2-5s (Qwen 3:14B on CPU), <1s with GPU
- **Memory Usage**: ~5MB cache (data) + ~8GB (LLM model)
- **Frontend Bundle**: 1.1MB gzipped
- **Initial Load**: <2s

## Technical Highlights

1. **AI-Powered Data Analysis**
   - Local LLM inference with Ollama
   - Context-aware responses using current filter state
   - Automated statistics calculation and summarization
   - Multi-turn conversation with history retention
   - Traditional Chinese language support

2. **High-Performance Coordinate Conversion**
   - Numba JIT compilation
   - Vectorized NumPy operations
   - 260k+ conversions/second

3. **Reactive State Management**
   - Vue 3 Composition API
   - Efficient dependency tracking
   - Minimal re-renders

4. **Smart Data Caching**
   - In-memory DataFrame
   - On-demand filtering
   - 5MB footprint

5. **Production-Ready Packaging**
   - Single-file executable
   - Embedded Python runtime
   - Auto-browser launch

## Data Model

> **Data Privacy Notice**: Due to privacy and confidentiality concerns, the actual customer data files (`data/data.csv`) are **not included** in this GitHub repository. The application requires a properly formatted CSV file with TWD97 TM2 grid coordinates to function. Contact the developer for a sample dataset or see the schema below to prepare your own data.

## Documentation

- [Developer Quickstart](specs/001-heatmap-visualization/quickstart.md)
- [Data Model](specs/001-heatmap-visualization/data-model.md)
- [API Specification](specs/001-heatmap-visualization/spec.md)

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is available for educational and portfolio demonstration purposes.

## Contact
For questions, issues, or collaboration inquiries:

- Developer: Tom Huang
- Email: huang1473690@gmail.com
