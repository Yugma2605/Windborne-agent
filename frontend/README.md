# Windborne Frontend

A modern React frontend for the Windborne Balloon Tracking Agent.

## Features

- 🎈 **Real-time Balloon Tracking** - Track weather balloons globally
- 🤖 **AI Agent Chat** - Interactive chat with the Windborne agent
- 📊 **Analytics Dashboard** - Visualize balloon data and trends
- 🌍 **Global Coverage** - Worldwide balloon and weather data
- 📱 **Responsive Design** - Works on desktop and mobile
- 🎨 **Modern UI** - Beautiful glassmorphism design with Tailwind CSS

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Make sure the backend is running on `http://localhost:8000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Tech Stack

- **React 19** - Frontend framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **Lucide React** - Icon library
- **Axios** - HTTP client for API calls

## Project Structure

```
src/
├── components/          # React components
│   ├── ChatInterface.jsx    # AI agent chat
│   ├── Dashboard.jsx        # Main dashboard
│   ├── Analytics.jsx        # Data visualization
│   ├── Navigation.jsx       # App navigation
│   └── Settings.jsx         # App settings
├── services/            # API services
│   └── api.js              # Backend API client
├── App.jsx              # Main app component
└── index.css            # Global styles
```

## Backend Integration

The frontend connects to the FastAPI backend running on `http://localhost:8000` with the following endpoints:

- `GET /health` - Health check
- `POST /ask` - Send questions to the agent

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Development

The app uses Tailwind CSS for styling. Key design patterns:

- **Glassmorphism** - Semi-transparent cards with backdrop blur
- **Gradient backgrounds** - Blue to purple gradients
- **Responsive grid** - Mobile-first responsive design
- **Dark theme** - Optimized for dark backgrounds

## Features Overview

### Dashboard
- Quick action buttons for common queries
- Real-time connection status
- System statistics

### Chat Interface
- Interactive chat with the Windborne agent
- Message history
- Real-time responses
- Error handling

### Analytics
- Balloon altitude distribution
- Country statistics
- Speed rankings
- Live data from agent

### Settings
- API configuration
- Notification preferences
- Theme settings
- System information