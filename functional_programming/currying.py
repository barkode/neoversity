from typing import Callable, Dict


def add(a, b):
    return a + b


# Applying currying to the add function

def add(a):
    def add_b(b):
        return a + b

    return add_b


add_5 = add(5)
result = add_5(10)
print(result)


# def apply_discount(price: float, discount_percentage: int) -> float:
#     return price * (1 - discount_percentage / 100)


# discounted_price = apply_discount(500, 10)  # discount 10% for a price 500
# print(discounted_price)
#
# discounted_price = apply_discount(500, 20)  # discount 20% for a price 500
# print(discounted_price)


# Applying currying apply_discount function
def discount(discount_percentage: int) -> Callable[[float], float]:
    def apply_discount(price: float) -> float:
        return price * (1 - discount_percentage / 100)

    return apply_discount


# currying in action
ten_percent_discount = discount(10)
twenty_percent_discount = discount(20)

discounted_price = ten_percent_discount(500)
print(discounted_price)

discounted_price = twenty_percent_discount(500)
print(discounted_price)

discount_functions: Dict[str, Callable] = {
    '10%': discount(10),
    '20%': discount(20),
    '30%': discount(30),
    }

price = 500
discount_type = "20%"

discounted_price = discount_functions[discount_type](price)
print(f"Sale price {discounted_price}")