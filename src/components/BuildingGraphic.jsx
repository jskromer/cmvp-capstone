/**
 * SVG building elevation of Greenfield Municipal Center.
 * Shows 4 wings with ECM locations marked.
 */
export default function BuildingGraphic() {
  return (
    <svg viewBox="0 0 800 340" style={{ width: "100%", maxWidth: 800, display: "block", margin: "0 auto 1rem" }}>
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#d4e6f1" />
          <stop offset="100%" stopColor="#eaf2f8" />
        </linearGradient>
        <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#a8c8e0" />
          <stop offset="100%" stopColor="#c5dbe8" />
        </linearGradient>
        <pattern id="roofHatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="8" stroke="#95a5a6" strokeWidth="1" />
        </pattern>
      </defs>

      {/* Sky */}
      <rect x="0" y="0" width="800" height="340" fill="url(#sky)" rx="8" />

      {/* Ground */}
      <rect x="0" y="280" width="800" height="60" fill="#c8d6c5" rx="0" />
      <rect x="0" y="280" width="800" height="3" fill="#a8b8a5" />

      {/* === Wing A — Office (left, 2 stories) === */}
      <g>
        {/* Main structure */}
        <rect x="40" y="120" width="280" height="160" fill="#f0e6d3" stroke="#b8a898" strokeWidth="1.5" />
        {/* Roof */}
        <rect x="35" y="112" width="290" height="12" fill="#8e7c6a" rx="2" />
        {/* ECM-3 insulation indicator */}
        <rect x="35" y="108" width="290" height="6" fill="#e67e22" opacity="0.6" rx="1" />
        {/* Floor divider */}
        <line x1="40" y1="200" x2="320" y2="200" stroke="#b8a898" strokeWidth="1" />

        {/* Windows — Floor 2 */}
        {[60, 100, 140, 180, 220, 260].map(x => (
          <rect key={`a2-${x}`} x={x} y="135" width="22" height="50" fill="url(#glass)" rx="2" stroke="#8faabe" strokeWidth="0.5" />
        ))}
        {/* Windows — Floor 1 */}
        {[60, 100, 140, 180, 220, 260].map(x => (
          <rect key={`a1-${x}`} x={x} y="215" width="22" height="50" fill="url(#glass)" rx="2" stroke="#8faabe" strokeWidth="0.5" />
        ))}

        {/* Door */}
        <rect x="155" y="235" width="34" height="45" fill="#6d5c4e" rx="2" />
        <circle cx="183" cy="258" r="2" fill="#b8860b" />

        {/* AHU-1 on roof */}
        <rect x="80" y="88" width="40" height="22" fill="#95a5a6" rx="3" stroke="#7f8c8d" strokeWidth="1" />
        <text x="100" y="102" textAnchor="middle" fontSize="7" fill="white" fontWeight="600">AHU-1</text>

        {/* ECM-1 LED icon */}
        <g transform="translate(290, 140)">
          <circle cx="0" cy="0" r="10" fill="#f1c40f" opacity="0.3" />
          <circle cx="0" cy="0" r="5" fill="#f1c40f" />
          <text x="14" y="4" fontSize="8" fill="#e67e22" fontWeight="700">LED</text>
        </g>

        {/* Label */}
        <text x="180" y="305" textAnchor="middle" fontSize="13" fill="#2c3e50" fontWeight="700">Wing A — Office</text>
        <text x="180" y="318" textAnchor="middle" fontSize="10" fill="#7f8c8d">35,000 sf · 2 floors</text>
      </g>

      {/* === Wing B — Library (right, 2 stories) === */}
      <g>
        <rect x="420" y="120" width="200" height="160" fill="#e8dff0" stroke="#b8a0c8" strokeWidth="1.5" />
        {/* Roof */}
        <rect x="415" y="112" width="210" height="12" fill="#7d6b8a" rx="2" />
        {/* ECM-3 insulation */}
        <rect x="415" y="108" width="210" height="6" fill="#e67e22" opacity="0.6" rx="1" />
        {/* Floor divider */}
        <line x1="420" y1="200" x2="620" y2="200" stroke="#b8a0c8" strokeWidth="1" />

        {/* Windows — Floor 2 (larger, library style) */}
        {[440, 490, 540, 585].map(x => (
          <rect key={`b2-${x}`} x={x} y="130" width="28" height="58" fill="url(#glass)" rx="2" stroke="#8faabe" strokeWidth="0.5" />
        ))}
        {/* Windows — Floor 1 */}
        {[440, 490, 540, 585].map(x => (
          <rect key={`b1-${x}`} x={x} y="210" width="28" height="55" fill="url(#glass)" rx="2" stroke="#8faabe" strokeWidth="0.5" />
        ))}

        {/* Door */}
        <rect x="505" y="238" width="30" height="42" fill="#5d4e6e" rx="2" />

        {/* AHU-2 on roof */}
        <rect x="480" y="88" width="40" height="22" fill="#95a5a6" rx="3" stroke="#7f8c8d" strokeWidth="1" />
        <text x="500" y="102" textAnchor="middle" fontSize="7" fill="white" fontWeight="600">AHU-2</text>

        {/* ECM-1 LED icon */}
        <g transform="translate(595, 140)">
          <circle cx="0" cy="0" r="10" fill="#f1c40f" opacity="0.3" />
          <circle cx="0" cy="0" r="5" fill="#f1c40f" />
          <text x="14" y="4" fontSize="8" fill="#e67e22" fontWeight="700">LED</text>
        </g>

        {/* Label */}
        <text x="520" y="305" textAnchor="middle" fontSize="13" fill="#2c3e50" fontWeight="700">Wing B — Library</text>
        <text x="520" y="318" textAnchor="middle" fontSize="10" fill="#7f8c8d">15,000 sf · 2 floors</text>
      </g>

      {/* === Wing C — Data Center (small, attached right) === */}
      <g>
        <rect x="620" y="190" width="80" height="90" fill="#f0d8d8" stroke="#c8a0a0" strokeWidth="1.5" />
        <rect x="617" y="184" width="86" height="10" fill="#8a6868" rx="2" />
        {/* ECM-3 insulation */}
        <rect x="617" y="180" width="86" height="6" fill="#e67e22" opacity="0.6" rx="1" />
        {/* CRAC unit */}
        <rect x="640" y="200" width="30" height="20" fill="#3498db" opacity="0.5" rx="3" stroke="#2980b9" strokeWidth="0.5" />
        <text x="655" y="213" textAnchor="middle" fontSize="6" fill="#1a365d" fontWeight="600">CRAC</text>
        {/* Server racks */}
        {[638, 658, 678].map(x => (
          <rect key={`srv-${x}`} x={x} y="228" width="12" height="40" fill="#2c3e50" rx="1" />
        ))}
        {/* Blinking lights */}
        {[641, 661, 681].map(x => (
          <g key={`led-${x}`}>
            <circle cx={x + 3} cy="235" r="1.5" fill="#2ecc71" />
            <circle cx={x + 3} cy="240" r="1.5" fill="#2ecc71" />
            <circle cx={x + 3} cy="245" r="1.5" fill="#f1c40f" />
          </g>
        ))}

        <text x="660" y="305" textAnchor="middle" fontSize="11" fill="#2c3e50" fontWeight="700">Wing C</text>
        <text x="660" y="318" textAnchor="middle" fontSize="9" fill="#7f8c8d">Data Center · 2k sf</text>
      </g>

      {/* === Common Areas (connector between A and B) === */}
      <g>
        <rect x="320" y="170" width="100" height="110" fill="#f5ecd0" stroke="#d4c8a0" strokeWidth="1.5" />
        <rect x="317" y="164" width="106" height="10" fill="#a09060" rx="2" />
        {/* ECM-3 insulation */}
        <rect x="317" y="160" width="106" height="6" fill="#e67e22" opacity="0.6" rx="1" />

        {/* Lobby entrance — glass doors */}
        <rect x="345" y="220" width="50" height="60" fill="url(#glass)" rx="3" stroke="#8faabe" strokeWidth="1" />
        <line x1="370" y1="220" x2="370" y2="280" stroke="#8faabe" strokeWidth="0.5" />

        {/* AHU-3 on roof */}
        <rect x="345" y="140" width="35" height="22" fill="#95a5a6" rx="3" stroke="#7f8c8d" strokeWidth="1" />
        <text x="362" y="154" textAnchor="middle" fontSize="7" fill="white" fontWeight="600">AHU-3</text>

        <text x="370" y="305" textAnchor="middle" fontSize="11" fill="#2c3e50" fontWeight="700">Common</text>
        <text x="370" y="318" textAnchor="middle" fontSize="9" fill="#7f8c8d">Lobby · 10k sf</text>
      </g>

      {/* === ECM Legend === */}
      <g transform="translate(40, 20)">
        <rect x="0" y="0" width="720" height="60" fill="rgba(255,255,255,0.85)" rx="6" stroke="#e0d8cc" strokeWidth="1" />
        {/* ECM-1 */}
        <circle cx="30" cy="20" r="6" fill="#f1c40f" />
        <text x="42" y="24" fontSize="10" fill="#2c3e50" fontWeight="600">ECM-1: LED Lighting</text>
        {/* ECM-2 */}
        <circle cx="200" cy="20" r="6" fill="#3498db" />
        <text x="212" y="24" fontSize="10" fill="#2c3e50" fontWeight="600">ECM-2: Chiller/DX</text>
        {/* ECM-3 */}
        <rect x="362" y="14" width="16" height="6" fill="#e67e22" opacity="0.7" rx="1" />
        <text x="384" y="24" fontSize="10" fill="#2c3e50" fontWeight="600">ECM-3: Roof Insulation</text>
        {/* ECM-4 */}
        <circle cx="560" cy="20" r="6" fill="#27ae60" />
        <text x="572" y="24" fontSize="10" fill="#2c3e50" fontWeight="600">ECM-4: VFDs on AHUs</text>
        {/* Subtitle */}
        <text x="360" y="48" textAnchor="middle" fontSize="10" fill="#7f8c8d" fontStyle="italic">
          Greenfield Municipal Center · 62,000 sf · Mid-Atlantic CZ 4A · ESPC 15-year term
        </text>
      </g>

      {/* VFD indicators on AHUs */}
      <circle cx="100" cy="88" r="4" fill="#27ae60" />
      <circle cx="500" cy="88" r="4" fill="#27ae60" />
      <circle cx="362" cy="140" r="4" fill="#27ae60" />
    </svg>
  );
}
