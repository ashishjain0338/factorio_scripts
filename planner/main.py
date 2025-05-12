import json
from utils.pretty_printers import pprint_req, pretty_print_dataframe
from utils.utils import load_recipe_files, get_full_planet_name
from calculators.speed_and_machine_count_calculator import SpeedAndQuantityCalculator


def raw_material_summary(df):
    i = 1
    for index, row in df[df["is_raw_material"]].iterrows():
        # print(index, row)
        Q = row['quantity']
        Q /= 1000 # Millions
        Q = round(Q, 3)
        print(f"{i}. You need {Q} M units of {row['item']}")
        i += 1

def intiate_speed_and_machine_count_calculations(req, recipe_catalog, calc_obj):
    out = {}
    for item, details in req.items():
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
    df = calc_obj.get_dataframe(out, recipe_catalog)
    # print(df)
    
    return df
    


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

    print("Calculating....")
    planet = get_full_planet_name(req["planet"])
    calc_obj = SpeedAndQuantityCalculator(RAW_MATERIAL[planet], planet)
    df = intiate_speed_and_machine_count_calculations(req["req"], recipe_catalog, calc_obj)
    pretty_print_dataframe(df)
    print("-------------- Raw-material Summary ------------------------------")
    raw_material_summary(df)
    exportedfile = "output/processed.csv"
    df.to_csv(exportedfile, index = False)
    print("File exported to : ", exportedfile)
    
