# balloons/enricher.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geospatial_simple import find_country_for_point_simple

def enrich_balloons(balloons):
    """
    Enrich balloons with country info using simple geospatial operations.
    """
    enriched = []
    for balloon in balloons:
        # Find country for this balloon's coordinates
        country = find_country_for_point_simple(balloon["lat"], balloon["lon"])
        
        enriched.append({
            "id": balloon.get("id", ""),
            "lat": balloon["lat"],
            "lon": balloon["lon"],
            "altitude": balloon.get("altitude", balloon.get("alt", 0)),
            "country": country
        })
    return enriched
