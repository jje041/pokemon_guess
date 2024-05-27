"""The Pokémon module. Contains the implementation of the
Pokémon class."""

from __future__ import annotations

from colorama import init

__version__ = "2.0.1"
__author__ = "Jørn Olav Jensen"


# The maximum and minimum value for a Pokémon stat.
MAX_STAT = 255
MIN_STAT = 1

# Maximum length of a stat when shown in the terminal
# that is, the number of boxes used.
MAX_STAT_DISPLAY_SIZE = 50


class Pokemon:
    """
    Pokémon Class

    A class representing a Pokémon with various attributes, 
    including: basic information, stats, abilities, size, and more.

    Parameters
    ----------
    dex_num : int
        The national dex number of the Pokémon.
    name : str
        The name of the Pokémon.
    gen : int
        The generation in which the Pokémon was introduced.
    type1 : str
        The primary type of the Pokémon.
    type2 : str or None
        The secondary type of the Pokémon. If the Pokémon is monotype, this will be None.
    stats : dict[str, int]
        A dictionary containing the Pokémon's stats in the format {HP, ATK, DEF, SP_ATK, SP_DEF, SPD}.
    abilities : dict[str, str or None]
        A dictionary for the Pokémon's abilities in the format {first, second, hidden}.
    height : float
        The height of the Pokémon in meters.
    weight : float
        The weight of the Pokémon in kilograms.
    egg_groups : tuple[str, str or None]
        A tuple representing the Pokémon's egg groups. Always non-empty.
    genders : tuple[float or None, float or None]
        A tuple representing the gender ratio in percentages. Format: (male, female).
    catch_rate : int
        The catch rate for the Pokémon, always between 3 and 255.

    Raises
    ------
    ValueError
        If the 'stats' parameter is not a dictionary.
        If the 'gen' parameter is not a positive integer.
        If the 'height' or 'weight' parameters are not non-negative floats.
        If the 'egg_groups' parameter is not a tuple with at least one string.
        If the 'genders' parameter is not a tuple with two elements, each being None or a float.
        If the 'catch_rate' parameter is not an integer.

    Attributes
    ----------
    dex_num : int
        The national dex number of the Pokémon.
    name : str
        The name of the Pokémon.
    gen : int
        The generation in which the Pokémon was introduced.
    type1 : str
        The primary type of the Pokémon.
    type2 : str or None
        The secondary type of the Pokémon. If the Pokémon is monotype, this will be None.
    stats : dict[str, int]
        A dictionary containing the Pokémon's stats in the format {HP, ATK, DEF, SP_ATK, SP_DEF, SPD}.
    abilities : dict[str, str or None]
        A dictionary for the Pokémon's abilities in the format {first, second, hidden}.
    height : float
        The height of the Pokémon in SI units.
    weight : float
        The weight of the Pokémon in SI units.
    egg_groups : tuple[str, str or None]
        A tuple representing the Pokémon's egg groups. Always non-empty.
    genders : tuple[float or None, float or None]
        A tuple representing the gender ratio in percentages. Format: (male, female).
    catch_rate : int
        The catch rate for the Pokémon in percentage.
    """

    def __init__(self, dex_num: int, name: str, gen: int, type1: str, type2: str | None,
                 stats: dict[str, int], abilities: dict[str, str | None], height: float, weight: float,
                 egg_groups: tuple[str, str | None], genders: tuple[float | None, float | None], catch_rate: int
                 ) -> None:

        init()

        # Check if 'stats' is a dictionary.
        if not isinstance(stats, dict):
            raise ValueError("Invalid stats supplied.")

        # Check if 'gen' is a positive integer.
        if not isinstance(gen, int) or gen <= 0:
            raise ValueError("'gen' must be a positive integer.")

        # Check if 'height' and 'weight' are non-negative floats.
        if (not isinstance(height, (float, int)) or height < 0 or not isinstance(weight, (float, int)) or weight < 0):
            raise ValueError("'height' and 'weight' must be non-negative floats.")

        # Check if 'egg_groups' is a tuple with at least one string.
        if (not isinstance(egg_groups, tuple) or not egg_groups or not all(isinstance(group, str) or group is None for group in egg_groups)):
            raise ValueError("'egg_groups' must be a tuple with at least one string.")

        # Check if 'genders' is a tuple with two elements, each being None or a float.
        if not isinstance(genders, tuple) or len(genders) != 2 or not all((g is None or isinstance(g, (float, int))) for g in genders):
            raise ValueError("'genders' must be a tuple with two elements, each being None or a float.")

        # Check if 'catch_rate' is an integer.
        if not isinstance(catch_rate, int):
            raise ValueError("'catch_rate' must be an integer.")

        # Basic info, like the national dex number, name, debut generation and types.
        self.dex_num: int = dex_num
        self.name: str = name
        self.gen: int = gen
        self.type1: str = type1
        self.type2: str | None = type2  # If the Pokémon is monotype, this will be None.

        # Dictionary containing stats, formatted as: {HP, ATK, DEF, SP_ATK, SP_DEF, SPD}.
        self.stats: dict[str, int] = stats

        # Dictionary for abilities of the Pokémon, format: {first, second, hidden}.
        self.abilities: dict[str, str | None] = abilities

        # Height and weight in SI units.
        self.height: float = height
        self.weight: float = weight

        # Tuple for the egg groups, always non-empty.
        self.egg_groups: tuple[str, str | None] = egg_groups

        # Tuple for the gender ratio, format: (male, female) as percentages.
        self.genders: tuple[float | None, float | None] = genders

        # Catch rate for the Pokémon, always between 3 (low catch rate) and 255 (high catch rate).
        self.catch_rate: int = catch_rate

    def __str__(self) -> str:
        """Formatted display of the Pokémon objects. 
        This will only show the basic info, like name, generation and type.

        Returns
        -------
        str
            A formatted string with the basic info. 
        """

        # Color the generation number and the typings, based on GEN_COLORS and TYPE_COLORS values.
        gen = self._color_gen()
        types = self._color_types()

        return f"{gen}{self.name:<15}{types}"

    def print_no_types(self) -> str:
        """Method to print the Pokémon with
        the type information hidden.

        Returns
        -------
        str
            Same formatted string as __str__ 
            but with the types removed.
        """

        gen = self._color_gen()

        return f"{gen}{self.name:<15}"

    def __eq__(self, other: Pokemon) -> bool:
        """Equality Comparison Method (__eq__)

        Determines whether the current instance is equal to another instance of the Pokémon class.
        The other object has to be of the Pokémon class, if not, it always returns False. 

        Parameters
        ----------
        other : pokemon
            The other Pokémon instance to compare for equality.

        Returns
        -------
        bool
            True if all attributes of the two instances are equal, False otherwise.
        """

        if isinstance(other, type(self)):
            return all(getattr(self, attr) == getattr(other, attr) for attr in vars(self))
        return False

    def __lt__(self, other: Pokemon) -> bool:
        """Less-than check, implements the < operator
        on the Pokemon class. A Pokemon object is considered
        'less-than' if the other object's dex_num is greater. 

        Parameters
        ----------
        other : Pokemon
            The other Pokemon object to compare to.

        Returns
        -------
        bool
            Returns true if self is less than other.
        """

        return self.dex_num < other.dex_num

    def show_basics(self) -> None:
        """Method to display the basic information of a 
        Pokémon object. This displays the same information
        as just printing the object, but it is formatted differently.
        """

        print(f"National Dex Number: {GEN_COLORS[self.gen]}{self.dex_num}\x1b[0;0m")
        print(f"Name: {self.name}")
        print(f"Introduced in generation: {GEN_COLORS[self.gen]}{self.gen}\x1b[0;0m")

        print(f"Type: {self._color_types()}")

    def info(self) -> None:
        """Method to display all the info related to
        the Pokémon class. 
        """

        print("========= BASICS =========")
        self.show_basics()
        print()

        print("========= STATS =========")
        self.show_stats()
        print()

        print("========= GENDER RATIO =========")
        self.show_gender_ratio()
        print()

        print("========= HEIGHT, WEIGHT =========")
        self.show_height_and_weight()
        print()

        print("========= ABILITIES =========")
        self.show_abilities()
        print()

        print("========= EGG GROUPS =========")
        self.show_egg_groups()
        print()

    def _print_stat(self, stat_name: str, stat_value: int) -> None:
        """Helper function to color and display a stat
        in the terminal. The function will calculate the
        number of boxes and find the associated color
        of the stat to display.

        Parameters
        ----------
        stat_name : str
            The name of the stat to display.
        stat_value : int
            The base stat value for the Pokémon.
        """

        print(f"{stat_name} : {stat_value}\t", end="")

        num_boxes = int((stat_value/MAX_STAT)*MAX_STAT_DISPLAY_SIZE)

        # Stat coloring scheme:
        # red       : 1  - 29
        # orange    : 30 - 59
        # yellow    : 60 - 89
        # green     : 90 - 119
        # dark green: 120 - 149
        # light blue: 150 - 255

        # Determine which color to use for the stat.
        color_ranges = {
            (1, 30): 88,      # Red.
            (30, 60): 202,    # Orange.
            (60, 90): 190,    # Yellow.
            (90, 120): 40,    # Green.
            (120, 150): 29,   # Dark green.
            (150, 256): 12    # Light blue.
        }

        # Find which color to use for the stat.
        for range_, color in color_ranges.items():
            if stat_value in range(*range_):
                break

        # Give a visual indication of the stat
        for _ in range(num_boxes):
            print(f"\x1b[38;5;{color}m{chr(9646)}\x1b[0;0m", end="")
        print()

    def show_stats(self) -> None:
        """Display the Pokémon base stats in the terminal. 
        This method will color-code the stats in a similar
        manner as https://pokemondb.net.
        """

        pok_hp = self.stats['HP']
        pok_atk = self.stats['ATK']
        pok_def = self.stats['DEF']
        pok_sp_atk = self.stats['SP_ATK']
        pok_sp_def = self.stats['SP_DEF']
        pok_spd = self.stats['SPD']

        # Format, color and display each stat in the terminal.
        self._print_stat("HP     ", pok_hp)
        self._print_stat("ATK    ", pok_atk)
        self._print_stat("DEF    ", pok_def)
        self._print_stat("SP. ATK", pok_sp_atk)
        self._print_stat("SP. DEF", pok_sp_def)
        self._print_stat("SPD    ", pok_spd)

        stat_total = pok_hp + pok_atk + pok_def + pok_sp_atk + pok_sp_def + pok_spd
        print(f"Total   : {stat_total}")

    def show_gender_ratio(self) -> None:
        """Method to display the gender ratio
        for a Pokémon. Formatted as: % male, % female.
        """

        male, female = self.genders

        if male is None and female is None:
            print(f"\x1b[38;5;103mGenderless\x1b[0;0m")
        else:
            # Male gender ratio shown in blue and female in pink.
            # Print the percentage ratio as: % male, % female.
            male_color = 4
            female_color = 200
            print(f"\x1b[38;5;{male_color}m{male}% male\x1b[0;0m", end="")
            print(f", \x1b[38;5;{female_color}m{female}% female\x1b[0;0m")

    def show_egg_groups(self) -> None:
        """Method to display all the egg groups
        for the Pokémon, may be one or two. 
        """

        group1, group2 = self.egg_groups

        if group2 is None:
            # If the Pokémon has only one egg group.
            print(f"Egg group(s): {group1}")
        else:
            print(f"Egg group(s): {group1}, {group2}")

    def show_abilities(self) -> None:
        """Method to print the abilities of the Pokémon,
        some Pokémon only have one ability. 
        """

        # Extract the abilities, ability2 and the hidden ability may be None.
        ability1 = self.abilities.get("first")
        ability2 = self.abilities.get("second")
        hidden = self.abilities.get("hidden")

        print(f"First ability: {ability1}\t\t", end="")

        if ability2 is not None:
            print(f"Second ability: {ability2}\t\t", end="")

        if hidden is not None:
            print(f"Hidden ability: {hidden}", end="")

        print()

    def show_height_and_weight(self) -> None:
        """Method to display the height and weight
        of the Pokémon. The information is only shown
        in SI units. 
        """

        print(f"Height: {self.height} m\t", end="")
        print(f"Weight: {self.weight} kg")

    def _color_types(self) -> str:
        """Private method to color the type of a Pokémon
        object. 

        Returns
        -------
        str
            A formatted string with the types and the added color. 
        """

        return f"{self._get_type_color(self.type1)}{self._get_type_color(self.type2)}"

    def _color_gen(self) -> str:
        """Private method to color the Pokémon's dex number 
        based on which generation they are in.

        Returns
        -------
        str
            Colored version of the national dex number as a string.
        """

        return f"{GEN_COLORS[self.gen]}{self.dex_num:<10}\x1b[0;0m"

    def _get_type_color(self, type: str | None) -> str:
        """Private method to map the type to a colored 
        text type to be displayed in the terminal. 

        Parameters
        ----------
        type : str | None
            The type to color, the type can be None, like for
            Pokémon with no second type. 

        Returns
        -------
        str
            The type formatted as a colored string or
            the empty string if type is None.

        Raises
        ------
        ValueError
            Thrown if the type is not None or any of the valid Pokémon types. 
        """

        if type is None or type == "":
            # If None, the Pokémon has no second type, return empty string.
            return ""

        if type in TYPE_COLORS.keys():
            # Get the corresponding color for the type and format it.
            return f"\x1b[38;5;{TYPE_COLORS[type]}m{type:10}\x1b[0;0m"

        raise ValueError("Invalid type argument.")


# Dictionary of colors, one for each generation.
GEN_COLORS: dict[int, str] = {
    1: "\x1b[38;5;1m",        # The values corresponding to each key
    2: "\x1b[38;5;87m",       # makes the text in the terminal
    3: "\x1b[38;5;40m",       # a different color, depending on the generation.
    4: "\x1b[38;5;69m",
    5: "\x1b[38;5;246m",
    6: "\x1b[38;5;126m",
    7: "\x1b[38;5;208m",
    8: "\x1b[38;5;200m",
    9: "\x1b[38;5;92m",
}

TYPE_COLORS: dict[str, int] = {
    # There are a total of 18 types in Pokémon.
    "Dark": 239,
    "Fire": 202,
    "Psychic": 200,
    "Water": 26,
    "Normal": 222,
    "Fairy": 213,
    "Grass": 34,
    "Ice": 44,
    "Ghost": 92,
    "Bug": 106,
    "Ground": 3,
    "Electric": 226,
    "Fighting": 52,
    "Flying": 122,
    "Rock": 95,
    "Dragon": 57,
    "Poison": 90,
    "Steel": 103,
}


if __name__ == "__main__":

    glimmora = Pokemon(
        970, 'Glimmora', 9, 'Rock', 'Poison',
        {
            'HP': 83,
            'ATK': 55,
            'DEF': 90,
            'SP_ATK': 130,
            'SP_DEF': 81,
            'SPD': 86
        },
        {
            'first': 'Toxic Debris',
            'second': None,
            'hidden': 'Corrosion'
        },
        1.5, 45.0,
        ('Mineral', None),
        (50, 50), 25
    )

    glimmora.info()
