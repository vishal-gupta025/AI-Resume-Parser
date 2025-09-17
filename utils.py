import os
import tempfile
import json
from typing import List, Dict

def save_json(results: List[Dict], filename="parsed_resumes.json") -> str:
    """Save results to a temp JSON file and return path"""
    json_path = os.path.join(tempfile.gettempdir(), filename)
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
    return json_path
