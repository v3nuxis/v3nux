# Price Class Implementation

## Description
The `Price` class allows performing arithmetic operations (addition and subtraction) on monetary values with support for currency conversion using the Alpha Vantage API.

## Features
- **Currency Support**: Handles different currencies and performs operations in a common intermediate currency (`CHF`).
- **API Integration**: Fetches real-time exchange rates from [Alpha Vantage](https://www.alphavantage.co). 
- **Asynchronous Operations**: Uses `aiohttp` for non-blocking API requests.
- **Error Handling**: Provides custom exceptions for invalid data or network issues.

## Usage

### 1. Initialize Price Objects
Create instances of the `Price` class with an amount, currency, and API key:
```python
a = Price(100, "USD", api_key="YOUR_API_KEY")
b = Price(150, "UAH", api_key="YOUR_API_KEY")

2. Perform Arithmetic Operations
Use the + and - operators to add or subtract Price objects:

c = await a.__add__(b)  # Addition
d = await a.__sub__(b)  # Subtraction
3. View Results
Print the results to see the calculated values:

Example Output
Addition: Price(amount=103.75, currency='USD')
Subtraction: Price(amount=96.25, currency='USD')

4.Notes
Ensure your API key is valid and has sufficient quota.
The intermediate currency for conversions is CHF.
Handle exceptions like CurrencyConversionError for robust error management.
