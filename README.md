# 📄 Money Exchange Simulator Documentation

This documentation provides a brief overview of the **Money Exchange Simulator** program. The simulator allows users to manage virtual funds by buying and selling currencies based on real-time or historical exchange rates.

---

## 📚 Overview

The **Money Exchange Simulator** allows users to:
- Start with an initial balance.
- Buy and sell currencies.
- View historical exchange rates.
- Save and load user profiles from JSON files.

---

## 📂 File Structure

- **`user.py`**  
  Contains the `User` class, which handles user profiles, balance, and currency transactions.

- **`functions.py`**  
  Contains utility functions for interacting with APIs and managing the game loop.

- **`game_in_terminal.py`**  
  The main entry point for running the simulation.

- **`user_data.json`**  
  Stores user profile data.

- **`transaction_data.json`**  
  Stores historical transaction data.

- **`data.json`**  
  Contains the latest exchange rate data from the NBP API.

---

## 🧩 Main Components

### 📦 `user.py`
Defines the **`User`** class and handles core functionalities such as balance management, currency transactions, and API interactions.

#### 📜 Key Methods:
- **`create_user(file)`**  
  Prompts the user to set an initial balance and creates a new profile.

- **`load_user(file)`**  
  Loads an existing user profile from a JSON file.

- **`buy_currency(currency_code, amount)`**  
  Buys a specified amount of a currency using the current exchange rate.

- **`sell_currency(currency_code, amount)`**  
  Sells a specified amount of a currency and updates the balance.

- **`show_values_from_latest_days(currency_code, n)`**  
  Displays and plots exchange rates for the last `n` days using `matplotlib`.

---

### 📦 `functions.py`
Utility functions for interacting with APIs and managing the main game loop.

#### 📜 Key Functions:
- **`request_info()`**  
  Fetches and saves the latest exchange rate data from the **NBP API**.

- **`game(user1)`**  
  Runs the main simulation loop, allowing the user to buy and sell currencies.

---

## 🎮 How to Play

1. **Run the Program**  
   Start the simulation by running the `game_in_terminal.py` file.

2. **Choose an Action**  
   Follow the on-screen prompts to perform actions like:
   - `info` to view your account details.
   - `buy` to purchase currencies.
   - `sell` to sell currencies.
   - `latest days` to view historical exchange rates.

3. **Exit the Game**  
   Use the `quit` command to exit the game.

---

## 📋 Available Commands in the Game

| Command         | Description                     |
|-----------------|---------------------------------|
| `info`          | Shows the user's balance and transactions. |
| `currencies`    | Displays all available currencies with their exchange rates. |
| `buy`           | Allows the user to buy currencies. |
| `sell`          | Allows the user to sell currencies. |
| `latest days`   | Shows exchange rates for the past 10 days. |
| `commands`      | Lists all available commands. |
| `quit`          | Exits the game. |

---

## 🛠️ Dependencies

The program requires the following Python libraries:
- `json`
- `datetime`
- `os`
- `requests`
- `matplotlib`

---

## 📦 API Integrations

The simulator integrates with the **NBP API** to fetch the latest exchange rates.

---

## 🧪 Example Usage

1. **Run the Program:**
   ```bash
   python game_in_terminal.py
