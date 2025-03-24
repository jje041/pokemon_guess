import unittest

from game_api.backend.exceptions_database import (PokemonGenericError,
                                                  PokemonInvalidGenerations,
                                                  PokemonInvalidTypes,
                                                  PokemonSyntaxError,
                                                  PokemonTableDoesNotExist)
from game_api.backend.pokemon import Pokemon
from game_api.backend.pokemon_database_api import PokemonDatabase


class TestPokemonDatabase(unittest.TestCase):

    def __init__(self, methodName: str) -> None:
        self.db = PokemonDatabase()
        super().__init__(methodName)

    # ========================== GET_POKEMON_BY_GENS ==========================

    def test_get_pokemon_by_gens_generation123(self) -> None:
        all_pokemon = self.db.get_pokemon_by_gens('pokemon', [1, 2, 3], types=None)

        self.assertEqual(386, len(all_pokemon))

    def test_get_pokemon_by_gens_generation18(self) -> None:
        all_pokemon = self.db.get_pokemon_by_gens('pokemon', [1, 8], types=None)

        self.assertEqual(247, len(all_pokemon))

    def test_get_pokemon_by_gens_filter_by_gen_and_type(self) -> None:
        all_pokemon = self.db.get_pokemon_by_gens('pokemon', [1], types=['Ghost'])

        self.assertEqual(3, len(all_pokemon))

    def test_get_pokemon_by_gens_filter_by_gen_and_type_not_capital_type(self) -> None:
        all_pokemon = self.db.get_pokemon_by_gens('pokemon', [1], types=['ghost'])

        self.assertEqual(3, len(all_pokemon))

    def test_get_pokemon_by_gens_filter_by_gens_and_types(self) -> None:
        all_pokemon = self.db.get_pokemon_by_gens('pokemon', [1, 5], types=['Ghost', 'Fire'])

        self.assertEqual(3, len(all_pokemon))

    def test_get_pokemon_by_gens_not_sorted_gens(self) -> None:
        all_pokemon = self.db.get_pokemon_by_gens('pokemon', [5, 1], types=['Ghost', 'Fire'])

        self.assertEqual(3, len(all_pokemon))

    def test_get_pokemon_by_gens_wrong_input_gens(self) -> None:
        with self.assertRaises(PokemonInvalidGenerations):
            self.db.get_pokemon_by_gens('pokemon', ['wrong', 'input'])  # type: ignore

    def test_get_pokemon_by_gens_partial_wrong_input(self) -> None:
        with self.assertRaises(PokemonInvalidGenerations):
            self.db.get_pokemon_by_gens('pokemon', [1, 'error'])  # type: ignore

    def test_get_pokemon_by_gens_wrong_types(self) -> None:

        with self.assertRaises(PokemonInvalidTypes):
            self.db.get_pokemon_by_gens('pokemon', [5, 6], ['not', 'a', 'type'])

    # ============================ GET POKEMON BY NAME ============================

    def test_get_pokemon_by_name(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', 'mew')

        mew = Pokemon(
            151, 'Mew', 1, 'Psychic', None,
            {
                'HP': 100,
                'ATK': 100,
                'DEF': 100,
                'SP_ATK': 100,
                'SP_DEF': 100,
                'SPD': 100
            },
            {
                'first': 'Synchronize',
                'second': None,
                'hidden': None
            },
            0.4, 4.0,
            ('Undiscovered', None),
            (None, None),
            45
        )

        self.assertEqual(mew, pokemon)

    def test_get_pokemon_by_name_with_type(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', 'jellicent')

        jellicent = Pokemon(
            593, 'Jellicent', 5, 'Water', 'Ghost',
            {
                'HP': 100,
                'ATK': 60,
                'DEF': 70,
                'SP_ATK': 85,
                'SP_DEF': 105,
                'SPD': 60
            },
            {
                'first': 'Water Absorb',
                'second': 'Cursed Body',
                'hidden': 'Damp'
            },
            2.2, 135,
            ('Amorphous', None),
            (50, 50),
            60
        )

        self.assertEqual(jellicent, pokemon)

    def test_special_pokemon_name1(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', 'farfetchd')

        farfetchd = Pokemon(
            83, "Farfetch'd", 1, 'Normal', 'Flying',
            {
                'HP': 52,
                'ATK': 90,
                'DEF': 55,
                'SP_ATK': 58,
                'SP_DEF': 62,
                'SPD': 60
            },
            {
                'first': 'Keen Eye',
                'second': 'Inner Focus',
                'hidden': 'Defiant'
            },
            0.8, 15,
            ('Field', 'Flying'),
            (50, 50),
            45
        )

        self.assertEqual(farfetchd, pokemon)

    def test_special_pokemon_name2(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', "farfetch'd")

        farfetchd = Pokemon(
            83, "Farfetch'd", 1, 'Normal', 'Flying',
            {
                'HP': 52,
                'ATK': 90,
                'DEF': 55,
                'SP_ATK': 58,
                'SP_DEF': 62,
                'SPD': 60
            },
            {
                'first': 'Keen Eye',
                'second': 'Inner Focus',
                'hidden': 'Defiant'
            },
            0.8, 15,
            ('Field', 'Flying'),
            (50, 50),
            45
        )

        self.assertEqual(farfetchd, pokemon)

    def test_special_pokemon_name3(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', "Farfetch'd")

        farfetchd = Pokemon(
            83, "Farfetch'd", 1, 'Normal', 'Flying',
            {
                'HP': 52,
                'ATK': 90,
                'DEF': 55,
                'SP_ATK': 58,
                'SP_DEF': 62,
                'SPD': 60
            },
            {
                'first': 'Keen Eye',
                'second': 'Inner Focus',
                'hidden': 'Defiant'
            },
            0.8, 15,
            ('Field', 'Flying'),
            (50, 50),
            45
        )

        self.assertEqual(farfetchd, pokemon)

    def test_special_pokemon_name4(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', "Farfetchd")

        farfetchd = Pokemon(
            83, "Farfetch'd", 1, 'Normal', 'Flying',
            {
                'HP': 52,
                'ATK': 90,
                'DEF': 55,
                'SP_ATK': 58,
                'SP_DEF': 62,
                'SPD': 60
            },
            {
                'first': 'Keen Eye',
                'second': 'Inner Focus',
                'hidden': 'Defiant'
            },
            0.8, 15,
            ('Field', 'Flying'),
            (50, 50),
            45
        )

        self.assertEqual(farfetchd, pokemon)

    def test_special_pokemon_name5(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', 'Kommo-o')

        kommo_o = Pokemon(
            784, "Kommo-o", 7, 'Dragon', 'Fighting',
            {
                'HP': 75,
                'ATK': 110,
                'DEF': 125,
                'SP_ATK': 100,
                'SP_DEF': 105,
                'SPD': 85
            },
            {
                'first': 'Bulletproof',
                'second': 'Soundproof',
                'hidden': 'Overcoat'
            },
            1.6, 78.2,
            ('Dragon', None),
            (50, 50),
            45
        )

        self.assertEqual(kommo_o, pokemon)

    def test_get_pokemon_by_name_capitalized(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', 'Glimmora')

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

        self.assertEqual(glimmora, pokemon)

    def test_get_pokemon_by_name_wrong_name(self) -> None:
        pokemon = self.db.get_pokemon_by_name('pokemon', 'error')

        self.assertEqual(None, pokemon)

    def test_get_pokemon_invalid_table(self) -> None:

        with self.assertRaises(PokemonTableDoesNotExist):
            self.db.get_pokemon_by_name('notfound', 'mew')

    # ============================= GET POKEMON BY STAT =============================

    def test_get_pokemon_by_stat_hp(self) -> None:
        pokemon, _ = self.db.get_pokemon_by_stat('pokemon', 'hp', 0, '10')

        self.assertEqual(3, len(pokemon))

    def test_get_pokemon_by_stat_atk(self) -> None:
        pokemon, _ = self.db.get_pokemon_by_stat('pokemon', 'atk', '150', 200)
        
        self.assertEqual(9, len(pokemon))

    def test_get_pokemon_by_stat_def(self) -> None:
        pokemon, _ = self.db.get_pokemon_by_stat('pokemon', 'def', '200', '250')

        self.assertEqual(4, len(pokemon))

    def test_get_pokemon_by_stat_sp_atk(self) -> None:
        pokemon, _ = self.db.get_pokemon_by_stat('pokemon', 'sp_atk', 160, 180)

        self.assertEqual(1, len(pokemon))

    def test_get_pokemon_by_stat_sp_def(self) -> None:
        pokemon, _ = self.db.get_pokemon_by_stat('pokemon', 'sp_def', '0', '20')

        self.assertEqual(6, len(pokemon))

    def test_get_pokemon_by_stat_speed(self) -> None:
        pokemon, _ = self.db.get_pokemon_by_stat('pokemon', 'spd', 150, 200)

        self.assertEqual(5, len(pokemon))

    def test_get_pokemon_by_stat_invalid_stat(self) -> None:
        with self.assertRaises(ValueError):
            self.db.get_pokemon_by_stat('pokemon', 'not a stat', 10, 20)

    def test_get_pokemon_by_stat_invalid_min_max(self) -> None:
        with self.assertRaises(ValueError):
            self.db.get_pokemon_by_stat('pokemon', 'hp', 'invalid', 'stats')

    def test_get_pokemon_by_stat_total(self) -> None:
        pokemon, _ = self.db.get_pokemon_by_stat_total('pokemon', 670, 720)

        self.assertEqual(23, len(pokemon))

    def test_get_pokemon_by_stat_total_invalid(self) -> None:
        with self.assertRaises(ValueError):
            self.db.get_pokemon_by_stat_total('pokemon', 'not', 'valid')  # type: ignore

    def test_get_pokemon_by_stat_total_partial_invalid(self) -> None:
        with self.assertRaises(ValueError):
            self.db.get_pokemon_by_stat_total('pokemon', 520, 'mistake')  # type: ignore

    # =========================== GET POKEMON BY ABILITY ===========================

    def test_get_pokemon_by_ability_single_word(self) -> None:
        pokemon = self.db.get_pokemon_by_ability('pokemon', 'Static')

        self.assertEqual(20, len(pokemon))

    def test_get_pokemon_by_ability_double_word(self) -> None:
        pokemon = self.db.get_pokemon_by_ability('pokemon', 'Water Absorb')

        self.assertEqual(26, len(pokemon))

    def test_get_pokemon_by_ability_invalid(self) -> None:
        # No Pokémon will be found.
        pokemon = self.db.get_pokemon_by_ability('pokemon', 'incorrect')

        self.assertListEqual([], pokemon)

    def test_get_pokemon_by_ability_invalid_type(self) -> None:

        with self.assertRaises(TypeError):
            # The ability should be a string, AbilityError exception shall be thrown.
            self.db.get_pokemon_by_ability('pokemon', {1, 'p'})  # type: ignore

    # ========================= GET POKEMON BY TYPE =========================

    def test_get_pokemon_one_type(self) -> None:

        pokemon = self.db.get_pokemon_by_type('pokemon', 'ghost', [])

        self.assertEqual(65, len(pokemon))

    def test_get_pokemon_one_type_parentheses(self) -> None:

        pokemon = self.db.get_pokemon_by_type('pokemon', '(ice) ', [])

        self.assertEqual(48, len(pokemon))

    def test_get_pokemon_simple_and(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', 'ghost and ice', [])

        self.assertEqual(1, len(pokemon))

    def test_get_pokemon_simple_and_with_parentheses(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(ghost and fire)', [])

        self.assertEqual(6, len(pokemon))

    def test_get_pokemon_simple_or(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', 'ghost or ice', [])

        self.assertEqual(112, len(pokemon))

    def test_get_pokemon_simple_or_with_parentheses(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(ghost or ice)', [])

        self.assertEqual(112, len(pokemon))

    def test_get_pokemon_and_parentheses_then_or(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(dark and water) or ice', [])

        self.assertEqual(52, len(pokemon))

    def test_get_pokemon_and_single_then_parentheses(self) -> None:

        pokemon = self.db.get_pokemon_by_type('pokemon', 'ice or (dark and water)', [])

        self.assertEqual(52, len(pokemon))

    def test_get_pokemon_two_and_parentheses_with_or(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(dark and water) or (dark and fire)', [])

        self.assertEqual(8, len(pokemon))

    def test_get_pokemon_three_and_parentheses_with_two_or(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(dark and water) or (dark and fire) or (dark and grass)', [])

        self.assertEqual(15, len(pokemon))

    def test_get_pokemon_or_then_and(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(ghost or dark) and ice', [])

        self.assertEqual(4, len(pokemon))

    def test_get_pokemon_single_then_parentheses(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', 'ice and (ghost or dark)', [])

        self.assertEqual(4, len(pokemon))

    def test_get_pokemon_double_parentheses_then_single(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(ghost and dark) or (fire and dark) or bug', [])

        self.assertEqual(98, len(pokemon))

    def test_get_pokemon_three_or(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', 'dark or Fairy or dragon', [])

        self.assertEqual(195, len(pokemon))

    def test_get_pokemon_three_and(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', 'bug and flying and dragon', [])

        self.assertEqual(0, len(pokemon))

    def test_get_pokemon_and_then_or_in_par(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', 'dragon and (dark or Ice)', [])

        self.assertEqual(9, len(pokemon))

    def test_get_pokemon_nested_par(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', 'Dragon and (dark or (fairy and normal))', [])

        self.assertEqual(5, len(pokemon))

    def test_get_pokemon_double_par_and_or(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(bug and electric) or (fire and ghost)', [])

        self.assertEqual(10, len(pokemon))

    def test_get_pokemon_double_par_triple_and(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(fire and ghost) and (fire and ghost)', [])

        self.assertEqual(6, len(pokemon))

    def test_get_pokemon_double_par_two_and_one_or(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(ghost and fire) OR (grass and dark)', [])

        self.assertEqual(13, len(pokemon))

    # ================================ NOT OPERATOR ================================

    def test_get_pokemon_by_types_simple_not(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', 'bug not flying', [])

        self.assertEqual(79, len(pokemon))

    def test_get_pokemon_by_types_not_and(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(bug and electric) not flying', [])

        self.assertEqual(4, len(pokemon))

    def test_get_pokemon_by_types_not_or(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(bug or fire) not ice', [])

        self.assertEqual(167, len(pokemon))

    def test_get_pokemon_by_types_double_not(self) -> None:
        pokemon = self.db.get_pokemon_by_type('pokemon', '(bug not fire) not ice', [])

        self.assertEqual(86, len(pokemon))

    # ============================== PARSE ERROR DETECTION ============================== #

    def test_simple_invalid_type(self) -> None:
        valid_tokens = self.db._verify_input('wrong')

        self.assertEqual(False, valid_tokens)

    def test_simple_invalid_character(self) -> None:
        input_string = '*'
        valid_tokens = self.db._verify_input(input_string)

        self.assertEqual(False, valid_tokens)

    def test_simple_and_operator(self) -> None:
        input_string = 'test AND test2'
        valid_tokens = self.db._verify_input(input_string)

        self.assertEqual(False, valid_tokens)


if __name__ == "__main__":

    unittest.main()
