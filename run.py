import sys
import yaml
import os
import shutil
import pathlib
import glob
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

	finalP8Path = writeP8file(gamedir, gameslug, finalContents)

	writeReadme(gamedir)

	exportHtml(finalP8Path)

	exportGameplayPng(finalP8Path)

	# print('deleting existing .p8')
	# destPath = f'{outputLocation}/carts/{gameslug}'
	# for p8 in glob.glob(outputLocation + '/*.p8'):
	# 	os.remove(p8)
	# print('existing .p8 removed')

	# with open

def exportGameplayPng(finalP8Path):
	gamedir, cartName = os.path.split(finalP8Path)
	screenshotDir = f'{gamedir}/screenshots'
	pathlib.Path(screenshotDir).mkdir()
	with open(screenshotDir + '/x.png', 'wb'):
		pass


def exportHtml(finalP8Path):
	gamedir, cartName = os.path.split(finalP8Path)
	cartName += '.png'


	print('Exporting')
	os.system(f'{pico8Location} -export index.html {finalP8Path}')
	os.system(f'{pico8Location} -export {cartName} {finalP8Path}')
	print('Export complete')

	exportLoc = f'{gamedir}/export'
	print('creating export dir')
	pathlib.Path(exportLoc).mkdir()
	print('export dir complete')

	print('copying files')
	shutil.move('index.html', exportLoc)
	shutil.move('index.js', exportLoc)
	shutil.move(cartName, exportLoc)
	print('copying files complete')

		

def upload(inputPath):
	os.command(f'butler')

compile('template.p8')
# exportHtml('./template.p8')
