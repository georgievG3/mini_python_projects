import psycopg2


class MonthlyExpenses:

    def __init__(self, db_config: dict):
        # Connect to PostgreSQL
        try:
            self.conn = psycopg2.connect(**db_config)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as e:
            print(f"Error connecting to database: {e}")
            exit()

    def create_tables(self):
        # Create tables for balance and transactions if they don't exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS balance (
            id SERIAL PRIMARY KEY,
            amount FLOAT NOT NULL
        );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            type VARCHAR(10) NOT NULL,
            value FLOAT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        # Initialize balance if not set
        self.cursor.execute("SELECT * FROM balance;")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO balance (amount) VALUES (0);")
            self.conn.commit()

    def get_balance(self):
        self.cursor.execute("SELECT amount FROM balance;")
        return self.cursor.fetchone()[0]

    def update_balance(self, new_balance):
        self.cursor.execute("UPDATE balance SET amount = %s;", (new_balance,))
        self.conn.commit()

    def print_balance(self):
        balance = self.get_balance()
        return f"Your balance is: {balance}!"

    def print_transactions(self):
        self.cursor.execute("SELECT type, value, date FROM transactions;")
        transactions = self.cursor.fetchall()
        return transactions

    def add_expense(self, value: float):
        balance = self.get_balance()
        new_balance = balance - value
        self.update_balance(new_balance)

        self.cursor.execute("INSERT INTO transactions (type, value) VALUES (%s, %s);", ("Outcome", value))
        self.conn.commit()

        print("Expense added successfully!")

    def add_income(self, value: float):
        balance = self.get_balance()
        new_balance = balance + value
        self.update_balance(new_balance)

        self.cursor.execute("INSERT INTO transactions (type, value) VALUES (%s, %s);", ("Income", value))
        self.conn.commit()

        print("Income added successfully!")

    def run(self):
        while True:
            command = input(f"Choose option: '1 - check balance'; '2 - add expense'; '3 - add income'; '4 - transaction history'; '5 - EXIT'\n")

            if command == "5":
                print("Goodbye!")
                break

            elif command == "1":
                print(self.print_balance())
                continue

            elif command == "2":
                try:
                    expense_value = float(input("How much is the expense? - "))
                    self.add_expense(expense_value)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                continue

            elif command == "3":
                try:
                    income_value = float(input("How much is the income? - "))
                    self.add_income(income_value)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                continue

            elif command == "4":
                transactions = self.print_transactions()
                for t in transactions:
                    print(f"Type: {t[0]}, Value: {t[1]}, Date: {t[2]}")
                continue

# Database configuration
db_config = {
    "dbname": "monthly_expenses",
    "user": "postgres",
    "password": "1237654",
    "host": "localhost",
    "port": 5432
}

program = MonthlyExpenses(db_config)
program.run()
