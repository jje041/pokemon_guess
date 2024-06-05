from game_api.backend.pokemon import Pokemon
from game_api.backend.pokemon_database_api import PokemonDatabase

MAX_GENERATIONS = 9

valid_types = ["normal", "water", "fire", "grass", "fighting", "psychic", "ice", "electric",
               "dragon", "fairy", "dark", "ghost", "steel", "rock", "ground", "flying", "bug", "poison"]


class GameApi:
    """
    GameApi class

    Interface for the main game. Provides the major
    functionality of the game, and interacts directly with 
    the database API.

    Attributes
    ----------
    pokemon_db : PokemonDatabase
        The database API, gives the GameApi access to
        the underlying database methods.

    Methods
    -------
    find_generations(self, argv: list[str]) -> list[int]
        Method to parse the command line arguments
        into a list of generations to use in the game.
    find_number_of_pokemon(self, gens: list[int]) -> int
        Method to compute the total number of Pokémon in
        the game session.
    get_pokemon_in_game(self, table: str, gens: list[int]) -> list[Pokemon]
        Method to fetch all the Pokémon to use in the current game session.
    progress(self, score: int, num_pokemon: int) -> None
        Method to print a progress bar.
    show_pokemon_info(self, guess: str) -> None
        Method to info for a Pokémon. Includes stats, typing,
        egg groups, gender, height, weight and abilities.
    show_pokemon_stats(self, guess: str) -> None
        Method to display the stats of the provided Pokémon.
    show_pokemon_by_stat(self, table: str, guess: str) -> None
        Method to display Pokémon based on attack, defense, special attack, 
        special defense, speed or the stat total. Will sort the result based
        on the national dex number.
    show_pokemon_by_generation_and_type(self, table: str, guess: str) -> None
        Method to print out Pokémon based on generations and types.
    check_pokemon_by_name(self, name: str, gens: list[int]) -> tuple[bool, bool]
        Method to check if a Pokémon name corresponds to a Pokémon and
        if it is already guessed or not.
    setup_game_session(self, gens: list[int]) -> None
        Method to setup guessing table.
    """

    def __init__(self) -> None:
        self.pokemon_db = PokemonDatabase()

    def find_generations(self, argv: list[str]) -> list[int]:
        """Method to parse the command line
        arguments into a list of generations to be
        used in the game. 

        Parameters
        ----------
        argv : list[str]
            A list of strings containing the arguments 
            from the terminal. 

        Returns
        -------
        list[int]
            The parsed generations to be used in the game. 

        Raises
        ------
        ValueError
            If the arguments from argv are invalid, that is,
            not numbers from 1-9.
        """

        # Remove the first element of the list (always the original file name).
        argv.pop(0)

        if not argv:
            return list(range(1, MAX_GENERATIONS + 1))

        # Find the valid generations for the game.
        valid_gens = set({str(gen) for gen in range(1, MAX_GENERATIONS + 1)})

        # Check that the input is acceptable.
        if not set(argv).issubset(valid_gens):
            raise ValueError("Invalid generations requested, can only be numbers from 1-9.")

        return sorted({int(entry) for entry in argv})

    def find_number_of_pokemon(self, gens: list[int]) -> int:
        """Method to find the total number of Pokémon to be used 
        given the required generations. Generations are not checked,
        and has to be verified by caller. 

        Parameters
        ----------
        generations : list[int]
            A list containing all the generations
            to be used in sorted order.

        Returns
        -------
        int
            The total number of Pokémon that the requested generations have,
            combined, which is 0 if the input is wrong.
        """

        generation_pokemon_count = {
            1: 151,
            2: 100,
            3: 135,
            4: 107,
            5: 156,
            6: 72,
            7: 88,
            8: 96,
            9: 120
        }

        return sum(generation_pokemon_count[gen] for gen in gens if gen in generation_pokemon_count)

    def get_pokemon_in_game(self, table: str, gens: list[int]) -> list[Pokemon]:
        """Method to fetch the Pokémon to use in the current game.

        Parameters
        ----------
        table : str
            The table to fetch the data from.

        gens : list[int]
            The requested generations the player wants.

        Returns
        -------
        list[Pokemon]
            List of all Pokémon from
            the requested generations.

        Raises
        ------
        PokemonInvalidGenerations
            If the provided generations are invalid.
        """

        return self.pokemon_db.get_pokemon_by_gens(table, gens, types=None)

    def progress(self, score: int, num_pokemon: int) -> None:
        """Method to display a progress bar
        in the terminal for the player.

        Parameters
        ----------
        score : int
            The player's current score, that is,
            the number of Pokémon correctly guessed.
        num_pokemon : int
            The total number of Pokémon in the generations
            the player has selected.
        """

        remain = num_pokemon - score

        print(f"You have {score} correct guesses, meaning there is {remain} left to guess.")

        progress = int(100 * score / num_pokemon)
        # 9646 and 9647 represents the progress bar character.
        progress_bar = [chr(9646) if i < progress else chr(9647) for i in range(100)]
        print("".join(progress_bar), end="")
        print()

    def show_pokemon_info(self, guess: str) -> None:
        """Method to display the info for
        the requested Pokémon.

        Parameters
        ----------
        guess : str
            The input from the user, having the
            info <name> syntax, not case-sensitive.
        """

        name = guess.lower().replace("info", "").strip()

        if pokemon_list := self.pokemon_db.get_pokemon_by_name("pokemon", name):
            for pokemon in pokemon_list:
                pokemon.info()
        else:
            print(f"No Pokémon named {name}")

    def show_pokemon_stats(self, guess: str) -> None:
        """Method to display the stats of
        a requested Pokémon.

        Parameters
        ----------
        guess : str
            The user input, of the form
            stats <name>, not case-sensitive.
        """

        name = guess.lower().replace("stats", "").strip()

        if pokemon_list := self.pokemon_db.get_pokemon_by_name("pokemon", name):
            for pokemon in pokemon_list:
                pokemon.show_stats()
        else:
            print(f"No Pokémon named {name}")

    def show_pokemon_by_stat(self, table: str, guess: str) -> None:
        """Method to show Pokémon based on the 
        requested stat and range. Method will sort the 
        Pokémon based on the national dex number.

        Parameters
        ----------
        table : str
            Which table to fetch the stats from.

        guess : str
            The input request, which must have the form
            stat <stat> <min> <max>, where <stat> is either
            hp, atk, def, sp_atk, sp_def or spd, total is also allowed.
            Both min and max are inclusive.
        """

        try:
            stat, min_stat, max_stat = guess.replace("stat", "").strip().split(" ")
        except ValueError:
            print(f"Syntax error, got {guess}, expected stat <stat> <min> <max>. Run the h command for help.")
            return

        try:
            min_stat = int(min_stat)
            max_stat = int(max_stat)
        except ValueError:
            print(f"{min_stat} and {max_stat} must be integer values! Got {min_stat} and {max_stat}.")
            return

        if stat == "total":
            try:
                all_pokemon = self.pokemon_db.get_pokemon_by_stat_total(table, min_stat, max_stat)
            except (ValueError, TypeError) as e:
                print(f"Error: {e}")
                return
        else:
            try:
                all_pokemon = self.pokemon_db.get_pokemon_by_stat(table, stat, min_stat, max_stat)
            except (ValueError, TypeError) as e:
                print(f"Error: {e}")
                return

        if not all_pokemon:
            print(f"No Pokémon in the range {min_stat}-{max_stat} for the {stat} stat.")

        pok_sort = sorted(all_pokemon)

        for pokemon in pok_sort:
            print(pokemon)

    def show_pokemon_by_ability(self, table: str, guess: str) -> None:
        """Method to show all Pokémon
        with the requested ability.

        Parameters
        ----------
        table : str
            Which table to fetch the abilities from.

        guess : str
            The input request, which must be on the format
            <ability> <ability_name>.
        """

        # Only split once, to avoid issues with the number of values.
        _, ability_name = guess.split(" ", maxsplit=1)

        try:
            all_pokemon = self.pokemon_db.get_pokemon_by_ability(table, ability_name)
        except TypeError as e:
            print(f"Error: {e}")
            return

        if not all_pokemon:
            print(f"No Pokémon has the ability: '{ability_name}'")
            return

        for pokemon in all_pokemon:
            print(pokemon)

    def show_pokemon_by_generation_and_type(self, table: str, guess: str) -> None:
        """Method to filter the Pokemon in the current
        game state based on generations and types. The following
        syntax is used: 
        p1, p2 and so on, represent generations to filter based on.
        Types can be filtered based on the logical operations AND, OR and NOT.

        Parameters
        ----------
        table : str
            Which table to extract the query on.
        guess : str
            The requested generations and types.
        """

        gens = []
        all_gens = {"p1": 1, "p2": 2, "p3": 3, "p4": 4, "p5": 5, "p6": 6, "p7": 7, "p8": 8, "p9": 9}

        # Extract the generational info from the guess argument.
        for gen_command, gen_value in all_gens.items():
            if gen_command in guess:
                guess = guess.replace(gen_command, "")
                gens.append(gen_value)

        gens.sort()
        guess = guess.strip()

        # Determine if the user wants to see any types.
        show_types = any(pokemon_type in guess for pokemon_type in valid_types)

        all_pokemon = self.pokemon_db.get_pokemon_by_type(table, guess, gens)

        for pokemon in all_pokemon:
            if show_types:
                print(pokemon)
            else:
                print(pokemon.print_no_types())

    def check_pokemon_by_name(self, name: str, gens: list[int]) -> tuple[bool, bool]:
        """Method to check if the provided name is a valid Pokémon.

        Parameters
        ----------
        name : str
            The Pokémon name to check for.
        gens : list[int]
            The generations that the Pokémon should be from.

        Returns
        -------
        tuple[bool, bool]
            First value is True if the name provided
            corresponds to a valid Pokémon, the second
            value is True if the Pokémon is in the guessing table.
        """

        try:
            # Try to pop, if it fails, there is no Pokémon with the provided name.
            fetched_pokemon = self.pokemon_db.get_pokemon_by_name("pokemon", name).pop(0)
        except IndexError:
            return False, False

        # Check if the Pokémon is in the generations that are used.
        if fetched_pokemon.gen not in gens:
            return False, False

        try:
            # Check if the Pokémon is already in the guessing table.
            self.pokemon_db.get_pokemon_by_name("guessing", name).pop(0)
        except IndexError:
            self.pokemon_db.update_pokemon_name("guessing", fetched_pokemon.dex_num, name)
            return True, False

        return True, True

    def setup_game_session(self, gens: list[int]) -> None:
        """Method to setup the guessing table.

        Parameters
        ----------
        gens : list[int]
            Which generations the guessing
            table should contain.
        """

        self.pokemon_db.setup_guessing(gens)


if __name__ == "__main__":

    game = GameApi()

    gens = game.find_generations(["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    num_pokemon = game.find_number_of_pokemon(gens)

    game.show_pokemon_info("info mr. mime")
    game.show_pokemon_by_ability("pokemon", "ability volt absorb")

    game.show_pokemon_by_stat("pokemon", "total 140 200")

    game.show_pokemon_by_generation_and_type("pokemon", "fire or (ghost p5 p6")
