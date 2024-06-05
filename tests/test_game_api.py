import unittest

from game_api.pokemon_game_api import GameApi


class TestGameApi(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.game = GameApi()
        super().__init__(methodName)

    # ========================= FIND GENERATIONS =========================

    def test_simple_find_generations(self) -> None:
        result = self.game.find_generations(["filename", "1", "3", "6", "9"])

        correct_list = [1, 3, 6, 9]

        self.assertListEqual(result, correct_list)

    def test_unordered_find_generations(self) -> None:
        result = self.game.find_generations(["filename", "6", "7", "3", "1"])

        correct_list = [1, 3, 6, 7]

        self.assertListEqual(result, correct_list)

    def test_repeated_find_generations(self) -> None:
        result = self.game.find_generations(["filename", "3", "5", "3", "5"])

        correct_list = [3, 5]

        self.assertListEqual(result, correct_list)

    def test_invalid_gen_find_generations(self) -> None:
        with self.assertRaises(ValueError) as error:
            self.game.find_generations(["filename", "3", "5", "10"])
        self.assertEqual(str(error.exception), "Invalid generations requested, can only be numbers from 1-9.")

    def test_invalid_input_find_generations(self) -> None:
        with self.assertRaises(ValueError) as error:
            self.game.find_generations(["filename", "not", "a", "valid", "number", "4"])
        self.assertEqual(str(error.exception), "Invalid generations requested, can only be numbers from 1-9.")

    def test_file_name_only_find_generations(self) -> None:
        result = self.game.find_generations(["filename"])

        correct_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.assertListEqual(result, correct_list)

    # ======================== FIND NUMBER OF POKEMON ========================

    def test_find_number_of_pokemon(self) -> None:
        result = self.game.find_number_of_pokemon([1, 2])

        correct_result = 251

        self.assertEqual(result, correct_result)

    def test_all_find_number_of_pokemon(self) -> None:
        result = self.game.find_number_of_pokemon([1, 2, 3, 4, 5, 6, 7, 8, 9])

        correct_result = 1025

        self.assertEqual(result, correct_result)

    def test_only_one_number_of_pokemon(self) -> None:
        result = self.game.find_number_of_pokemon([5])

        correct_result = 156

        self.assertEqual(result, correct_result)


if __name__ == "__main__":

    unittest.main()
