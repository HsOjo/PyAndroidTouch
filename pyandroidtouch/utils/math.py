import math


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def angle(x1, y1, x2, y2):
    if x2 == x1:
        if y2 > y1:
            return math.pi * 0.5
        else:
            return math.pi * 1.5
    elif y2 == y1:
        if x2 > x1:
            return 0
        else:
            return math.pi
    else:
        angle = math.atan((y1 - y2) / (x1 - x2))
        if x2 < x1 and y2 > y1:
            return angle + math.pi
        elif x2 < x1 and y2 < y1:
            return angle + math.pi
        elif x2 > x1 and y2 < y1:
            return angle + 2 * math.pi
        else:
            return angle


def move(x, y, step, angel_=0):
    nx = x + step * math.cos(angel_)
    ny = y + step * math.sin(angel_)
    return nx, ny
