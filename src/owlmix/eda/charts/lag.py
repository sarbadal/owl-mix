# src/owlmix/eda/charts/lag.py
 
import matplotlib.pyplot as plt
 
 
def plot_lag_correlation(series, title="Lag Correlation", show=True):
    fig, ax = plt.subplots()
 
    ax.plot(series.index, series.values, marker="o")
 
    ax.set_xlabel("Lag")
    ax.set_ylabel("Correlation")
 
    fig.suptitle(title)
    fig.tight_layout()
 
    if show:
        plt.show()
 
    return fig