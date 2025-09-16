# Windborne Balloon Tracking Agent

A comprehensive balloon tracking and weather intelligence system with a modern React frontend and Flask backend, featuring AI-powered analysis and real-time global balloon tracking.

## 🌟 Features

### Backend (Flask + LangChain)
- **AI-Powered Agent** - Google Gemini 2.0 Flash integration with LangChain
- **Real-time Balloon Tracking** - Global weather balloon data from Windborne Systems
- **Country Detection** - Lightweight local dataset for instant country identification
- **Weather Intelligence** - Hurricane and wildfire tracking capabilities
- **Geographic Analysis** - Country-based balloon filtering and analysis
- **Data Enrichment** - Enhanced balloon data with location and country info
- **Caching System** - File-based caching for performance optimization
- **Production Ready** - Deployed on Render with Gunicorn

### Frontend (React + Tailwind CSS)
- **Modern Dashboard** - Beautiful glassmorphism UI with quick actions
- **Interactive Chat** - Real-time agent communication with conversation history
- **Interactive Map** - Leaflet-based balloon visualization with altitude-based color coding
- **Responsive Design** - Mobile and desktop optimized
- **Real-time Updates** - Live data refresh capabilities
- **Visual Legend** - Altitude-based color legend for map understanding

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google API Key (for Gemini)
- NASA FIRMS API Key (optional, for wildfire data)

### Installation

1. **Clone and setup backend:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Setup environment variables:**
```bash
# Create .env file in backend directory
GOOGLE_API_KEY=your_google_api_key_here
NASA_FIRMS_KEY=your_nasa_firms_key_here
```

3. **Setup frontend:**
```bash
cd frontend
npm install
```

### Running the Application

**Option 1: Use the startup scripts**
```bash
# Windows
./start.bat
# or
./start.ps1
```

**Option 2: Manual startup**
```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Health Check: http://localhost:8000/health

## 🎯 Agent Capabilities

The Windborne agent can answer questions about:

- **Balloon Analytics**
  - Highest altitude balloons globally
  - Average global altitude statistics
  - Fastest moving balloons
  - Balloons by country (with real country detection)
  - Speed analysis and rankings

- **Weather Data**
  - Active hurricanes and storm tracking
  - Recent wildfires with NASA FIRMS data
  - Weather anomalies detection
  - Atmospheric pattern analysis

- **Geographic Analysis**
  - Country-specific balloon data
  - Travel history of specific balloons
  - Regional weather patterns
  - Ocean and land-based balloon distribution

## 📊 Example Queries

Try asking the agent:

- "What is the highest balloon currently?"
- "Which country has the most balloons?"
- "Show me balloons in the United States"
- "Which balloon moved the fastest in the last 2 hours?"
- "What is the average altitude of all balloons?"
- "Show me current active hurricanes"
- "Find recent wildfires in the US"
- "How many balloons are in India?"

## 🗺️ Map Features

- **Altitude-Based Color Coding**
  - 🔴 Red: High Altitude (15+ km)
  - 🟠 Orange: Medium-High (10-15 km)
  - 🟡 Yellow: Medium (5-10 km)
  - 🟢 Green: Low Altitude (0-5 km)
  - ⭐ Star: Highest Balloon indicator

- **Interactive Features**
  - Click balloons for detailed information
  - Zoom and pan capabilities
  - Real-time data updates
  - Fixed legend for easy reference

## 🏗️ Architecture

```
Windborne/
├── backend/                 # Flask backend
│   ├── agent.py            # LangChain agent setup
│   ├── tools.py            # Balloon tracking tools
│   ├── main.py             # Flask server
│   ├── country_dataset.py  # Local country detection
│   ├── render.yaml         # Render deployment config
│   └── data/               # Cache and data storage
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   └── MapVisualization.jsx
│   │   ├── services/       # API client
│   │   └── App.jsx         # Main app
│   └── package.json
├── start.bat              # Windows startup script
├── start.ps1              # PowerShell startup script
└── README.md
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework (switched from FastAPI for better deployment)
- **LangChain** - AI agent framework
- **Google Gemini 2.0 Flash** - LLM integration
- **Local Country Dataset** - Fast country detection (no external APIs)
- **HTTPX** - Async HTTP client
- **Gunicorn** - Production WSGI server

### Frontend
- **React 19** - Frontend framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Axios** - HTTP client
- **React Leaflet** - Map visualization

## 📈 Data Sources

- **Windborne Systems** - Balloon tracking data
- **NOAA** - Hurricane tracking
- **NASA FIRMS** - Wildfire detection
- **Local Country Dataset** - 100+ countries with precise boundaries

## 🚀 Deployment

### Production Deployment (Render)
The backend is deployed on Render with the following configuration:

```yaml
# render.yaml
services:
  - type: web
    name: windborne-backend-v2
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    pythonVersion: 3.11.7
```

### Local Development
```bash
# Backend
cd backend
python main.py

# Frontend
cd frontend
npm run dev
```

## 🔧 Configuration

### Backend Configuration
- **Country Detection**: Local dataset with 100+ countries
- **Caching**: File-based caching for performance
- **API Keys**: Environment variables for external services

### Frontend Configuration
- **API URL**: Configured in `frontend/.env`
- **Map Settings**: Leaflet configuration for optimal performance
- **Responsive Design**: Mobile-first approach

## 🎨 UI/UX Features

- **Glassmorphism Design** - Modern glass-like UI elements
- **Responsive Navigation** - Mobile-friendly sidebar
- **Interactive Map** - Real-time balloon visualization
- **Chat Interface** - Conversational AI agent
- **Quick Actions** - One-click common queries
- **Visual Feedback** - Loading states and error handling

## 📊 Performance Optimizations

- **Local Country Detection** - Instant country identification (no API calls)
- **File-based Caching** - 30-minute data cache
- **Parallel Processing** - Async balloon data processing
- **Optimized Map Rendering** - Efficient balloon visualization
- **Production Server** - Gunicorn for better performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Windborne Systems for balloon tracking data
- NOAA for hurricane data
- NASA for wildfire detection
- Google for Gemini AI capabilities
- Render for hosting infrastructure

## 🔗 Live Demo

- **Frontend**: [Windborne Dashboard](https://windborne-dashboard.vercel.app)
- **Backend API**: [Windborne Agent](https://windborne-agent.onrender.com)
- **Health Check**: [API Status](https://windborne-agent.onrender.com/health)