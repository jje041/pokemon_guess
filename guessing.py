import pokedex as dex
from pokemon import Pokemon
import config
import os
import sys
import time

MAX_GENERATIONS = 9

class GuessingGame:
    """A class for representing the main guessing game.

    Attributes
    ----------
    score : int
        The score, total number of correct guesses from the player. 

    generations : list[int]
        A list of the generations (as integers) the player want to use. 

    guessed : dict[int, Pokemon]
        A dictionary of the correct guesses the player has. 

    set_of_pokemon : dict[int, Pokemon]
        A dictionary with all the Pokémon in the game. 

    special_cases : list[str]
        Pokémon that have spaces in their names have to be treated a bit differently. 

    load : bool
        True of False if the game currently being played in a loaded game or not. 

    valid_types : list[str]
        A list with all the valid Pokémon types stored as strings. 
    """

    def __init__(self, score: int, special_cases: list[str], load: bool) -> None:
        """The initializer for the GuessingGame class.

        Parameters
        ----------
        score : int
            The score, total number of correct guesses from the player. 
        special_cases : list[str]
            Pokémon that have spaces in their names have to be treated a bit differently. 
        load : bool
            True of False if the game currently being played in a loaded game or not. 
        """

        self.score = score
        self.generations = []
        self.guessed: dict[int, Pokemon] = {}
        self.set_of_pokemon = {}
        self.special_cases = special_cases
        self.load = load

        self.valid_types = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel',
                            'Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy']

    def _create_saved_directory(self) -> None:
        """Used to create the saved directory 
        needed to save and load. 
        """

        # create a save directory if there no
        if not os.path.exists("saved"):
            os.mkdir("saved")
    
    def _determine_generations(self) -> None:
        """Method to determine the generations 
        the user would like to have in the game. It is
        okay if the arguments are entered out of order. 
        The method will sort the generations properly.
        """

        if len(sys.argv) > 10: 
            exit("Too many arguments, exiting.")

        if len(sys.argv) == 1:
            # if the user does not enter any generations, use all of them (1-9)
            self.generations = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            return

        # find the valid generations for the game
        valid_gens = [str(gen) for gen in range(1, MAX_GENERATIONS + 1)]

        # extract valid generations from the terminal input
        self.generations = [int(entry) for entry in sys.argv if entry in valid_gens]

        if not self.generations:
            self.end_game("generation fail")

        self.generations.sort()

    def _setup_dex(self) -> None:
        """Initialize the complete Pokédex using the generations the user wants, also setup the guessed dictionary.
        """

        # go through the Pokédex list
        for pokemon_entry in dex.Pokedex:
            # save name, dex number, generation and both types
            name, dex_number, gen, type1, type2 = pokemon_entry

            # if a Pokémon is in a generation that the user wants, add it to the dictionary of all the Pokémon
            if gen in self.generations:
                # also add guessed, but set name to '?'
                self.set_of_pokemon[dex_number] = Pokemon(name,dex_number,gen,type1,type2)
                self.guessed[dex_number]        = Pokemon('?',dex_number,gen,type1,type2)

    def _print_guessed(self, guess: str) -> None:
        """Function to help with printing Pokémon already guessed.
        Print the generation specified in the guess argument.

        Parameters
        ----------
        guess : str
            Generation the user wants to print.
        """

        # firstly, determine which generation to print
        match guess:
            case "p1":
                gen_range = [1,152]
            case "p2":
                gen_range = [152,252]
            case "p3":
                gen_range = [252,387]
            case "p4":
                gen_range = [387,494]
            case "p5":
                gen_range = [494,650]
            case "p6":
                gen_range = [650,722]
            case "p7":
                gen_range = [722,810]
            case "p8":
                gen_range = [810,906]
            case "p9":
                gen_range = [906,1009]
            case _:
                # print all the valid gens, using the generation to determine the color
                for key in self.set_of_pokemon:
                    print(f"{self.guessed[key].genColoredID()}\t\t{self.guessed[key].name}")
                return

        # to only print one generation, use the generation bounds as limits
        start, stop = gen_range

        # go through only one generation and print using the generation to determine the color
        for key in range(start,stop):
            try:
                print(f"{self.guessed[key].genColoredID()}\t\t{self.guessed[key].name}")
            except KeyError:
                pass

    def _progress(self) -> None:
        """Method to display a progress bar in the terminal.
        """

        # determine how many Pokémon remain
        remain = len(self.set_of_pokemon) - self.score

        # check if the user has only one correct guess
        if remain == len(self.set_of_pokemon) - 1:
            # if the user have only one correct guess, use singular instead of plural
            print(f"You have {self.score} correct guess, meaning there is {remain} left to guess.")
        else:
            print(f"You have {self.score} correct guesses, meaning there is {remain} left to guess.")

        # print a progress bar, showing the percentage of the progress
        progress = int(100*self.score/len(self.set_of_pokemon))
        for i in range(100):
            if i < progress: print(chr(9646),end='')
            else:            print(chr(9647),end='')

        print("")

    def _instructions(self) -> None:
        """Method to print instructions to the user. Function is called
        when 'h' or 'help' is typed in the terminal.
        """

        instructions = '''
                ==================== Instructions ====================
                The goal here is to guess every Pokémon in the Pokédex.
                Type the Pokémon name in the terminal and hit enter to make your guess. 
                The following commands are implemented to help in your journey:\n
                1.
                You can type 'p' to print the Pokédex. This will display the Pokémon you have entered.
                and the ones you are missing, these being displayed by a '?' symbol.
                Note that you must use a capital letter at the beginning of each name.
                Alternatively, you can use 'p1', 'p2', 'p3' and so on... to print only the generation behind p\n
                2.
                You can also write a Pokémon type. Either capitalized or not, i.e. you can type 'Fire' or 'fire'.
                This will print out all the guessed and not guessed Pokémon of that type. 
                In particular, not guessed Pokémon are marked with a '?' and correctly guessed Pokémon are shown with their name
                and corresponding PokéDex number.
                To help you out, the types are displayed if you use these commands.\n
                3.
                In the terminal you can enter the numbers between 1-8, or any combinations you desire, 
                you also type the commands in any order, like 3 2 1 is fine.
                Note that you have to separate the numbers with spaces, only!
                The game will then run with only the specified generations. All other commands work as before.
                However, typing p4 when generation 4 is excluded does not do anything.\n
                4.
                Typing 'r' will show the number of remaining Pokémon left and how many correct guesses you have.
                A progress bar showing the percentage is also displayed.\n
                5.
                You save the game by typing 'save' and load a previous game with 'load'.
                These commands will give further instructions for how to load or save.\n
                6.
                New feature! You can also type p1, p2, ..., p8 and a type to print only the types in that generation.\n
                7.
                You can type yield to exit the game, this will show you the Pokémon you missed.\n
                8.
                Finally! You can type q or exit to quit. This does not show you the Pokémon you missed.
                Enjoy!\n
        '''

        print(instructions)

    def _save_game_choice(self) -> None:
        """Function to handle menuing after saving.
        """

        # prompt the user to continue or not
        print("Do you want to quit the game? [y/n]: ",end='')
        choice = input()

        # check the input
        if choice in ['y', 'yes', 'Y', 'YES']:
            print("Quiting!")
            exit()
        elif choice in ['n', 'no', 'N', 'NO']:
            print("Continuing!")
            return
        else:
            print("Invalid option!")
            self._save_game_choice()

    def save_game(self) -> None:
        """This method saves the current progress of the game, in particular, 
        it stores the main attributes of the GuessingGame class.
        """

        # get filename to save game as
        print("Enter save game name: ",end='')
        save_name = input()

        # path to where game should be saved
        path = f"saved/{save_name}"

        # delete existing file, if any
        if os.path.exists(path):
            os.remove(path)
        
        # open file, this will create a new file
        f = open(path, "w")

        # store the number of correct guesses
        f.write(str(self.score))
        f.write("\n")

        # save current guesses in the file
        for key in self.guessed:
            f.write(f"{key}\t{self.guessed[key].name}\n")

        # store magic number, used to know where to stop reading Pokémon
        f.write(str(78111114100105115107))
        f.write("\n")

        # store the generations used in the game
        for gen in self.generations:
            f.write(str(gen))
            f.write("\n")
        
        # close the file
        f.close()

        # call the save_game_choice function to handle the user choice
        self._save_game_choice()

    def load_game(self) -> None:
        """Method to load a saved game. Using this method will nullify
        the timer for the game.
        """

        # get saved directory
        save_dir = os.listdir("saved")

        # tell the user to select a save
        print("Please select your savefile: ")

        # go through the save directory
        for file in save_dir:
            print("\t"+file)

        print("")
        # prompt the user to enter save game filename to load
        print("Select game to load: ",end='')
        load_name = input()

        # path to the file to load
        path = "saved/"+load_name

        # try to open the file
        try:
            f = open(path,"r")
        except FileNotFoundError:
            # ask the user to try again, if the request failed
            print("Couldn't locate save game. Did you make a typo?")
            print("Do you wish to load?")
            print("[y/n]: ",end='')
            answer = input()
            # return None to exit load, this will continue the program as if nothing happened
            if answer == 'n' or answer == 'no' or answer == 'N' or answer == 'NO':
                return None
            else:
                self.load_game()

        # initialize the new generation list and guessed dictionary
        new_gens = []
        new_guessed_tmp = {}

        # the first line in the text file contains the score
        idx = int(f.readline())

        # each line in the Pokédex is on the form DexNumber\tPokémonName
        for line in f:    
            # split line at the tab, line_list is then of the form line_list = ['DexNumber','PokémonName\n']
            line_list = line.split("\t")

            # get the DexNumber and convert to an integer
            dex_number = int(line_list[0])

            # check if the DexNumber is the magic number, meaning the end of the Pokédex has been reached
            if dex_number == 78111114100105115107: # <- easter egg ;)
                break

            # remove the newline character from the Pokémon name and get the first element of the list
            pokemon = (line_list[1].split("\n"))[0]

            # add the Pokémon to the dictionary
            new_guessed_tmp[dex_number] = pokemon

        # loop through the end of the file, which contains the generations used in the saved game
        for line in f:
            new_gens.append(int(line))

        # close the file
        f.close()

        # initialize the Pokémon as an empty dictionary
        new_set_of_pokemon = {}
        new_guessed = {}

        # go through the Pokédex
        for pokemon_entry in dex.Pokedex:
            name = pokemon_entry[0]
            dex_number = pokemon_entry[1]
            gen = pokemon_entry[2]
            type1 = pokemon_entry[3]
            type2 = pokemon_entry[4]

            # constructs the Pokédex from the loaded game
            if gen in new_gens:
                new_set_of_pokemon[dex_number] = Pokemon(name,dex_number,gen,type1,type2)
                new_guessed[dex_number] = Pokemon(new_guessed_tmp[dex_number],dex_number,gen,type1,type2)

        # update attributes
        self.set_of_pokemon = new_set_of_pokemon
        self.guessed = new_guessed
        self.score = idx
        self.generations = new_gens
        self.load = True

    def _parseGuess(self, guess: str | list) -> str | None:
        """Parses the guess and converts to uppercase on the first letter, if needed

        Parameters
        ----------
        guess : str, list
            The users guess. The method will parse this argument and act accordingly. The parsing includes
            finding out which type (or types) are entered. Method might call itself, if necessary.

        Returns
        -------
        str | None
            Returns the parsed type, now having the first letter capitalized or None if there is no type provided or
            an error occures.
        """

        # check if the argument is a list
        if isinstance(guess, list):
            # check if the first argument is of length 2 (basically check if the first argument is p3, as an example)
            if len(guess[0]) <= 2:
                # extract the generation and type, according to which one is first
                gen, typ = guess
            else:
                typ, gen = guess

            # having found the type and gen, parse the type
            typ = self._parseGuess(typ)
            
            # check if the type is a valid type
            if self._isValidType(typ):
                # try and print the types
                try:
                    # take the gen string, which is of the form px, where x is the actual generation, thus, send this number in
                    self._printTypes(typ, int(gen[1]))
                except IndexError:
                    # handle the errors
                    print('\a', end='')
                    print("Invalid generation, try again.")
                    return
                except ValueError:
                    print('\a', end='')
                    print("Not in the Pokédex. Perhaps a typo? Try again.")
                    return
            else:
                # not a valid type, play error sound
                print('\a', end='')
                print("Invalid type! Try Again.")

        else:
            first_letter = ""

            try:
                # get the first letter
                first_letter = guess[0]
            except IndexError:
                pass

            if first_letter.islower(): # if the first letter is lowercase
                # change it to uppercase
                guess = guess.capitalize()

            return guess

    def _isValidType(self, guess: str) -> bool:
        """Method to check if the guess is a valid Pokémon type

        Parameters
        ----------
        guess : str
            The type to check the validity of. 

        Returns
        -------
        bool
            True if the input is a valid type in Pokémon, False otherwise. 
        """

        # parse the guess, will return a Pokémon type or None
        guess = self._parseGuess(guess)

        return any(tmp == guess for tmp in self.valid_types)

    def _printTypes(self, guess: str, gen=None) -> None:
        """Print all Pokémon of a given type, either type1 or type2

        Parameters
        ----------
        guess : str
            The type to print.
        gen : _type_, optional
            The generation to print from, by default None
        """

        # check if an invalid generation is entered
        if gen not in self.generations and (self._isValidType(guess) and gen is not None):
            print('\a',end='')
            print(f"Invalid generation, only generation {self.generations} supported.")

        # go through all the Pokémon in the current game
        for key in self.set_of_pokemon:
            # determine which Pokémon has the type specified with guess
            if (self.set_of_pokemon[key].type1 == guess or self.set_of_pokemon[key].type2 == guess) and (self.set_of_pokemon[key].gen == gen or gen is None):
                # print the guessed Pokémon of these types, showing unknown as '?'
                print(self.guessed[key])

    def initialize_game(self) -> None:
        """This method sets up the attributes of the game and creates the necessary data.
        """

        # setup the save directory, the generations and the Pokédex
        self._create_saved_directory()
        self._determine_generations()
        self._setup_dex()

        # prompt the user with some useful commands to get started
        print("==== Pokémon Guessing Game ==== [press h for help or r to show progress]")

    def convert_time(self, time_in_seconds: float) -> tuple[int,int]:
        """Method to convert the time to seconds and minutes.

        Parameters
        ----------
        time_in_seconds : float
            The time the user took to complete the game. 

        Returns
        -------
        tuple[int,int]
            Tuple consisting of the time in minutes and seconds, respectively as integers.
        """

        # compute the number of seconds and minutes spent completing a game
        seconds = int(time_in_seconds) % 60
        minutes = int((time_in_seconds - seconds) / 60)

        return minutes, seconds

    def end_game(self, end_code: str, final_time=0) -> None:
        """Method called when the game has finished executing.

        Parameters
        ----------
        end_code : str
            Code to determine the reason for the game ending.
        final_time : int, optional
            The time to complete the Pokédex by the player, by default 0
        """

        if end_code == 'end':
            print("Here is the completed Pokédex:")
            print("==============================================")
            print("Dex number\tPokémon")

            # print the completed Pokédex
            for key in self.guessed:
                print(self.guessed[key])
            print("")
            print("Congratulations! You did it!!")

            # get the time taken to complete the Pokédex

            # tell the user the total time if the game was not loaded
            if self.load == False:
                # format the time in minutes and seconds
                ret_times = self.convert_time(final_time)
                print(f"You completed the Pokédex in {ret_times[0]} minutes and {ret_times[1]} seconds.")
                print(f"Final time [{ret_times[0]}:{ret_times[1]}]")

        # if the player called yield, print the Pokémon they missed and exit
        elif end_code == 'yield':
            # calculate remaining Pokémon
            remain = len(self.set_of_pokemon) - self.score
            print(f"You missed {remain} Pokémon.")

            # display Pokémon missing
            print("You forget these Pokémon:")
            for key in self.set_of_pokemon:
                if self.guessed[key].name == '?':
                    print(self.set_of_pokemon[key])

            print("Please try again.")
            exit()
        elif end_code == 'quit':
            print("Quiting!")
            exit()
        elif end_code == "generation fail":
            print("Error, invalid generations")
            exit()
        else:
            print("Quiting!")

    def start_game(self) -> None:
        """Main game, handles input from the user and acts on it.
        """

        # keep going until the score is the same as the number of Pokémon
        while self.score < len(self.set_of_pokemon):
            print("Enter your guess: ", end="")
            try:
                guess = input()
            except KeyboardInterrupt:
                print("")
                print("Quiting!")
                exit()

            if guess not in self.special_cases:
                # split the input to check if there are more than one word
                guess_list = guess.split(" ")
                if len(guess_list) == 2:
                    self._parseGuess(guess_list)
                    continue

            if guess == 'p': self._print_guessed(guess)
            elif guess == 'p1': print("Gen 1 Pokédex:"); self._print_guessed(guess)
            elif guess == 'p2': print("Gen 2 Pokédex:"); self._print_guessed(guess)
            elif guess == 'p3': print("Gen 3 Pokédex:"); self._print_guessed(guess)
            elif guess == 'p4': print("Gen 4 Pokédex:"); self._print_guessed(guess)
            elif guess == 'p5': print("Gen 5 Pokédex:"); self._print_guessed(guess)
            elif guess == 'p6': print("Gen 6 Pokédex:"); self._print_guessed(guess)
            elif guess == 'p7': print("Gen 7 Pokédex:"); self._print_guessed(guess)
            elif guess == 'p8': print("Gen 8 Pokédex:"); self._print_guessed(guess)
            elif guess == 'p9': print("Gen 9 Pokédex:"); self._print_guessed(guess)
            elif guess == 'r': self._progress()
            elif guess == 'q' or guess == 'exit' or guess == 'quit': self.end_game("quit")
            elif guess == 'h' or guess == 'help': self._instructions()
            elif guess == 'save': self.save_game()
            elif guess == 'load': self.load_game()
            elif guess == 'yield': self.end_game('yield')
            elif guess == 'clear': os.system('cls' if os.name == 'nt' else 'clear')

            # print types to help the user
            elif self._isValidType(guess):
                guess = self._parseGuess(guess)
                self._printTypes(guess)

            else:
                # to check for duplicates, we keep the score before checking the guess
                tmp = self.score
                duplicate = False
                # go through all the Pokémon
                for key in self.set_of_pokemon:
                    # check if the guess corresponds to the name of any Pokémon
                    if guess == self.set_of_pokemon[key].name:
                        # if the guessed dictionary has a '?' it means this is a newly guessed Pokémon
                        if self.guessed[key].name == '?':
                            # add it to the guessed dictionary and update the score
                            self.guessed[key].name = guess
                            self.score += 1
                            break
                        else:
                            # if there was no '?' it means the Pokémon has been guessed
                            print('\a', end='')
                            print("Already in the Pokédex.")
                            duplicate = True
                            break
                    else:
                        pass
                # if the score didn't change and the duplicate flag wasn't set, it was a typo or mistake
                if tmp == self.score and duplicate == False:
                    print('\a', end='')
                    print("Not in the Pokédex. Perhaps a typo? Try again.")

if __name__ == '__main__':
    # initialize the GuessingGame class with the parameters specified in config
    game = GuessingGame(config.score, config.special_cases, config.load)

    # initialize the game by created the necessary directory and filling in data
    game.initialize_game()

    # start the main game
    time0 = time.perf_counter()
    game.start_game()
    time1 = time.perf_counter()

    # compute the final time
    final_time = time1 - time0
    
    # if the user guessed everything start the end game method
    game.end_game("end",final_time)
