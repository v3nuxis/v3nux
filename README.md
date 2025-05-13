Lesson 5

## Bank System Project
This project simulates a simple banking system with user authentication, payment operations, and price calculations. Below is a detailed description of the project and how to use it.

Table of Contents
Features
How to Use
Commands
Classes and Functionality
Contributing
Features
User Authentication : Users can log in using their username and password. After successful login, the system displays the user's information (username and balance).
Payment System : Users can perform banking operations such as depositing money, withdrawing money, and checking their balance.
Price Operations : The system supports currency conversion between USD, EUR, and CHF (Swiss Francs). Users can perform addition and subtraction operations on amounts with different currencies.
Payload Display : Each user has a unique payload that is displayed when executing a command after logging in.
Classes and Functionality
1. Price Class
Handles currency operations (addition, subtraction, and conversion).
Supports the following currencies: USD, EUR, CHF.
Automatically converts amounts to a common currency (CHF) for operations involving different currencies.
2. PaymentSystem Class
Manages user-specific banking operations.
Includes methods for depositing money, withdrawing money, and checking the balance.
3. auth Decorator
Ensures that only authorized users can execute certain commands.
Caches the user's login status to avoid repeated authentication.
4. User and Database Classes
Represent user data and store user information (username, password, balance).
Simulates a database of users.