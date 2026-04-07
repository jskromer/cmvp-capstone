
---
# CMVP Capstone — Audit Prompt

**Purpose:** Run this prompt against `docs/prototype.html`, 
`docs/handouts.html`, and `docs/capstone-flow.md` to produce a 
timestamped build status report. Save output to 
`docs/audits/audit-YYYY-MM-DD_HHMM.md`.

---

## Instructions

Read the three source files. Get the current date and time (PDT).
Begin the report with:

  CMVP Capstone — Build Status Audit
  Run: YYYY-MM-DD HH:MM PDT

Then produce the following 7 sections:

---

### SECTION 1 — COMPLETE
Fully built and functional checkpoints, pages, and tools.
| Page | Checkpoint # | Checkpoint Name | Interactive Tool | Data Wired |

### SECTION 2 — STUB / PLACEHOLDER
Content present but interactive tool not built.
| Checkpoint # | Name | What Exists | What's Missing |

### SECTION 3 — NOT BUILT
Defined in capstone-flow.md but absent from prototype.html.
| Step | Name | Notes |

### SECTION 4 — HANDOUTS
For each checkpoint: does a handout exist in handouts.html?
Flag gaps where prototype is COMPLETE but handout is missing,
or handout exists but prototype is still a stub.
| Checkpoint # | Handout Exists | Prototype Status | Gap? |

### SECTION 5 — KNOWN BUGS
| # | Severity | Location | Issue |

### SECTION 6 — PEDAGOGY INTEGRITY
Review all built content for:

- LANGUAGE: Flag any use of "measure the savings" or 
  "measured savings." Savings are INFERRED, ESTIMATED, 
  CALCULATED, or DETERMINED — never measured.

- COUNTERFACTUAL FRAMING: Is the baseline model applied to 
  reporting-period OAT conditions — not copied from baseline 
  period observations? Flag any table using raw observed 
  baseline values as the savings reference.

- IPMVP LANGUAGE: Flag any use of "Option A/B/C/D." 
  These are legacy. Use CfD framework: Boundary, Model Form, 
  Duration.

- CfD FRAMEWORK: Are Boundary, Model Form, and Duration
  represented correctly throughout?

- BOUNDARY DOCUMENT COMPLETENESS: For any checkpoint or tool that involves
  boundary setting or stipulation, verify that a "Who Controls?"
  or equivalent responsibility assignment is present. The boundary
  document must be able to answer: "Who turns on/off the lights?"
  Flag any boundary tool that assigns parameters without assigning
  responsibility.

| Location | Issue | Severity |

### SECTION 7 — NAVIGATION INTEGRITY
Trace the full student path:
  Hub → Day 1 → Checkpoint 1 → Checkpoint 2 → Day 2 → Checkpoint 3 → Checkpoint 4 →
  Checkpoint 5 → Checkpoint 6 → Day 3 → Checkpoint 7 → Checkpoint 8 → Checkpoint 9 → Hub

For each transition verify:
- "→ Next" or "Proceed" button exists with working onclick
- Target section renders correctly
- No dead ends without explanation

| Transition | Button Exists? | onclick Wired? | Status |

---

## Standing Rules
Include at the bottom of every audit output:

> STANDING RULES:
> - Never write "measure the savings." Savings are inferred, 
>   determined, estimated, or calculated. Energy is measured.
> - Never reference IPMVP Options A/B/C/D. Use CfD framework: 
>   Boundary, Model Form, Duration.
> - The IDF is the epistemological basis for all M&V decisions.

---

## Saving
1. Get current date and time (PDT), format: YYYY-MM-DD_HHMM
2. Save to docs/audits/audit-YYYY-MM-DD_HHMM.md
3. Create docs/audits/ directory if it does not exist
4. Never overwrite an existing audit file
---
