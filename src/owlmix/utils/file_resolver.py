"""Configuration Resolver Module"""
from pathlib import Path
from typing import Any, Union
import json

from .io import read_file, save_json


class ConfigFileResolver:
    """
    Resolves file references in a configuration dictionary or JSON file.
    Keys ending with `_file` are treated as file paths, and their content is read
    and injected into the config under a new key without the suffix.

    Args:
        config (Union[str, Path, dict]): A path to a JSON config file or a dictionary.

    Methods:
        resolve() -> dict: Resolves all file references and returns the updated config.
        print(): Nicely prints the resolved config with proper formatting.
        to_python_string() -> str: Returns the resolved config as a valid Python dictionary string.
        save(output_path: Union[str, Path]): Saves the resolved config to a JSON file.

    Example:
        resolver = ConfigFileResolver(config="config.json")
        resolved_config = resolver.resolve()
        resolver.print()
        python_str = resolver.to_python_string()
        resolver.save("resolved_config.json")
    """

    def __init__(self, config: Union[str, Path, dict]):
        self.raw_config = self._load_config(config)
        self._cache = {}
        self.resolved_config = None

    @staticmethod
    def _load_config(config: Union[str, Path, dict]) -> dict:
        if isinstance(config, (str, Path)):
            path = Path(config).resolve()
            with open(path, mode="r", encoding="utf-8") as f:
                return json.load(f)
        if isinstance(config, dict):
            return config
        raise TypeError("config must be dict or path to JSON file")

    def resolve(self) -> dict:
        """Resolves all ``*_file`` keys and returns the updated config."""
        self.resolved_config = self._resolve_recursive(self.raw_config)
        return self.resolved_config

    def print(self):
        """Nicely prints the resolved config with proper formatting."""
        if self.resolved_config is None:
            raise ValueError("Call resolve() before printing.")

        self._print_recursive(self.resolved_config)

    @classmethod
    def _print_recursive(cls, obj: Any, indent: int = 0) -> None:
        space = " " * indent
        if isinstance(obj, dict):
            print(f"{space}{{")
            for k, v in obj.items():
                print(f"{space}  {k}: ", end="")
                cls._print_recursive(v, indent + 4)
            print(f"{space}}}")
        elif isinstance(obj, list):
            print(f"{space}[")
            for item in obj:
                cls._print_recursive(item, indent + 4)
            print(f"{space}]")
        elif isinstance(obj, str):
            if "\n" in obj:
                print()
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

    @classmethod
    def _format_python(cls, obj, indent: int = 0) -> str:
        space = " " * indent
        if isinstance(obj, dict):
            items = []
            for k, v in obj.items():
                formatted_value = cls._format_python(v, indent + 4)
                items.append(f'{space}    "{k}": {formatted_value}')
            return "{\n" + ",\n".join(items) + f"\n{space}}}"

        if isinstance(obj, list):
            items = [cls._format_python(v, indent + 4) for v in obj]
            return "[\n" + ",\n".join(f"{space}    {item}" for item in items) + f"\n{space}]"

        if isinstance(obj, str):
            if "\n" in obj:
                return f'"""\n{obj}\n{space}"""'
            return f'"{obj}"'

        return repr(obj)

    def _resolve_recursive(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                if key.endswith("_file") and isinstance(value, str):
                    new_key = key[:-5]
                    file_content = self._read_file(value)
                    new_dict[new_key] = file_content
                else:
                    new_dict[key] = self._resolve_recursive(value)
            return new_dict

        if isinstance(obj, list):
            return [self._resolve_recursive(item) for item in obj]

        return obj

    def _read_file(self, path: str) -> str:
        if path in self._cache:
            return self._cache[path]

        content = read_file(path)
        self._cache[path] = content
        return content

    def save(self, output_path: Union[str, Path]) -> None:
        if self.resolved_config is None:
            raise ValueError("Call resolve() before saving.")

        save_json(self.resolved_config, output_path)