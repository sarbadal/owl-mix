# src/owlmix/eda/charts/correlation.py
 
import matplotlib.pyplot as plt
import numpy as np
 
 
def plot_correlation_heatmap(df, title="Correlation Heatmap", show=True):
    corr = df.corr(numeric_only=True)
 
    fig, ax = plt.subplots()
 
    cax = ax.imshow(corr.values)
 
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
 
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
 
    # Annotate values
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.values[i, j]:.2f}",
                    ha="center", va="center", fontsize=8)
 
    fig.colorbar(cax)
 
    fig.suptitle(title)
    fig.tight_layout()
 
    if show:
        plt.show()
 
    return fig