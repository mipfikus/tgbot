from objects.orders import Orders

class OrderHandler:
    def __init__(self):
        self.orders = Orders()

    def handle_orders(self, material, diameter_mm, depth_cm, quantity):
        self.orders.add_item(material, diameter_mm, depth_cm, quantity)
        return self.orders.get_items()
