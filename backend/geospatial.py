"""
Lightweight geospatial utilities to replace GeoPandas.
Provides point-in-polygon functionality for country detection.
"""
import json
from typing import List, Dict, Optional
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.prepared import prep


class CountryFinder:
    """Lightweight country finder using Shapely for point-in-polygon operations."""
    
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
            
            # Convert geometry to Shapely objects
            if geometry['type'] == 'Polygon':
                coords = geometry['coordinates'][0]  # Exterior ring
                polygon = Polygon(coords)
            elif geometry['type'] == 'MultiPolygon':
                polygons = []
                for poly_coords in geometry['coordinates']:
                    polygons.append(Polygon(poly_coords[0]))  # Exterior ring of each polygon
                polygon = MultiPolygon(polygons)
            else:
                continue  # Skip unsupported geometry types
            
            # Create prepared geometry for faster point-in-polygon tests
            prepared = prep(polygon)
            
            countries.append({
                'name': country_name,
                'geometry': polygon,
                'prepared': prepared
            })
        
        return countries
    
    def find_country(self, lat: float, lon: float) -> str:
        """Find the country for a given latitude and longitude."""
        point = Point(lon, lat)  # Note: Shapely uses (x, y) = (lon, lat)
        
        for country in self.countries:
            if country['prepared'].contains(point):
                return country['name']
        
        return "Unknown"


# Global instance - will be initialized when needed
_country_finder: Optional[CountryFinder] = None


def get_country_finder() -> CountryFinder:
    """Get or create the global country finder instance."""
    global _country_finder
    if _country_finder is None:
        _country_finder = CountryFinder("data/items.json")
    return _country_finder


def find_country_for_point(lat: float, lon: float) -> str:
    """Find the country for a given latitude and longitude."""
    finder = get_country_finder()
    return finder.find_country(lat, lon)
