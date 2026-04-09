# 🦉 Owl Mix
 
**Owl Mix** is a Python package designed for **data transformation and exploratory data analysis (EDA)**, specifically tailored for **Marketing Mix Modeling (MMM)** workflows.
 
It helps data scientists and analysts:
- Transform raw marketing data into model-ready features
- Perform structured exploratory analysis
- Understand relationships between media variables and target outcomes
 
---
 
## 🚀 Key Features
 
### 🔄 Transformations (MMM-ready)
- Lag creation
- Adstock (carryover effects)
- Saturation (diminishing returns)
- Pipeline-based transformation workflow
 
### 📊 Exploratory Data Analysis
- Dataset summary (missing values, types, stats)
- Correlation analysis
- Lag correlation with target variable
- Exportable text reports
 
### 🧱 Modular Design
- Clean and extensible architecture
- Easily add custom transformations and EDA components
 
---
 
## 📦 Installation
 
```bash
pip install owl-mix
```
 
Then import in Python:
 
```python
import owlmix
```
 
---
 
## ⚡ Quick Example
 
```python
from owlmix.transform.pipeline import TransformPipeline
from owlmix.eda import EDAAnalyzer
from owlmix.utils.cleanup import final_cleanup
 
# Step 1: Transform data
pipeline = TransformPipeline()
 
pipeline.add_lag("tv_spend", lag=1)
pipeline.add_adstock("tv_spend", decay=0.5)
pipeline.add_saturation("tv_spend", method="hill", k=100, s=2)
 
df_transformed = pipeline.run(df)
 
# Step 2: Cleanup
df_clean = final_cleanup(df_transformed)
 
# Step 3: EDA
eda = EDAAnalyzer(df_clean, target="sales")
 
print(eda.basic_stats())
print(eda.correlation())
 
report = eda.summary()
 
with open("eda_report.txt", "w") as f:
    f.write(report)
```
 
---
 
## 📁 Project Structure
 
```text
owlmix/
│
├── eda/
│   ├── analyzer.py
│   ├── stats.py
│   ├── correlation.py
│   ├── summary.py
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
examples/
docs/
```
 
---
 
## 📚 Documentation
 
Detailed documentation is available in the `docs/` folder:
 
- `docs/eda.md` → EDA module
- `docs/transform.md` → Transformation pipeline
- `docs/saturation.md` → Saturation methods
 
---
 
## 🧪 Examples
 
Ready-to-run examples are available in the `examples/` folder:
 
- `eda_basic.py`
- `eda_full_workflow.py`
- `transform_pipeline_example.py`
- `mmm_workflow_example.py` ⭐
 
---
 
## 🧠 Use Case: Marketing Mix Modeling (MMM)
 
Owl Mix is particularly useful for:
 
- Preprocessing marketing data
- Feature engineering for MMM
- Understanding lagged media effects
- Generating EDA reports before modeling
 
---
 
## 🔧 Roadmap
 
Planned enhancements:
 
- Visualization support (plots, heatmaps)
- HTML report generation
- Automated MMM diagnostics
- CLI support
 
---
 
## 🤝 Contributing
 
Contributions are welcome!
 
Feel free to:
- Open issues
- Suggest features
- Submit pull requests
 
---
 
## 📄 License
 
This project is licensed under the MIT License.
 
---
 
## ⭐ Support
 
If you find this project useful, consider giving it a star ⭐ on GitHub!
 