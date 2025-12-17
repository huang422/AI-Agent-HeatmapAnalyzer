# Development Quickstart Guide

**Feature**: 001-heatmap-visualization
**Date**: 2025-12-15
**Audience**: Developers setting up the project for the first time

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python**: 3.9 or higher
- **Node.js**: 16.x or higher (LTS recommended)
- **npm**: 8.x or higher (comes with Node.js)
- **Git**: For version control
- **Conda** (optional but recommended): For Python environment management

---

## Quick Start (5 Minutes)

### 1. Clone and Setup

```bash
# Clone repository (adjust URL as needed)
git clone <repository-url>
cd store_heatmap

# Checkout feature branch
git checkout 001-heatmap-visualization
```

### 2. Backend Setup

```bash
# Create and activate conda environment
conda create -n fapi python=3.9
conda activate fapi

# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Backend should now be running at http://127.0.0.1:8000

### 3. Frontend Setup (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend should now be running at http://localhost:5173

### 4. Verify Setup

- **Backend API docs**: http://127.0.0.1:8000/docs (FastAPI Swagger UI)
- **Frontend**: http://localhost:5173
- **Test API**: `curl http://127.0.0.1:8000/api/metadata`

---

## Detailed Setup Guide

### Backend Configuration

#### 1. Python Environment Setup

**Option A: Using Conda (Recommended)**

```bash
# Create environment
conda create -n fapi python=3.9 -y
conda activate fapi

# Verify Python version
python --version  # Should show 3.9.x
```

**Option B: Using venv**

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Key Dependencies:**
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `pandas==2.1.3` - Data processing
- `numpy==1.26.2` - Numerical operations
- `numba==0.58.1` - JIT compilation for coordinate conversion

#### 3. Verify Data File

```bash
# Check that data file exists
ls ../data/data.csv

# View first few lines
head -n 5 ../data/data.csv
```

Expected output:
```
month,gx,gy,day_type,hour,avg_total_users,...
202412,7165,7152,假日,0,20.67,...
```

#### 4. Run Backend

**Development Mode (with auto-reload):**
```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

**Production Mode:**
```bash
uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 4
```

#### 5. Test Backend Endpoints

```bash
# Get metadata
curl http://127.0.0.1:8000/api/metadata

# Get heatmap data
curl "http://127.0.0.1:8000/api/heatmap?month=202412&hour=0"

# Get demographics
curl "http://127.0.0.1:8000/api/demographics?month=202412&hour=14"

# Health check
curl http://127.0.0.1:8000/health
```

---

### Frontend Configuration

#### 1. Install Node Dependencies

```bash
cd frontend
npm install
```

**Key Dependencies:**
- `vue@^3.4.0` - Framework
- `ol@^9.0.0` - OpenLayers mapping library
- `echarts@^5.4.0` - Charting library
- `vue-echarts@^6.6.0` - Vue wrapper for ECharts
- `proj4@^2.11.0` - Coordinate projection

#### 2. Configuration Files

**vite.config.js** (should already exist):
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
```

This proxies API requests from frontend (port 5173) to backend (port 8000).

#### 3. Run Frontend

```bash
# Development mode (hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

#### 4. Verify Frontend

Open http://localhost:5173 in your browser. You should see:
- A map centered on Taiwan
- Control panels for month, metric, hour selection
- Demographic charts (may be empty until backend connected)

---

## Development Workflow

### Typical Development Session

```bash
# Terminal 1: Backend
conda activate fapi
cd backend
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Testing/Git
pytest backend/tests/
git status
```

### Making Changes

**Backend Changes:**
1. Edit files in `backend/src/`
2. Server auto-reloads (uvicorn --reload)
3. Test at http://127.0.0.1:8000/docs
4. Run tests: `pytest backend/tests/`

**Frontend Changes:**
1. Edit files in `frontend/src/`
2. Browser auto-reloads (Vite HMR)
3. Check browser console for errors
4. Test UI interactions

---

## Project Structure Overview

```
store_heatmap/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── main.py            # Entry point
│   │   ├── api/               # API routes
│   │   ├── services/          # Business logic
│   │   └── models/            # Data models
│   ├── tests/                 # Backend tests
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Vue.js frontend
│   ├── src/
│   │   ├── main.js            # Entry point
│   │   ├── App.vue            # Root component
│   │   ├── components/        # Vue components
│   │   ├── composables/       # Composition API logic
│   │   └── services/          # API client
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Build configuration
│
├── data/
│   └── data.csv               # Source data
│
└── specs/001-heatmap-visualization/
    ├── spec.md                # Feature specification
    ├── plan.md                # Implementation plan
    ├── research.md            # Technical research
    ├── data-model.md          # Data models
    ├── contracts/openapi.yaml # API contracts
    └── quickstart.md          # This file
```

---

## Common Tasks

### Run Tests

**Backend:**
```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/test_coordinate_converter.py -v
```

**Frontend (when tests are added):**
```bash
cd frontend
npm run test
```

### Check Code Quality

**Backend:**
```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type checking (if using mypy)
mypy src/
```

**Frontend:**
```bash
# Lint
npm run lint

# Format (if using prettier)
npm run format
```

### Update Dependencies

**Backend:**
```bash
pip list --outdated
pip install --upgrade <package-name>
pip freeze > requirements.txt
```

**Frontend:**
```bash
npm outdated
npm update
npm install <package-name>@latest
```

---

## Troubleshooting

### Backend Issues

**Problem: `ModuleNotFoundError: No module named 'fastapi'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem: `FileNotFoundError: data/data.csv`**
```bash
# Solution: Verify data file exists
ls ../data/data.csv

# If missing, ensure you're in correct directory
pwd  # Should end with /backend
```

**Problem: Port 8000 already in use**
```bash
# Solution: Use different port
uvicorn src.main:app --reload --port 8001

# Or kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

**Problem: CORS errors from frontend**
```bash
# Solution: Ensure CORS middleware is configured in main.py
# (Should already be set up)
```

### Frontend Issues

**Problem: `npm: command not found`**
```bash
# Solution: Install Node.js from https://nodejs.org/
# Verify installation
node --version
npm --version
```

**Problem: `Failed to resolve import 'vue'`**
```bash
# Solution: Install dependencies
npm install
```

**Problem: API calls return 404**
```bash
# Solution: Check proxy configuration in vite.config.js
# Ensure backend is running on port 8000
curl http://127.0.0.1:8000/health
```

**Problem: Map not displaying**
```bash
# Solution: Check browser console for errors
# Verify OpenLayers is installed
npm list ol

# If missing
npm install ol@^9.0.0
```

### Coordinate Conversion Issues

**Problem: `ValueError` in coordinate conversion**
```bash
# Solution: Verify gx/gy values are within Taiwan bounds
# Check data/gxgy_transfer.ipynb for reference implementation
```

**Problem: Slow coordinate conversion**
```bash
# Solution: Ensure numba is installed for JIT compilation
pip install numba==0.58.1

# Verify numba is working
python -c "from numba import jit; print('Numba OK')"
```

---

## Environment Variables

Create `.env` file in backend directory (optional):

```bash
# Backend configuration
API_HOST=127.0.0.1
API_PORT=8000
DATA_PATH=../data/data.csv

# Development settings
DEBUG=true
LOG_LEVEL=info
```

Load in `src/main.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
API_PORT = int(os.getenv('API_PORT', 8000))
```

---

## Building for Production

### Frontend Build

```bash
cd frontend
npm run build

# Output will be in dist/ directory
ls dist/
```

### Backend + Frontend Combined (Executable)

```bash
# 1. Build frontend
cd frontend
npm run build

# 2. Build executable
cd ../backend
python build_exe.py

# Output: backend/dist/StoreHeatmap.exe
```

See [research.md](./research.md#5-pyinstaller-packaging-strategy) for detailed packaging instructions.

---

## Next Steps

1. **Understand the codebase**: Read [spec.md](./spec.md) and [data-model.md](./data-model.md)
2. **Review API contracts**: Check [contracts/openapi.yaml](./contracts/openapi.yaml)
3. **Explore research**: See [research.md](./research.md) for technology decisions
4. **Start coding**: Follow the project structure in [plan.md](./plan.md)
5. **Run tests**: Ensure everything works before making changes

---

## Getting Help

- **API Documentation**: http://127.0.0.1:8000/docs (Swagger UI)
- **Project Specs**: `specs/001-heatmap-visualization/`
- **Constitution**: `.specify/memory/constitution.md`
- **Data Reference**: `data/gxgy_transfer.ipynb`

---

## Tips for Efficient Development

1. **Use two terminals**: One for backend, one for frontend
2. **Keep Swagger UI open**: http://127.0.0.1:8000/docs for API testing
3. **Use browser DevTools**: Network tab to inspect API calls
4. **Check console**: Both terminal and browser console for errors
5. **Hot reload**: Both servers support auto-reload - just save and see changes
6. **Git often**: Commit frequently with clear messages
7. **Read the spec**: When in doubt, check spec.md for requirements
8. **Test early**: Run tests before making big changes

---

**Last Updated**: 2025-12-15
**Version**: 1.0.0
