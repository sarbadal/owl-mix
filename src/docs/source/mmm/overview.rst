.. _mmm.overview:

MMM Module
==========

The `mmm` (Marketing Mix Modeling) module provides a comprehensive suite of 
tools for building, analyzing, and visualizing marketing mix models. 
It is organized into several submodules, each responsible for a specific 
aspect of the modeling workflow.

Submodules
----------

analysis
--------

The `analysis` submodule contains tools for evaluating and interpreting model results.

- **classifier.py**: Implements classification utilities for model outputs.
- **contribution.py**: Calculates the contribution of each feature or channel.
- **metrics.py**: Provides metrics for model evaluation.
- **response_curve.py**: Generates and analyzes response curves.
- **s_curve_filler.py**: Fills and smooths S-curves for response analysis.
- **summary.py**: Summarizes model results and key findings.

config
------

The `config` submodule manages configuration settings for MMM pipelines.

- **transform_config.py**: Handles transformation configurations for data preprocessing.

models
------

The `models` submodule defines the core modeling classes and interfaces.

- **base.py**: Abstract base classes for all models.
- **liner.py**: Linear model implementations.
- **simple_model.py**: Simple baseline models for quick prototyping.
- **sklearn.py**: Wrappers and utilities for scikit-learn models.

pipeline
--------

The `pipeline` submodule orchestrates the end-to-end modeling workflow.

- **model_pipeline.py**: Defines the main pipeline for model training and evaluation.
- **pipeline.py**: General pipeline utilities and helpers.

transformers
------------

The `transformers` submodule provides data transformation utilities.

- **adstock.py**: Implements adstock transformation for media variables.
- **base.py**: Base classes for all transformers.
- **hill.py**: Hill function transformation for diminishing returns.
- **log.py**: Log transformation utilities.
- **saturation.py**: Saturation transformation for media response.
- **scaler.py**: Scaling utilities for feature normalization.

utils
-----

The `utils` submodule contains helper functions and utilities.

- **helpers.py**: General-purpose helper functions used throughout the module.

visualization
-------------

The `visualization` submodule provides tools for visualizing model results.

- **marginal_roi.py**: Plots marginal ROI curves.
- **plotter.py**: General plotting utilities for model outputs.

Usage Example
-------------

.. code-block:: python

   from owlmix.mmm.models.simple_model import SimpleModel
   from owlmix.mmm.pipeline.model_pipeline import ModelPipeline
   from owlmix.mmm.transformers.adstock import AdstockTransformer

   # Example: Build and run a simple MMM pipeline
   model = SimpleModel()
   transformer = AdstockTransformer()
   pipeline = ModelPipeline(model=model, transformer=transformer)
   results = pipeline.run(data)

   # Visualize results
   from owlmix.mmm.visualization.plotter import plot_results
   plot_results(results)

Module Structure
----------------

.. code-block:: text

   mmm/
   ├── analysis/
   ├── config/
   ├── models/
   ├── pipeline/
   ├── transformers/
   ├── utils/
   └── visualization/

For detailed API documentation, refer to the respective submodule documentation.

Further Reading
---------------

- :doc:`Analysis Overview <analysis/overview>`
- :doc:`Configuration Overview <config/overview>`

----

*This documentation provides an overview of the MMM module. For more details on each class and function, see the API reference and example notebooks.*

:ref:`Back to Home <home>`