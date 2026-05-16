.. _reporting.sections.ccf:

.. currentmodule:: owlmix.reporting.sections.ccf

➡️ sections.ccf
===============

**Builds the Cross-Correlation Function (CCF) analysis section for the report.**

This function retrieves configuration for CCF analysis from the report builder,
initializes the appropriate analyzer class with its parameters,
computes the CCF results, and returns a dictionary
containing both the computed data and chart metadata (currently set to ``None``).

Functions
---------

.. py:function:: build_ccf_section(report_builder)

    :param report_builder: The report builder instance containing the dataframe and configuration.
    :type report_builder: ``ReportBuilderProtocol``

    :returns: A dictionary with keys:

                - ``data``: The computed CCF results.
                - ``chart``: Metadata and image for the generated plot (currently ``None``).
    :rtype: ``dict``

**Workflow:**

1. Retrieves the CCF configuration from the report builder.
2. Fetches the analyzer class and its parameter class from the registry.
3. Initializes the analyzer parameter object using the configuration.
4. Instantiates the analyzer with the DataFrame and parameters, then computes the CCF results.
5. Returns a dictionary containing both the computed data and chart metadata (currently ``None``).

**Example Usage:**

.. code-block:: python

    section = build_ccf_section(report_builder)
    data = section["data"]
    chart = section["chart"]

Dependencies
------------

- ``os``: For file path operations.
- ``register_section``, ``ANALYZERS_REGISTRY``: For section registration and dynamic class retrieval.
- ``ReportBuilderProtocol``: Protocol for the report builder object.

Registries
----------

- ``ANALYZERS_REGISTRY["ccf"]``: Provides the analyzer class and its parameter class for CCF.

Section Registration
--------------------

The function is registered as a report section under the name ``"ccf"`` using the ``@register_section`` decorator.

.. code-block:: python

    @register_section("ccf")
    def build_ccf_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
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