import { useState, useEffect, useCallback } from 'react';

export function useWebSocket(mode, hookKey = 0) {  // ✅ Add hookKey parameter
  const [stats, setStats] = useState({
    total_processed: 0,
    fraud_detected: 0,
    missed_fraud: 0,
    false_alarms: 0,
    detection_rate: 0,
    processing_speed: 0,
    alert_rate: 0,
    threshold: 0.063
  });
  const [transactions, setTransactions] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [batchSize, setBatchSize] = useState(10);

  useEffect(() => {
    console.log(`🎯 Hook #${hookKey} - Creating NEW WebSocket for ${mode} mode`);
    
    const wsUrl = mode === 'simulation' 
      ? 'ws://localhost:8000/ws/simulation'
      : 'ws://localhost:8000/ws/real-model';
    
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log(`✅ Hook #${hookKey} - Connected to ${mode} mode`);
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
    
        if (data.type === 'connected') {
          console.log('Server connected:', data.message);
      // ✅ OPTION 2: Reset stats to zero when first connecting
      // This ensures fresh start even if backend hasn't fully reset
          setStats({
            total_processed: 0,
            fraud_detected: 0,
            missed_fraud: 0,
            false_alarms: 0,
            detection_rate: 0,
            processing_speed: 0,
            alert_rate: 0,
            threshold: 0.063
          });
          setTransactions([]);
        } 
        else if (data.type === 'batch' || data.type === 'transactions') {
          if (data.batch_size) {
            setBatchSize(data.batch_size);
          }
      
          if (data.transactions && data.transactions.length > 0) {
            setTransactions(prev => [...data.transactions, ...prev].slice(0, 50));
          }
      
          if (data.stats) {
        // Only update stats if they're not all zero (avoid overwriting our reset)
        // Check if backend sent non-zero stats (means it didn't reset properly)
            const isBackendReset = data.stats.total_processed === 0 && 
                                    data.stats.fraud_detected === 0;
        
            if (!isBackendReset) {
          // Backend still has old stats, use them
              setStats(data.stats);
            }
        // If backend stats are zero, keep our zero stats
          }
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      console.log(`WebSocket #${hookKey} closed`);
      setIsConnected(false);
    };

    // Cleanup function
    return () => {
      console.log(`🧹 DESTROYING WebSocket #${hookKey} for ${mode} mode`);
      if (ws.readyState === WebSocket.OPEN) {
        ws.close(1000, 'Hook unmounting');
      }
    };
  }, [mode, hookKey]); // ✅ Add hookKey to dependencies

  const startMode = useCallback(() => {
    fetch(`http://localhost:8000/api/mode/${mode}/start`, {
      method: 'POST'
    })
    .then(response => {
      if (response.ok) {
        console.log(`Mode ${mode} started`);
      }
    })
    .catch(error => {
      console.log('Could not start via API:', error);
    });
  }, [mode]);

  const stopMode = useCallback(() => {
    fetch(`http://localhost:8000/api/mode/${mode}/stop`, {
      method: 'POST'
    })
    .then(response => {
      if (response.ok) {
        console.log(`Mode ${mode} stopped`);
      }
    })
    .catch(error => {
      console.log('Could not stop via API:', error);
    });
  }, [mode]);

  const clearTransactions = useCallback(() => {
    setTransactions([]);
  }, []);

  // Simple reset - parent will handle remounting
  const resetStats = useCallback(() => {
    console.log('Resetting stats...');
    stopMode();
    // Don't reset stats here - parent will remount us
  }, [stopMode]);

  return { 
    stats, 
    transactions, 
    isConnected, 
    batchSize,
    startMode,
    stopMode,
    clearTransactions,
    resetStats
  };
}