import csv

price_list = []
with open('prices.csv', 'r') as prices:
    reader = csv.reader(prices, delimiter=';')
    for row in reader:
        price_list.append(row)

def get_prices(order):
    m = 1 if order.material == 'кирпич' else 2 if order.material == 'бетон' else 3
    diameter = order.diameter
    for i in range(1, len(price_list)):
        upper = int(price_list[i][0].split("-")[-1])
        if diameter <= upper:
            return int(price_list[i][m])
    return int(price_list[-1][m])

def calculate_price(order):
    price_per_cm = get_prices(order)
    return order.depth * price_per_cm * order.quantity
