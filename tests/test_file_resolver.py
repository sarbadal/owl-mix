# tests/test_file_resolver.py
import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))


from owlmix.file_resolver import ConfigFileResolver


def main():
    config_file_path = "config/config.json"
    resolved_config_file_path = "config/resolved_config.json"

    resolver = ConfigFileResolver(
        config=config_file_path,
    )
    resolved_config = resolver.resolve()

    # resolver.print()
    f = resolver.to_python_string()
    print(f)

    # resolver.save(resolved_config_file_path)
    


if __name__ == "__main__":
    main()
