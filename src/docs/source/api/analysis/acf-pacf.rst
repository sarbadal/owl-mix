.. _acf-pacf:

ACF and PACF Module - Analysis
==============================

.. currentmodule:: owlmix.analysis.acf_pacf

Autocorrelation and partial autocorrelation are essential tools in time series analysis, helping to identify patterns, 
seasonality, and the appropriate lag structure for modeling.

The ``AcfPacfAnalyzer`` class provides an easy interface to compute the Autocorrelation Function (ACF) 
and Partial Autocorrelation Function (PACF) for specified columns in a pandas DataFrame. 
It leverages the `statsmodels` library for time series analysis and supports configurable lag and precision settings.

It is particularly useful in identifying lag relationships and temporal dependencies in MMM (Market Mix Modeling) datasets.

Overview
--------

The module exposes a calculator class that:
 
- Accepts a pandas DataFrame
- Computes ACF and PACF values for selected columns
- Supports configurable lag values
- Returns structured output for downstream analysis or visualization


Class Reference
---------------

.. toggle:: click to expand

  .. autoclass:: owlmix.analysis.acf_pacf.AcfPacfParams
     :members:
     :show-inheritance:

     Dataclass for specifying ACF/PACF analysis parameters.

     :param columns: List of column names to include in the analysis. If None, all numeric columns are used.
     :type columns: Optional[List[str]]
     :param n_lags: Number of lag values to compute for ACF and PACF.
     :type n_lags: int
     :param precision: Number of decimal places to round ACF and PACF values.
     :type precision: int

  .. autoclass:: owlmix.analysis.acf_pacf.AcfPacfAnalyzer(df, params)
     :members:
     :show-inheritance:
 
     Calculates the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)
     for specified columns in a pandas DataFrame.
 
     :param df: Input DataFrame containing time series data.
     :type df: pandas.DataFrame
     :param params: Configuration parameters for ACF/PACF analysis.
     :type params: AcfPacfParams

**Example:**

.. code-block:: python

  import pandas as pd
  from owlmix.analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams

  # Example DataFrame
  df = pd.DataFrame({
      "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      "col2": [2, 3, 2, 5, 7, 8, 6, 5, 4, 3]
  })

  acf_pacf_params = AcfPacfParams(columns=["col1", "col2"], n_lags=5, precision=2)

  analyzer = AcfPacfAnalyzer(df=df, params=acf_pacf_params)
  result = analyzer.generate()
  print(result)

Methods
-------

.. py:method:: generate()

   Calculates ACF and PACF for each specified column.

   :returns: A dictionary with a "data" key containing a list of results for each column.
   :rtype: dict[str, list[dict]]

   Each result dictionary contains:
     - ``column``: Name of the column analyzed.
     - ``n_obs``: Number of non-null observations.
     - ``lags``: List of lag indices.
     - ``acf``: List of ACF values (rounded to specified precision).
     - ``pacf``: List of PACF values (rounded to specified precision).

Usage Example
-------------
 
Below is a simple example of how to use the calculator:
 
.. code-block:: python
 
    import numpy as np
    import pandas as pd
    from owlmix.analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams

    # Sample data
    num_rows = 100 
    df = pd.DataFrame({
        "sales": np.random.randint(90, 200, size=num_rows).tolist(),
        "spend": np.random.randint(8, 25, size=num_rows).tolist(),
        "impressions": np.random.randint(900, 1500, size=num_rows).tolist(),
        "tv_grp": np.round(np.random.uniform(4, 10, size=num_rows), 1).tolist()
    })

    # Initialize calculator
    acf_pacf_params = AcfPacfParams(columns=["sales", "spend", "impressions", "tv_grp"], n_lags=3, precision=2)
    analyzer = AcfPacfAnalyzer(df=df, params=acf_pacf_params)

    # Generate ACF & PACF values
    result = analyzer.compute()

    print("Print the result in formatted JSON")
    analyzer.print_results_json(results=result)

    print("Print the ACF/PACF analysis result in a tabular format")
    analyzer.print_results(results=result)

**Result in tabular format**

Column: sales (n_obs=100)

.. list-table:: ACF and PACF for sales
    :header-rows: 1
    :widths: 10 15 15

    * - Lag
      - ACF
      - PACF
    * - 0
      - 1.0
      - 1.0
    * - 1
      - 0.04
      - 0.04
    * - 2
      - -0.0
      - -0.0
    * - 3
      - -0.09
      - -0.09
    * - 4
      - 0.15
      - 0.16
    * - 5
      - 0.12
      - 0.11

Column: spend (n_obs=100)

.. list-table:: ACF and PACF for spend
    :header-rows: 1
    :widths: 10 15 15

    * - Lag
      - ACF
      - PACF
    * - 0
      - 1.0
      - 1.0
    * - 1
      - -0.14
      - -0.14
    * - 2
      - -0.14
      - -0.17
    * - 3
      - 0.03
      - -0.02
    * - 4
      - 0.11
      - 0.09
    * - 5
      - -0.19
      - -0.17

Column: impressions (n_obs=100)

.. list-table:: ACF and PACF for impressions
     :header-rows: 1
     :widths: 10 15 15

     * - Lag
       - ACF
       - PACF
     * - 0
       - 1.0
       - 1.0
     * - 1
       - 0.03
       - 0.03
     * - 2
       - -0.06
       - -0.06
     * - 3
       - -0.16
       - -0.17
     * - 4
       - -0.16
       - -0.17
     * - 5
       - 0.06
       - 0.05

Column: tv_grp (n_obs=100)

.. list-table:: ACF and PACF for tv_grp
    :header-rows: 1
    :widths: 10 15 15

    * - Lag
      - ACF
      - PACF
    * - 0
      - 1.0
      - 1.0
    * - 1
      - 0.1
      - 0.1
    * - 2
      - -0.01
      - -0.02
    * - 3
      - 0.01
      - 0.01
    * - 4
      - -0.0
      - -0.0
    * - 5
      - 0.04
      - 0.04   

**Result in formatted JSON**

.. code-block:: json

    [
        {
            "column": "sales",
            "n_obs": 100,
            "lags": [0, 1, 2, 3],
            "acf": [1.0, 0.02, 0.08, 0.18],
            "pacf": [1.0, 0.02, 0.09, 0.19]
        },
        {
            "column": "spend",
            "n_obs": 100,
            "lags": [0, 1, 2, 3],
            "acf": [1.0, -0.22, -0.03, -0.05],
            "pacf": [1.0, -0.22, -0.09, -0.08]
        },
        {
            "column": "impressions",
            "n_obs": 100,
            "lags": [0, 1, 2, 3],
            "acf": [1.0, -0.05, 0.02, -0.17],
            "pacf": [1.0, -0.05, 0.02, -0.17]
        },
        {
            "column": "tv_grp",
            "n_obs": 100,
            "lags": [0, 1, 2, 3],
            "acf": [1.0, -0.13, -0.02, 0.04],
            "pacf": [1.0, -0.13, -0.04, 0.03]
        }
    ]

Notes
-----

- Only numeric columns are processed; non-numeric columns are skipped.
- Missing values are automatically dropped before computation.
- The class inherits from ``ColumnMixin`` for flexible column selection.

Dependencies
------------

- pandas
- numpy
- statsmodels

See Also
--------

- `statsmodels documentation <https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.acf.html>`_
- `Partial Autocorrelation <https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html>`_