# agent.py
import os, asyncio
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

# Import the enriched tools
from tools import (
    fastest_balloon_last2h_tool,
    fetch_balloons,
    fetch_hurricanes,
    fetch_wildfires,               # raw fetcher (still available)
    highest_balloon_tool,
    average_altitude_tool,
    fastest_balloon_tool,
    balloons_in_country_tool,
    visited_countries_tool,
    get_all_balloon_speeds_tool,
    fastest_balloons_by_country_tool,
    top_fastest_balloons_tool,
    balloon_speed_analysis_tool,
    most_distance_covered_tool,
    distance_rankings_tool,
    wind_analysis_tool,
    atmospheric_anomalies_tool,
    weather_fronts_tool,
    comprehensive_weather_analysis_tool
)

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Load Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=API_KEY)

# --- Tools ---
balloon_tools = [
    Tool(
        name="highest_balloon",
        func=lambda *args, **kwargs: asyncio.run(highest_balloon_tool()),
        description="Get the balloon with the highest altitude globally. Returns enriched info with country."
    ),
    Tool(
        name="average_altitude",
        func=lambda *args, **kwargs: asyncio.run(average_altitude_tool()),
        description="Compute average altitude of all balloons globally."
    ),
    Tool(
        name="fastest_balloon_last2h",
        func=lambda *args, **kwargs: asyncio.run(fastest_balloon_last2h_tool(*args, **kwargs)),
        description="Returns the balloon that moved the fastest between the last 2 hours."
    ),
    Tool(
        name="balloons_in_country",
        func=lambda country: asyncio.run(balloons_in_country_tool(country)),
        description="List all balloons currently in a given country. Input: country name as a string."
    ),
    Tool(
        name="visited_countries",
        func=lambda balloon_id: asyncio.run(visited_countries_tool(balloon_id)),
        description="Get the list of countries that a balloon has traveled through. Input: balloon ID string (e.g., 'B021')."
    ),
    Tool(
        name="get_hurricanes",
        func=lambda *args, **kwargs: asyncio.run(fetch_hurricanes()),
        description="Fetch current active hurricanes and their positions."
    ),
    Tool(
        name="get_wildfires",
        func=lambda bbox="-125,25,-66,49", hours=24: fetch_wildfires(bbox, hours),
        description="Fetch recent wildfires from NASA FIRMS. Input optional: bounding box and time window in hours."
    ),
    Tool(
        name="get_all_balloon_speeds",
        func=lambda *args, **kwargs: asyncio.run(get_all_balloon_speeds_tool()),
        description="Get speeds for all balloons in the last hour. Returns list of balloons with speed data."
    ),
    Tool(
        name="fastest_balloons_by_country",
        func=lambda *args, **kwargs: asyncio.run(fastest_balloons_by_country_tool()),
        description="Get the fastest balloon in each country. Returns dictionary with country names as keys."
    ),
    Tool(
        name="top_fastest_balloons",
        func=lambda *args, **kwargs: asyncio.run(top_fastest_balloons_tool(10)),
        description="Get the top 10 fastest balloons. Returns list of fastest balloons with speed data."
    ),
    Tool(
        name="balloon_speed_analysis",
        func=lambda *args, **kwargs: asyncio.run(balloon_speed_analysis_tool()),
        description="Get comprehensive speed analysis including statistics, fastest/slowest balloons, and averages."
    ),
    Tool(
        name="most_distance_covered",
        func=lambda *args, **kwargs: asyncio.run(most_distance_covered_tool()),
        description="Get the balloon that has covered the most distance in the past hour."
    ),
    Tool(
        name="distance_rankings",
        func=lambda *args, **kwargs: asyncio.run(distance_rankings_tool()),
        description="Get all balloons ranked by distance covered in the past hour."
    ),
    Tool(
        name="wind_analysis",
        func=lambda *args, **kwargs: asyncio.run(wind_analysis_tool()),
        description="Analyze wind patterns, directions, and speeds across all balloons and countries."
    ),
    Tool(
        name="atmospheric_anomalies",
        func=lambda *args, **kwargs: asyncio.run(atmospheric_anomalies_tool()),
        description="Detect atmospheric anomalies, unusual speeds, altitudes, or wind patterns."
    ),
    Tool(
        name="weather_fronts",
        func=lambda *args, **kwargs: asyncio.run(weather_fronts_tool()),
        description="Detect potential weather fronts based on balloon movement patterns across regions."
    ),
    Tool(
        name="comprehensive_weather_analysis",
        func=lambda *args, **kwargs: asyncio.run(comprehensive_weather_analysis_tool()),
        description="Get comprehensive weather analysis including wind patterns, anomalies, and fronts."
    ),
]

# --- Initialize agent ---
agent = initialize_agent(
    tools=balloon_tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)

# --- Async wrapper ---
async def ask(question: str, chat_history=None):
    loop = asyncio.get_event_loop()
    chat_history = chat_history or []
    
    response = await loop.run_in_executor(
        None,
        lambda: agent.run({"input": question, "chat_history": list(chat_history)})
    )
    return response
