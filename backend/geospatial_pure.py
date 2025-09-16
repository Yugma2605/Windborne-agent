"""
Pure Python geospatial utilities - no external dependencies.
Provides point-in-polygon functionality for country detection.
"""
import json
from typing import List, Dict, Optional


def point_in_polygon(point_x: float, point_y: float, polygon_coords: List[List[float]]) -> bool:
    """
    Ray casting algorithm to determine if a point is inside a polygon.
    Pure Python implementation - no external dependencies.
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


def point_in_multipolygon(point_x: float, point_y: float, multipolygon_coords: List[List[List[List[float]]]]) -> bool:
    """
    Check if a point is inside any polygon in a multipolygon.
    """
    for polygon_group in multipolygon_coords:
        for polygon_coords in polygon_group:
            if point_in_polygon(point_x, point_y, polygon_coords):
                return True
    return False


class PureCountryFinder:
    """Pure Python country finder with no external dependencies."""
    
    def __init__(self, geojson_path: str):
        """Initialize with GeoJSON file containing country boundaries."""
        self.countries = self._load_countries(geojson_path)
    
    def _load_countries(self, geojson_path: str) -> List[Dict]:
        """Load countries from GeoJSON file."""
        with open(geojson_path, 'r') as f:
            data = json.load(f)
        
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
                    if point_in_polygon(lon, lat, polygon_coords):
                        return country['name']
            elif country['type'] == 'multipolygon':
                # Handle multipolygon
                if point_in_multipolygon(lon, lat, country['coordinates']):
                    return country['name']
        
        return "Unknown"


# Global instance - will be initialized when needed
_pure_country_finder: Optional[PureCountryFinder] = None


def get_pure_country_finder() -> PureCountryFinder:
    """Get or create the global pure country finder instance."""
    global _pure_country_finder
    if _pure_country_finder is None:
        _pure_country_finder = PureCountryFinder("data/items.json")
    return _pure_country_finder


def find_country_for_point_pure(lat: float, lon: float) -> str:
    """Find the country for a given latitude and longitude using pure Python."""
    finder = get_pure_country_finder()
    return finder.find_country(lat, lon)
