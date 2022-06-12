from ast import literal_eval

# print({
# 	'desc' : [[
# 	]]
# 	})

parsedFromCart = '''
__controls__ = {
	{
		inputs = {'arrow keys'},
		desc = [[
move player
]]
	},
	{
		inputs = {'left click', 'x'},
		desc = [[

]]
	}
}
'''
desc, inputs = 'desc', 'inputs'

controls = parsedFromCart.split('__controls__')[1].strip().strip('=')
controls = (controls
	.replace('=', ':')
	.replace('[[', '"""')
	.replace(']]', '"""'))
controls = controls.replace('{', '[', 1)
controls = controls.rsplit('}',1)[0] + ']'
print(controls)
print(eval(controls))