import { useState, useEffect } from 'react';
import { 
  Globe, 
  TrendingUp, 
  Zap, 
  MapPin, 
  Wind, 
  Flame, 
  Activity,
  RefreshCw,
  AlertCircle
} from 'lucide-react';
import { balloonAPI } from '../services/api';

const Dashboard = ({ onQuickAction }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    checkConnection();
    setLastUpdate(new Date());
  }, []);

  const checkConnection = async () => {
    try {
      await balloonAPI.healthCheck();
      setIsConnected(true);
    } catch (error) {
      setIsConnected(false);
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await checkConnection();
    setLastUpdate(new Date());
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  const quickActions = [
    {
      title: 'Fastest Balloon',
      description: 'Find the balloon moving fastest right now',
      icon: Zap,
      color: 'from-yellow-500 to-orange-600',
      action: 'Which balloon is currently moving the fastest?'
    },
    {
      title: 'Speed Analysis',
      description: 'Comprehensive speed statistics and rankings',
      icon: TrendingUp,
      color: 'from-green-500 to-emerald-600',
      action: 'Give me a complete speed analysis of all balloons'
    },
    {
      title: 'Fastest by Country',
      description: 'Fastest balloon in each country',
      icon: MapPin,
      color: 'from-blue-500 to-cyan-600',
      action: 'Which country has the fastest balloon?'
    },
    {
      title: 'Top 10 Fastest',
      description: 'Ranking of the 10 fastest balloons',
      icon: Activity,
      color: 'from-purple-500 to-pink-600',
      action: 'Show me the top 10 fastest balloons'
    },
    {
      title: 'Most Distance',
      description: 'Balloon that covered most distance in past hour',
      icon: Globe,
      color: 'from-emerald-500 to-teal-600',
      action: 'Which balloon has covered the most distance in the past hour?'
    },
    {
      title: 'Weather Anomalies',
      description: 'Detect atmospheric anomalies and unusual patterns',
      icon: AlertCircle,
      color: 'from-red-500 to-orange-600',
      action: 'Detect any atmospheric anomalies or unusual weather patterns'
    },
    {
      title: 'Weather Fronts',
      description: 'Detect potential weather fronts',
      icon: Activity,
      color: 'from-indigo-500 to-purple-600',
      action: 'Are there any potential weather fronts detected?'
    },
    {
      title: 'Highest Balloon',
      description: 'Find the balloon at highest altitude',
      icon: TrendingUp,
      color: 'from-indigo-500 to-blue-600',
      action: 'What is the highest balloon currently?'
    },
    {
      title: 'Balloons by Country',
      description: 'Find balloons in specific countries',
      icon: Globe,
      color: 'from-cyan-500 to-teal-600',
      action: 'Show me balloons in the United States'
    },
    {
      title: 'Active Hurricanes',
      description: 'Current hurricane tracking data',
      icon: Wind,
      color: 'from-red-500 to-rose-600',
      action: 'Show me current active hurricanes'
    },
    {
      title: 'Wildfire Data',
      description: 'Recent wildfire detection',
      icon: Flame,
      color: 'from-orange-500 to-red-600',
      action: 'Show me recent wildfires in the US'
    }
  ];

  const stats = [
    {
      title: 'Global Coverage',
      value: 'Worldwide',
      icon: Globe,
      color: 'text-blue-400'
    },
    {
      title: 'Real-time Data',
      value: 'Live Updates',
      icon: Activity,
      color: 'text-green-400'
    },
    {
      title: 'Data Sources',
      value: 'Multiple APIs',
      icon: RefreshCw,
      color: 'text-purple-400'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Windborne Dashboard</h1>
          <p className="text-gray-300 mt-1">Real-time balloon tracking and weather intelligence</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`} />
            <span className="text-sm text-gray-300">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="btn-secondary flex items-center space-x-2"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="card">
            <div className="flex items-center space-x-3">
              <stat.icon className={`w-8 h-8 ${stat.color}`} />
              <div>
                <p className="text-sm text-gray-300">{stat.title}</p>
                <p className="text-lg font-semibold text-white">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((action, index) => (
            <div
              key={index}
              className="card hover:bg-white/20 transition-all duration-200 cursor-pointer group"
              onClick={() => {
                if (onQuickAction) {
                  onQuickAction(action.action);
                }
              }}
            >
              <div className="flex items-start space-x-3">
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${action.color} flex items-center justify-center group-hover:scale-110 transition-transform duration-200`}>
                  <action.icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-white group-hover:text-blue-300 transition-colors">
                    {action.title}
                  </h3>
                  <p className="text-sm text-gray-300 mt-1">
                    {action.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Status Alert */}
      {!isConnected && (
        <div className="card border-red-500/30 bg-red-500/10">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-6 h-6 text-red-400" />
            <div>
              <h3 className="font-semibold text-red-400">Backend Connection Lost</h3>
              <p className="text-sm text-red-300">
                Unable to connect to the Windborne agent backend. Please check if the server is running.
              </p>
            </div>
          </div>
        </div>
      )}

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

export default Dashboard;
