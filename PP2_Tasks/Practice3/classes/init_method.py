class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # Updates the instance variable balance
        self.balance += amount


account = BankAccount("Malika", 1000)

print(account.balance)
account.deposit(500)      # Modify using method
account.owner = "M. K."   # Modify directly
print(account.balance)
print(account.owner)