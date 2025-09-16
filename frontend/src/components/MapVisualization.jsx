import { useState, useEffect, useCallback } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Icon } from 'leaflet';
import { 
  MapPin, 
  RefreshCw, 
  Zap, 
  Activity,
  Globe,
  Clock
} from 'lucide-react';
import { balloonAPI } from '../services/api';

// Fix for default markers in react-leaflet
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Simple, small balloon icon
const createBalloonIcon = (altitude, isHighest) => {
  // Color based on altitude: higher altitude = more red/orange
  let color = '#22c55e'; // green for low altitude
  if (altitude > 15) color = '#ef4444'; // red for high altitude
  else if (altitude > 10) color = '#f97316'; // orange for medium-high
  else if (altitude > 5) color = '#eab308'; // yellow for medium
  
  // Create SVG string with proper encoding
  const svgString = `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="8" cy="8" r="6" fill="${color}" stroke="white" stroke-width="1"/>
    <circle cx="8" cy="8" r="3" fill="white" opacity="0.8"/>
    ${isHighest ? '<text x="8" y="10" text-anchor="middle" fill="white" font-size="6" font-weight="bold">★</text>' : ''}
  </svg>`;
  
  // Use encodeURIComponent instead of btoa to avoid encoding issues
  const encodedSvg = encodeURIComponent(svgString);
  
  return new Icon({
    iconUrl: `data:image/svg+xml;charset=utf-8,${encodedSvg}`,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
    popupAnchor: [0, -8]
  });
};

const MapVisualization = () => {
  const [balloons, setBalloons] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [error, setError] = useState(null);

  // Cache management functions
  const getCachedData = () => {
    try {
      const cached = localStorage.getItem('windborne_balloons_cache');
      if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        const now = Date.now();
        const thirtyMinutes = 30 * 60 * 1000; // 30 minutes in milliseconds
        
        // Check if cache is still valid (less than 30 minutes old)
        if (now - timestamp < thirtyMinutes) {
          console.log('Using cached data (age:', Math.round((now - timestamp) / 60000), 'minutes)');
          return data;
        } else {
          console.log('Cache expired, will fetch new data');
          localStorage.removeItem('windborne_balloons_cache');
        }
      }
    } catch (error) {
      console.error('Error reading cache:', error);
      localStorage.removeItem('windborne_balloons_cache');
    }
    return null;
  };

  const setCachedData = (data) => {
    try {
      const cacheData = {
        data,
        timestamp: Date.now()
      };
      localStorage.setItem('windborne_balloons_cache', JSON.stringify(cacheData));
      console.log('Data cached successfully');
    } catch (error) {
      console.error('Error caching data:', error);
    }
  };

  const fetchBalloons = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    // First, try to get cached data
    const cachedData = getCachedData();
    if (cachedData) {
      console.log('Using cached data:', cachedData.length, 'balloons');
      processBalloonData(cachedData);
      setIsLoading(false);
      return;
    }
    
    try {
      console.log('Fetching balloons from backend API...');
      const response = await balloonAPI.get('/balloons');
      
      const apiResponse = response.data;
      console.log('Backend API response:', apiResponse);
      
      if (apiResponse.error) {
        throw new Error(apiResponse.error);
      }
      
      const data = apiResponse.balloons;
      console.log('Balloon data received:', data.length, 'balloons');
      
      // Cache the data
      setCachedData(data);
      
      processBalloonData(data);
    } catch (error) {
      console.error('Failed to fetch balloons:', error);
      setError(error.message);
      
      // Try to use cached data even if expired
      const expiredCache = localStorage.getItem('windborne_balloons_cache');
      if (expiredCache) {
        try {
          const { data } = JSON.parse(expiredCache);
          console.log('Using expired cache as fallback');
          processBalloonData(data);
          setError('Using cached data (API unavailable)');
        } catch (cacheError) {
          console.error('Error reading expired cache:', cacheError);
          // Fallback to mock data
          useMockData();
        }
      } else {
        // Fallback to mock data
        useMockData();
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const processBalloonData = (data) => {
    // Backend already provides data in the correct format
    const parsedBalloons = data.map((balloon) => ({
      ...balloon,
      lastUpdate: new Date(balloon.lastUpdate || new Date())
    }));
    
    console.log('Processed balloons:', parsedBalloons.length);
    setBalloons(parsedBalloons);
    setLastUpdate(new Date());
  };

  const useMockData = () => {
    console.log('Using mock data as fallback');
    const mockBalloons = [
      { id: 'B001', lat: 40.7128, lng: -74.0060, speed: 25.3, altitude: 12.5, country: 'United States', city: 'New York', lastUpdate: new Date() },
      { id: 'B002', lat: 51.5074, lng: -0.1278, speed: 18.7, altitude: 8.2, country: 'United Kingdom', city: 'London', lastUpdate: new Date() },
      { id: 'B003', lat: 35.6762, lng: 139.6503, speed: 32.1, altitude: 15.8, country: 'Japan', city: 'Tokyo', lastUpdate: new Date() },
      { id: 'B004', lat: -33.8688, lng: 151.2093, speed: 22.4, altitude: 9.1, country: 'Australia', city: 'Sydney', lastUpdate: new Date() },
      { id: 'B005', lat: 55.7558, lng: 37.6176, speed: 28.9, altitude: 11.3, country: 'Russia', city: 'Moscow', lastUpdate: new Date() }
    ];
    setBalloons(mockBalloons);
    setLastUpdate(new Date());
  };

  useEffect(() => {
    fetchBalloons();
  }, [fetchBalloons]);

  const getSpeedColor = (speed) => {
    if (speed > 30) return 'text-red-400';
    if (speed > 20) return 'text-orange-400';
    if (speed > 10) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getAltitudeColor = (altitude) => {
    if (altitude > 15) return 'text-red-400';
    if (altitude > 10) return 'text-orange-400';
    if (altitude > 5) return 'text-yellow-400';
    return 'text-green-400';
  };

  const fastestBalloon = balloons.reduce((fastest, current) => 
    current.speed > fastest.speed ? current : fastest, balloons[0] || { speed: 0 }
  );

  const highestBalloon = balloons.reduce((highest, current) => 
    current.altitude > highest.altitude ? current : highest, balloons[0] || { altitude: 0 }
  );

  // Display all balloons
  const displayBalloons = balloons;

  return (
    <div className="space-y-6 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Balloon Map</h1>
          <p className="text-gray-300 mt-1">Real-time balloon tracking across the globe</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-green-400" />
            <span className="text-sm text-gray-300">
              {balloons.length} Balloons Displayed
            </span>
          </div>
          <button
            onClick={fetchBalloons}
            disabled={isLoading}
            className="btn-primary flex items-center space-x-2"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="card border-red-500/30 bg-red-500/10">
          <div className="flex items-center space-x-3">
            <div className="w-6 h-6 text-red-400">⚠️</div>
            <div>
              <h3 className="font-semibold text-red-400">API Error</h3>
              <p className="text-sm text-red-300">{error}</p>
              <p className="text-xs text-red-300 mt-1">Using cached or mock data</p>
            </div>
          </div>
        </div>
      )}


      {/* Map Container */}
      <div className="flex-1 min-h-0">
        <div className="h-full rounded-xl overflow-hidden border border-white/20 bg-gray-800">
          <div style={{ height: 'calc(100vh - 300px)', width: '100%', minHeight: '500px' }}>
            <MapContainer
              center={[20, 0]}
              zoom={2}
              style={{ height: '100%', width: '100%' }}
              zoomControl={true}
              scrollWheelZoom={true}
              doubleClickZoom={true}
              dragging={true}
              maxZoom={18}
              minZoom={1}
              worldCopyJump={false}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                noWrap={true}
                bounds={[[-85, -180], [85, 180]]}
              />
              
              {displayBalloons.map((balloon) => (
                <Marker
                  key={balloon.id}
                  position={[balloon.lat, balloon.lng]}
                  icon={createBalloonIcon(balloon.altitude, balloon.id === highestBalloon?.id)}
                >
                  <Popup>
                    <div className="p-2 min-w-[180px]">
                      <div className="flex items-center space-x-2 mb-2">
                        <MapPin className="w-4 h-4 text-blue-500" />
                        <span className="font-semibold text-gray-800">{balloon.id}</span>
                        {balloon.id === highestBalloon?.id && (
                          <span className="text-xs bg-yellow-100 text-yellow-800 px-1 py-0.5 rounded">Highest</span>
                        )}
                      </div>
                      <div className="space-y-1 text-xs">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Location:</span>
                          <span className="text-gray-800">{balloon.city}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Altitude:</span>
                          <span className={`font-medium ${getAltitudeColor(balloon.altitude)}`}>
                            {balloon.altitude.toFixed(2)} km
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Speed:</span>
                          <span className={`font-medium ${getSpeedColor(balloon.speed)}`}>
                            {balloon.speed.toFixed(1)} km/h
                          </span>
                        </div>
                      </div>
                    </div>
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center space-x-3">
            <Globe className="w-6 h-6 text-blue-400" />
            <div>
              <p className="text-sm text-gray-300">Total Balloons</p>
              <p className="text-lg font-semibold text-white">{balloons.length}</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center space-x-3">
            <Activity className="w-6 h-6 text-green-400" />
            <div>
              <p className="text-sm text-gray-300">Highest Balloon</p>
              <p className="text-lg font-semibold text-white">
                {highestBalloon ? `${highestBalloon.id} (${highestBalloon.altitude.toFixed(2)} km)` : 'N/A'}
              </p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center space-x-3">
            <Zap className="w-6 h-6 text-yellow-400" />
            <div>
              <p className="text-sm text-gray-300">Fastest Balloon</p>
              <p className="text-lg font-semibold text-white">
                {fastestBalloon ? `${fastestBalloon.id} (${fastestBalloon.speed.toFixed(1)} km/h)` : 'N/A'}
              </p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center space-x-3">
            <MapPin className="w-6 h-6 text-purple-400" />
            <div>
              <p className="text-sm text-gray-300">Countries Covered</p>
              <p className="text-lg font-semibold text-white">
                {new Set(balloons.map(b => b.country)).size}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Last Update */}
      {lastUpdate && (
        <div className="text-center">
          <p className="text-sm text-gray-400">
            Last updated: {lastUpdate.toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
};

export default MapVisualization;
