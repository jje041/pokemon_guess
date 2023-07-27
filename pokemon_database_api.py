import re
import sqlite3
from pokemon import Pokemon
from pokemon_data import generation1, generation2, generation3, generation4, generation5, generation6, generation7, generation8, generation9
from pokemon_query_parser import PokemonParser

DATABASE_NAME = 'pokemon.db'

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
                            catch_rate INTEGER NOT NULL
                            )
                '''


class PokemonDatabase:

    def __init__(self) -> None:
        self.con = sqlite3.connect(f"{DATABASE_NAME}")
        self.cursor = self.con.cursor()

        sql_create_table = f'''CREATE TABLE IF NOT EXISTS {pokemon_schema}'''

        self.cursor.execute(sql_create_table)

        self.cursor.close()

    def _populate(self, pokemon_data: tuple) -> None:

        query = '''INSERT INTO pokemon(
                        dex_num, name, gen, type1, type2, 
                        HP, ATK, DEF, SP_ATK, SP_DEF, SPD, 
                        ability1, ability2, hidden, 
                        height, weight, 
                        egg_group1, egg_group2, 
                        male, female, 
                        catch_rate
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''

        self.cursor.execute(query, pokemon_data)
        self.con.commit()

    def _update_database(self) -> None:

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

    # =================== HELPER METHODS =================== #

    def _connect(self) -> None:
        self.con = sqlite3.connect(f"{DATABASE_NAME}")
        self.cursor = self.con.cursor()

    def _close(self) -> None:
        self.cursor.close()

    def _convert_to_pokemon(self, database_record: tuple) -> Pokemon:
        """Helper method to convert a database record to
        a Pokémon object. The recieved values are not 
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

        dex_num, name, gen, type1, type2 = database_record[:5]
        hp, atk, defs, sp_atk, sp_def, speed = database_record[5:11]
        ability1, ability2, hidden = database_record[11:14]
        height, weight = database_record[14:16]
        egg_group1, egg_group2 = database_record[16:18]
        male, female = database_record[18:20]
        catch_rate = database_record[20]

        stats = {'HP': hp, 'ATK': atk, 'DEF': defs,
                 'SP_ATK': sp_atk, 'SP_DEF': sp_def, 'SPD': speed}

        abilities = {'first': ability1, 'second': ability2, 'hidden': hidden}

        egg_groups = (egg_group1, egg_group2)

        genders = (male, female)

        return Pokemon(dex_num, name, gen, type1, type2,
                       stats, abilities, height, weight,
                       egg_groups=egg_groups, genders=genders, catch_rate=catch_rate)

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

        pokemon = []

        for unparsed_pokemon in result:
            parsed_pokemon = self._convert_to_pokemon(unparsed_pokemon)
            pokemon.append(parsed_pokemon)

        return pokemon

    def _validate_generation(self, gens: list[int]) -> bool:
        """Helper method to check if a
        list of numbers is a valid list
        for Pokémon generations. Valid means
        a list consisting of only integer values
        from 1 to 9. 

        Parameters
        ----------
        gens : list[int]
            The list of numbers to check. 

        Returns
        -------
        bool
            True if the list is valid, False otherwise. 
        """

        # check both the type and the value
        for gen in gens:
            if not isinstance(gen, int):
                return False

            if gen > 9 or gen < 1:
                return False

        return True

    def _validate_types(self, types: list[str]) -> bool:
        """Support method to validate a list
        for correct Pokémon types. The types has to
        be lowercase, otherwise, it will be invalid. 
        Method will check the type of the entries 
        in addition to their values. 

        Parameters
        ----------
        types : list[str]
            The list to check for correctness.

        Returns
        -------
        bool
            True if the list contains Pokémon generations, 
            False otherwise. 
        """

        for type in types:
            if not isinstance(type, str):
                return False

        return all(typ.lower() in valid_types for typ in types)

    # ====================== GET METHODS ====================== #

    def get_pokemon_by_gens(self, table: str, gens: list[int], types: list[str] | None = None) -> list[Pokemon]:
        """Method to fetch all the Pokémon
        in the requested table. Method can 
        filter based on the generations
        and types provided. Note that the
        types provided must have the first letter
        capitalized. 

        Parameters
        ----------
        table : str
            The database table to fetch the
            Pokémon data from.
        gens : list[int]
            The generations the Pokémon should be from. The order 
            of the generations does not matter.
        types : list[str] | None, optional
            Types wanted, by default None. If None, 
            all types are returned, otherwise filter based
            on all the types specified. The ordering of the types
            does not matter.

        Returns
        -------
        list[Pokemon]
            A list of Pokémon objects, resulting from the request
            or an empty list if the query did not find any Pokémon
            satisfying the request. 

        Raises
        ------
        ValueError
            If the generations provided are incorrect or the
            types specified is invalid. 

        Examples
        --------
            >>> PokemonDatabase.get_pokemon_by_gens(table='pokemon', gens=[1, 2, 5], types=['Ghost', 'Fire'])
            This will query the database, giving Pokémon from generation 1, 2 or 5 only, but
            only display the Pokémon that have the type 'Ghost' and 'Fire'. Which type is primary and 
            secondary does not matter, that is, ['Fire', 'Ghost'] gives the same result. 
        """

        self._connect()

        # guard against invalid generations
        if not self._validate_generation(gens):
            raise ValueError(
                "Invalid Pokémon generation. Only 1-8 are allowed.")

        # guard against invalid types
        if types and not self._validate_types(types):
            raise ValueError("Invalid Pokémon type encountered.")

        # needed in case the list is not in increasing order
        # the query constructions assumes the generations are sorted
        gens.sort()

        # construct a query that has every generation requested, no filter on typing
        query = f'SELECT * FROM {table} WHERE ' + ''.join(
            f'gen = {gen} OR ' if gen != max(gens) else f'gen = {gen}' for gen in gens)

        if types:
            # add filtering on types
            type_filter = ' INTERSECT '.join(
                f'SELECT * FROM {table} WHERE type1="{p_type}" OR type2="{p_type}"' for p_type in types)
            query += f' INTERSECT {type_filter}'

        result = self.cursor.execute(query).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

    def get_pokemon_by_name(self, name: str) -> list[Pokemon]:
        """Method to get all the available data
        for the provided Pokémon. 

        Parameters
        ----------
        name : str
            Name of the Pokémon to fetch the
            data for. Name is not case sensitive. 

        Returns
        -------
        list[Pokemon]
            A list of the corresponding Pokémon objects.
            If the Pokémon does not exist, an empty 
            list is returned. 
        """

        self._connect()

        # name must be capitalized, as all Pokémon are stored as such
        # have to use title, as some Pokémon have two words as names (e.g. Tapu Koko)
        name = name.title()

        query = f'SELECT * FROM pokemon WHERE name = "{name}"'
        result = self.cursor.execute(query).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

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
            Minumum stat value to include. Input must
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
            If the min or max types are invalid. 
        """

        self._connect()

        valid_stats = ["hp", "atk", "def", "sp_atk", "sp_def", "spd"]

        if stat.lower() not in valid_stats:
            raise ValueError(f"Invalid Pokémon stat encountered: {stat}")

        if not (isinstance(min, (str, int))):
            raise TypeError("min must be either integer type or string.")

        if not (isinstance(max, (str, int))):
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
            Minumum stat total for the Pokémon to include.
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

        if not (isinstance(min, (str, int))):
            raise TypeError("min must be either integer type or string.")

        if not (isinstance(max, (str, int))):
            raise TypeError("max must be either integer type or string.")

        if isinstance(min, str) and not min.isdecimal():
            raise ValueError(f"Invalid min value encountered: {min}")

        if isinstance(max, str) and not max.isdecimal():
            raise ValueError(f"Invalid max value encountered: {max}")

        query = f'''SELECT *, HP + ATK + DEF + SP_ATK + SP_DEF + SPD AS total 
                    FROM {table} 
                    WHERE total BETWEEN {min} AND {max} ORDER BY total'''
        result = self.cursor.execute(query).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

    def get_pokemon_by_ability(self, table: str, ability: str) -> list[Pokemon]:
        """Method to fetch Pokémon that has the provided
        ability. The Pokémon is fetched if it is possible
        for it to have the ability, even if it
        is a hidden ability. 

        Parameters
        ----------
        table : str
            Which database table to fetch from.
        ability : str
            Which ability to filter the Pokémon on. 

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
            raise TypeError(
                "Invalid ability type encountered. Ability must be provided as str object.")

        query = f'''SELECT * 
                    FROM {table} 
                    WHERE ability1 = ? OR ability2 = ? OR hidden = ?'''
        result = self.cursor.execute(
            query, (ability, ability, ability)).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

    def get_pokemon_by_type(self, table: str, expression: str) -> list[Pokemon]:
        """Method to fetch Pokémon based on the types
        specified in the expression. The expression must follow
        the following Backus–Naur form:
            query ::= ANDterm | ANDterm "NOT" query
            ANDterm ::= ORterm | ORterm "AND" ANDterm
            ORterm ::= type | type "OR" ORterm
            type ::= "(" query ")" |fire|water|grass (and so on..)            

        Parameters
        ----------
        table : str
            Which table to fetch the Pokémon from.
        expression : str
            A Pokémon type expression. 

        Returns
        -------
        list[Pokemon]
            A list of Pokémon objects satisfying the expression. 

        Examples
        --------
        >>> fire and dark
            will fetch all Pokémon that are fire and dark type.
            All commands are independent of which type is 
            primary and secondary typing.
        >>> water or ice
            will fetch all Pokémon that are water or ice type.
        >>> bug not flying
            will fetch Pokémon that are bug, but not flying type. 
        >>> dragon or (ice and (water or grass))
            will get Pokémon that are dragon type or dual type ice and water or water and grass. 
        """

        self._connect()

        sql_query = self._type_query_parser(table, expression)

        result = self.cursor.execute(sql_query).fetchall()

        self._close()

        return self._convert_to_pokemon_list(result)

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
        valid_word_pattern = rf"^({pattern_operators}|{pattern_types}|{pattern_gens}|\s*|\(|\))( ({pattern_operators}|{pattern_types}|{pattern_gens}|\s*|\(|\)))*$"

        return bool(re.fullmatch(valid_word_pattern, expression))

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
            A SQL query obtained from the parsed query or
            an empty string if a syntax error was encountered. 
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

        # if the query is just a string, it corresponds to a type, so return a simple query
        if isinstance(query, str):
            return construct_simple_query(query)

        # if the query is a tuple, the first entry is the operation and the next are the arguments
        operation, arg1, arg2 = query

        if operation == "AND":
            if self._validate_types([arg1, arg2]):
                # if both arguments are valid types, intersect the two simple queries
                return construct_intersect_query(construct_simple_query(arg1), construct_simple_query(arg2))
            elif self._validate_types([arg1]):
                # in this case, arg2 needs more parsing before intersecting
                return construct_intersect_query(construct_simple_query(arg1), self._construct_sql_query(table, arg2))
            elif self._validate_types([arg2]):
                # likewise, arg1 needs more parsing
                return construct_intersect_query(self._construct_sql_query(table, arg1), construct_simple_query(arg2))
            else:
                # both arguments needs further parsing
                return construct_intersect_query(self._construct_sql_query(table, arg1), self._construct_sql_query(table, arg2))

        elif operation == "OR":
            if self._validate_types([arg1, arg2]):
                # if both arguments are valid types, union the two simple queries
                return construct_union_query(construct_simple_query(arg1), construct_simple_query(arg2))
            elif self._validate_types([arg1]):
                # here arg2 needs to be parsed more
                return construct_union_query(construct_simple_query(arg1), self._construct_sql_query(table, arg2))
            elif self._validate_types([arg2]):
                # arg1 needs to be handled
                return construct_union_query(self._construct_sql_query(table, arg1), construct_simple_query(arg2))
            else:
                # both arguments need to be parsed before taking the union
                return construct_union_query(self._construct_sql_query(table, arg1), self._construct_sql_query(table, arg2))

        elif operation == "NOT":
            if self._validate_types([arg1, arg2]):
                # both arguments being types, except the simple queries
                return construct_except_query(construct_simple_query(arg1), construct_simple_query(arg2))
            elif self._validate_types([arg1]):
                # parse arg2 before doing the except
                return construct_except_query(construct_simple_query(arg1), self._construct_sql_query(table, arg2))
            elif self._validate_types([arg2]):
                # likewise, but arg1 needs more parsing
                return construct_except_query(self._construct_sql_query(table, arg1), construct_simple_query(arg2))
            else:
                # both arguments needs to be handled before we can except
                return construct_except_query(self._construct_sql_query(table, arg1), self._construct_sql_query(table, arg2))

        else:
            print(f"Invalid operation: {operation}")
            return ""

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
            The query/request from the user. 

        Returns
        -------
        str
            A SQL query, that will grant the request 
            from the expression, or an empty string
            if an error occurred.           
        """

        # lowercase the expression, add spaces and make sure the operators are capitalized
        expression = expression.lower()
        expression = expression.replace('and', ' AND ').replace(
            ' or ', ' OR ').replace(' not ', ' NOT ')
        expression = expression.replace('(', '( ').replace(')', ' )')

        # guard against expressions that contain any invalid words, syntax is not checked, only characters
        if not self._verify_input(expression):
            print(f"Invalid words encountered in the expression: {expression}")
            return ''
        
        # split the expression based on the spaces, to get a list of tokens
        tokens = expression.split()

        # create a paser for the tokens
        parser = PokemonParser(tokens)

        # parse the query to obtain a type or a tuple
        try:
            parsed_query = parser.parse()
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
            return ""

        return self._construct_sql_query(table, parsed_query)


if __name__ == "__main__":
    db = PokemonDatabase()

    db._update_database()
