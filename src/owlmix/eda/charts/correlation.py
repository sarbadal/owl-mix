# src/owlmix/eda/charts/correlation.py
 
import os
import matplotlib.pyplot as plt
import seaborn as sns
 
 
class CorrelationChart:
    def __init__(self, df, output_dir="charts"):
        self.df = df
        self.output_dir = output_dir
 
    def generate(self):
        os.makedirs(self.output_dir, exist_ok=True)
        corr = self.df.corr(numeric_only=True)
 
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm")
 
        file_path = os.path.join(self.output_dir, "correlation.png")
        plt.savefig(file_path)
        plt.close()
 
        return file_path