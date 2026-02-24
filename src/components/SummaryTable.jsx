export default function SummaryTable({ baseline, reporting, noNRA, showAnswerKey }) {
  if (!baseline || !reporting) return null;

  const sum = (arr, key) => arr.reduce((s, d) => s + d[key], 0);
  const fmt = (v) => v.toLocaleString(undefined, { maximumFractionDigits: 0 });
  const sqft = 62000;
  const eui = (kwh) => ((kwh * 3.412) / sqft).toFixed(1);
  const gEui = (thm) => ((thm * 100000) / (sqft * 1000)).toFixed(1);

  const bKwh = sum(baseline, 'total_kwh');
  const rKwh = sum(reporting, 'total_kwh');
  const bThm = sum(baseline, 'total_therms');
  const rThm = sum(reporting, 'total_therms');

  return (
    <table className="summary-table">
      <thead>
        <tr>
          <th>Metric</th>
          <th>Baseline Year</th>
          <th>Reporting Year</th>
          {showAnswerKey && noNRA && <th>Reporting (no NRA)</th>}
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Annual Electric (kWh)</td>
          <td>{fmt(bKwh)}</td>
          <td>{fmt(rKwh)}</td>
          {showAnswerKey && noNRA && <td>{fmt(sum(noNRA, 'total_kwh'))}</td>}
        </tr>
        <tr>
          <td>Annual Gas (therms)</td>
          <td>{fmt(bThm)}</td>
          <td>{fmt(rThm)}</td>
          {showAnswerKey && noNRA && <td>{fmt(sum(noNRA, 'total_therms'))}</td>}
        </tr>
        <tr>
          <td>Electric EUI (kBtu/ft²)</td>
          <td>{eui(bKwh)}</td>
          <td>{eui(rKwh)}</td>
          {showAnswerKey && noNRA && <td>{eui(sum(noNRA, 'total_kwh'))}</td>}
        </tr>
        <tr>
          <td>Gas EUI (kBtu/ft²)</td>
          <td>{gEui(bThm)}</td>
          <td>{gEui(rThm)}</td>
          {showAnswerKey && noNRA && <td>{gEui(sum(noNRA, 'total_therms'))}</td>}
        </tr>
        <tr>
          <td>Apparent Electric Change</td>
          <td colSpan={showAnswerKey && noNRA ? 3 : 2}>
            {fmt(bKwh - rKwh)} kWh ({((bKwh - rKwh) / bKwh * 100).toFixed(1)}%)
            {bKwh - rKwh < 0 ? ' ⚠ consumption increased' : ''}
          </td>
        </tr>
        <tr>
          <td>Gas Change</td>
          <td colSpan={showAnswerKey && noNRA ? 3 : 2}>
            {rThm > bThm ? '+' : ''}{fmt(rThm - bThm)} therms ({((rThm - bThm) / bThm * 100).toFixed(1)}%)
          </td>
        </tr>
      </tbody>
    </table>
  );
}
