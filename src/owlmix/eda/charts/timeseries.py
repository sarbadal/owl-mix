# src/owlmix/eda/charts/timeseries.py
 
import matplotlib.pyplot as plt
 
 
def plot_time_series(df, columns, date_col=None, show=True):
    fig, ax = plt.subplots()
 
    if date_col:
        x = df[date_col]
    else:
        x = df.index
 
    for col in columns:
        ax.plot(x, df[col], label=col)
 
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.legend()
 
    fig.tight_layout()
 
    if show:
        plt.show()
 
    return fig