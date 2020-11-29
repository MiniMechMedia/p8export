import sys
import yaml
import os
import shutil
import pathlib
import glob
import base64
from PIL import Image
from slugify import slugify
# TODO support going through the entire directory
# This is the path to a given .p8 file
# inputLocation = sys.argv[1]

# TODO
# HTML stuff - instead of markdown for some stuff...
# Ability to update only, and not have it blow away the folder
# 	- Argparser (but later)
# Have pico8 start in the repo? Not by default, but make it easy
# Make an editpico8config alias

# Make the final .p8 still have all the metadata, so it can be the source of truth for maintenance
# Keep the top two lines generic though. Need to create intermediary for the export

# Config section
studio = 'Caterpillar Games'
itch_name = 'caterpillargames'
outputLocation = "/Users/nathandunn/Projects/pico8-games"
pico8Location = '/Applications/PICO-8.app/Contents/MacOS/pico8'

# gameslug = 'test-game'
readmeTempalte = '''\
# {game_name}
{description}
{extras}
[![{img_alt}](screenshots/cover.png)](https://{itch_name}.itch.io/{game_slug})

Play it now on [itch.io](https://{itch_name}.itch.io/{game_slug})

## Controls
{controls}

## About
Created for [TriJam #{trijam_number}](https://itch.io/jam/trijam-{trijam_number}/entries)
Theme: {trijam_theme}
Development Time: {develop_time}
'''

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


def writeP8file(config, gamedir, gameslug):
	# finalContents = frontMatter + backMatter
	finalContents = config.original_contents
	# Can't use `format` because of the curlies
	finalContents = (finalContents
		.replace('{GAMENAME}',config.game_name.lower())
		.replace('{AUTHORINFO}', f'by {config.studio.lower()}')
	)

	finalP8Path = f'{gamedir}/{gameslug}.p8'
	print('writing p8 result')
	with open(finalP8Path, 'w') as outFile:
		outFile.write(finalContents)
	print('finished writing p8 result')
	return finalP8Path

def writeReadme(config):
	rendered = readmeTempalte.format(**config.source)
	with open(f'{config.game_dir}/README.md', 'w') as outFile:
		outFile.write(rendered)

def updateRootReadme(config):
	with open(config.root_readme_path, 'r') as inFile:
		contents = inFile.read()

	gameContent = f'''\
## [{config.game_name}](carts/{config.game_slug})
<a href="carts/{config.game_slug}">
	<img alt="Cover image for {config.game_name} - {config.img_alt}"
		src="carts/{config.game_slug}/screenshots/cover.png"
		>
</a>'''

	gameSectionStart = '<!--BEGIN GAMES-->'
	sectionStart = f'<!--BEGIN {config.game_slug}-->'
	sectionEnd = f'<!--END {config.game_slug}-->'
	if sectionStart in contents:
		front, rest = contents.split(sectionStart)
		_, back = rest.split(sectionEnd)
		front = front.rstrip()
		back = back.lstrip()
	else:
		front, back = contents.split(gameSectionStart)
		front += gameSectionStart
	
	finalContents = f'''\
{front}
{sectionStart}
{gameContent}
{sectionEnd}
{back}'''
	
	with open(config.root_readme_path, 'w') as outFile:
		outFile.write(finalContents)


class Config:
	def __init__(self, yamlDict, **supplemental):
		self.source = yamlDict
		self.source['itch_name'] = itch_name
		self.source['studio'] = studio
		self.source['game_slug'] = self.source['game_slug'] or slugify(self.source['game_name'])
		# self.source['original_p8file_loc'] = inputPath
		self.source.update(supplemental)

	def __getattr__(self, key):
		return self.source[key]

	def validate(self):
		# 31 is max characters that can fit on a cartridge without getting cut off
		if len(self.game_name) > 31:
			raise Exception(f'Game name "{self.game_name}" is too long')

	@property
	def game_dir(self):
		return f'{outputLocation}/carts/{self.game_slug}'

	@property
	def repo_root(self):
		return f'{outputLocation}'

	@property
	def root_readme_path(self):
		return f'{self.repo_root}/README.md'
	
	
	

def compile(inputPath):
	with open(inputPath, 'r') as inputFile:
		contents = inputFile.read()

	frontMatter, temp = contents.split('--[[')
	yamlContent, backMatter = temp.split('--]]')
	parsed = yaml.safe_load(yamlContent)

	config = Config(parsed, original_p8file_loc=inputFile, original_contents=contents)
	config.validate()

	# TODO deprecate these variables
	gameslug = config.game_slug
	# print(parsed)
	# exit()
	# finalContents = contents
	# TODO parse out label image

	gamedir = f'{outputLocation}/carts/{gameslug}'
	resetGameDir(gamedir)

	# TODO detect if file has no label image
	finalP8Path = writeP8file(config, gamedir, gameslug)

	writeReadme(config)

	updateRootReadme(config)

	htmlLoc = exportArtifacts(finalP8Path, gameslug)

	exportGameplayPng(gamedir, finalP8Path)

	# TODO command line arg to suppress upload
	if False:
		upload(htmlLoc, gameslug, config)

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



def exportGameplayPng(gamedir, finalP8Path):
	# print(htmlFilePath)
	# with open(htmlFilePath, 'r') as htmlFile:
	# 	contents = htmlFile.read()

	with open(finalP8Path, 'r') as p8File:
		contents = p8File.read()

	pixels = []

	scale = 3

	for row in contents.split('__label__')[1].split():
		if not all(c in '0123456789abcdef' for c in row):
			break
		# Also break if we get an empty line in there
		if not row:
			break
		# pixelRow = [*(scale * [colmap[f'0x{c}']]) for c in row]
		pixelRow = []
		for c in row:
			color = colmap['0x' + c]
			for _ in range(scale):
				pixelRow.append(color)

		for _ in range(scale):
			pixels.append(pixelRow)

	# TODO scale up to 3x
	newimg = Image.new('RGB', (scale*128, scale*128))
	newimg.putdata(sum(pixels, start = []))
	screenshotDir = f'{gamedir}/screenshots'
	pathlib.Path(screenshotDir).mkdir()
	newimg.save(f'{gamedir}/screenshots/cover.png')
	# newimg.save(f'mytest.png')
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
	return htmlLoc

		

def upload(htmlLoc, gameslug, config):
	cmd = (f'butler push --if-changed {htmlLoc} {config.itch_name}/{gameslug}:web')
	print('invoking butler')
	print(cmd)
	os.system(cmd)
	print('butler push success')

# compile('template.p8')
compile(sys.argv[1])
# exportHtml('./template.p8')
