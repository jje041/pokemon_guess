import pokedex as dex
import pokemon as pkm
import config
import os
import sys
import time

class GuessingGame:
    '''
    A class that contains the game's attributes and methods 

    Attributes:
        (Name: score; Type: int)
        Description: number of correct guesses the user has

        (Name: generations; Type: list (of int))
        Description: list of generations the user is playing with

        (Name: guessed; Type: dictionary (int key : class Pokemon))
        Description: the correct guesses the user has, the key corresponds to the Pokédex number 
                     and the value is a an object of the Pokémon class, contain information about the Pokémon

        (Name: set_of_pokemon; Type: dictionary (int key : class Pokemon))        
        Description: all the Pokémon corresponding to the generations in the generations attribute 
                     stored as Pokédex number : Pokémon class

        (Name: valid_types; Type: list (of strings))
        Description: list of strings, the strings are the types the Pokémon can have

        (Name: load; Type: boolean)
        Description: used to check if the user is playing a loaded game, used by the timing handler

    Methods:
        __init__(score,generations,guessed,set_of_pokemon)
            return None

        __create_save_directory()
            return None

        __determine_generations()
            return None

        __setup_dex()
            return None

        __print_guessed(guess)
            return None

        __progress()
            return None

        __instructions()
            return None

        __save_game_choice()
            return None
        
        save_game()
            return None

        load_game()
            return None

        __parseGuess(guess)
            return guess

        __isValidType(guess)
            return Bool

        __printTypes(guess)
            return None
        
        initialize_game()
            return None
    '''

    def __init__(self,score,generations,guessed,set_of_pokemon,special_cases,load):
        ''' initialize the GuessingGame class '''
        self.score = score
        self.generations = generations
        self.guessed = guessed
        self.set_of_pokemon = set_of_pokemon
        self.special_cases = special_cases
        self.load = load

        self.valid_types = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel',
                            'Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy']

    def __create_save_directory(self):
        ''' used to create the saved directory needed to save and load '''

        # check if the 'saved' directory exists
        if os.path.exists("saved"):
            # if it exists, do nothing
            pass
        else:
            # if not, create it
            os.mkdir("saved")

    def __determine_generations(self):
        ''' function to determine the generations the user wants '''
        # the user can input the generation wanted in the game, the supported generations are 1-8 (so far)
        if len(sys.argv) > 8: exit("Too many arguments, exiting.")

        # the generations supported in the game
        valid_gens = ['1','2','3','4','5','6','7','8']

        # determine which generations to add, if len(sys.argv) > 1 the user has entered command line arguments
        if len(sys.argv) > 1:
            # loop through the arguments in the argument vector, skipping the first argument (this is guessing.py)
            for entry in sys.argv[1:]:
                for tmp in valid_gens:
                    # if entry == tmp, then add this generation to the gens used in the game
                    if entry == tmp:
                        # if the entry in the argument vector contains a valid generation,
                        # it is added to the gens list 
                        self.generations.append(int(entry))
        else:
            # if no gens are entered the game runs with all the generations supported, that is gen 1-8
            self.generations = [1,2,3,4,5,6,7,8]

        # if the user has entered something strange, quit properly
        if not self.generations:
            self.end_game("generation fail")

        # sort the generations
        self.generations.sort()

    def __setup_dex(self):
        ''' initialize the complete Pokédex using the generations the user wants, also setup the guessed dictionary '''

        # go through the Pokédex list
        for pokemon_entry in dex.Pokedex:
            # save name, dex number, generation and both types
            name = pokemon_entry[0]
            dex_number = pokemon_entry[1]
            gen = pokemon_entry[2]
            type1 = pokemon_entry[3]
            type2 = pokemon_entry[4]

            # if a Pokémon is in a generation that the user wants, add it to the dictionary of all the Pokémon
            if gen in self.generations:
                # also add guessed, but set name to '?'
                self.set_of_pokemon[dex_number] = pkm.Pokemon(name,dex_number,gen,type1,type2)
                self.guessed[dex_number]        = pkm.Pokemon('?',dex_number,gen,type1,type2)

    def __print_guessed(self,guess):
        """
        ''' function to help with printing Pokémon already guessed '''

            arguments:
                guess: generation the user wants to print
        
            return:
                None
        """
        
        # firstly, determine which generation to print
        if guess == 'p1': gen_range = [1,152]
        elif guess == 'p2': gen_range = [152,252]
        elif guess == 'p3': gen_range = [252,387]
        elif guess == 'p4': gen_range = [387,494]
        elif guess == 'p5': gen_range = [494,650]
        elif guess == 'p6': gen_range = [650,722]
        elif guess == 'p7': gen_range = [722,810]
        elif guess == 'p8': gen_range = [810,906]
        else:
            # print all the valid gens, using the generation to determine the color
            for key in self.set_of_pokemon:
                print(f"{self.guessed[key].setColorOfGeneration()}\t\t{self.guessed[key].name}")
            return

        # to only print one generation, use the generation bounds as limits
        start = gen_range[0]
        stop  = gen_range[1]

        # go through only one generation and print using the generation to determine the color
        for key in range(start,stop):
            try:
                print(f"{self.guessed[key].setColorOfGeneration()}\t\t{self.guessed[key].name}")
            except KeyError:
                pass

    def __progress(self):
        ''' method to display a progress bar in the terminal '''

        # determine how many Pokémon remain
        remain = len(self.set_of_pokemon) - self.score
        if remain == len(self.set_of_pokemon) - 1:
            # if the user have only one correct guess, use singular instead of plural
            print(f"You have {self.score} correct guess, meaning there is {remain} left to guess.")
            # print a progress bar, showing the percentage of the progress
            progress = int(100*self.score/len(self.set_of_pokemon))
            for i in range(100):
                if i < progress: print(chr(9646),end='')
                else:            print(chr(9647),end='')

            print("")
        else:
            print(f"You have {self.score} correct guesses, meaning there is {remain} left to guess.")
            # print a progress bar, showing the percentage of the progress
            progress = int(100*self.score/len(self.set_of_pokemon))
            for i in range(100):
                if i < progress: print(chr(9646),end='')
                else:            print(chr(9647),end='')

            print("")

    def __instructions(self):
            ''' function to print instructions to the user '''
            print("==================== Instructions ====================")
            print("The goal here is to guess every Pokémon in the Pokédex. ")
            print("Type the Pokémon name in the terminal and hit enter to make your guess. ")
            print("The following commands are implemented to help in your journey:")
            print("1.")
            print("You can type 'p' to print the Pokédex. This will display the Pokémon you have guessed")
            print("and the ones you are missing, these being displayed by a '?' symbol.")
            print("Note that you must use a capital letter at the beginning of each name.")
            print("Alternatively, you can use 'p1', 'p2', 'p3' and so on... to print only the generation behind p")
            print("2.")
            print("You can also write a Pokémon type. Either capitalized or not, i.e. you can type 'Fire' or 'fire'. ")
            print("This will print out all the guessed and not guessed Pokémon of that type. ")
            print("In particular, not guessed Pokémon are marked with a '?' and correctly guessed Pokémon are shown with their name")
            print("and corresponding PokéDex number.")
            print("To help you out, the types are displayed if you use these commands.")
            print("3.")
            print("In the terminal you can enter the numbers between 1-8, or any combinations you desire, ")
            print("you also type the commands in any order, like 3 2 1 is fine.")
            print("Note that you have to separate the numbers with spaces, only!")
            print("The game will then run with only the specified generations. All other commands work as before.")
            print("However, typing p4 when generation 4 is excluded does not do anything.")
            print("4.")
            print("Typing 'r' will show the number of remaining Pokémon left and how many correct guesses you have.")
            print("A progress bar showing the percentage is also displayed.")
            print("5.")
            print("You save the game by typing 'save' and load a previous game with 'load'.")
            print("These commands will give further instructions for how to load or save.")
            print("6.")
            print("New feature! You can also type p1, p2, ..., p8 and a type to print only the types in that generation.")
            print("7.")
            print("You can type yield to exit the game, this will show you the Pokémon you missed.")
            print("8.")
            print("Finally! You can type q or exit to quit. This does not show you the Pokémon you missed.")
            print("Enjoy!")

    def __save_game_choice(self):
        ''' function to handle menuing after saving '''
        # prompt the user to continue or not
        print("Do you want to quit the game? [y/n]: ",end='')
        choice = input()

        # check the input
        if choice == 'y' or choice == 'yes' or choice == 'Y' or choice == 'YES':
            print("Quiting!")
            exit()
        elif choice == 'n' or choice == 'no' or choice == 'N' or choice == 'NO':
            print("Continuing!")
            return
        else:
            print("Invalid option!")
            self.__save_game_choice()

    def save_game(self):
        ''' this method saves the current progress of the game, in particular, it stores the main attributes of the GuessingGame class '''

        # get filename to save game as
        print("Enter save game name: ",end='')
        save_name = input()

        # path to where game should be saved
        path = "saved/"+save_name

        # delete existing file, if any
        if os.path.exists(path):
            os.remove(path)
        
        # open file, this will create a new file
        f = open(path,"w")

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
        self.__save_game_choice()

    def load_game(self):
        ''' method to load a saved game '''

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
                new_set_of_pokemon[dex_number] = pkm.Pokemon(name,dex_number,gen,type1,type2)
                new_guessed[dex_number]        = pkm.Pokemon(new_guessed_tmp[dex_number],dex_number,gen,type1,type2)

        # update attributes
        self.set_of_pokemon = new_set_of_pokemon
        self.guessed = new_guessed
        self.score = idx
        self.generations = new_gens
        self.load = True

    def __parseGuess(self,guess):
        ''' parses the guess and converts to uppercase on the first letter, if needed 
        
            arguments:
                guess - type to be parsed

            return
                guess - parsed type, now having the first letter capitalized
        '''

        # check if the argument is a list
        if isinstance(guess,list):
            # check if the first argument is of length 2 (basically check if the first argument is p3, as an example)
            if len(guess[0]) <= 2:
                typ = guess[1]
                gen = guess[0]
            else:
                typ = guess[0]
                gen = guess[1]

            # having found the type and gen, parse the type
            typ = self.__parseGuess(typ)
            
            # check if the type is a valid type
            if self.__isValidType(typ):
                # try and print the types
                try:
                    # take the gen string, which is of the form px, where x is the actual generation, thus, send this number in
                    self.__printTypes(typ,int(gen[1]))
                except IndexError:
                    # handle the errors
                    print('\a',end='')
                    print("Invalid generation, try again.")
                    return
                except ValueError:
                    print('\a',end='')
                    print("Not in the Pokédex. Perhaps a typo? Try again.")
                    return
            else:
                # not a valid type, play error sound
                print('\a',end='')
                print("Invalid type! Try Again.")

        else:
            # get the first letter
            first_letter = guess[0]

            if first_letter.islower(): # if the first letter is lowercase
                # change it to uppercase
                guess = guess.capitalize()

            return guess

    def __isValidType(self,guess):
        ''' method to check if the guess is a valid Pokémon type,
            returns True/False '''

        guess = self.__parseGuess(guess)

        # goes through the list of valid types to check if it is there
        for tmp in self.valid_types:
            if tmp == guess:
                return True

        return False

    def __printTypes(self,guess,gen=None):
        ''' print all Pokémon of a given type, either type1 or type2 '''

        # check if an invalid generation is entered
        if gen not in self.generations:
            # invalid generation, but is it a type?
            if self.__isValidType(guess) and gen is not None:
                print('\a',end='')
                print(f"Invalid generation, only generation {self.generations} supported.")

        # go through all the Pokémon in the current game
        for key in self.set_of_pokemon:
            # determine which Pokémon has the type specified with guess
            if (self.set_of_pokemon[key].type1 == guess or self.set_of_pokemon[key].type2 == guess) and (self.set_of_pokemon[key].gen == gen or gen == None):
                # print the guessed Pokémon of these types, showing unknown as '?'
                print(self.guessed[key])

    def initialize_game(self):
        ''' this method sets up the attributes of the game and creates the necessary data '''
        self.__create_save_directory()
        self.__determine_generations()
        self.__setup_dex()

        # prompt the user with some useful commands to get started
        print("==== Pokémon Guessing Game ==== [press h for help or r to show progress]")

    def convert_time(self,time_in_seconds):
        ''' method to convert the time to seconds and minutes '''
        seconds = int(time_in_seconds) % 60
        minutes = int((time_in_seconds - seconds) / 60)

        return (minutes,seconds)

    def end_game(self,end_code,final_time=0):
        ''' method called when the game has finished executing '''

        if end_code == 'end':
            # display information to the user
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

            # exit
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

    def start_game(self):
        ''' main game, handles input from the user and acts on it '''

        # keep going until the score is the same as the number of Pokémon
        while self.score < len(self.set_of_pokemon):
            print("Enter your guess: ",end='')
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
                    self.__parseGuess(guess_list)
                    continue

            # logic to parse the user input
            if guess == 'p': self.__print_guessed(guess)
            elif guess == 'p1': print("Gen 1 Pokédex:"); self.__print_guessed(guess)
            elif guess == 'p2': print("Gen 2 Pokédex:"); self.__print_guessed(guess)
            elif guess == 'p3': print("Gen 3 Pokédex:"); self.__print_guessed(guess)
            elif guess == 'p4': print("Gen 4 Pokédex:"); self.__print_guessed(guess)
            elif guess == 'p5': print("Gen 5 Pokédex:"); self.__print_guessed(guess)
            elif guess == 'p6': print("Gen 6 Pokédex:"); self.__print_guessed(guess)
            elif guess == 'p7': print("Gen 7 Pokédex:"); self.__print_guessed(guess)
            elif guess == 'p8': print("Gen 8 Pokédex:"); self.__print_guessed(guess)
            elif guess == 'r': self.__progress()

            elif guess == 'q' or guess == 'exit' or guess == 'quit': self.end_game("quit")
            elif guess == 'h' or guess == 'help': self.__instructions()

            # handle save and load
            elif guess == 'save': self.save_game()
            elif guess == 'load': self.load_game()

            elif guess == 'yield': self.end_game('yield')

            elif guess == 'clear': os.system('cls' if os.name == 'nt' else 'clear')

            # print types to help the user
            elif self.__isValidType(guess):
                guess = self.__parseGuess(guess)
                self.__printTypes(guess)

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
                            print('\a',end='')
                            print("Already in the Pokédex.")
                            duplicate = True
                            break
                    else:
                        pass
                # if the score didn't change and the duplicate flag wasn't set, it was a typo or mistake
                if tmp == self.score and duplicate == False:
                    print('\a',end='')
                    print("Not in the Pokédex. Perhaps a typo? Try again.")

if __name__ == '__main__':
    # initialize the GuessingGame class with the parameters specified in config
    game = GuessingGame(config.score,config.generations,config.correct,config.valid,config.special_cases,config.load)

    # initialize the game by created the necessary directory and filling in data
    game.initialize_game()

    # start the main game
    time0 = time.perf_counter()
    game.start_game()
    time1 = time.perf_counter()

    final_time = time1 - time0
    
    # if the user guessed everything start the end game method
    game.end_game("end",final_time)
