#!/usr/bin/env python

"""
Generates DXF drawings of rectangular patterns for a japanese lamp
"""

import ezdxf

# Create a new DXF drawing
doc = ezdxf.new()

# Retrieve the modelspace, which is where the drawing entities are added
msp = doc.modelspace()

total_width = 4
total_height = 15.5
offset_y = .75
offset_x = .75
margin = .2

n_rows = 4 # 8
n_cols = 2

rectangle_width = (total_width - (n_cols - 1) * margin) / n_cols
rectangle_height = (total_height - (n_rows - 1) * margin) / n_rows

print(rectangle_width, rectangle_height)

for row in range(n_rows):
    for col in range(n_cols):
        x = offset_x + col * (rectangle_width + margin)
        y = offset_y + row * (rectangle_height + margin)
        print("x, y: ", x, y)
        
        # Add a rectangle to the modelspace
        msp.add_lwpolyline(points=[(x, y), 
                                   (x + rectangle_width, y), 
                                   (x + rectangle_width, y + rectangle_height), 
                                   (x, y + rectangle_height), 
                                   (x, y)], 
                           )

# Save the drawing to a DXF file
dxf_file_path = "/mnt/c/Users/eschl/Downloads/grid_rectangles.dxf"
doc.saveas(dxf_file_path)