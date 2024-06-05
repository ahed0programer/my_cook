import pandas as pd

recipes  = pd.read_csv("recipes.csv")

try:
    df = pd.read_csv("recipes.csv")
except FileNotFoundError:
    df = pd.DataFrame()  # If the file does not exist, create an empty DataFrame

print("starting storing new recipes ...... , enter 'quit' to exit->")
while True:
    name = input("Enter the recipe name : ")
    if(name == "quit"):
        break

    print("enter an ingrediant ......enter 'pass' to end adding ingrediants")
    print("sperate the igrediants with comma , to add more than one /n ->  ") 
    ingrediant = input()
 
    if(ingrediant=="quit"):
        break
    
    ingrediants = ingrediant.split(",")
    print(ingrediants)

    enough_for = input("enter number of people : ")
    if(enough_for=="quit"):
        break
    enough_for = int(enough_for)
        
    new_data = {'name': name, 'ingrediants': ingrediants, 'enough_for':enough_for }
    new_row = pd.DataFrame([new_data])
    recipes = pd.concat([recipes, new_row], ignore_index=True)
    print("........................................................")

try:
    recipes.to_csv("recipes.csv", index=False)
    print("data's been stored sucessfully")
except Exception:
    print("Faild to save the data")

