import requests
import time
import json
import datetime
import user

# Funkcja stworzona do przechwytywania danych ze strony NBP
# W sytuacji gdy plik istnieje - nie wywoluje requesta- poniewaz to
# strata czasu
#
#
def request_info():
    base_url = 'http://api.nbp.pl/api/exchangerates/tables/a/'
    current_date = time.strftime("%Y-%m-%d")
    filename = 'data.json'

    try:
        url = f'{base_url}today/?format=json'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Data fetched from API for today and saved to '{filename}'.")
        return filename

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for today: {e}")

        for i in range(1, 6):
            past_date = (datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            past_url = f'{base_url}{past_date}/?format=json'

            try:
                response = requests.get(past_url)
                response.raise_for_status()
                data = response.json()

                # Save the data to 'data.json'
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)

                print(f"Data fetched from API for {past_date} and saved to '{filename}'.")
                return filename

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {past_date}: {e}")

        print(f"No data available for the last 5 days.")
        raise FileNotFoundError("No data available for the last 5 days")


def game(user1: user.User):

    def commands():
        print("="*30)
        print("info - shows Player's statistics")
        print("currencies - shows all available currencies")
        print("sell - sell your currencies")
        print("buy - buy new currencies")
        print("Latest days - to see the prices of currenceis from latest 10 days")
        print("quit - quit")

    def show_currencies():
        file_path = user1.file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            for currency in data[0]["rates"]:
                print(f"{currency['code']} : {round(currency['mid'],2)}")

    print("------------------------------------------")
    print("-Welcome to the Money exchange simulator!-")
    print("------------------------------------------\n")
    while True:
        print("="*30)

        print("choose action (all actions: 'commands')")
        action = input("print: ").strip().lower()

        if action == "info":

            print("=" * 30)
            user1.show_info()

        elif action == "currencies":
            print("=" * 30)
            show_currencies()


        elif action == "sell":
            print("=" * 30)
            currency_to_sell = input("Currency name: ").strip().upper()
            while True:
                try:
                    amount = float(input("Amount: "))
                    if amount <= 0:
                        print("Amount must be greater than zero. Please try again.")
                        continue
                    user1.sell_currency(currency_to_sell, amount)
                    break
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
        elif action == "buy":
            print("=" * 30)
            currency_to_buy = input("Currency name: ").strip().upper()
            while True:
                try:
                    amount = float(input("Amount: "))
                    if amount <= 0:
                        print("Amount must be greater than zero. Please try again.")
                        continue
                    user1.buy_currency(currency_to_buy, amount)
                    break
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
        elif action == "quit":
            print("goodbye")
            break
        elif action == "commands":
            commands()

        elif action == "latest days":
            currency_to_buy = input("Currency name: ").strip().upper()
            user1.show_values_from_latest_days(currency_to_buy, 100)




        else:
            print("Invalid command")


