# src/owlmix/eda/charts/outliers.py
 
import os
import matplotlib.pyplot as plt
 
 
class OutlierChart:
    def __init__(self, df, output_dir, columns=None):
        self.df = df
        self.output_dir = output_dir
        self.columns = columns
 
    def generate(self):
        if self.columns is None:
            cols = self.df.select_dtypes(include="number").columns.tolist()
            cols = cols[:5]  # limit
        elif isinstance(self.columns, str):
            cols = [self.columns]
        else:
            cols = self.columns
 
        # -------------------------
        # Validate columns
        # -------------------------
        valid_cols = [c for c in cols if c in self.df.columns]
 
        if not valid_cols:
            raise ValueError("No valid columns found for OutliersChart")
 
        # -------------------------
        # Plot
        # -------------------------
        plt.figure(figsize=(10, 5))
 
        self.df[valid_cols].boxplot()
 
        plt.title("Outliers Detection (Box Plot)")
 
        file_path = os.path.join(self.output_dir, "outliers.png")
        plt.savefig(file_path)
        plt.close()
 
        return file_path
 