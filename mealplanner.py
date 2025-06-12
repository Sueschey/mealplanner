import json
import os
import argparse
import random
"""
To-Do:
Carb-Variety implementieren
Meat-Preferences einstellbar machen + filtern beim Erstellen von Plänen
Carbs mitprinten bei den Tagen, falls vorhanden
"""
RECIPE_DATA = "recipes.json"
SETTINGS_FILE = "settings.json"

## SETTINGS

def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "days_to_plan": 5,
            "min_healthy_per_week": 2,
            "min_vegetarian_per_week": 2,
            "min_vegan_per_week": 0,
            "min_berk_favorite_per_week": 0,
            "min_stella_favorite_per_week": 0,
            "max_expensive_per_week": 1,
            "min_carb_variety_per_week": 2,
            "meat_preferences": ["poultry", "beef", "pork", "fish", "other"],
        }
def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

def change_settings():
    settings = load_settings()
    for key, val in settings.items():
        print(f"Current {key}: {val}")
        inp = input(f"Change {key} to (Enter to skip): ").strip()
        if not inp:
            continue

        if isinstance(val, int):
            if inp.isdigit():
                settings[key] = int(inp)
            else: print(f"Invalid input for {key}, must be an integer")
        elif isinstance(val, bool):
            if inp.lower() == "y":
                settings[key] = True
            elif inp.lower() == "n":
                settings[key] = False
            else: print(f"Invalid input for {key}, please enter either 'y' or 'n'.")
        elif isinstance(val, list):
            settings[key] = [x.strip() for x in inp.split(",") if x.strip()]

    save_settings(settings)
    print("Settings saved!")

def print_settings():
    settings = load_settings()
    print(r"""
   (\  /)
  ( • ω •)   <(These are your current settings!)
c/ > ♡ <     
""")
    for key, val in settings.items():
        print(f"\t{key}: {val}")


## RECIPES

def load_recipes():
    if not os.path.exists(RECIPE_DATA):
        return []
    with open(RECIPE_DATA, "r", encoding="utf-8") as f:
        return json.load(f)

def save_recipe(recipe):
    if os.path.exists(RECIPE_DATA):
        with open(RECIPE_DATA, "r", encoding="utf-8") as f:
            try:
                recipes = json.load(f)
            except json.JSONDecodeError:
                recipes = []
    else:
        recipes = []
    recipes.append(recipe)
    with open(RECIPE_DATA, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)

def add_recipe():
    print(r""" 
           (\  (\
          („• ֊ •)   <(Let's add a new recipe together!)
        c/ づ♡  
    """)
    name = input("Name of dish: ").strip()
    url = input("URL (optional): ").strip()
    meat_type = "none"
    vegan = input("Is the meal vegan? ").strip().lower() == "y"
    if vegan: vegetarian = True
    if not vegan:
        vegetarian = input("Is the meal vegetarian? ").strip().lower() == "y"
        if not vegetarian:
            print("What meat? Enter 1/2/3/4/5")
            print("[1] Poultry (e.g. chicken)")
            print("[2] Beef")
            print("[3] Pork")
            print("[4] Fish")
            print("[5] Other")
            meat_options = {
                "1": "poultry",
                "2": "beef",
                "3": "pork",
                "4": "fish",
                "5": "other"
            }
            while True:
                choice = input("Meat (1–5): ").strip()
                if choice in meat_options:
                    meat_type = meat_options[choice]
                    break
                else:
                    print("Please enter a number between 1 and 5.")
    tags = []
    if input("Is this meal expensive? y/n: ").strip().lower() == "y":
        tags.append("expensive")
    if input("Is this meal healthy? y/n: ").strip().lower() == "y":
        tags.append("healthy")
    if input("Does Berk love this dish? y/n: ").strip().lower() == "y":
        tags.append("berk")
    if input("Does Stella love this dish? y/n: ").strip().lower() == "y":
        tags.append("stella")

    carbs_recom = []
    if input("Would you like to add which carbs you recommend for this meal? (y/n): ").strip().lower() == "y":
        print("\nAnswer 'y' if the meal goes well with the following carbs: ")

        carb_options = [
            "Rice",
            "Bulgur",
            "Pasta",
            "Lentils",
            "Potatoes",
            "Mashed potatoes",
            "Bread"
        ]

        for carb in carb_options:
            if input(f"{carb}? y/n: ").strip().lower() == "y":
                carbs_recom.append(carb)

        if input("Would you like to add another carb? y/n: ").strip().lower() == "y":
            other_carb = input("Type name of carb: ").strip()
            if other_carb:
                carbs_recom.append(other_carb.capitalize())
    recipe = {"name": name,
              "url": url,
              "meat_type": meat_type,
              "vegan": vegan,
              "vegetarian": vegetarian,
              "tags": tags,
              "carbs_recom": carbs_recom}
    save_recipe(recipe)

def change_recipe():
    recipes = load_recipes()
    print(r"""
           /)  /)
          ( • ֊ •)     <(I'll help you change your recipe!)
        c/ づ づ  
 """)
    inp = input("Which recipe would you like to change? ").strip().lower()
    for recipe in recipes:
        if recipe["name"].lower() == inp:
            print(f"Change the following recipe? (y/n):")
            for key, value in recipe.items():
                print(f"\t{key}: {value}")
            if input("Type 'y' or 'n': ").strip().lower() == "y":
                while True:
                    print("Chose what to change:")
                    print("[1] Name")
                    print("[2] URL")
                    print("[3] Vegan/Vegetarian/Meat")
                    print("[4] Tags")
                    print("[5] Recommended carbs")
                    match input("Enter digit"):
                        case "1":
                            new_name = input("New name of dish: ").strip()
                            recipe["name"] = new_name
                        case "2":
                            url = input("New URL: ").strip()
                            recipe["url"] = url
                        case "3":
                            print("Which is true for the meal? (Choose one)")
                            print("[1] Vegan")
                            print("[2] Vegetarian (but not vegan)")
                            print("[3] Poultry")
                            print("[4] Beef")
                            print("[5] Pork")
                            print("[6] Fish")
                            print("[7] Other meat")
                            match input("Enter digit"):
                                case "1":
                                    recipe["vegan"] = True
                                    recipe["vegetarian"] = True
                                    recipe["meat_type"] = None
                                case "2":
                                    recipe["vegan"] = False
                                    recipe["vegetarian"] = True
                                    recipe["meat_type"] = None
                                case "3":
                                    recipe["vegan"] = False
                                    recipe["vegetarian"] = False
                                    recipe["meat_type"] = "poultry"
                                case "4":
                                    recipe["vegan"] = False
                                    recipe["vegetarian"] = False
                                    recipe["meat_type"] = "beef"
                                case "5":
                                    recipe["vegan"] = False
                                    recipe["vegetarian"] = False
                                    recipe["meat_type"] = "pork"
                                case "6":
                                    recipe["vegan"] = False
                                    recipe["vegetarian"] = False
                                    recipe["meat_type"] = "fish"
                                case "7":
                                    recipe["vegan"] = False
                                    recipe["vegetarian"] = False
                                    recipe["meat_type"] = "other"
                                case _:
                                    print("Invalid input!")
                        case "4":
                            tags = []
                            if input("Is this meal expensive? y/n: ").strip().lower() == "y":
                                tags.append("expensive")
                            if input("Is this meal healthy? y/n: ").strip().lower() == "y":
                                tags.append("healthy")
                            if input("Does Berk love this dish? y/n: ").strip().lower() == "y":
                                tags.append("berk")
                            if input("Does Stella love this dish? y/n: ").strip().lower() == "y":
                                tags.append("stella")
                            recipe["tags"] = tags
                        case "5":
                            print("\nAnswer 'y' if the meal goes well with the following carbs: ")
                            carbs_recom = []
                            carb_options = [
                                "Rice",
                                "Bulgur",
                                "Pasta",
                                "Lentils",
                                "Potatoes",
                                "Mashed potatoes"
                            ]

                            for carb in carb_options:
                                if input(f"{carb}? (y/n): ").strip().lower() == "y":
                                    carbs_recom.append(carb)

                            if input("Would you like to add another carb? (y/n): ").strip().lower() == "y":
                                other_carb = input("Type name of carb: ").strip()
                                if other_carb:
                                    carbs_recom.append(other_carb.capitalize())
                            recipe["carbs_recom"] = carbs_recom
                        case _: print("Invalid input!")
                    if input("Stop changing recipe? (y/n): ").strip().lower() == "y": break
    print("Couldn't find that recipe...")
def get_url(name):
    recipes = load_recipes()
    for recipe in recipes:
        if recipe["name"] == name:
            return recipe["url"]
    return None


def delete_recipe(name):
    recipes = load_recipes()
    original_length = len(recipes)
    recipes = [r for r in recipes if r["name"].strip().lower() != name.strip().lower()] #löschen
    with open(RECIPE_DATA, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)
    if len(recipes) == original_length:
        print("No recipe to delete!")
    else: print(f"Successfully deleted {original_length - len(recipes)} recipes.")

def print_recipes():
    recipes = load_recipes()
    print(r"""
           (\  /)
          („^ ᵕ ^)   <(Your current recipes are: )
        c/ っ   っ
              """)
    i = 1
    for recipe in recipes:
        print(f"\t {i}. {recipe['name']}")
        i += 1
### MEAL PLANNER
def generate():
    recipes = load_recipes()
    settings = load_settings()
    days = settings["days_to_plan"]
    needed_healthy = settings["min_healthy_per_week"]
    needed_vegan = settings["min_vegan_per_week"]
    needed_vegetarian = settings["min_vegetarian_per_week"]
    allowed_expensive = settings["max_expensive_per_week"]
    needed_berk = settings["min_berk_favorite_per_week"]
    needed_stella = settings["min_stella_favorite_per_week"]
    needed_variety = settings["min_carb_variety_per_week"]

    current_healthy, current_vegan, current_vegetarian, current_expensive, current_berk, current_stella, current_variety =\
        0, 0, 0, 0, 0, 0, 0
    i = 0
    while i < 1000:
        temp_plan = []
        random.shuffle(recipes)

        #fulfill vegan settings
        while needed_vegan > current_vegan:
            for recipe in recipes:
                if current_vegan >= needed_vegan:
                    break
                if recipe["name"] in temp_plan:
                    continue
                elif recipe["vegan"] == True:
                    if "expensive" in recipe["tags"] and allowed_expensive <= 0:
                        continue
                    temp_plan.append(recipe["name"])
                    current_vegan += 1
                    current_vegetarian += 1
                    if "berk" in recipe["tags"]: current_berk += 1
                    if "stella" in recipe["tags"]: current_stella += 1
                    if "expensive" in recipe["tags"]: current_expensive += 1
                    if "healthy" in recipe["tags"]: current_healthy += 1

        #fulfill vegetarian settings
        while needed_vegetarian > current_vegetarian:
            for recipe in recipes:
                if current_vegetarian >= needed_vegetarian:
                    break
                if recipe["name"] in temp_plan:
                    continue
                elif recipe["vegetarian"] == True:
                    if "expensive" in recipe["tags"] and allowed_expensive <= 0:
                        continue
                    temp_plan.append(recipe["name"])
                    current_vegetarian += 1

                    if recipe["vegan"] == True: current_vegan += 1
                    if "berk" in recipe["tags"]: current_berk += 1
                    if "stella" in recipe["tags"]: current_stella += 1
                    if "expensive" in recipe["tags"]: current_expensive += 1
                    if "healthy" in recipe["tags"]: current_healthy += 1

        #fulfill healthy settings
        while needed_healthy > current_healthy:
            for recipe in recipes:
                if current_healthy >= needed_healthy:
                    break
                if recipe["name"] in temp_plan:
                    continue
                elif "healthy" in recipe["tags"]:
                    if "expensive" in recipe["tags"] and allowed_expensive <= 0:
                        continue
                    temp_plan.append(recipe["name"])
                    current_healthy += 1

                    if recipe["vegan"] == True: current_vegan += 1
                    if recipe["vegetarian"] == True: current_vegetarian += 1
                    if "berk" in recipe["tags"]: current_berk += 1
                    if "stella" in recipe["tags"]: current_stella += 1
                    if "expensive" in recipe["tags"]: current_expensive += 1
        #fulfill Berk favorite settings
        while needed_berk > current_berk:
            for recipe in recipes:
                if current_berk >= needed_berk:
                    break
                if recipe["name"] in temp_plan:
                    continue
                elif "berk" in recipe["tags"]:
                    if "expensive" in recipe["tags"] and allowed_expensive <= 0:
                        continue
                    temp_plan.append(recipe["name"])
                    current_berk += 1
                    if recipe["vegan"] == True: current_vegan += 1
                    if recipe["vegetarian"] == True: current_vegetarian += 1
                    if "healthy" in recipe["tags"]: current_healthy += 1
                    if "stella" in recipe["tags"]: current_stella += 1
                    if "expensive" in recipe["tags"]: current_expensive += 1

        #fulfill Stella favorite settings
        while needed_stella > current_stella:
            for recipe in recipes:
                if current_stella >= needed_stella:
                    break
                if recipe["name"] in temp_plan:
                    continue
                elif "stella" in recipe["tags"]:
                    if "expensive" in recipe["tags"] and allowed_expensive <= 0:
                        continue
                    temp_plan.append(recipe["name"])
                    current_stella += 1
                    if recipe["vegan"] == True: current_vegan += 1
                    if recipe["vegetarian"] == True: current_vegetarian += 1
                    if "healthy" in recipe["tags"]: current_healthy += 1
                    if "berk" in recipe["tags"]: current_berk += 1
                    if "expensive" in recipe["tags"]: current_expensive += 1
        #fill rest of days
        while len(temp_plan) < days:
            for recipe in recipes:
                if len(temp_plan) >= days:
                    break
                if recipe["name"] in temp_plan:
                    continue
                if "expensive" in recipe["tags"] and allowed_expensive <= 0:
                    continue
                temp_plan.append(recipe["name"])
                if recipe["vegan"] == True: current_vegan += 1
                if recipe["vegetarian"] == True: current_vegetarian += 1
                if "healthy" in recipe["tags"]: current_healthy += 1
                if "berk" in recipe["tags"]: current_berk += 1
                if "stella" in recipe["tags"]: current_stella += 1
                if "expensive" in recipe["tags"]: current_expensive += 1
        #check if all requirements are met
        if len(temp_plan) == days:
            if (current_vegan >= needed_vegan and
                current_vegetarian >= needed_vegetarian and
                current_healthy >= needed_healthy and
                current_berk >= needed_berk and
                current_stella >= needed_stella and
                current_expensive <= allowed_expensive):
                return temp_plan, current_vegan, current_vegetarian, current_healthy, current_berk, current_stella, current_expensive
        i +=1
    return None



def main():
    parser = argparse.ArgumentParser(description="Weekly meal planner")
    subparsers = parser.add_subparsers(dest="commands")
    subparsers.add_parser("add", help="Add a new recipe")
    subparsers.add_parser("del", help="Delete recipes")
    subparsers.add_parser("list", help="List recipes")
    subparsers.add_parser("settings", help="See current settings and adjust them")
    subparsers.add_parser("change", help="Change recipes")
    subparsers.add_parser("gen", help="Generate meal plan")
    args = parser.parse_args()

    if not args.commands:
        parser.print_help()
        return

    elif args.commands == "add":
        add_recipe()

    elif args.commands == "del":
        print(r"""
           (\  /)
          (.>﹏<)   <(It's okay if you wanna get rid of some recipes...
        c/ づ♡づ               just don't get rid of me!)
                """)
        while True:
            inp= input("What recipe would you like to delete? (press Enter to return) ").strip().lower()
            if not inp: break
            else: delete_recipe(inp)

    elif args.commands == "list":
        print_recipes()

    elif args.commands == "change":
        change_recipe()

    elif args.commands == "settings":
        print_settings()
        if input("Would you like to change settings? (y/n): ").strip().lower() == "y":
            change_settings()

    elif args.commands == "gen":
        plan, vegan, vegetarian, healthy, berk, stella, expensive = generate()
        if plan:
            print(r"""
 ⠀     (\__/)      
       (•ㅅ•)      <(Finally... My training has paid off...)
    ＿ノヽ ノ＼＿   
`/　`/ ⌒Ｙ⌒ Ｙ  ヽ'            __  __            _     ____  _     
( 　(三ヽ人　 /　  |          |  \/  | ___  __ _| |   |  _ \| | __ _ _ __  
|　ﾉ⌒＼ ￣￣ヽ   ノ           | |\/| |/ _ \/ _` | |   | |_) | |/ _` | '_ \ 
ヽ＿＿＿＞､＿_／              | |  | |  __/ (_| | |   |  __/| | (_| | | | |
     ｜( 王 ﾉ〈               |_|  |_|\___|\__,_|_|   |_|   |_|\__,_|_| |_|
     /ﾐ`ー―彡  \ 
    / ╰    ╯    \ 
""")
            print("***" * 10)
            for day in range(len(plan)):
                print("\nDay %i : %s \n" % (day+1, plan[day]))
                url = get_url(plan[day])
                if url: print("URL: %s" % url)
                print("- - - " * 10)
            print("Stats...")
            print("- Vegan: " + str(vegan))
            print("- Vegetarian: " + str(vegetarian))
            print("- Healthy: " + str(healthy))
            print("- Among Berk's favorites: " + str(berk))
            print("- Among Stella's favorites: " + str(stella))
            print("- Expensive: " + str(expensive))
        else: print("No plans have been generated!")

if __name__ == "__main__":
    main()