utils.file_resolver
===================

.. module:: owlmix.utils.file_resolver
   :synopsis: A utility for resolving file references in JSON configurations.

Overview
--------

The **File Resolver** module provides the :class:`ConfigFileResolver` class, which automates the injection of external file content into a JSON-based configuration. This is particularly useful for managing large or complex configurations where some values are best stored in separate files (such as documentation, HTML, or markdown content).

The resolver scans a configuration dictionary (or a JSON file) for keys ending with ``_file``. When such a key is found, it replaces the key (removing the ``_file`` suffix) and populates it with the raw text content of the referenced file.

Key Features
------------

- **Recursive Resolution**: Handles nested dictionaries and lists, resolving all ``*_file`` keys at any depth.
- **Content Caching**: Prevents redundant disk I/O by caching file contents during resolution.
- **Flexible Input**: Accepts a dictionary, a path to a JSON file, or a string path as input.
- **Formatting Utilities**: Includes methods for pretty-printing the resolved configuration and exporting it back to JSON.
- **Supports Any File Type**: Works with HTML, TXT, MD, and other text-based files.

API Reference
-------------

.. py:class:: ConfigFileResolver

    A class to resolve file references in a configuration dictionary or JSON file.
    
    :param config: Input configuration as a dictionary or path to a JSON file.
    :type config: ``dict`` or ``str``
    
    .. py:method:: resolve() -> dict
    
        Resolves all ``*_file`` keys in the configuration and returns the updated dictionary.
    
        :returns: Resolved configuration with file contents injected.
        :rtype: ``dict``
    
    .. py:method:: pretty_print()
    
        Prints the resolved configuration in a human-readable format.
    
    .. py:method:: to_json(file_path: str)
    
        Exports the resolved configuration to a JSON file.
    
        :param file_path: Path to save the resolved configuration as JSON.
        :type file_path: ``str``

Example
-------

.. code-block:: python

    from owlmix.utils.file_resolver import ConfigFileResolver

    # Example input configuration
    config = {
        "title": "My Report",
        "description_file": "docs/description.txt",
        "metadata": {
            "summary_file": "docs/summary.md"
        }
    }

    resolver = ConfigFileResolver(config)
    resolved = resolver.resolve()

    # Result:
    # {
    #     "title": "My Report",
    #     "description": "<content of docs/description.txt>",
    #     "metadata": {
    #         "summary": "<content of docs/summary.md>"
    #     }
    # }


How It Works
------------

- The resolver loads the configuration from a dictionary or JSON file.
- It recursively searches for keys ending with ``_file``.
- For each such key, it reads the referenced file and replaces the key (removing ``_file``) with the file's content.
- The process is repeated for all nested dictionaries and lists.

Error Handling
--------------

- Raises :exc:`TypeError` if the input config is not a dict or a valid path to a JSON file.
- Raises :exc:`FileNotFoundError` if a referenced file does not exist.

----

For more advanced usage and examples, see the user guide and API documentation.
