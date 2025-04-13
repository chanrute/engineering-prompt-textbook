def calculate_items():
    total_payment = 10000
    pudding_price = 320
    chocolate_price = 210
    change = 450

    for pudding_quantity in range(total_payment // pudding_price):
        for chocolate_quantity in range(total_payment // chocolate_price):
            if (pudding_quantity * pudding_price + chocolate_quantity * chocolate_price + change == total_payment):
                return {"チョコ": chocolate_quantity, "プリン": pudding_quantity}

result = calculate_items()
print(result)