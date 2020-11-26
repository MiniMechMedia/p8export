import sys
import yaml
import os
import shutil
import pathlib
# TODO support going through the entire directory
# This is the path to a given .p8 file
# inputLocation = sys.argv[1]

# Config section
studio = 'Caterpillar Games'
itchName = 'caterpillargames'
outputLocation = "/Users/nathandunn/Projects/pico8-games"
pico8Location = '/Applications/PICO-8.app/Contents/MacOS/pico8'

gameslug = 'test-game'


def compile(inputPath):
	with open(inputPath, 'r') as inputFile:
		contents = inputFile.read()

	frontMatter, temp = contents.split('--[[')
	yamlContent, backMatter = temp.split('--]]')
	parsed = yaml.safe_load(yamlContent)
	print(parsed)
	# TODO parse out label image

def exportHtml(inputPath):
	gameslug = 'test-game'
	print('Exporting')
	cartName = f'{gameslug}.p8.png'
	os.system(f'{pico8Location} -export index.html {inputPath}')
	os.system(f'{pico8Location} -export {cartName} {inputPath}')
	print('Export complete')
	print()
	try:
		exportLoc = f'{outputLocation}/carts/{gameslug}/export'
		print('deleting ', exportLoc)
		shutil.rmtree(exportLoc)
	except FileNotFoundError:
		print('export location not found')
	print('deleting exportLoc complete')
	print()

	pathlib.Path(exportLoc).mkdir()
	inputDir = os.path.split(inputPath)[0]
	print('copying files')
	shutil.move(inputDir + '/index.html', exportLoc)
	shutil.move(inputDir + '/index.js', exportLoc)
	shutil.move(inputDir + f'/{cartName}', exportLoc)
	print('copying files complete')

		

def upload(inputPath):
	os.command(f'butler')

# compile('template.p8')
exportHtml('./template.p8')