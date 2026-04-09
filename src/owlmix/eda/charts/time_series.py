# src/owlmix/eda/charts/timeseries.py
 
import os
import matplotlib.pyplot as plt
 
 
class TimeSeriesChart:
    def __init__(self, df, output_dir, columns=None, target=None):
        self.df = df
        self.output_dir = output_dir
        self.columns = columns
        self.target = target
 
    def generate(self):
        # -------------------------
        # Resolve columns
        # -------------------------
        if self.columns is None:
            if self.target and self.target in self.df.columns:
                cols = [self.target]
            else:
                # fallback: numeric columns only
                cols = self.df.select_dtypes(include="number").columns.tolist()
 
                # avoid plotting too many
                cols = cols[:5]
 
        else:
            cols = self.columns
 
        if not cols:
            raise ValueError("No valid columns available for TimeSeriesChart")
 
        # -------------------------
        # Plot
        # -------------------------
        plt.figure(figsize=(10, 5))
 
        for col in cols:
            plt.plot(self.df[col], label=col)
 
        plt.legend()
        plt.title("Time Series Plot")
 
        file_path = os.path.join(self.output_dir, "time_series.png")
        plt.savefig(file_path)
        plt.close()
 
        return file_path