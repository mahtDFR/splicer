#!/usr/bin/env python3

""""
Script to automate gcode splicing for SVG patterned-prints
See example: https://www.youtube.com/watch?v=zSgW0KoguXc

Usage:
Place script in a folder
Edit the script so model_input and svg_input to point to your pre-generated gcode files from Cura

Run the following from a terminal/cmd/powershell
$ cd <SCRIPTDIRECTORY>
$ python3 autoreplace.py

(Where <SCRIPTDIRECTORY> is the location of the script)
"""

# Edit model_input and svg_input to point to your gcode files
model_input = "cylinder70x30.gcode"
svg_input = "tumbling-blocks-cartesian.gcode"
output = "spliced.gcode"
#TODO: add argparse for these

# initiate a list to store svg gcode to insert as the first layer
svg_buffer = []

"""
CuraEngine outputs gcode with useful comments to identify different print elements, e.g. layers, walls, skin, etc.
We'll exploit this to find everything between the comments ";LAYER:0" and ";LAYER:1" (aka the first layer,
because software is weird and counts from zero, not one (zero index))


Open the svg gcode file and read through it line by line.
Any lines between ";LAYER:0" and ";LAYER:1" are saved to the list
"""
with open(svg_input, "r") as svg_gcode:
    copy = False

    for line in svg_gcode:
        if line.strip() == ";LAYER:0":
            copy = True
            continue
        elif line.strip() == ";LAYER:1":
            copy = False
            continue
        elif copy:
            svg_buffer.append(line)

# close the file to save some RAM
svg_gcode.close()

"""
Open the model_input file, and also create a new file called "spliced.gcode"
Copy the lines of model input until it sees the comment ";LAYER:0"
After that, dump each line of the svg_buffer list, until it sees ";LAYER:1"
After that, continue dumping the rest of the model_input code

NOTE: this is problematic because the extrusion values and z height is out of whack between files and will
result in erratic printer behaviour, like rapid retractions, z jumps, etc. Gotta fix that.

"""

print("opening model gcode")
with open(model_input, "r") as model_gcode, open(output, "w") as spliced:
    paste = True

    for line in model_gcode:
        if line.strip() == ";LAYER:0":
            paste = False
            spliced.write("\n;LAYER:0\n") # bit hacky here, sorry
            spliced.writelines(svg_buffer)
            continue
        elif line.strip() == ";LAYER:1":
            paste = True
            spliced.write("\n;LAYER:1\n") # sorry again.
        elif paste:
            spliced.write(line) # write out the results to a new file called "spliced.gcode"

# close all the files
model_gcode.close()
spliced.close()

# user message
print("finished.")

#TODO: E values difference bug
# layer height difference bug
# remove svg gcode if it exceeds layer1 area
