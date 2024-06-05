

class PokemonTableDoesNotExist(Exception):
    
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class PokemonSyntaxError(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class PokemonInvalidGenerations(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class PokemonInvalidTypes(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class PokemonGenericError(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
