# Transform Module
 
The **Transform module** in Owl Mix provides a structured pipeline for applying feature engineering techniques commonly used in **Marketing Mix Modeling (MMM)**.
 
---
 
## 🎯 Purpose
 
Transform raw input data into **model-ready features** using:
 
- Lag transformations
- Adstock (carryover effects)
- Saturation (diminishing returns)
 
---
 
## 🏗️ Main Class: `TransformPipeline`
 
```python
from owlmix.transform.pipeline import TransformPipeline
```
 
---
 
## 🚀 Example Usage
 
```python
pipeline = TransformPipeline()
 
pipeline.add_lag(column="tv_spend", lag=1)
pipeline.add_adstock(column="tv_spend", decay=0.5)
pipeline.add_saturation(column="tv_spend", method="hill", k=100, s=2)
 
df_transformed = pipeline.run(df)
```
 
---
 
## 🔄 Transformation Order
 
Transformations are applied sequentially:
 
1. Lag
2. Adstock
3. Saturation
 
This reflects standard MMM preprocessing workflows.
 
---
 
## 🔧 Available Transformations
 
### 1. Lag
 
Shifts values by a specified number of periods.
 
```python
pipeline.add_lag(column="tv_spend", lag=1)
```
 
---
 
### 2. Adstock
 
Captures carryover effects of marketing spend.
 
```python
pipeline.add_adstock(column="tv_spend", decay=0.5)
```
 
---
 
### 3. Saturation
 
Applies diminishing returns transformation.
 
```python
pipeline.add_saturation(column="tv_spend", method="hill", k=100, s=2)
```
 
---
 
## 🧱 Design Principles
 
- Modular: Each transformation is independent
- Chainable: Easily build pipelines
- Extensible: Add custom transformations
 
---
 
## 🧩 Adding Custom Transformations
 
```python
pipeline.add_custom(func=my_function, column="sales")
```
 
---
 
## ⚠️ Important Notes
 
- Transformations may introduce `NaN` values
- Always apply cleanup after transformations
- Ensure data is time-ordered
 
---
 
## 🔗 Integration with EDA
 
Typical workflow:
 
1. Run transformations
2. Clean data
3. Perform EDA
4. Build model
 