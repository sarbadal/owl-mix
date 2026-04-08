# Owl Mix
 
**Owl Mix** is a flexible and modular Python pipeline designed for data transformation and exploratory data analysis (EDA), with a strong focus on **Marketing Mix Modeling (MMM)** workflows.
 
It helps practitioners efficiently **explore, analyze, and transform data before model building**, making it particularly useful in MMM use cases where feature engineering plays a critical role.
 
---
 
## 🚀 Features
 
- 📊 Built for **MMM data preparation and exploration**
- 📉 Lag feature generation
- 🔁 Adstock transformations (capture media carryover effects)
- 📈 Saturation transformations for diminishing returns:
  - Hill
  - Logarithmic
  - Exponential
- 🧹 Final cleanup utilities:
  - Drop NA values
  - Reset index
- 🧱 Modular and extensible pipeline design
 
---
 
## 🎯 Use Case
 
**Owl Mix** is especially helpful for:
 
- Marketing Mix Modeling (MMM)
- Pre-model data transformation
- Exploratory Data Analysis (EDA)
- Time series feature engineering
- Preparing datasets for regression or machine learning models
 
In MMM workflows, it is commonly used to:
 
- Analyze trends and patterns in marketing data  
- Transform raw variables into model-ready features  
- Apply domain-specific transformations like **adstock and saturation**  
- Clean and finalize datasets before model training  
 
---
 
## 📦 Installation
 
```bash
pip install owl-mix
```
 
Or install locally:
 
```bash
pip install -e .
```
 
---
 
## 🧠 Core Transformations
 
### 1. Lag Transformation
 
Shifts a column by `n` time steps.
 
```python
df["lag_1"] = df["value"].shift(1)
```
 
---
 
### 2. Adstock Transformation
 
Captures carryover effects of marketing spend.
 
```python
def adstock(series, decay):
    result = []
    prev = 0
    for val in series:
        prev = val + decay * prev
        result.append(prev)
    return result
```
 
---
 
### 3. Saturation Functions
 
Models diminishing returns of media spend.
 
#### Hill Function
 
```python
def hill(x, k, s):
    return (x ** s) / (x ** s + k ** s)
```
 
#### Logarithmic
 
```python
def log_saturation(x):
    return np.log1p(x)
```
 
#### Exponential
 
```python
def exp_saturation(x, alpha):
    return 1 - np.exp(-alpha * x)
```
 
---
 
### 4. Final Cleanup
 
Removes missing values and resets index after transformations.
 
```python
def cleanup_data(df):
    return df.dropna().reset_index(drop=True)
```
 
---
 
## 🏗️ Pipeline Usage
 
### Example Workflow
 
```python
from owlmix.transform import MMMTransformPipeline
from owlmix.utils.cleanup import cleanup_data
 
pipeline = MMMTransformPipeline()
 
pipeline.add_lag(column="sales", lag=1)
pipeline.add_adstock(column="marketing_spend", decay=0.5)
pipeline.add_saturation(column="marketing_spend", method="hill", k=100, s=2)
 
df_transformed = pipeline.transform(df)
 
# Final cleanup
df_final = cleanup_data(df_transformed)
```
 
---
 
## ⚙️ Transformation Pipeline Order
 
Transformations are applied sequentially:
 
1. Lag
2. Adstock
3. Saturation
4. Final cleanup (recommended)
 
This mirrors standard MMM preprocessing workflows.
 
---
 
## 📁 Suggested Project Structure
 
```
owlmix/
│
├── transform/
│   ├── pipeline.py
│   ├── lag.py
│   ├── adstock.py
│   ├── saturation.py
│
├── utils/
│   ├── cleanup.py
│
├── __init__.py
```
 
---
 
## 🧩 Extending the Pipeline
 
You can add custom transformations:
 
```python
pipeline.add_custom(func=my_function, column="sales")
```
 
---
 
## ⚠️ Notes
 
- Lag and adstock transformations introduce `NaN` values — always apply cleanup.
- Ensure data is **time-ordered** before applying transformations.
- Designed with MMM workflows in mind but usable for general feature engineering.
 
---
 
## 🤝 Contributing
 
Contributions are welcome! Feel free to open issues or submit pull requests.
 
---
 
## 📄 License
 
MIT License
 