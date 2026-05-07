.. _file_resolver:

Configuration Management with File Resolver
==========================================

The ``ConfigFileResolver`` utility simplifies managing configuration files by automatically resolving file references in JSON configs. This is useful for keeping configuration data organized across multiple files.

.. code-block:: python

    from owlmix.file_resolver import ConfigFileResolver

    # Create a resolver with a JSON config file
    resolver = ConfigFileResolver(config="config.json")

    # Resolve *_file keys to their actual content
    resolved_config = resolver.resolve()

    # Save the resolved config
    resolver.save("resolved_config.json")

    # Get as Python dictionary string
    python_dict_string = resolver.to_python_string()
    print(python_dict_string)

    # Print formatted output
    resolver.print()

How it works:
-------------

- Any JSON key ending with ``_file`` is automatically resolved to the file's content
- Supports any file type (HTML, TXT, MD, JSON, etc.)
- Works recursively through nested dictionaries and lists
- Includes built-in caching for efficiency

Example Configuration:
----------------------

.. code-block:: json

    {
        "report_template": {
            "description_file": "templates/report_description.html",
            "title": "Analysis Report",
            "metadata_file": "config/metadata.json"
        }
    }

After resolution, ``description_file`` key becomes ``description`` with the HTML file's content, and ``metadata_file`` becomes ``metadata`` with the JSON content.