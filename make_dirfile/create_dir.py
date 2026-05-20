import os
import yaml
 
 
def create_from_yaml(yaml_path: str, base_path: str = "."):
    with open(yaml_path, "r", encoding="utf-8") as f:
        structure = yaml.safe_load(f)
 
    def _create(node, current_path):
        for name, content in node.items():
            path = os.path.join(current_path, name)
 
            # Case 1: Folder
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                _create(content, path)
 
            # Case 2: File
            else:
                os.makedirs(current_path, exist_ok=True)
 
                file_content = content if content is not None else ""
 
                with open(path, "w", encoding="utf-8") as f:
                    f.write(file_content)
 
                print(f"Created file: {path}")
 
    _create(structure, base_path)

if __name__ == "__main__":
    create_from_yaml("mmm.yaml", "./")