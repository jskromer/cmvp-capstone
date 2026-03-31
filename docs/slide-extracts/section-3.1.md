# CMVP_v2.0_Section-3.1_Interlude-Basic-Concepts-in-Statistics_G_v1.1.pptx


## Slide 1
INTERLUDEBasic Concepts in Statistics

> *Notes:* Instructor Note: The concepts in this section will be reinforced and shown in action in examples. If the instructor has spreadsheets or other tools to teach these concepts—go for it.

## Slide 2
Uncertainty

## Slide 3
Descriptive Statistics
Descriptive statistics involves analyzing data in a dataset in order to describe and offer meaningful information about the data, including possible relationships among data points.

## Slide 4
Mean
The mean of a set of values is its average, as the term is commonly understood.
It is the sum of all values in the set divided by the number of values.

> *Notes:* Instructor Note: The other types of averages are the median and the mode. The median is the “middle” value in an ascending or descending list of values, or the mean of the two middle-most values if there is an even number of values in the set. The mode is the value that occurs most frequently in a set.

## Slide 5
Maximum and Minimum
Maximum
The largest value in a dataset.
Minimum
The smallest value in a dataset.

## Slide 6
Range and Variance
Range
The difference between the highest and lowest values in a dataset.
Variance
The average of the squared differences from the mean.

## Slide 7
Standard Deviation
A statistical measure of how dispersed the data in a dataset is relative to the mean.
A high standard deviation indicates that the data in a dataset is widely dispersed relative to the mean.
A low standard deviation indicates that the data is clustered relatively closely around the mean.

## Slide 8
Coefficient of Variation (CV)
CV is the ratio of the standard deviation to the mean, often expressed as a percentage.
It tells us how spread out the values in a dataset are relative to the mean: the higher the CV, the greater the dispersion in the dataset.

## Slide 9
CV(RMSE)
Coefficient of variation of root-mean squared error.
In a regression analysis of energy data, CV(RMSE) indicates the model’s predictive capabilities. Put another way, it is a measure of how much uncertainty is inherent in a model.
The lower the CV(RMSE), the lower the uncertainty.

> *Notes:* Instructor Notes
ASHRAE Guideline 14 specifies acceptable CV(RMSE) values for M&V models.
You may wish to mention t-statistics at this point as another means of validating a regression model, degrees of freedom, etc.
Open an Excel spreadsheet to demonstrate.

## Slide 10
Whole-Building Prescriptive Path
“the baseline model shall have a maximum CV(RMSE) of 20% for energy use and 30% for demand quantities when less than 12 months’ worth of post-retrofit data are available for computing savings. These requirements are 25% and 35%, respectively, when 12 to 60 months of data will be used in computing savings. When more than 60 months of data will be available, these requirements are 30% and 40%, respectively”
From ASHRAE Guideline 14

## Slide 11
Normalized Mean Bias Error

## Slide 12
Exercise
Your instructor will give you a string and a ruler. Measure the string five times, writing down each measurement.
For the resulting dataset, calculate the mean, maximum, minimum, range, variance, standard deviation, CV, and CV(RMSE).

## Slide 13
Sampling: Techniques
The selection of a representative and manageable subgroup of data points from a large group (statistical population).
Source: Dan Kernler | CC BY-SA 4.0

## Slide 14
Two samples with the same mean (100) but different standard deviations.

> *Notes:* Instructor Note: You can demonstrate this concept to learners using a spreadsheet.

## Slide 15
Inferential Statistics
Inferential statistics involves analyzing data samples in order to make predictions or inferences about a statistical population.

## Slide 16
Regression Analysis
An analysis of the relationship between independent and dependent variables.
In a graph, a regression line is a visual representation of a linear regression (which assumes a linear relationship between variables).

## Slide 17
Variables in Regression
Independent Variable
A variable presumed to exert influence on a dependent variable
Conventionally plotted on the x-axis of a graph
Dependent Variable
A variable presumed to be influenced by an independent variable
Conventionally plotted on the y-axis of a graph

## Slide 18
Dimensionality
One-Dimensional
Involves one independent variable (predictor) and one dependent variable (response).
Graphically represented by a scatter plot with a line (or curve, depending on the type of regression) that best fits the data points.
Two-Dimensional
Involves two independent variables (predictors) and one dependent variable (response).
In a three-dimensional space, graphically represented by a scatter plot with a plane (or some curved surface) that best fits the data points.

## Slide 19
R (Correlation Coefficient)
A statistical measure ranging from -1.0 to 1.0 that represents how positively or negatively correlated variables are.
There are several ways to determine slope and intercept.
Source: Laerd Statistics | CC BY-SA 4.0

## Slide 20
R2 (Coefficient of Determination)
A statistical measure of how much influence the independent variable has on the dependent variable. It is as measure of both the slope of the linear model and scatter around the line.
It ranges from 0 to 1, with a higher number representing a better “fit” between data and regression line and a ”steeper” slope.

> *Notes:* Open Statistics Spreadsheet

## Slide 21
R-Squared: 0.16

> *Notes:* Instructor Note: At 0.16, the R2 value is low, indicating a poor fit between the data and the regression line.

## Slide 22
Defining Accuracy and Precision
Source: St. Olaf College

## Slide 23
Bias
The Guide to the Expression of Uncertainty in Measurement (GUM) defines bias as “the result of a systematic error”—an error that consistently affects measurements in the same direction.
In other words, bias refers to a consistent or systematic discrepancy between the average of measurement results and the true value.

## Slide 24
Relation to Normal Distribution
High Precision and Low Accuracy

## Slide 25
Normal Distribution and Standard Deviation
Standard deviation represents the confidence interval or the value of the error at a certain confidence level
Source: Gouda Mohamed

## Slide 26
Size of Standard Error vs. Confidence Interval
With different data sets, the same CL represents the same area under the distribution, but the size of the deviation or interval is different.
The smaller the value of the interval, the better the precision.
Source: Johnathan Mun

> *Notes:* https://www.researchgate.net/publication/362345420_Metodos_Quantitativos_de_Pesquisa_Aplicacao_da_Simulacao_de_Risco_Monte_Carlo_Inteligencia_Artificial_Aprendizado_de_Maquina_Ciencia_de_Dados_Previsao_Estocastica_Analise_de_Dados_e_Business_Intellige

## Slide 27
Typical Confidence Levels and Errors
Metering and laboratory results typically operate at a CL of 95%.
A class 1 billing meter thus has an error of 1% at a 95% confidence level.
The social sciences typically work with smaller confidence levels and higher accepted deviations.
A social study with sampled interviews will evaluate results at typically 68% confidence level.

> *Notes:* Instructor Note: This is an illustration of the difference between “machine CL” and “human CL.”

## Slide 28
Acceptable CL and Error Levels for M&V
There are no hard and fast rules regarding acceptable confidence levels and intervals for M&V. Acceptability is function of cost and effort to reduce error.
Some rules of thumb from South Africa (example):
Report at confidence level of 80% (mixture of human and machine)
Precision of plus-or-minus 7% for up to 15 data points
Precision of plus-or-minus 15% for 16–52 data points
Precision of plus-or-minus 20% for more than 52 data points

> *Notes:* Instructor Note: Precision values come from SANAS (South African National Accreditation System) TG50-02. Values may vary depending on the contractual agreement between stakeholders.

## Slide 29
Combining Uncertainty
Measured 80 units before
Measured 60 units after
With a 5% meter accuracy
What’s the relative uncertainty (Utot) of the impact?
Utot = sqrt ((80*.05)^2 + (60*.05)^2) = sqrt (16+9)= 5
5/20 = .25 or 25%
IPMVP is a registered trademark of EVO. AEE is using the term “IPMVP” only to refer to the protocol.
Pythagorus?

## Slide 30
Degrees of Freedom
Degrees of freedom (df) in a basic statistics course typically refers to the number of independent pieces of information available for calculating a statistical parameter or test statistic. It represents how many values can vary freely after certain constraints (like means or totals) have been applied.
For example, when calculating the variance of a sample with n observations, you first estimate the mean, and thus lose one degree of freedom, resulting in n−1 degrees of freedom.
In short, degrees of freedom indicate how many numbers in your calculation are free to vary once you've accounted for other parameters or constraints.

## Slide 31
Links to Resources
BPA Uncertainty Guide
EVO – IPMVP 2012 – APPENDIX B
EVO STATS AND UNCERTAINTY GUIDE
ASHRAE 14
EVO= Efficiency Valuation Organization
IPMVP is a registered trademark of EVO. AEE is using the term “IPMVP” only to refer to the protocol.