class Orders:
    def __init__(self):
        self.items = {}
        self.next_id = 1

    def add_item(self, material, diameter_mm, depth_cm, quantity):
        from objects.order import Order
        item_id = self.next_id
        self.items[item_id] = Order(material, diameter_mm, depth_cm, quantity)
        self.next_id += 1

    def get_items(self):
        return {item_id: vars(order) for item_id, order in self.items.items()}

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]

    def remove_all(self):
        self.items.clear()
        self.next_id = 1

    def get_summary(self):
        total_price = 0
        total_weight = 0
        total_quantity = 0
        total_volume = 0
        for order in self.items.values():
            total_price += order.price
            total_weight += order.weight
            total_quantity += order.quantity
            total_volume += order.volume
        return {
            'total_price': total_price,
            'total_weight': total_weight,
            'total_quantity': total_quantity,
            'total_volume': round(total_volume, 4)
        }

    def update_item_field(self, item_id, field, value):
        if item_id in self.items and hasattr(self.items[item_id], field):
            setattr(self.items[item_id], field, value)
            self.items[item_id].volume = self.items[item_id].calculate_volume()
            self.items[item_id].weight = self.items[item_id].calculate_weight()
            self.items[item_id].price = self.items[item_id].calculate_price()
