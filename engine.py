from experta import *
from recipes import recipes
from myFacts import *

class MealRecommender(KnowledgeEngine):
    recipes=[]
    currentrecipe ={
                "name":"",
                "ingredient":[],
                "order":0
            }
    @DefFacts()
    def _initial_action(self):
        yield Fact(recipes_count=0)
        for recipe in recipes:
            yield Recipe(name=recipe['name'] , type=recipe['type'],servings=recipe['servings'] , order=0)
            for ingredient in recipe['ingredients']:
                yield Recipe_Ingredient(recipe_name = recipe['name'] , ingredient=ingredient , quantity=recipe['ingredients'][ingredient] , Changed=True , haveit=False)

    
    @Rule(NOT(MyIngredient(name=W())) ,salience=90)
    def ask_ingredients(self):
        ingredients = input("Enter the ingredients you have, separated by commas: ").strip().lower().split(',')
        ingredients = [ingredient.strip() for ingredient in ingredients]
        confirmation = input(f"You entered the following ingredients: {', '.join(ingredients)}. Is this correct? (yes/no): ").strip().lower()
        if confirmation == 'yes':
           for ingredient in ingredients:
                self.declare(MyIngredient(name=ingredient))
                self.declare(Fact(action='find_meal'))
        else:
            print("Let's try again.")
            self.ask_ingredients()  # Retry input if confirmation fails
            

    @Rule(Fact(action='find_meal') , NOT(MealType(type=W())) , salience=100 )
    def ask_meal_type(self):
        valid_meal_types = ["breakfast", "lunch", "dinner"]
        while True:
            meal_type = input("What type of meal do you want? (breakfast/lunch/dinner): ").strip().lower()
            if meal_type in valid_meal_types:
                self.declare(MealType(type=meal_type))
                break
            else:
                print(f"Invalid input: '{meal_type}'. Please enter a valid meal type (breakfast/lunch/dinner).")

        count = self.ask_number_of_people()
        self.declare(NumberOfPeople(count))
        self.declare(Fact(suggest=True))

    # assign a a priority to a recipe based on the ingredients we have
    @Rule( MealType(type=MATCH.type),
        AS.f << Fact(action='find_meal') ,
        AS.recipe_ingridient <<Recipe_Ingredient(recipe_name=MATCH.name ,ingredient=MATCH.ingredient , quantity=MATCH.quantity , Changed=MATCH.ischanged , haveit=W()),
        AS.recipe <<Recipe(name=MATCH.name , type=MATCH.type , servings=MATCH.servings,order=MATCH.order),
        MyIngredient(name=MATCH.ingredient),
        NumberOfPeople(MATCH.numOfPeople),
        TEST(lambda ischanged : ischanged),
        salience=10
        )
    def search_for_recipes(self, recipe , recipe_ingridient , order , servings, numOfPeople ,quantity):
        new_quantity = self.adjust_quantity(quantity , numOfPeople  , servings)
        self.modify(recipe_ingridient , quantity = new_quantity , Changed=False , haveit=True)
        order+=1
        self.modify(recipe , order=order)

    # to extract the recipes and rearrange them based on the user's needs
    @Rule( 
        MealType(type=MATCH.type),
        AS.f << Fact(action='find_meal') ,
        Recipe_Ingredient(recipe_name=MATCH.name ,ingredient=MATCH.ingredient_name , quantity=MATCH.quantity , Changed=MATCH.ischanged , haveit=MATCH.haveit),
        Recipe(name=MATCH.name , type=MATCH.type , servings=MATCH.servings,order=MATCH.order),
        salience=5
    )
    def extractMeals(self, name, ingredient_name , quantity , order , haveit):
        if(not name==self.currentrecipe["name"]):
            self.currentrecipe ={
                "name":name,
                "ingredients":[],
                "order":order
            }
            self.recipes.append(self.currentrecipe)
            self.recipes.sort(key=lambda x : x["order"] , reverse=True)

        ingredient = {
            "name":ingredient_name,
            "quantity":quantity ,
            "haveit":haveit
        }
        self.currentrecipe["ingredients"].append(ingredient)
      
    @Rule(Fact(suggest=True),NumberOfPeople(MATCH.numpeople) ,salience=0)
    def suggestMeal(self , numpeople):
        In=0
        for recipe in self.recipes:
            print("--------------------------------------")
            print(f"here you are 🤗 , I suggest you to cook {recipe['name']} ,it's a good taste recipe and enough for {numpeople} normal people")
            for ingredient in recipe["ingredients"]:
                if(ingredient['haveit']):
                    print(f"you need {ingredient['quantity']} of {ingredient['name']} that you already have")

            for ingredient in recipe["ingredients"]:
                if(not ingredient['haveit']):
                    print(f"you need to get {ingredient['quantity']} of {ingredient['name']} if it's not a problem")
            In = input(f"\n if you liked it enter 'ok' or click Enter to show more 🤞")
            if(In == 'ok'):
                break
        if(In!="ok"):
            print("😞😞 sorry my friend this is everything I know about cooking ")
            print("you can ask Sanji from ONE PIECE 🏴 ☠️  !! He is an amazing cook")
        
    def ask_number_of_people(self):
        while True:
            try:
                count = int(input("For how many people are you cooking?: ").strip())
                return count
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    
    def adjust_quantity(self, quantity, newservings , servings=1):
        # Adjust the quantity based on the number of servings
        ratio =newservings/servings
        if " " in quantity:
            number, unit = quantity.split(" ", 1)
            try:
                total_quantity = float(number) * ratio
                return f"{total_quantity} {unit}"
            except ValueError:
                return quantity  # In case quantity is not a number
        else:
            try:
                total_quantity = float(quantity) * ratio
                return f"{total_quantity}"
            except ValueError:
                return quantity  # In case quantity is not a number
