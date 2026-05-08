.. _vif:


Variance Inflation Factor (VIF)
===============================


Methodology
-----------

The Variance Inflation Factor (VIF) is a diagnostic metric used to detect **multicollinearity** in a multiple linear regression model. It measures how much the variance of an estimated regression coefficient is increased due to collinearity with other predictor variables.

Conceptual Formula
^^^^^^^^^^^^^^^^^^

For a specific independent variable :math:`X_j`, the VIF is calculated as:

.. math::

   VIF_j = \frac{1}{1 - R_j^2}

Where:
*  :math:`VIF_j` is the factor for the :math:`j`-th predictor.
*  :math:`R_j^2` is the coefficient of determination obtained by regressing :math:`X_j` against all other independent variables in the model.

Calculation Steps
^^^^^^^^^^^^^^^^^

To compute the VIF for a dataset with :math:`k` independent variables, follow these steps:

1. Select a Predictor
^^^^^^^^^^^^^^^^^^^^^
Choose one independent variable (:math:`X_j`) to be the "dependent" variable for the diagnostic test.

2. Run an Auxiliary Regression
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Perform a linear regression where :math:`X_j` is predicted by all other remaining independent variables (:math:`X_1, X_2, ..., X_{j-1}, X_{j+1}, ..., X_k`).

   *Example:* If your model is :math:`Y \sim X_1 + X_2 + X_3`, to find the VIF for :math:`X_1`, run the regression:
   :math:`X_1 = \alpha + \beta_2 X_2 + \beta_3 X_3 + \epsilon`

3. Extract the R-squared
^^^^^^^^^^^^^^^^^^^^^^^^
Calculate the :math:`R^2` value (the proportion of variance in :math:`X_j` explained by the other predictors) from the auxiliary regression performed in Step 2.

4. Calculate the VIF
^^^^^^^^^^^^^^^^^^^^
Apply the VIF formula:
:math:`VIF = 1 / (1 - R^2)`.

5. Repeat
^^^^^^^^^
Repeat steps 1 through 4 for every independent variable in the original model.

Interpretation of Results
^^^^^^^^^^^^^^^^^^^^^^^^^

*  **VIF = 1:** No correlation between the :math:`j`-th predictor and the remaining variables.
*  **1 < VIF < 5:** Moderate correlation; generally considered acceptable in most social science contexts.
*  **VIF > 5 or 10:** High multicollinearity. The coefficients are poorly estimated, and the p-values may be unreliable.

Implementation Example (Python)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Python, the `statsmodels` library is the standard tool for this calculation:

.. code-block:: python

   from statsmodels.stats.outliers_influence import variance_inflation_factor
   import pandas as pd

   # Assuming 'df' contains only your independent variables
   vif_data = pd.DataFrame()
   vif_data["feature"] = df.columns
   vif_data["VIF"] = [variance_inflation_factor(df.values, i) 
                      for i in range(len(df.columns))]

   print(vif_data)

.. note::
   The VIF calculation assumes that the independent variables are linearly related and that the model is correctly specified. It does not account for non-linear relationships or interactions between variables.


Calculator Module
-----------------

.. currentmodule:: owlmix.eda.vif

**Overview**

The ``VIFCalculator`` class computes the Variance Inflation Factor (VIF) for features in a pandas DataFrame. This is useful for detecting multicollinearity in regression analysis by quantifying how much the variance of a regression coefficient is inflated due to collinearity with other predictors.

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

   df = pd.DataFrame({
       "x1": [1, 2, 3],
       "x2": [2, 4, 6],
       "y": [3, 6, 9]
   })

   vif_calc = VIFCalculator(df, target_column="y", features=["x1", "x2"], precision=2)
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

Dependencies
------------

- pandas
- numpy
- statsmodels

See Also
--------

- :class:`owlmix.eda.utils.ColumnMixin`
- :class:`owlmix.eda.args.vif.SetVIFConfigArgs`