
#-------------------

import requests
import sqlite3
import csv

class StockPortfolioTracker:
    API_KEY = "Q1AHLO438OKICSU2"
    BASE_URL = "https://www.alphavantage.co/query"
    DB_NAME = "portfolio.db"

    def __init__(self):
        self.create_db()

    def create_db(self):
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT UNIQUE,
                    quantity INTEGER,
                    buy_price REAL
                )
            """)
            conn.commit()

    def add_stock(self, symbol, quantity, buy_price):
        if not symbol.isalpha():
            print("Invalid stock symbol! Please enter a valid stock ticker.")
            return
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO stocks (symbol, quantity, buy_price) VALUES (?, ?, ?)", (symbol, quantity, buy_price))
                conn.commit()
                print(f"Added {quantity} shares of {symbol} at ${buy_price}")
            except sqlite3.IntegrityError:
                print("Stock already exists! Use update_stock instead.")

    def update_stock(self, symbol, quantity, buy_price):
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE stocks SET quantity = ?, buy_price = ? WHERE symbol = ?", (quantity, buy_price, symbol))
            if cursor.rowcount == 0:
                print("Stock not found!")
            else:
                conn.commit()
                print(f"Updated {symbol} to {quantity} shares at ${buy_price}")

    def remove_stock(self, symbol):
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stocks WHERE symbol = ?", (symbol,))
            conn.commit()
            print(f"Removed {symbol} from portfolio.")




    def get_stock_price(self, symbol):
        params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": self.API_KEY}
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        try:
            return float(data["Global Quote"]["05. price"])
        except KeyError:
            print("Invalid Symbol or API Limit Reached!")
            return None

    def track_portfolio(self):
        total_investment = 0
        total_current_value = 0
        
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stocks")
            stocks = cursor.fetchall()
        
        print("\nYour Portfolio:")
        for stock in stocks:
            symbol, quantity, buy_price = stock[1], stock[2], stock[3]
            current_price = self.get_stock_price(symbol)
            if current_price:
                total_invested = quantity * buy_price
                total_current = quantity * current_price
                profit_loss = total_current - total_invested
                total_investment += total_invested
                total_current_value += total_current
                print(f"{symbol}: {quantity} shares | Buy: ${buy_price} | Now: ${current_price} | P/L: ${profit_loss:.2f}")
        
        print(f"\nTotal Investment: ${total_investment:.2f}")
        print(f"Current Portfolio Value: ${total_current_value:.2f}")
        print(f"Overall Profit/Loss: ${total_current_value - total_investment:.2f}")

    def export_to_csv(self):
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stocks")
            stocks = cursor.fetchall()
        
        with open("portfolio.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Symbol", "Quantity", "Buy Price"])
            for stock in stocks:
                writer.writerow([stock[1], stock[2], stock[3]])
        print("Portfolio exported to portfolio.csv")

    def run(self):
        while True:
            print("\nStock Portfolio Tracker")
            print("1. Add Stock")
            print("2. Update Stock")
            print("3. Remove Stock")
            print("4. Track Portfolio")
            print("5. Export to CSV")
            print("6. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                symbol = input("Enter Stock Symbol: ").upper()
                quantity = int(input("Enter Quantity: "))
                buy_price = float(input("Enter Buy Price: "))
                self.add_stock(symbol, quantity, buy_price)
            elif choice == "2":
                symbol = input("Enter Stock Symbol to Update: ").upper()
                quantity = int(input("Enter New Quantity: "))
                buy_price = float(input("Enter New Buy Price: "))
                self.update_stock(symbol, quantity, buy_price)
            elif choice == "3":
                symbol = input("Enter Stock Symbol to Remove: ").upper()
                self.remove_stock(symbol)
            elif choice == "4":
                self.track_portfolio()
            elif choice == "5":
                self.export_to_csv()
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice! Try again.")

if __name__ == "__main__":
    StockPortfolioTracker().run()
