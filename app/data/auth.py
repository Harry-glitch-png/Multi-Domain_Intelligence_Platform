import bcrypt
import re

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=10)
    hashed = (bcrypt.hashpw(password_bytes, salt)).decode("utf-8")
    return hashed

def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))

def register_user(username, password):
    if user_exists(username):
        return False
    else:
        with open(USER_DATA_FILE, "a") as udf:
            hashed_password = hash_password(password)
            udf.write(username + " " + hashed_password + "\n")
            return True

def user_exists(username):
    with open(USER_DATA_FILE, "r") as udf:
        for line in udf:
            stored_user, _ = line.strip().split(" ")
            if stored_user == username:
                return True
    return False

def login_user(username, password):
    with open(USER_DATA_FILE, "r") as udf:
        for line in udf:
            stored_user, stored_hash = line.strip().split()
            if stored_user == username and verify_password(password, stored_hash):
                return True
    print("Invalid username or password.")
    return False

def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 20:
        return False, "Username must be at most 20 characters long."

    if re.search(r" ", username):
        return False, "There can be no spaces in your username."
    elif re.search(r"[a-zA-Z]", username):
        return True, "Valid username."
    return False, "The must be alphanumeric characters in your username."

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 50:
        return False, "Password must be at most 50 characters long."
    if re.search(r" ", password):
        return False, "There can be no spaces in your password"
    elif (
    re.search(r"[a-z]", password) and
    re.search(r"[A-Z]", password) and
    re.search(r"\d", password) and
    re.search(r"[!@#$%^&*()_+=\-{}[\]:;\"'<>,.?/]", password)
    ):
        return True, "Valid password."
    return False, "Password must contain uppercase and lowercase letters, and at less one number and special character."

def display_menu():
 """Displays the main menu options."""
 print("\n" + "="*50)
 print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
 print(" Secure Authentication System")
 print("="*50)
 print("\n[1] Register a new user")
 print("[2] Login")
 print("[3] Exit")
 print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user

            if register_user(username, password):
                print(f"\nSuccess: User '{username}' registered successfully!")
            else:
                print(f"\nFailure: Username '{username}' already exists.")

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")

            # Optional: Ask if they want to logout or exit
            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
 main()