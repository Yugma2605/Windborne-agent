"""
Fallback geospatial utilities that tries Shapely first, then falls back to pure Python.
"""
import os
import sys

# Try to import Shapely, fall back to pure Python if it fails
try:
    from geospatial import find_country_for_point as _shapely_find_country
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False
    print("Shapely not available, using pure Python fallback")

try:
    from geospatial_pure import find_country_for_point_pure as _pure_find_country
    PURE_AVAILABLE = True
except ImportError:
    PURE_AVAILABLE = False
    print("Pure Python fallback not available")


def find_country_for_point(lat: float, lon: float) -> str:
    """
    Find country for a point, using Shapely if available, otherwise pure Python.
    """
    if SHAPELY_AVAILABLE:
        try:
            return _shapely_find_country(lat, lon)
        except Exception as e:
            print(f"Shapely failed: {e}, falling back to pure Python")
            if PURE_AVAILABLE:
                return _pure_find_country(lat, lon)
            else:
                return "Unknown"
    elif PURE_AVAILABLE:
        return _pure_find_country(lat, lon)
    else:
        print("No geospatial libraries available, returning Unknown")
        return "Unknown"
