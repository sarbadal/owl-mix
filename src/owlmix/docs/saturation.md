# Saturation Functions
 
Saturation functions model **diminishing returns** in Marketing Mix Modeling (MMM).
 
As marketing spend increases, the incremental impact on the target variable (e.g., sales) decreases.
 
---
 
## 🎯 Why Saturation Matters
 
- Prevents overestimating impact of high spend
- Reflects real-world marketing behavior
- Improves model realism
 
---
 
## 📊 Available Methods
 
### 1. Hill Function
 
```python
def hill(x, k, s):
    return (x ** s) / (x ** s + k ** s)
```
 
#### Parameters
 
| Parameter | Description |
|----------|-------------|
| k | Half-saturation point |
| s | Shape parameter |
 
---
 
### 2. Logarithmic Saturation
 
```python
def log_saturation(x):
    return np.log1p(x)
```
 
- Simple and stable
- Good baseline transformation
 
---
 
### 3. Exponential Saturation
 
```python
def exp_saturation(x, alpha):
    return 1 - np.exp(-alpha * x)
```
 
#### Parameters
 
| Parameter | Description |
|----------|-------------|
| alpha | Growth rate |
 
---
 
## 🚀 Usage in Pipeline
 
```python
pipeline.add_saturation(
    column="tv_spend",
    method="hill",
    k=100,
    s=2
)
```
 
---
 
## 📈 Choosing the Right Function
 
| Method | When to Use |
|------|------------|
| Hill | Most flexible, widely used in MMM |
| Log | Simple baseline |
| Exponential | Smooth growth behavior |
 
---
 
## ⚠️ Notes
 
- Always apply after adstock
- Ensure values are non-negative
- Parameter tuning is critical for model performance
 