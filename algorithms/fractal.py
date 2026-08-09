import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_triangle(vertices, ax):
    triangle = patches.Polygon(vertices, fill=False, edgecolor='black')
    ax.add_patch(triangle)

def midpoint(point1, point2):
    return [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]

def sierpinski(vertices, level, ax):
    draw_triangle(vertices, ax)
    if level > 0:
        sierpinski([vertices[0], midpoint(vertices[0], vertices[1]), midpoint(vertices[0], vertices[2])], level-1, ax)
        sierpinski([vertices[1], midpoint(vertices[0], vertices[1]), midpoint(vertices[1], vertices[2])], level-1, ax)
        sierpinski([vertices[2], midpoint(vertices[2], vertices[1]), midpoint(vertices[0], vertices[2])], level-1, ax)

def main():
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_axis_off()
    vertices = [[0, 0], [0.5, 0.75], [1, 0]]
    sierpinski(vertices, 3, ax)
    plt.show()

main()

import turtle

def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)

def draw_koch_curve(order, size=300):
    window = turtle.Screen()
    window.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-size / 2, 0)
    t.pendown()

    koch_curve(t, order, size)

    window.mainloop()

# Виклик функції
draw_koch_curve(3)
