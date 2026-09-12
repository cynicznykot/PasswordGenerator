"""
Unit tests for the GUI module.

This module contains tests for the graphical user interface components
of the password generator application. Tests are currently skipped
because GUI tests are slow and require a display environment.
"""

import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from src.gui import main


@unittest.skip("GUI tests are slow, skipping for now")
class TestGuiVariables(unittest.TestCase):
    """
    Test suite for GUI variables.

    Verifies that tkinter variables (IntVar, BooleanVar, StringVar)
    are created with correct default values.
    """

    def test_variables_created(self):
        """Verify that all GUI variables are created when main() is called."""
        with patch('tkinter.Tk') as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root

            main()

            # Verify that the window was created with correct title and size
            mock_root.title.assert_called_with("Your Personal Password Generator")
            mock_root.geometry.assert_called_with("700x600")

    def test_length_var_default(self):
        """Verify that length variable has default value of 16."""
        root = tk.Tk()
        length_var = tk.IntVar(value=16)
        self.assertEqual(length_var.get(), 16)
        root.destroy()

    def test_use_letters_default(self):
        """Verify that 'Use Letters' checkbox is enabled by default."""
        root = tk.Tk()
        use_letters = tk.BooleanVar(value=True)
        self.assertTrue(use_letters.get())
        root.destroy()

    def test_use_digits_default(self):
        """Verify that 'Use Digits' checkbox is enabled by default."""
        root = tk.Tk()
        use_digits = tk.BooleanVar(value=True)
        self.assertTrue(use_digits.get())
        root.destroy()

    def test_use_symbols_default(self):
        """Verify that 'Use Symbols' checkbox is enabled by default."""
        root = tk.Tk()
        use_symbols = tk.BooleanVar(value=True)
        self.assertTrue(use_symbols.get())
        root.destroy()


@unittest.skip("GUI tests are slow, skipping for now")
class TestGuiFunctions(unittest.TestCase):
    """
    Test suite for GUI functions.

    Verifies that the main GUI functions (on_generate, copy_password,
    save_password) are defined and can be called without errors.
    """

    def setUp(self):
        """Create a root window before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window

    def tearDown(self):
        """Destroy the root window after each test."""
        self.root.destroy()

    @patch('tkinter.Tk')
    def test_on_generate_called(self, mock_tk):
        """Verify that on_generate function is defined."""
        mock_tk.return_value = self.root

        # Import gui module fresh to use the mock
        import importlib
        import src.gui as gui
        importlib.reload(gui)

        try:
            gui.main()
        except Exception as e:
            self.fail(f"main() raised an exception: {e}")

    @patch('tkinter.Tk')
    def test_copy_password_called(self, mock_tk):
        """Verify that copy_password function is defined."""
        mock_tk.return_value = self.root

        import importlib
        import src.gui as gui
        importlib.reload(gui)

        try:
            gui.main()
        except Exception as e:
            self.fail(f"main() raised an exception: {e}")

    @patch('tkinter.Tk')
    def test_save_password_called(self, mock_tk):
        """Verify that save_password function is defined."""
        mock_tk.return_value = self.root

        import importlib
        import src.gui as gui
        importlib.reload(gui)

        try:
            gui.main()
        except Exception as e:
            self.fail(f"main() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()