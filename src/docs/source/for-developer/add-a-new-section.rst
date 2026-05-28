.. _for-developer.add-a-new-section:

Add a New Reporting Section
===========================

This guide explains how to add a new reporting section in OwlMix end to end.
It covers analysis, plotting, registry wiring, params, report section registration,
and docs/template integration.

Overview
--------

When you add a new section, all related keys must stay consistent across modules.
For example, if the section key is ``my_section``, reuse the same key in:

- ``ANALYZERS_REGISTRY`` key (if analyzer exists)
- ``PLOTTERS_REGISTRY`` key (if plotter exists)
- ``@register_section("my_section")`` decorator
- config attribute names such as ``my_section_config``

Core flow:

1. Create analysis and/or plotting classes.
2. Register classes in central registries.
3. Create params and expose them via ``params/__init__.py``.
4. Add config wiring in ``config_builder.py``.
5. Create a reporting section builder under ``reporting/sections``.
6. Import the section module in ``reporting/sections/__init__.py``.
7. Optionally add enum and HTML template support.

Step-by-step
------------

1. Pick a section key and scope
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choose one stable key such as ``my_section`` and decide if the section is:

- analysis-only
- plotting-only
- both analysis and plotting

2. Add analysis and/or plotting implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If analysis is required:

- Add analyzer class and analyzer params in ``src/owlmix/analysis``.

If plotting is required:

- Add plotter class and plotter params in ``src/owlmix/plotting``.

3. Register classes in ``registry.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update ``src/owlmix/registry/registry.py``:

- Import your analyzer and params class (if any).
- Import your plotter and params class (if any).
- Add entry to ``ANALYZERS_REGISTRY`` for analyzer sections.
- Add entry to ``PLOTTERS_REGISTRY`` for plotting sections.

Expected dictionary formats:

- Analyzer registry entry:

  .. code-block:: python

      "my_section": {
          "analyzer": MySectionAnalyzer,
          "params": MySectionAnalyzerParams,
      }

- Plotter registry entry:

  .. code-block:: python

      "my_section": {
          "plotter": MySectionPlotter,
          "params": MySectionPlotParams,
      }

4. Create params module and export in ``params/__init__.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``src/owlmix/params/my_section.py`` with config args/dataclass and a
``build(...)`` path that matches your existing params pattern.

Then update ``src/owlmix/params/__init__.py``:

- import ``my_section`` module
- export config args and params class in ``__all__``
- add ``Args.my_section = my_section`` style wiring

This is required so config builder can call ``Args.my_section.build(...)``.

5. Wire config in ``config_builder.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update ``src/owlmix/config/config_builder.py``:

- In ``_init_config`` add:

  .. code-block:: python

      self.my_section_config = Args.my_section.build(...)

- In ``update_config`` mapping add:

  .. code-block:: python

      "my_section": self.update_my_section_config,

- Add updater method:

  .. code-block:: python

      def update_my_section_config(self, **kwargs: Unpack[MySectionConfigArgs]) -> Self:
          self.my_section_config = replace(self.my_section_config, **kwargs)
          return self

6. Add reporting section builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``src/owlmix/reporting/sections/my_section.py`` and register it with
the section key.

Skeleton:

.. code-block:: python

    from typing import Any, Dict
    from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
    from .protocol_cls import ReportBuilderProtocol


    @register_section("my_section")
    def build_my_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
        config = report_builder.config.my_section_config

        # Optional analyzer path
        data: Dict[str, Any] = {}
        if "my_section" in ANALYZERS_REGISTRY:
            analyzer_cls = ANALYZERS_REGISTRY["my_section"]["analyzer"]
            analyzer_params_cls = ANALYZERS_REGISTRY["my_section"]["params"]
            analyzer_params = analyzer_params_cls(...)
            analyzer = analyzer_cls(df=report_builder.df.copy(deep=True), params=analyzer_params)
            data = analyzer.compute()

        # Optional plotter path
        chart = None
        if "my_section" in PLOTTERS_REGISTRY:
            plotter_cls = PLOTTERS_REGISTRY["my_section"]["plotter"]
            plotter_params_cls = PLOTTERS_REGISTRY["my_section"]["params"]
            plotter_params = plotter_params_cls(...)
            plotter = plotter_cls(df=report_builder.df, params=plotter_params)
            path = plotter.plot(output_dir=f"{report_builder.config.output_dir}/charts")
            chart = {
                "title": "My Section",
                "description": "Description for My Section.",
                "alt_text": "My section chart",
                "image": report_builder.image_to_base64(path),
            }

        return {"data": data, "chart": chart}

7. Import section module in sections ``__init__.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update ``src/owlmix/reporting/sections/__init__.py`` and add:

.. code-block:: python

    from . import my_section

This import is mandatory. Without it, decorator execution does not happen and
the section is not added to ``SECTION_BUILDERS``.

8. Optional but recommended: add enum support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use enum-based section selection APIs, add the section into
``src/owlmix/typing/enums.py`` under ``SectionEnum``.

Example:

.. code-block:: python

    MY_SECTION = ("my_section", "My Section")

9. Optional but recommended: add HTML template rendering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If section output must appear in rendered HTML reports:

- Create template file under ``src/owlmix/reporting/_templates/sections``
  (for example ``my_section.html``)
- Include it in ``src/owlmix/reporting/_templates/_default.html``

Without template integration, section data may exist in JSON but not in the
final HTML page.

10. Validation checklist
~~~~~~~~~~~~~~~~~~~~~~~~

Before opening PR, verify all items:

1. New analyzer and/or plotter class added.
2. Registries updated in ``registry.py``.
3. Params module created and exported via ``params/__init__.py``.
4. ``ConfigBuilder`` default and update wiring added.
5. Reporting section builder added with ``@register_section``.
6. Module imported in ``reporting/sections/__init__.py``.
7. SectionEnum updated (if enum selection is used).
8. HTML template added and included (if HTML rendering is required).
9. Relevant tests added or updated.

Common pitfalls
---------------

- Inconsistent section key naming across files.
- Missing import in ``reporting/sections/__init__.py``.
- Config attribute name mismatch (for example, using ``config.my_config`` but
  defining ``self.my_section_config``).
- Registry key mismatch between section builder and ``registry.py``.
- Forgetting to expose params in ``params/__init__.py``.

:ref:`Back to Home <home>`