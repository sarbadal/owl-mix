## Including, Excluding, and Reordering Charts in OwlMixReport

This guide demonstrates how to include, exclude, and reorder charts in your EDA report using the `OwlMixReport` class.

### Example Usage

```python
from owlmix.report import OwlMixReport
from owlmix.typing.enums import ChartID
from owlmix.utils.sample_data_generator import create_sample_data

df = create_sample_data(n=2046)
report = OwlMixReport(
    df,
    target="sales",
    date_column="time",
)

charts = [
    ChartID.DISTRIBUTION_CHART,
    ChartID.CORRELATION_CHART,
    ChartID.VIF_CHART,
]

# To include only specific charts:
report.summary_builder.include_charts(*charts)

# To exclude specific charts:
report.summary_builder.exclude_charts(*charts)

# To reorder charts:
report.summary_builder.reorder_charts(*charts)
```

### Parameters
- `include_charts(*charts)`: Only the specified charts will be included in the report.
- `exclude_charts(*charts)`: The specified charts will be excluded from the report.
- `reorder_charts(*charts)`: The charts will appear in the specified order in the report.

Avoid using include and exclude at the sametime. However, reopen can be used with exclude/include method.
```