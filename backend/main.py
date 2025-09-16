from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import ask  # <-- this ask uses the agent from agent.py
from collections import deque
from tools import fetch_balloons, format_balloons, enrich_with_country
import asyncio
import os

chat_history = deque(maxlen=20)
app = Flask(__name__)

# Add CORS support
CORS(app, origins="*")

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "healthy", "message": "Windborne agent is running"}

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask_endpoint():
    if request.method == "OPTIONS":
        return "", 200
    
    try:
        data = request.get_json()
        question = data.get("question", "")
        
        # Run async function in sync context
        response = asyncio.run(ask(question, list(chat_history)))
        
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": response})
        
        return {"answer": response}
    except Exception as e:
        return {"error": f"Failed to process question: {str(e)}"}, 500

@app.route("/balloons", methods=["GET"])
def get_balloons():
    """Get current balloon data with country information"""
    try:
        # Run async function in sync context with timeout
        raw_balloons = asyncio.run(asyncio.wait_for(fetch_balloons(0), timeout=10.0))
        
        # Format balloon data
        formatted_balloons = format_balloons(raw_balloons)
        
        # Enrich with country information (with timeout)
        try:
            enriched_balloons = asyncio.run(asyncio.wait_for(enrich_with_country(formatted_balloons), timeout=30.0))
        except asyncio.TimeoutError:
            print("Country detection timed out, using fallback")
            # Fallback: add "Unknown" to all balloons
            enriched_balloons = formatted_balloons
            for balloon in enriched_balloons:
                balloon["country"] = "Unknown"
        
        # Add balloon IDs and mock data for frontend
        balloons_with_ids = []
        for i, balloon in enumerate(enriched_balloons):
            balloon_data = {
                "id": f"B{str(i + 1).zfill(3)}",
                "lat": balloon["lat"],
                "lng": balloon["lon"],  # Frontend expects 'lng'
                "altitude": balloon["alt"],
                "speed": round(15 + (i % 20), 1),  # Mock speed between 15-35 km/h
                "country": balloon.get("country", "Unknown"),  # Real country detection
                "city": "Unknown",  # Simplified - no city detection
                "lastUpdate": "2024-01-01T00:00:00Z"  # Mock timestamp
            }
            balloons_with_ids.append(balloon_data)
        
        return {
            "balloons": balloons_with_ids,
            "total": len(balloons_with_ids),
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except asyncio.TimeoutError:
        return {"error": "Request timed out - country detection is taking too long"}, 500
    except Exception as e:
        return {"error": f"Failed to fetch balloon data: {str(e)}"}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
