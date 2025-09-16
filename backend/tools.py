import datetime
from typing import List, Dict
import math
from pathlib import Path
import requests
import httpx
import os
import json
import time

# --- Load world countries using simple geospatial ---
from geospatial_simple import find_country_for_point_simple
CACHE_FILE = Path("data/balloons_cache.json")
CACHE_TTL = 30 * 60  # 30 minutes in seconds

async def fetch_balloons(hours_ago: int = 0):
    """
    Fetch balloons from API or cache (JSON).
    If cache is older than 30 minutes, refresh.
    """
    now = time.time()

    # Check if cache exists and is fresh
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            cached = json.load(f)
        cached_time = cached.get("timestamp", 0)
        if now - cached_time < CACHE_TTL and str(hours_ago) in cached["data"]:
            return cached["data"][str(hours_ago)]

    # Otherwise fetch from API
    url = f"https://a.windbornesystems.com/treasure/{hours_ago:02d}.json"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        balloons = resp.json()

    # Update cache (store multiple hours if fetched)
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            cached = json.load(f)
    else:
        cached = {"timestamp": now, "data": {}}

    cached["timestamp"] = now
    cached["data"][str(hours_ago)] = balloons

    os.makedirs(CACHE_FILE.parent, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cached, f)

    return balloons

def format_balloons(raw_balloons: List[List[float]]) -> List[Dict]:
    """Convert raw API balloons [[lat, lon, alt], ...] into dicts."""
    return [{"lat": b[0], "lon": b[1], "alt": b[2]} for b in raw_balloons]

# --- Enrichment: add country info ---
def enrich_with_country(balloons: list) -> list:
    enriched = []
    for b in balloons:
        # Find country using simple geospatial operations
        country = find_country_for_point_simple(b["lat"], b["lon"])
        b["country"] = country
        enriched.append(b)
    return enriched

# --- Analytics ---
def highest_balloon(balloons: List[Dict]) -> Dict:
    return max(balloons, key=lambda b: b["alt"]) if balloons else {}

def average_altitude(balloons: List[Dict]) -> float:
    return sum(b["alt"] for b in balloons) / len(balloons) if balloons else 0.0

def calculate_speed(balloon_current: Dict, balloon_previous: Dict, time_hours: float = 1.0) -> Dict:
    """Calculate speed of a balloon between two positions."""
    if not balloon_current or not balloon_previous:
        return {"speed_kmh": 0, "speed_ms": 0, "distance_km": 0}
    
    # Calculate distance using Haversine formula for accurate Earth distance
    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) * math.sin(dlon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    # Calculate horizontal distance
    distance_km = haversine_distance(
        balloon_previous["lat"], balloon_previous["lon"],
        balloon_current["lat"], balloon_current["lon"]
    )
    
    # Calculate altitude change
    alt_change_km = abs(balloon_current["alt"] - balloon_previous["alt"]) / 1000  # Convert m to km
    
    # Calculate 3D distance
    total_distance_km = math.sqrt(distance_km**2 + alt_change_km**2)
    
    # Calculate speed
    speed_kmh = total_distance_km / time_hours if time_hours > 0 else 0
    speed_ms = speed_kmh / 3.6  # Convert km/h to m/s
    
    return {
        "speed_kmh": round(speed_kmh, 2),
        "speed_ms": round(speed_ms, 2),
        "distance_km": round(total_distance_km, 2),
        "horizontal_distance_km": round(distance_km, 2),
        "altitude_change_km": round(alt_change_km, 2)
    }

def fastest_balloon(balloons_current: List[Dict], balloons_previous: List[Dict]) -> Dict:
    """Find the fastest balloon between two time periods."""
    if not balloons_current or not balloons_previous:
        return {}
    
    fastest = {"speed_kmh": 0, "balloon": None, "speed_data": {}}
    
    for i, (b_curr, b_prev) in enumerate(zip(balloons_current, balloons_previous)):
        speed_data = calculate_speed(b_curr, b_prev)
        if speed_data["speed_kmh"] > fastest["speed_kmh"]:
            fastest["speed_kmh"] = speed_data["speed_kmh"]
            fastest["balloon"] = b_curr
            fastest["speed_data"] = speed_data
            fastest["balloon_index"] = i
    
    return fastest

def get_balloon_speeds(balloons_current: List[Dict], balloons_previous: List[Dict]) -> List[Dict]:
    """Get speeds for all balloons."""
    if not balloons_current or not balloons_previous:
        return []
    
    speeds = []
    for i, (b_curr, b_prev) in enumerate(zip(balloons_current, balloons_previous)):
        speed_data = calculate_speed(b_curr, b_prev)
        balloon_with_speed = {
            **b_curr,
            "speed_kmh": speed_data["speed_kmh"],
            "speed_ms": speed_data["speed_ms"],
            "distance_km": speed_data["distance_km"],
            "balloon_index": i
        }
        speeds.append(balloon_with_speed)
    
    return sorted(speeds, key=lambda x: x["speed_kmh"], reverse=True)

def fastest_balloons_by_country(balloons_current: List[Dict], balloons_previous: List[Dict]) -> Dict:
    """Get fastest balloon in each country."""
    if not balloons_current or not balloons_previous:
        return {}
    
    speeds = get_balloon_speeds(balloons_current, balloons_previous)
    country_fastest = {}
    
    for balloon in speeds:
        country = balloon.get("country", "Unknown")
        if country not in country_fastest or balloon["speed_kmh"] > country_fastest[country]["speed_kmh"]:
            country_fastest[country] = balloon
    
    return country_fastest

# --- Async wrappers for agent ---
async def highest_balloon_tool():
    balloons = format_balloons(await fetch_balloons(0))
    enriched = enrich_with_country(balloons)
    return highest_balloon(enriched)

async def average_altitude_tool():
    balloons = format_balloons(await fetch_balloons(0))
    return average_altitude(enrich_with_country(balloons))

async def fastest_balloon_tool():
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    return fastest_balloon(enrich_with_country(curr), enrich_with_country(prev))

async def balloons_in_country_tool(country: str):
    balloons = format_balloons(await fetch_balloons(0))
    enriched = enrich_with_country(balloons)
    return [b for b in enriched if b["country"].lower() == country.lower()]

async def visited_countries_tool(balloon_id: str) -> list:
    """
    Given a balloon ID, get its current position and determine the country.
    This is a simplified version that just returns the current country.
    """
    try:
        # Get current balloons
        balloons = format_balloons(await fetch_balloons(0))
        enriched = enrich_with_country(balloons)
        
        # Find the balloon by ID (assuming balloon_id is an index)
        if balloon_id.isdigit():
            index = int(balloon_id)
            if 0 <= index < len(enriched):
                balloon = enriched[index]
                return [balloon.get("country", "Unknown")]
        
        return ["Balloon not found"]
    except Exception as e:
        return [f"Error: {str(e)}"]


async def fetch_hurricanes(_=None):
    url = "https://www.nhc.noaa.gov/CurrentStorms.json"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        storms = resp.json().get("storms", [])

    detailed_list = []
    for s in storms:
        # Example: Each storm may have a 'advisoryURL' or 'trackURL'
        adv_url = s.get("advisoryURL")
        if adv_url:
            async with httpx.AsyncClient(timeout=10) as client:
                adv_resp = await client.get(adv_url)
                # Parse JSON or XML depending on API
                adv_data = adv_resp.json()
                detailed_list.append({
                    "name": s.get("name"),
                    "basin": s.get("basin"),
                    "lat": adv_data.get("latitude"),
                    "lon": adv_data.get("longitude"),
                    "advisory": adv_data.get("advisory_number"),
                    # more fields as needed
                })
    return detailed_list

async def fastest_balloon_last2h_tool(*args, **kwargs):
    """
    Returns the balloon that moved the fastest between the last 2 hours.
    Accepts dummy positional arguments because LangChain always passes one.
    """
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    return fastest_balloon(curr, prev)

async def get_all_balloon_speeds_tool():
    """Get speeds for all balloons in the last hour."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    return get_balloon_speeds(enriched_curr, enriched_prev)

async def fastest_balloons_by_country_tool():
    """Get the fastest balloon in each country."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    return fastest_balloons_by_country(enriched_curr, enriched_prev)

async def top_fastest_balloons_tool(limit=10):
    """Get the top N fastest balloons."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    speeds = get_balloon_speeds(enriched_curr, enriched_prev)
    return speeds[:limit]

async def balloon_speed_analysis_tool():
    """Get comprehensive speed analysis including statistics."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    speeds = get_balloon_speeds(enriched_curr, enriched_prev)
    
    if not speeds:
        return {"error": "No speed data available"}
    
    speed_values = [b["speed_kmh"] for b in speeds]
    
    analysis = {
        "total_balloons": len(speeds),
        "fastest_balloon": speeds[0] if speeds else None,
        "slowest_balloon": speeds[-1] if speeds else None,
        "average_speed_kmh": round(sum(speed_values) / len(speed_values), 2),
        "max_speed_kmh": max(speed_values),
        "min_speed_kmh": min(speed_values),
        "top_5_fastest": speeds[:5],
        "countries_with_balloons": len(set(b.get("country", "Unknown") for b in speeds))
    }
    
    return analysis

async def most_distance_covered_tool():
    """Get the balloon that has covered the most distance in the last hour."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    
    if not enriched_curr or not enriched_prev:
        return {"error": "No data available for distance calculation"}
    
    max_distance = 0
    most_traveled_balloon = None
    
    for i, (b_curr, b_prev) in enumerate(zip(enriched_curr, enriched_prev)):
        speed_data = calculate_speed(b_curr, b_prev)
        distance = speed_data["distance_km"]
        
        if distance > max_distance:
            max_distance = distance
            most_traveled_balloon = {
                **b_curr,
                "distance_covered_km": distance,
                "balloon_index": i
            }
    
    return most_traveled_balloon or {"error": "No balloons found"}

async def distance_rankings_tool():
    """Get all balloons ranked by distance covered in the last hour."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    
    if not enriched_curr or not enriched_prev:
        return []
    
    distances = []
    for i, (b_curr, b_prev) in enumerate(zip(enriched_curr, enriched_prev)):
        speed_data = calculate_speed(b_curr, b_prev)
        balloon_with_distance = {
            **b_curr,
            "distance_covered_km": speed_data["distance_km"],
            "balloon_index": i
        }
        distances.append(balloon_with_distance)
    
    return sorted(distances, key=lambda x: x["distance_covered_km"], reverse=True)

# --- Weather Analysis Async Wrappers ---

async def wind_analysis_tool():
    """Analyze wind patterns and directions across all balloons."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    return analyze_wind_patterns(enriched_curr, enriched_prev)

async def atmospheric_anomalies_tool():
    """Detect atmospheric anomalies from balloon behavior patterns."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    return detect_atmospheric_anomalies(enriched_curr, enriched_prev)

async def weather_fronts_tool():
    """Detect potential weather fronts based on balloon movement patterns."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    return detect_weather_fronts(enriched_curr, enriched_prev)

async def comprehensive_weather_analysis_tool():
    """Get comprehensive weather analysis including wind patterns, anomalies, and fronts."""
    curr = format_balloons(await fetch_balloons(0))
    prev = format_balloons(await fetch_balloons(1))
    enriched_curr = enrich_with_country(curr)
    enriched_prev = enrich_with_country(prev)
    
    wind_analysis = analyze_wind_patterns(enriched_curr, enriched_prev)
    anomaly_analysis = detect_atmospheric_anomalies(enriched_curr, enriched_prev)
    front_analysis = detect_weather_fronts(enriched_curr, enriched_prev)
    
    return {
        "timestamp": "Current",
        "wind_patterns": wind_analysis,
        "atmospheric_anomalies": anomaly_analysis,
        "weather_fronts": front_analysis,
        "summary": {
            "total_balloons": len(enriched_curr),
            "anomalies_detected": anomaly_analysis.get("anomalies_detected", 0),
            "potential_fronts": len(front_analysis.get("potential_fronts", [])),
            "average_wind_speed": wind_analysis.get("global_analysis", {}).get("average_wind_speed_kmh", 0)
        }
    }

# --- Weather Analysis Tools ---

def calculate_wind_vector(balloon_current: Dict, balloon_previous: Dict, time_hours: float = 1.0) -> Dict:
    """Calculate wind vector from balloon movement."""
    if not balloon_current or not balloon_previous:
        return {"wind_speed_kmh": 0, "wind_direction_deg": 0, "wind_direction_cardinal": "N/A"}
    
    # Calculate displacement
    dlat = balloon_current["lat"] - balloon_previous["lat"]
    dlon = balloon_current["lon"] - balloon_previous["lon"]
    
    # Convert to km (approximate)
    lat_km = dlat * 111.32  # 1 degree latitude ≈ 111.32 km
    lon_km = dlon * 111.32 * math.cos(math.radians(balloon_current["lat"]))
    
    # Calculate wind speed
    wind_speed_kmh = math.sqrt(lat_km**2 + lon_km**2) / time_hours
    
    # Calculate wind direction (bearing from previous to current position)
    wind_direction_deg = math.degrees(math.atan2(dlon, dlat))
    if wind_direction_deg < 0:
        wind_direction_deg += 360
    
    # Convert to cardinal direction
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    wind_direction_cardinal = directions[int((wind_direction_deg + 11.25) / 22.5) % 16]
    
    return {
        "wind_speed_kmh": round(wind_speed_kmh, 2),
        "wind_direction_deg": round(wind_direction_deg, 1),
        "wind_direction_cardinal": wind_direction_cardinal,
        "displacement_lat_km": round(lat_km, 2),
        "displacement_lon_km": round(lon_km, 2)
    }

def detect_atmospheric_anomalies(balloons_current: List[Dict], balloons_previous: List[Dict]) -> Dict:
    """Detect atmospheric anomalies from balloon behavior patterns."""
    if not balloons_current or not balloons_previous:
        return {"error": "No data available for anomaly detection"}
    
    anomalies = []
    
    # Calculate statistics for comparison
    current_speeds = []
    current_altitudes = []
    wind_vectors = []
    
    for b_curr, b_prev in zip(balloons_current, balloons_previous):
        speed_data = calculate_speed(b_curr, b_prev)
        wind_data = calculate_wind_vector(b_curr, b_prev)
        
        current_speeds.append(speed_data["speed_kmh"])
        current_altitudes.append(b_curr["alt"])
        wind_vectors.append(wind_data["wind_speed_kmh"])
    
    # Calculate thresholds for anomaly detection
    avg_speed = sum(current_speeds) / len(current_speeds)
    avg_altitude = sum(current_altitudes) / len(current_altitudes)
    avg_wind = sum(wind_vectors) / len(wind_vectors)
    
    speed_std = math.sqrt(sum((s - avg_speed)**2 for s in current_speeds) / len(current_speeds))
    altitude_std = math.sqrt(sum((a - avg_altitude)**2 for a in current_altitudes) / len(current_altitudes))
    
    # Detect anomalies
    for i, (b_curr, b_prev) in enumerate(zip(balloons_current, balloons_previous)):
        speed_data = calculate_speed(b_curr, b_prev)
        wind_data = calculate_wind_vector(b_curr, b_prev)
        
        balloon_anomalies = []
        
        # Speed anomaly (2 standard deviations above mean)
        if speed_data["speed_kmh"] > avg_speed + 2 * speed_std:
            balloon_anomalies.append(f"High speed anomaly: {speed_data['speed_kmh']:.1f} km/h")
        
        # Altitude anomaly
        if abs(b_curr["alt"] - avg_altitude) > 2 * altitude_std:
            balloon_anomalies.append(f"Altitude anomaly: {b_curr['alt']:.0f}m (avg: {avg_altitude:.0f}m)")
        
        # Wind anomaly
        if wind_data["wind_speed_kmh"] > avg_wind + 2 * math.sqrt(sum((w - avg_wind)**2 for w in wind_vectors) / len(wind_vectors)):
            balloon_anomalies.append(f"High wind anomaly: {wind_data['wind_speed_kmh']:.1f} km/h")
        
        if balloon_anomalies:
            anomalies.append({
                "balloon_index": i,
                "position": {"lat": b_curr["lat"], "lon": b_curr["lon"], "alt": b_curr["alt"]},
                "country": b_curr.get("country", "Unknown"),
                "anomalies": balloon_anomalies,
                "speed_kmh": speed_data["speed_kmh"],
                "wind_speed_kmh": wind_data["wind_speed_kmh"],
                "wind_direction": wind_data["wind_direction_cardinal"]
            })
    
    return {
        "total_balloons": len(balloons_current),
        "anomalies_detected": len(anomalies),
        "anomaly_rate": round(len(anomalies) / len(balloons_current) * 100, 1),
        "average_speed_kmh": round(avg_speed, 2),
        "average_altitude_m": round(avg_altitude, 0),
        "average_wind_kmh": round(avg_wind, 2),
        "anomalous_balloons": anomalies
    }

def analyze_wind_patterns(balloons_current: List[Dict], balloons_previous: List[Dict]) -> Dict:
    """Analyze wind patterns across different regions."""
    if not balloons_current or not balloons_previous:
        return {"error": "No data available for wind analysis"}
    
    wind_data = []
    country_winds = {}
    
    for b_curr, b_prev in zip(balloons_current, balloons_previous):
        wind_vector = calculate_wind_vector(b_curr, b_prev)
        country = b_curr.get("country", "Unknown")
        
        wind_info = {
            **wind_vector,
            "country": country,
            "altitude": b_curr["alt"],
            "position": {"lat": b_curr["lat"], "lon": b_curr["lon"]}
        }
        wind_data.append(wind_info)
        
        # Group by country
        if country not in country_winds:
            country_winds[country] = []
        country_winds[country].append(wind_info)
    
    # Analyze wind patterns by country
    country_analysis = {}
    for country, winds in country_winds.items():
        if len(winds) > 0:
            avg_wind_speed = sum(w["wind_speed_kmh"] for w in winds) / len(winds)
            wind_directions = [w["wind_direction_deg"] for w in winds]
            
            # Calculate dominant wind direction
            direction_counts = {}
            for direction in wind_directions:
                cardinal = directions[int((direction + 11.25) / 22.5) % 16]
                direction_counts[cardinal] = direction_counts.get(cardinal, 0) + 1
            
            dominant_direction = max(direction_counts, key=direction_counts.get) if direction_counts else "Variable"
            
            country_analysis[country] = {
                "balloon_count": len(winds),
                "average_wind_speed_kmh": round(avg_wind_speed, 2),
                "dominant_direction": dominant_direction,
                "wind_direction_variance": round(math.sqrt(sum((d - sum(wind_directions)/len(wind_directions))**2 for d in wind_directions) / len(wind_directions)), 1)
            }
    
    # Global wind analysis
    all_wind_speeds = [w["wind_speed_kmh"] for w in wind_data]
    all_directions = [w["wind_direction_deg"] for w in wind_data]
    
    return {
        "global_analysis": {
            "total_balloons": len(wind_data),
            "average_wind_speed_kmh": round(sum(all_wind_speeds) / len(all_wind_speeds), 2),
            "max_wind_speed_kmh": round(max(all_wind_speeds), 2),
            "min_wind_speed_kmh": round(min(all_wind_speeds), 2),
            "wind_direction_variance": round(math.sqrt(sum((d - sum(all_directions)/len(all_directions))**2 for d in all_directions) / len(all_directions)), 1)
        },
        "country_analysis": country_analysis,
        "wind_data": wind_data
    }

def detect_weather_fronts(balloons_current: List[Dict], balloons_previous: List[Dict]) -> Dict:
    """Detect potential weather fronts based on balloon movement patterns."""
    if not balloons_current or not balloons_previous:
        return {"error": "No data available for front detection"}
    
    # Group balloons by geographic regions
    regions = {
        "north_america": [],
        "europe": [],
        "asia": [],
        "south_america": [],
        "africa": [],
        "oceania": []
    }
    
    for b_curr, b_prev in zip(balloons_current, balloons_previous):
        lat, lon = b_curr["lat"], b_curr["lon"]
        wind_data = calculate_wind_vector(b_curr, b_prev)
        
        balloon_info = {
            "position": {"lat": lat, "lon": lon, "alt": b_curr["alt"]},
            "wind": wind_data,
            "country": b_curr.get("country", "Unknown")
        }
        
        # Categorize by region
        if 15 <= lat <= 70 and -170 <= lon <= -50:
            regions["north_america"].append(balloon_info)
        elif 35 <= lat <= 70 and -10 <= lon <= 40:
            regions["europe"].append(balloon_info)
        elif 10 <= lat <= 60 and 60 <= lon <= 180:
            regions["asia"].append(balloon_info)
        elif -60 <= lat <= 15 and -90 <= lon <= -30:
            regions["south_america"].append(balloon_info)
        elif -40 <= lat <= 40 and -20 <= lon <= 60:
            regions["africa"].append(balloon_info)
        elif -50 <= lat <= 0 and 110 <= lon <= 180:
            regions["oceania"].append(balloon_info)
    
    # Analyze each region for front-like patterns
    front_analysis = {}
    for region, balloons in regions.items():
        if len(balloons) < 2:
            continue
            
        wind_speeds = [b["wind"]["wind_speed_kmh"] for b in balloons]
        wind_directions = [b["wind"]["wind_direction_deg"] for b in balloons]
        
        # Look for significant wind speed changes (potential fronts)
        speed_variance = math.sqrt(sum((s - sum(wind_speeds)/len(wind_speeds))**2 for s in wind_speeds) / len(wind_speeds))
        avg_speed = sum(wind_speeds) / len(wind_speeds)
        
        # Look for wind direction convergence/divergence
        direction_variance = math.sqrt(sum((d - sum(wind_directions)/len(wind_directions))**2 for d in wind_directions) / len(wind_directions))
        
        front_analysis[region] = {
            "balloon_count": len(balloons),
            "average_wind_speed_kmh": round(avg_speed, 2),
            "wind_speed_variance": round(speed_variance, 2),
            "wind_direction_variance": round(direction_variance, 1),
            "potential_front": speed_variance > avg_speed * 0.5 or direction_variance > 90,
            "front_strength": "Strong" if speed_variance > avg_speed * 0.8 else "Weak" if speed_variance > avg_speed * 0.3 else "None"
        }
    
    return {
        "analysis_timestamp": "Current",
        "regions_analyzed": len([r for r in front_analysis.values() if r["balloon_count"] > 0]),
        "potential_fronts": [region for region, data in front_analysis.items() if data["potential_front"]],
        "regional_analysis": front_analysis
    }

def fetch_wildfires(bbox="-125,25,-66,49", hours=24):
    """
    bbox = minLon, minLat, maxLon, maxLat (default: continental US)
    hours = how many past hours to fetch
    """
    NASA_FIRMS_KEY = os.getenv("NASA_FIRMS_KEY")
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/json/{NASA_FIRMS_KEY}/VIIRS_SNPP_NRT/{bbox}/{hours}"
    resp = requests.get(url, timeout=10)
    data = resp.json()

    fires = []
    for f in data.get("features", []):
        props = f["properties"]
        fires.append({
            "lat": f["geometry"]["coordinates"][1],
            "lon": f["geometry"]["coordinates"][0],
            "brightness": props.get("bright_ti4"),
            "confidence": props.get("confidence"),
            "acq_time": props.get("acq_time")
        })
    return fires