.. _section.vif:

Section VIF
===========

This module provides the implementation for building the VIF (Variance Inflation Factor) section in a report. It integrates with the report builder framework and utilizes registered analyzers and plotters to compute and visualize VIF for specified features in a DataFrame.

.. automodule:: owlmix.reporting.sections.vif
    :members:
    :undoc-members:
    :show-inheritance:

Functions
---------

.. py:function:: build_vif_section(report_builder)
    :no-index:

    Builds the VIF section for the report.

    This function retrieves configuration for VIF analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the VIF data, generates the corresponding plot, and returns a dictionary
    containing both the computed data and chart metadata (including a base64-encoded image).

    :param report_builder: The report builder instance containing the dataframe and configuration.
    :type report_builder: ReportBuilderProtocol

    :returns: A dictionary with keys:
        - ``data``: The computed VIF results.
        - ``chart``: Metadata and image for the generated plot, including:
        - ``title``: Title of the chart.
        - ``description``: Description of the chart.
        - ``alt_text``: Alternative text for the image.
        - ``image``: Base64-encoded image of the plot.
    :rtype: dict

    **Workflow:**

    1. Retrieves the VIF configuration from the report builder.
    2. Fetches the analyzer and plotter classes and their parameter classes from the registries.
    3. Initializes analyzer and plotter parameter objects using the configuration.
    4. Instantiates the analyzer with the DataFrame and parameters, then computes the VIF data.
    5. Instantiates the plotter with the computed data and plot parameters, then generates the plot.
    6. Converts the plot image to a base64 string for embedding in the report.
    7. Returns a dictionary containing both the computed data and chart metadata.

    **Example Usage:**

    .. code-block:: python

        section = build_vif_section(report_builder)
        data = section["data"]
        chart = section["chart"]

Dependencies
------------

- ``os``: For file path operations.
- ``register_section``, ``ANALYZERS_REGISTRY``, ``PLOTTERS_REGISTRY``: For section registration and dynamic class retrieval.
- ``ReportBuilderProtocol``: Protocol for the report builder object.

Registries
----------

- ``ANALYZERS_REGISTRY["vif"]``: Provides the analyzer class and its parameter class for VIF.
- ``PLOTTERS_REGISTRY["vif"]``: Provides the plotter class and its parameter class for VIF.

Section Registration
--------------------

The function is registered as a report section under the name ``"vif"`` using the ``@register_section`` decorator.

.. code-block:: python

    @register_section("vif")
    def build_vif_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
        ...

See Also
--------

- :mod:`owlmix.registry.registry`
- :mod:`owlmix.reporting.sections.protocol_cls`
- :mod:`owlmix.eda.vif`
- :mod:`owlmix.plotting.vif`