.. _vif:

Variance Inflation Factor (VIF)
===============================

.. currentmodule:: owlmix.eda.vif

Variance Inflation Factor (VIF) is a diagnostic metric used to detect **multicollinearity** in multiple linear regression models. It quantifies how much the variance of a regression coefficient is inflated due to collinearity with other predictors. High VIF values indicate that a predictor has a strong linear relationship with other predictors, which can make model estimates unstable.

Overview
--------

The ``VIFCalculator`` class computes the Variance Inflation Factor for features in a pandas DataFrame. This is useful for detecting multicollinearity in regression analysis by quantifying how much the variance of a regression coefficient is inflated due to collinearity with other predictors.

Key features:

- Accepts a pandas DataFrame
- Computes VIF for selected features (optionally excluding a target column)
- Supports custom feature selection, precision, and color-coding
- Returns structured output for downstream analysis or visualization

Methodology
-----------

The VIF for a specific independent variable :math:`X_j` is calculated as:

.. math::

   VIF_j = \frac{1}{1 - R_j^2}

Where:
  - :math:`VIF_j` is the factor for the :math:`j`-th predictor.
  - :math:`R_j^2` is the coefficient of determination obtained by regressing :math:`X_j` against all other independent variables.

Calculation steps:

1. **Select a predictor** :math:`X_j` to be the "dependent" variable for the diagnostic test.
2. **Run an auxiliary regression:** regress :math:`X_j` on all other predictors.
3. **Extract the :math:`R^2` value** from this regression.
4. **Calculate the VIF** using the formula above.
5. **Repeat** for every independent variable.

Interpretation:

- **VIF = 1:** No correlation with other predictors.
- **1 < VIF < 5:** Moderate correlation; generally acceptable.
- **VIF > 5 or 10:** High multicollinearity; coefficients may be unreliable.

Class Reference
---------------

.. autoclass:: VIFCalculator
   :members:
   :undoc-members:
   :show-inheritance:

Initialization
--------------

.. py:class:: VIFCalculator(df, target_column=None, features=None, precision=3, color_thresholds=None)

   :param df: Input pandas DataFrame containing the features.
   :type df: pandas.DataFrame

   :param target_column: (Optional) The target column to exclude from VIF calculation.
   :type target_column: str, optional

   :param features: (Optional) List of features to include. If None, all columns except the target are used.
   :type features: list[str] or None

   :param precision: (Optional) Decimal precision for VIF values. Default is 3.
   :type precision: int, optional

   :param color_thresholds: (Optional) List of (threshold, color) tuples for coloring VIF values.
   :type color_thresholds: list[tuple[float, str]], optional

Usage Example
-------------

.. code-block:: python

   import pandas as pd
   from owlmix.eda.vif import VIFCalculator

   COLOR_RULES  = [(5, "green"), (10, "orange"), (float("inf"), "red")]

   df = pd.DataFrame({
       "x1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
       "x2": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
       "y": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
   })

   vif_calc = VIFCalculator(
      df, 
      target_column="y", 
      features=["x1", "x2"], 
      precision=2, 
      color_thresholds=COLOR_RULES
   )

   result = vif_calc.compute_vif()
   print(result)

Methods
-------

.. py:method:: compute_vif()

   Computes the VIF for the selected features.

   :returns: Dictionary with keys:
      - 'feature': list of feature names
      - 'vif_value': list of VIF values (float)
      - 'color': list of color strings (if color_thresholds provided, else 'black')
   :rtype: dict

   If the number of features is less than 2, returns NaN for VIF values.

.. py:method:: add_colors(vif_values)

   Assigns colors to VIF values based on specified thresholds.

   :param vif_values: List of VIF values.
   :type vif_values: list[float]
   :return: List of color strings corresponding to each VIF value.
   :rtype: list[str]

Details
-------

- **Feature Selection:** By default, all columns except the target are used. You can specify a subset via the `features` parameter.
- **Precision:** VIF values are rounded to the specified decimal precision.
- **Color Coding:** If `color_thresholds` are provided, VIF values are color-coded for easier interpretation.
- **Output:** The result is a dictionary suitable for further analysis or visualization.

Notes
-----

- Only numeric columns are processed; non-numeric columns are skipped.
- The VIF calculation assumes linear relationships between predictors.
- High VIF values indicate multicollinearity, but do not specify which variables are problematic.
- Always validate findings with domain knowledge and further statistical analysis.

Dependencies
------------

- pandas
- numpy
- statsmodels

See Also
--------

- :class:`owlmix.eda.utils.ColumnMixin`
- :class:`owlmix.eda.args.vif.SetVIFConfigArgs`
- `statsmodels documentation <https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html>`_