"""
Lightweight country detection for balloon coordinates.
Uses free reverse geocoding API with caching to avoid rate limits.
"""
import json
import time
from typing import Dict, Optional
import httpx
import os

class CountryDetector:
    """Lightweight country detector with caching."""
    
    def __init__(self, cache_file: str = "data/country_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.api_delay = 0.1  # 100ms delay between API calls to be respectful
    
    def _load_cache(self) -> Dict:
        """Load country cache from file."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load country cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save country cache to file."""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
        except Exception as e:
            print(f"Warning: Could not save country cache: {e}")
    
    def _get_cache_key(self, lat: float, lon: float) -> str:
        """Generate cache key for coordinates (rounded to 2 decimal places)."""
        return f"{round(lat, 2)},{round(lon, 2)}"
    
    async def get_country(self, lat: float, lon: float) -> str:
        """Get country for given coordinates."""
        cache_key = self._get_cache_key(lat, lon)
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Try multiple free APIs
        country = await self._fetch_country_from_api(lat, lon)
        
        # Cache the result
        self.cache[cache_key] = country
        self._save_cache()
        
        return country
    
    async def _fetch_country_from_api(self, lat: float, lon: float) -> str:
        """Fetch country from free reverse geocoding API."""
        # Try multiple free APIs in order of preference
        apis = [
            self._try_nominatim_api,
            self._try_bigdatacloud_api,
            self._try_geocode_xyz_api
        ]
        
        for api_func in apis:
            try:
                country = await api_func(lat, lon)
                if country and country != "Unknown":
                    return country
            except Exception as e:
                print(f"API failed: {e}")
                continue
        
        return "Unknown"
    
    async def _try_nominatim_api(self, lat: float, lon: float) -> str:
        """Try OpenStreetMap Nominatim API (free, no key required)."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = f"https://nominatim.openstreetmap.org/reverse"
            params = {
                "lat": lat,
                "lon": lon,
                "format": "json",
                "addressdetails": 1
            }
            headers = {"User-Agent": "Windborne-Balloon-Tracker/1.0"}
            
            response = await client.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get("address", {}).get("country", "Unknown")
        
        return "Unknown"
    
    async def _try_bigdatacloud_api(self, lat: float, lon: float) -> str:
        """Try BigDataCloud API (free tier available)."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = f"https://api.bigdatacloud.net/data/reverse-geocode-client"
            params = {"latitude": lat, "longitude": lon, "localityLanguage": "en"}
            
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("countryName", "Unknown")
        
        return "Unknown"
    
    async def _try_geocode_xyz_api(self, lat: float, lon: float) -> str:
        """Try GeoCode.xyz API (free tier available)."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = f"https://geocode.xyz/{lat},{lon}"
            params = {"json": 1}
            
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("country", "Unknown")
        
        return "Unknown"

# Global instance
_country_detector = None

def get_country_detector() -> CountryDetector:
    """Get or create the global country detector instance."""
    global _country_detector
    if _country_detector is None:
        _country_detector = CountryDetector()
    return _country_detector

async def get_country_for_coordinates(lat: float, lon: float) -> str:
    """Get country for given coordinates."""
    detector = get_country_detector()
    return await detector.get_country(lat, lon)
