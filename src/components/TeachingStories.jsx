import { useState } from 'react';

const DATASET = [
  { month: 29, hdd: 450, gas: '210,692' },
  { month: 33, hdd: 440, gas: '208,664' },
  { month: 26, hdd: 220, gas: '157,886' },
  { month: 30, hdd: 150, gas: '120,793' },
  { month: 32, hdd: 90, gas: '134,568' },
  { month: 31, hdd: 20, gas: '107,272' },
  { month: 30, hdd: 14, gas: '95,411' },
  { month: 31, hdd: 29, gas: '126,423' },
  { month: 31, hdd: 125, gas: '149,333' },
  { month: 28, hdd: 275, gas: '166,202' },
  { month: 33, hdd: 300, gas: '183,060' },
  { month: 30, hdd: 723, gas: '224,958' },
];

const stories = [
  {
    id: 'story1',
    num: 1,
    title: '"We\'re Doing Option B" — Measuring Everything, Concluding Nothing',
    ecm: 'Boiler replacement',
    confusion: 'Continuous measurement ≠ continuous verification',
    content: (
      <>
        <p>
          A controls contractor wins a performance contract to replace three aging boilers at a 60,000 sf
          municipal building. The M&V plan says: "Option B — all parameters measured."
        </p>
        <p>
          The engineer installs gas meters on each boiler, temperature sensors on every supply and return loop,
          a weather station on the roof, and flow meters on the hydronic piping. Twenty-two measurement points.
          The data acquisition system costs $44,000. Monthly reports run fifty pages.
        </p>
        <p>
          Eight months in, the building owner asks: <em>"Are the new boilers saving gas?"</em>
        </p>
        <p>
          The engineer pulls up a spreadsheet. Thousands of hourly readings. But no model. No adjusted baseline.
          No counterfactual.
        </p>
        <p>
          Imagine he had the dataset above — 12 months of baseline HDD and gas consumption. He could see that
          in a month with 450 HDD, the old boilers consumed 210,692 therms. In the reporting period, a month
          with similar HDD shows lower consumption. But <em>how much lower than expected?</em> Without the
          regression — y&nbsp;=&nbsp;173.08x&nbsp;+&nbsp;111,372 — he has no way to answer. The model is what translates
          "450 HDD" into "the old system <em>would have used</em> 189,258 therms." The difference between
          189,258 and what the meter actually read is the avoided energy use.
        </p>
        <p>
          He has <strong>evidence</strong> — mountains of it. What he doesn't have is <strong>inference</strong>.
          He can tell you the lead boiler consumed 847 therms at 2 PM on February 12th. He cannot tell you what
          the old boiler <em>would have consumed</em> under those same conditions.
        </p>

        <div className="prompt-box" style={{ borderLeftColor: '#e67e22' }}>
          <strong style={{ color: '#e67e22' }}>What went wrong</strong>
          He read "all parameter measurement" as a hardware procurement list. He missed the two questions
          that retrofit isolation actually asks:
          <ul style={{ margin: '0.5rem 0 0', paddingLeft: '1.5rem' }}>
            <li><strong>Does it perform?</strong> (At commissioning — do the new boilers hit rated efficiency at design conditions?)</li>
            <li><strong>Does it keep operating?</strong> (Across seasons — does efficiency hold as load varies from 14 HDD in July to 723 HDD in January?)</li>
          </ul>
        </div>

        <p>
          The first question needed a commissioning test. The second needed a model — even a simple relationship
          between boiler output and heating load — that creates a counterfactual against which to compare
          reporting-period performance.
        </p>
        <p>
          The $44,000 in sensors could have been $8,000 in targeted metering with an analytical plan: meter gas
          input and heat output continuously, verify rated efficiency at commissioning, model the efficiency-vs-load
          relationship, compare reporting period to the modeled baseline.
        </p>

        <div className="prompt-box">
          <strong>Takeaway</strong>
          "Continuous performance verification" was reduced to "continuous measurement." Verification requires
          a counterfactual. Measurement alone is monitoring.
        </div>
      </>
    ),
  },
  {
    id: 'story2',
    num: 2,
    title: '"We Have to Comply with IPMVP"',
    ecm: 'Mixed — 200 school buildings',
    confusion: 'IPMVP is a protocol, not a building code',
    content: (
      <>
        <p>
          A state energy office issues an RFP for M&V services on 200 school buildings.
          The RFP says: "All M&V shall comply with IPMVP."
        </p>
        <p>
          Two firms submit plans that read like compliance checklists. Every section header is a clause reference.
          The approach selection table has four rows: Option A, Option B, Option C, Option D. One firm proposes
          Option C for every building — not because a whole-facility inverse model fits every case, but because
          it's the only approach their software supports and the protocol doesn't say they can't.
        </p>
        <p>A third firm submits something different. For each school cluster, they describe the ECMs and select
          the approach that fits the physics:</p>
        <ul>
          <li>
            <strong>Lighting-only retrofits</strong> → retrofit isolation with key parameter measurement.
            LED wattage doesn't drift. Stipulated hours. No regression needed — you don't need to model
            y&nbsp;=&nbsp;173.08x&nbsp;+&nbsp;111,372 to verify that a fixture draws 12 watts instead of 32.
          </li>
          <li>
            <strong>Boiler replacements</strong> → whole-facility inverse model. <em>This</em> is where the
            regression matters — you need the adjusted baseline to construct a counterfactual, because you can't
            isolate boiler savings from the gas meter without one.
          </li>
          <li>
            <strong>Ground-source heat pump conversion</strong> → calibrated simulation (forward model).
            The system interactions are too complex for a regression — a change in heating source changes the
            electric and gas signatures simultaneously.
          </li>
        </ul>
        <p>
          Their plan never mentions "Option A" or "Option C" in a heading. IPMVP appears in a methodology
          crosswalk appendix.
        </p>
        <p>
          The state energy office scores the third firm highest. The program manager explains:
          <em> "The first two firms showed me they could read a document. The third showed me they understood
          the buildings."</em>
        </p>

        <div className="prompt-box" style={{ borderLeftColor: '#e67e22' }}>
          <strong style={{ color: '#e67e22' }}>What went wrong</strong>
          IPMVP is a <em>protocol</em> — a framework for structuring M&V decisions. It is not a building code.
          It has no mandatory provisions. There is no IPMVP inspector. You cannot "violate" it.
          When practitioners treat it as a compliance document, they optimize for audit defensibility instead of
          analytical quality. They pick the Option that's easiest to justify on paper rather than the approach
          that matches the physics.
        </div>

        <div className="prompt-box">
          <strong>Takeaway</strong>
          The letters become a shield against professional judgment. The third firm demonstrated judgment;
          the first two demonstrated compliance.
        </div>
      </>
    ),
  },
  {
    id: 'story3',
    num: 3,
    title: '"Option C Is Regression, Option D Is Simulation"',
    ecm: 'University campus — plant, envelope, controls',
    confusion: 'Letters create a false binary between model types',
    content: (
      <>
        <p>
          An ESCO's M&V lead reviews approach selection for a university campus — central plant optimization,
          envelope upgrades, and a controls retrofit across 14 buildings.
        </p>
        <p>The junior engineer's table:</p>

        <table className="stats-table" style={{ maxWidth: 500, margin: '1rem 0' }}>
          <thead>
            <tr><th>ECM</th><th>Option</th><th>Justification</th></tr>
          </thead>
          <tbody>
            <tr><td>Central plant</td><td>D</td><td>"Complex system, need simulation"</td></tr>
            <tr><td>Envelope</td><td>C</td><td>"Whole building, use regression"</td></tr>
            <tr><td>Controls</td><td>C</td><td>"Whole building, use regression"</td></tr>
          </tbody>
        </table>

        <p>The senior engineer asks: <em>"Why regression for the controls?"</em></p>
        <p>"Whole facility means Option C. Option C means regression."</p>
        <p>
          "Pull up the baseline gas data." The scatter plot appears — HDD vs. gas consumption,
          y&nbsp;=&nbsp;173.08x&nbsp;+&nbsp;111,372, R²&nbsp;=&nbsp;0.9193. "This regression captures the relationship
          between weather and gas use. It works because heating load drives gas consumption in a predictable way.
          Now — the controls retrofit changes <em>when</em> the system runs, not <em>how much energy it uses
          per degree-day</em>. The slope doesn't change. The change points don't move. The schedules shift.
          What does the regression see?"
        </p>
        <p>"...Nothing?"</p>
        <p>
          "Exactly. The savings are real but invisible to an inverse model. The energy signature looks the same
          pre and post. You need a forward model — a simulation — that can represent the schedule changes and
          calculate the difference."
        </p>

        <div style={{
          overflowX: 'auto',
          margin: '1.5rem 0',
          background: 'white',
          border: '1px solid var(--border)',
          borderRadius: 8,
          padding: '1rem 1.25rem',
          boxShadow: 'var(--shadow)',
        }}>
          <p style={{ margin: '0 0 0.5rem', fontWeight: 600, color: 'var(--dark)', fontSize: '0.9rem' }}>
            The Model Spectrum
          </p>
          <table className="stats-table" style={{ margin: 0, fontSize: '0.85rem' }}>
            <thead>
              <tr>
                <th style={{ background: 'var(--blue)' }}>Data-driven →</th>
                <th style={{ background: '#2980b9' }}></th>
                <th style={{ background: '#1a6da0' }}></th>
                <th style={{ background: 'var(--blue-dark)' }}>← Physics-driven</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Simple linear regression</td>
                <td>Change-point models</td>
                <td>Hybrid / gray-box</td>
                <td>Calibrated simulation</td>
              </tr>
              <tr>
                <td>Minimal physics needed</td>
                <td>Physical intuition (slopes, break points)</td>
                <td>Physics structure + data fitting</td>
                <td>Full physical description</td>
              </tr>
              <tr>
                <td>Fast, cheap, transparent</td>
                <td>Moderate effort</td>
                <td>Specialized expertise</td>
                <td>Expensive, time-consuming</td>
              </tr>
              <tr>
                <td><em>Fails when savings are invisible to the meter</em></td>
                <td>Works when energy signature changes shape</td>
                <td>Bridges the gap</td>
                <td>Works for any mechanism</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="prompt-box">
          <strong>Takeaway</strong>
          The campus project used a forward model for both the central plant and controls (physics drove
          the counterfactual) and a change-point regression for envelope (the heating slope shift was detectable).
          No one needed to say "D, D, C." They needed to say: "Here's the inference method that produces a
          credible counterfactual for each ECM, and here's why."
        </div>
      </>
    ),
  },
  {
    id: 'story4',
    num: 4,
    title: '"We Measured the Savings"',
    ecm: 'Utility program — boiler retrofit',
    confusion: 'Savings are inference, not measurement',
    content: (
      <>
        <p>
          A utility program administrator presents results to the public utilities commission.
          The slide says: <strong>"Measured savings: 12.4 GWh."</strong>
        </p>
        <p>
          A commissioner asks: <em>"How do you measure savings?"</em>
        </p>
        <p>
          Consider the gas dataset above. Baseline year: 12 months of HDD and gas consumption. Reporting year:
          12 more months, after the boiler retrofit. The administrator subtracted reporting-year totals from
          baseline-year totals and reported the difference as "measured savings."
        </p>
        <p>
          But January in the baseline year had 723 HDD. January in the reporting year had 580 HDD. Of course
          gas went down — it was warmer. That's not savings, that's weather.
        </p>

        <p style={{ fontWeight: 600, color: 'var(--dark)', marginTop: '1rem' }}>
          What the M&V professional actually did (or should have done):
        </p>
        <ol style={{ paddingLeft: '1.5rem', lineHeight: 1.8 }}>
          <li><strong>Measured</strong> baseline gas consumption — the 12 rows in the table <span style={{ color: 'var(--green)', fontWeight: 600 }}>(evidence)</span></li>
          <li><strong>Measured</strong> reporting-period gas consumption <span style={{ color: 'var(--green)', fontWeight: 600 }}>(evidence)</span></li>
          <li><strong>Built the regression</strong> — y&nbsp;=&nbsp;173.08x&nbsp;+&nbsp;111,372 — from baseline data <span style={{ color: 'var(--blue)', fontWeight: 600 }}>(inference)</span></li>
          <li><strong>Fed reporting-period HDD into the model</strong> to calculate the counterfactual <span style={{ color: 'var(--blue)', fontWeight: 600 }}>(inference)</span></li>
          <li><strong>Subtracted</strong> actual from adjusted baseline to estimate avoided energy use <span style={{ color: 'var(--blue)', fontWeight: 600 }}>(inference)</span></li>
        </ol>

        <p>
          Steps 1 and 2 are measurement. Steps 3 through 5 are inference. The reported number is not a measured
          quantity — it's the output of a model. It depends on which variables were included, how the model was
          specified, and what professional judgments were made.
        </p>
        <p>
          For a month with 580 HDD in the reporting period, the model predicts:
          173.08&nbsp;&times;&nbsp;580&nbsp;+&nbsp;111,372&nbsp;=&nbsp;<strong>211,758 therms</strong>.
          If the new boilers actually consumed 185,000 therms, the avoided energy use is 26,758 therms. That
          number came from the model, not from a meter.
        </p>

        <div className="prompt-box" style={{ borderLeftColor: '#e67e22' }}>
          <strong style={{ color: '#e67e22' }}>Why it matters</strong>
          When savings are called "measured," they inherit the authority of physical measurement. But savings have
          model uncertainty, parameter uncertainty, and specification uncertainty stacked on top of metering accuracy.
          Calling them "measured" closes the door on the question that matters most: <em>how confident are we in this
          number, and what would change it?</em>
        </div>

        <div className="prompt-box">
          <strong>Takeaway</strong>
          The precise term is <strong>avoided energy use</strong>. "Savings" is fine as shorthand. "Measured savings" is not.
        </div>
      </>
    ),
  },
];

export default function TeachingStories() {
  const [activeStory, setActiveStory] = useState(null);

  return (
    <div>
      {/* Evidence vs Inference framework */}
      <div style={{
        background: 'white',
        border: '1px solid var(--border)',
        borderRadius: 8,
        padding: '1.25rem 1.5rem',
        marginBottom: '1.5rem',
        boxShadow: 'var(--shadow)',
      }}>
        <h3 style={{ margin: '0 0 0.75rem', color: 'var(--dark)' }}>
          The Foundational Framework: Evidence vs. Inference
        </h3>
        <table className="stats-table" style={{ margin: '0.5rem 0', maxWidth: 700 }}>
          <thead>
            <tr><th>Category</th><th>What It Is</th><th>Examples</th></tr>
          </thead>
          <tbody>
            <tr>
              <td><strong style={{ color: 'var(--green)' }}>Evidence</strong></td>
              <td>What you directly observe or measure</td>
              <td>Baseline energy bills, reporting-period meter data, OAT, fixture wattage, fan kW</td>
            </tr>
            <tr>
              <td><strong style={{ color: 'var(--blue)' }}>Inference</strong></td>
              <td>What you conclude from evidence</td>
              <td>Adjusted baseline model, the counterfactual, avoided energy use ("savings")</td>
            </tr>
          </tbody>
        </table>
        <p style={{ margin: '0.75rem 0 0.5rem', fontWeight: 600, color: 'var(--dark)', fontSize: '0.95rem' }}>
          Savings are never evidence. Savings are always inference.
        </p>

        {/* Factual/counterfactual matrix */}
        <table className="stats-table" style={{ margin: '0.75rem 0 0', maxWidth: 600 }}>
          <thead>
            <tr><th></th><th>Pre-Implementation</th><th>Post-Implementation</th></tr>
          </thead>
          <tbody>
            <tr>
              <td><strong style={{ color: 'var(--green)' }}>Evidence</strong> (factual)</td>
              <td>Baseline metered energy</td>
              <td>Reporting-period metered energy</td>
            </tr>
            <tr>
              <td><strong style={{ color: 'var(--blue)' }}>Inference</strong> (counterfactual)</td>
              <td>—</td>
              <td>Adjusted baseline model → avoided energy use</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Shared dataset */}
      <div style={{
        background: 'white',
        border: '1px solid var(--border)',
        borderRadius: 8,
        padding: '1.25rem 1.5rem',
        marginBottom: '1.5rem',
        boxShadow: 'var(--shadow)',
      }}>
        <h3 style={{ margin: '0 0 0.5rem', color: 'var(--dark)' }}>
          The Shared Dataset
        </h3>
        <p style={{ margin: '0 0 0.75rem', fontSize: '0.9rem', color: 'var(--gray-500)' }}>
          All four stories reference this baseline dataset and its regression model.
        </p>
        <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap', alignItems: 'flex-start' }}>
          <table className="stats-table" style={{ margin: 0, maxWidth: 320, flex: '0 0 auto' }}>
            <thead>
              <tr><th>Days</th><th>HDD</th><th>Gas (therms)</th></tr>
            </thead>
            <tbody>
              {DATASET.map((row, i) => (
                <tr key={i}>
                  <td>{row.month}</td>
                  <td>{row.hdd}</td>
                  <td style={{ textAlign: 'right' }}>{row.gas}</td>
                </tr>
              ))}
              <tr style={{ fontWeight: 600, background: 'var(--cream-dark)' }}>
                <td colSpan={2}>Average</td>
                <td style={{ textAlign: 'right' }}>158,769</td>
              </tr>
            </tbody>
          </table>
          <div style={{ flex: '1 1 260px', minWidth: 260 }}>
            <div style={{
              background: 'var(--cream)',
              border: '1px solid var(--border)',
              borderRadius: 6,
              padding: '1rem 1.25rem',
              fontFamily: "'SF Mono', Consolas, monospace",
              fontSize: '0.95rem',
            }}>
              <div style={{ fontWeight: 600, color: 'var(--dark)', marginBottom: '0.5rem' }}>
                Regression model:
              </div>
              <div style={{ fontSize: '1.1rem', color: 'var(--blue-dark)' }}>
                y = 173.08x + 111,372
              </div>
              <div style={{ marginTop: '0.25rem', color: 'var(--gray-500)' }}>
                R² = 0.9193
              </div>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--gray-500)', marginTop: '0.75rem', lineHeight: 1.5 }}>
              This regression <em>is</em> the inference engine. It is the adjusted baseline model.
              Without it, the 12 rows of HDD and gas consumption are just evidence sitting in a table.
            </p>
          </div>
        </div>
      </div>

      {/* Instructor note */}
      <div className="instructor-toggle" style={{ marginBottom: '1.5rem' }}>
        <strong>Instructor note:</strong> The regression-based adjusted baseline applies mainly to{' '}
        <em>counterfactual methods</em> — whole-facility approaches where you must construct what{' '}
        <em>would have happened</em>. Performance verification (retrofit isolation) doesn't do this;
        it verifies the ECM itself.
      </div>

      {/* Story cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {stories.map((story) => (
          <div
            key={story.id}
            style={{
              background: 'white',
              border: `1px solid ${activeStory === story.id ? 'var(--blue)' : 'var(--border)'}`,
              borderRadius: 8,
              boxShadow: activeStory === story.id ? '0 2px 8px rgba(41,128,185,0.15)' : 'var(--shadow)',
              overflow: 'hidden',
              transition: 'border-color 0.2s, box-shadow 0.2s',
            }}
          >
            {/* Header — always visible */}
            <button
              onClick={() => setActiveStory(activeStory === story.id ? null : story.id)}
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                gap: '1rem',
                padding: '1rem 1.25rem',
                background: activeStory === story.id ? 'var(--blue-light)' : 'transparent',
                border: 'none',
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '1rem',
                color: 'var(--dark)',
                transition: 'background 0.15s',
              }}
            >
              <span style={{
                flex: '0 0 auto',
                width: 32, height: 32,
                borderRadius: '50%',
                background: activeStory === story.id ? 'var(--blue)' : 'var(--gray-200)',
                color: activeStory === story.id ? 'white' : 'var(--gray-700)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontWeight: 700, fontSize: '0.9rem',
                transition: 'background 0.15s, color 0.15s',
              }}>
                {story.num}
              </span>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600 }}>{story.title}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--gray-500)', marginTop: 2 }}>
                  {story.ecm} — <em>{story.confusion}</em>
                </div>
              </div>
              <span style={{
                fontSize: '1.2rem',
                color: 'var(--gray-500)',
                transform: activeStory === story.id ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.2s',
              }}>
                ▾
              </span>
            </button>

            {/* Body — collapsible */}
            {activeStory === story.id && (
              <div style={{ padding: '0 1.5rem 1.5rem', lineHeight: 1.7, fontSize: '0.95rem' }}>
                {story.content}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Discussion prompt */}
      <div className="prompt-box" style={{ marginTop: '1.5rem' }}>
        <strong>Discuss</strong>
        These stories all share a common thread: the confusion between evidence and inference.
        In each case, how does the letter-based terminology (Options A/B/C/D) contribute to the misunderstanding?
        How would the descriptive terms — retrofit isolation, key parameter measurement, continuous performance
        verification, whole facility, inverse model, forward model — have changed the conversation?
      </div>
    </div>
  );
}
