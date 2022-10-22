class Pokemon:
    """
    A class for representing Pokémon 


    Attributes:
    ----------

    name : str
        the name of the Pokémon

    dex_number : int
        the associated Pokédex entry number

    gen : int
        the generation the Pokémon belongs to

    type1 : str
        the first type the Pokémon has, can be 18 different types

    type2 : str
        the second type the Pokémon has, can be empty

    Methods:
    --------
    setColorToGeneration(self) -> str
        method to set the color of the generation the Pokémon belongs to
        
    """

    def __init__(self, name: str, dex_number: int, gen: int, type1: str, type2: str) -> None:
        """Constructor for the Pokémon class; will verify the correctness of the input """

        # check that the inputs are of the correct type
        assert(type(name) == str),'Invalid name'
        assert(type(dex_number) == int and dex_number > 0),'Invalid dex number'
        assert(type(gen) == int and 1 <= gen <= 8),'Invalid generation'
        assert(type(type1) == str),'Invalid type 1'
        assert(type(type2) == str),'Invalid type 2'

        # set attributes
        self.dex_number = dex_number
        self.name = name
        self.gen = gen
        self.type1 = type1
        self.type2 = type2

        # used to format output when the objects are printed
        self.max_string_length = 7

    def __str__(self) -> str:
        """Used to print the Pokémon objects, called when print method is used on an object of the Pokémon class """

        # this function is called to print the Pokémon in the terminal, here different methods are used to obtain color of the text
        # how many tabs are used is dependent upon the length of the Pokémon name and the first Pokémon type
        if len(self.name) <= self.max_string_length:
            # if the string is 7 we use three tabs, if not use two tabs to separate name and type1
            if len(self.type1) <= self.max_string_length:
                # if the type length is less than or equal to 7 print using two tabs
                return f"{self.setColorOfGeneration()}\t\t{self.name}\t\t\t{self.__colorType(self.type1)}\t\t{self.__colorType(self.type2)}"
            else:
                # otherwise, use only one tab
                return f"{self.setColorOfGeneration()}\t\t{self.name}\t\t\t{self.__colorType(self.type1)}\t{self.__colorType(self.type2)}"
        else:
            # if the Pokémon name length is greater than 7 we only need two tabs
            if len(self.type1) <= self.max_string_length:
                return f"{self.setColorOfGeneration()}\t\t{self.name}\t\t{self.__colorType(self.type1)}\t\t{self.__colorType(self.type2)}"
            else:
                # same handling as the previous statement
                return f"{self.setColorOfGeneration()}\t\t{self.name}\t\t{self.__colorType(self.type1)}\t{self.__colorType(self.type2)}"

    def setColorOfGeneration(self) -> str:
        """Method to color the Pokémon's dex number based on which generation they are in
        
        Parameters:
        ----------
        
        Returns:
        --------
        str
            string that is the colored version of the generation number

        """

        # dictionary of colors, one for each generation
        colors = {'p1' : "\x1b[38;5;1m",        # the values corresponding to each key;
                  'p2' : "\x1b[38;5;87m",       # makes the text in the terminal;
                  'p3' : "\x1b[38;5;40m",       # a different color depending on the generation
                  'p4' : "\x1b[38;5;69m",
                  'p5' : "\x1b[38;5;246m",
                  'p6' : "\x1b[38;5;126m",
                  'p7' : "\x1b[38;5;208m",
                  'p8' : "\x1b[38;5;200m"}

        # check which generation the Pokémon is in to determine the generation
        match self.gen:
            # create the complete string used to print the colors and return it
            case 1:
                return f"{colors['p1']}{str(self.dex_number)}\x1b[0;0m"
            case 2:
                return f"{colors['p2']}{str(self.dex_number)}\x1b[0;0m"
            case 3:
                return f"{colors['p3']}{str(self.dex_number)}\x1b[0;0m"
            case 4:
                return f"{colors['p4']}{str(self.dex_number)}\x1b[0;0m"
            case 5:
                return f"{colors['p5']}{str(self.dex_number)}\x1b[0;0m"
            case 6:
                return f"{colors['p6']}{str(self.dex_number)}\x1b[0;0m"
            case 7:
                return f"{colors['p7']}{str(self.dex_number)}\x1b[0;0m"
            case 8:
                return f"{colors['p8']}{str(self.dex_number)}\x1b[0;0m"
            case _:
                return f"Invalid generation: {self.gen}"

    def __colorType(self, pokemon_type: str) -> dict[str,str]:
        """Method to color the different types 
        
        Parameters:
        -----------

        pokemon_type: str
            the type to color

        Returns:
        --------
            A dictionary with the associated as the key and the colored string with the type as the value
        """

        # there are a total of 18 types in Pokémon
        color = {
            "Dark" : "\x1b[38;5;239mDark\x1b[0;0m", 
            "Fire" : "\x1b[38;5;202mFire\x1b[0;0m",
            "Psychic" : "\x1b[38;5;200mPsychic\x1b[0;0m",
            "Water" : "\x1b[38;5;26mWater\x1b[0;0m",
            "Normal" : "\x1b[38;5;222mNormal\x1b[0;0m",
            "Fairy" : "\x1b[38;5;213mFairy\x1b[0;0m",
            "Grass" : "\x1b[38;5;34mGrass\x1b[0;0m",
            "Ice" : "\x1b[38;5;44mIce\x1b[0;0m",
            "Ghost" : "\x1b[38;5;92mGhost\x1b[0;0m",
            "Bug" : "\x1b[38;5;106mBug\x1b[0;0m",
            "Ground" : "\x1b[38;5;3mGround\x1b[0;0m",
            "Electric" : "\x1b[38;5;226mElectric\x1b[0;0m",
            "Fighting" : "\x1b[38;5;52mFighting\x1b[0;0m",
            "Flying" : "\x1b[38;5;122mFlying\x1b[0;0m",
            "Rock" : "\x1b[38;5;95mRock\x1b[0;0m",
            "Dragon" : "\x1b[38;5;57mDragon\x1b[0;0m",
            "Poison" : "\x1b[38;5;90mPoison\x1b[0;0m",
            "Steel" : "\x1b[38;5;103mSteel\x1b[0;0m",
        "" : ""} # <- added an empty string in case the second type is empty

        # check if the type is valid
        try:
            color[pokemon_type]
        except KeyError:
            return f"Invalid type encountered! {pokemon_type} is not a valid type."
    
        # return the correct type
        return color[pokemon_type]

def perform_test():
    pokemon1 = Pokemon("Pikachu",25,1,"Electric","")
    pokemon2 = Pokemon("Chandelure",609,5,"Ghost","Fire")
    pokemon3 = Pokemon("Hoppip",187,2,"Grass","Electric")
    # pokemon4 = Pokemon("",0,-1,"","Not a type")           # will be stopped by the assert

    pokemon1.setColorOfGeneration()


if __name__ == "__main__":
    perform_test()

    