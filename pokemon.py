# Pokémon class, used to store the information for each Pokémon
class Pokemon:
    def __init__(self,name,dex_number,gen,type1,type2):
        # error checks
        assert(type(name)==str),'Invalid name'
        assert(type(dex_number)==int),'Invalid dex number'
        assert(type(gen)==int),'Invalid generation'
        assert(type(type1)==str),'Invalid type 1'

        self.name = name
        self.dex_number = dex_number
        self.gen = gen
        self.type1 = type1
        self.type2 = type2

    # print method for the class 
    def __str__(self):
        return f"Name: {self.name}\tDex: {self.dex_number}\tType1: {self.type1}\tType2: {self.type2}"

# list of all Pokémon types
valid_types = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel',
'Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy']

def parse_guess(guess):
    """Parses the guess and converts to uppercase on the first letter, if needed"""
    '''Returns the guess, parsed with an uppercase first letter'''
    first_letter = guess[0] # get the first letter

    if first_letter.islower(): # if the first letter is lowercase
        # change it to uppercase
        guess = guess.capitalize()

    return guess

def is_valid_type(guess):
    guess = parse_guess(guess)

    # goes through the list of valid types to check if it is there
    for tmp in valid_types:
        if tmp == guess:
            return 1

    return 0






