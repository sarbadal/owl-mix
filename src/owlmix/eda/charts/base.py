# src/owlmix/eda/charts/base.py
 
import matplotlib.pyplot as plt


class BaseChart:
    def __init__(self, output_dir="outputs/charts", style=None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.style = style
 
    def setup(self):
        if self.style:
            plt.style.use(self.style)
 
    def save(self, filename: str):
        import matplotlib.pyplot as plt
 
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        return str(filepath)