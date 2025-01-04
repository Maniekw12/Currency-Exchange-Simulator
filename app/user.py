import json
import datetime
import os.path
import requests
import matplotlib.pyplot as plt

class User:
    #Zmienna klasy przechowująca nazwę pliku JSON
    JSON_FILE = 'user_data.json'

    TRANSACTION_FILE = f"transaction_data.json"

    def __init__(self, balance, values=None, stocks=None, file=''):

        #rozwiazanie jednego zoltego problemu przez kompilator
        if values is None:
            values = {}

        if stocks is None:
            stocks = {}

        self.balance = balance
        self.values = values
        self.stocks = stocks
        self.starting_balance = 0
        self.file = file
    def to_json(self):
        return {
            "balance": self.balance,
            "values": self.values,
            "stocks": self.stocks,
            "starting balance": self.starting_balance
        }

    @staticmethod
    def create_user(file):
        while True:
            try:
                balance = float(input("What is your starting balance: "))
                break  # Exit the loop if input is valid
            except ValueError:
                print("That's not a valid number. Please enter a float value.")

        data = {
            "balance": balance,
            "values": {},
            "stocks": {}
        }

        user = User(balance, data["values"], data["stocks"], file)
        user.starting_balance = balance
        user.save_to_json()
        return user


    @staticmethod
    def create_api_user(file, money: int):
        user = User(money, {}, {}, file)
        user.starting_balance = money
        user.save_to_json()
        return user

    @staticmethod
    def load_user(file):
        try:
            with open(User.JSON_FILE, 'r') as json_file:
                json_data = json.load(json_file)
                loaded_user = User.from_json(json_data)
                loaded_user.file = file
                return loaded_user
        except FileNotFoundError:
            print("file does not exist.")
            return None
        except json.JSONDecodeError:
            print("Json file decoding error.")
            return None



    @staticmethod
    def starting_program(file):
        start = ""
        while start != "new" and start != "load":
            print("If you want to create a new profile, type 'New'.")
            print("If you want to load existing data, type 'Load'.")
            start = input("").lower()

        if start == "new":
            return User.create_user(file)

        elif start == "load":
            return User.load_user(file)

        else:
            print("Invalid command.")
            return None

    def save_to_json(self):
        user_json = json.dumps(self.to_json(), indent=4)
        with open(User.JSON_FILE, 'w') as json_file:
            json_file.write(user_json)


    def show_info(self):
        print(f"Balance: {self.balance}")
        print("Bought currencies:")
        for key, value in self.values.items():
            print(f"{key} : {value}")

        print("Bought stocks:")
        for key, value in self.stocks.items():
            print(f"{key} : {value}")


        print(f"Starting balance: {self.starting_balance}")
        return {
            "balance": self.balance,
            "currencies": self.values,
            "starting balance": self.starting_balance
        }


    def buy_currency(self, currency_code: str, amount: float):
        if not self.validate_amount(amount):
            return

        try:
            with open(self.file, 'r') as json_file:
                data = json.load(json_file)

                if isinstance(data, list):
                    data = data[0]

                for rate in data["rates"]:
                    if rate["code"] == currency_code:
                        cost_per_unit = round(rate["mid"], 2)
                        cost = round((cost_per_unit * float(amount)),2)

                        if cost <= self.balance:
                            self.balance = round((self.balance - cost),2)
                            print(f"You bought {amount} {currency_code.upper()}")
                            print(f"Your balance: {self.balance}")
                        else:
                            print("I'm sorry, you don't have enough money")
                            return

                        if currency_code.upper() in self.values:
                            self.values[currency_code.upper()] = float(self.values[currency_code.upper()]) + float(amount)
                        else:
                            self.values[currency_code.upper()] = float(amount)

                        self.save_to_json()
                        return
                print(f"I'm sorry, I didn't find {currency_code.upper()}")
        except FileNotFoundError:
            print(f"File {self.file} not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON file.")

    def sell_currency(self,currency_code: str, amount:float):
        if not self.validate_amount(amount):
            return

        try:
            with open(self.file, 'r') as json_file:
                data = json.load(json_file)

                if isinstance(data,list):
                    data = data[0]

                for rate in data["rates"]:
                    if rate["code"] == currency_code:
                        value_per_unit = round(rate["mid"], 2)
                        value = round((value_per_unit * float(amount)), 2)

                        if currency_code.upper() in self.values and float(self.values[currency_code.upper()]) >= amount:
                            self.values[currency_code.upper()] = float(self.values[currency_code.upper()]) - float(amount)
                            self.balance = round((self.balance + value), 2)
                            print(f"You sold {amount} {currency_code.upper()}")
                            print(f"Your balance: {self.balance}")

                            if self.values[currency_code.upper()] == 0:
                                del self.values[currency_code.upper()]
                            self.save_to_json()
                            return
                        else:
                            print("I'm sorry, you don't have enough currency to sell")
                            return

        except FileNotFoundError:
            print(f"File {self.file} not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON file.")

    def buy_stock(self, stock_code: str, amount: float):
        if not self.validate_amount(amount):
            return

        stock_code = stock_code.upper()
        usd_price = self.get_actual_price("USD")
        stock = Stock(stock_code)
        print(stock.price)
        if not isinstance(stock.price,float):
            print("I'm sorry couldn't load data")
            return None
        if not isinstance(usd_price,float):
            print("I'm sorry couldn't load data")
            return None


        cost = round((stock.price * float(amount) * float(usd_price)), 2)

        if self.balance < cost:
            print("you do not have enough money!")
            return None
        else:
            self.balance = self.balance - cost

            if stock_code in self.stocks:
                self.stocks[stock_code] += float(amount)
            else:
                print("dupa")
                self.stocks[stock_code] = amount

            print(f"updated stocks {self.stocks}")
            self.save_to_json()
            print(f"Successfully bought {amount} of {stock_code} stock.")

    def sell_stock(self, stock_code: str, amount: float):
        if not self.validate_amount(amount):
            return

        stock_code = stock_code.upper()
        if stock_code not in self.stocks.keys():
            print("Stock wasn't found :(")
            return

        usd_price = self.get_actual_price("USD")
        stock = Stock(stock_code)

        if not isinstance(stock.price, float):
            print("I'm sorry, couldn't load data")
            return None

        cost = round((stock.price * float(amount) * usd_price), 2)

        if self.stocks[stock_code] < amount:
            print("Cannot sell")
            return
        else:
            self.stocks[stock_code] -= amount
            self.balance += cost
            if self.stocks[stock_code] == 0:
                del self.stocks[stock_code]

        self.save_to_json()
        print(f"Successfully sold {amount} of {stock_code} stock.")

    def get_actual_price(self, currency_code):
        # Validate input
        if not isinstance(currency_code, str) or len(currency_code) != 3:
            print("Invalid currency code. It should be a 3-letter string.")
            return None

        try:
            with open(self.file, 'r') as json_file:
                data = json.load(json_file)

                if isinstance(data, list):
                    data = data[0]

                # Find the currency code in the data
                for rate in data.get("rates", []):
                    if rate.get("code") == currency_code:
                        cost_per_unit = round(rate.get("mid", 0), 2)
                        return cost_per_unit

                print(f"Currency code {currency_code.upper()} not found in data.")
                return None

        except FileNotFoundError:
            print(f"File {self.file} not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return None

    def validate_amount(self, amount: float):
        if amount < 0:
            print("You cannot handle a negative amount of currencies.")
            return False
        if round(amount, 2) != amount:
            print("Amount has more than two decimal places.")
            return False
        return True

    @staticmethod
    def read_transaction_history(currency_name):

        if os.path.exists(User.TRANSACTION_FILE):
            try:
                with open(User.TRANSACTION_FILE,"r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Eroror decoding transaction hisotry JSON file")
                return {}
        else:
            return {}

    @staticmethod
    def save_to_transaction_history(currency_name,n=50):
        transaction_history = User.read_transaction_history(currency_name)
        for i in range(n):
            past_date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            if past_date not in transaction_history:
                json_data = User.fetch_exchange_rate_for_date(past_date)
                if json_data:
                    transaction_history[past_date] = json_data

        with open(User.TRANSACTION_FILE, 'w') as file:
            json.dump(transaction_history, file, indent=4)

    def load_from_transactions_history(self):
        pass

    @staticmethod
    def from_json(json_data):
        user = User(balance = json_data["balance"], values = json_data["values"],stocks = json_data["stocks"])
        #user.stocks = json_data["stocks"]
        user.starting_balance = json_data["starting balance"]
        return user

    @staticmethod
    def fetch_exchange_rate_for_date(date_str):
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if date.weekday() >= 5:
                print(f"Date {date_str}: It's weekend. Data unavailable")
                return None
        except ValueError as e:
            print(f"Invalid date format: {e}")
            return None

        base_url = 'http://api.nbp.pl/api/exchangerates/tables/a/'
        url = f'{base_url}{date_str}/?format=json'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {date_str}: {e}")
            return None


    @staticmethod
    def show_values_from_latest_days(currency_code, n=50):
        exchange_rates = {}
        User.save_to_transaction_history(currency_code, n)
        transaction_history = User.read_transaction_history(currency_code)

        for i in range(n):
            past_date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            json_data = transaction_history.get(past_date)

            if not json_data:
                json_data = User.fetch_exchange_rate_for_date(past_date)
                if json_data:
                    transaction_history[past_date] = json_data

            if json_data:
                values = json_data[0].get("rates", [])
                for value in values:
                    if value.get("code") == currency_code:
                        exchange_rates[past_date] = round(value["mid"], 2)
                        break

        with open(User.TRANSACTION_FILE, 'w') as file:
            json.dump(transaction_history, file, indent=4)

        if exchange_rates:
            sorted_dates = sorted(exchange_rates.keys())
            sorted_values = [exchange_rates[date] for date in sorted_dates]

            # Plotting
            plt.figure(figsize=(10, 5))
            plt.plot(sorted_dates, sorted_values, marker='o')
            plt.xticks(rotation=45)
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.title(f'Value: {currency_code}')
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print(f"No values found for the given currency code in the last {n} days.")


class Stock:
    INTERVAL = '5min'
    API_KEY = 'demo'
    BASE_URL = 'https://www.alphavantage.co/query'

    def __init__(self, symbol):
        self.stock_code = symbol
        self.price = self.__get_latest_stock()
        self.purchase_date = None

    def get_purchase_info(self):
        return {
            'purchase_date': self.purchase_date,
            'purchase_price': self.price
        }

    def __get_stock_data(self):
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': self.stock_code,
            'interval': Stock.INTERVAL,
            'apikey': Stock.API_KEY
        }
        try:
            response = requests.get(Stock.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching stock data: {e}")
            return None

    def __get_latest_stock(self):
        stock_data = self.__get_stock_data()
        print(stock_data)
        if not stock_data or "Time Series (5min)" not in stock_data:
            return None



        time_series = stock_data["Time Series (5min)"]
        latest_time = max(time_series.keys())
        latest_close = time_series[latest_time]["4. close"]
        self.purchase_date = latest_time
        return round(float(latest_close),2)

    def last(self):
        return self.__get_latest_stock()




