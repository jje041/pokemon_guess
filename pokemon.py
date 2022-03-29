class Pokemon:
    ''' A class for storing Pokémon data 
    
    Attributes:
        (Name: dex_number; Type: int)
        Description: A Pokémon's associated Pokédex number

        (Name: name; Type: str)
        Description: Name of the Pokémon

        (Name: gen; Type: int)
        Description: which generation the Pokémon belongs to

        (Name: type1; Type: str)
        Description: first type of the Pokémon

        (Name: type2; Type: str)
        Description: secoond type, may be empty    

    Methods:
        __init__
            return Pokémon object

        __str__
            return str

        setColorToGeneration
            return str 
        
        __colorType
            return str
    '''

    def __init__(self,name,dex_number,gen,type1,type2):
        ''' constructor for the Pokémon class '''

        # check that the inputs are of the correct type
        assert(type(name)==str),'Invalid name'
        assert(type(dex_number)==int),'Invalid dex number'
        assert(type(gen)==int),'Invalid generation'
        assert(type(type1)==str),'Invalid type 1'
        assert(type(type2)==str),'Invalid type 1'

        # set attributes
        self.dex_number = dex_number
        self.name = name
        self.gen = gen
        self.type1 = type1
        self.type2 = type2

        # used to format output when the objects are printed
        self.max_string_length = 7

    def __str__(self):
        ''' used to print the Pokémon objects '''

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

    def setColorOfGeneration(self):
        ''' method to color the Pokémon's dex number based on which generation they are in '''

        # dictionary of colors, one for each generation
        colors = {'p1' : "\x1b[38;5;1m",        # the values corresponding to each key
                  'p2' : "\x1b[38;5;87m",       # makes the text in the terminal 
                  'p3' : "\x1b[38;5;40m",       # a different color depending on the generation
                  'p4' : "\x1b[38;5;69m",
                  'p5' : "\x1b[38;5;246m",
                  'p6' : "\x1b[38;5;126m",
                  'p7' : "\x1b[38;5;208m",
                  'p8' : "\x1b[38;5;200m",}

        if self.gen == 1:
            # create the complete string used to print the colors and return it
            return colors['p1'] + str(self.dex_number) + "\x1b[0;0m"
        elif self.gen == 2:
            return colors['p2'] + str(self.dex_number) + "\x1b[0;0m"
        elif self.gen == 3:
            return colors['p3'] + str(self.dex_number) + "\x1b[0;0m"
        elif self.gen == 4:
            return colors['p4'] + str(self.dex_number) + "\x1b[0;0m"
        elif self.gen == 5:
            return colors['p5'] + str(self.dex_number) + "\x1b[0;0m"
        elif self.gen == 6:
            return colors['p6'] + str(self.dex_number) + "\x1b[0;0m"
        elif self.gen == 7:
            return colors['p7'] + str(self.dex_number) + "\x1b[0;0m"
        elif self.gen == 8:
            return colors['p8'] + str(self.dex_number) + "\x1b[0;0m"
        else:
            pass

    def __colorType(self,pokemon_type):
        ''' method to color the different types 
        
        argument: pokemon_type, which is taken as a key to the color dictionary
        return: string to color the type        
        '''

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
        "" : ""} # added empty string in case a second type is empty

        return color[pokemon_type]