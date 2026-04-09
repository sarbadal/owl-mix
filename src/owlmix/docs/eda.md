# EDA Module
 
The **EDA module** in Owl Mix provides tools for exploratory data analysis tailored for **Marketing Mix Modeling (MMM)** workflows.
 
It helps users:
- Understand dataset structure
- Identify missing values
- Analyze correlations
- Explore lag relationships between variables and target
 
---
 
## 📦 Main Class: `EDAAnalyzer`
 
```python
from owlmix.eda import EDAAnalyzer
```
 
### Initialization
 
```python
eda = EDAAnalyzer(df, target="sales")
```
 
| Parameter | Description |
|----------|-------------|
| df | Input pandas DataFrame |
| target | Target variable (optional but required for lag analysis) |
 
---
 
## 🔍 Available Methods
 
### 1. `basic_stats()`
 
Returns column-level summary:
 
- Data type
- Missing count
- Missing percentage
- Unique values
 
```python
eda.basic_stats()
```
 
---
 
### 2. `correlation()`
 
Computes correlation matrix for numeric variables.
 
```python
eda.correlation()
```
 
---
 
### 3. `lag_correlation(column, lags)`
 
Analyzes correlation between lagged feature and target.
 
```python
eda.lag_correlation("tv_spend", lags=[1, 2, 3])
```
 
---
 
### 4. `summary()`
 
Generates a formatted text report combining:
 
- Dataset overview
- Missing values
- Descriptive statistics
- Correlation matrix
 
```python
report = eda.summary()
```
 
Save to file:
 
```python
with open("eda_report.txt", "w") as f:
    f.write(report)
```
 
---
 
## 🧠 Why EDA Matters in MMM
 
In Marketing Mix Modeling:
 
- Data transformations depend heavily on **lag relationships**
- Correlation helps identify **potential drivers**
- Missing values can distort model estimation
 
The EDA module helps prepare **model-ready insights before transformation and modeling**.
 
---
 
## 🔧 Extensibility
 
You can extend the summary using internal builder methods:
 
```python
builder.add_custom("My custom section")
```
 
Future extensions may include:
 
- Seasonality detection
- Trend decomposition
- Outlier detection
 