import random
import string
import time
import sys


# --- 1. AUXILIARY FUNCTIONS ---


def greed():
    print("\n" + "=" * 50)
    print("🔑 Welcome to the 'Personal Password Generator'!")
    print("=" * 50)

    time.sleep(0.3)
    print("🛡️ You can create a password of any length and flexibly customize it to suit your needs!")


def get_number(prompt):
    while True:
        try:
            user_length = int(input(prompt))
            if user_length < 5:
                print("⚠️ Warning! The your password is too short!")
                print("🛡️ The password must be at least 5 characters long!")
                continue
            return user_length
        except ValueError:
            print("❌ Error! Please enter a number!")


# --- 2. APP LOGIC


def get_character_options():
    user_letters = input("Include letters? (y/n): ").lower() == 'y'
    user_digits = input("Include digits? (y/n): ").lower() == 'y'
    user_symbols = input("Include symbols? (y/n): ").lower() == 'y'
    return user_letters, user_digits, user_symbols


def build_character_pool(user_letters, user_digits, user_symbols):
    characters = ""
    if user_letters:
        characters += string.ascii_letters
    if user_digits:
        characters += string.digits
    if user_symbols:
        characters += string.punctuation
    return characters


def generate_password(length, character_pool):
    if not character_pool:
        print("❌ Error! No characters selected!")
        return None
    return "".join(random.choice(character_pool) for _ in range(length))


def generate_again():
    user_answer = input("Do you want to generate another password? (y/n): ").lower()
    possitive = ['y', 'yes', 'yeah', 'da', 'd', 'a']
    negative = ['n', 'no', 'not', 'net', 'nope']

    if user_answer in possitive:
        return True
    elif user_answer in negative:
        return False
    else:
        print("⚠️ Please answer 'y' or 'n'!")
        return generate_again()


# --- 3. MAIN FUNC


def main():
    while True:
        greed()
        user_length = get_number("Enter your password length: ")

        print("\nChoose character types: ")
        user_letters, user_digits, user_symbols = get_character_options()

        character_pool = build_character_pool(user_letters, user_digits, user_symbols)

        if not character_pool:
            print("❌ You must choose at least one character type!")
            continue

        user_password = generate_password(user_length, character_pool)

        print("\n" + "=" * 50)
        print(f"✅ Your generated password: {user_password}")
        print("=" * 50)

        if not generate_again():
            print("👋 Thank you for using my Password Generator! Goodbye!")
            break

        else:
            print("\nReloading..", end="", flush=True)
            for _ in range(3):
                time.sleep(1)
                print(".", end="", flush=True)


# --- 4. ENTRY POINT ---

if __name__ == "__main__":
    main()
