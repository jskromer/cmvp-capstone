# CMVP_v2.0_Section-6.0_Retrofit-Isolation_G_v1.1.pptx


## Slide 1
MODULE 6Retrofit Isolation

## Slide 2
Learning Objectives
Understand retrofit isolation approaches and list their strengths and weaknesses
Understand the challenges of interactive effects and tools used to quantify them
Identify significant parameters as well as parameters that can be estimated
Discuss the range of field engineering skills required for retrofit isolation approaches as well as safety requirements

## Slide 3
What Is Retrofit Isolation?
To investigate a change—the impact of an energy savings project, for example—it is often feasible/beneficial to study the change as close to its source as possible.
The smaller the change, the closer one must get to the source of the change to obtain clear and reliable results.

## Slide 4
What Is Retrofit Isolation?
With retrofit isolation, the source of the change is small relative to its environment—a single piece of equipment, perhaps.
To ensure that environmental “noise” isn’t clouding our measurements, we need to get close to the change. We draw a measurement boundary around the source of the change.
We ignore everything outside that boundary, assuming that it doesn’t have a direct, meaningful influence on the change being assessed.

## Slide 5
July 22-24

## Slide 6
What Is a Single Line Diagram?
Also called: Riser Diagram, One-Line Diagram
A simplified notation for representing:
• Electrical power distribution system
• Path from utility to end uses
• Major equipment: transformers, switchgear, panels
• Shows connectivity, not physical layout
• Critical for understanding measurement boundaries
Simplified Example
UTILITY
│
↓
Main Meter
│
Switchgear
├
┼
┤
Panel A
Lighting
Panel B
HVAC
Panel C
Plugs
Key Point: Shows WHERE to meter
and defines measurement boundaries

## Slide 7
Why Single Line Diagrams Matter in M&V
Define Measurement
Boundary
Shows what's inside/outside
the project scope
Identify Metering
Locations
Where to place meters
for retrofit isolation
Document Baseline
Record system configuration
at baseline
Plan Retrofits
Understand impacts
on electrical system
Verify Installation
Confirm ECMs installed
as designed
Support Settlement
Evidence for disputes
and verification
Without a single line diagram, you're doing M&V blind!

## Slide 8
Reading a Single Line Diagram
Key symbols and what they tell us for M&V
Common Symbols:
⚡
Power source / Utility connection
⊓
Transformer (voltage conversion)
◼
Circuit breaker / Disconnect
⊙
Meter (energy measurement point)
━
Bus / Main distribution
├┤
Branch circuit
⬚
Load (equipment, panel, etc.)
What to Look For in M&V:
✓ Existing meters and their locations
✓ Where you could add sub-meters
✓ What loads are on which circuits
✓ Voltage levels (480V, 208V, 120V)
✓ Transformer locations and sizes
✓ Service entrance and utility connection
✓ Emergency/standby power systems
✓ Major loads: HVAC, lighting, data center

## Slide 9
Example: Real Single Line Diagram
INSERT YOUR REAL DIAGRAM IMAGE HERE
PLACEHOLDER FOR
YOUR REAL
SINGLE LINE DIAGRAM
JPG IMAGE
(Delete this shape and insert your image here)
Teaching Points for Your Diagram:
• Identify the main meter location   • Trace power flow from utility to loads
• Find potential sub-metering points   • Note measurement boundaries for different ECMs

## Slide 10
Using Single Line Diagrams in M&V Process
M&V Planning Phase
✓ Request existing diagram from facility
✓ Verify diagram matches reality (site visit)
✓ Identify existing meters
✓ Mark potential sub-meter locations
✓ Define measurement boundaries
✓ Include annotated diagram in M&V Plan
Implementation & Reporting
✓ Document ECM locations on diagram
✓ Show installed meters
✓ Update for any system changes
✓ Include in post-installation report
✓ Use for operational verification
✓ Reference in settlement discussions
Key Action: Annotate the Diagram for Your Specific M&V Project
★ Highlight measurement boundary with colored box or dashed line
★ Mark all meter locations with labels (M1, M2, etc.)
★ Indicate ECM locations (use color coding or symbols)
★ Add legend explaining your annotations
★ Include both 'before' and 'after' versions if system changes

## Slide 11
Single Line Diagrams: Common M&V Scenarios
How the diagram guides your measurement approach
Scenario 1: Lighting Retrofit (Option A)
What Diagram Shows:
Shows panel serving lighting circuits
M&V Approach:
Sub-meter at lighting panel
OR
Stipulate hours, measure watts
Scenario 2: HVAC Upgrade (Option B)
What Diagram Shows:
Shows dedicated HVAC electrical service
M&V Approach:
Sub-meter at HVAC disconnect
Measure all parameters (kW, runtime, etc.)
Scenario 3: Whole Building (Option C)
What Diagram Shows:
Shows main utility meter location
M&V Approach:
Use existing main meter
No new metering required

## Slide 12
Interactive Effects
Interactive effects are the influence of an ECM on the energy use of other equipment in a facility. For example: lighting reduction  cooling savings.
Some possible approaches: ignore, estimate, measure, or expand the measurement boundary.
Methods for estimating interactive effects:
Calibrated computer simulation
Spreadsheet calculation
Sub-metering
Stipulation from reference

## Slide 13
“Savings” Attribution
When multiple ECMs exist in a single system, it can be challenging to attribute “savings” to specific ECMs.
Example: lighting power and occupancy sensors.

## Slide 14
Fundamental Methods of Measurement in Retrofit Isolation
Performance
Snapshot measurements are taken of the key parameters of energy use in the system.
Justified and auditable estimates provide the rest of the data.
Performance/Operation
Continuous measurements are taken of the key parameters.
No assumptions or estimates are made.

## Slide 15
Common Terminology
IPMVP refers to the performance approach as “key parameter measurement(s)” (Option A) and to the performance/operation approach as “all parameter measurement” (Option B).
ASHRAE distinguishes more than twenty retrofit isolation approaches in Table 5-2 of ASHRAE Guideline 14-2014.
ISO does not provide terminology for retrofit isolation approaches.
IPMVP is a registered trademark of EVO. AEE is using the term “IPMVP” only to refer to the protocol.

> *Notes:* Instructor Note
Consider opening Table 5-2 during the class session. It is on page twenty-nine of this PDF: 
https://piller.s3.us-east-2.amazonaws.com/ASHRAE+Guideline+14-2014.pdf

## Slide 16
Identifying Significant Parameters
Identifying the significant parameters—ones that must be measured—when using a retrofit isolation approach is usually a straightforward process, but there can be challenges, and oversights are always possible.
A set of checks can ensure that no significant parameters are missed:
Review the project’s contractual performance clauses.
Consider additional parameters that will likely be influenced by the ECM.
Define alternative parameters that the client and/or implementer might need measured.

## Slide 17
Identifying Estimable Parameters – when accuracy is key
Whereas significant parameters must (?) be measured, estimations must (?) be justified and auditable.
If a parameter meaningfully influences the range of the reported answer, then the parameter should likely be defined as a significant parameter and be measured rather than estimated. In other words, estimating the parameter would be unjustifiable. (if cost effective)(or allowed)
In terms of audibility, an estimate should be able to be traced to its origin and thus evaluated based on its applicability and “correctness.”

## Slide 18
Enhanced Measurement Approaches
Apart from counting items and measuring electricity, numerous forms of parameter measurement are available in a retrofit isolation approach. Some typical parameters and their measurement approaches include:
Process or ambient temperature: Dedicated probes or infrared sensors
Process flow: Internal or external flow meters
Humidity: Dedicated sensors adapted for environmental or process-specific use
Quality: Batch sampling or continuous measurement, using devices ranging from lasers to belt scales to cameras allowing for visual inspections by AI
Fuel energy: Periodic lab tests and flow meters capable of applying the calorific value to the actual volume measured

## Slide 19
Other Metering Considerations
Sometimes additional metering is not required as it is already in existence. Measurements may be available through the building management system (BMS) or supervisory control and data acquisition (SCADA) system.
In some cases, a measurement could even be sourced from outside the physical measurement boundary—from a weather station, for example.
Each source should be assessed for credibility and applicability.

> *Notes:* https://www.nrel.gov/docs/fy08osti/43156.pdf

## Slide 20
Excel Example
CMVP_Retrofit_Isolation_Example.xlsx

> *Notes:* Update example with something that has variability in the baseline. 
Hannah Seeger?
Show ENRON or other typical physical models for retrofit isolation.

## Slide 21
Key Takeaways
Retrofit isolation approaches draw a measurement boundary around a specific equipment or systems affected by an energy conservation measure.
There are two fundamental methods of measurement in retrofit isolation: performance and performance/operation. These are sometimes referred to as Option A and Option B.

## Slide 22
Module 6: Retrofit Isolation
Describe how you would determine whether a parameter should be measured directly or can be reasonably estimated in a retrofit isolation study.
What are interactive effects, and how might they complicate the attribution of savings in a facility with multiple ECMs?
What field skills are most critical for a practitioner carrying out a retrofit isolation approach, and how do safety considerations come into play?