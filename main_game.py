import os
import sys
from enum import IntEnum
from typing import TextIO

from game_api.pokemon_game_api import GameApi

__version__ = "2.0.0"
__author__ = "Jørn Olav Jensen"

# Recognized commands for the game.
keywords = {"p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9",
            "bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "grass",
            "ground", "ghost", "ice", "normal", "poison", "psychic", "rock", "steel", "water"}

SAVE_GAME_SEPARATOR = "78111114100105115107"


class ExitCode(IntEnum):
    ERROR = -1
    OK = 0
    YIELD = 1
    WIN = 2


class MainGame:

    def __init__(self) -> None:
        """Method to initialize the MainGame class.
        This includes setting up the game sessions, 
        finding the Pokémon to use and the score. 
        """

        self.game_api = GameApi()

        # Determine the generations the user wants, then compute the total number of Pokémon in the game.
        self.generations = self.game_api.find_generations(sys.argv)
        self.num_pokemon = self.game_api.find_number_of_pokemon(self.generations)
        self.score = 0

    def setup_game(self) -> None:
        """Method to setup everything before the game can start.
        This creates the guessing table and the saved directory for saving.
        """

        self.game_api.setup_game_session(self.generations)

        # Create the saved directory to store saved game files.
        if not os.path.exists("saved"):
            os.mkdir("saved")

    def _instructions(self) -> None:
        """Method to print instructions to the user. Method is called
        when 'h', ':h' or 'help' is entered in the terminal.
        """

        instructions = '''
            ==================== Instructions ====================
            The goal here is to see if you remember every Pokémon in the Pokédex.
            Type the Pokémon name in the terminal and hit enter to make your guess.
            The following commands are implemented to help in your journey:\n
            1.
            You can type 'p' to print the Pokédex. This will display the Pokémon you have entered
            and the ones you are missing, these being displayed by a '?' symbol.
            Alternatively, you can use 'p1', 'p2', 'p3' and so on... to print the corresponding generations.
            In other words, if you want to see only generation 3, type p3. If you want to see generation 4 and 5,
            you can type p4 p5.\n
            2.
            You can also write a Pokémon type. Either capitalized or not, i.e. you can type 'Fire' or 'fire'.
            This will print out all the guessed and not guessed Pokémon of that type. 
            In particular, not guessed Pokémon are marked with a '?' and correctly guessed Pokémon are shown with their name
            and corresponding Pokédex number. Doing this will display all the types of the Pokémon. 
            You can filter the types based on the generations as above. As an example: fire p4 p5
            will display all generation 4 and 5 Pokémon that are part fire type. 
            You can also combine different types with AND, OR and NOT (not case sensitive) 
            operations to filter the display even more, and filtered on generations.\n
            3.
            In the terminal you can enter the numbers between 1-8, or any combinations you desire, 
            you also type the commands in any order, like p3 p2 p1 is fine.
            Note that you have to separate the numbers with spaces, only!
            The game will then run with only the specified generations. All other commands work as before.
            However, typing p4 when generation 4 is excluded does not display anything.\n
            4.
            Typing 'r' will show the number of remaining Pokémon left and how many correct guesses you have.
            A progress bar showing the percentage is also displayed.\n
            5.
            You save the game by typing 'save' and load a previous game with 'load'.
            These commands will give further instructions for how to load or save.\n
            6.
            You can type yield to exit the game, this will show you the Pokémon you missed.\n
            7. 
            You can use the stats command to display the stats of a Pokémon. Example: stats mew
            will display mew's stats. There is also the command stat, this displays all the Pokémon
            in a given range for a given stat. Example: stat atk 100 120, displays Pokémon that have an
            attack stat between 100 120 (both inclusive). 
            8. 
            You can also use the ability command. Example: ability water absorb, will show all 
            Pokémon with the ability water absorb (includes hidden abilities). 
            9.
            Finally! You can type q or exit to quit. This does not show you the Pokémon you missed.
            Enjoy!\n
        '''

        print(instructions)

    def _check_guess(self, guess: str, update_score=True) -> bool:
        """Checks the user guess. If it is correct
        the score is updated, otherwise a message tells
        the user that the Pokémon has already been entered.
        """

        valid, guessed = self.game_api.check_pokemon_by_name(guess, self.generations)

        if valid:
            if not guessed and update_score:
                self.score += 1
            elif update_score:
                print("Already in the Pokédex.")

        return valid

    def play_game(self) -> None:
        """The main part of the game happens in this method.
        Here the user enters guesses and they are checked for correctness.
        Any input parsing is also handled here. 
        """

        print("==== Pokémon Guessing Game ==== [press h for help or r to show progress]")

        # Continue the game mechanics until the user has guessed everything (or quits).
        while self.score < self.num_pokemon:

            guess = input("Enter your guess: ")
            guess = guess.lower()  # Convert input to lower case for easier parsing.

            if guess in {"q", "quit", "exit", ":q"}:
                self.end_game(ExitCode.OK)
            elif guess in {"yield"}:
                self.end_game(ExitCode.YIELD)
            elif guess in {"h", "help", ":h"}:
                self._instructions()
            elif guess == "clear":
                os.system("clear")
            elif guess in {"r", "remain", "left", ":r"}:
                self.game_api.progress(self.score, self.num_pokemon)
            elif self._check_guess(guess):
                pass
            elif guess == "p":
                # Convert the list of generations into a parsable form.
                gens = " ".join([f"p{str(gen)}" for gen in self.generations])  # Only use the user specified generations.
                self.game_api.show_pokemon_by_generation_and_type("guessing", gens)
            elif "info" in guess:
                self.game_api.show_pokemon_info(guess)
            elif "stats" in guess:
                self.game_api.show_pokemon_stats(guess)
            elif "stat" in guess:
                self.game_api.show_pokemon_by_stat("guessing", guess)
            elif "ability" in guess:
                self.game_api.show_pokemon_by_ability("guessing", guess)
            elif any(word in guess for word in keywords):
                self.game_api.show_pokemon_by_generation_and_type("guessing", guess)
            elif guess == "save":
                self.save_game()
            elif guess == "load":
                self.load_game()
                print(f"Score after loading is complete: {self.score}")
            elif guess == "update":
                self.update_data()
            else:
                print("\a", end="")
                print("Not in the Pokédex. Perhaps a typo?")

    def update_data(self) -> None:
        """Method to update the data stored
        in the database.
        """

        print("Updating the Pokémon data...")

        self.game_api.pokemon_db.update_database()

        print("Update complete!")

    def _save_game_choice(self) -> None:
        """Helper method to handle the menu after saving.
        """

        choice = input("Do you want to quit the game? [y/n]: ")

        if choice in {'y', 'yes', 'Y', 'YES'}:
            self.end_game(ExitCode.OK)
        elif choice in {'n', 'no', 'N', 'NO'}:
            print("Continuing!")
            return
        else:
            print("Invalid option!")
            self._save_game_choice()

    def save_game(self) -> None:
        """This method saves the current progress of the game.
        The saved game is stored as a file in the saved folder.
        """

        # Get the file contents of the saved directory.
        save_dir: list[str] = os.listdir("saved")

        print("\nCurrent save files:")

        # Show the user the saved directory contents.
        for file in save_dir:
            print(f"\t{file}")

        save_name = input("Enter save game name: ")

        with open(f"saved/{save_name}", "w") as f:

            f.write(f"{str(self.score)}\n")

            for gen in self.generations:
                f.write(f"{str(gen)}\n")

            # Store magic number, used to know where to stop reading Pokémon.
            f.write(f"{str(SAVE_GAME_SEPARATOR)}\n")

            all_pokemon = self.game_api.get_pokemon_in_game("guessing", self.generations)

            for pokemon in all_pokemon:
                f.write(f"{pokemon.name}\n")

        self._save_game_choice()

    def _load_file_contents(self, f: TextIO) -> None:
        """Helper method to read the save file content
        and reconstruct the game state.

        Parameters
        ----------
        f : TextIO
            The save game file to load.
        """

        # The first line is the number of correct guesses.
        try:
            self.score = int(f.readline().strip())
        except ValueError:
            self.end_game(ExitCode.ERROR)

        print(f"Score in _load_file_contents_line_247: {self.score}")

        gens = []

        line = ""

        while line != SAVE_GAME_SEPARATOR:
            line = f.readline().strip()

            if line and line != SAVE_GAME_SEPARATOR:
                gens.append(int(line))

        pokemon_names_pos = f.tell()

        self.generations = gens
        self.num_pokemon = self.game_api.find_number_of_pokemon(gens)

        # Recreate the game session from the save file.
        self.game_api.setup_game_session(gens)

        # Skip to the Pokémon names.
        f.seek(pokemon_names_pos, 0)

        # Fill in the Pokémon names from the save file.
        for line in f:
            potential_pokemon = line.strip()
            if potential_pokemon != "?":
                self._check_guess(potential_pokemon, update_score=False)

    def load_game(self) -> None:
        """Method to load a saved game. 
        """

        # Get the file contents of the saved directory.
        save_dir: list[str] = os.listdir("saved")

        print("Please select your save file: ")

        # Show the user the saved directory contents.
        for file in save_dir:
            print(f"\t{file}")

        load_name = input("Select game to load: ")

        try:
            with open(f"saved/{load_name}", "r") as f:
                self._load_file_contents(f)
        except FileNotFoundError:
            # Ask the user to try again, if the request failed.
            print("Couldn't locate save game. Did you make a typo?")
            answer = input("Do you wish to load? [y/n]: ")
            if answer in {"n", "no", "N", "NO"}:
                return
            print("Reloading...")
            self.load_game()

    def end_game(self, exit_code=0) -> None:
        """Method to quit the game.
        What happens is based on the exit code.

        Parameters
        ----------
        exit_code : int, optional
            Determines which behavior occurs when
            the game exits, by default 0.
        """

        match exit_code:
            case ExitCode.OK:  # 0
                print("Quitting!")
            case ExitCode.YIELD:  # 1
                print("You missed these Pokémon:")

                all_pokemon = self.game_api.get_pokemon_in_game("pokemon", self.generations)
                guessed_pokemon = self.game_api.get_pokemon_in_game("guessing", self.generations)

                for pokemon, guessed in zip(all_pokemon, guessed_pokemon):
                    if guessed.name == "?":
                        print(pokemon)
            case ExitCode.WIN:  # 2
                print("Congratulations! You completed the Pokédex!.")
            case _:
                print("An error has occurred. Exiting.")

        exit()


if __name__ == "__main__":

    guessing_game = MainGame()

    guessing_game.setup_game()
    guessing_game.play_game()
    guessing_game.end_game(ExitCode.WIN)
