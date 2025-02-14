import sqlite3
import hashlib
import os
from getpass import getpass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_database():
    with sqlite3.connect("fitness_tracker.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                weight REAL,
                height REAL,
                fitness_goals TEXT
            )
        ''')
        conn.commit()

class FitnessTracker:
    def __init__(self):
        self.current_user_id = None

    def register(self):
        try:
            clear_screen()
            print("--- Register ---")
            username = input("Enter a username: ")
            password = getpass("Enter a password: ")
            age = int(input("Enter your age: "))
            weight = float(input("Enter your weight (kg): "))
            height = float(input("Enter your height (cm): "))
            fitness_goals = input("Enter your fitness goals: ")

            hashed_password = hash_password(password)

            with sqlite3.connect("fitness_tracker.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password, age, weight, height, fitness_goals)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, hashed_password, age, weight, height, fitness_goals))
                conn.commit()

            print("Registration successful!")
        except sqlite3.IntegrityError:
            print("Error: Username already exists. Try another one.")
        except Exception as e:
            print(f"Error: {e}")

    def login(self):
        try:
            clear_screen()
            print("--- Login ---")
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")
            hashed_password = hash_password(password)

            with sqlite3.connect("fitness_tracker.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id FROM users WHERE username = ? AND password = ?
                ''', (username, hashed_password))
                result = cursor.fetchone()

            if result:
                self.current_user_id = result[0]
                print("Login successful!")
                return True
            else:
                print("Invalid username or password.")
                return False
        except Exception as e:
            print(f"Error: {e}")

    def logout(self):
        self.current_user_id = None
        print("Logged out.")

# Main Program
def main():
    initialize_database()
    tracker = FitnessTracker()

    while True:
        clear_screen()
        print("Welcome to the Fitness Tracker App")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            tracker.register()
            input("Press Enter to return to the main menu...")
        elif choice == "2":
            if tracker.login():
                print("Welcome to your dashboard!")
                input("Press Enter to continue...")
        elif choice == "3":
            print("Exiting the app. Goodbye!")
            break
        else:
            print("Invalid choice.")
            input("Press Enter to try again...")

if __name__ == "__main__":
    main()
