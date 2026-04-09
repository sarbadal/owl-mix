# src/owlmix/eda/summary.py
 
import pandas as pd
import textwrap
 
 
class SummaryBuilder:
    def __init__(self, df: pd.DataFrame, target: str | None = None):
        self.df = df
        self.target = target
        self.sections = []
 
    def add_basic_info(self):
        info = textwrap.dedent(f"""
            DATASET OVERVIEW
            ----------------
            Rows: {self.df.shape[0]}
            Columns: {self.df.shape[1]}
            Target: {self.target}
        """).strip()
    
        self.sections.append(info)
 
    def add_missing_summary(self):
        missing = self.df.isna().sum()
        section = "\nMISSING VALUES\n--------------\n"
        section += missing.to_string()
        self.sections.append(section)
 
    def add_descriptive_stats(self):
        desc = self.df.describe().to_string()
        section = "\nDESCRIPTIVE STATS\n-----------------\n" + desc
        self.sections.append(section)
 
    def add_correlation(self):
        corr = self.df.corr(numeric_only=True)
        section = "\nCORRELATION MATRIX\n------------------\n" + corr.to_string()
        self.sections.append(section)
 
    def add_custom(self, text: str):
        self.sections.append(text)
 
    def build(self) -> str:
        return "\n\n".join(self.sections)