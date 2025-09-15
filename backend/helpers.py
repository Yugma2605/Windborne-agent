# helpers.py

STATE_BBOXES = {
    "texas": {"lat_min": 25.8, "lat_max": 36.5, "lon_min": -106.6, "lon_max": -93.5},
    "arizona": {"lat_min": 31.3, "lat_max": 37.0, "lon_min": -114.8, "lon_max": -109.0},
    # Add more states...
}

def balloons_in_region(balloons, state_name):
    bbox = STATE_BBOXES.get(state_name.lower())
    if not bbox:
        return balloons  # return all if unknown

    filtered = [
        b for b in balloons
        if bbox["lat_min"] <= b[0] <= bbox["lat_max"]  # latitude
        and bbox["lon_min"] <= b[1] <= bbox["lon_max"]  # longitude
    ]
    return filtered

def average_altitude(balloons):
    if not balloons:
        return 0
    return sum(b[2] for b in balloons) / len(balloons)

def highest_balloon(balloons):
    if not balloons:
        return None
    highest = max(balloons, key=lambda x: x[2])
    return {"id": balloons.index(highest), "lat": highest[0], "lon": highest[1], "altitude": highest[2]}

def fastest_balloon(current, previous):
    if not current or not previous:
        return None, 0
    speeds = []
    for i, b in enumerate(current):
        if i < len(previous):
            prev = previous[i]
            # Rough 2D distance / delta t (assuming 1 hour)
            dist = ((b[0]-prev[0])**2 + (b[1]-prev[1])**2)**0.5
            speeds.append((i, dist))
    if not speeds:
        return None, 0
    fastest = max(speeds, key=lambda x: x[1])
    return fastest  # returns index and speed
