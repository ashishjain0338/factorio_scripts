import json
from utils.pretty_printers import pprint_req
from utils.utils import load_recipe_files
from calculators.speed_and_machine_count_calculator import calculate_speed, get_dataframe, fill_machine_count

def generate_insights(df):
    # 1. Quantity of each Raw-Material and 
    pass

def intiate_speed_and_machine_count_calculations(req, recipe_catalog):
    # In the recipes catolog, set your required items as item = custom i.e.
    custom_req = {}
    planet = "N"
    for item, details in req.items():
        custom_req[item] = details["speed"] # Item and which speed you want
        planet = details["planet"]

    your_custom_recipe = {
        "unit": 1,
        "time": 1,
        "req": custom_req
    }

    # Set your recipe
    recipe_catalog["custom"] = your_custom_recipe
    # Calculate Speed of intermediate and raw-material based on your custom recipe:
    out = {}
    calculate_speed("custom", 1, recipe_catalog, out, 0)
    df = get_dataframe(out)
    df = fill_machine_count(df, recipe_catalog)
    print(df)

    # Now Fill some Known data
    


if __name__ == '__main__':
    print("Currently All recipes must be produced on same one planet")
    recipe_catalog = load_recipe_files()
    req_key = "main"
    with open('requirement.json', 'r') as fp:
        req = json.load(fp)
        req = req[req_key]
    pprint_req(req)

    print("Calculating the speed")
    intiate_speed_and_machine_count_calculations(req, recipe_catalog)
    
