def calculate_volume(order):
    radius_m = (order.diameter / 1000) / 2
    height_m = order.depth / 100
    volume = 3.14159 * (radius_m ** 2) * height_m * order.quantity
    return volume
