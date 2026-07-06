"""
Unit tests for the password generator module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import string
from src.generator import (
    build_character_pool,
    generate_password,
    check_strength
)


class TestBuildCharacterPool(unittest.TestCase):
    """Test suite for build_character_pool function."""

    def test_letters_only(self):
        """Should return a pool containing only alphabetic characters."""
        pool = build_character_pool(True, False, False)
        self.assertTrue(all(c.isalpha() for c in pool))
        self.assertFalse(any(c.isdigit() for c in pool))
        self.assertFalse(any(c in string.punctuation for c in pool))

    def test_digits_only(self):
        """Should return a pool containing only digits (0-9)."""
        pool = build_character_pool(False, True, False)
        self.assertTrue(all(c.isdigit() for c in pool))

    def test_symbols_only(self):
        """Should return a pool containing only punctuation symbols."""
        pool = build_character_pool(False, False, True)
        self.assertTrue(all(c in string.punctuation for c in pool))

    def test_letters_and_digits(self):
        """Should return a pool containing both letters and digits, but no symbols."""
        pool = build_character_pool(True, True, False)
        self.assertTrue(any(c.isalpha() for c in pool))
        self.assertTrue(any(c.isdigit() for c in pool))
        self.assertFalse(any(c in string.punctuation for c in pool))

    def test_all_types(self):
        """Should return a pool containing letters, digits, and symbols."""
        pool = build_character_pool(True, True, True)
        self.assertTrue(any(c.isalpha() for c in pool))
        self.assertTrue(any(c.isdigit() for c in pool))
        self.assertTrue(any(c in string.punctuation for c in pool))

    def test_no_types(self):
        """Should return an empty string when no character types are selected."""
        pool = build_character_pool(False, False, False)
        self.assertEqual(pool, "")


class TestGeneratePassword(unittest.TestCase):
    """Test suite for generate_password function."""

    def test_length_16(self):
        """Should generate a password of exactly 16 characters."""
        pool = "abc123!@#"
        password = generate_password(16, pool)
        self.assertEqual(len(password), 16)

    def test_length_30(self):
        """Should generate a password of exactly 30 characters."""
        pool = "abc123!@#"
        password = generate_password(30, pool)
        self.assertEqual(len(password), 30)

    def test_length_64(self):
        """Should generate a password of exactly 64 characters."""
        pool = "abc123!@#"
        password = generate_password(64, pool)
        self.assertEqual(len(password), 64)

    def test_zero_length(self):
        """Should return an empty string when length is 0."""
        pool = "abc123!@#"
        password = generate_password(0, pool)
        self.assertEqual(password, "")

    def test_empty_pool(self):
        """Should return None when the character pool is empty."""
        password = generate_password(10, "")
        self.assertIsNone(password)

    def test_pool_with_letters_only(self):
        """Should generate a password containing only letters."""
        pool = string.ascii_letters
        password = generate_password(20, pool)
        self.assertTrue(all(c.isalpha() for c in password))

    def test_pool_with_digits_only(self):
        """Should generate a password containing only digits."""
        pool = string.digits
        password = generate_password(20, pool)
        self.assertTrue(all(c.isdigit() for c in password))

    def test_randomness(self):
        """Should generate different passwords on each call (randomness check)."""
        pool = "abc123!@#"
        password1 = generate_password(20, pool)
        password2 = generate_password(20, pool)
        self.assertNotEqual(password1, password2)


class TestCheckStrength(unittest.TestCase):
    """Test suite for check_strength function."""

    def test_weak_short(self):
        """Very short password should be classified as 'Not Safe'."""
        result = check_strength("abc")
        self.assertEqual(result, "Not Safe")

    def test_weak_only_lowercase_16(self):
        """16 characters of only lowercase letters should be 'Not Safe'."""
        result = check_strength("abcdefghijklmnop")
        self.assertEqual(result, "Not Safe")

    def test_weak_only_digits_16(self):
        """16 characters of only digits should be 'Not Safe'."""
        result = check_strength("1234567890123456")
        self.assertEqual(result, "Not Safe")

    def test_moderate_letters_and_digits_16(self):
        """16 characters with letters and digits should be 'Moderate'."""
        result = check_strength("Abcdefgh12345678")
        self.assertEqual(result, "Moderate")

    def test_moderate_letters_and_symbols_16(self):
        """16 characters with letters and symbols should be 'Moderate'."""
        result = check_strength("Abcdefgh!@#$%^&*")
        self.assertEqual(result, "Moderate")

    def test_strong_all_types_16(self):
        """16 characters with all types should be 'Very Strong'."""
        result = check_strength("Abc123!@#Def456$%^")
        self.assertEqual(result, "Very Strong")

    def test_strong_long_all_types_30(self):
        """30 characters with all types should be 'Very Strong'."""
        result = check_strength("Abc123!@#Def456$%^Ghi789&*()")
        self.assertEqual(result, "Very Strong")

    def test_empty(self):
        """Empty password should be classified as 'Not Safe'."""
        result = check_strength("")
        self.assertEqual(result, "Not Safe")

    def test_score_2(self):
        """Score 2 should be 'Not Safe'."""
        result = check_strength("abcdefghijklmnop")
        self.assertEqual(result, "Not Safe")

    def test_score_3(self):
        """Score 3 should be 'Moderate'."""
        result = check_strength("Abcdefghijklmnop")
        self.assertEqual(result, "Moderate")

    def test_score_5(self):
        """Score 5 should be 'Very Strong'."""
        result = check_strength("Abc123!@#Def456$%^")
        self.assertEqual(result, "Very Strong")


# import pytest
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])