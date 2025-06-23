class Order:
    def __init__(self, material, diameter_mm, depth_cm, quantity):
        self.material = material
        self.diameter = diameter_mm
        self.depth = depth_cm
        self.quantity = quantity
        self.volume = self.calculate_volume()
        self.weight = self.calculate_weight()
        self.price = self.calculate_price()

    def calculate_volume(self):
        from calculators.volume_calculator import calculate_volume
        return calculate_volume(self)

    def calculate_weight(self):
        from calculators.weight_calculator import calculate_weight
        return calculate_weight(self)

    def calculate_price(self):
        from calculators.price_calculator import calculate_price
        return calculate_price(self)
