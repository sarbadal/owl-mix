.. _reporting.sections.box-plot:

.. currentmodule:: owlmix.reporting.sections.box_plot

➡️ sections.box_plot
====================

**Builds the Box Plot section for the report.**

This function retrieves configuration for box plot analysis from the report builder,
initializes the appropriate analyzer and plotter classes with their parameters,
computes the necessary data for box plots, generates the corresponding plots,
and returns a dictionary containing both the computed data and chart metadata (including a base64-encoded image).


Functions
---------

.. py:function:: build_box_plot_section(report_builder)

    :param report_builder: The report builder instance containing the dataframe and configuration.
    :type report_builder: ``ReportBuilderProtocol``

    :returns: A dictionary with keys:

                - ``data``: The computed box plot results.
                - ``chart``: Metadata and image for the generated plot, including:

                    - ``title``: Title of the chart.
                    - ``description``: Description of the chart.
                    - ``alt_text``: Alternative text for the image.
                    - ``images``: Dictionary with base64-encoded image(s) of the plot.
    :rtype: ``dict``

**Workflow:**

1. Retrieves the box plot configuration from the report builder.
2. Fetches the analyzer and plotter classes and their parameter classes from the registries.
3. Initializes analyzer and plotter parameter objects using the configuration.
4. Instantiates the analyzer with the DataFrame and parameters, then computes the box plot data.
5. Instantiates the plotter with the computed data and plot parameters, then generates the plot.
6. Converts the plot image to a base64 string for embedding in the report.
7. Returns a dictionary containing both the computed data and chart metadata.

**Example Usage:**

.. code-block:: python

    section = build_box_plot_section(report_builder)
    data = section["data"]
    chart = section["chart"]

Dependencies
------------

- ``os``: For file path operations.
- ``register_section``, ``ANALYZERS_REGISTRY``, ``PLOTTERS_REGISTRY``: For section registration and dynamic class retrieval.
- ``ReportBuilderProtocol``: Protocol for the report builder object.

Registries
----------

- ``ANALYZERS_REGISTRY["box_plot"]``: Provides the analyzer class and its parameter class for box plots.
- ``PLOTTERS_REGISTRY["box_plot"]``: Provides the plotter class and its parameter class for box plots.

Section Registration
--------------------

The function is registered as a report section under the name ``"box_plot"`` using the ``@register_section`` decorator.

.. code-block:: python

    @register_section("box_plot")
    def build_box_plot_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
        ...

See Also
--------

- :ref:`ACF/PACF <reporting.sections.acf-pacf>`
- :ref:`Box Plot <reporting.sections.box-plot>`
- :ref:`Causality <reporting.sections.causality>`
- :ref:`Correlation <reporting.sections.correlation>`
- :ref:`Cross-Correlation Function (CCF) <reporting.sections.ccf>`
- :ref:`VIF <reporting.sections.vif>`
- :ref:`Protocol <reporting.sections.protocol-cls>`

:ref:`Back to Home <home>`