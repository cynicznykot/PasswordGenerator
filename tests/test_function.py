"""
Test script for the generator module.
"""

import os
import csv
from src.generator import save_passwords_csv

def test_save_passwords_csv():
    """Test save_passwords_csv function."""
    test_passwords = [
        {"service": "Google", "login": "user@gmail.com", "password": "P@ssw0rd!"},
        {"service": "GitHub", "login": "username", "password": "Abc123!"}
    ]

    file_path = "test_passwords.csv"

    save_passwords_csv(file_path, test_passwords)

    assert os.path.exists(file_path), "File was not created!"

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2, "Wrong number of rows!"
        assert rows[0]["service"] == "Google", "Wrong service name!"

    print("✅ All tests passed!")

    os.remove(file_path)
    print("🗑️ Test file removed.")

if __name__ == "__main__":
    test_save_passwords_csv()