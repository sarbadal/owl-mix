.. _mmm.analysis.s_curve_fitter:

📁 analysis.s_curve_fitter
==========================

.. currentmodule:: mmm.analysis.s_curve_fitter

The :class:`SCurveFitter` module within the `analysis` submodule of the MMM package
provides tools for fitting S-curves to features in marketing mix models (MMM).
It enables flexible fitting of S-curves using customizable transformers and models.

Overview
--------

This module exposes an S-curve fitter class that:

- A reusable curve fitter class for spend-response style modeling
- Built-in support for exponential and logistic curve families
- Parameter estimation using scipy.optimize.curve_fit
- Prediction from fitted parameters
- Clear error handling for unsupported curve types and unfitted use

Class Reference
---------------

.. py:class:: SCurveFitter(curve_type="exponential", transformers=None)

  A class for fitting S-curves to features.

  :param curve_type: Type of S-curve to fit (e.g., "exponential", "logistic").
  :type curve_type: ``str``
   - Supported values: ``"exponential"``, ``"logistic"``
   - exponential: ``f(x) = a * (1 - exp(-b * x))``
   - logistic: ``f(x) = a / (1 + exp(-b * (x - c)))``
  :param transformers: Optional dictionary mapping feature names to transformer pipelines.
  :type transformers: ``dict[str, TransformerPipeline]`` or ``None``

  .. py:method:: fit(X, y)

    Fits the S-curve model to the provided data.

    :param X: Feature data as a pandas DataFrame.
    :type X: ``pandas.DataFrame``
    :param y: Target variable as a pandas Series or array-like.
    :type y: ``pandas.Series`` or array-like

  .. py:method:: predict(X)

    Predicts target values using the fitted S-curve model.

    :param X: Feature data as a pandas DataFrame.
    :type X: ``pandas.DataFrame``
    :returns: Predicted target values.
    :rtype: ``numpy.ndarray``

**Note** The `fit` method must be called before `predict`, and the specified `curve_type` must be supported.

Example Usage
-------------

.. code-block:: python

    from mmm.analysis.s_curve_fitter import SCurveFitter
    import pandas as pd

    # Sample data
    df = pd.DataFrame({
        'spend': [0, 10, 20, 30, 40],
        'response': [0, 5, 15, 25, 30]
    })

    # Initialize the S-curve fitter
    fitter = SCurveFitter(curve_type="exponential")

    # Fit the model
    fitter.fit(df[['spend']], df['response'])

    # Predict using the fitted model
    predictions = fitter.predict(df[['spend']])
    print(predictions)

Note
----

- The class is intentionally minimal and focused on curve fitting only.
- It is designed to be used by higher-level analyzers that handle feature orchestration and reporting.
- Additional curve families can be added by extending the registry inside fit.
- The quality and stability of fitting can depend on data quality and initial parameter guesses.

Common Errors
--------------

- **UnsupportedCurveTypeError**: Raised if an unsupported `curve_type` is specified.
- **NotFittedError**: Raised if `predict` is called before `fit`.

Extension Guidance
------------------

- To add new curve types, implement the mathematical function and add it to the registry in the `fit` method.
- Add a registry entry in fit with:

  - function reference
  - sensible initial parameter guess

- Ensure that the new curve type is properly documented and tested for stability.

References
----------

- :ref:`MMM Overview <mmm.overview>`

:ref:`Back to Home <home>`