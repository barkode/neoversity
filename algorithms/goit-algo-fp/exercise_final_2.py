import matplotlib.pyplot as plt
import numpy as np


def draw_branch():
    if depth == 0:
        return

    # Реалізація логіки візуалізації фракталу
    pass


# Налаштування вікна для малювання
plt.figure(figsize=(8, 8))
plt.axis('off')


depth = 8  #TODO додати можливість задати параметр глибини користувачу

draw_branch(depth)

plt.show()
