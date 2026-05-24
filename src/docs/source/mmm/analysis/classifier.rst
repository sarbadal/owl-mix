.. _mmm.analysis.classifier:

Classifier Analysis
===================

.. currentmodule:: mmm.analysis.classifier

The :class:`ResponseCurveClassifier` module within the `analysis` submodule of the MMM package 
provides tools for classifying model results based on predefined criteria. 
This can be useful for categorizing model performance, identifying key drivers, 
or segmenting results for further analysis.

Overview
--------

The module exposes a classifier class that:

- Accepts model results and classification parameters
- Applies classification rules to categorize results
- Returns structured output for downstream analysis or reporting

Class Reference
---------------

.. py:class:: ResponseCurveClassifier(curve, low_ratio=0.3, high_ratio=0.7)

  Classifies model results based on specified criteria.

  :param curve: Configuration parameters for classification.
  :type curve: `Dict`
  :param low_ratio: Threshold for classifying results as "underspend". Default is 0.3.
  :type low_ratio: ``float``
  :param high_ratio: Threshold for classifying results as "saturated". Default is 0.7.
  :type high_ratio: ``float``

  .. py:method:: classify()

    Applies classification rules to the provided model results.

    :returns: A dictionary containing classified results.
    :rtype: ``Dict``

**Result Example**

.. code-block:: javascript

  {
    "zones": [
      "underspend", "underspend", ..., 
      "optimal", "optimal", ..., 
      "saturated", "saturated", ...
    ],
    "marginal": [0.2, 0.4, ..., 0.5, 0.6, ..., 0.3, 0.1],
    "thresholds": {
      "low": 0.3,
      "high": 0.7
    }
  }

Notes
-----
- The classification logic is based on predefined thresholds for marginal returns, which can be customized as needed.
- This module is designed to work with the output of MMM models, providing insights into the effectiveness of different marketing channels or tactics.
- The results can be used to inform budget allocation decisions, optimize marketing strategies, or identify areas for improvement in the model.

References
----------
- :ref:`MMM Overview <mmm.overview>`
- :ref:`MMM Analysis Overview <mmm.analysis.overview>`
- :ref:`MMM Configuration Overview <mmm.config.overview>`

:ref:`Back to Home <home>`
