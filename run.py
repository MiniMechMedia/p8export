import sys
import yaml
import os
import shutil
import pathlib
import glob
import base64
import markdown
from PIL import Image
from slugify import slugify
import glob
from datetime import datetime, timedelta

# TODO support going through the entire directory
# This is the path to a given .p8 file
# inputLocation = sys.argv[1]

# TODO
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

rootReadmeTemplate = '''\
## [{game_name}](carts/{game_slug})
[![Cover image for {game_name} - {img_alt}](carts/{game_slug}/screenshots/cover.png)](carts/{game_slug})
'''

acknowledgementsTemplate = '''\
## Acknowledgements
{acknowledgements}
'''

todoTemplate = '''\
## TODO
{todo}
'''

hintTemplate = '''\
## Hints
{hints}
'''

shared = '''\
## Controls
{controls}

{hints}

## About
Created for [TriJam #{trijam_number}](https://itch.io/jam/trijam-{trijam_number}/entries)  
Theme: {trijam_theme}  
Development Time: {develop_time}  
Source Code: On [GitHub](https://github.com/CaterpillarGames/pico8-games/tree/master/carts/{game_slug})

{acknowledgements}
'''
# <!-- TOOD figure out {{aboutextras}} -->

submissionTemplate = '''\
{tagline}

<!-- BREAK -->

{description}

''' + shared

# gameslug = 'test-game'
readmeTemplate = '''\
# {game_name}
{description}
[![{img_alt}](screenshots/cover.png)](https://{itch_name}.itch.io/{game_slug})

Play it now on [itch.io](https://{itch_name}.itch.io/{game_slug})

''' + shared + '{todo}'

def resetGameDir(gamedir):
	print('removing existing')
	try:
		# shutil.rmtree(gamedir)
		for p8 in glob.glob(f'{gamedir}/*.p8'):
			os.remove(p8)
		print('removed p8')
		shutil.rmtree(f'{gamedir}/export')
		print('removed export')
		os.remove(f'{gamedir}/README.md')
		print('removed README')
		os.remove(f'{gamedir}/screenshots/cover.png')
		print('removed cover')

	except FileNotFoundError:
		print('did not exist')
	print('remove existing complete')

	print('creating new dir')
	try:
		pathlib.Path(gamedir).mkdir()
	except FileExistsError:
		print('new dir existed')
	else:
		print('new dir complete')


def writeP8file(config, gamedir, gameslug):
	frontMatter, backMatter, _ = parseContents(config.original_contents)
	finalContents = frontMatter + backMatter
	# finalContents = config.original_contents

	# Can't use `format` because of the curlies
	finalContents = (finalContents
		.replace('{GAMENAME}',config.game_name_for_cart)
		.replace('{AUTHORINFO}', f'by {config.studio.lower()}')
	)

	finalP8Path = f'{gamedir}/{gameslug}.p8'
	print('writing p8 result')
	with open(finalP8Path, 'w') as outFile:
		outFile.write(finalContents)
	print('finished writing p8 result')
	return finalP8Path

def writeText(config):
	rendered = readmeTemplate.format(**config.source)
	with open(f'{config.game_dir}/README.md', 'w') as outFile:
		outFile.write(rendered)

	with open(f'{config.export_dir}/submission.html', 'w') as file:
		rendered = markdown.markdown(submissionTemplate.format(**config.source))
		file.write(rendered)




def updateRootReadme(config):
	with open(config.root_readme_path, 'r') as inFile:
		contents = inFile.read()

	gameContent = rootReadmeTemplate.format(**config.source)
# <a href="carts/{config.game_slug}">
# 	<img alt="Cover image for {config.game_name} - {config.img_alt}"
# 		src="carts/{config.game_slug}/screenshots/cover.png"
# 		>
# </a>'''

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


def calcDevelopTime(time_left_str):
	s1 = time_left_str
	# print(time_left_str)
	# raise	Exception()
	s2 = '3:00:00'
	fwkDev = timedelta(seconds = 3*60 + 51)  #'0:03:51'
	FMT = '%H:%M:%S'
	tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT) - fwkDev
	# Seriously, python?
	hours = tdelta.seconds // 3600
	minutes = (tdelta.seconds // 60)%60
	seconds = tdelta.seconds % 60
	return f'{hours}h {minutes}m {seconds}s'

class Config:
	def __init__(self, yamlDict, **supplemental):
		self.source = yamlDict
		self.source['itch_name'] = itch_name
		self.source['studio'] = studio
		self.source['game_slug'] = self.source['game_slug'] or slugify(self.source['game_name'])
		# self.source['original_p8file_loc'] = inputPath
		self.source.update(supplemental)

		self.testSelf('acknowledgements', acknowledgementsTemplate)
		self.testSelf('todo', todoTemplate)
		self.testSelf('hints', hintTemplate)

		if not self.source['develop_time']:
			self.source['develop_time'] = calcDevelopTime(self.source['time_left'])
		# if self.source['acknowledgements']:
			# self.source['acknowledgements'] = acknowledgementsTemplate.format(acknowledgements = self.source['acknowledgements'])

	def testSelf(self, key, template):
		if self.source[key]:
			self.source[key] = template.format(**self.source)

	def __getattr__(self, key):
		return self.source[key]

	def validate(self):
		# 31 is max characters that can fit on a cartridge without getting cut off
		if len(self.game_name) > 31:
			raise Exception(f'Game name "{self.game_name}" is too long')

		if any('XX' in val for val in self.source.values() if type(val) is str):
			raise Exception('Templated content')

	@property
	def game_name_for_cart(self):
		return self.game_name.lower().ljust(31) + 'v' + self.source['version']
	
	@property
	def game_dir(self):
		return f'{outputLocation}/carts/{self.game_slug}'

	@property
	def export_dir(self):
		return f'{self.game_dir}/export'
	

	@property
	def repo_root(self):
		return f'{outputLocation}'

	@property
	def root_readme_path(self):
		return f'{self.repo_root}/README.md'
	
	
def parseContents(contents):

	frontMatter, temp = contents.split('--[[')
	yamlContent, backMatter = temp.split('--]]')
	parsed = yaml.safe_load(yamlContent)

	return frontMatter, backMatter, parsed

def compile(inputPath):
	with open(inputPath, 'r') as inputFile:
		contents = inputFile.read()

	_, _, parsed = parseContents(contents)

	config = Config(parsed, original_p8file_loc=inputFile, original_contents=contents)
	config.validate()

	# TODO deprecate these variables
	gameslug = config.game_slug
	# print(parsed)
	# exit()
	# finalContents = contents
	# TODO parse out label image

	gamedir = config.game_dir
	resetGameDir(gamedir)

	# TODO detect if file has no label image
	finalP8Path = writeP8file(config, gamedir, gameslug)

	updateRootReadme(config)

	htmlLoc = exportArtifacts(finalP8Path, gameslug, config)

	writeText(config)

	# exportSubmissionText(config)

	exportGameplayPng(gamedir, finalP8Path)

	# TODO command line arg to suppress upload
	if True:
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
	try:
		pathlib.Path(screenshotDir).mkdir()
	except FileExistsError:
		pass

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
def exportArtifacts(finalP8Path, gameslug, config):
	gamedir, cartName = os.path.split(finalP8Path)
	cartName += '.png'

	print('Exporting')
	os.system(f'{pico8Location} -export index.html {finalP8Path}')
	os.system(f'{pico8Location} -export {cartName} {finalP8Path}')
	print('Export complete')

	exportLoc = config.export_dir
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
	cmd = (f'butler push --if-changed {htmlLoc} {config.itch_name}/{gameslug}:web --userversion {config.version}')
	# cmd = (f'butler push {htmlLoc} {config.itch_name}/{gameslug}:web --userversion {config.version}')
	print('invoking butler')
	print(cmd)
	# os.system(cmd)
	print('butler push success')

# compile('template.p8')
compile(sys.argv[1])
# exportHtml('./template.p8')
