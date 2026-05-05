from owlmix.typing.enums import ChartID, Period, ComparisonType, PlotMode

def main():
    """Main function."""
    enum_class = ComparisonType

    class_list = enum_class.list()

    class_options = enum_class.options()
    class_pretty_options = enum_class.pretty_options()

    print(class_pretty_options)

if __name__ == "__main__":
    main()