from utils.utils import  get_full_planet_name
from tabulate import tabulate

def pprint_req(req):
    i = 1
    P = get_full_planet_name(req["planet"])
    for item, details in req["req"].items():
        Q = details["quantity"]
        S = details["speed"]
        print(f"{i}. You Want to produce {Q} K {item} with a speed of {S} items/sec on planet {P}")
        i += 1
    
    print("----------------------------------------------------------------------------")
    input("Please hit Enter to Confirm or exit the script :)")

def pretty_print_dataframe(df):
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    

