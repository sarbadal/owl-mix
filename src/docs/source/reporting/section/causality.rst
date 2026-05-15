.. _section.causality:

reporting.sections.causality
============================

This function provides the implementation for building the causality analysis section in a report. It integrates with the report builder framework and utilizes registered analyzers to compute causality results for specified features in a DataFrame.

.. currentmodule:: owlmix.reporting.sections.causality

Functions
---------

.. py:function:: build_causality_section(report_builder)

    Builds the causality analysis section for the report.

    This function retrieves configuration for causality analysis from the report builder,
    initializes the appropriate analyzer class with its parameters,
    computes the causality results, and returns a dictionary
    containing both the computed data and chart metadata (currently set to ``None``).

    :param report_builder: The report builder instance containing the dataframe and configuration.
    :type report_builder: ReportBuilderProtocol

    :returns: A dictionary with keys:

                - ``data``: The computed causality results.
                - ``chart``: Metadata and image for the generated plot (currently ``None``).
    :rtype: ``dict``

**Workflow:**

1. Retrieves the causality configuration from the report builder.
2. Fetches the analyzer class and its parameter class from the registry.
3. Initializes the analyzer parameter object using the configuration.
4. Instantiates the analyzer with the DataFrame and parameters, then computes the causality results.
5. Returns a dictionary containing both the computed data and chart metadata (currently ``None``).

**Example Usage:**

.. code-block:: python

    section = build_causality_section(report_builder)
    data = section["data"]
    chart = section["chart"]

Dependencies
------------

- ``os``: For file path operations.
- ``register_section``, ``ANALYZERS_REGISTRY``: For section registration and dynamic class retrieval.
- ``ReportBuilderProtocol``: Protocol for the report builder object.

Registries
----------

- ``ANALYZERS_REGISTRY["causality"]``: Provides the analyzer class and its parameter class for causality.

Section Registration
--------------------

The function is registered as a report section under the name ``"causality"`` using the ``@register_section`` decorator.

.. code-block:: python

    @register_section("causality")
    def build_causality_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
        ...

See Also
--------

- :mod:`owlmix.registry.registry`
- :mod:`owlmix.reporting.sections.protocol_cls`
- :mod:`owlmix.eda.causality`