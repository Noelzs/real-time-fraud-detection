import { useState, useCallback } from 'react';
import { Dashboard } from './components/Dashboard';
import { useWebSocket } from './hooks/useWebSocket';

function App() {
  const [mode, setMode] = useState('simulation');
  const [hookKey, setHookKey] = useState(0); // Key to force remount
  
  // Every time hookKey changes, useWebSocket completely remounts
  const { 
    stats, 
    transactions, 
    isConnected, 
    batchSize,
    startMode,
    stopMode,
    clearTransactions,
    resetStats: originalResetStats // This won't be used anymore
  } = useWebSocket(mode, hookKey); // ✅ Pass hookKey here

  // Custom reset handler that remounts the hook
  // Custom reset handler that remounts the hook
const handleResetStats = useCallback(async () => {
  console.log('🔄 NUCLEAR RESET - Remounting WebSocket hook');
  
  // 1. Stop the current mode
  stopMode();
  
  // 2. Call backend reset API FIRST
  try {
    console.log(`Calling backend reset for ${mode} mode...`);
    const response = await fetch(`http://localhost:8000/api/reset/${mode}`, {
      method: 'POST'
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('Backend stats reset:', data.message);
    } else {
      console.log('Backend reset failed, continuing with frontend reset');
    }
  } catch (error) {
    console.log('Could not reset backend (might be offline):', error);
  }
  
  // 3. Increment key to force COMPLETE hook remount
  setHookKey(prev => {
    const newKey = prev + 1;
    console.log(`Hook key changed from ${prev} to ${newKey}`);
    return newKey;
  });
}, [stopMode, mode]); // Add mode to dependencies

  // Custom mode change handler
  const handleModeChange = useCallback((newMode) => {
    console.log(`Changing mode from ${mode} to ${newMode}`);
    setMode(newMode);
    // Also reset hook key when changing modes for clean slate
    setHookKey(prev => prev + 1);
  }, [mode]);

  return (
    <Dashboard 
      stats={stats}
      transactions={transactions}
      isConnected={isConnected}
      mode={mode}
      onModeChange={handleModeChange}
      batchSize={batchSize}
      onStartMode={startMode}
      onStopMode={stopMode}
      onClearTransactions={clearTransactions}
      onResetStats={handleResetStats}
    />
  );
}

export default App;