import { useState, useEffect } from 'react';
import Navigation from './components/Navigation';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import MapVisualization from './components/MapVisualization';
import Settings from './components/Settings';
import { balloonAPI } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isConnected, setIsConnected] = useState(false);
  const [prefilledMessage, setPrefilledMessage] = useState('');

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      await balloonAPI.healthCheck();
      setIsConnected(true);
    } catch (error) {
      setIsConnected(false);
    }
  };

  const handleQuickAction = (message) => {
    setPrefilledMessage(message);
    setActiveTab('chat');
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard onQuickAction={handleQuickAction} />;
      case 'chat':
        return <ChatInterface prefilledMessage={prefilledMessage} onMessageSent={() => setPrefilledMessage('')} />;
      case 'map':
        return <MapVisualization />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard onQuickAction={handleQuickAction} />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="flex h-screen">
        {/* Navigation Sidebar */}
        <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
        
        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden lg:ml-0">
          {/* Top Bar */}
          <div className="glass border-b border-white/20 p-4 lg:hidden">
            <div className="flex items-center justify-between">
              <h1 className="text-xl font-bold text-white">Windborne</h1>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`} />
                <span className="text-sm text-gray-300">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>
          </div>
          
          {/* Content Area */}
          <main className="flex-1 overflow-y-auto p-6">
            {renderContent()}
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
