import inspect

users = [
    {"username": "john_doe", "password": "aB3#xY9", "payload": "User data for John Doe"},
    {"username": "alice_smith", "password": "pQ7&wZ2", "payload": "User data for Alice Smith"},
    {"username": "bob_jones", "password": "mN5%tR8", "payload": "User data for Bob Jones"},
    {"username": "emma_wilson", "password": "kL1@vX4", "payload": "User data for Emma Wilson"},
    {"username": "mike_brown", "password": "qW9!cD6", "payload": "User data for Mike Brown"},
    {"username": "sara_taylor", "password": "fG3^hJ7", "payload": "User data for Sara Taylor"},
    {"username": "james_miller", "password": "rT8&yU2", "payload": "User data for James Miller"},
    {"username": "lily_davis", "password": "zX6#bV5", "payload": "User data for Lily Davis"},
    {"username": "david_clark", "password": "nM4!wQ3", "payload": "User data for David Clark"},
    {"username": "olivia_white", "password": "vK7@pL9", "payload": "User data for Olivia White"},
]

class User:
    def __init__(self, login: str, password: str, balance: int):
        self.login: str = login
        self.password: str = password
        self.balance: int = balance

class Database:
    users = {
        1: User(
            login="john",
            password="john",
            balance=0
        ),
        2: User(
            login="marry",
            password="marry",
            balance=0,
        ),
    }

class Price:
    EXCHANGE = {
        "USD": 1.1,  # 1 USD = 1.1 CHF или же франки
        "EUR": 0.9,  # 1 EUR = 0.9 CHF  или же франки
        "CHF": 1.0   # 1 CHF = 1 CHF или же франки
    }

    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def convert_to(self, target_currency):
        """Конвертирует сумму в указанную валюту через CHF."""
        if self.currency == target_currency:
            return self.amount
        chf_amount = self.amount / Price.EXCHANGE[self.currency]
        return chf_amount * Price.EXCHANGE[target_currency]

    def __add__(self, other):
        if self.currency == other.currency:
            return Price(self.amount + other.amount, self.currency)
        converted_amount = other.convert_to(self.currency)
        return Price(self.amount + converted_amount, self.currency)

    def __sub__(self, other):
        if self.currency == other.currency:
            return Price(self.amount - other.amount, self.currency)
        converted_amount = other.convert_to(self.currency)
        return Price(self.amount - converted_amount, self.currency)

    def __repr__(self):
        return f"{self.amount} {self.currency}"


current_user = None


def auth(func):
    def wrapper(*args, **kwargs):
        global current_user
        if current_user:
            return func(*args, **kwargs)
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")
            for user in users:
                if user["username"] == username and user["password"] == password:
                    print("Authorization successful!")
                    current_user = user
                    return func(*args, **kwargs)
            print("Invalid username or password. Try again.")
    return wrapper


@auth
def command(payload):
    print(f"Executing command by authorized user.\nPayload: {payload}")


class PaymentSystem:
    def __init__(self, user: dict):
        self.connected_to_the_atm = False
        self.user = user

    def deposit(self, amount: int):
        self.user["balance"] += amount
        print(f"Deposited {amount}. Total balance: {self.user['balance']}")

    def withdraw(self, amount: int):
        if amount > self.user["balance"]:
            print("Insufficient funds")
            return
        self._validate_money()
        self._connect_to_the_atm()
        self._count_the_cash(amount)
        self._get_money(amount)

    def _validate_money(self):
        if self.user["balance"] < 0:
            print("Account balance is invalid")
        else:
            print("Money validated")

    def _connect_to_the_atm(self):
        self.connected_to_the_atm = True
        print("Connected to ATM")

    def _count_the_cash(self, amount: int):
        if self.connected_to_the_atm:
            print(f"Counting {amount} in the ATM")
        else:
            print("ATM connection failed")

    def _get_money(self, amount: int):
        if self.connected_to_the_atm:
            self.user["balance"] -= amount
            print(f"Withdrew {amount}. Remaining balance: {self.user['balance']}")
        else:
            print("ATM connection failed")

    def balance(self):
        print(f"Current balance: {self.user['balance']}")


def output():
    payment_system = None
    while True:
        print("\nHello user, welcome to the bank Johnshpohon")
        print("\nAvailable commands:")
        print("1. Login")
        print("2. Execute command")
        print("3. Price operations")
        print("4. Deposit money")
        print("5. Withdraw money")
        print("6. Check balance")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            for user in users:
                if user["username"] == username and user["password"] == password:
                    print("Authorization successful!")
                    global current_user
                    current_user = user
                    payment_system = PaymentSystem(user)
                    print(f"User info: Username: {user['username']}, Balance: {user.get('balance', 0)}")
                    break
            else:
                print("Invalid username or password.")

        elif choice == "2":
            if not current_user:
                print("You need to login first.")
                continue
            command(current_user["payload"])

        elif choice == "3":
            try:
                amount1 = float(input("Enter first amount: "))
                currency1 = input("Enter first currency (USD/EUR/CHF): ").upper()
                amount2 = float(input("Enter second amount: "))
                currency2 = input("Enter second currency (USD/EUR/CHF): ").upper()
                operation = input("Choose operation (+/-): ")
                price1 = Price(amount1, currency1)
                price2 = Price(amount2, currency2)
                if operation == "+":
                    result = price1 + price2
                    print(f"Result: {result}")
                elif operation == "-":
                    result = price1 - price2
                    print(f"Result: {result}")
                else:
                    print("Invalid operation.")
            except ValueError:
                print("Invalid input for price operations.")

        elif choice == "4":
            if not payment_system:
                print("You need to login first.")
                continue
            try:
                amount = int(input("Enter deposit amount: "))
                payment_system.deposit(amount)
            except ValueError:
                print("Invalid input for deposit amount.")

        elif choice == "5":
            if not payment_system:
                print("You need to login first.")
                continue
            try:
                amount = int(input("Enter withdrawal amount: "))
                payment_system.withdraw(amount)
            except ValueError:
                print("Invalid input for withdrawal amount.")

        elif choice == "6":
            if not payment_system:
                print("You need to login first.")
                continue
            payment_system.balance()

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    output()