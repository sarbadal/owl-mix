# src/owlmix/eda/charts/outliers.py
 
import matplotlib.pyplot as plt
 
 
def plot_boxplot(df, columns, show=True):
    fig, ax = plt.subplots()
 
    data = [df[col].dropna() for col in columns]
 
    ax.boxplot(data, labels=columns)
 
    ax.set_title("Boxplot (Outlier Detection)")
    ax.set_ylabel("Values")
 
    fig.tight_layout()
 
    if show:
        plt.show()
 
    return fig