export default function SummaryTable({ baseline, reporting, noNRA }) {
  if (!baseline || !reporting || !noNRA) return null;

  const sum = (arr, key) => arr.reduce((s, d) => s + d[key], 0);
  const bKwh = sum(baseline, 'total_kwh');
  const rKwh = sum(reporting, 'total_kwh');
  const nKwh = sum(noNRA, 'total_kwh');
  const bThm = sum(baseline, 'total_therms');
  const rThm = sum(reporting, 'total_therms');
  const nThm = sum(noNRA, 'total_therms');

  const sqft = 62000;
  const fmt = (v) => v.toLocaleString(undefined, { maximumFractionDigits: 0 });
  const eui = (kwh) => ((kwh * 3.412) / sqft).toFixed(1);
  const gEui = (thm) => ((thm * 100000) / (sqft * 1000)).toFixed(1); // kBtu/ft²

  return (
    <table className="summary-table">
      <thead>
        <tr>
          <th>Metric</th>
          <th>Baseline</th>
          <th>Reporting (w/NRA)</th>
          <th>Reporting (no NRA)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Annual Electric (kWh)</td>
          <td>{fmt(bKwh)}</td>
          <td>{fmt(rKwh)}</td>
          <td>{fmt(nKwh)}</td>
        </tr>
        <tr>
          <td>Annual Gas (therms)</td>
          <td>{fmt(bThm)}</td>
          <td>{fmt(rThm)}</td>
          <td>{fmt(nThm)}</td>
        </tr>
        <tr>
          <td>Electric EUI (kBtu/ft²)</td>
          <td>{eui(bKwh)}</td>
          <td>{eui(rKwh)}</td>
          <td>{eui(nKwh)}</td>
        </tr>
        <tr>
          <td>Gas EUI (kBtu/ft²)</td>
          <td>{gEui(bThm)}</td>
          <td>{gEui(rThm)}</td>
          <td>{gEui(nThm)}</td>
        </tr>
        <tr>
          <td>Electric Savings (no NRA)</td>
          <td colSpan={3}>
            {fmt(bKwh - nKwh)} kWh ({((bKwh - nKwh) / bKwh * 100).toFixed(1)}%)
          </td>
        </tr>
        <tr>
          <td>NRA Impact</td>
          <td colSpan={3}>
            +{fmt(rKwh - nKwh)} kWh (Aug-Dec step change)
          </td>
        </tr>
      </tbody>
    </table>
  );
}
