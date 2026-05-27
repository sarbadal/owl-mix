.. _mmm.analysis.contribution:

📁 analysis.contribution
========================

.. currentmodule:: mmm.analysis.contribution

The :class:`ContributionAnalyzer` class within the `analysis` submodule of the MMM package
provides tools for analyzing the contribution of different marketing channels or tactics
to the overall model results. This is useful for understanding the impact of each
channel on the target metric and for optimizing marketing strategies.

Overview
--------

The module exposes a contribution analysis class that:

- Accepts model results and contribution parameters
- Computes the contribution of each channel to the overall results using a "zero-out" approach
- Provides methods for total, average, and per-row contributions
- Returns structured output for downstream analysis or reporting

Class Reference
---------------

.. py:class:: ContributionAnalyzer(df, model, feature_cols)

   Analyzes the contribution of different marketing channels or tactics to the overall model results.

   :param df: Input dataframe containing model results.
   :type df: ``pandas.DataFrame``
   :param model: Model object with a ``fit`` and ``predict`` method.
   :type model: ``Any``
   :param feature_cols: List of column names representing the features/channels to analyze.
   :type feature_cols: ``list[str]``

   .. py:method:: feature_contribution(df, feature)

      Computes the per-row contribution of a feature by zeroing it out and measuring the prediction difference.

      :param df: DataFrame to use for contribution calculation.
      :type df: ``pandas.DataFrame``
      :param feature: Feature/column name to analyze.
      :type feature: ``str``
      :returns: Numpy array of per-row contributions.
      :rtype: ``np.ndarray``

   .. py:method:: total_contribution(df, feature)

      Computes the total contribution of a feature across all rows.

      :param df: DataFrame to use for contribution calculation.
      :type df: ``pandas.DataFrame``
      :param feature: Feature/column name to analyze.
      :type feature: ``str``
      :returns: Total contribution as a float.
      :rtype: ``float``

   .. py:method:: average_contribution(df, feature)

      Computes the average contribution of a feature across all rows.

      :param df: DataFrame to use for contribution calculation.
      :type df: ``pandas.DataFrame``
      :param feature: Feature/column name to analyze.
      :type feature: ``str``
      :returns: Average contribution as a float.
      :rtype: ``float``

   .. py:method:: summary(df, feature)

      Returns a summary dictionary with per-row, total, and average contributions for a feature.

      :param df: DataFrame to use for contribution calculation.
      :type df: ``pandas.DataFrame``
      :param feature: Feature/column name to analyze.
      :type feature: ``str``
      :returns: Dictionary with keys ``contribution`` (list), ``total_contribution`` (float), and ``average_contribution`` (float).
      :rtype: ``dict``

Example Use Case
----------------

.. code-block:: python

   from mmm.analysis.contribution import ContributionAnalyzer
   import pandas as pd
   from sklearn.ensemble import RandomForestRegressor

   class Model:
        def fit(self, X, y):
            raise NotImplementedError

        def predict(self, X):
            raise NotImplementedError

   # Sample data and model setup
   df = pd.DataFrame({
       'channel_1': [100, 150, 200],
       'channel_2': [50, 75, 100],
       'target': [200, 300, 400]
   })
   X = df[['channel_1', 'channel_2']]
   y = df['target']
   model = RandomForestRegressor().fit(X, y)

   # Initialize the analyzer
   analyzer = ContributionAnalyzer(df=X, model=model, feature_cols=['channel_1', 'channel_2'])

   # Analyze contribution for channel_1
   contribution_summary = analyzer.summary(df=X, feature='channel_1')
   print(contribution_summary)

**Result Example**

.. code-block:: javascript

  {
    "contribution": [0.1, 0.2, ..., 0.05],
    "total_contribution": 15.0,
    "average_contribution": 0.15
  }

References
----------
- :ref:`MMM Overview <mmm.overview>`
- :ref:`MMM Analysis Overview <mmm.analysis.overview>`
- :ref:`MMM Configuration Overview <mmm.config.overview>`

:ref:`Back to Home <home>`