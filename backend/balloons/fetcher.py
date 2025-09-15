# balloons/fetcher.py
import random

def fetch_balloons():
    """
    Simulates fetching balloon data.
    Replace with your real API call.
    """
    return [
        {"id": "B001", "lat": 48.8566, "lon": 2.3522, "altitude": 10500},  # Paris
        {"id": "B002", "lat": 40.7128, "lon": -74.0060, "altitude": 9000}, # New York
        {"id": "B003", "lat": 28.6139, "lon": 77.2090, "altitude": 11000}, # Delhi
        {"id": "B004", "lat": random.uniform(-90, 90), "lon": random.uniform(-180, 180), "altitude": 8000}
    ]
