"""
Test script for the generator module.
"""

import os
import csv
import json
from src.generator import save_passwords_csv, save_passwords_json, save_passwords_txt


def get_test_passwords():
    """Return a lisr of test passwords."""
    return [
        {"service": "Google", "login": "user@gmail.com", "password": "P@ssw0rd!"},
        {"service": "GitHub", "login": "username", "password": "Abc123!"}
    ]


def test_save_passwords_csv():
    """Test save_passwords_csv function."""
    test_passwords = get_test_passwords()
    file_path = "test_passwords.csv"

    try:
        save_passwords_csv(file_path, test_passwords)

        assert os.path.exists(file_path), "File was not created!"

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2, "Wrong number of rows!"
            assert rows[0]["service"] == "Google", "Wrong service name!"

        print("✅ All tests for csv format passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("🗑️ Test file removed.")


def test_save_passwords_json():
    """Test save_passwords_json function."""
    test_passwords = get_test_passwords()
    file_path = "test_passwords.json"

    try:
        save_passwords_json(file_path, test_passwords)

        assert os.path.exists(file_path), "File was not created!"

        with open(file_path, "r", encoding="utf-8") as f:
            rows = json.load(f)
            assert len(rows) == 2, "Wrong number of rows!"
            assert rows[0]["service"] == "Google", "Wrong service name!"

        print("✅ All tests for json format passed!")

    except Exception as e:
        print(f"❌ Test failed:{e}")
        raise
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("🗑️ Test file removed.")


def test_save_passwords_txt():
    """Test save_passwords_txt function."""
    test_passwords = get_test_passwords()
    file_path = "text_passwords.txt"

    try:
        save_passwords_txt(file_path, test_passwords), "File was not created!"

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 2, "Wrong number of lines!"

            expected = "Service: Google | Login/email: user@gmail.com | Password: P@ssw0rd!\n"
            assert lines[0] == expected, "Wrong content in first line!"

        print("✅ All tests for txt format passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        if os.remove(file_path):
            os.remove(file_path)
            print("🗑️ Test file removed.")


def test_empty_passwords_csv():
    """Test save_passwords_csv with empty list."""
    file_path = "test_empty.csv"

    try:
        save_passwords_csv(file_path, [])

        assert os.path.exists(file_path), "File was not created!"

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 0, "File should be empty!"

        print("✅ Empty CSV test passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("🗑️ Tests file removed.")


def test_empty_passwords_json():
    """Test save_passwords_json with empty list."""
    file_path = "test_empty.json"

    try:
        save_passwords_json(file_path, [])

        assert os.path.exists(file_path), "File was not created!"

        with open(file_path, "r", encoding="utf-8") as f:
            rows = json.load(f)
            assert len(rows) == 0, "File should be empty!"

        print("✅ Empty JSON test passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("🗑️ Test file removed.")


def test_empty_passwords_txt():
    """Test save_passwords_txt with empty list."""
    file_path = "test_empty.txt"

    try:
        save_passwords_txt(file_path, [])

        assert os.path.exists(file_path), "File was not created!"

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert content == "", "File should be empty!"

        print("✅ Empty TXT test passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("🗑️ Test file removed.")


if __name__ == "__main__":
    test_save_passwords_csv()
    test_save_passwords_json()
    test_save_passwords_txt()
    test_empty_passwords_csv()
    test_empty_passwords_json()
    test_empty_passwords_txt()

