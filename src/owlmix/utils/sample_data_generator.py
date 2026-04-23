"""
Sample data generator for MMM testing and demonstrations.

This module provides utilities to generate realistic sample datasets
for Marketing Mix Modeling use cases.
"""

import pandas as pd
import numpy as np
from owlmix.utils.distribution_data_generator import CategoryDistributionGenerator


# Sample data categories
COLORS = [
    "#1f77b4",  # muted blue
    "#ff7f0e",  # safety orange
    "#2ca02c",  # cooked asparagus green
    "#d62728",  # brick red
    "#9467bd",  # muted purple
    "#8c564b",  # chestnut brown
    "#e377c2",  # raspberry yogurt pink
    "#7f7f7f",  # middle gray
    "#bcbd22",  # curry yellow-green
    "#17becf",  # blue-teal
    "#aec7e8",  # light blue
    "#ffbb78",  # light orange
    "#98df8a",  # light green
    "#ff9896",  # light red
    "#c5b0d5",  # light purple
    "#c49c94",  # light brown
    "#f7b6d2",  # light pink
    "#c7c7c7",  # light gray
    "#dbdb8d",  # light yellow-green
    "#9edae5",  # light blue-teal
]

SMARTPHONES = [
    "Apple iPhone 17 Pro",
    "Apple iPhone 16 Plus",
    "Samsung Galaxy S25 Ultra",
    "Samsung Galaxy S25 FE",
    "Samsung Galaxy Z Fold7",
    "Google Pixel 10 Pro XL",
    "OnePlus 15 5G",
    "OnePlus 13",
    "Xiaomi 17 Ultra",
    "Xiaomi Redmi Note 15",
    "Vivo X300 Pro",
    "Nothing Phone (3a) Lite",
    "Motorola Edge 70 Fusion",
    "Realme GT 8 Pro",
    "iQOO 15 Apex"
]

CAR_MODELS = [
    "Toyota Corolla",
    "Honda Civic",
    "Ford F-150",
    "Tesla Model 3",
    "BMW M4",
    "Mercedes-Benz C-Class",
    "Porsche 911",
    "Hyundai Tucson",
    "Kia Sportage",
    "Volkswagen Golf",
    "Audi Q5",
    "Chevrolet Silverado",
    "Mazda CX-5",
    "Subaru Outback",
    "Land Rover Defender"
]

POPULAR_LANGUAGES = [
    "Python",
    "JavaScript",
    "Java",
    "C#",
    "C++",
    "TypeScript",
    "PHP",
    "Go",
    "Rust",
    "Swift",
    "SQL",
    "Kotlin",
    "Ruby",
    "R",
    "Dart",
    "Scala",
    "Shell",
    "Objective-C",
    "Perl",
    "Haskell",
    "Lua",
    "Elixir",
    "MATLAB",
    "Solidity",
    "Julia",
    "Clojure",
    "Groovy",
    "F#",
    "Erlang",
    "Fortran",
    "Cobol",
    "VHDL"
]


def create_sample_data(
    n: int = 100,
    start_date: str = "2021-01-01",
    include_nan: bool = True,
    seed: int = None
) -> pd.DataFrame:
    """
    Create a sample Marketing Mix Modeling (MMM) dataset.
    
    This function generates synthetic data with marketing spend variables,
    impressions, categorical features, and a target sales variable with
    realistic relationships.
    
    Parameters
    ----------
    n : int, default=100
        Number of daily observations to generate.
    start_date : str, default="2021-01-01"
        Starting date for the time series in YYYY-MM-DD format.
    include_nan : bool, default=True
        Whether to introduce missing values in the data.
    seed : int, optional
        Random seed for reproducibility. If provided, ensures consistent
        data generation across runs.
    
    Returns
    -------
    pd.DataFrame
        A DataFrame with MMM sample data containing:
        
        - time: Date column (YYYY-MM-DD format)
        - tv_spend: TV advertising spend (100-500)
        - digital_spend: Digital advertising spend (50-300)
        - radio_spend: Radio advertising spend (20-150)
        - tv_grp: TV Gross Rating Points (10-100)
        - radio_grp: Radio GRPs (20-150)
        - digital_imp: Digital impressions (10-100)
        - radio_imp: Radio impressions (20-150)
        - inflation: Inflation index (10-100)
        - color: Random product color category
        - smartphone: Random smartphone model
        - car_model: Random car model
        - language: Random programming language
        - sales: Target variable (synthesized with marketing spend relationships)
    
    Examples
    --------
    >>> # Generate 500 days of sample data with consistent seed
    >>> df = create_sample_data(n=500, seed=42)
    >>> print(df.shape)
    (500, 14)
    
    >>> # Generate data without missing values
    >>> df = create_sample_data(n=100, include_nan=False)
    >>> print(df.isnull().sum().sum())
    0
    
    Notes
    -----
    - The sales variable is created with a linear combination of marketing spend
      variables plus random noise to simulate realistic MMM scenarios.
    - Missing values are randomly introduced in tv_spend and radio_spend columns
      to reflect real-world data quality issues.
    - Categorical columns use the CategoryDistributionGenerator to create
      realistic distribution patterns.
    """
    if seed is not None:
        np.random.seed(seed)
 
    # Generate date range
    dates = pd.date_range(start=start_date, periods=n, freq="D")
    
    # Generate categorical variables with realistic distributions
    colors_ = CategoryDistributionGenerator(COLORS).generate(n_samples=n, sigma=0.5)
    smartphones_ = CategoryDistributionGenerator(SMARTPHONES).generate(n_samples=n, sigma=0.5)
    car_models_ = CategoryDistributionGenerator(CAR_MODELS).generate(n_samples=n, sigma=0.5)
    languages_ = CategoryDistributionGenerator(POPULAR_LANGUAGES).generate(n_samples=n, sigma=0.5)
 
    # Create base dataframe
    df = pd.DataFrame({
        "time": dates,
        "tv_spend": np.random.randint(100, 500, size=n),
        "digital_spend": np.random.randint(50, 300, size=n),
        "radio_spend": np.random.randint(20, 150, size=n),
        "tv_grp": np.random.randint(10, 100, size=n),
        "radio_grp": np.random.randint(20, 150, size=n),
        "digital_imp": np.random.randint(10, 100, size=n),
        "radio_imp": np.random.randint(20, 150, size=n),
        "inflation": np.random.randint(10, 100, size=n),
        "color": colors_,
        "smartphone": smartphones_,
        "car_model": car_models_,
        "language": languages_,
    })

    # Format time column as string (YYYY-MM-DD)
    df['time'] = df['time'].dt.strftime("%Y-%m-%d")
 
    # Create synthetic sales with realistic relationships to marketing spend
    # Coefficients represent relative impact of each variable
    df["sales"] = (
        0.3 * df["tv_spend"]
        + 0.5 * df["digital_spend"]
        + 0.2 * df["radio_spend"]
        + 0.2 * df["tv_grp"]
        + 0.2 * df["radio_grp"]
        + 0.2 * df["digital_imp"]
        + np.random.normal(0, 20, size=n)
    )
 
    # Add realistic missing values
    if include_nan:
        df.loc[5:10, "tv_spend"] = np.nan
        df.loc[20:25, "radio_spend"] = np.nan
 
    return df


# Convenience aliases for direct access to category data
def get_colors() -> list[str]:
    """Get the list of color hex codes."""
    return COLORS.copy()


def get_smartphones() -> list[str]:
    """Get the list of smartphone models."""
    return SMARTPHONES.copy()


def get_car_models() -> list[str]:
    """Get the list of car models."""
    return CAR_MODELS.copy()


def get_languages() -> list[str]:
    """Get the list of programming languages."""
    return POPULAR_LANGUAGES.copy()
