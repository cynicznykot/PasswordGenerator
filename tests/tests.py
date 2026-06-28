import unittest
import string
from unittest.mock import patch
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from main import (
    get_number,
    get_character_options,
    build_character_pool,
    generate_password,
    generate_again,
    greed
)


class TestAuxiliaryFunctions(unittest.TestCase):
    """Tests for auxiliary functions"""

    @patch('builtins.print')
    def test_greed_output(self, mock_print):
        """Test greed"""
        greed()
        self.assertTrue(mock_print.called)

    def test_get_number_valid_input(self):
        """Test getting valid number"""
        with patch('builtins.input', return_value='10'):
            result = get_number("Enter length: ")
            self.assertEqual(result, 10)

    @patch('builtins.print')
    def test_get_number_too_short(self, mock_print):
        """Test too short password"""
        with patch('builtins.input', side_effect=['3', '10']):
            result = get_number("Enter length: ")
            self.assertEqual(result, 10)

    @patch('builtins.print')
    def test_get_number_too_long(self, mock_print):
        """Test to long password"""
        with patch('builtins.input', side_effect=['40', '10']):
            result = get_number("Enter length: ")
            self.assertEqual(result, 10)

    @patch('builtins.print')
    def test_get_number_invalid_input(self, mock_print):
        """Test invalid input"""
        with patch('builtins.input', side_effect=['abc', '10']):
            result = get_number("Enter length: ")
            self.assertEqual(result, 10)

    def test_get_number_boundary_values(self):
        """Test boundary values"""
        with patch('builtins.input', return_value='5'):
            result = get_number("Enter length: ")
            self.assertEqual(result, 5)

        with patch('builtins.input', return_value='35'):
            result = get_number("Enter length: ")
            self.assertEqual(result, 35)


class TestAppLogic(unittest.TestCase):
    """Tests for main application logic"""

    def test_get_character_options_all_yes(self):
        """Test selecting all character types"""
        with patch('builtins.input', side_effect=['y', 'y', 'y']):
            letters, digits, symbols = get_character_options()
            self.assertTrue(letters)
            self.assertTrue(digits)
            self.assertTrue(symbols)

    def test_get_character_options_all_no(self):
        """Test rejecting all character types"""
        with patch('builtins.input', side_effect=['n', 'n', 'n']):
            letters, digits, symbols = get_character_options()
            self.assertFalse(letters)
            self.assertFalse(digits)
            self.assertFalse(symbols)

    def test_get_character_options_mixed(self):
        """Test mixed selection"""
        with patch('builtins.input', side_effect=['y', 'n', 'y']):
            letters, digits, symbols = get_character_options()
            self.assertTrue(letters)
            self.assertFalse(digits)
            self.assertTrue(symbols)

    def test_build_character_pool_all(self):
        """Test building pool with all characters"""
        pool = build_character_pool(True, True, True)
        expected = string.ascii_letters + string.digits + string.punctuation
        self.assertEqual(pool, expected)

    def test_build_character_pool_only_letters(self):
        """Test building pool with only letters"""
        pool = build_character_pool(True, False, False)
        self.assertEqual(pool, string.ascii_letters)

    def test_build_character_pool_only_digits(self):
        """Test building pool with only digits"""
        pool = build_character_pool(False, True, False)
        self.assertEqual(pool, string.digits)

    def test_build_character_pool_only_symbols(self):
        """Test building pool with only symbols"""
        pool = build_character_pool(False, False, True)
        self.assertEqual(pool, string.punctuation)

    def test_build_character_pool_empty(self):
        """Test building pool with no characters"""
        pool = build_character_pool(False, False, False)
        self.assertEqual(pool, "")

    def test_generate_password_valid(self):
        """Test generating valid password"""
        pool = string.ascii_letters + string.digits
        password = generate_password(10, pool)
        self.assertEqual(len(password), 10)
        for char in password:
            self.assertIn(char, pool)

    def test_generate_password_empty_pool(self):
        """Test generating password with empty pool"""
        result = generate_password(10, "")
        self.assertIsNone(result)

    def test_generate_password_length(self):
        """Test generating password with length"""
        pool = string.ascii_letters
        for length in [5, 10, 15, 20, 25, 30, 35]:
            password = generate_password(length, pool)
            self.assertEqual(len(password), length)

    def test_generate_password_randomness(self):
        """Test uniqueness of generated passwords"""
        pool = string.ascii_letters + string.digits
        passwords = set()
        for _ in range(100):
            password = generate_password(10, pool)
            passwords.add(password)
        self.assertEqual(len(passwords), 100)

    @patch('builtins.print')
    def test_generate_again_positive(self, mock_print):
        """Test generating positive passwords"""
        positive_responses = ['y', 'yes', 'yeah', 'da', 'd', 'a']
        for response in positive_responses:
            with patch('builtins.input', return_value=response):
                result = generate_again()
                self.assertTrue(result)

    @patch('builtins.print')
    def test_generate_again_negative(self, mock_print):
        """Test generating negative passwords"""
        negative_responses = ['n', 'no', 'not', 'net', 'nope']
        for response in negative_responses:
            with patch('builtins.input', return_value=response):
                result = generate_again()
                self.assertFalse(result)

    @patch('builtins.print')
    def test_generate_again_invalid_then_valid(self, mock_print):
        """Test generating invalid passwords"""
        with patch('builtins.input', side_effect=['invalid', 'y']):
            result = generate_again()
            self.assertTrue(result)
            mock_print.assert_any_call("⚠️ Please answer 'y' or 'n'!")


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    @patch('builtins.print')
    def test_full_generation_flow(self, mock_print):
        """Test full generation flow"""
        with patch('builtins.input', side_effect=['10', 'y', 'y', 'n']):
            length = get_number("Enter length: ")
            letters, digits, symbols = get_character_options()
            pool = build_character_pool(letters, digits, symbols)
            password = generate_password(length, pool)
            self.assertEqual(len(password), 10)
            self.assertIsNotNone(password)

    def test_character_pool_contains_correct_chars(self):
        """Test character pool contains correct characters"""
        pool = build_character_pool(True, False, False)
        self.assertTrue(all(c in string.ascii_letters for c in pool))

        pool = build_character_pool(False, True, False)
        self.assertTrue(all(c in string.digits for c in pool))

        pool = build_character_pool(False, False, True)
        self.assertTrue(all(c in string.punctuation for c in pool))

    def test_password_strength_indicators(self):
        """Test password strength indicators"""
        # Пароль только из букв
        pool = string.ascii_letters
        password = generate_password(8, pool)
        self.assertTrue(all(c.isalpha() for c in password))

        # Пароль только из цифр
        pool = string.digits
        password = generate_password(8, pool)
        self.assertTrue(all(c.isdigit() for c in password))

        # Пароль из букв и цифр
        pool = string.ascii_letters + string.digits
        password = generate_password(8, pool)
        self.assertTrue(any(c.isalpha() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))


class TestEdgeCases(unittest.TestCase):
    """Edge cases tests"""

    def test_minimum_length_with_all_types(self):
        """Test minimum length with all types"""
        pool = string.ascii_letters + string.digits + string.punctuation
        password = generate_password(5, pool)
        self.assertEqual(len(password), 5)

    def test_maximum_length(self):
        """Test maximum length with all types"""
        pool = string.ascii_letters
        password = generate_password(35, pool)
        self.assertEqual(len(password), 35)

    def test_single_character_type(self):
        """Test single character type"""
        pool = build_character_pool(True, False, False)
        password = generate_password(10, pool)
        self.assertTrue(all(c in string.ascii_letters for c in password))

        pool = build_character_pool(False, True, False)
        password = generate_password(10, pool)
        self.assertTrue(all(c in string.digits for c in password))

    def test_unicode_characters_not_included(self):
        """Test that Unicode characters are not included"""
        pool = build_character_pool(True, True, True)
        for char in pool:
            self.assertTrue(ord(char) < 128)


if __name__ == '__main__':
    unittest.main(verbosity=2)