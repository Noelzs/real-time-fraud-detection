import { useState } from 'react';
import { StatsCard } from './StatsCard';
import { TransactionList } from './TransactionList';
import { ModeSelector } from './ModeSelector';
import { Controls } from './Controls';
import { ConnectionStatus } from './ConnectionStatus';

export function Dashboard({ 
  stats, 
  transactions, 
  isConnected, 
  mode, 
  onModeChange,
  batchSize,
  onStartMode,
  onStopMode,
  onClearTransactions,
  onResetStats
}) {
  // Add display mode state
  const [displayMode, setDisplayMode] = useState('all'); // 'all' or 'interesting'

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 md:mb-8 gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold mb-2">
              <img src="/fraud-prevention.png" alt="Logo" className="h-12 w-18 mr-4 inline" /> Fraud Shield
            </h1>
            <p className="text-gray-400">
              Real-time monitoring at{' '}
              <span className="text-cyan-400 font-bold">
                {stats.processing_speed 
                  ? Math.round(stats.processing_speed).toLocaleString() 
                  : '10,000+'
                }
              </span>{' '}
              transactions/second
            </p>
          </div>
          <ConnectionStatus isConnected={isConnected} />
        </div>

        {/* Main Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
          <StatsCard 
            title="Total Processed" 
            value={stats.total_processed?.toLocaleString() || '0'} 
            icon="📊"
            color="border-white-500"
            subtext="Since session start"
          />
          <StatsCard 
            title="Fraud Detected" 
            value={stats.fraud_detected?.toLocaleString() || '0'} 
            icon="✅"
            color="border-green-500"
            valueColor="text-green-400"
            subtext="True positives"
          />
          <StatsCard 
            title="Detection Rate" 
            value={stats.detection_rate ? `${stats.detection_rate.toFixed(1)}%` : '0%'} 
            icon="🎯"
            color="border-white-500"
            subtext="Of actual fraud"
          />
          <StatsCard 
            title="Processing Speed" 
            value={stats.processing_speed 
              ? `${Math.round(stats.processing_speed).toLocaleString()}`
              : '0'} 
            icon="⚡"
            color="border-cyan-500"
            valueColor="text-cyan-400"
            subtext="Transactions/second"
          />
        </div>

        {/* Secondary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 md:mb-8">
          <div className="bg-gray-800 rounded-xl p-4">
            <div className="flex justify-between items-center">
              <div>
                <div className="text-sm text-gray-400">Missed Fraud</div>
                <div className="text-2xl font-bold text-red-400">
                  {stats.missed_fraud?.toLocaleString() || '0'}
                </div>
              </div>
              <span className="text-2xl">❌</span>
            </div>
          </div>
          <div className="bg-gray-800 rounded-xl p-4">
            <div className="flex justify-between items-center">
              <div>
                <div className="text-sm text-gray-400">False Alarms</div>
                <div className="text-2xl font-bold text-yellow-400">
                  {stats.false_alarms?.toLocaleString() || '0'}
                </div>
              </div>
              <span className="text-2xl">⚠️</span>
            </div>
          </div>
          <div className="bg-gray-800 rounded-xl p-4">
            <div className="flex justify-between items-center">
              <div>
                <div className="text-sm text-gray-400">Alert Rate</div>
                <div className="text-2xl font-bold text-blue-400">
                  {stats.alert_rate ? `${stats.alert_rate.toFixed(1)}%` : '0%'}
                </div>
              </div>
              <span className="text-2xl">🚨</span>
            </div>
          </div>
        </div>

        {/* Mode Selection - Updated with display mode */}
        <ModeSelector 
          currentMode={mode}
          onModeChange={onModeChange}
          displayMode={displayMode}
          onDisplayModeChange={setDisplayMode}
        />

        {/* Live Transactions - Updated with display mode */}
        <div className="bg-gray-800 rounded-xl overflow-hidden mb-6 md:mb-8">
          <div className="px-4 md:px-6 py-4 border-b border-gray-700 flex flex-col md:flex-row justify-between items-start md:items-center gap-2">
            <div className="flex items-center">
              <h2 className="text-xl font-bold flex items-center mr-4">
                <span className="mr-2">
                  {displayMode === 'all' ? '📈' : '🔍'}
                </span>
                {displayMode === 'all' ? 'Live Transaction Stream' : 'Interesting Transactions Only'}
              </h2>
              
              {/* Display mode badge */}
              <span className={`px-2 py-1 rounded text-xs font-semibold ${
                displayMode === 'all' 
                  ? 'bg-blue-900 text-blue-200' 
                  : 'bg-purple-900 text-purple-200'
              }`}>
                {displayMode === 'all' ? 'SHOWING ALL' : 'INTERESTING ONLY'}
              </span>
            </div>
            
            <div className="flex items-center gap-4 mt-2 md:mt-0">
              <span className="text-sm text-gray-400">
                Batch size: {batchSize}
              </span>
              <div className="text-sm">
                <span className="text-gray-400">Threshold: </span>
                <span className="font-bold text-gray-400">0.063</span>
              </div>
            </div>
          </div>
          
          {/* Pass displayMode to TransactionList */}
          <TransactionList 
            transactions={transactions} 
            displayMode={displayMode}
          />
        </div>

        {/* Controls */}
        <Controls 
          stats={stats}
          onStart={onStartMode}
          onStop={onStopMode}
          onClearTransactions={onClearTransactions}
          onResetStats={onResetStats}
        />

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm mt-8">
          <p>
            ⚡ Batch processing at 10,000+ transactions/second • 🎯 39.7% detection rate @ 8.8% false alarms
          </p>
          <p className="mt-2">
            Backend: FastAPI + WebSocket • Model: XGBoost v5 • Display: {displayMode === 'all' ? 'All transactions' : 'Interesting only'}
          </p>
        </div>
      </div>
    </div>
  );
}