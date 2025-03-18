import re
import sqlite3
import unicodedata

from .exceptions_database import (PokemonGenericError,
                                  PokemonInvalidGenerations,
                                  PokemonInvalidTypes, PokemonSyntaxError,
                                  PokemonTableDoesNotExist)
from .pokemon import Pokemon
from .pokemon_data import (generation1, generation2, generation3, generation4,
                           generation5, generation6, generation7, generation8,
                           generation9)
from .pokemon_parser import PokemonParser

__version__ = "2.0.3"
__author__ = "Jørn Olav Jensen"

DATABASE_NAME = "./game_api/backend/pokemon.db"
CURRENT_GENS = 9  # Currently, there are 9 generations of Pokémon.

valid_types = ["normal", "water", "fire", "grass", "fighting", "psychic", "ice", "electric",
               "dragon", "fairy", "dark", "ghost", "steel", "rock", "ground", "flying", "bug", "poison"]

pokemon_schema = '''pokemon(dex_num INTEGER PRIMARY KEY ASC, 
                            name varchar(15) NOT NULL, 
                            gen INTEGER NOT NULL, 
                            type1 varchar(10) NOT NULL, 
                            type2 varchar(10), 
                            HP INTEGER NOT NULL, 
                            ATK INTEGER NOT NULL, 
                            DEF INTEGER NOT NULL, 
                            SP_ATK INTEGER NOT NULL, 
                            SP_DEF INTEGER NOT NULL, 
                            SPD INTEGER NOT NULL, 
                            ability1 varchar(20) NOT NULL, 
                            ability2 varchar(20), 
                            hidden varchar(20), 
                            height NUMERIC(1,1) NOT NULL, 
                            weight NUMERIC(1,1) NOT NULL, 
                            egg_group1 varchar(15) NOT NULL, 
                            egg_group2 varchar(15), 
                            male NUMERIC(3,1), 
                            female NUMERIC(3,1), 
                            catch_rate INTEGER NOT NULL,
                            search_name varchar(15) NOT NULL
                            )
                '''

guessing_schema = '''guessing(dex_num INTEGER PRIMARY KEY ASC, 
                            name varchar(15) NOT NULL, 
                            gen INTEGER NOT NULL, 
                            type1 varchar(10) NOT NULL, 
                            type2 varchar(10), 
                            HP INTEGER NOT NULL, 
                            ATK INTEGER NOT NULL, 
                            DEF INTEGER NOT NULL, 
                            SP_ATK INTEGER NOT NULL, 
                            SP_DEF INTEGER NOT NULL, 
                            SPD INTEGER NOT NULL, 
                            ability1 varchar(20) NOT NULL, 
                            ability2 varchar(20), 
                            hidden varchar(20), 
                            height NUMERIC(1,1) NOT NULL, 
                            weight NUMERIC(1,1) NOT NULL, 
                            egg_group1 varchar(15) NOT NULL, 
                            egg_group2 varchar(15), 
                            male NUMERIC(3,1), 
                            female NUMERIC(3,1), 
                            catch_rate INTEGER NOT NULL
                            )
                '''


class PokemonDatabase:
    """
    PokemonDatabase Class

    Interface for the underlying sqlite database used. 

    Attributes
    ----------
    con : Connection
        The sqlite database connection.

    cursor : Cursor
        The database cursor. 

    Methods
    -------
    setup_guessing(self, gens: list[int]) -> None
        Method to setup the guessing table in the database. Used to keep track of the users progress.
    update_database(self) -> None
        Method for launching an update of the database contents. 
    get_pokemon_by_gens(table: str, gens: list[int], types: list[str] | None = None) -> list[Pokemon]
        Method to fetch Pokémon from the database, based on generation and types. 
    get_pokemon_by_name(self, name: str) -> list[Pokemon]
        Method to fetch a Pokémon based on the name. 
    get_pokemon_by_stat(self, table: str, stat: str, min: int | str, max: int | str) -> list[Pokemon]
        Method to fetch Pokémon based a stat and its range.
    get_pokemon_by_stat_total(self, table: str, min: int, max: int) -> list[Pokemon]
        Method to fetch Pokémon based on the stat total. 
    get_pokemon_by_ability(self, table: str, ability: str) -> list[Pokemon]
        Method to fetch Pokémon based on their ability. Hidden ability does not matter.
    get_pokemon_by_type(self, table: str, expression: str, gens: list[int]) -> list[Pokemon]
        Method to fetch Pokémon based on their type, can also filter on generation. 
    update_pokemon_name(self, table: str, dex_num: int, name: str) -> None
        Method to insert the name of the provided Pokémon into the table. 
    """

    def __init__(self) -> None:
        """Creates the database for storing 
        the Pokémon data and sets up the corresponding
        table.
        """

        self.con = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.con.cursor()

        sql_create_table = f'''CREATE TABLE IF NOT EXISTS {pokemon_schema}'''
        self.cursor.execute(sql_create_table)

        self.cursor.close()

    # =================== CREATE/UPDATE METHODS =================== #

    def setup_guessing(self, gens: list[int]) -> None:
        """Method to create the guessing table
        used to store the users guesses. Method
        deletes already existing tables.

        Parameters
        ----------
        gens : list[int]
            The generations the user wants the
            guessing table to contain.
        """

        self._connect()

        self.cursor.execute("DROP TABLE IF EXISTS guessing")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {guessing_schema}")

        self._populate_guessing(gens)

        self.con.commit()
        self._close()

    def _populate_guessing(self, gens: list[int]) -> None:
        """Helper method to insert the Pokémon information
        into the guessing table.

        Parameters
        ----------
        gens : list[int]
            Which generations of Pokémon to insert. 
        """

        query = 'SELECT * FROM pokemon WHERE ' + ''.join(
            f'gen = {gen} OR ' if gen != max(gens) else f'gen = {gen}'
            for gen in gens
        )

        results = self.cursor.execute(query).fetchall()

        insert_query = '''INSERT INTO guessing(
                        dex_num, name, gen, type1, type2, 
                        HP, ATK, DEF, SP_ATK, SP_DEF, SPD, 
                        ability1, ability2, hidden, 
                        height, weight, 
                        egg_group1, egg_group2, 
                        male, female, catch_rate
                        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''

        for pokemon in results:
            # We don't store the name in the guessing table!
            dex_num, _, gen, type1, type2, HP, ATK, DEF, SP_ATK, SP_DEF, SPD, ability1, ability2, hidden, height, weight, egg_group1, egg_group2, male, female, catch_rate = pokemon
            self.cursor.execute(insert_query,
                                (dex_num, "?", gen, type1, type2, HP, ATK, DEF, SP_ATK, SP_DEF, SPD, ability1, ability2, hidden, height, weight, egg_group1, egg_group2, male, female, catch_rate)
                                )

        self.con.commit()

    def _populate(self, pokemon_data: tuple) -> None:
        """Helper method to fill in the
        Pokémon data into the database.

        Parameters
        ----------
        pokemon_data : tuple
            The data to insert, the tuple contains all
            the information needed for the underlying Pokemon class.
        """

        dex_num, name, gen, type1, type2, HP, ATK, DEF, SP_ATK, SP_DEF, SPD, ability1, ability2, hidden, height, weight, egg_group1, egg_group2, male, female, catch_rate = pokemon_data

        database_tuple = (
            dex_num, name, gen, type1, type2,
            HP, ATK, DEF, SP_ATK, SP_DEF, SPD,
            ability1, ability2, hidden,
            height, weight,
            egg_group1, egg_group2,
            male, female,
            catch_rate, self._filter_pokemon_name(name)
        )

        query = '''INSERT INTO pokemon(
                        dex_num, name, gen, type1, type2, 
                        HP, ATK, DEF, SP_ATK, SP_DEF, SPD, 
                        ability1, ability2, hidden, 
                        height, weight, 
                        egg_group1, egg_group2, 
                        male, female, catch_rate, search_name
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''

        self.cursor.execute(query, database_tuple)
        self.con.commit()

    def update_database(self) -> None:
        """Method to update the information in the database.
        """

        self._connect()

        self.cursor.execute('DROP TABLE IF EXISTS pokemon')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {pokemon_schema}')

        for pokemon in generation1.pokedex:
            self._populate(pokemon)

        for pokemon in generation2.pokedex:
            self._populate(pokemon)

        for pokemon in generation3.pokedex:
            self._populate(pokemon)

        for pokemon in generation4.pokedex:
            self._populate(pokemon)

        for pokemon in generation5.pokedex:
            self._populate(pokemon)

        for pokemon in generation6.pokedex:
            self._populate(pokemon)

        for pokemon in generation7.pokedex:
            self._populate(pokemon)

        for pokemon in generation8.pokedex:
            self._populate(pokemon)

        for pokemon in generation9.pokedex:
            self._populate(pokemon)

        self._close()

    # =================== DATABASE HELPER METHODS =================== #

    def _connect(self) -> None:
        self.con = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.con.cursor()

    def _close(self) -> None:
        self.cursor.close()

    # =================== PARSER METHODS =================== #

    def _validate_generation(self, gens: list[int]) -> bool:
        """Helper method to check if a list of numbers 
        is a valid list for Pokémon generations. 
        Valid means a list consisting of integer values
        from 1 to 9. Also checks the types of the entries in the list.

        Parameters
        ----------
        gens : list[int]
            The list of numbers (generations) to check.

        Returns
        -------
        bool
            True if the list is valid, False otherwise.
        """

        # Check both the type and the value.
        for gen in gens:
            if not isinstance(gen, int):
                return False

            if gen > CURRENT_GENS or gen <= 0:
                return False

        return True

    def _validate_types(self, types: list[str]) -> bool:
        """Support method to validate a list
        for correct Pokémon types. The check is not
        case sensitive, so capital types will also work. 
        Method will check the type of the entries 
        in addition to their values. 

        Parameters
        ----------
        types : list[str]
            The list to check for correctness.

        Returns
        -------
        bool
            True if the list contains valid Pokémon types, 
            False otherwise. 
        """

        for type in types:
            # Verify that the types in the list are correct.
            if not isinstance(type, str):
                return False

        # Check if all the types are valid types, if yes, return True.
        return all(typ.lower() in valid_types for typ in types)

    def _verify_input(self, expression: str) -> bool:
        """Helper method to check that only valid
        words are present in the expression 
        before parsing it. Does not check the syntax,
        only the words themselves. 

        Parameters
        ----------
        expression : str
            The input to check.

        Returns
        -------
        bool
            return True if valid, False otherwise.
        """

        pattern_types = r"normal|water|fire|grass|fighting|psychic|ice|electric|dragon|fairy|dark|ghost|steel|rock|ground|flying|bug|poison"
        pattern_operators = r"NOT|AND|OR"
        pattern_gens = r"p1|p2|p3|p4|p5|p6|p7|p8|p9"
        valid_word_pattern = rf'''^({pattern_operators}|{pattern_types}|{pattern_gens}
                             |\s*|\(|\))( ({pattern_operators}|{pattern_types}|{pattern_gens}
                             |\s*|\(|\)))*$'''

        return bool(re.fullmatch(valid_word_pattern, expression))

    def _filter_pokemon_name(self, name: str) -> str:
        """Convert a Pokémon name to a lower case version
        removing all special characters and spaces.
        """

        # Replace all special characters, such as é, á.
        filtered_name = unicodedata.normalize("NFD", name).encode("ascii", "ignore").decode("utf-8")

        # Only keep ascii characters and numbers.
        return re.sub(r"[^a-z0-9]", "", filtered_name.lower())

    def _construct_sql_query(self, table: str, query: tuple | str) -> str:
        """Helper method for _type_query_parser. This method 
        takes a `table` name and a `query` tuple or string as input 
        and constructs an SQL query string based on the provided parameters.
        The `query` can either be a simple condition (string) or a tuple 
        representing a complex condition with an operation (AND, OR, NOT)
        and two arguments.

        Parameters
        ----------
        table : str
            The table to fetch the Pokémon from.
        query : tuple | str
            The parsed query to convert to SQL.

        Returns
        -------
        str
            A SQL query obtained from the parsed query.
            An exception is raised if an error occurred in the parsing.

        Raises
        ------
        PokemonSyntaxError
            If the query could not be parsed properly.
        """

        def construct_simple_query(query: str) -> str:
            return f'''
                    SELECT * 
                    FROM {table} 
                    WHERE type1="{query.capitalize()}" OR type2="{query.capitalize()}"
                    '''

        def construct_union_query(query1: str, query2: str) -> str:
            return f'''
                    SELECT * 
                    FROM ({query1}) AS FIRST 
                    UNION 
                    SELECT * 
                    FROM ({query2}) AS SECOND
                    '''

        def construct_intersect_query(query1: str, query2: str) -> str:
            return f'''
                    SELECT * 
                    FROM ({query1}) 
                    INTERSECT 
                    SELECT * 
                    FROM ({query2})
                    '''

        def construct_except_query(query1: str, query2: str) -> str:
            return f'''
                    SELECT * 
                    FROM ({query1}) 
                    EXCEPT 
                    SELECT * 
                    FROM ({query2})
                    '''

        # If the query is just a string, it corresponds to a type, so return a simple query.
        if isinstance(query, str):
            return construct_simple_query(query)

        # If the query is a tuple, the first entry is the operation and the next are the arguments.
        operation, arg1, arg2 = query

        if operation == "AND":
            if self._validate_types([arg1, arg2]):
                # If both arguments are valid types, intersect the two simple queries.
                return construct_intersect_query(construct_simple_query(arg1), construct_simple_query(arg2))
            elif self._validate_types([arg1]):
                # In this case, arg2 needs more parsing before intersecting.
                return construct_intersect_query(construct_simple_query(arg1), self._construct_sql_query(table, arg2))
            elif self._validate_types([arg2]):
                # Likewise, arg1 needs more parsing.
                return construct_intersect_query(self._construct_sql_query(table, arg1), construct_simple_query(arg2))
            else:
                # Both arguments needs further parsing.
                return construct_intersect_query(self._construct_sql_query(table, arg1), self._construct_sql_query(table, arg2))

        elif operation == "OR":
            if self._validate_types([arg1, arg2]):
                # If both arguments are valid types, union the two simple queries.
                return construct_union_query(construct_simple_query(arg1), construct_simple_query(arg2))
            elif self._validate_types([arg1]):
                # Here arg2 needs to be parsed more.
                return construct_union_query(construct_simple_query(arg1), self._construct_sql_query(table, arg2))
            elif self._validate_types([arg2]):
                # arg1 needs to be handled.
                return construct_union_query(self._construct_sql_query(table, arg1), construct_simple_query(arg2))
            else:
                # Both arguments need to be parsed before taking the union.
                return construct_union_query(self._construct_sql_query(table, arg1), self._construct_sql_query(table, arg2))

        elif operation == "NOT":
            if self._validate_types([arg1, arg2]):
                # Both arguments being types, except the simple queries.
                return construct_except_query(construct_simple_query(arg1), construct_simple_query(arg2))
            elif self._validate_types([arg1]):
                # Parse arg2 before doing the except.
                return construct_except_query(construct_simple_query(arg1), self._construct_sql_query(table, arg2))
            elif self._validate_types([arg2]):
                # Likewise, but arg1 needs more parsing.
                return construct_except_query(self._construct_sql_query(table, arg1), construct_simple_query(arg2))
            else:
                # Both arguments needs to be handled before we can except.
                return construct_except_query(self._construct_sql_query(table, arg1), self._construct_sql_query(table, arg2))
        else:
            raise PokemonSyntaxError(f"Error encountered in the parsing of the query. Could not parse: {query}")

    def _type_query_parser(self, table: str, expression: str) -> str:
        """Helper method to the get_pokemon_by_type
        method. This method handles the parsing of
        the expression into an SQL query. This method 
        will also verify that the expression is 
        syntactically correct. 

        Parameters
        ----------
        table : str
            Which table to perform the query on.
        expression : str
            The input to convert to an SQL query. 

        Returns
        -------
        str
            A SQL query, that will grant the request 
            from the expression, or an exception if the
            request could not be granted.

        Raises
        ------
        PokemonSyntaxError
            If the expression does not satisfy the proper syntax or
            contain words not supported.
        """

        # Lowercase the expression, add spaces and make sure the operators are capitalized.
        expression = expression \
            .lower() \
            .replace('and', ' AND ') \
            .replace(' or ', ' OR ') \
            .replace(' not ', ' NOT ') \
            .replace('(', '( ') \
            .replace(')', ' )') \

        # Guard against expressions that contain any invalid words, syntax is not checked, only characters.
        if not self._verify_input(expression):
            raise PokemonSyntaxError(f"Invalid words encountered in the expression: {expression}")

        # Split the expression based on the spaces, to get a list of tokens.
        tokens = expression.split()

        parser = PokemonParser(tokens)
        parsed_query = parser.parse()

        return self._construct_sql_query(table, parsed_query)

    # =================== CONVERTER METHODS ===================

    def _convert_to_pokemon(self, database_record: tuple) -> Pokemon:
        """Helper method to convert a database record to
        a Pokémon object. The received values are not 
        checked for correctness. 

        Parameters
        ----------
        database_record : tuple
            A record from the `pokemon` table, 
            which contains 21 columns.

        Returns
        -------
        Pokemon
            A Pokémon object, with the information from 
            the database record.
        """

        # Extract all the information from the database record. (21 columns)
        (
            dex_num, name, gen, type1, type2,
            hp, atk, defs, sp_atk, sp_def, speed,
            ability1, ability2, hidden,
            height, weight,
            egg_group1, egg_group2,
            male, female,
            catch_rate
        ) = database_record

        stats = {'HP': hp, 'ATK': atk, 'DEF': defs,
                 'SP_ATK': sp_atk, 'SP_DEF': sp_def, 'SPD': speed}

        abilities = {'first': ability1, 'second': ability2, 'hidden': hidden}

        egg_groups = (egg_group1, egg_group2)

        genders = (male, female)

        return Pokemon(dex_num, name, gen, type1, type2,
                       stats, abilities, height, weight,
                       egg_groups=egg_groups, genders=genders,
                       catch_rate=catch_rate)

    def _convert_to_pokemon_list(self, result: list[tuple]) -> list[Pokemon]:
        """Helper method to convert the result
        from a database query (list of database records, or tuples)
        to a list of Pokémon objects. 

        Parameters
        ----------
        result : list[tuple]
            A list of database records. 

        Returns
        -------
        list[Pokemon]
            A list of Pokémon objects.
        """

        return [self._convert_to_pokemon(pokemon) for pokemon in result]

    # ====================== GET METHODS ====================== #

    def get_pokemon_by_gens(self, table: str, gens: list[int], types: list[str] | None = None) -> list[Pokemon]:
        """Method to fetch all the Pokémon in the requested table. 
        Method can filter based on the generations and types provided. 
        Note that the types provided must have the first letter
        capitalized. 

        Parameters
        ----------
        table : str
            The database table to fetch the Pokémon data from.
        gens : list[int]
            The generations the Pokémon should be from. The order 
            of the generations does not matter.
        types : list[str] | None, optional
            Types wanted, by default None. If None, 
            all types are returned, otherwise filter based
            on all the types specified. The ordering of the types
            does not matter. Types have to be capitalized on 
            the first letter.

        Returns
        -------
        list[Pokemon]
            A list of Pokémon objects, resulting from the request
            or an empty list if the query did not find any Pokémon
            satisfying the request. 

        Raises
        ------
        PokemonInvalidGenerations
            If the generations provided are invalid.

        PokemonInvalidTypes
            If the specified types are invalid.
        """

        self._connect()

        # Guard against invalid generations.
        if not self._validate_generation(gens):
            raise PokemonInvalidGenerations(f"Invalid Pokémon generation. Only 1-9 are allowed. Got: {gens}")

        # Guard against invalid types.
        if types and not self._validate_types(types):
            raise PokemonInvalidTypes(f"Invalid Pokémon type encountered. Got: {types}")

        # Needed in case the list is not in increasing order,
        # the query constructions assumes the generations are sorted.
        gens.sort()

        # Construct a query that has every generation requested, no filter on typing (yet).
        query = f'SELECT * FROM {table} WHERE ' + ''.join(f'gen = {gen} OR ' if gen != max(gens) else f'gen = {gen}' for gen in gens)

        if types:
            # Add filtering on types, if any.
            type_filter = ' INTERSECT '.join(f'SELECT * FROM {table} WHERE type1="{p_type.title()}" OR type2="{p_type.title()}"' for p_type in types)
            query += f' INTERSECT {type_filter}'

        result = self.cursor.execute(query).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

    def get_pokemon_by_name(self, table: str, name: str) -> list[Pokemon]:
        """Method to get all the available data
        for the provided Pokémon name.

        Parameters
        ----------
        table : str
            Which table to fetch from.

        name : str
            Name of the Pokémon to fetch the
            data for. Name is not case sensitive. 

        Returns
        -------
        list[Pokemon]
            A list of the corresponding Pokémon objects.
            If the Pokémon does not exist, an empty 
            list is returned. 

        Raises
        ------
        PokemonTableDoesNotExist
            If the provided table does not exist.

        PokemonSyntaxError
            If an underlying syntax error occurred.
        """

        self._connect()

        name = name.replace("'", "").replace("-", " ").replace(":", "")

        name = " ".join(word.capitalize() for word in name.split())

        # FIXME: Find better solution.
        if name == "Kommo O":
            name = "Kommo o"

        query = f'SELECT * FROM {table} WHERE REPLACE(REPLACE(REPLACE(REPLACE(name, ".", ""), "\'", ""), "-", " "), ":", "") = "{name}"'

        try:
            result = self.cursor.execute(query).fetchall()
        except sqlite3.OperationalError as e:
            error_msg = str(e)

            if "no such table" in error_msg:
                raise PokemonTableDoesNotExist(f"{e}") from e
            elif "syntax error" in error_msg:
                raise PokemonSyntaxError(f"{e}") from e
        finally:
            self._close()

        return self._convert_to_pokemon_list(result) if table == "pokemon" else result

    def get_pokemon_by_stat(self, table: str, stat: str, min: int | str, max: int | str) -> list[Pokemon]:
        """Method to fetch all Pokémon based on a certain stat
        in a provided range. 

        Parameters
        ----------
        table : str
            The database table to fetch from.
        stat : str
            Which stat to filtered on. Valid options are:
            hp, atk, def, sp_atk, sp_def and spd. Not case
            sensitive. 
        min : int | str
            Minimum stat value to include. Input must
            be an integer or an integer as a string. 
        max : int | str
            Maximum stat value to include, same rules here
            as for min. 

        Returns
        -------
        list[Pokemon]
            All Pokémon having the stat in the range min-max as a list. 
            The list is empty if nothing is found.

        Raises
        ------
        ValueError
            If the stat requested does not exist or the
            stat given is not a valid number. 

        TypeError
            If the min or max types are invalid. ValueError
        """

        self._connect()

        valid_stats = {"hp", "atk", "def", "sp_atk", "sp_def", "spd"}

        if stat.lower() not in valid_stats:
            raise ValueError(f"Invalid Pokémon stat encountered: {stat}")

        if not isinstance(min, (str, int)):
            raise TypeError("min must be either integer type or string.")

        if not isinstance(max, (str, int)):
            raise TypeError("max must be either integer type or string.")

        if isinstance(min, str) and not min.isdecimal():
            raise ValueError(f"Invalid min value encountered: {min}")

        if isinstance(max, str) and not max.isdecimal():
            raise ValueError(f"Invalid max value encountered: {max}")

        query = f'SELECT * FROM {table} WHERE {stat} BETWEEN ? AND ? ORDER BY {stat}'
        result = self.cursor.execute(query, (min, max)).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

    def get_pokemon_by_stat_total(self, table: str, min: int, max: int) -> list[Pokemon]:
        """Method to fetch Pokémon by their stat total, 
        being between min and max. 

        Parameters
        ----------
        table : str
            Which table to search in.
        min : int
            Minimum stat total for the Pokémon to include.
        max : int
            Maximum stat total for the Pokémon to include. 

        Returns
        -------
        list[Pokemon]
            A list of Pokémon having a stat total
            between min and max (both inclusive).

        Raises
        ------
        ValueError
            If the stat given is not a valid number. 

        TypeError
            If the min or max types are invalid. 
        """

        self._connect()

        if not isinstance(min, (str, int)):
            raise TypeError("min must be either integer type or string.")

        if not isinstance(max, (str, int)):
            raise TypeError("max must be either integer type or string.")

        if isinstance(min, str) and not min.isdecimal():
            raise ValueError(f"Invalid min value encountered: {min}")

        if isinstance(max, str) and not max.isdecimal():
            raise ValueError(f"Invalid max value encountered: {max}")

        query = f'''SELECT dex_num, name, gen, type1, type2, 
                           HP, ATK, DEF, SP_ATK, SP_DEF, SPD, 
                           ability1, ability2, hidden, height, weight, 
                           egg_group1, egg_group2, male, female, catch_rate FROM (
                        SELECT *, HP + ATK + DEF + SP_ATK + SP_DEF + SPD AS total 
                        FROM {table}
                        ) AS subquery
                    WHERE total BETWEEN {min} AND {max}
                    ORDER BY total'''

        result = self.cursor.execute(query).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

    def get_pokemon_by_ability(self, table: str, ability: str) -> list[Pokemon]:
        """Method to fetch Pokémon that has the provided
        ability. Includes hidden ability.

        Parameters
        ----------
        table : str
            Which database table to fetch from.
        ability : str
            Which ability to filter the Pokémon on. 
            Not case sensitive.

        Returns
        -------
        list[Pokemon]
            A list of Pokémon objects, where each Pokémon
            in the list has the provided ability. 

        Raises
        ------
        TypeError
            If the ability provided is not of type str. 
        """

        self._connect()

        if not isinstance(ability, str):
            raise TypeError("Invalid ability type encountered. Ability must be provided as str object.")

        ability = ability.title()

        query = f'''SELECT * 
                    FROM {table} 
                    WHERE ability1 = ? OR ability2 = ? OR hidden = ?'''
        result = self.cursor.execute(query, (ability, ability, ability)).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

    def get_pokemon_by_type(self, table: str, expression: str, gens: list[int]) -> list[Pokemon]:
        """Method to fetch Pokémon based on the types specified 
        in the expression. The expression must follow the following 
        Backus–Naur form:
            query ::= ANDterm | ANDterm "NOT" query
            ANDterm ::= ORterm | ORterm "AND" ANDterm
            ORterm ::= type | type "OR" ORterm
            type ::= "(" query ")" |fire|water|grass (and so on..)            

        Parameters
        ----------
        table : str
            Which table to fetch the Pokémon from.
        expression : str
            A Pokémon type expression that includes types with the 
            AND, OR and NOT operations.
        gens : list[int]
            A list of the generations to filter the Pokémon on. 
            If empty, no filtering is done based on the generations. 
            Must be sorted in ascending order. 

        Returns
        -------
        list[Pokemon]
            A list of Pokémon objects satisfying the expression. 

        Examples
        --------
        >>> fire and dark
            # Will fetch all Pokémon that are fire and dark type.
            # All commands are independent of which type is primary and secondary typing.
        >>> water or ice
            # Will fetch all Pokémon that are water or ice type.
        >>> bug not flying
            # Will fetch Pokémon that are bug, but not flying type. 
        >>> dragon or (ice and (water or grass))
            # Will get Pokémon that are dragon type or dual type ice and water or water and grass. 
        """

        self._connect()

        try:
            sql_query = self._type_query_parser(table, expression) if expression else ''
        except PokemonSyntaxError as e:
            print(f"Syntax error: {e}")
            self._close()
            return []

        # Construct the WHERE clause if there are any generations to filter on.
        if gens:
            gens_query = ' WHERE ' + ''.join(f'gen = {gen} OR ' if gen != max(gens) else f'gen = {gen}' for gen in gens)
        else:
            gens_query = ''

        sql_query = f'SELECT * FROM ({sql_query}){gens_query}' if sql_query else f'SELECT * FROM {table}{gens_query}'

        try:
            result = self.cursor.execute(sql_query).fetchall()
        except sqlite3.OperationalError as e:
            print(f"Error in 'get_pokemon_by_type' query '{sql_query}' invalid.")
            print(f"Error message: {e}")
            return []

        self._close()

        return self._convert_to_pokemon_list(result)

    def update_pokemon_name(self, table: str, dex_num: int, name: str) -> None:
        """Method to insert a Pokémon into a database,
        used to update the guessing table. Fills in the generation,
        name and types.

        Parameters
        ----------
        table : str
            Which table to insert into (guessing table).
        dex_num : int
            The PokéDex number of the Pokémon to update.
        name : str
            The name of the Pokémon to update the information for.
        """

        # Pop the list, there is only one element in the list.
        pokemon_to_add = self.get_pokemon_by_name("pokemon", name).pop(0)

        self._connect()

        # Remove -, making the capitalize method work properly based on spaces alone.
        name = name.replace("-", " ")
        name = " ".join(word.capitalize() for word in name.split())

        # FIXME: Make sure the last o in Jangmo-o, Hakamo-o and Kommo-o are not capitalized.
        # This causes the problem with these Pokémon.

        convert_names = {"Farfetchd": "Farfetch'd",
                         "Mr Mime": "Mr. Mime",
                         "Sirfetchd": "Sirfetch'd",
                         "Mr Rime": "Mr. Rime",
                         "Ho Oh": "Ho-Oh",
                         "Jangmo O": "Jangmo-o",
                         "Hakamo O": "Hakamo-o",
                         "Kommo O": "Kommo-o",
                         "Porygon Z": "Porygon-Z",
                         "Wo Chien": "Wo-Chien",
                         "Chien Pao": "Chien-Pao",
                         "Ting Lu": "Ting-Lu",
                         "Chi Yu": "Chi-Yu",
                         "Type Null": "Type: Null"
                         }

        # Convert the name if in the dictionary as a special case, otherwise use default name.
        name = convert_names.get(name, name)

        print(name)

        gen = pokemon_to_add.gen
        type1 = pokemon_to_add.type1
        type2 = pokemon_to_add.type2

        update_query = f'''
            UPDATE {table}
            SET name = ?, gen = ?, type1 = ?, type2 = ?
            WHERE dex_num = ?
        '''

        self.cursor.execute(update_query, (name, gen, type1, type2, dex_num))
        self.con.commit()

        self._close()


if __name__ == "__main__":

    pokemon_test_db = PokemonDatabase()

    pokemon_test_db.update_database()

    # Test 1.
    gens = [2, 5, 7, 8]
    types = ["rock", "fire"]

    # Test 2.
    name = "Chandelure"

    # Test 3.
    stat = "ATK"
    stat_min = 150
    stat_max = 200

    # Test 4.
    stat_total_min = 650
    stat_total_max = 700

    # Test 5.
    ability = "Volt Absorb"

    # Test 6.
    query = "(fire AND dark) OR (grass AND dark) OR (water AND dark)"
    gens_s = [2, 3, 4, 5, 6, 7, 8, 9]

    test1 = pokemon_test_db.get_pokemon_by_gens("pokemon", gens, types)
    test2 = pokemon_test_db.get_pokemon_by_name("pokemon", name)
    test3 = pokemon_test_db.get_pokemon_by_stat("pokemon", stat, stat_min, stat_max)
    test4 = pokemon_test_db.get_pokemon_by_stat_total("pokemon", stat_total_min, stat_total_max)
    test5 = pokemon_test_db.get_pokemon_by_ability("pokemon", ability)
    test6 = pokemon_test_db.get_pokemon_by_type("pokemon", query, gens_s)

    print("\n==============================================================")
    print(f"Testing get_pokemon_by_gens with: Gens = {gens}, types = {types}.")
    print("==============================================================")

    for pok in test1:
        print(pok)

    print("\n==============================================================")
    print(f"Testing get_pokemon_by_name with: name = {name}.")
    print("==============================================================")

    for pok in test2:
        print(pok)

    print("\n==============================================================")
    print(f"Testing get_pokemon_by_stat with: STAT = {stat} from {stat_min} to {stat_max}.")
    print("==============================================================")

    for pok in test3:
        print(pok)

    print("\n==============================================================")
    print(f"Testing get_pokemon_by_stat_total with: TOTAL from {stat_total_min} to {stat_total_max}.")
    print("==============================================================")

    for pok in test4:
        print(pok)

    print("\n==============================================================")
    print(f"Testing get_pokemon_by_ability with: {ability}")
    print("==============================================================")

    for pok in test5:
        print(pok)

    print("\n==============================================================")
    print(f"Testing get_pokemon_by_type with: {query} with gens {gens_s}")
    print("==============================================================")

    for pok in test6:
        print(pok)
