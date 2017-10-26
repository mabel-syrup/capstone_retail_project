from objects import drinkStep, drink, Recipe
from drinks_database import add_recipe, get_drink_names, close, make_db_if_deleted, get_drink_recipe, get_drink_abbreviation

drinks = []

def main():
    load_drinks_to_db()
    parse_drinks_to_list()
    close()
    finished = False
    while not finished:
        finished = parse_drink_input()


def parse_drink_input():
    size = None
    while size is None:
        in_size = str(input('Please choose a cup size:\nShort (8oz)\nTall (12oz)\nGrande (16oz)\nVenti (24oz)\n>')).lower()
        if in_size == 'short':
            size = 0
        elif in_size == 'tall':
            size = 1
        elif in_size == 'grande':
            size = 2
        elif in_size == 'venti':
            size = 3
        else:
            print('Size input invalid.  Please enter name of size only.')
    print("Please list the steps for drink creation.\n"
          "Enter in format '2 shots', '3 pumps vanilla', 'pour milk steamed to top'")
    done = False
    drink_steps = []
    while not done:
        step_input = input(">")
        if step_input == 'done':
            done = True
            continue
        step = drinkStep(step_input)
        if step.error:
            print("Incorrect format.")
        else:
            drink_steps.append(step)
    final_drink = drink(drink_steps, size)
    final_output = final_drink.get_cup_marking()
    best_match = None
    best_score = -1
    for recipe_obj in drinks:
        #print('Trying {}...'.format(recipe_obj.name))
        score = recipe_obj.is_modified(final_drink)
        if score != -1:
            #print("MATCH: Drink is a modified {} with a score of {}".format(recipe_obj.name, str(score)))
            if score < best_score or best_score == -1:
                best_match = recipe_obj
        #else:
            #print("No match.")

    if not best_match is None:
        final_output = best_match.get_cup_marking(size, final_drink.steps)

    for recipe_obj in drinks:
        if recipe_obj.is_identical(final_drink):
            #print("MATCH: Drink is identical to {}".format(recipe_obj.name))
            final_output = recipe_obj.get_cup_marking(size, final_drink.steps)
            break
    print(final_output)
    return input("Press enter to continue, or type 'exit' to finish.").lower().replace("'", '') == 'exit'


def load_simple_drinks():
    global drinks

    #coffee
    print('Creating coffee.')
    drinks.append(create_recipe({0: ['pour coffee to top'],
                                1: ['pour coffee to top'],
                                2: ['pour coffee to top'],
                                3: ['pour coffee to top'],
                                4: ['pour coffee to top']}, 'coffee', 'PPR', True))
    drinks.append(create_recipe({0: ['pour coffee light to top'],
                                1: ['pour coffee light to top'],
                                2: ['pour coffee light to top'],
                                3: ['pour coffee light to top'],
                                4: ['pour coffee light to top']}, 'light roast coffee', 'BLOND', True))
    drinks.append(create_recipe({0: ['pour coffee dark to top'],
                                1: ['pour coffee dark to top'],
                                2: ['pour coffee dark to top'],
                                3: ['pour coffee dark to top'],
                                4: ['pour coffee dark to top']}, 'dark roast coffee', 'BOLD', True))

    #latte
    print('Creating latte.')
    drinks.append(create_recipe({0: ['1 shot', 'pour milk steamed to top'],
                                1: ['1 shot', 'pour milk steamed to top'],
                                2: ['2 shot', 'pour milk steamed to top'],
                                3: ['2 shot', 'pour milk steamed to top'],
                                4: ['3 shot', 'pour milk steamed to top']}, 'latte', 'L', True))

    # chai
    print('Creating chai.')
    drinks.append(create_recipe({0: ['2 pump chai', 'pour milk steamed to top', '1 shot'],
                                 1: ['3 pump chai', 'pour milk steamed to top', '1 shot'],
                                 2: ['4 pump chai', 'pour milk steamed to top', '2 shot'],
                                 3: ['5 pump chai', 'pour milk steamed to top', '2 shot'],
                                 4: ['6 pump chai', 'pour milk steamed to top', '3 shot']}, 'chai',
                                'CH', True))

    #macchiato
    print('Creating macchiato.')
    drinks.append(create_recipe({0: ['pour milk steamed to top', '1 shot'],
                                1: ['pour milk steamed to top', '1 shot'],
                                2: ['pour milk steamed to top', '2 shot'],
                                3: ['pour milk steamed to top', '2 shot'],
                                4: ['pour milk steamed to top', '3 shot']}, 'macchiato', 'LM', True))
    drinks.append(create_recipe({0: ['1 pump vanilla', 'pour milk steamed to top', '1 shot'],
                                1: ['2 pump vanilla', 'pour milk steamed to top', '1 shot'],
                                2: ['3 pump vanilla', 'pour milk steamed to top', '2 shot'],
                                3: ['4 pump vanilla', 'pour milk steamed to top', '2 shot'],
                                4: ['5 pump vanilla', 'pour milk steamed to top', '3 shot']}, 'caramel macchiato', 'CM', True))

    # mocha
    print('Creating mocha.')
    drinks.append(create_recipe({0: ['2 pump mocha', '1 shot', 'pour milk steamed to top'],
                                 1: ['3 pump mocha', '1 shot', 'pour milk steamed to top'],
                                 2: ['4 pump mocha', '2 shot', 'pour milk steamed to top'],
                                 3: ['5 pump mocha', '2 shot', 'pour milk steamed to top'],
                                 4: ['6 pump mocha', '3 shot', 'pour milk steamed to top']}, 'mocha', 'M', True))
    drinks.append(create_recipe({0: ['2 pump whitemocha', '1 shot', 'pour milk steamed to top'],
                                 1: ['3 pump whitemocha', '1 shot', 'pour milk steamed to top'],
                                 2: ['4 pump whitemocha', '2 shot', 'pour milk steamed to top'],
                                 3: ['5 pump whitemocha', '2 shot', 'pour milk steamed to top'],
                                 4: ['6 pump whitemocha', '3 shot', 'pour milk steamed to top']}, 'white mocha', 'WM', True))

    # pumpkin spice latte
    print('Creating seasonals.')
    drinks.append(create_recipe({0: ['2 pump pumpkinspice', '1 shot', 'pour milk steamed to top'],
                                 1: ['3 pump pumpkinspice', '1 shot', 'pour milk steamed to top'],
                                 2: ['4 pump pumpkinspice', '2 shot', 'pour milk steamed to top'],
                                 3: ['5 pump pumpkinspice', '2 shot', 'pour milk steamed to top'],
                                 4: ['6 pump pumpkinspice', '3 shot', 'pour milk steamed to top']}, 'pumpkin spice latte', 'PSL', True))
    drinks.append(create_recipe({0: ['2 pump maplepecan', '1 shot', 'pour milk steamed to top'],
                                 1: ['3 pump maplepecan', '1 shot', 'pour milk steamed to top'],
                                 2: ['4 pump maplepecan', '2 shot', 'pour milk steamed to top'],
                                 3: ['5 pump maplepecan', '2 shot', 'pour milk steamed to top'],
                                 4: ['6 pump maplepecan', '3 shot', 'pour milk steamed to top']},
                                'maple pecan latte', 'MPL', True))

    load_drinks_to_db()
    print("DRINKS IN DATABASE: {}".format(get_drink_names()))
    print(get_drink_recipe('Latte','Tall'))
    close()

    print("RUNNING TESTS:")
    print("type(Latte.drink(2)): " + str(type(drinks[3].drink(2))))
    print("Latte = Latte: " + str(drinks[3].is_identical(drinks[3].drink(2))))
    print("Latte = 2 shots + steamed milk: " + str(drinks[3].drink(2).is_identical(create_drink(['2 shot', 'pour milk steamed to top']))))
    print("Latte = Coffee: " + str(drinks[3].is_identical(drinks[0])))
    print("Coffee = Macchiato: " + str(str(drinks[0].is_identical(drinks[4].drink(2)))))

def parse_drinks_to_list():
    for drink_tuple in get_drink_names():
        drink_name = drink_tuple[0]
        drink_abbreviation = get_drink_abbreviation(drink_name)
        steps = {}
        steps[0] = get_drink_recipe(drink_name, 'Short')
        steps[1] = get_drink_recipe(drink_name, 'Tall')
        steps[2] = get_drink_recipe(drink_name, 'Grande')
        steps[3] = get_drink_recipe(drink_name, 'Venti')
        drink_obj = create_recipe(steps, drink_name, drink_abbreviation)
        drinks.append(drink_obj)


def load_drinks_to_db():
    add_recipe('Latte', 'L', {0: ['1 shot', 'pour milk steamed to top'],
                              1: ['1 shot', 'pour milk steamed to top'],
                              2: ['2 shot', 'pour milk steamed to top'],
                              3: ['2 shot', 'pour milk steamed to top']
                              }
               )
    add_recipe('Mocha', 'M', {0: ['2 pump mocha', '1 shot', 'pour milk steamed to top'],
                              1: ['3 pump mocha', '1 shot', 'pour milk steamed to top'],
                              2: ['4 pump mocha', '2 shot', 'pour milk steamed to top'],
                              3: ['5 pump mocha', '2 shot', 'pour milk steamed to top']
                              }
               )
    add_recipe('White Mocha', 'WM', {0: ['2 pump whitemocha', '1 shot', 'pour milk steamed to top'],
                                     1: ['3 pump whitemocha', '1 shot', 'pour milk steamed to top'],
                                     2: ['4 pump whitemocha', '2 shot', 'pour milk steamed to top'],
                                     3: ['5 pump whitemocha', '2 shot', 'pour milk steamed to top']
                                     }
               )
    add_recipe('Macchiato', 'LM', {0: ['pour milk steamed to top', '1 shot'],
                              1: ['pour milk steamed to top', '1 shot'],
                              2: ['pour milk steamed to top', '2 shot'],
                              3: ['pour milk steamed to top', '2 shot'],
                              }
               )
    add_recipe('Caramel Macchiato', 'CM', {0: ['1 pump vanilla', 'pour milk steamed to top', '1 shot'],
                                   1: ['2 pump vanilla', 'pour milk steamed to top', '1 shot'],
                                   2: ['3 pump vanilla', 'pour milk steamed to top', '2 shot'],
                                   3: ['4 pump vanilla', 'pour milk steamed to top', '2 shot'],
                                   }
               )
    add_recipe('Coffee', 'PPR', {0: ['pour coffee medium to top'],
                                 1: ['pour coffee medium to top'],
                                 2: ['pour coffee medium to top'],
                                 3: ['pour coffee medium to top']
                              }
               )
    add_recipe('Light Roast Coffee', 'BLND', {0: ['pour coffee light to top'],
                                 1: ['pour coffee light to top'],
                                 2: ['pour coffee light to top'],
                                 3: ['pour coffee light to top']
                                 }
               )
    add_recipe('Dark Roast Coffee', 'BOLD', {0: ['pour coffee dark to top'],
                                              1: ['pour coffee dark to top'],
                                              2: ['pour coffee dark to top'],
                                              3: ['pour coffee dark to top']
                                              }
               )
    add_recipe('Decaf Coffee', 'Dcf', {0: ['pour coffee decaf to top'],
                                             1: ['pour coffee decaf to top'],
                                             2: ['pour coffee decaf to top'],
                                             3: ['pour coffee decaf to top']
                                             }
               )
    add_recipe('Pumpkin Spice Latte', 'PSL', {0: ['2 pump pumpkinspice', '1 shot', 'pour milk steamed to top'],
                              1: ['3 pump pumpkinspice', '1 shot', 'pour milk steamed to top'],
                              2: ['4 pump pumpkinspice', '2 shot', 'pour milk steamed to top'],
                              3: ['5 pump pumpkinspice', '2 shot', 'pour milk steamed to top']
                              }
               )
    add_recipe('Maple Pecan Latte', 'MPL', {0: ['2 pump maplepecan', '1 shot', 'pour milk steamed to top'],
                                              1: ['3 pump maplepecan', '1 shot', 'pour milk steamed to top'],
                                              2: ['4 pump maplepecan', '2 shot', 'pour milk steamed to top'],
                                              3: ['5 pump maplepecan', '2 shot', 'pour milk steamed to top']
                                              }
               )
    add_recipe('Salted Caramel Mocha', 'SCM', {0: ['2 pump toffeenut', '2 pump mocha', '1 shot', 'pour milk steamed to top'],
                                              1: ['3 pump toffeenut', '3 pump mocha', '1 shot', 'pour milk steamed to top'],
                                              2: ['4 pump toffeenut', '4 pump mocha', '2 shot', 'pour milk steamed to top'],
                                              3: ['5 pump toffeenut', '5 pump mocha', '2 shot', 'pour milk steamed to top']
                                              }
               )
    add_recipe('Chai Tea Latte', 'CH', {0: ['2 pump chai', '1 shot', 'pour milk steamed to top'],
                              1: ['3 pump chai', '1 shot', 'pour milk steamed to top'],
                              2: ['4 pump chai', '2 shot', 'pour milk steamed to top'],
                              3: ['5 pump chai', '2 shot', 'pour milk steamed to top']
                              }
               )
    add_recipe('Lightly Sweet Chai Tea Latte', 'LSCH', {0: ['2 pump lschai', '1 shot', 'pour milk steamed to top'],
                              1: ['3 pump lschai', '1 shot', 'pour milk steamed to top'],
                              2: ['4 pump lschai', '2 shot', 'pour milk steamed to top'],
                              3: ['5 pump lschai', '2 shot', 'pour milk steamed to top']
                              }
               )


def create_recipe(steps, name='unnamed drink', abbreviation='', predefined=False):
    drink_steps = {}
    for size in steps:
        drink_steps[size] = []
        for step in range(len(steps[size])):
            step_obj = drinkStep(steps[size][step])
            if step_obj.error:
                print("Drink error in {}!".format(name))
                return
            else:
                drink_steps[size].append(step_obj)
    out_drink = Recipe(drink_steps)
    out_drink.name = name
    out_drink.abbreviation = abbreviation
    return out_drink


def create_drink(steps):
    drink_steps = []
    for step in steps:
        step_obj = drinkStep(step)
        if step_obj.error:
            print("Drink error!")
            return
        else:
            drink_steps.append(step_obj)
    out_drink = drink(drink_steps)
    return out_drink


if __name__ == '__main__':
    main()
