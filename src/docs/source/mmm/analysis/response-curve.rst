.. _mmm.analysis.response_curve:

📁 analysis.response_curve
==========================

.. currentmodule:: mmm.analysis.response_curve

The :class:`ResponseCurveAnalyzer` module within the `analysis` submodule of the MMM package
provides tools for analyzing and visualizing response curves for marketing mix models (MMM).
It enables fitting S-curves to model features, generating response curves, and quantifying feature contributions.

Overview
--------

This module exposes a response curve analyzer class that:

- Accepts a DataFrame and configuration parameters
- Fits S-curves to features using customizable transformers and models
- Generates response curves for features, including predicted targets and contributions
- Provides utilities for feature contribution analysis and reporting

Class Reference
---------------

.. py:class:: ResponseCurveParams(model=None, feature_columns=None, target_column=None, transformers=None, curve_type="exponential", add_default_transformers=True)

  Configuration parameters for response curve analysis.

  :param model: The model to use for fitting (must implement ModelProtocol).
  :type model: ModelProtocol or None
  :param feature_columns: List of feature column names to analyze.
  :type feature_columns: list[str]
  :param target_column: Name of the target column.
  :type target_column: str
  :param transformers: Dictionary mapping feature names to transformer pipelines.
  :type transformers: dict[str, TransformerPipeline] or None
  :param curve_type: Type of S-curve to fit (e.g., "exponential").
  :type curve_type: str
  :param add_default_transformers: Whether to add default transformers if not provided.
  :type add_default_transformers: bool

.. py:class:: ResponseCurveAnalyzer(df, params)

  Analyzes response curves for features in a DataFrame.

  :param df: Input data as a pandas DataFrame.
  :type df: pandas.DataFrame
  :param params: Configuration parameters for analysis.
  :type params: ResponseCurveParams

  .. py:method:: fit(num_points=100, generate_curves=True, clip_negative_target=True, return_raw_target=True, return_uplift=False)

    Fits S-curves for each feature and optionally generates curve data.

    :param num_points: Number of points in the response curve grid.
    :type num_points: int
    :param generate_curves: Whether to generate curve data after fitting.
    :type generate_curves: bool
    :param clip_negative_target: If True, negative predictions are floored at 0.
    :type clip_negative_target: bool
    :param return_raw_target: If True, includes raw predicted targets in output.
    :type return_raw_target: bool
    :param return_uplift: If True, includes uplift vs. baseline in output.
    :type return_uplift: bool
    :returns: Dictionary of curves (if generate_curves=True) or self.

  .. py:method:: generate_curve(feature, num_points=50, clip_negative_target=True, return_raw_target=True, return_uplift=False)

    Generates a response curve for a specific feature.

    :param feature: Feature name to generate the curve for.
    :type feature: str
    :param num_points: Number of points in the curve grid.
    :type num_points: int
    :param clip_negative_target: If True, negative predictions are floored at 0.
    :type clip_negative_target: bool
    :param return_raw_target: If True, includes raw predicted targets in output.
    :type return_raw_target: bool
    :param return_uplift: If True, includes uplift vs. baseline in output.
    :type return_uplift: bool
    :returns: Dictionary containing curve data.

  .. py:method:: feature_contribution(feature)

    Computes the contribution of a feature by comparing predictions with and without the feature.

    :param feature: Feature name.
    :type feature: str
    :returns: Numpy array of contributions.

  .. py:method:: total_contribution(feature)

    Computes the total contribution of a feature.

    :param feature: Feature name.
    :type feature: str
    :returns: Total contribution as a float.

  .. py:method:: average_contribution(feature)

    Computes the average contribution of a feature.

    :param feature: Feature name.
    :type feature: str
    :returns: Average contribution as a float.

  .. py:method:: print_curve(curve)

    Prints the response curve as a formatted table.

    :param curve: Curve dictionary as returned by generate_curve.
    :type curve: dict

  .. py:method:: print_curve_json(curve, indent=2)

    Prints the response curve as formatted JSON.

    :param curve: Curve dictionary as returned by generate_curve.
    :type curve: dict
    :param indent: Indentation level for JSON output.
    :type indent: int

**Curve Output Example**

.. code-block:: javascript

  {
    "feature": "tv_spend",
    "input_value": [0.0, 10.0, ..., 100.0],
    "observed_input_min": 0.0,
    "observed_input_max": 100.0,
    "predicted_target": [100.0, 110.0, ..., 200.0],
    "contribution": {
      "contribution": [0.0, 5.0, ..., 50.0],
      "total_contribution": 500.0,
      "average_contribution": 25.0
    },
    "predicted_target_raw": [100.0, 110.0, ..., 200.0],
    "predicted_target_clipped": [100.0, 110.0, ..., 200.0],
    "predicted_target_uplift": [0.0, 10.0, ..., 100.0]
  }

Notes
-----

- The analyzer supports custom transformer pipelines for each feature.
- S-curve fitting is robust to missing or infinite values, with warnings for dropped rows.
- Negative predictions can be clipped to zero for interpretability.
- Feature contributions are computed by comparing model predictions with and without the feature.
- Designed for use with MMM models to visualize and interpret feature effects.

References
----------

- :ref:`MMM Overview <mmm.overview>`

:ref:`Back to Home <home>`