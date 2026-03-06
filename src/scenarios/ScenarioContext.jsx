import { useState } from 'react';
import { ScenarioContext } from './context';
import { SCENARIOS, DEFAULT_SCENARIO } from './index';

export function ScenarioProvider({ children }) {
  const [scenarioId, setScenarioId] = useState(DEFAULT_SCENARIO);
  const scenario = SCENARIOS[scenarioId];

  return (
    <ScenarioContext.Provider value={{ scenario, scenarioId, setScenarioId }}>
      {children}
    </ScenarioContext.Provider>
  );
}
