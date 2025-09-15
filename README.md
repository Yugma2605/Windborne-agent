# Windborne Balloon Tracking Agent

A comprehensive balloon tracking and weather intelligence system with a modern React frontend and FastAPI backend.

## 🌟 Features

### Backend (FastAPI + LangChain)
- **AI-Powered Agent** - Google Gemini 2.0 Flash integration
- **Real-time Balloon Tracking** - Global weather balloon data
- **Weather Intelligence** - Hurricane and wildfire tracking
- **Geographic Analysis** - Country-based balloon filtering
- **Data Enrichment** - Enhanced balloon data with location info
- **Caching System** - 30-minute data cache for performance

### Frontend (React + Tailwind CSS)
- **Modern Dashboard** - Beautiful glassmorphism UI
- **Interactive Chat** - Real-time agent communication
- **Analytics Visualization** - Data charts and insights
- **Responsive Design** - Mobile and desktop optimized
- **Real-time Updates** - Live data refresh capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
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
- API Docs: http://localhost:8000/docs

## 🎯 Agent Capabilities

The Windborne agent can answer questions about:

- **Balloon Analytics**
  - Highest altitude balloons
  - Average global altitude
  - Fastest moving balloons
  - Balloons by country

- **Weather Data**
  - Active hurricanes
  - Recent wildfires
  - Storm tracking

- **Geographic Analysis**
  - Country-specific balloon data
  - Travel history of specific balloons
  - Regional weather patterns

## 📊 Example Queries

Try asking the agent:

- "What is the highest balloon currently?"
- "Show me balloons in the United States"
- "Which balloon moved the fastest in the last 2 hours?"
- "What is the average altitude of all balloons?"
- "Show me current active hurricanes"
- "Find recent wildfires in the US"

## 🏗️ Architecture

```
Windborne/
├── backend/                 # FastAPI backend
│   ├── agent.py            # LangChain agent setup
│   ├── tools.py            # Balloon tracking tools
│   ├── main.py             # FastAPI server
│   ├── config.py           # Configuration
│   └── data/               # Geographic data cache
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   └── App.jsx         # Main app
│   └── package.json
├── start.bat              # Windows startup script
├── start.ps1              # PowerShell startup script
└── README.md
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Web framework
- **LangChain** - AI agent framework
- **Google Gemini** - LLM integration
- **GeoPandas** - Geographic data processing
- **HTTPX** - Async HTTP client
- **Pydantic** - Data validation

### Frontend
- **React 19** - Frontend framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Axios** - HTTP client

## 📈 Data Sources

- **Windborne Systems** - Balloon tracking data
- **NOAA** - Hurricane tracking
- **NASA FIRMS** - Wildfire detection
- **Natural Earth** - Geographic boundaries

## 🔧 Configuration

### Backend Configuration
Edit `backend/config.py` for:
- API endpoints
- Cache settings
- Data refresh intervals

### Frontend Configuration
Edit `frontend/src/services/api.js` for:
- Backend URL
- Request timeouts
- Error handling

## 🚀 Deployment

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment
```bash
cd frontend
npm run build
# Serve the dist/ folder with any static server
```

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

