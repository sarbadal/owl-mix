.. _user-guide.overview:

Overview
========
 
OwlMix EDA is a specialized exploratory data analysis (EDA) toolkit designed
for pre-modeling analysis in Market Mix Modeling (MMM) workflows.
 
It helps analysts and data scientists understand the structure, behavior,
and relationships within time-series marketing data before building models.
 
Why OwlMix EDA?
----------------
 
In MMM and similar time-series problems, understanding the data is critical.
Raw datasets often contain:
 
- Time dependencies (lags, seasonality)
- Non-linear relationships
- Delayed feature impact on target variables
- Mixed data types (numerical and categorical)
 
OwlMix EDA provides a structured and automated way to explore these aspects,
reducing manual effort and improving analysis consistency.
 
What Problems It Solves
-----------------------
 
OwlMix EDA focuses on answering key pre-modeling questions:
 
- How does each feature relate to the target variable?
- Are there lag effects in the data?
- What is the correlation structure across variables?
- How do distributions differ across variables?
- Are there observable trends over time (YoY, QoQ)?
- Is there any indication of causality between variables?
 
Core Capabilities
------------------
 
The library provides the following major analysis components:
 
**1. Variable Relationship Analysis**
   - Target vs feature plots
   - Scatter plots and trend visualization
   - Correlation matrices
 
**2. Time Series & Lag Analysis**
   - Lag correlation analysis (X_t vs X_{t-k})
   - Identification of delayed effects
   - Temporal dependency visualization
 
**3. Distribution Analysis**
   - Numerical feature distributions
   - Categorical frequency distributions
   - Skewness and spread insights
 
**4. Time-Based Comparisons**
   - Year-over-Year (YoY) comparisons
   - Quarter-over-Quarter (QoQ) analysis
   - Trend and seasonality visualization
 
**5. Causality Analysis**
   - Statistical tests for directional relationships
   - Helps identify potential cause-effect patterns
 
How It Fits in Your Workflow
----------------------------
 
OwlMix EDA is intended to be used as the **first step** in your modeling pipeline:
 
1. Load and prepare your dataset
2. Run OwlMix EDA analysis
3. Identify important features and patterns
4. Use insights to guide feature engineering and modeling
 
This ensures that your downstream MMM models are built on a well-understood
data foundation.
 
Design Philosophy
-----------------
 
OwlMix EDA is built with the following principles:
 
- **Clarity over complexity** — simple, interpretable outputs
- **MMM-focused** — tailored for marketing and time-series data
- **Automation-first** — minimal manual configuration required
- **Extensible** — easy to integrate into existing workflows
 
Next Steps
----------
 
To get started, continue to:
 
- :doc:`../getting-started/quickstart`
- :doc:`../user-guide/overview`

:ref:`Back to Home <home>`
