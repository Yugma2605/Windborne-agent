# balloons/enricher.py
import geopandas as gpd
from shapely.geometry import Point

# Load world countries once
WORLD = gpd.read_file("data/items.json").to_crs(epsg=4326)

def enrich_balloons(balloons):
    """
    Enrich balloons with country info.
    """
    points = gpd.GeoDataFrame(
        balloons,
        geometry=[Point(b["lon"], b["lat"]) for b in balloons],
        crs="EPSG:4326"
    )

    # Spatial join: balloons with countries
    joined = gpd.sjoin(points, WORLD, how="left", predicate="within")

    enriched = []
    for _, row in joined.iterrows():
        enriched.append({
            "id": row["id"],
            "lat": row["lat"],
            "lon": row["lon"],
            "altitude": row["altitude"],
            "country": row["NAME"] if row["NAME"] else "Unknown"
        })
    return enriched
