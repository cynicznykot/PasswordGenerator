from src.generator import save_passwords_csv

test_passwords = [
    {"service": "Google", "login": "user@gmail.com", "password": "P@ssw0rd!"},
    {"service": "GitHub", "login": "username", "password": "Abc123!"}
]

save_passwords_csv("test_passwords.csv", test_passwords)