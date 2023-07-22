from pathlib import Path
import sys
import glob

pattern = sys.argv[1]
if pattern == "default":
    pattern = "/Users/nathandunn/Projects/pico8-games/carts/*/*.p8"
key = sys.argv[2]
default = sys.argv[3]


def addField(filePath: str, fieldName: str, defaultValue: str):
    with open(filePath) as file:
        contents = file.read()

    if "__meta:cart_info_end__" not in contents:
        print("error: ", filePath)
    newContents = contents.replace(
        "__meta:cart_info_end__", f"{fieldName}: {defaultValue}\n__meta:cart_info_end__"
    )
    # for line in contents.split('\n'):
    #     newContents.append(line)

    with open(filePath, "w") as file:
        file.write(newContents)


for file in glob.glob(pattern):
    addField(file, key, default)
