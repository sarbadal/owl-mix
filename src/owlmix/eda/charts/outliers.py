# src/owlmix/eda/charts/outliers.py
import os
import pandas as pd
import matplotlib.pyplot as plt
 

# TODO: Add datapoints to the charts

class OutlierChart:
    def __init__(self, df, output_dir: str, columns=None, max_cols_per_chart=4, single_image=True):
        """
        Parameters:
        - df: pandas DataFrame
        - output_dir: where images will be saved
        - max_cols_per_chart: number of columns per boxplot
        - single_image: if True → one grid image, else multiple images
        """
        self.df = df
        self.output_dir = output_dir
        self.columns = columns
        self.max_cols_per_chart = max_cols_per_chart
        self.single_image = single_image

    def _get_numeric_columns(self):
        if self.columns is None:
            return self.df.select_dtypes(include=["number"]).columns.tolist()

        valid_columns = []
        numeric_cols = self.df.select_dtypes(include=["number"]).columns.tolist()
        for col in self.columns:
            if col in numeric_cols:
                valid_columns.append(col)

        return valid_columns

    def _chunk_columns(self, columns):
        """Split columns into chunks"""
        for i in range(0, len(columns), self.max_cols_per_chart):
            yield columns[i:i + self.max_cols_per_chart]

    def _generate_multiple_images(self, numeric_cols):
        image_paths = []
 
        for idx, cols in enumerate(self._chunk_columns(numeric_cols)):
            plt.figure(figsize=(6 * len(cols), 5))
 
            self.df[cols].boxplot()
            plt.title(f"Outliers: {', '.join(cols)}")
            plt.xticks(rotation=45)
 
            file_path = os.path.join(self.output_dir, f"outliers_{idx}.png")
            plt.savefig(file_path, bbox_inches="tight")
            plt.close()
 
            image_paths.append(file_path)
 
        return image_paths

    def _generate_single_image(self, numeric_cols):
        chunks = list(self._chunk_columns(numeric_cols))
        n_chunks = len(chunks)
 
        fig, axes = plt.subplots(
            nrows=n_chunks,
            figsize=(10, 5 * n_chunks)
        )
 
        if n_chunks == 1:
            axes = [axes]
 
        image_path = os.path.join(self.output_dir, "outliers_combined.png")
 
        for ax, cols in zip(axes, chunks):
            self.df[cols].boxplot(ax=ax)
            ax.set_title(f"Outliers: {', '.join(cols)}")
            ax.tick_params(axis='x', rotation=45)
 
        plt.tight_layout()
        plt.savefig(image_path, bbox_inches="tight")
        plt.close()
 
        return image_path

    def generate(self):
        numeric_cols = self._get_numeric_columns()
 
        if not numeric_cols:
            return []
 
        if self.single_image:
            return self._generate_single_image(numeric_cols)
        
        return self._generate_multiple_images(numeric_cols)
 