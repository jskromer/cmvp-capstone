
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
Fully built and functional cuts, pages, and tools.
| Page | Cut # | Cut Name | Interactive Tool | Data Wired |

### SECTION 2 — STUB / PLACEHOLDER
Content present but interactive tool not built.
| Cut # | Name | What Exists | What's Missing |

### SECTION 3 — NOT BUILT
Defined in capstone-flow.md but absent from prototype.html.
| Step | Name | Notes |

### SECTION 4 — HANDOUTS
For each cut: does a handout exist in handouts.html?
Flag gaps where prototype is COMPLETE but handout is missing, 
or handout exists but prototype is still a stub.
| Cut # | Handout Exists | Prototype Status | Gap? |

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

| Location | Issue | Severity |

### SECTION 7 — NAVIGATION INTEGRITY
Trace the full student path:
  Hub → Day 1 → Cut 1 → Cut 2 → Day 2 → Cut 3 → Cut 4 →
  Cut 5 → Cut 6 → Day 3 → Cut 7 → Cut 8 → Cut 9 → Hub

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
