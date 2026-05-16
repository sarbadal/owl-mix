.. _api.analysis.vif:

➡️ analysis.vif
===============

.. currentmodule:: owlmix.analysis.vif

Variance Inflation Factor (VIF) is a key diagnostic tool in regression analysis, used to detect 
multicollinearity among explanatory variables. High VIF values indicate that a feature is highly 
collinear with other features, which can adversely affect model interpretability and stability.

The :class:`VIFAnalyzer` class provides a convenient interface to compute VIF values for selected columns 
in a pandas DataFrame. It supports configurable precision and optional color-coding for visualization, 
making it easy to identify problematic features.

Overview
--------

The module exposes:

- A parameter dataclass for flexible configuration
- An analyzer class that:

  - Accepts a pandas DataFrame
  - Computes VIF values for selected features (excluding the target column)
  - Supports configurable precision and color thresholds
  - Returns structured output for downstream analysis or visualization

Class Reference
---------------

.. py:class:: VIFParams

    Dataclass for specifying VIF analysis parameters.

    :param target_column: The name of the target column to exclude from VIF calculation.
    :type target_column: str
    :param features: List of feature column names to include in the analysis. If None, all numeric columns are used.
    :type features: Optional[List[str]]
    :param precision: Number of decimal places to round VIF values.
    :type precision: int
    :param color_thresholds: List of (threshold, color) tuples for color-coding VIF values. If None, no color-coding is applied.
    :type color_thresholds: Optional[List[Tuple[float, str]]]

.. py:class:: VIFAnalyzer(df, params)

    Calculates the Variance Inflation Factor (VIF) for specified features in a pandas DataFrame.

    :param df: Input DataFrame containing the data.
    :type df: pandas.DataFrame
    :param params: Configuration parameters for VIF analysis.
    :type params: VIFParams

    .. py:method:: compute()

        Calculates VIF values for each specified feature.

        :returns: A dictionary with keys:
            - ``feature``: List of feature names analyzed.
            - ``vif``: List of VIF values (rounded to specified precision).
            - ``color``: List of color codes for each VIF value (if color_thresholds provided).
        :rtype: ``dict[str, list]``

    .. py:method:: add_colors(vif_values)

        Assigns colors to VIF values based on the defined color thresholds.

        :param vif_values: List of VIF values.
        :type vif_values: ``List[float]``
        :returns: List of color strings corresponding to each VIF value.
        :rtype: ``List[str]``

    .. py:method:: print_results_json(results=None, indent=2)

        Prints the results in JSON format.

        :param results: The results to print. If None, uses the computed results.
        :type results: ``list[dict], optional``
        :param indent: Indentation level for pretty-printing the JSON.
        :type indent: ``int``

    .. py:method:: print_results(results=None)

        Prints the results in a human-readable tabular format.

        :param results: The results to print. If None, uses the computed results.
        :type results: ``list[dict], optional``


Usage Example
-------------

Below is a simple example of how to use the analyzer:

.. code-block:: python

    import pandas as pd
    from owlmix.analysis.vif import VIFAnalyzer, VIFParams

    df = pd.DataFrame({
        "y": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "x1": [2, 3, 2, 5, 7, 8, 6, 5, 4, 3],
        "x2": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        "x3": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    })

    vif_params = VIFParams(
        target_column="y",
        features=["x1", "x2", "x3"],
        precision=2,
        color_thresholds=[(5, "orange"), (10, "red")]
    )
    analyzer = VIFAnalyzer(df=df, params=vif_params)
    result = analyzer.compute()
    print(result)

**Result Example**

.. code-block:: json

    {
        "feature": ["x1", "x2", "x3"],
        "vif": [1.23, 8.45, 4.56],
        "color": ["orange", "red", "orange"]
    }

Notes
-----

- The target column is always excluded from VIF calculation.
- If fewer than two features are provided, VIF is not defined and NaN is returned.
- Only numeric columns are processed; non-numeric columns are ignored.
- Missing values are automatically dropped before computation.
- Color-coding is optional and controlled via the ``color_thresholds`` parameter.

Dependencies
------------

- pandas
- numpy
- statsmodels

See Also
--------

- `statsmodels documentation <https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html>`_
- `Variance Inflation Factor (Wikipedia) <https://en.wikipedia.org/wiki/Variance_inflation_factor>`_

:ref:`Back to Home <home>`