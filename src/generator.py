"""
The password generator app.

A small application that allows you to generate a password of any complexity using a user-friendly
graphical interface with accessible settings and save it in a convenient 'txt' file so you don't forget
your social media passwords.
"""


from secrets import choice
import string
import time
import sys


# ===============================================================================================
# 1. AUXILIARY FUNCTIONS
# ===============================================================================================


def greed():
    """
    Display welcome message.

    Shows a formatted welcome screen with emojis and explains the goal
    of the game. Includes short pauses for better user experience.
    """
    print("\n" + "=" * 50)
    print("🔑 Welcome to the 'Personal Password Generator'!")
    print("=" * 50)

    time.sleep(0.5)
    print("🛡️ You can create a password of the developer's specified "
          "length (from 16 to 64) and flexibly customize it to suit "
          "your needs!")


def get_number(prompt):
    """
       Get a valid integer from the user.

       Continuously prompts the user until a valid integer is entered.
       Handles ValueError exceptions and displays an error message.
       """
    while True:
        try:
            user_length = int(input(prompt))
            if user_length < 16:
                print("⚠️ Warning! The your password is too short!")
                print("🛡️ The password must be at least 16 characters long!")
                continue
            if user_length > 64:
                print("⚠️ Warning! The password is too long!")
                print("🛡️ The password must be at least 64 characters long!")
                continue
            return user_length
        except ValueError:
            print("❌ Error! Please enter a number!")


# ==============================================================================================
# 2. APP LOGIC
# ==============================================================================================


def get_character_options():
    """
    Get password complexity settings from the user
    based on the presence of letters, numbers, and symbols.

    Returns data for creating a password.
    """
    user_letters = input("Include letters? (y/n): ").lower() == 'y'
    user_digits = input("Include digits? (y/n): ").lower() == 'y'
    user_symbols = input("Include symbols? (y/n): ").lower() == 'y'
    return user_letters, user_digits, user_symbols


def build_character_pool(user_letters, user_digits, user_symbols):
    """
    Input data for the settings for the future password.
    """
    characters = ""
    if user_letters:
        characters += string.ascii_letters
    if user_digits:
        characters += string.digits
    if user_symbols:
        characters += string.punctuation
    return characters


def generate_password(length, character_pool):
    """
    Generate a password based on the entered data.

    Generation will not occur if the user has not previously
    selected password settings (no letters, numbers, or symbols).
    """
    if not character_pool:
        print("❌ Error! No characters selected!")
        return None
    return "".join(choice(character_pool) for _ in range(length))


def check_strength(password):
    """
    Password strength check based on input data.
    Total password length, including presence of letters,
    numbers, and symbols.

    """
    score = 0

    # Check length
    if 16 <= len(password) <= 29:
        score += 1
    if len(password) >= 30:
        score += 2

    # Check all symbols
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()" for c in password):
        score += 1

    # Return result
    if score <= 2:
        return f"Not Safe"
    elif score <= 4:
        return f"Moderate"
    else:
        return f"Very Strong"


def generate_again():
    """
    Asks the user if he wants to repeat the generation of a new password.
    """
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


# ============================================================================================
# 3. MAIN FUNC
# ============================================================================================


def main():
    """
    The main controller of the application.

    Greets the user and starts the application cycle. After each cycle,
    asks the user if they want to restart the generation.
    """
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

        print(check_strength(user_password))

        if not generate_again():
            print("\n" + "=" * 55)
            print("👋 Thank you for using my Password Generator! Goodbye!")
            print("=" * 55)
            break

        else:
            print("\nReloading..", end="", flush=True)
            for _ in range(3):
                time.sleep(1)
                print(".", end="", flush=True)


# This code will be removed in the future.
# It was added to test code within a file without connecting the interface.

# if __name__ == "__main__":
#     main()