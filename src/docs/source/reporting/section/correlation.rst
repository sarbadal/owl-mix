.. _section.correlation:

reporting.sections.correlation
==============================

This function provides the implementation for building the correlation analysis 
section in a report. It integrates with the report builder framework and utilizes 
registered analyzers and plotters to compute and visualize correlation matrices 
and lagged correlations for specified features in a DataFrame.

.. currentmodule:: owlmix.reporting.sections.correlation

Functions
---------

.. py:function:: build_correlation_section(report_builder)

    Builds the correlation analysis section for the report.

    This function retrieves configuration for correlation analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the correlation matrix and lagged correlations, generates the corresponding plots,
    and returns a dictionary containing both the computed data and chart metadata (including base64-encoded images).

    :param report_builder: The report builder instance containing the dataframe and configuration.
    :type report_builder: ReportBuilderProtocol

    :returns: A dictionary with keys:

        - ``data``: The computed correlation results.
        - ``chart``: Metadata and images for the generated plots, including:
        
            - ``title``: Title of the chart.
            - ``description``: Description of the chart.
            - ``alt_text``: Alternative text for the images.
            - ``images``: Dictionary with base64-encoded images for:
                - ``correlation_matrix``: Correlation matrix plot.
                - ``lagged_correlation_matrix``: Lagged correlation matrix plot.
    :rtype: ``dict``

**Workflow:**

1. Retrieves the correlation configuration from the report builder.
2. Fetches the analyzer and plotter classes and their parameter classes from the registries.
3. Initializes analyzer and plotter parameter objects using the configuration.
4. Instantiates the analyzer with the DataFrame and parameters, then computes the correlation data.
5. Instantiates the plotter with the computed data and plot parameters, then generates the plots.
6. Converts the plot images to base64 strings for embedding in the report.
7. Returns a dictionary containing both the computed data and chart metadata.

**Example Usage:**

.. code-block:: python

    section = build_correlation_section(report_builder)
    data = section["data"]
    chart = section["chart"]

Dependencies
------------

- ``os``: For file path operations.
- ``register_section``, ``ANALYZERS_REGISTRY``, ``PLOTTERS_REGISTRY``: For section registration and dynamic class retrieval.
- ``ReportBuilderProtocol``: Protocol for the report builder object.

Registries
----------

- ``ANALYZERS_REGISTRY["correlation"]``: Provides the analyzer class and its parameter class for correlation.
- ``PLOTTERS_REGISTRY["correlation"]``: Provides the plotter class and its parameter class for correlation.

Section Registration
--------------------

The function is registered as a report section under the name ``"correlation"`` using the ``@register_section`` decorator.

.. code-block:: python

    @register_section("correlation")
    def build_correlation_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
        ...

See Also
--------

- :mod:`owlmix.registry.registry`
- :mod:`owlmix.reporting.sections.protocol_cls`
- :mod:`owlmix.plotting.correlation`