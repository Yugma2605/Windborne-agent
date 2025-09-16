import { useState } from 'react';
import { 
  Home, 
  MessageSquare, 
  Map, 
  Menu, 
  X,
  Wind
} from 'lucide-react';

const Navigation = ({ activeTab, setActiveTab }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: Home,
      description: 'Overview and quick actions'
    },
    {
      id: 'chat',
      label: 'Agent Chat',
      icon: MessageSquare,
      description: 'Talk to the Windborne agent'
    },
    {
      id: 'map',
      label: 'Map',
      icon: Map,
      description: 'Balloon tracking map'
    },
  ];

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 glass p-2 rounded-lg"
      >
        {isMobileMenuOpen ? (
          <X className="w-6 h-6 text-white" />
        ) : (
          <Menu className="w-6 h-6 text-white" />
        )}
      </button>

      {/* Navigation Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-40 w-64 glass transform transition-transform duration-300 ease-in-out
        ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 lg:static lg:inset-0
      `}>
        {/* Logo */}
        <div className="p-6 border-b border-white/20">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <Wind className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Windborne</h1>
              <p className="text-sm text-gray-300">Balloon Tracking</p>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-4 space-y-2">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                setActiveTab(item.id);
                setIsMobileMenuOpen(false);
              }}
              className={`
                w-full flex items-center space-x-3 p-3 rounded-lg transition-all duration-200
                ${activeTab === item.id
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                  : 'text-gray-300 hover:bg-white/10 hover:text-white'
                }
              `}
            >
              <item.icon className="w-5 h-5" />
              <div className="text-left">
                <div className="font-medium">{item.label}</div>
                <div className="text-xs opacity-75">{item.description}</div>
              </div>
            </button>
          ))}
        </nav>

        {/* Footer */}
        <div className="absolute bottom-4 left-4 right-4">
          <div className="glass rounded-lg p-3">
            <p className="text-xs text-gray-400 text-center">
              Powered by Windborne Systems
            </p>
          </div>
        </div>
      </div>

      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </>
  );
};

export default Navigation;
