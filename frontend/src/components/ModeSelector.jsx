export function ModeSelector({ currentMode, onModeChange, displayMode, onDisplayModeChange }) {
  const modes = [
    { id: 'simulation', name: 'Simulation Mode', description: 'Real-time simulation for demonstration' },
    { id: 'real_model', name: 'Real XGBoost Model', description: 'Actual XGBoost v5 predictions on real data' }
  ];

  const displayModes = [
    { id: 'all', name: 'All Transactions', description: 'Show every transaction (⚪ circles for legitimate)' },
    { id: 'interesting', name: 'Interesting Only', description: 'Only show fraud-related transactions (✅❌⚠️)' }
  ];

  return (
    <div className="bg-gray-800 rounded-xl p-4 mb-6">
      {/* Detection Mode Selection */}
      <div className="mb-4">
        <h3 className="text-sm text-gray-400 mb-2">Detection Mode</h3>
        <div className="flex space-x-4">
          {modes.map(mode => (
            <button
              key={mode.id}
              onClick={() => onModeChange(mode.id)}
              className={`px-4 py-2 rounded-lg font-semibold flex-1 ${
                currentMode === mode.id 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {mode.name}
            </button>
          ))}
        </div>
        
        {/* Mode Description */}
        <div className="mt-2 text-sm text-gray-300">
          {modes.map(mode => (
            <div 
              key={mode.id} 
              className={`${currentMode === mode.id ? '' : 'hidden'}`}
            >
              <p>{mode.description}</p>
              {mode.id === 'real_model' && (
                <p className="text-xs text-gray-400 mt-1">
                  <strong>Performance:</strong> 39.7% detection @ 8.8% false alarms • 
                  <strong> AUC:</strong> 0.77 • 
                  <strong> Features:</strong> 22
                </p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Display Mode Selection */}
      <div>
        <h3 className="text-sm text-gray-400 mb-2">Display Mode</h3>
        <div className="flex space-x-4">
          {displayModes.map(mode => (
            <button
              key={mode.id}
              onClick={() => onDisplayModeChange(mode.id)}
              className={`px-4 py-2 rounded-lg font-semibold flex-1 ${
                displayMode === mode.id 
                  ? 'bg-purple-600 text-white' 
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {mode.name}
            </button>
          ))}
        </div>
        
        {/* Display Mode Description */}
        <div className="mt-2 text-sm text-gray-300 p-2 bg-gray-900/50 rounded-lg">
          {displayMode === 'all' ? (
            <p>Showing <span className="text-blue-400">all transactions</span>: ⚪ legitimate, ✅ detected fraud, ❌ missed fraud, ⚠️ false alarms</p>
          ) : (
            <p>Showing <span className="text-purple-400">interesting only</span>: Only fraud-related transactions (✅❌⚠️) - cleaner view</p>
          )}
        </div>
      </div>

      {/* Model Info Panel for Real Model */}
      {currentMode === 'real_model' && (
        <div className="mt-4 bg-gray-900 rounded-xl p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-3 bg-gray-800 rounded-lg">
              <div className="text-sm text-gray-400">Model Version</div>
              <div className="text-lg font-bold">v5_xg_20251109_154848</div>
            </div>
            <div className="text-center p-3 bg-gray-800 rounded-lg">
              <div className="text-sm text-gray-400">AUC Score</div>
              <div className="text-lg font-bold">0.77</div>
            </div>
            <div className="text-center p-3 bg-gray-800 rounded-lg">
              <div className="text-sm text-gray-400">Features</div>
              <div className="text-lg font-bold">22</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}