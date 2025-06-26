def calculate_weight(order):
    density = 1700 if order.material == 'кирпич' else 2400 if order.material == 'бетон' else 2500
    weight = order.volume * density
    return round(weight, 2)
