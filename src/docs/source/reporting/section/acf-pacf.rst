.. _section.acf-pacf:

reporting.sections.acf_pacf
===========================

.. currentmodule:: owlmix.reporting.sections.acf_pacf

This function provides the implementation for building the ACF (Autocorrelation Function) 
and PACF (Partial Autocorrelation Function) section in a report. It integrates with the 
report builder framework and utilizes registered analyzers and plotters to compute a
nd visualize ACF/PACF for specified columns in a DataFrame.


Functions
---------

.. py:function:: build_acf_pacf_section(report_builder)

    Builds the ACF and PACF section for the report.

    This function retrieves configuration for ACF/PACF analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the ACF/PACF data, generates the corresponding plots, and returns a dictionary
    containing both the computed data and chart metadata (including a base64-encoded image).

    :param report_builder: The report builder instance containing the dataframe and configuration.
    :type report_builder: ReportBuilderProtocol

    :returns: A dictionary with keys:

                - ``data``: The computed ACF/PACF results.
                - ``chart``: Metadata and image for the generated plot, including:

                    - ``title``: Title of the chart.
                    - ``description``: Description of the chart.
                    - ``alt_text``: Alternative text for the image.
                    - ``image``: Base64-encoded image of the plot.
    :rtype: ``dict``

**Workflow:**

1. Retrieves the ACF/PACF configuration from the report builder.
2. Fetches the analyzer and plotter classes and their parameter classes from the registries.
3. Initializes analyzer and plotter parameter objects using the configuration.
4. Instantiates the analyzer with the DataFrame and parameters, then computes the ACF/PACF data.
5. Instantiates the plotter with the computed data and plot parameters, then generates the plot.
6. Converts the plot image to a base64 string for embedding in the report.
7. Returns a dictionary containing both the computed data and chart metadata.

**Example Usage:**

.. code-block:: python

    section = build_acf_pacf_section(report_builder)
    data = section["data"]
    chart = section["chart"]

Dependencies
------------

- ``os``: For file path operations.
- ``register_section``, ``ANALYZERS_REGISTRY``, ``PLOTTERS_REGISTRY``: For section registration and dynamic class retrieval.
- ``ReportBuilderProtocol``: Protocol for the report builder object.

Registries
----------

- ``ANALYZERS_REGISTRY["acf_pacf"]``: Provides the analyzer class and its parameter class for ACF/PACF.
- ``PLOTTERS_REGISTRY["acf_pacf"]``: Provides the plotter class and its parameter class for ACF/PACF.

Section Registration
--------------------

The function is registered as a report section under the name ``"acf_pacf"`` using the ``@register_section`` decorator.

.. code-block:: python

    @register_section("acf_pacf")
    def build_acf_pacf_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
        ...

See Also
--------

- :mod:`owlmix.registry.registry`
- :mod:`owlmix.reporting.sections.protocol_cls`
- :mod:`owlmix.reporting.sections.acf_pacf`
