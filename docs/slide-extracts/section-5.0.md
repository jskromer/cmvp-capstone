# CMVP_v2.0_Section-5.0_Whole-Facility-Approaches_G_v1.2.pptx


## Slide 1
MODULE 5Whole Facility Approaches

## Slide 2
Learning Objectives
Define key terms: whole facility approach, statistical and physical models, significant parameter, proxy variable, stepwise analysis, parameter sweep, static factor, non-routine adjustment
Discuss the strengths and weaknesses of whole facility approaches
Identify the metering requirements of whole facility approaches
Differentiate between contractual and utility program whole facility approaches

## Slide 3
What Is a Whole Facility Approach?
Whole facility approaches measure the effects of ECMs on whole facilities (or parts of facilities) rather than the effects on isolated equipment or systems.
Such approaches generate estimates of “total” savings, usually encompassing multiple interventions and often including savings from measures that are too difficult or costly to directly quantify using other means.
Sometimes a whole facility is necessary—and sometimes it is simply preferred due to the ready availability of meters.

## Slide 4
Statistical and Hybrid/Physical Models
There are two fundamental methods in whole facility approaches for developing adjusted baseline models:
Statistical, or “inverse” modeling, which relies on the measurement of independent and dependent variables and the analysis of their relationship. In Module 1, we called these models statistical models.
Physics-based “forward” simulation modeling. Throughout this training, we call these models physical models.

> *Notes:* Instructor Note: These are Options C and D in FEMP (or IPMVP).

## Slide 5
STATISTICAL MODELS = COUNTERFACTUAL MACHINES
STEP 1: BASELINE PERIOD (Learning / fitting)
Energy = f(Weather, Occupancy, Time) + error
↓
Model learns relationships
STEP 2: REPORTING PERIOD ()
Input: This year's conditions
Apply: Learned relationships
Output: THE COUNTERFACTUAL
Meaning: "What WOULD have happened"
STEP 3: CALCULATE SAVINGS
Counterfactual - Actual = Avoided Energy
The model  baseline into future.

## Slide 6
Whole Facility ApproachesStatistical (AKA Option C)
Strengths
All the metering you need is often already installed: utility billing meter.
Sometimes cheaper.
Captures interactive effects.
Weaknesses
Can you identify the factors that influence energy use and create a model?
Can you see the savings at this level?
Cannot determine ECM-level results.
Possibly complex non-routine adjustments.

## Slide 7
Whole Facility ApproachesStatistical (AKA Option C)
Examples
Custom
NMEC (California and elsewhere)
Normalized Metered Energy Consumption
Strategic Energy Management (ISO 50001)
CalTrack / OpenEE Meter

## Slide 8
Why Load Shape Matters Now
• Energy rates vary by time-of-use (TOU), season, and demand charges.
• A kWh saved during peak hours is more valuable than off-peak.
• Load shape reveals the distribution of energy use over time.

## Slide 9
Significant Parameters Statistical Models
Significant parameters are identifiable factors (occurring within the measurement boundary) that meaningfully influence a dependent variable.
Identifying significant parameters requires both subject matter expertise and professional judgment.
Some significant parameters might be used as independent variables in the baseline model.

> *Notes:* Instructor Notes
Significant parameters are potential independent variables.
The first step in M&V is to identify these parameters. The next step is to build a model.

## Slide 10
Physical Models
These are simplified models describing first principles engineering (such as heat and mass transfer) created with custom spreadsheets or complex (open- or closed-source) software tools.
Regardless of the software used, physical models:
Use sets of input data
Are connected by algorithms
Generate sets of output data

> *Notes:* Open Title 24 Compliance 
CBECC.com
Add slides for eQuest and Open Studio and IES. ;…

https://energy-models.com

https://www.ibpsa.us

https://unmethours.com/questions/

Useful for – New Construction
	Code Compliance
	Interactive Effects
	Non-routine adjustments

## Slide 11
Physical Models
Physical models are useful for…
New construction
Code compliance (such as California’s Title 24)
Interactive effects
Non-routine adjustments
Static Factors = all the variables in a simulation….

## Slide 12
Physical Models: Tools

> *Notes:* Instructor Note: Here, briefly demonstrate a range of “whole facility” tools:
Excel
ECAM
UT3
eQuest
OpenStudio
Trace 3D Plus
IES
IBPSA

## Slide 13
Building Energy Asset Score
(Mention that this is another dimension of ”Performance”)
Is the equipment / assets in place to run efficiently. No guarantee!  But important to know when thinking about M&V planning
Further Reading: energy.gov/eere/buildings/building-energy-asset-score

## Slide 14
Significant Parameters Physical Models
Physical models contain many more inputs than statistical models.
Significant parameters are the subset of all the inputs that have a significant influence on the outputs.
The challenge for M&V is to identify and quantify a manageable number of parameters. Judgement is required!

> *Notes:* More training is coming!!!

## Slide 15
Sensitivity AnalysisFor Physical Models
Input sensitivity tests are performed to determine which inputs have the greatest impact on the dependent variable.
Typically, the influence of each parameter is ranked, and appropriate parameter measurement systems are identified until the budget for measurement systems is approached. Often, a building management system (BMS) can be cost effectively configured to provide near-direct measurements of significant parameters, which can be transformed into the inputs of the physical model.

> *Notes:* - Link to Monte Carlo simulatons - https://support.microsoft.com/en-us/office/introduction-to-monte-carlo-simulation-in-excel-64c0ba99-752a-4fa8-bbd3-4450d8db16f1

Parametric Analysis Tools - https://nrel.github.io/OpenStudio-user-documentation/reference/parametric_analysis_tool_2/

eQuest - https://energy-models.com/training/equest/parametric-runs

## Slide 16
Additional Tools
Introduction to Monte Carlo Simulation in Excel
Parametric Analysis Tool (PAT) Interface Guide
Parametric Runs in eQUEST

## Slide 17
Static Factors
Static factors can significantly influence a dependent variable but are stable during the baseline and are not expected to vary during reporting period. They are all the variables not selected as “significant.”
By their very nature, projects employing whole facility approaches have expansive measurement boundaries that encompass many parameters that can and do influence the dependent variable.
Because finite time and resources are available to establish baseline static factors, judgment of where and how to prioritize efforts is needed.

## Slide 18
Documenting Static Factors
The development of an adequate and accurate accounting of a project’s baseline static factors allows for an equitable estimate of the impact of a change in static factors if and when such a change is observed. This is referred to as a non-routine adjustment.
An effective M&V plan should identify the project’s baseline static factors and address how, when, and by whom static factors will be monitored during the reporting period.

## Slide 19
Proxy Variables
Budget or technical constraints often require that proxy variables be substituted for significant parameters.
A proxy variable must have an understood, highly correlated relationship with a group of significant factors while also being simpler and less expensive to measure than measuring all the significant parameters that it represents separately.
Proxy variables are selected based on a cost/benefit analysis.

> *Notes:* Instructor Note: Example—dam level variation vs. flow rate (weir).

## Slide 20
Using (Calibrated) Physical Models
Goals
Identify significant model inputs. For calibration, measure.
Identify insignificant model inputs. For calibration, use fixed value.
ASHRAE Guideline 14 has criteria for “good enough” calibration, but some judgment is required!

## Slide 21
Interactive Effects
When whole facility statistical models are used, it is difficult to quantify the savings generated by an individual ECM. It is also unnecessary to quantify any interactions that occur between ECMs—a common issue in retrofit isolation approaches.
By contrast, physical models can be used to develop estimates of both individual ECM savings and “package” savings: savings estimates that account for interactions between ECMs.
Be careful!! Order of Operations Matters!!
= Attributing savings to multiple measures – what order?

## Slide 22
Advanced Monitoring Methods for Static Factor Changes
Advanced whole facility M&V methods that leverage data analytics technology are available. In general, these methods use custom “data pipelines” along with automated routines to identify changes in static factors. When a change is identified, first principles engineering techniques can be applied to estimate its impact.
An entire industry focuses on fault detection (FDD) and anomaly detection. One example of this technology is SkySpark’s suite of energy analysis tools: https://skyfoundry.com/.

## Slide 23
Uncertainty for Whole Facility
Statistical Models
CV(RMSE) is the main statistic of interest.
Fractional savings uncertainty (FSU).
“Savings” should be at least two times the RMSE.
Physical Models
A full discussion of uncertainty is beyond the scope of this class.
More information can be found through ASHRAE.

> *Notes:* Link to statistics spreadsheet.

Instructor Note: This is a link to a discussion of uncertainty in physical models (Option D): https://github.com/NREL/IPMVP/blob/master/docs/Option%20D%2005242017.docx

## Slide 24
Fractional Savings Uncertainty
Reddy and Claridge, “Uncertainty of ‘Measured’ Energy Savings from Statistical Baseline Models”
Touzani et al., “Evaluation of Methods to Assess the Uncertainty in Estimated Energy Savings”
The ratio of uncertainty in “savings” to the total expected (or realized) energy ”savings.”

## Slide 25
Fractional Savings Uncertainty

## Slide 26
Excel Example
CMVP_Option_C_Energy_Balance_Example.xlsm

## Slide 27
Utility Program Considerations
Depending on the regulations that govern an energy efficiency program, calculating savings using a whole facility approach may or may not be permissible.
Review the utility and regulator guidelines and restrictions to determine if a whole facility approach can be used.
If the whole facility approach is allowed, requirements for data cleaning, model statistics, eligible projects, adjustments, savings magnitude, and reporting requirements will be outlined in the utility and regulator guidelines.

> *Notes:* Instructor Note
If possible, the instructor should share sets of regulations to illustrate the information contained in this slide. Try to choose locally relevant sets of regulations. Here are some US-specific guidelines: 
PG&E M&V Requirements for Site-Level NMEChttps://www.pge.com/pge_global/common/pdfs/save-energy-money/facility-improvements/custom-retrofit/PGE-Site-NMEC-MV-Requirements.pdf
California Industrial SEM M&V Guidehttps://semhub.com/assets/resources/CA_Industrial_SEM_MV_Guide.pdf
Commercial & Industrial SEM M&V Reference Guidehttps://www.bpa.gov/-/media/Aep/energy-efficiency/measurement-verification/12-bpa-ci-sem-mv-ref-guide-v10.pdf

## Slide 28
Measurement Boundary
Meters don’t always just measure one building.
Over or under served
You can always put your own metering on the building!

## Slide 29
Key Takeaways
There are two types of models: statistical and physical.
The main advantage of the whole facility approach is that it captures all energy savings, regardless of cause.
For statistical models, the main disadvantage is that it can be more difficult to attribute energy savings to specific retrofits.
Energy Models (physical) are often superior, but difficult
The potential for “noise” (non-routine adjustments) is always an issue.
In all cases, balance costs and benefits!

> *Notes:* Instructor Notes
In this approach, non-routine adjustments can be very expensive, and these costs can build over time.
The number and complexity of non-routine adjustments is typically greater than with retrofit isolation.

## Slide 30
Module 5: Whole Facility Approaches
What are the main advantages and disadvantages of using statistical modeling versus physical modeling for whole facility M&V?
How does the CV(RMSE) statistic help you assess whether your baseline model is ‘good enough’ for energy savings determination?
In what situations would significant parameters be substituted with proxy variables, and what are the risks of doing so?