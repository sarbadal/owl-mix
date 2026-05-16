.. _reporting.sections.protocol-cls:

.. currentmodule:: owlmix.reporting.sections.protocol_cls

📑 sections.protocol_cls
========================

**Protocol for report builder classes.**

Any class implementing this protocol must provide the following attributes 
and methods, which are used for constructing and managing report sections, 
handling data, and exporting results.

Classes
-------

.. py:class:: ReportBuilderProtocol

    **Attributes:**

    - **df** (*pandas.DataFrame*): The main DataFrame containing the data for analysis.
    - **target_col** (*str*): The name of the target column for analysis.
    - **date_col** (*str*): The name of the date column in the DataFrame.
    - **config** (*ConfigBuilder*): The configuration object for the report.

    **Methods:**

    .. py:method:: add_all_sections()
        :abstractmethod:

        Add all available sections to the report.

    .. py:method:: include_sections(sections)
        :abstractmethod:

        Include only the specified sections in the report.

        :param sections: List of section names to include.
        :type sections: ``list[str]``

    .. py:method:: exclude_sections(sections)
        :abstractmethod:

        Exclude the specified sections from the report.

        :param sections: List of section names to exclude.
        :type sections: ``list[str]``

    .. py:method:: add_section(name, data, chart)
        :abstractmethod:

        Add a section to the report with the given name, data, and chart.

        :param name: Name of the section.
        :type name: ``str``
        :param data: Data dictionary for the section.
        :type data: ``dict``
        :param chart: Chart dictionary for the section.
        :type chart: ``dict``
        :returns: Self (the report builder instance).

    .. py:method:: add_section_by_name(name)
        :abstractmethod:

        Add a section to the report by its name.

        :param name: Name of the section.
        :type name: ``str``
        :returns: Self (the report builder instance).

    .. py:method:: build(output_path)
        :abstractmethod:

        Build the report and output it to the specified path.

        :param output_path: Path to save the report.
        :type output_path: ``str`` or ``pathlib.Path``
        :returns: Dictionary containing the report data.

    .. py:method:: image_to_base64(path)
        :abstractmethod:

        Convert an image at the given path to a base64-encoded string.

        :param path: Path to the image file.
        :type path: ``str`` or ``pathlib.Path``
        :returns: Base64-encoded string of the image.

    .. py:method:: save(path)
        :abstractmethod:

        Save the report to the specified path.

        :param path: Path to save the report.
        :type path: ``str`` or ``pathlib.Path``

Dependencies
------------

- ``pandas``
- ``typing.Protocol``
- ``pathlib.Path``
- ``ConfigBuilder`` from ``owlmix.config.config_builder``

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
