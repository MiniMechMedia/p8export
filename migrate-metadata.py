import sys
import os

target = sys.argv[1]
try:
    other = sys.argv[2]
except:
    other = "template.p8"
try:
    target = f"/Users/nathandunn/Projects/pico8-games/raw/{(target)}/{other}"
except:
    pass

if not os.path.exists(target):
    print(f"{target} does not exist. Try")
    os.system(f"ls {target.rsplit('/',1)[0]}")

with open(target) as file:
    contents = file.read()

metadata = contents.split("--[[")[1].split("--]]")[0].strip()
metadata = "cart_type: game\n" + metadata
metadata = metadata.replace("todo: ''", "to_do: []")

name = None
maybeslug = None
for line in metadata.split("\n"):
    if line.startswith("game_name"):
        name = line.split("game_name: ")[1].strip()
    if line.startswith("game_slug"):
        maybeslug = line.split("game_slug: ")[1].strip()

slug = maybeslug or name.lower().replace(" ", "-").replace(".", "").replace(
    "'", ""
).replace("é", "e")

copy = metadata
metadata = ""
trijamNumber = None
trijamTheme = None
startControls = True
for line in copy.split("\n"):
    if line.startswith("trijam_number"):
        trijamNumber = line.split("trijam_number:")[1].strip()
    elif line.startswith("trijam_theme"):
        trijamTheme = line.split("trijam_theme:")[1].strip()
        metadata += f"""jam_info:
  - jam_name: TriJam
    jam_number: {trijamNumber}
    jam_url: null
    jam_theme: {trijamTheme}\n"""
    elif line.startswith("controls:"):
        startControls = True
        metadata += "controls:\n"
    elif startControls:
        if line.startswith("  *"):
            rawdesc = line.split("  *")[1]
            # print(f'{rawdesc=}')
            inputs, desc = rawdesc.split("-", 1)
            inputsText = ""
            for inp in inputs.split("/"):
                inputsText += inp.strip().replace(" ", "_").upper() + ","
            metadata += f"  - inputs: [{inputsText[:-1]}]\n"
            metadata += f"    desc: {desc}\n"
        else:
            metadata += line + "\n"
            startControls = False
    else:
        metadata += line + "\n"

newfile = f"/Users/nathandunn/Projects/pico8-games/carts/{slug}/{slug}.p8"

with open(newfile) as file:
    newfilecontents = file.read()
    newfilecontents = newfilecontents.split("__meta:cart_info_start__")[0]

newfilecontents += f"""
__meta:cart_info_start__
{metadata}
__meta:cart_info_end__
"""

with open(newfile, "w") as file:
    file.write(newfilecontents)

with open(
    "/Users/nathandunn/Projects/p8export3/p8export-fresh/tmp/info.txt", "w"
) as file:
    file.write(newfile + "\n")

print("Migrated ", newfile)

# os.system()
