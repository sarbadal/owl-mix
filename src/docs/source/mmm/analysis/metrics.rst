.. _mmm.analysis.metrics:

📁 analysis.metrics
===================

The :class:`ResponseMetrics` module within the analysis submodule of the MMM package
provides utility methods for computing key response-curve performance metrics.
It helps summarize spend efficiency, marginal return behavior, and investment status
from a curve object produced by MMM analysis.

Overview
--------

The module exposes a metrics class that:

- Reads spend, prediction, and contribution arrays from a response-curve dictionary
- Computes ROI and marginal ROI indicators
- Identifies saturation behavior using configurable thresholds
- Produces a consolidated summary dictionary for downstream reporting

Class Reference
---------------

.. py:class:: ResponseMetrics(curve)

   Utility class for response curve metrics.

   Expected Curve Structure (minimum keys)

   - curve["input_value"]: sequence of spend values (x-axis)
   - curve["predicted_target"]: sequence of predicted response values (y-axis)
   - curve["contribution"]["contribution"]: sequence of contribution value

   .. py:method:: current_spend()

      Returns the latest/current spend level.

      Logic:
      - Uses observed_input_max when present.
      - Falls back to the last value in input_value.

      :returns: Current spend.
      :rtype: ``float``

   .. py:method:: average_spend(window=None)

      Computes the average spend over a specified window.

      Logic:
      - If window is None, averages all input values.
      - Otherwise, averages the last 'window' number of input values.

      :param window: Number of recent values to average (optional).
      :type window: ``int`` or ``None``
      :returns: Average spend.
      :rtype: ``float``

   .. py:method:: roi()

      Computes the Return on Investment (ROI) as the ratio of predicted target to input spend.

      Logic:
      - Uses the latest predicted_target and input_value for calculation.

      :returns: ROI value.
      :rtype: ``float``

   .. py:method:: marginal_roi()

      Computes the Marginal Return on Investment (mROI) as the ratio of the change in predicted target to the change in input spend.

      Logic:
      - Uses the difference between the latest and previous predicted_target and input_value for calculation.

      :returns: Marginal ROI value.
      :rtype: ``float``

   .. py:method:: current_marginal_roi()

        Computes the current Marginal ROI based on the latest two points.
    
        Logic:
        - Similar to marginal_roi but specifically focuses on the most recent change.
    
        :returns: Current Marginal ROI value.
        :rtype: ``float``

   .. py:method:: peak_marginal_roi()

        Computes the peak Marginal ROI across all points.
    
        Logic:
        - Iterates through all points to find the maximum marginal ROI value.
    
        :returns: Peak Marginal ROI value.
        :rtype: ``float``

   .. py:method:: saturation_point(threshold_ratio=0.2)

        Identifies the saturation point where the marginal ROI falls below a specified threshold ratio of the peak marginal ROI.

        Logic:
        - Computes the peak marginal ROI.
        - Iterates through the marginal ROI values to find the point where it drops below the threshold ratio of the peak.

        :param threshold_ratio: Ratio of peak marginal ROI to define saturation (default is 0.2).
        :type threshold_ratio: ``float``
        :returns: Saturation point spend value or None if not found.
        :rtype: ``float`` or ``None``

   .. py:method:: efficiency_ratio()
    
        Computes the efficiency ratio as the ratio of current ROI to peak marginal ROI.

        Logic:
        - Uses the current ROI and peak marginal ROI for calculation.

        :returns: Efficiency ratio value.
        :rtype: ``float``

   .. py:method:: classify_status(high_threshold=0.7, low_threshold=0.3)

        Classifies the current investment status based on the efficiency ratio.

        Logic:
        - Computes the efficiency ratio.
        - Classifies as "Over-invested" if above high_threshold, "Under-invested" if below low_threshold, and "Optimal" otherwise.

        :param high_threshold: Efficiency ratio threshold for over-investment classification (default is 0.7).
        :type high_threshold: ``float``
        :param low_threshold: Efficiency ratio threshold for under-investment classification (default is 0.3).
        :type low_threshold: ``float``
        :returns: Investment status classification ("Over-invested", "Under-invested", or "Optimal").
        :rtype: ``str``

   .. py:method:: summary()
    
        Returns a compact dictionary of key metrics.

        Included fields:

        - current_spend
        - average_spend
        - roi
        - current_marginal_roi
        - peak_marginal_roi
        - saturation_point
        - efficiency_ratio
        - status

        :returns: Aggregated response-curve metrics.
        :rtype: ``Dict``

Result Example
--------------

.. code-block:: json

  {
    "current_spend": 150.0,
    "average_spend": 125.0,
    "roi": 1.5,
    "current_marginal_roi": 0.8,
    "peak_marginal_roi": 1.2,
    "saturation_point": 200.0,
    "efficiency_ratio": 0.67,
    "status": "Optimal"
  }

Notes
-----

- The class expects curve arrays to be numerically valid and aligned in length.
- marginal_roi is numerically estimated, so spacing and shape of input_value affects gradient stability.
- Classification thresholds are configurable and should be calibrated to your business context.
- saturation_point is sensitivity-based and depends on the chosen threshold_ratio.

References
----------
- :ref:`MMM Overview <mmm.overview>`

:ref:`Back to Home <home>`