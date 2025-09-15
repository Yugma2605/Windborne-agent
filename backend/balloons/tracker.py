# balloons/tracker.py
from collections import defaultdict

# Memory store for visited countries (replace with Redis/DB in prod)
visited_countries = defaultdict(set)

def update_visited(balloons):
    """
    Updates visited countries for each balloon.
    """
    for b in balloons:
        if b["country"] and b["country"] != "Unknown":
            visited_countries[b["id"]].add(b["country"])

def get_visited_countries(balloon_id):
    """
    Get all countries a balloon has traveled to.
    """
    return list(visited_countries[balloon_id])
