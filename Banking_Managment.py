from abc import ABC, abstractmethod
from datetime import datetime


class Transaction:
    transactions = []

    def __init__(self, account_no, transaction_type, amount) -> None:
        self.account_no = account_no
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = datetime.now()
        Transaction.transactions.append(self)

    def show_info(self):
        print(f"Transaction Type: {self.transaction_type}")
        print(f"Amount: ${self.amount}")
        print(f"Timestamp: {self.timestamp}")


class Account(ABC):
    accounts = []
    account_number_counter = 1

    def __init__(self, name, email, address, account_type) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_no = Account.account_number_counter
        self.transactions = []
        Account.account_number_counter += 1
        Account.accounts.append(self)

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            print(f"\n--> Deposited ${amount}. Now Balance: ${self.balance}")
            self.transactions.append(Transaction(self.account_no, "Deposit", amount))
        else:
            print("\n--> Invalid Deposit amount")

    def withdraw(self, amount):
        if 0 <= amount <= self.balance:
            self.balance -= amount
            print(f"\n--> withdraw ${amount}. Now Balance: ${self.balance}")
            self.transactions.append(Transaction(self.account_no, "Withdrawal", amount))

        else:
            print("\n--> Withdraw amount exceeded or invalid")

    def check_balance(self):
        print(f"\n--> Available Balance: ${self.balance}")

    def show_transaction_history(self):
        print("\n=== Transaction History ===")
        for transaction in self.transactions:
            transaction.show_info()
            print("\n---")

    @abstractmethod
    def show_info(self):
        pass


class SavingsAccount(Account):
    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address, "Savings")
        self.interest_rate = 3

    def show_info(self):
        print(f"Account Type: {self.account_type}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Number: {self.account_no}")
        print(f"Balance: ${self.balance}")
        print(f"Interest Rate: {self.interest_rate}%")

    def apply_interest(self):
        interest = self.balance * (self.interest_rate / 100)
        self.deposit(interest)
        print("\n--> Interest Applied")


class CurrentAccount(Account):
    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address, "Current")
        self.overdraft_limit = 500

    def show_info(self):
        print(f"Account Type: {self.account_type}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Number: {self.account_no}")
        print(f"Balance: ${self.balance}")
        print(f"Overdraft Limit: {self.overdraft_limit}")

    def withdraw(self, amount):
        if 0 <= amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            print(f"\n--> Withdraw ${amount}. Now Balance: ${self.balance}")
            self.transactions.append(Transaction(self.account_no, "Withdrawal", amount))
        else:
            print("\n--> Withdrawal Amount exeeded or Invalid")


class LoanAccount(Account):
    load_feature_enabled = False

    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address, "Loan")

    def apply_for_loan(self, amount):
        if LoanAccount.load_feature_enabled:
            self.deposit(amount)
            print("\n--> Loan applied successfully!")

        else:
            print("\n--> Loan feature is currenly disabled")

    def get_load_amount(self):
        return sum(
            transaction.amount
            for transaction in self.transactions
            if transaction.transaction_type == "Deposit"
        )


class Admin:
    def create_account(self):
        print("\n=== Create User Account ===")
        name = input("Name: ")
        email = input("Email: ")
        address = input("Address: ")
        account_type = input("Account Type (Savings/Current/Loan)").capitalize()

        if account_type == "Savings":
            account = SavingsAccount(name, email, address)
        elif account_type == "Current":
            account = CurrentAccount(name, email, address)
        elif account_type == "Loan":
            account = LoanAccount(name, email, address)
        else:
            print("\n--> Invalid account type. Account not created.")
            return
        print("\n--> account created successfully.")
        return account

    def delete_account(self):
        print("\n=== Delete User Account ===")
        try:
            account_number = int(input("Enter the account number to delete: "))
            account = self.find_account(account_number)
            if account:
                Account.accounts.remove(account)
                print("\n-->Account Deleted successfully.")
            else:
                print("\n--> Account not found.")
        except ValueError:
            print("\n--> Please enter a valid account number. ")

    def view_all_accounts(self):
        print("\n=== All User Accounts ===")
        for account in Account.accounts:
            account.show_info()
            print("\n---")

    def check_total_balance(self):
        total_balance = sum(account.balance for account in Account.accounts)
        print(f"\n--> Total Available Banalace: ${total_balance}")

    def check_total_loan_amount(self):
        total_load_amount = sum(
            account.get_loan_amount()
            for account in Account.accounts
            if isinstance(account, LoanAccount)
        )
        print(f"\n--> Total Loan Amount ${total_load_amount}")

    def toggle_loan_feature(self, enable):
        LoanAccount.load_feature_enabled = enable
        status = "enable" if enable else "disabled"
        print(f"\n--> Loan feature is now {status}")

    def find_account(self, account_number):
        for account in Account.accounts:
            if account.account_no == account_number:
                return account
        return None


admin = Admin()
user_account = None
while True:
    print("\n=== Banking Management system ===")
    print("\n1. User Operations")
    print("2. Admin Operations")
    print("3. Exit")

    try:
        choice = int(input("Enter Your Choice (1/2/3): "))
    except ValueError:
        print("\n--> Please Enter a Valid Number.")
        continue

    if choice == 1:
        print("\n=== User Operations ===")
        print("\n1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Take Loan")
        print("7. Transfer Amount")
        print("8. Exit")

        try:
            user_choice = int(input("Enter Your Choice (1-8): "))
        except ValueError:
            print("\n-->Please enter a valid number.")
            continue

        if user_choice == 1:
            user_account = admin.create_account()
        elif user_choice == 2:
            if user_account:
                try:
                    amount = float(input("Enter The Deposit Amount: "))
                    user_account.deposit(amount)
                except ValueError:
                    print("\n--> Please enter a valid amount.")
            else:
                print("\n--> Create an account first.")

        elif user_choice == 3:
            if user_account:
                try:
                    amount = float(input("Enter The withdrawal amount: "))
                    user_account.withdraw(amount)
                except ValueError:
                    print("\n--> Please enter a valid amount.")
            else:
                print("\n--> Create an account first.")
        elif user_choice == 4:
            if user_account:
                user_account.check_balance()
            else:
                print("\n--> Create an account first.")
        elif user_choice == 5:
            if user_account:
                user_account.show_transaction_history()
            else:
                print("\n--> Create an account first.")
        elif user_choice == 6:
            if isinstance(user_account, LoanAccount):
                try:
                    amount = float(input("Enter The withdrawal amount: "))
                    user_account.apply_for_loan(amount)
                except ValueError:
                    print("\n--> Please enter a valid amount.")
            else:
                print("\n--> Only Loan accounts can apply for loans")

        elif user_choice == 7:
            if isinstance(user_account, (SavingsAccount, CurrentAccount)):
                try:
                    target_account_number = int(
                        input("Enter the account number to transfer to: ")
                    )
                    target_account = admin.find_account(target_account_number)
                    if target_account:
                        try:
                            transfer_amount = float(
                                input("Enter the transfer amount: ")
                            )
                            if (
                                isinstance(user_account, SavingsAccount)
                                and transfer_amount > user_account.balance
                            ):
                                print("\n--> Insuddicient balance for transfer.")

                            else:
                                user_account.withdraw(transfer_amount)
                                target_account.deposit(transfer_amount)
                                print("\n-->Transfer Successfully.")
                        except ValueError:
                            print("\n--> Please enter a valid amount.")
                    else:
                        print("\n-->Target account not found.")
                except ValueError:
                    print("\n--> Please enter a valid amount number.")

        elif user_choice == 8:
            print("\nExiting User Operations.")

    elif choice == 2:
        print("\n=== Admin Operations ===")
        print("\n1. Create Account")
        print("2. Delete Account")
        print("3. View All Account")
        print("4. Check Total Balance")
        print("5. Check Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. Exit")
        try:
            admin_choice = int(input("Enter Your Choice (1-7): "))
        except ValueError:
            print("\n--> Please enter a valid number.")
            continue
        if admin_choice == 1:
            admin.create_account()
        elif admin_choice == 2:
            admin.delete_account()
        if admin_choice == 3:
            admin.view_all_accounts()
        if admin_choice == 4:
            admin.check_total_balance()
        if admin_choice == 5:
            admin.check_total_loan_amount()
        if admin_choice == 6:
            try:
                enable_loan_deature = input(
                    "Do you want to enable the load feature? (yes/no)"
                ).lower()
                admin.toggle_loan_feature(enable_loan_deature == "yes")
            except ValueError:
                print("\n--> Please enter a valid choice.")
                continue
        elif admin_choice == 7:
            print("\nExiting Admin Operations.")

    elif choice == 3:
        print("\nExiting the Banking Managment System.")
        break

    else:
        print("\nInvalid choice. Please Enter 1,2 or 3. ")
