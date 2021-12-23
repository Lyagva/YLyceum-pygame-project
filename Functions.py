import numpy as np
from numba import njit
import math as mt


@njit(fastmath=True)
def get_hypotenuse(x1, x2, y1, y2):
    return mt.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


@njit(fastmath=True)
def get_collide_rect(x1, y1, w1, h1, x2, y2, w2, h2):
    return True if len(np.intersect1d(np.array(list(map(lambda x: x, range(x1, x1 + w1 + 1))), dtype='int16'),
                                      np.array(list(map(lambda x: x, range(x2, x2 + w2 + 1))), dtype='int16'))) > 0 and \
                   len(np.intersect1d(np.array(list(map(lambda x: x, range(y1, y1 + h1 + 1))), dtype='int16'),
                                      np.array(list(map(lambda x: x, range(y2, y2 + h2 + 1))), dtype='int16'))) > 0 else False


@njit(fastmath=True)
def linesAreParallel(x1, y1, x2, y2, x3, y3, x4, y4):
    return ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)) == 0


@njit(fastmath=True)
def intersectionPoint(x1, y1, x2, y2, x3, y3, x4, y4):
    # x, y
    return ((((x1 * y2) - (y1 * x2)) * (x3 - x4)) - ((x1 - x2) * ((x3 * y4) - (y3 * x4)))) / (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))), \
           ((((x1 * y2) - (y1 * x2)) * (y3 - y4)) - ((y1 - y2) * ((x3 * y4) - (y3 * x4)))) / (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))


def lineRectIntersectionPoints(line, sprites):
    result = []
    line_x1, line_y1, line_x2, line_y2 = line[0][0], line[0][1], line[1][0], line[1][1]

    for sprite in sprites:
        #  Begin the intersection tests
        result = []
        pos_x, pos_y, width, height = sprite.rect

        #  Convert the rectangle into 4 lines
        rect_lines = [(pos_x, pos_y, pos_x + width, pos_y), (pos_x, pos_y + height, pos_x + width, pos_y + height),
                      # top & bottom
                      (pos_x, pos_y, pos_x, pos_y + height),
                      (pos_x + width, pos_y, pos_x + width, pos_y + height)]  # left & right

        #  intersect each rect-side with the line
        for r in rect_lines:
            rx1, ry1, rx2, ry2 = r
            if not linesAreParallel(line_x1, line_y1, line_x2, line_y2, rx1, ry1, rx2, ry2):  # если не парралельны
                pX, pY = intersectionPoint(line_x1, line_y1, line_x2, line_y2, rx1, ry1, rx2, ry2)
                pX = round(pX)
                pY = round(pY)
                # Lines intersect, but is on the rectangle, and between the line end-points?
                if sprite.rect.collidepoint(pX, pY) and min(line_x1, line_x2) <= pX <= max(line_x1, line_x2) and \
                        min(line_y1, line_y2) <= pY <= max(line_y1, line_y2):
                    result.append((pX, pY))  # keep it
                    if len(result) > 1:
                        break  # Once we've found 2 intersection points, that's it
        if result:
            break
    return result
