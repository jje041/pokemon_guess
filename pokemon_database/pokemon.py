"""The Pokémon module. Contains the implementation of the
Pokemon class."""

from __future__ import annotations

__version__ = "2.0.0"
__author__ = "Jørn Olav Jensen"


class Pokemon:
    """
    Pokemon Class

    A class representing a Pokémon with various attributes including basic information, stats, abilities, size, and more.

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
        The height of the Pokémon in SI units.
    weight : float
        The weight of the Pokémon in SI units.
    egg_groups : tuple[str, str or None]
        A tuple representing the Pokémon's egg groups. Always non-empty.
    genders : tuple[float or None, float or None]
        A tuple representing the gender ratio in percentages. Format: (male, female).
    catch_rate : int
        The catch rate for the Pokémon in percentage.

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
                 egg_groups: tuple[str, str | None], genders: tuple[float | None, float | None], catch_rate: int) -> None:

        # Check if 'stats' is a dictionary.
        if not isinstance(stats, dict):
            raise ValueError("Invalid stats supplied.")

        # Check if 'gen' is a positive integer.
        if not isinstance(gen, int) or gen <= 0:
            raise ValueError("'gen' must be a positive integer.")

        # Check if 'height' and 'weight' are non-negative floats.
        if not (isinstance(height, (float, int)) and height >= 0) or not (isinstance(weight, (float, int)) and weight >= 0):
            raise ValueError("'height' and 'weight' must be non-negative floats.")

        # Check if 'egg_groups' is a tuple with at least one string.
        if not isinstance(egg_groups, tuple) or len(egg_groups) < 1 or not all(isinstance(group, str) or group is None for group in egg_groups):
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

        # Dictionary containing stats, format: {HP, ATK, DEF, SP_ATK, SP_DEF, SPD}.
        self.stats: dict[str, int] = stats

        # Dictionary for abilities of the Pokémon, format: {first, second, hidden}.
        self.abilities: dict[str, str | None] = abilities

        # Height and weight in SI units.
        self.height: float = height
        self.weight: float = weight

        # Tuple for the egg groups, always non-empty.
        self.egg_groups: tuple[str, str | None] = egg_groups

        # Tuple for the gender ratio, format: (male, female) percentages.
        self.genders: tuple[float | None, float | None] = genders

        # Catch rate for the Pokémon, in percentage.
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

    def __eq__(self, other: Pokemon) -> bool:
        """
        Equality Comparison Method (__eq__)

        Determines whether the current instance is equal to another instance of the Pokemon class.
        The other object has to be of the Pokémon class, if not, it always returns False. 

        Parameters
        ----------
        other : Pokemon
            The other Pokemon instance to compare for equality.

        Returns
        -------
        bool
            True if all attributes of the two instances are equal, False otherwise.
        """

        if isinstance(other, type(self)):
            return all(getattr(self, attr) == getattr(other, attr) for attr in vars(self))
        return False


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

        if type is None:
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

    bulbasaur = Pokemon(1, "Bulbasaur", 1, "Grass", "Poison", {"HP": 50}, {"ability1": "Overgrow", "ability2": None, "hidden": None}, 10, 10, ("Monster", None), (None, None), 12)
    mew = Pokemon(151, 'Mew', 1, 'Psychic', None, {
        'HP': 100, 'ATK': 100, 'DEF': 100, 'SP_ATK': 100, 'SP_DEF': 100, 'SPD': 100},
        {'first': 'Synchronize', 'second': None, 'hidden': None}, 0.4, 4.0,
        ('Undiscovered', None), (None, None), 45
    )

    print(bulbasaur)
    print(mew)
