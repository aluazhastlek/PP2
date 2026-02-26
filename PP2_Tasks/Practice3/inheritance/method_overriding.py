# Example 3: Method overriding

class PremiumEmployee(Employee):
    def info(self):
        # Overrides parent method
        base_info = super().info()   # Calls parent version
        return base_info + " with premium benefits."


pe = PremiumEmployee("Madina", "Designer")
print(pe.info())