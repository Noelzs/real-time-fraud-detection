import { useState } from 'react';

export function Controls({ stats, onStart, onStop, onClearTransactions, onResetStats }) {
  return (
    <div className="bg-gray-800 rounded-xl p-6 mb-8">
      <h3 className="text-xl font-bold mb-4">🎮 Demo Controls</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <button 
          onClick={onStart}
          className="bg-green-600 hover:bg-green-700 text-white py-3 px-6 rounded-lg font-semibold transition"
        >
          ▶ Start Current Mode
        </button>
        <button 
          onClick={onStop}
          className="bg-red-600 hover:bg-red-700 text-white py-3 px-6 rounded-lg font-semibold transition"
        >
          ⏸ Pause Current Mode
        </button>
        <button 
          onClick={onClearTransactions}
          className="bg-gray-700 hover:bg-gray-600 text-white py-3 px-6 rounded-lg font-semibold transition"
        >
          🗑️ Clear Display
        </button>
        <button
          onClick={onResetStats}
          className="bg-gray-700 hover:bg-gray-600 text-white py-3 px-6 rounded-lg font-semibold transition"
        >
          🔄 Reset Session
        </button>
      </div>
    </div>
  );
}