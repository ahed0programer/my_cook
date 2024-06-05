from experta import *
import pandas as pd

recipes = pd.read_csv("recipes.csv")

class Recipe(Fact):
    name = Field(str , True)
    # a set of ingrediants and its amount needed to make this recipe
    ingrediants = Field(list , True)

    # ** Note : if the user requested this recipe for a different number of people from the number specifed for this recipe /n
    # ** we can calclulate the new ampount of ingrediants needed based on the ratio
    # to tell how many people this recipe enough for 
    enough_for = Field(int , True)

# to express the ingradiant as a pair of name and ammount 
# TODO : find a way to deal with different types of units used to masure ingrediants e.c gram,g for tomato like ; ml,spoon for salt
class ingrediant(Fact):
    name=Field(str , True)
    amount=Field(str , True)

# this class is made to express the ingrediants the user has 
# * in the beginneng we shall request the user to enter the ingrediants as facts and store it here 
class My_ingrediants(Fact):
    ingrediants = Field(list , True)


class MyCook_Engine(KnowledgeEngine):
    def __init__(self):
        super().__init__()

    @DefFacts()
    def init_Data(self):
        # ** store the recipes that our system has to suggest
        # get the recipes from a csv file for cleaner code 
        for i in recipes.index:
            yield Recipe(name= recipes.loc[i , "name"] , ingrediants=recipes.loc[i , "ingrediants"] , enough_for = recipes.loc[i , "enough_for"])
        
        # // TODO : add more recipes like these
        # ** you can add more recipes by running the store_trcipes python script ,,,, check it
        #  TODO : fix the recipes to store the ingrediants as a pair (ingrediant , amount)
        
    # Rule uesd to handle the suggestion operation
    @Rule()
    def suggest_recipes(self):
        pass
        # ! dear Luay & Jaafar , this needs to be filled \^_^/   !!!!
        # we rely on you 


    # TODO : idea ! -> we can make the system inference new recipes ..... think about it after finishing the code above ^ !!!
    Rule()
    def inferance_NewRecipes(self):
        pass
        # ! dear Luay & Jaafar , this needs to be filled \^_^/   !!!!
        # we rely on you 


my_cook = MyCook_Engine()
my_cook.reset()
my_cook.run()

  