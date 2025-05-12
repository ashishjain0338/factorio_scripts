import os
import json

def get_full_planet_name(planet_code):
    planet_map = {
        "N": "nauvis",
        "V": "vulcanus",
        "F": "fulgora",
        "A": "aquilo"
    }
    return planet_map[planet_code]

def load_recipe_files(folder_path = "recipes"):
    combined_data = {}

    # List all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        combined_data.update(data)
                        print("Loaded Recipe-File: ", file_path)
                    else:
                        print(f"Warning: Skipped {filename} because it does not contain a dictionary.")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {filename}: {e}")
    
    return combined_data