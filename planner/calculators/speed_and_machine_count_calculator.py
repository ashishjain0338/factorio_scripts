import pandas as pd
import math

RAW_MATERIAL = ["copper_ore", "iron_ore", "water", "crude_oil", "coal", "stone"]

def calculate_speed(item, speed_req, recipes, out, tabs):
    # print(f"TabLevel : {tabs}  :Running for item ", item, " Speed: ", speed_req)
    # tabStr = ""
    if item not in recipes.keys():
        if item not in RAW_MATERIAL:
            print(f"WARNING: Item {item} not found")
            exit(101)
        return
    if item in RAW_MATERIAL:
        return
        

    item_recipe = recipes[item]
    speed_req_per_unit = speed_req/item_recipe["unit"]
    for ingredients, count in item_recipe["req"].items():
        # print(f"Ingredients Level: {tabs}, = {ingredients}")
        speed_for_ingredient = count*speed_req_per_unit
        if ingredients in out.keys():
            out[ingredients] += speed_for_ingredient
        else:
            out[ingredients] = speed_for_ingredient
        calculate_speed(ingredients, speed_for_ingredient, recipes, out, tabs + 1)

def get_dataframe(out):
    df = pd.DataFrame(list(out.items()), columns=['item', 'speed'])
    df = df.sort_values(by='item')
    return df

def fill_machine_count(df, recipes):
    df["machine_count"] = [0 for i in range(len(df))]
    for index, row in df.iterrows():
        speed_req = row["speed"] # Units required per second
        item = row["item"]
        if item in RAW_MATERIAL:
            continue
        unit_made_per_second_per_machine = recipes[item]["unit"]/ recipes[item]["time"]# units made per second
        machine_count =  math.ceil(speed_req / unit_made_per_second_per_machine)
        df.loc[index, "machine_count"] = machine_count
    return df




# if __name__ == '__main__':
#     calculate_speed("overall", 1, recipes, out, 0)
    
#     df = get_dataframe(out)
#     df = df.sort_values(by='item')
#     fill_machine_count(df, recipes)
#     print(df)
#     pretty_print(df)
#     df.to_csv("processed.csv", index=False)