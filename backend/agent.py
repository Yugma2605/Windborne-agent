# agent.py
import os, asyncio
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

# Import only the tools that exist
from tools import (
    fetch_balloons,
    format_balloons,
    highest_balloon
)

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Load Gemini LLM with fallback
if API_KEY:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=API_KEY)
else:
    print("Warning: GOOGLE_API_KEY not found. AI agent will not work properly.")
    # Create a dummy LLM for testing
    class DummyLLM:
        def run(self, input_data):
            return "I'm sorry, but the AI agent is not properly configured. Please check the GOOGLE_API_KEY environment variable."
    llm = DummyLLM()

# --- Simplified Tools ---
async def get_balloons_tool():
    """Get current balloon data"""
    try:
        raw_balloons = await fetch_balloons(0)
        formatted_balloons = format_balloons(raw_balloons)
        return {"balloons": formatted_balloons, "count": len(formatted_balloons)}
    except Exception as e:
        return {"error": f"Failed to fetch balloons: {str(e)}"}

async def get_highest_balloon_tool():
    """Get the balloon with the highest altitude"""
    try:
        raw_balloons = await fetch_balloons(0)
        formatted_balloons = format_balloons(raw_balloons)
        highest = highest_balloon(formatted_balloons)
        return highest
    except Exception as e:
        return {"error": f"Failed to get highest balloon: {str(e)}"}

balloon_tools = [
    Tool(
        name="get_balloons",
        func=lambda *args, **kwargs: asyncio.run(get_balloons_tool()),
        description="Get current balloon data with positions and altitudes."
    ),
    Tool(
        name="get_highest_balloon",
        func=lambda *args, **kwargs: asyncio.run(get_highest_balloon_tool()),
        description="Get the balloon with the highest altitude currently."
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
    try:
        loop = asyncio.get_event_loop()
        chat_history = chat_history or []
        
        response = await loop.run_in_executor(
            None,
            lambda: agent.run({"input": question, "chat_history": list(chat_history)})
        )
        return response
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}. Please try again or check if the balloon data is available."
