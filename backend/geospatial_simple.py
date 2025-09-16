"""
Ultra-simple geospatial utilities with zero external dependencies.
Provides basic country detection using a simple approach.
"""
import json
from typing import List, Dict, Optional


def point_in_polygon_simple(point_x: float, point_y: float, polygon_coords: List[List[float]]) -> bool:
    """
    Simple ray casting algorithm for point-in-polygon test.
    Pure Python, no external dependencies.
    """
    x, y = point_x, point_y
    n = len(polygon_coords)
    inside = False
    
    p1x, p1y = polygon_coords[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_coords[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


class SimpleCountryFinder:
    """Simple country finder with zero external dependencies."""
    
    def __init__(self, geojson_path: str):
        """Initialize with GeoJSON file containing country boundaries."""
        self.countries = self._load_countries(geojson_path)
    
    def _load_countries(self, geojson_path: str) -> List[Dict]:
        """Load countries from GeoJSON file."""
        try:
            with open(geojson_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {geojson_path} not found, using fallback")
            return []
        
        countries = []
        for feature in data['features']:
            geometry = feature['geometry']
            properties = feature['properties']
            
            # Get country name from properties
            country_name = properties.get('NAME') or properties.get('ADMIN') or properties.get('name', 'Unknown')
            
            # Store coordinates based on geometry type
            if geometry['type'] == 'Polygon':
                coords = geometry['coordinates']
                countries.append({
                    'name': country_name,
                    'type': 'polygon',
                    'coordinates': coords
                })
            elif geometry['type'] == 'MultiPolygon':
                coords = geometry['coordinates']
                countries.append({
                    'name': country_name,
                    'type': 'multipolygon',
                    'coordinates': coords
                })
        
        return countries
    
    def find_country(self, lat: float, lon: float) -> str:
        """Find the country for a given latitude and longitude."""
        for country in self.countries:
            if country['type'] == 'polygon':
                # Handle single polygon
                for polygon_coords in country['coordinates']:
                    if point_in_polygon_simple(lon, lat, polygon_coords):
                        return country['name']
            elif country['type'] == 'multipolygon':
                # Handle multipolygon
                for polygon_group in country['coordinates']:
                    for polygon_coords in polygon_group:
                        if point_in_polygon_simple(lon, lat, polygon_coords):
                            return country['name']
        
        return "Unknown"


# Global instance - will be initialized when needed
_simple_country_finder: Optional[SimpleCountryFinder] = None


def get_simple_country_finder() -> SimpleCountryFinder:
    """Get or create the global simple country finder instance."""
    global _simple_country_finder
    if _simple_country_finder is None:
        _simple_country_finder = SimpleCountryFinder("data/items.json")
    return _simple_country_finder


def find_country_for_point_simple(lat: float, lon: float) -> str:
    """Find the country for a given latitude and longitude using simple approach."""
    finder = get_simple_country_finder()
    return finder.find_country(lat, lon)
