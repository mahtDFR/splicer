model_input = "cylinder70x30.gcode"
svg_input = "tumbling-blocks-cartesian.gcode"
output = "spliced.gcode"

svg_buffer = []

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

svg_gcode.close()

print("opening model gcode")
with open(model_input, "r") as model_gcode, open(output, "w") as spliced:
    paste = True

    for line in model_gcode:
        if line.strip() == ";LAYER:0":
            paste = False
            spliced.write("\n;LAYER:0\n")
            spliced.writelines(svg_buffer)
            continue
        elif line.strip() == ";LAYER:1":
            paste = True
            spliced.write("\n;LAYER:1\n")
        elif paste:
            spliced.write(line)

model_gcode.close()
spliced.close()
print("finished.")
