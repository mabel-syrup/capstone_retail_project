

flavors = {
    'vanilla': 'V',
    'sfvanilla': 'SFV',
    'caramel': 'C',
    'cinnamondolce': 'CD',
    'hazelnut': 'H',
    'toffeenut': 'TN',
    'classic': 'Cl',
    'sfcinnamondolce': 'SFCD',
    'peppermint': 'Ppm',
    'raspberry': 'R',
    'mocha': 'M',
    'whitemocha': 'WM',
    'pumpkinspice': 'PS',
    'chai': 'CH',
    'lschai': 'LSCH',
    'maplepecan': 'MP'
}

milks = {
    '2%': '2%',
    'skim': 'N',
    'whole': 'W',
    'breve': 'H+H',
    'half&half': 'H+H',
    'cocnut': 'Co',
    'soy': 'S',
    'almond': 'A'
}

sizes = {
    0: 'Short',
    1: 'Tall',
    2: 'Grande',
    3: 'Venti'
}


class drinkStep:

    amount = 0
    shot = False
    pump = False
    decaf = False
    flavor = ''
    milk = False
    hot = False
    coffee = False
    inclusion = False
    pour_to = 0
    #1: Bottom Line
    #2: Middle Line
    #3: Top Line
    #4: Middle
    #5: Top

    error = False

    raw_step_string = ''

    def __init__(self, step):
        self.parse_step(step)
        self.raw_step_string = step

    def similar(self, other):
        equal = True
        if other.shot != self.shot:
            equal = False
        if other.pump != self.pump:
            equal = False
        if other.milk != self.milk:
            equal = False
        if other.hot != self.hot:
            equal = False
        if other.coffee != self.coffee:
            equal = False
        if other.inclusion != self.inclusion:
            equal = False
        return equal

    def equals(self, other):
        equal = True
        if not self.similar(other):
            equal = False
        if other.amount != self.amount:
            equal = False
        if other.decaf != self.decaf:
            equal = False
        if other.flavor != self.flavor:
            equal = False
        if other.pour_to != self.pour_to:
            equal = False
        return equal


    def parse_step(self, step):
        instruction = step.lower().split(' ')
        if instruction[0].isdigit():
            self.parse_counted(instruction)
        elif instruction[0] == 'pour':
            self.parse_pour(instruction)

    #[number] [ingredient] ([flavor])
    def parse_counted(self, instruction):
        self.amount = int(instruction[0])
        i_type = instruction[1]
        if i_type[:4] == 'shot':
            self.shot = True
            if len(instruction) > 2 and instruction[2] == 'decaf':
                self.decaf = True
        elif i_type[:4] == 'pump':
            self.pump = True
            if len(instruction) < 3:
                self.error = True
                return
            else:
                self.flavor = instruction[2]
        elif i_type[:5] == 'scoop':
            self.inclusion = True
            if len(instruction) < 3:
                self.error = True
                return
            else:
                self.flavor = instruction[2]

    #pour [drink] ([drink_b]) to [height]
    def parse_pour(self,step):
        height_remainder = []
        if len(step) < 4:
            self.error = True
            return
        if step[1] == 'milk':
            self.milk = True
            if step[2] == 'steamed':
                self.hot = True
                if step[3] == 'to':
                    self.flavor = '2%'
                    height_remainder = step[3:]
                else:
                    self.flavor = step[3]
                    height_remainder = step[4:]
            else:
                if step[2] == 'to':
                    self.flavor = '2%'
                    height_remainder = step[2:]
                else:
                    self.flavor = step[2]
                    height_remainder = step[3:]
        elif step[1] == 'coffee':
            self.coffee = True
            if step[2] == 'light' or step[2][:5] == 'blond':
                self.flavor = 'light'
            elif step[2] == 'dark' or step[2] == 'bold':
                self.flavor = 'dark'
            elif step[2] == 'decaf':
                self.flavor = 'decaf'
                self.decaf = True
            elif step[2] == 'medium' or step[2][:4] == 'pike' or step[2] == 'to':
                self.flavor = 'medium'
            if step[2] == 'to':
                height_remainder = step[2:]
            else:
                height_remainder = step[3:]
        if len(height_remainder) == 0:
            self.error = True
        level = height_remainder[1]
        if len(height_remainder) == 2:
            if level[:3] == 'mid':
                self.pour_to = 4
            elif level == 'top':
                self.pour_to = 5
        else:
            if level[:3] == 'low' or level[:3] == 'bot':
                self.pour_to = 1
            elif level[:3] == 'mid':
                self.pour_to = 2
            elif level == 'top' or level[0] == 'h':
                self.pour_to = 3
            else:
                self.error = True


class drink:

    name = ''
    abbreviation = ''
    steps = []
    is_predefined = False
    size = 1
    # 0: Short
    # 1: Tall
    # 2: Grande
    # 3: Venti
    # 4: Trenta

    def __init__(self, in_steps, in_size=0, predefined=False):
        self.steps = in_steps
        self.size = in_size
        self.is_predefined = predefined

    def get_cup_marking(self):
        if self.is_predefined:
            return '{}\n[ ]\n[ ]\n[ ]\n[ ]\n[{}]'.format(self.name.upper(), self.abbreviation)
        decaf = ' '
        shots = 0
        milk = ' '
        flavor = ' '
        is_decaf = True
        for step in self.steps:
            if step.shot:
                shots = step.amount
                if not step.decaf:
                    is_decaf = False
            elif step.pump:
                flavor = '{}{}'.format(step.amount, step.flavor)
            elif step.coffee and step.flavor != 'decaf':
                is_decaf = False
        if is_decaf:
            decaf = 'X'
        if shots == 0:
            shots = ' '
        return 'Decaf\n[{}]\nShots\n[{}]\nSyrup\n[{}]\nMilk\n[{}]\nCustom\n[{}]\nDrink\n[{}]'.format(decaf, shots, flavor, milk, ' ', ' ')

    def print_raw_steps(self):
        print("DRINK: " + self.name)
        for step in self.steps:
            print(step.raw_step_string)

    def is_identical(self, second_drink):
        if len(self.steps) != len(second_drink.steps):
            return False
        for i in range(len(self.steps)):
            if not self.steps[i].equals(second_drink.steps[i]):
                return False
        else:
            return True


class Recipe:

    name = ''
    abbreviation = ''
    steps = {}

    def __init__(self, in_steps):
        self.steps = in_steps
        #print("Recipe steps: {} (should be dict)".format(type(self.steps)))

    def is_identical(self, second_drink):
        if type(second_drink) == drink:
            comp_size = second_drink.size
            second_steps = second_drink.steps
        else:
            comp_size = 2
            second_steps = second_drink.steps[comp_size]
        comp_steps = self.steps[comp_size]
        if len(comp_steps) != len(second_steps):
            return False
        for i in range(len(comp_steps)):
            if not comp_steps[i].equals(second_steps[i]):
                return False
        else:
            return True

    def is_modified(self, second_drink):
        this_steps = self.steps[second_drink.size]
        #print("Steps is {} of {}".format(str(type(self.steps)), str(type(this_steps))))
        this_steps_cropped = []
        second_steps = []

        flavors_difference = 0
        flavors_original = []
        flavors_new = []

        for step in second_drink.steps:
            if not step.pump:
                second_steps.append(step)
            else:
                if step.flavor not in flavors_new:
                    for i in range(step.amount):
                        flavors_new.append(step.flavor)

        for step in this_steps:
            if not step.pump:
                this_steps_cropped.append(step)

        if len(second_steps) != len(this_steps_cropped):
            return -1

        for i in range(len(second_steps)):
            if not this_steps_cropped[i].similar(second_steps[i]):
                return -1

        for step in this_steps:
            if step.pump:
                if step.flavor not in flavors_original:
                    flavors_original.append(step.flavor)

        for flavor in flavors_original:
            if flavor not in flavors_new:
                #print('{} not present.'.format(flavor))
                return -1

        for flavor in flavors_new:
            if flavor not in flavors_original:
                flavors_difference += 1

        return flavors_difference


    def drink(self, size):
        drink_steps = self.steps[size]
        out_drink = drink(drink_steps, size)
        out_drink.name = self.name
        out_drink.abbreviation = self.abbreviation
        return out_drink

    def get_cup_marking(self, size, steps=None):
        if steps is None:
            steps = self.steps[size]
        decaf = ' '
        shots_difference = ' '
        flavor_difference = ' '
        milk_difference = ' '
        custom_difference = ' '

        this_shots = 0
        this_flavor = {}
        this_milk = ' '
        this_custom = ''

        comp_shots = 0
        comp_flavor = {}
        comp_decaf = True
        comp_milk = ' '


        for step in self.steps[size]:
            if step.shot:
                this_shots += step.amount
            elif step.pump:
                this_flavor[step.flavor] = step.amount
            elif step.milk:
                this_milk = step.flavor

        for step in steps:
            if step.shot:
                comp_shots += step.amount
                if not step.decaf:
                    comp_decaf = False
            elif step.pump:
                comp_flavor[step.flavor] = step.amount
            elif step.coffee and step.flavor != 'decaf':
                comp_decaf = False
            elif step.milk:
                comp_milk = step.flavor

        if comp_decaf:
            decaf = 'X'

        if this_shots != comp_shots:
            shots_difference = str(comp_shots)
        if this_milk != comp_milk:
            milk_difference = try_get_milk_abbreviation(comp_milk)
        for flavor in comp_flavor:
            if flavor not in this_flavor:
                flavor_difference += '{} {} '.format(comp_flavor[flavor], try_get_flavor_abbreviation(flavor))
            elif this_flavor[flavor] != comp_flavor[flavor]:
                flavor_difference += '{} {} '.format(comp_flavor[flavor], try_get_flavor_abbreviation(flavor))

        description = '{} {} {}'.format('Hot', sizes[size], self.name)


        return 'Decaf\n[{}]\nShots\n[{}]\nSyrup\n[{}]\nMilk\n[{}]\nCustom\n[{}]\nDrink\n[{}]\n{}'\
            .format(decaf, shots_difference, flavor_difference, milk_difference, ' ', self.abbreviation, description)

def try_get_flavor_abbreviation(in_flavor):
    flavor = in_flavor.lower()
    if flavor not in flavors:
        return flavor
    return flavors[flavor]

def try_get_milk_abbreviation(in_milk):
    milk = in_milk.lower()
    if milk not in milks:
        return milk
    return milks[milk]