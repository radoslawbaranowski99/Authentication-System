#Importing necessary libraries
import re
import hashlib
from datetime import datetime
import os

# Defining file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Audit = os.path.join(BASE_DIR, "audit.log.txt")
Users = os.path.join(BASE_DIR, "users.txt")

# Creating files if they do not exist
for file_path in [Audit, Users]:
    if not os.path.exists(file_path):
        open(file_path, "w", encoding="utf-8").close()

#Hashing passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Checking password strength
def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special symbol."
    return True, "Password is strong."

# Logging activities
def log_activity(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(Audit, "a", encoding="utf-8") as file:
        file.write(f"{timestamp}: {event}\n")

# Validating username
def is_valid_username(username):
    if not username:
        return False, "Username cannot be empty."
    if " " in username:
        return False, "Username cannot contain spaces."
    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, "Username is valid."

#Registration function
def register_user():
    raw_username = input("Enter a username: ")
    username = raw_username.strip()

# Validating username
    is_valid, msg = is_valid_username(username)
    if not is_valid:
        print(f"Invalid username: {msg}")
        log_activity(f"Failed registration attempt for username: '{raw_username}'")
        return
# Checking if user already exists   
    with open(Users, "r", encoding="utf-8") as file:
        existing_users = [line.strip().split(":")[0] for line in file]
        if username in existing_users:
            print(f"User {username} is already registered.")
            log_activity(f"Failed registration attempt for existing user: {username}")
            return
# Getting and validating password      
    password = input("Enter a password: ")
    is_valid, feedback = is_strong_password(password)
    if not is_valid:
        print("Password is not strong enough:")
        print(feedback)
        log_activity(f"Failed registration attempt for username: {username}")
        return
# Saving new user    
    hashed_password = hash_password(password)
    with open(Users, "a", encoding="utf-8") as file:
        file.write(f"{username}:{hashed_password}\n")
    print(f"User {username} registered successfully!")
    log_activity(f"User registered: {username}")
    return username, password

#Login function
def login_user():
    username = input("Enter your username: ").strip()
    is_valid, msg = is_valid_username(username)
    if not is_valid:
        print(f"Invalid username: {msg}")
        log_activity(f"Failed login attempt for username: {username}")
        return
  # Getting password and verifying  
    password = input("Enter your password: ")
    with open(Users, "r", encoding="utf-8") as file:
        users = file.readlines()
    for user in users:
        stored_username, stored_password = user.strip().split(":")
        stored_username = stored_username.strip()
        if username == stored_username and hash_password(password) == stored_password:
            print(f"User: {username} logged in successfully!")
            log_activity(f"User logged in: {username}")
            post_login_menu(username)
            return
    print("Login failed. Invalid username or password.")
    log_activity(f"Failed login attempt for username: {username}")

# Viewing logs
def view_logs(username):
    print(f"\nLogs for user '{username}':")
    with open(Audit, "r", encoding="utf-8") as log_file:
        logs = log_file.readlines()
    
    user_logs = [log.strip() for log in logs if username in log]
    if user_logs:
        for log in user_logs:
            print(log)
    else:
        print("No logs found for this user.")

#Post login menu
def post_login_menu(username):
    while True:
        print("\nPost Login Menu")
        print("1. View Logs")
        print("2. Logout")
        choice = input("Please enter your choice: ")

        if choice == "1":
            view_logs(username)
        elif choice == "2":
            print(f"User {username} logged out.")
            log_activity(f"User logged out: {username}")
            break
        else:
            print("Invalid choice, please try again.")

#Main Menu
def main():
    while True:
        print("\nWelcome to the User Registration and Login System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Please enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Exiting the system")
            log_activity("System exited")
            break
        else:
            print("Invalid choice, please try again.")

# Running the main function
main()
