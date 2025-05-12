import pandas as pd
import math
from utils.exceptions import ItemNotFoundInRecipeCatalogError


class SpeedAndQuantityCalculator:

    def __init__(self, raw_material, planet):
        self.raw_material = raw_material
        self.planet = planet

    def calculate_speed(self, item, speed_req, recipes, out, tabs):
        # print(f"TabLevel : {tabs}  :Running for item ", item, " Speed: ", speed_req)
        # tabStr = ""
        if item not in recipes.keys():
            if item not in self.raw_material:
                print(f"WARNING: Item {item} not found")
                exit(101)
            return
        if item in self.raw_material:
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
            self.calculate_speed(ingredients, speed_for_ingredient, recipes, out, tabs + 1)

    def calculate_speed_and_quantity_item_wise(self, item, speed_req, quantity, recipes, out, tabs):
        # print(f"TabLevel : {tabs}  :Running for item ", item, " Speed: ", speed_req)
        # tabStr = ""
        if item not in recipes.keys():
            if item not in self.raw_material:
                # print(f"WARNING: Item {item} not found")
                raise ItemNotFoundInRecipeCatalogError(f"WARNING: Item {item} not found")
            return
        if item in self.raw_material:
            return
            

        item_recipe = recipes[item]
        speed_req_per_unit = speed_req/item_recipe["unit"]
        product_unit_count = item_recipe["unit"] # How many number of products will be produced with this recipe
        for ingredients, ingredient_count in item_recipe["req"].items():
            # ingredient_count is How many units of ingredient are requied for this recipe
            # print(f"Ingredients Level: {tabs}, = {ingredients}")
            speed_for_ingredient = ingredient_count*speed_req_per_unit
            quantity_for_ingredient = (ingredient_count/ product_unit_count ) * quantity
            if ingredients in out.keys():
                out[ingredients]["speed"] += speed_for_ingredient
                out[ingredients]["quantity"] += quantity_for_ingredient
            else:
                out[ingredients] = {
                    "speed": speed_for_ingredient,
                    "quantity": quantity_for_ingredient
                }
            try:
                # Check if any planet specific recipe exist
                self.calculate_speed_and_quantity_item_wise(f"{ingredients}_{self.planet}", speed_for_ingredient, quantity_for_ingredient, recipes, out, tabs + 1)
            except ItemNotFoundInRecipeCatalogError:
                # If not, then go the default way
                self.calculate_speed_and_quantity_item_wise(ingredients, speed_for_ingredient, quantity_for_ingredient, recipes, out, tabs + 1)
            except Exception as err:
                # If any error other than that, It is not intended
                print("unknown error occured : Error: ", err)
                exit(102)

    def get_dataframe(self, out, recipe_catalog):
        table = []
        for item, details in out.items():
            row = [item, details["speed"], details["quantity"]]
            table.append(row)

        df = pd.DataFrame(table, columns=['item', 'speed', 'quantity'])
        df = df.sort_values(by='item')
        self.fill_machine_count(df, recipe_catalog)
        df["is_raw_material"] = df["item"].isin(self.raw_material)
        return df

    def fill_machine_count(self, df, recipes):
        df["machine_count"] = [0 for i in range(len(df))]
        for index, row in df.iterrows():
            speed_req = row["speed"] # Units required per second
            item = row["item"]
            if item in self.raw_material:
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