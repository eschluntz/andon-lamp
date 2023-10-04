#!/usr/bin/env python

"""
Generates DXF drawings of hilbert patterns for a japanese lamp
"""
import ezdxf
import matplotlib.pyplot as plt

MAKE_DXF = True


def xy2d(n, x, y):
    d = 0
    s = n // 2
    while s > 0:
        rx = int((x & s) > 0)
        ry = int((y & s) > 0)
        d += s * s * ((3 * rx) ^ ry)
        x, y = rot(s, x, y, rx, ry)
        s //= 2
    return d

def d2xy(n, d):
    x = y = 0
    t = d
    s = 1
    while s < n:
        rx = int(1 & (t // 2))
        ry = int(1 & (t ^ rx))
        x, y = rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y

def rot(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        x, y = y, x
    return x, y

def plot_transformed_solid_hilbert_curve(n, start_x, start_y, width, height, y_stacks):

    # there are 16 "blocks" in the pattern, so "height" should be 16x the spacing
    height += height / y_stacks / 17.0
    height = height * 16.0/17.0 / y_stacks

    for stack in range(y_stacks):
        xs = []
        ys = []
        for d in range(n*n):
            x, y = d2xy(n, d)
            # Scaling and translating the coordinates
            x = x * width / (n - 1) + start_x
            y = y * height / n + start_y + height / n + 17.0/16.0 * height * stack# last piece is for the final line that gets added
            if d == 0:
                first_y = y
            xs.append(x)
            ys.append(y)
        
        # Add extra lines to make it solid by going downwards
        xs.append(xs[-1])
        ys.append(ys[-1] - height/n)
        xs.append(start_x)
        ys.append(ys[-1])
        xs.append(start_x)
        ys.append(first_y)
        
        plt.fill(xs, ys, color="skyblue", edgecolor="black")

        if MAKE_DXF:
            msp.add_lwpolyline(points=list(zip(xs,ys)))

    plt.axis('equal')
    plt.show()

if MAKE_DXF:
    doc = ezdxf.new()
    msp = doc.modelspace()

# Plotting the transformed solid Hilbert curve starting at (50, 50) with width and height of 300
plot_transformed_solid_hilbert_curve(16, .5, .5, 4.5, 16, 3)

if MAKE_DXF:
    dxf_file_path = "/mnt/c/Users/eschl/Downloads/hilbert3.dxf"
    doc.saveas(dxf_file_path)