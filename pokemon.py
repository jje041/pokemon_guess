MAX_STR_LEN = 7

class Pokemon:
    """
    A class for representing Pokémon.

    Attributes:
    ----------

    name : str
        The name of the Pokémon.

    dex_number : int
        The associated Pokédex entry number.

    gen : int
        The generation the Pokémon belongs to.

    type1 : str
        The first type the Pokémon has, can be 18 different types.

    type2 : str
        The second type the Pokémon has, can be empty.

    Methods:
    --------
    setColorToGeneration(self) -> str
        Method to set the color of the generation the Pokémon belongs to.
    """

    def __init__(self, name: str, dex_number: int, gen: int, type1: str, type2="") -> None:
        """Initializer for the Pokémon class. The initializer will verify the input arguments.

        Parameters
        ----------
        name : str
            The name of the Pokémon, should start with a capital letter.
        dex_number : int
            The Pokédex number for the Pokémon.
        gen : int
            The generation the Pokémon belongs to. 
        type1 : str
            The primary type for the Pokémon. 
        type2 : str
            The secondary type for the Pokémon, empty string if no second type is provided
        """

        # check that the inputs are of the correct type
        assert type(name) == str,'Invalid name'
        assert type(dex_number) == int and dex_number > 0,'Invalid dex number'
        assert type(gen) == int and 1 <= gen <= 9,'Invalid generation'
        assert type(type1) == str,'Invalid type 1'
        assert type(type2) == str,'Invalid type 2'

        # set attributes
        self.dex_number = dex_number
        self.name = name
        self.gen = gen
        self.type1 = type1
        self.type2 = type2

    def __str__(self) -> str:
        """Used to print the Pokémon objects, called when print method is used on an object of the Pokémon class.

        Returns
        -------
        str
            Formatted Pokémon information. 
        """

        return self.genColoredID() + '\t\t' + self.name + ('\t\t' if len(self.name) > MAX_STR_LEN else '\t\t\t') + self.types()

    def types (self) -> str:
        return type_color(self.type1) + ('\t' if len(self.type1) > MAX_STR_LEN else '\t\t') + type_color(self.type2)


    def genColoredID(self) -> str:
        """Method to color the Pokémon's dex number based on which generation they are in.

        Returns
        -------
        str
            Colored version of the national dex number as a string.
        """

        return f'{gen_colors[self.gen]}{self.dex_number}\x1b[0;0m'

# dictionary of colors, one for each generation
gen_colors = {
    1: "\x1b[38;5;1m",        # the values corresponding to each key
    2: "\x1b[38;5;87m",       # makes the text in the terminal
    3: "\x1b[38;5;40m",       # a different color depending on the generation
    4: "\x1b[38;5;69m",
    5: "\x1b[38;5;246m",
    6: "\x1b[38;5;126m",
    7: "\x1b[38;5;208m",
    8: "\x1b[38;5;200m",
    9: "\x1b[38;5;92m"
}

TYPE_COLORS = {
    # there are a total of 18 types in Pokémon
    'Dark': 239,
    'Fire': 202,
    'Psychic': 200,
    'Water': 26,
    'Normal': 222,
    'Fairy': 213,
    'Grass': 34,
    'Ice': 44,
    'Ghost': 92,
    'Bug': 106,
    'Ground': 3,
    'Electric': 226,
    'Fighting': 52,
    'Flying': 122,
    'Rock': 95,
    'Dragon': 57,
    'Poison': 90,
    'Steel': 103,
}

def type_color (type: str, text: str = None) -> str:
    if text is None:
        text = type

    if type == '':
        return text

    if type in TYPE_COLORS.keys():
        return f'\x1b[38;5;{TYPE_COLORS[type]}m{text}\x1b[0;0m'
    
    raise ValueError()