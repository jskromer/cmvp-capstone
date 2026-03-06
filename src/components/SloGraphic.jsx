// SVG 5-story office building elevation for SLO Large Office scenario
export default function SloGraphic() {
  return (
    <svg viewBox="0 0 800 360" style={{ width: '100%', maxWidth: 800, display: 'block', margin: '0 auto 1.5rem' }}>
      {/* Legend */}
      <g transform="translate(30, 10)">
        <rect x="0" y="0" width="12" height="12" fill="#fef3cd" stroke="#856404" rx="2" />
        <text x="18" y="11" fontSize="10" fill="#4a4540">ECM-1: LED Lighting</text>
        <rect x="160" y="0" width="12" height="12" fill="#d1ecf1" stroke="#0c5460" rx="2" />
        <text x="178" y="11" fontSize="10" fill="#4a4540">ECM-2: Chiller Replacement</text>
        <rect x="360" y="0" width="12" height="12" fill="#d4edda" stroke="#155724" rx="2" />
        <text x="378" y="11" fontSize="10" fill="#4a4540">ECM-3: VAV Optimization</text>
      </g>

      {/* Ground */}
      <rect x="100" y="320" width="600" height="8" fill="#d5ccc0" rx="2" />

      {/* Building body — 5 floors */}
      {[0, 1, 2, 3, 4].map(floor => {
        const y = 270 - floor * 56;
        const floorLabel = `Floor ${floor + 1}`;
        return (
          <g key={floor}>
            {/* Floor slab */}
            <rect x="150" y={y} width="500" height="56" fill="#f9f6f0" stroke="#d5ccc0" strokeWidth="1.5" />
            {/* Floor label */}
            <text x="165" y={y + 33} fontSize="11" fill="#8c8478" fontWeight="500">{floorLabel}</text>
            {/* Windows */}
            {[240, 300, 360, 420, 480, 540].map(wx => (
              <rect key={wx} x={wx} y={y + 10} width="30" height="36" fill="#d1ecf1" stroke="#0c5460" strokeWidth="0.8" rx="2" />
            ))}
            {/* LED markers (ECM-1) */}
            <circle cx={600} cy={y + 28} r="6" fill="#fef3cd" stroke="#856404" strokeWidth="1" />
            <text x={600} y={y + 31} textAnchor="middle" fontSize="7" fill="#856404" fontWeight="700">L</text>
          </g>
        );
      })}

      {/* Roof */}
      <rect x="145" y="38" width="510" height="8" fill="#8c8478" rx="2" />

      {/* Mechanical penthouse */}
      <rect x="300" y="10" width="200" height="28" fill="#e0d8c8" stroke="#8c8478" rx="3" />
      <text x="400" y="28" textAnchor="middle" fontSize="10" fill="#4a4540" fontWeight="600">MECHANICAL</text>

      {/* Chiller (ECM-2) */}
      <rect x="510" y="12" width="40" height="24" fill="#d1ecf1" stroke="#0c5460" rx="3" />
      <text x="530" y="28" textAnchor="middle" fontSize="8" fill="#0c5460" fontWeight="700">CHL</text>

      {/* VAV boxes (ECM-3) — shown on right side */}
      {[1, 2, 3, 4].map(floor => {
        const y = 270 - floor * 56 + 20;
        return (
          <g key={`vav-${floor}`}>
            <rect x="620" y={y} width="24" height="16" fill="#d4edda" stroke="#155724" rx="2" />
            <text x="632" y={y + 12} textAnchor="middle" fontSize="7" fill="#155724" fontWeight="700">VAV</text>
          </g>
        );
      })}

      {/* Entrance */}
      <rect x="350" y="290" width="60" height="30" fill="#f5f0e8" stroke="#8c8478" rx="3" />
      <text x="380" y="310" textAnchor="middle" fontSize="9" fill="#4a4540">Entry</text>

      {/* Building name */}
      <text x="400" y="350" textAnchor="middle" fontSize="13" fill="#1a365d" fontWeight="600">
        SLO Large Office — 90,000 sf · 5 Floors · VAV System
      </text>
    </svg>
  );
}
