# owlmix/file_resolver/file_resolver.py
from pathlib import Path
from typing import Any, Union
import json


class ConfigFileResolver:
    """
    Resolves *_file keys in a JSON config:

    - "description_file": "path/to/file.html"
        ↓
      "description": "<file content>"

    - Works recursively for nested dicts/lists
    - Supports any file type (html, txt, md, etc.)
    """

    def __init__(self, config: Union[str, Path, dict]):
        self.raw_config = self._load_config(config)
        self._cache = {}
        self.resolved_config = None

    # Load JSON
    def _load_config(self, config):
        if isinstance(config, (str, Path)):
            path = Path(config).resolve()

            with open(path, mode="r", encoding="utf-8") as f:
                return json.load(f)

        if isinstance(config, dict):
            return config

        raise TypeError("config must be dict or path to JSON file")

    # Public resolve method
    def resolve(self) -> dict:
        self.resolved_config = self._resolve_recursive(self.raw_config)
        return self.resolved_config

    def print(self):
        """Nicely prints the resolved config with proper formatting."""
        if self.resolved_config is None:
            raise ValueError("Call resolve() before printing.")

        self._print_recursive(self.resolved_config)

    def _print_recursive(self, obj, indent: int = 0) -> None:
        space = " " * indent

        if isinstance(obj, dict):
            print(f"{space}{{")
            for k, v in obj.items():
                print(f"{space}  {k}: ", end="")
                self._print_recursive(v, indent + 4)
            print(f"{space}}}")

        elif isinstance(obj, list):
            print(f"{space}[")
            for item in obj:
                self._print_recursive(item, indent + 4)
            print(f"{space}]")

        elif isinstance(obj, str):
            # Key part: print multiline strings properly
            if "\n" in obj:
                print()  # move to next line
                for line in obj.splitlines():
                    print(f"{space}  {line}")
            else:
                print(obj)

        else:
            print(obj)

    def to_python_string(self) -> str:
        """
        Returns the resolved config as a valid Python dictionary string.
        - Strings are quoted
        - Multiline strings use triple quotes
        """
        if self.resolved_config is None:
            raise ValueError("Call resolve() first")

        return self._format_python(self.resolved_config)

    def _format_python(self, obj, indent: int = 0) -> str:
        space = " " * indent

        if isinstance(obj, dict):
            items = []
            for k, v in obj.items():
                formatted_value = self._format_python(v, indent + 4)
                items.append(f'{space}    "{k}": {formatted_value}')
            return "{\n" + ",\n".join(items) + f"\n{space}}}"

        if isinstance(obj, list):
            items = [self._format_python(v, indent + 4) for v in obj]
            return "[\n" + ",\n".join(f"{space}    {item}" for item in items) + f"\n{space}]"

        if isinstance(obj, str):
            if "\n" in obj:
                # multiline → triple quotes
                return f'"""\n{obj}\n{space}"""'
            return f'"{obj}"'

        return repr(obj)

    # Recursive resolver
    def _resolve_recursive(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            new_dict = {}

            for key, value in obj.items():

                # RULE: keys ending with "_file"
                if key.endswith("_file") and isinstance(value, str):
                    new_key = key[:-5]  # remove "_file"
                    file_content = self._read_file(value)

                    # recurse in case file content is structured later (optional safety)
                    new_dict[new_key] = file_content

                else:
                    new_dict[key] = self._resolve_recursive(value)

            return new_dict

        if isinstance(obj, list):
            return [self._resolve_recursive(item) for item in obj]

        return obj

    # File reader with caching
    def _read_file(self, path: str) -> str:
        if path in self._cache:
            return self._cache[path]

        file_path = Path(path).resolve()

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(file_path, mode="r", encoding="utf-8") as f:
            content = f.read()

        self._cache[path] = content
        return content

    # Optional: save output
    def save(self, output_path: Union[str, Path]) -> None:
        if self.resolved_config is None:
            raise ValueError("Call resolve() before saving.")

        output_path = Path(output_path).resolve()
        with open(output_path, mode="w", encoding="utf-8") as f:
            json.dump(self.resolved_config, f, indent=2, ensure_ascii=False)