class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def make_coffee(self):
        print(f"Making a {self.name}...")
        
    def serve_coffee(self):
        print(f"Serving {self.name} which costs ${self.price:.2f}")

class Espresso(Coffee):
    def __init__(self, price):
        super().__init__("Espresso", price)
    
    def add_water(self):
        print("Adding a small amount of water...")


class Latte(Coffee):
    def __init__(self, price):
        super().__init__("Latte", price)
    
    def add_milk(self):
        print("Adding steamed milk...")

class Cappuccino(Coffee):
    def __init__(self, price):
        super().__init__("Cappuccino", price)
    
    def add_milk_and_foam(self):
        print("Adding steamed milk and milk foam...")
