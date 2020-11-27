import sys
import yaml
import os
import shutil
import pathlib
import glob
import base64
from PIL import Image
# TODO support going through the entire directory
# This is the path to a given .p8 file
# inputLocation = sys.argv[1]

# Config section
studio = 'Caterpillar Games'
itchName = 'caterpillargames'
outputLocation = "/Users/nathandunn/Projects/pico8-games"
pico8Location = '/Applications/PICO-8.app/Contents/MacOS/pico8'

# gameslug = 'test-game'


def resetGameDir(gamedir):
	print('removing existing')
	try:
		shutil.rmtree(gamedir)
	except FileNotFoundError:
		print('did not exist')
	print('remove existing complete')

	print('creating new dir')
	pathlib.Path(gamedir).mkdir()
	print('new dir complete')


def writeP8file(gamedir, gameslug, finalContents):
	finalP8Path = f'{gamedir}/{gameslug}.p8'
	print('writing p8 result')
	with open(finalP8Path, 'w') as outFile:
		outFile.write(finalContents)
	print('finished writing p8 result')
	return finalP8Path

def writeReadme(gamedir):
	with open(f'{gamedir}/README.md', 'w') as outFile:
		outFile.write('test')


def compile(inputPath):
	with open(inputPath, 'r') as inputFile:
		contents = inputFile.read()

	frontMatter, temp = contents.split('--[[')
	yamlContent, backMatter = temp.split('--]]')
	parsed = yaml.safe_load(yamlContent)
	gameslug = parsed['game-slug']
	print(parsed)
	finalContents = contents
	# TODO parse out label image

	gamedir = f'{outputLocation}/carts/{gameslug}'
	resetGameDir(gamedir)

	# TODO detect if file has no label image
	finalP8Path = writeP8file(gamedir, gameslug, finalContents)

	writeReadme(gamedir)

	exportArtifacts(finalP8Path, gameslug)

	exportGameplayPng(finalP8Path)

	# print('deleting existing .p8')
	# destPath = f'{outputLocation}/carts/{gameslug}'
	# for p8 in glob.glob(outputLocation + '/*.p8'):
	# 	os.remove(p8)
	# print('existing .p8 removed')

	# with open

# https://pico-8.fandom.com/wiki/Palette
colmap = {}
for i, row in enumerate('''
0, 0, 0
29, 43, 83
126, 37, 83
0, 135, 81
171, 82, 54
95, 87, 79
194, 195, 199
255, 241, 232
255, 0, 77
255, 163, 0
255, 236, 39
0, 228, 54
41, 173, 255
131, 118, 156
255, 119, 168
255, 204, 170
'''.strip().split('\n')):
	colmap[hex(i)] = eval(f'({row})')



def exportGameplayPng(finalP8Path):
	# print(htmlFilePath)
	# with open(htmlFilePath, 'r') as htmlFile:
	# 	contents = htmlFile.read()

	with open(finalP8Path, 'r') as p8File:
		contents = p8File.read()

	pixels = []

	for row in contents.split('__label__')[1].split():
		if not all(c in '0123456789abcdef' for c in row):
			break
		pixelRow = [colmap[f'0x{c}'] for c in row]
		pixels.append(pixelRow)

	# TODO scale up to 3x
	newimg = Image.new('RGBA', (128, 128))
	newimg.putdata(sum(pixels, start = []))
	newimg.save('mytest.png')
	# hexImage = (contents.split('__label__')[1]
	# 	)

	# base64ImageData = (contents.split('.p8_start_button')[1]
	# 	.split('data:image/png;base64,')[1]
	# 	.split('"')[0]
	# )

	# decoded = base64.b64decode(base64ImageData)

	# gamedir, cartName = os.path.split(finalP8Path)
	# screenshotDir = f'{gamedir}/screenshots'
	# print(f'creating {screenshotDir}')
	# pathlib.Path(screenshotDir).mkdir()

	# # .p8_start_button
	# with open(f'{screenshotDir}/cover.png', 'wb') as screenshotFile:
	# 	screenshotFile.write(decoded)


# Returns the location of the html file
def exportArtifacts(finalP8Path, gameslug):
	gamedir, cartName = os.path.split(finalP8Path)
	cartName += '.png'


	print('Exporting')
	os.system(f'{pico8Location} -export index.html {finalP8Path}')
	os.system(f'{pico8Location} -export {cartName} {finalP8Path}')
	print('Export complete')

	exportLoc = f'{gamedir}/export'
	print('creating export dir')
	pathlib.Path(exportLoc).mkdir()
	htmlLoc = f'{exportLoc}/{gameslug}_html'
	pathlib.Path(htmlLoc).mkdir()
	print('export dir complete')

	print('copying files')
	shutil.move(f'index.html', htmlLoc)
	shutil.move('index.js', htmlLoc)
	shutil.move(cartName, exportLoc)
	print('copying files complete')
	# print (exportLoc)
	# exit()
	# return f'{htmlLoc}/index.html'

		

def upload(inputPath):
	os.command(f'butler')

compile('template.p8')
# exportHtml('./template.p8')
