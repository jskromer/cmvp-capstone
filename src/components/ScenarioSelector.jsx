import { SCENARIO_LIST } from '../scenarios/index';
import { useScenario } from '../scenarios/useScenario';

export default function ScenarioSelector() {
  const { scenarioId, setScenarioId } = useScenario();

  if (SCENARIO_LIST.length < 2) return null;

  return (
    <select
      value={scenarioId}
      onChange={(e) => setScenarioId(e.target.value)}
      style={{
        padding: '0.35rem 0.6rem',
        borderRadius: 6,
        border: '1px solid #d5ccc0',
        background: '#fffaf3',
        fontSize: '0.85rem',
        color: '#4a4540',
        cursor: 'pointer',
        fontWeight: 500,
      }}
    >
      {SCENARIO_LIST.map((s) => (
        <option key={s.id} value={s.id}>{s.name}</option>
      ))}
    </select>
  );
}
