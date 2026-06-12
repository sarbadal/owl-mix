.. _mmm_synthetic_data:

.. currentmodule:: owlmix.mmm_synth.generator

📁 mmm_synth.generator
======================

The synthetic MMM data generator creates a time-indexed dataset with:

- Calendar features (date, year, month, week)
- Simulated media channel spend/impressions
- A generated target column: ``weekly_sales_units``


Quick Start
-----------

.. code-block:: python

   from owlmix.mmm_synth.generator import MMMDataGenerator

   config = {
      "dataset": {
         "start_date": "2024-01-01",
         "end_date": "2024-12-31",
         "frequency": "weekly"
      },
      "media_channels": [
         {
            "name": "tv_spend",
            "type": "paid",
            "distribution": "gamma",
            "params": {"shape": 2.0, "scale": 80.0, "clip_min": 0}
         },
         {
            "name": "search_spend",
            "type": "paid",
            "distribution": "lognormal",
            "params": {"mean": 3.0, "sigma": 0.4, "zero_fraction": 0.05}
         }
      ],
      "channel_coefs": {
         "tv_spend": {"coefficient": 0.7, "adstock": 0.4},
         "search_spend": {"coefficient": 1.0, "adstock": 0.2}
      },
      "transformations": {
         "tv_spend": {"saturation": "log"}
      },
      "noise": {"type": "gaussian", "std": 40},
      "base_sales": 1200
   }

   generator = MMMDataGenerator(config)
   df = generator.generate()
   print(df.head())

Accepted Constructor Inputs
---------------------------

``MMMDataGenerator(config)`` accepts:

- A Python ``dict``
- A file path (``str`` or ``pathlib.Path``) to a YAML config

When a file path is provided, configuration is loaded and validated by ``ConfigLoader``.

Generation Pipeline
-------------------

``MMMDataGenerator.generate()`` performs the following steps:

1. Build a time DataFrame via ``TimeSeriesBuilder``
2. Simulate media channels via ``MediaChannelSimulator``
3. Merge time and media data
4. Apply channel correlations hook (currently a no-op placeholder)
5. Build the target via ``TargetAssembler``

The returned DataFrame includes all generated features and the target.

Configuration Reference
-----------------------

Required top-level sections (for YAML/path input, enforced by ``ConfigLoader``):

- ``dataset``
- ``target``
- ``media_channels``
- ``channel_coefs``

``dataset``
~~~~~~~~~~~

Required keys:

- ``start_date`` (ISO date string)
- ``end_date`` (ISO date string)
- ``frequency``: ``daily`` | ``weekly`` | ``monthly``

``media_channels``
~~~~~~~~~~~~~~~~~~

List of channel definitions. Each channel requires:

- ``name``
- ``distribution``: ``gamma`` | ``normal`` | ``lognormal``
- ``params`` (distribution-specific)

Supported ``params`` include:

- ``shape``, ``scale`` (gamma)
- ``mean``, ``std`` (normal)
- ``mean``, ``sigma`` (lognormal)
- Optional: ``clip_min``, ``zero_fraction``

``channel_coefs``
~~~~~~~~~~~~~~~~~

Dictionary keyed by channel name. Each value typically includes:

- ``coefficient`` (required by loader for YAML/path mode)
- Optional ``adstock`` between 0 and 1
- Optional ``saturation`` between 0 and 1 (loader validation)

In target assembly, coefficient entries are also used to derive adstock/saturation
transform settings if explicit transformation config is not provided.

For curve-based saturation (``log``, ``sqrt``, ``hill``), use the
``transformations`` section.

Optional sections
~~~~~~~~~~~~~~~~~

- ``channel_correlations`` (validated, correlation application hook exists)
- ``external_factors``
- ``noise``
- ``seed``
- ``transformations``
- ``include_latent_effects``

Target Assembly Behavior
------------------------

``TargetAssembler`` creates ``weekly_sales_units`` by combining:

- Base sales level (``base_sales``, default 1000)
- Transformed media effects per channel
- Random noise (default Gaussian with std=50)

Built-in transforms:

- Geometric adstock
- Saturation curves: ``log``, ``sqrt``, ``hill``

If ``include_latent_effects`` is ``True``, additional ``<channel>_effect`` columns
are included for debugging/analysis.

Notes on Schema Compatibility
-----------------------------

The generator includes a normalization helper for legacy naming (for example,
``media_channel`` and ``channel`` aliases). In practice, current object
initialization still expects ``media_channels`` to be present before simulation
components are created.

For reliable usage, provide modern keys directly:

- ``dataset``
- ``media_channels``
- ``channel_coefs``

Example YAML
------------

.. code-block:: yaml

    dataset:
       start_date: "2024-01-01"
       end_date: "2024-12-31"
       frequency: "weekly"

    target:
       name: "weekly_sales_units"
       base_level: 1000

    media_channels:
       - name: "tv_spend"
          type: "paid"
          distribution: "gamma"
          params:
             shape: 2.0
             scale: 80.0
             clip_min: 0
       - name: "search_spend"
          type: "paid"
          distribution: "normal"
          params:
             mean: 200
             std: 30
             zero_fraction: 0.05

    channel_coefs:
       tv_spend:
          coefficient: 0.7
          adstock: 0.4
       search_spend:
          coefficient: 1.0
          adstock: 0.2

    transformations:
       tv_spend:
          saturation: "log"

    noise:
       type: "gaussian"
       std: 40

See Also
--------

- :doc:`MMM Overview <overview>`
- :doc:`Generate Synthetic Data <generate-synthetic-data>`

:ref:`Back to Home <home>`