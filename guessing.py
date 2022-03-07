import sys
import pokemon as pkm
import pokedex as dex

# function to help with the printing
def print_guessed(guessed,guess):
    # firstly, determine which generation to print
    if guess == 'p1':
        gen_range = [1,152]
    elif guess == 'p2':
        gen_range = [152,252]
    elif guess == 'p3':
        gen_range = [252,387]
    elif guess == 'p4':
        gen_range = [387,494]
    elif guess == 'p5':
        gen_range = [494,650]
    elif guess == 'p6':
        gen_range = [650,722]
    elif guess == 'p7':
        gen_range = [722,808]
    else:
        # print all the valid gens
        for key in guessed:
            try:
                print(key,"\t\t",guessed[key])
            except KeyError:
                pass
        return

    # to only print one generation, use the generation bounds as limits
    start = gen_range[0]
    stop  = gen_range[1]

    # go through only one generation and print
    for k in range(start,stop):
        try:
            print(k,"\t\t",guessed[k])
        except KeyError:
            pass

# the user did it, print some messages
def end_game():
    print("Here is the completed Pokédex:")
    print("==============================================")
    print("Dex number\t Pokémon")
    for key in guessed:
        print(key,"\t\t",guessed[key])
    print("")
    print("Congratulations! You did it!!")

def play_game(set_of_pokemon,guessed):
    # counter of correct guesses
    idx = 0

    # the game continues as long as idx is less than the total number of Pokémon in play
    while idx < len(set_of_pokemon):
        print("Enter your guess: ",end='')
        guess = input()

        # logic to parse the user input
        if guess == 'p': print_guessed(guessed,guess)

        elif guess == 'p1':
            print("Gen 1 Pokédex:")
            print_guessed(guessed,guess)

        elif guess == 'p2':
            print("Gen 2 Pokédex:")
            print_guessed(guessed,guess)

        elif guess == 'p3':
            print("Gen 3 Pokédex:")
            print_guessed(guessed,guess)   

        elif guess == 'p4':
            print("Gen 4 Pokédex:")
            print_guessed(guessed,guess)
        
        elif guess == 'p5':
            print("Gen 5 Pokédex:")
            print_guessed(guessed,guess)

        elif guess == 'p6':
            print("Gen 6 Pokédex:")
            print_guessed(guessed,guess)

        elif guess == 'p7':
            print("Gen 7 Pokédex:")
            print_guessed(guessed,guess)

        elif guess == 'r':
            # show the progress to the user
            remain = len(set_of_pokemon) - idx
            if remain == len(set_of_pokemon) - 1:
                print(f"You have {idx} correct guess, meaning there is {remain} left to guess.")
                # print a progress bar, showing the percentage of the progress
                progress = int(100*idx/len(set_of_pokemon))
                for i in range(100):
                    if i < progress:
                        print(chr(9646),end='')
                    else:
                        print(chr(9647),end='')

                print("")
            else:
                print(f"You have {idx} correct guesses, meaning there is {remain} left to guess.")
                # print a progress bar, showing the percentage of the progress
                progress = int(100*idx/len(set_of_pokemon))
                for i in range(100):
                    if i < progress:
                        print(chr(9646),end='')
                    else:
                        print(chr(9647),end='')

                print("")

        elif guess == 'q': exit("Quiting!")

        elif guess == 'h':
            print("==================== Instructions ====================")
            print("The goal here is to guess every Pokémon in the Pokédex.")
            print("The following commands are implemented to help in your journey:")
            print("1.")
            print("You can type p to print all the Pokémon you have guessed. ")
            print("They will show up in the list if you typed the name correctly. ")
            print("Note that you must use a capital letter at the beginning of each name.")
            print("Alternatively, you can use p1, p2, p3 and so on... to print only the generation behind p")
            print("2.")
            print("You can also write a Pokémon type. Either capitalized or not, i.e. you can type Fire or fire. ")
            print("This will print out all the guessed and not guess Pokémon of that type. ")
            print("In particular, not guessed Pokémon are marked with a ? and correctly guessed Pokémon are shown with their name")
            print("and corresponding PokéDex number.")
            print("To help you out the types are displayed if you use these commands.")
            print("3.")
            print("In the terminal you can enter the number 1-7, or any combinations you desire, you also type the commands in any order, like 3 2 1 is fine.")
            print("Note that you have to separate the numbers with spaces, only!")
            print("The game will then run with only the specified generations. All other commands work as before.")
            print("However, typing p4 when generation 4 is excluded does not do anything.")
            print("4.")
            print("Typing r will show the number of remaining Pokémon left and how many correct guesses you have.")
            print("5.")
            print("Finally! You can type q to quit.")
            print("Enjoy!")

        elif pkm.is_valid_type(guess):
            guess = pkm.parse_guess(guess)
            dex.print_types(guess,set_of_pokemon,guessed)
        else:
            tmp = idx
            duplicate = False
            for key,val in set_of_pokemon.items():
                if val.name == guess:
                    if guessed[key] == '?':
                        guessed[val.dex_number] = val.name
                        idx += 1
                        break
                    else:
                        print("Already in the Pokédex.")
                        duplicate = True
                        break
                else:
                    pass
            if tmp == idx and duplicate == False:
                print("Not in the Pokédex. Perhaps a typo? Try again.")

if __name__ == '__main__':
    # prompt the user with some useful commands to get started
    print("==== Pokémon Guessing Game ==== [press h for help or r to show progress]")

    # the user can input the generation wanted in the game, the supported generations are 1-7 (so far)
    if len(sys.argv) > 8: exit("Too many arguments, exiting.")

    # initialize the generations used as empty
    gens = []
    valid_gens = ['1','2','3','4','5','6','7']

    # determine which generations to add, if len(sys.argv) > 1 the user has entered command line arguments
    if len(sys.argv) > 1:
        # loop through the arguments in the argument vector
        for entry in sys.argv:
            for tmp in valid_gens:
                # if entry == tmp, then add this generation to the gens used in the game
                if entry == tmp:
                    # if the entry in the argument vector contains a valid generation 
                    # it is added to the gens list 
                    gens.append(entry)
    else: 
        # if no gens are entered the game runs with all the generations supported, that is gen 1-7
        gens = valid_gens

    # sort the generations
    gens.sort()

    # initialize the dictionary of all the Pokémon
    set_of_pokemon = {}

    # go through the Pokédex
    for pokemon_entry in dex.Pokedex:
        name = pokemon_entry[0]
        dex_number = pokemon_entry[1]
        gen = str(pokemon_entry[2])
        type1 = pokemon_entry[3]
        type2 = pokemon_entry[4]

        # if a Pokémon is in a generation that the user wants, add it to the dictionary of all Pokémon
        if gen in gens:
            set_of_pokemon[dex_number] = pkm.Pokemon(name,dex_number,int(gen),type1,type2)

    # initialize the guessed dictionary (empty at the start)
    guessed = {}

    # add all the Pokémon as '?' at the start
    for key in set_of_pokemon:
        guessed[key] = '?'

    # start the game
    play_game(set_of_pokemon,guessed)
    end_game()