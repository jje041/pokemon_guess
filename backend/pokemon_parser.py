"""Implementation of the parser for the Pokémon Backus–Naur 
syntax used by the pokemon database api."""

__version__ = "2.0.0"
__author__ = "Jørn Olav Jensen"

valid_types = ["grass", "fire", "water", "ice", "ghost", "dark", "fairy", "fighting", "psychic",
               "electric", "dragon", "normal", "poison", "bug", "flying", "rock", "ground", "steel"
               ]


class PokemonParser:
    """
    PokemonParser Class

    A simple parser for querying Pokémon types using AND, OR, and NOT operations.

    Parameters
    ----------
    tokens : list[str]
        List of tokens to parse.

    Attributes
    ----------
    tokens : list[str]
        List of tokens to parse.
    current_token : str or None
        The current token being processed.

    Methods
    -------
    next_token()
        Advances to the next token in the list.
    parse() -> str | tuple
        Parses the input tokens and returns the result.
    query() -> str | tuple
        Parses a query expression.
    and_term() -> str | tuple
        Parses an AND term.
    or_term() -> str | tuple
        Parses an OR term.
    type() -> str | tuple
        Parses a Pokemon type.

    Raises
    ------
    SyntaxError
        If there is a syntax error in the input query.
    """

    def __init__(self, tokens: list[str]) -> None:

        # List of tokens to parse.
        self.tokens = tokens
        self.current_token = None

        # Get the next token.
        self.next_token()

    def next_token(self) -> None:
        """Advances to the next token in the list.
        """

        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse(self) -> str | tuple[str, ...]:
        """Parses the input tokens and returns the result.

        Returns
        -------
        str | tuple
            The parsed query result.
        """

        return self.query()

    def query(self) -> str | tuple:
        """Parses a query expression.

        Returns
        -------
        str | tuple
            The parsed query expression.
        """

        result = self.and_term()

        if self.current_token == "NOT":
            self.next_token()
            result = ("NOT", result, self.query())

        return result

    def and_term(self) -> str | tuple:
        """Parses an AND term.

        Returns
        -------
        str | tuple
            The parsed AND term.
        """

        result = self.or_term()

        if self.current_token == "AND":
            self.next_token()
            result = ("AND", result, self.and_term())

        return result

    def or_term(self) -> str | tuple:
        """Parses an OR term.

        Returns
        -------
        str | tuple
            The parsed OR term.
        """

        result = self.ptype()

        if self.current_token == "OR":
            self.next_token()
            result = ("OR", result, self.or_term())

        return result

    def ptype(self) -> str | tuple:
        """Parses a Pokemon type.

        Returns
        -------
        str
            The parsed Pokemon type.

        Raises
        ------
        SyntaxError
            If there is a syntax error in the input query.
        """

        if self.current_token == "(":
            self.next_token()
            result = self.query()
            if self.current_token != ")":
                raise SyntaxError("Expected ')'")

            self.next_token()
            return result

        if self.current_token in valid_types:
            result = self.current_token
            self.next_token()
            return result
        
        print(self.tokens)

        raise SyntaxError(f"Unexpected token: {self.current_token}")


def tokenize(input: str) -> list[str]:
    """Tokenizes the input string.
    The tokens must be separated by 
    white-spaces.

    Parameters
    ----------
    input_str : str
        The input string to tokenize.

    Returns
    -------
    List[str]
        The list of tokens.
    """

    # Assuming the input string is space-separated.
    return input.split()


if __name__ == "__main__":
    input_string = input("Enter your query (AND, OR, NOT supported): ")

    # Create the tokens for the input query.
    tokens: list[str] = tokenize(input_string)

    parser = PokemonParser(tokens)

    parsed_query = parser.parse()
    print(f"Parsed query: {parsed_query}")
