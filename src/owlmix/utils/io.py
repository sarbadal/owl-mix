import json
from pathlib import Path
from typing import Any, Dict, Union


def read_file(path: Union[str, Path]) -> str:
    """Reads the content of a file and returns it as a string."""
    path = Path(path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, mode="r", encoding="utf-8") as f:
        return f.read()
    

def save_json(data: Dict, path: Union[str, Path]) -> None:
    """Saves a dictionary to a JSON file."""
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)