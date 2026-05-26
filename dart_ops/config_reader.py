import yaml

def load_chapters_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
