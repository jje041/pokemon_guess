import sys
import pokemon as pkm
import pokedex as dex

def print_guessed(guessed,guess):
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
        for key in guessed:
            try:
                print(key,"\t\t",guessed[key])
            except KeyError:
                pass
        return

    start = gen_range[0]
    stop  = gen_range[1]

    for k in range(start,stop):
        try:
            print(k,"\t\t",guessed[k])
        except KeyError:
            pass

def end_game():
    print("")
    print("Congratulations! You did it!!")
    print("Here is the completed Pokédex:")
    print("==============================================")
    print("Dex number\t Pokémon")
    for key in guessed:
        print(key,"\t\t",guessed[key])

def play_game(set_of_pokemon,guessed):
    idx = 0

    while idx < len(set_of_pokemon):
        print("Enter your guess: ",end='')
        guess = input()

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
            remain = len(set_of_pokemon) - idx
            if remain == len(set_of_pokemon) - 1:
                print(f"You have {idx} correct guess, meaning there is {remain} left to guess.")
                b'\x17'.decode('cp437')
            else:
                print(f"You have {idx} correct guesses, meaning there is {remain} left to guess.")
                print(chr(2588))

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
            for key,val in set_of_pokemon.items():
                if val.name == guess and guessed[key] == '?':
                    guessed[val.dex_number] = val.name
                    idx += 1
                    break
            if tmp == idx:
                print("Not in the Pokédex or already in. Try again.")

if __name__ == '__main__':
    print("==== Pokémon Guessing Game ==== [press h for help or r to show progress]")

    # the user can input the generation wanted in the game, the supported generations being 1-7.
    if len(sys.argv) > 8: exit("Too many arguments, exiting.")

    gens = []
    valid_gens = ['1','2','3','4','5','6','7']

    if len(sys.argv) > 1:
        for entry in sys.argv:
            for tmp in valid_gens:
                if entry == tmp:
                    # if the entry in the argument vector contains a valid generation 
                    # it is added to the gens list 
                    gens.append(entry)
    else: 
        # if no gens are entered the game runs with all the generations supported, that is gen 1-7
        gens = valid_gens

    # sort the generations
    gens.sort()

    set_of_pokemon = {}

    for pokemon_entry in dex.Pokedex:
        name = pokemon_entry[0]
        dex_number = pokemon_entry[1]
        gen = str(pokemon_entry[2])
        type1 = pokemon_entry[3]
        type2 = pokemon_entry[4]

        if gen in gens:
            set_of_pokemon[dex_number] = pkm.Pokemon(name,dex_number,int(gen),type1,type2)

    guessed = {}

    for key in set_of_pokemon:
        guessed[key] = '?'

    play_game(set_of_pokemon,guessed)
    end_game()