# Adjusting the code to use a dictionary for items instead of a list of tuples.

# Define the items with their cost and calorie value.
items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
    }


# Greedy approach
def greedy_algorithm(items, budget):
    total_calories = 0
    remaining_budget = budget
    chosen_items = []
    items = sorted(items.items(),
                   key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
                   reverse=True)
    for item, details in items:
        if details["cost"] <= remaining_budget:
            chosen_items.append(item)
            total_calories += details["calories"]
            remaining_budget -= details["cost"]

    return total_calories, budget - remaining_budget, chosen_items


# Dynamic Programming approach
def dynamic_programming(items, budget):
    item_names = list(items.keys())

    # Create a DP table where rows represent up to the i-th item and columns represent budget
    dp_table = [[0 for x in range(budget + 1)] for y in range(len(items) + 1)]

    for i in range(1, len(item_names) + 1):
        name = item_names[i - 1]
        cost = items[name]["cost"]
        calories = items[name]["calories"]
        for w in range(budget + 1):
            dp_table[i][w] = dp_table[i - 1][w]
            if cost <= w:
                with_item = dp_table[i - 1][w - cost] + calories
                if with_item > dp_table[i][w]:
                    dp_table[i][w] = with_item

    chosen_items = []
    temp_budget = budget
    for i in range(len(item_names), 0, -1):
        if dp_table[i][temp_budget] != dp_table[i - 1][temp_budget]:
            name = item_names[i - 1]
            chosen_items.append(name)
            temp_budget -= items[name]["cost"]

    return dp_table[len(items)][budget], budget - temp_budget, chosen_items


if __name__ == '__main__':
    # Execute both algorithms
    budget = 100

    greedy_result = greedy_algorithm(items, budget)
    dp_result = dynamic_programming(items, budget)

    print(greedy_result, dp_result)
