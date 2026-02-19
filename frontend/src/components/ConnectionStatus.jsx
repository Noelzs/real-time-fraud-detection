export function ConnectionStatus({ isConnected }) {
  const status = isConnected ? ' Connected' : ' Disconnected';
  const colorClass = isConnected ? 'bg-green-900' : 'bg-red-900';
  const dotColor = isConnected ? 'bg-green-500' : 'bg-red-500';

  return (
    <div className={`px-4 py-2 rounded-lg ${colorClass}`}>
      <span className={`inline-block w-3 h-3 rounded-full mr-2 ${dotColor}`}></span>
      {status}
    </div>
  );
}