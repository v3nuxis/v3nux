# import inspect
#
import csv

from lessons.repo import IOTextWSr


# users = [
#     {"username": "john_doe", "password": "aB3#xY9", "payload": "User data for John Doe"},
#     {"username": "alice_smith", "password": "pQ7&wZ2", "payload": "User data for Alice Smith"},
#     {"username": "bob_jones", "password": "mN5%tR8", "payload": "User data for Bob Jones"},
#     {"username": "emma_wilson", "password": "kL1@vX4", "payload": "User data for Emma Wilson"},
#     {"username": "mike_brown", "password": "qW9!cD6", "payload": "User data for Mike Brown"},
#     {"username": "sara_taylor", "password": "fG3^hJ7", "payload": "User data for Sara Taylor"},
#     {"username": "james_miller", "password": "rT8&yU2", "payload": "User data for James Miller"},
#     {"username": "lily_davis", "password": "zX6#bV5", "payload": "User data for Lily Davis"},
#     {"username": "david_clark", "password": "nM4!wQ3", "payload": "User data for David Clark"},
#     {"username": "olivia_white", "password": "vK7@pL9", "payload": "User data for Olivia White"},
# ]
#
# class User:
#     def __init__(self, login: str, password: str, balance: int):
#         self.login: str = login
#         self.password: str = password
#         self.balance: int = balance
#
# class Database:
#     users = {
#         1: User(
#             login="john",
#             password="john",
#             balance=0
#         ),
#         2: User(
#             login="marry",
#             password="marry",
#             balance=0,
#         ),
#     }
#
# class Price:
#     EXCHANGE = {
#         "USD": 1.1,
#         "EUR": 0.9,
#         "CHF": 1.0
#     }
#
#     def __init__(self, amount: float, currency: str):
#         if currency not in Price.EXCHANGE:
#             raise ValueError(f"Unsupported currency: {currency}")
#         self.amount = amount
#         self.currency = currency
#
#     def convert_to(self, target_currency: str) -> float:
#         """Converts the amount to the specified target currency."""
#         if target_currency not in Price.EXCHANGE:
#             raise ValueError(f"Unsupported target currency: {target_currency}")
#         if self.currency == target_currency:
#             return self.amount
#         chf_amount = self.amount / Price.EXCHANGE[self.currency]
#         return chf_amount * Price.EXCHANGE[target_currency]
#
#     def __add__(self, other: 'Price') -> 'Price':
#         if not isinstance(other, Price):
#             raise TypeError("Operand must be an instance of Price")
#         if self.currency == other.currency:
#             return Price(self.amount + other.amount, self.currency)
#         converted_amount = other.convert_to(self.currency)
#         return Price(self.amount + converted_amount, self.currency)
#
#     def __sub__(self, other: 'Price') -> 'Price':
#         if not isinstance(other, Price):
#             raise TypeError("Operand must be an instance of Price")
#         if self.currency == other.currency:
#             return Price(self.amount - other.amount, self.currency)
#         converted_amount = other.convert_to(self.currency)
#         return Price(self.amount - converted_amount, self.currency)
#
#     def __repr__(self) -> str:
#         return f"{self.amount} {self.currency}"
#
#
# current_user = None
#
#
# def auth(func):
#     def wrapper(*args, **kwargs):
#         global current_user
#         if current_user:
#             return func(*args, **kwargs)
#         while True:
#             username = input("Enter username: ").strip()
#             if not username:
#                 print("Username cannot be empty.")
#                 continue
#             password = input("Enter password: ").strip()
#             if not password:
#                 print("Password cannot be empty.")
#                 continue
#             for user in users:
#                 if user["username"] == username and user["password"] == password:
#                     print("Authorization successful!")
#                     current_user = user
#                     return func(*args, **kwargs)
#             print("Invalid username or password. Try again.")
#     return wrapper
#
#
# @auth
# def command(payload):
#     print(f"Executing command by authorized user.\nPayload: {payload}")
#
#
# class PaymentSystem:
#     def __init__(self, user: dict):
#         self.connected_to_the_atm = False
#         self.user = user
#         self.user.setdefault("balance", 0)
#
#     def deposit(self, amount: int):
#         if amount <= 0:
#             print("Deposit amount must be positive.")
#             return
#         self.user["balance"] += amount
#         print(f"Deposited {amount}. Total balance: {self.user['balance']}")
#
#     def withdraw(self, amount: int):
#         if amount <= 0:
#             print("Withdrawal amount must be positive.")
#             return
#         if amount > self.user["balance"]:
#             print("Insufficient funds")
#             return
#         self._validate_money()
#         self._connect_to_the_atm()
#         self._count_the_cash(amount)
#         self._get_money(amount)
#
#     def _validate_money(self):
#         if self.user["balance"] < 0:
#             print("Account balance is invalid")
#         else:
#             print("Money validated")
#
#     def _connect_to_the_atm(self):
#         self.connected_to_the_atm = True
#         print("Connected to ATM")
#
#     def _count_the_cash(self, amount: int):
#         if self.connected_to_the_atm:
#             print(f"Counting {amount} in the ATM")
#         else:
#             print("ATM connection failed")
#
#     def _get_money(self, amount: int):
#         if self.connected_to_the_atm:
#             self.user["balance"] -= amount
#             print(f"Withdrew {amount}. Remaining balance: {self.user['balance']}")
#         else:
#             print("ATM connection failed")
#
#     def balance(self):
#         print(f"Current balance: {self.user['balance']}")
#
#
# def output():
#     global current_user
#     payment_system = None
#
#     while True:
#         if not current_user:
#             print("\nHello user, welcome to the bank Johnshpohon")
#             print("For use you ought to login into this bank")
#             print("1. Login")
#             print("2. Exit")
#             choice = input("Choose an option: ")
#
#             if choice == "1":
#                 username = input("Enter username: ")
#                 password = input("Enter password: ")
#                 for user in users:
#                     if user["username"] == username and user["password"] == password:
#                         print("Authorization successful!")
#                         current_user = user
#                         payment_system = PaymentSystem(user)
#                         print(f"User info: Username: {user['username']}, Balance: {user.get('balance', 0)}")
#                         break
#                 else:
#                     print("Invalid username or password.")
#                     continue
#
#             elif choice == "2":
#                 print("Exiting...")
#                 return
#
#             else:
#                 print("Invalid choice. Please try again.")
#                 continue
#
#         else:
#             print("\nAvailable commands:")
#             print("1. Execute command")
#             print("2. Price operations")
#             print("3. Deposit money")
#             print("4. Withdraw money")
#             print("5. Check balance")
#             print("6. Exit")
#             choice = input("Choose an option: ")
#
#             if choice == "1":
#                 command(current_user["payload"])
#
#             elif choice == "2":
#                 try:
#                     amount1 = float(input("Enter first amount: "))
#                     currency1 = input("Enter first currency (USD/EUR/CHF): ").upper()
#                     amount2 = float(input("Enter second amount: "))
#                     currency2 = input("Enter second currency (USD/EUR/CHF): ").upper()
#                     operation = input("Choose operation (+/-): ")
#                     price1 = Price(amount1, currency1)
#                     price2 = Price(amount2, currency2)
#                     if operation == "+":
#                         result = price1 + price2
#                         print(f"Result: {result}")
#                     elif operation == "-":
#                         result = price1 - price2
#                         print(f"Result: {result}")
#                     else:
#                         print("Invalid operation.")
#                 except ValueError as e:
#                     print(f"Error: {e}")
#
#             elif choice == "3":
#                 if not payment_system:
#                     print("You need to login first.")
#                     continue
#                 try:
#                     amount = int(input("Enter deposit amount: "))
#                     payment_system.deposit(amount)
#                 except ValueError:
#                     print("Invalid input for deposit amount.")
#
#             elif choice == "4":
#                 if not payment_system:
#                     print("You need to login first.")
#                     continue
#                 try:
#                     amount = int(input("Enter withdrawal amount: "))
#                     payment_system.withdraw(amount)
#                 except ValueError:
#                     print("Invalid input for withdrawal amount.")
#
#             elif choice == "5":
#                 if not payment_system:
#                     print("You need to login first.")
#                     continue
#                 payment_system.balance()
#
#             elif choice == "6":
#                 print("Exiting...")
#                 return
#
#             else:
#                 print("Invalid choice. Please try again.")
#
#
# if __name__ == "__main__":
#     output()


GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}

class Configuration:
    def __init__(self, updates, validator=None):
        self.updates = updates
        self.validator = validator
        self.original_config = None

    def __enter__(self):
        self.original_config = GLOBAL_CONFIG.copy()
        GLOBAL_CONFIG.update(self.updates)
        if self.validator:
            try:
                if not self.validator(GLOBAL_CONFIG):
                    raise ValueError("Invalid configuration after applying updates.")
            except ValueError as e:
                GLOBAL_CONFIG.clear()
                GLOBAL_CONFIG.update(self.original_config)
                raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            GLOBAL_CONFIG.clear()
            GLOBAL_CONFIG.update(self.original_config)
        except Exception as e:
            print(f"Error {e}")

def validate_config(config):
    return config.get("max_retries", 0) >= 0

# Test with valid updates
print("Original Configuration:", GLOBAL_CONFIG)
with Configuration({"feature_a": False, "max_retries": 5}, validator=validate_config):
    print("Inside Context (Valid Updates):", GLOBAL_CONFIG)
print("Restored Configuration:", GLOBAL_CONFIG)

# Test with invalid updates
try:
    with Configuration({"max_retries": -1}, validator=validate_config):
        print("Inside Context (Invalid Updates):", GLOBAL_CONFIG)
except ValueError as e:
    print("Validation Error:", e)
print("Restored Configuration:", GLOBAL_CONFIG)

# Test with an error inside the context
try:
    with Configuration({"feature_a": False}, validator=validate_config):
        print("Inside Context (Before Error):", GLOBAL_CONFIG)
        raise RuntimeError("An error occurred!")
except RuntimeError as e:
    print("Caught Exception:", e)
print("Restored Configuration:", GLOBAL_CONFIG)
