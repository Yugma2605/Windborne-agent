from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent import ask  # <-- this ask uses the agent from agent.py
from collections import deque
from tools import fetch_balloons, format_balloons

chat_history = deque(maxlen=20)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now - you can restrict this later
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly allow OPTIONS
    allow_headers=["*"],  # Allow all headers
)

class Query(BaseModel):
    question: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Windborne agent is running"}

@app.options("/ask")
async def ask_options():
    return JSONResponse(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

@app.post("/ask")
async def ask_endpoint(query: Query):
    response = await ask(query.question, list(chat_history))
    chat_history.append({"role": "user", "content": query.question})
    chat_history.append({"role": "assistant", "content": response})
    return {"answer": response}

@app.get("/balloons")
async def get_balloons():
    """Get current balloon data"""
    try:
        # Fetch raw balloon data (current hour)
        raw_balloons = await fetch_balloons(0)
        
        # Format balloon data
        formatted_balloons = format_balloons(raw_balloons)
        
        # Add balloon IDs and mock data for frontend
        balloons_with_ids = []
        for i, balloon in enumerate(formatted_balloons):
            balloon_data = {
                "id": f"B{str(i + 1).zfill(3)}",
                "lat": balloon["lat"],
                "lng": balloon["lon"],  # Frontend expects 'lng'
                "altitude": balloon["alt"],
                "speed": round(15 + (i % 20), 1),  # Mock speed between 15-35 km/h
                "country": "Unknown",  # Simplified - no country detection
                "city": "Unknown",  # Simplified - no city detection
                "lastUpdate": "2024-01-01T00:00:00Z"  # Mock timestamp
            }
            balloons_with_ids.append(balloon_data)
        
        return {
            "balloons": balloons_with_ids,
            "total": len(balloons_with_ids),
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to fetch balloon data: {str(e)}"}
        )
