export function StatsCard({ title, value, icon, color, subtext, valueColor = "" }) {
  return (
    <div className={`bg-gray-800 rounded-xl p-6 border-l-4 ${color}`}>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-gray-400 text-sm font-semibold uppercase">{title}</h3>
        <span className="text-2xl">{icon}</span>
      </div>
      <div className={`text-3xl font-bold ${valueColor}`}>{value}</div>
      <div className="text-sm text-gray-400 mt-2">{subtext}</div>
    </div>
  );
}