export function TransactionList({ transactions, displayMode = 'all' }) {
  const getColorClass = (type) => {
    const colors = {
      'detected_fraud': 'border-green-500 bg-green-900/20',
      'missed_fraud': 'border-red-500 bg-red-900/20',
      'false_alarm': 'border-yellow-500 bg-yellow-900/20',
      'legitimate': 'border-gray-600 bg-gray-900/20'
    };
    return colors[type] || 'border-gray-600 bg-gray-900/20';
  };

  const getIcon = (type) => {
    const icons = {
      'detected_fraud': '✅',
      'missed_fraud': '❌',
      'false_alarm': '⚠️',
      'legitimate': '⚪'
    };
    return icons[type] || '⚪';
  };

  // Filter transactions based on display mode
  const filteredTransactions = displayMode === 'interesting' 
    ? transactions.filter(tx => tx.type !== 'legitimate')
    : transactions;

  if (filteredTransactions.length === 0) {
    return (
      <div className="h-96 flex flex-col items-center justify-center text-gray-500">
        <div className="text-4xl mb-4">
          {displayMode === 'interesting' ? '🔍' : '⏳'}
        </div>
        <p className="text-lg">
          {displayMode === 'interesting' 
            ? 'No interesting transactions yet' 
            : 'Waiting for transactions...'}
        </p>
        <p className="text-sm mt-2">
          {displayMode === 'interesting' 
            ? 'Only fraud-related transactions (✅❌⚠️) will appear here' 
            : 'Transactions will appear here'}
        </p>
      </div>
    );
  }

  return (
    <div className="h-96 overflow-y-auto scrollbar-thin p-2">
      {filteredTransactions.map((tx, index) => (
        <div 
          key={index} 
          className={`transaction-enter mb-2 p-3 rounded-lg border-l-4 ${getColorClass(tx.type)}`}
        >
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <span className="text-2xl mr-3">{getIcon(tx.type)}</span>
              <div>
                <div className="font-bold">{tx.id}</div>
                <div className="text-sm text-gray-400">{tx.timestamp}</div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-xl font-bold">
                {tx.id && tx.id.includes('REAL') ? '$' : '₹'}
                {parseFloat(tx.amount || 0).toLocaleString()}
              </div>
              {/*<div className="text-xl font-bold">₹{parseFloat(tx.amount || 0).toLocaleString()}</div>*/}
              <div className={`text-sm ${tx.is_flagged ? 'text-red-400' : 'text-green-400'}`}>
                {tx.is_flagged ? '🚨 FLAGGED' : '✓ CLEAN'} • Risk: {((tx.fraud_prob || 0) * 100).toFixed(1)}%
              </div>
            </div>
          </div>
        </div>
      ))}
      
      {/* Show count of filtered vs total */}
      {displayMode === 'interesting' && transactions.length > 0 && (
        <div className="text-center text-sm text-gray-500 mt-4 pt-2 border-t border-gray-700">
          Showing {filteredTransactions.length} of {transactions.length} transactions
          <div className="text-xs">(Filtered: ⚪ legitimate transactions hidden)</div>
        </div>
      )}
    </div>
  );
}