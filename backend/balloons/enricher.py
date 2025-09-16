# balloons/enricher.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geospatial import find_country_for_point

def enrich_balloons(balloons):
    """
    Enrich balloons with country info using lightweight geospatial operations.
    """
    enriched = []
    for balloon in balloons:
        # Find country for this balloon's coordinates
        country = find_country_for_point(balloon["lat"], balloon["lon"])
        
        enriched.append({
            "id": balloon.get("id", ""),
            "lat": balloon["lat"],
            "lon": balloon["lon"],
            "altitude": balloon.get("altitude", balloon.get("alt", 0)),
            "country": country
        })
    return enriched
