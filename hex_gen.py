#!/usr/bin/env python

"""
Generates DXF drawings of hex patterns for a japanese lamp
"""
import ezdxf
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fill_ratio = .92

MAKE_DXF = True

def hexagon(center, size):
    """Generate the vertices for a regular hexagon given a center (x, y), and a size."""
    angle = math.pi / 3  # 60 degrees
    return [(center[0] + fill_ratio * size * math.cos(i * angle),
             center[1] + fill_ratio * size * math.sin(i * angle)) for i in range(7)]


def draw_corrected_hexagonal_pattern(width, height, hex_size):
    """Fill a rectangle of dimensions width x height with a pattern of hexagons of given size."""
    _, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim([0, width + hex_size])
    ax.set_ylim([0, height + hex_size])

    dx = hex_size * 3
    dy = math.sqrt(3) * hex_size # Vertical spacing remains the same
    nx = int(width / dx)
    ny = int(2 * height / dy)
    print(ny)

    INIT_OFFSET = .75 + hex_size * .7

    for i in range(ny):
        y_offset = 0 if i % 2 == 0 else 1.5 * hex_size
        actual_nx = nx if i % 2 == 0 else nx -1
        for j in range(actual_nx):
            center = (INIT_OFFSET + j * dx + y_offset, INIT_OFFSET + i * dy * 0.5)
            hex_pts = hexagon(center, hex_size)
            hex_patch = patches.Polygon(hex_pts, closed=True, edgecolor='black', facecolor='none')
            ax.add_patch(hex_patch)

            if MAKE_DXF:
                msp.add_lwpolyline(points=hex_pts)

    plt.gca().invert_yaxis()  # Invert y-axis to match the typical Cartesian coordinate system
    plt.axis('off')  # Turn off the axis
    plt.tight_layout()
    plt.show()

if MAKE_DXF:
    doc = ezdxf.new()
    msp = doc.modelspace()

# Execute the function to draw the corrected hexagonal pattern
draw_corrected_hexagonal_pattern(5.5, 15.5, .53)

if MAKE_DXF:
    dxf_file_path = "/mnt/c/Users/eschl/Downloads/hex.dxf"
    doc.saveas(dxf_file_path)