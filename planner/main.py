import json
from utils.pretty_printers import pprint_req
from utils.utils import load_recipe_files
from calculators.speed_and_machine_count_calculator import SpeedAndQuantityCalculator

def generate_insights(df):
    # 1. Quantity of each Raw-Material and 
    pass

def intiate_speed_and_machine_count_calculations(req, recipe_catalog, calc_obj):
    out = {}
    for item, details in req.items():
        print(item, details["speed"], details["quantity"])
        S = details["speed"]
        Q = details["quantity"]
        if item in out.keys():
            out[item]["speed"] += S
            out[item]["quantity"] += Q
        else:
            out[item] = {
                "speed": S,
                "quantity": Q
            }

        calc_obj.calculate_speed_and_quantity_item_wise(item, S, Q, recipe_catalog, out, 0)

    print(out)
    return
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
    with open("static-jsons/raw_material.json", "r") as fp:
        RAW_MATERIAL = json.load(fp)
    print(RAW_MATERIAL)
    recipe_catalog = load_recipe_files("static-jsons/recipes")
    req_key = "test1"
    with open('requirement.json', 'r') as fp:
        req = json.load(fp)
        req = req[req_key]
    pprint_req(req)

    print("Calculating the speed")
    calc_obj = SpeedAndQuantityCalculator(RAW_MATERIAL, "nauvis")
    intiate_speed_and_machine_count_calculations(req, recipe_catalog, calc_obj)
    
