pico-8 cartridge // http://www.pico-8.com
version 18
__lua__
--{GAMENAME}
--{AUTHORINFO} 

--[[
trijam-number: XX
trijam-theme: XX
develop-time: X:XX:XX
trijam-link: {SUBMISSIONLINK}
game-name: XXXXXXXX
# Leave blank to use game-name
game-slug: test-game
tagline: XXXXXXXX
description: |
  hello there
  this is multiline?
controls: |
  * Arrow Keys - stuff
  * X - start new game
--]]


function vec2(x, y)

end

dirs = {
	left = 0,
	right = 1,
	up = 2,
	down = 3, 
	z = 4,
	x = 5
}

col = {
	black = 0,
	darkblue = 1,

}

function _init()
	gs = {

	}
end

function _update()
end

function _draw()
end

__gfx__
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00700700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00077000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00077000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00700700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
__label__
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000055555555555555500000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000055555566666666666666655555500000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000555566666666666666666666666666655550000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000555666666666666666666666666666666666665550000000000000000000000000000000000000000000
00000000000000000000000000000000000000000555666666666666666666666666666666666666666665550000000000000000000000000000000000000000
00000000000000000000000000000000000000055666666666666666666666666666666666666666666666665500000000000000000000000000000000000000
00000000000000000000000000000000000005566666666666666666666666666666666666666666666666666655000000000000000000000000000000000000
00000000000000000000000000000000000556666666666666666666666666666666666666666666666666666666550000000000000000000000000000000000
00000000000000000000000000000000055666666666666666666666666666666666666666666666666666666666665500000000000000000000000000000000
00000000000000000000000000000005566666666666666666666666666666666666666666666666666666666666666655000000000000000000000000000000
00000000000000000000000000000056666666666666666666666666666666666666666666666666666666666666666666500000000000000000000000000000
00000000000000000000000000005566666666666666666666666666666666666666666666666666666666666666666666655000000000000000000000000000
00000000000000000000000000056666666666666666666666666666666666666666666666666666666666666666666666666500000000000000000000000000
00000000000000000000000000566666666666666666666666666666666666666666666666666666666666666666666666666650000000000000000000000000
00000000000000000000000055666666666666666666666666666666666666666666666666666666666666666666666666666665500000000000000000000000
00000000000000000000000566666666666666666666666666666666666666666666666666666666666666666666666666666666650000000000000000000000
00000000000000000000005666666666666666666666666666666666666666666666666666666666666666666666666666666666665000000000000000000000
00000000000000000000056666666666666666666666666666666666666666666666666666666666666666666666666666666666666500000000000000000000
00000000000000000000566666666666666666666666666666666666666666666666666666666666666666666666666666666666666650000000000000000000
00000000000000000005666666666666666666666666666666666666666666666666666666666666666666666666666666666666666665000000000000000000
00000000000000000056666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666500000000000000000
00000000000000000566666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666650000000000000000
00000000000000005666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666665000000000000000
00000000000000056666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666500000000000000
00000000000000056666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666500000000000000
00000000000000566666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666650000000000000
00000000000005666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666665000000000000
00000000000056666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666500000000000
00000000000056666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666500000000000
00000000000566666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666650000000000
00000000005666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666665000000000
00000000005666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666665000000000
00000000056666666666666666666666666666666666666666666666666668888888666666666666666666666666666666666666666666666666666500000000
00000000056666666666666666666666666666666666666666666666666886666666886666666666666666666666666666666666666666666666666500000000
00000000566666666666666666666666666666666666666666666666668666666666668666666666666666666666666666666666666666666666666650000000
0000000056666666666666666666666666666666666666666666666668666666e666666866666666666666666666666666666666666666666666666650000000
00000005666666666666666666666666666666666666666666666666866666644466666686666666666666666666666666666666666666666666666665000000
00000005666666666666666666666666666666666666666666666668666666444446666668666666666666666666666666666666666666666666666665000000
00000056666666666666666666666666666666666666666666666668666666404046666668666666666666666666666666666666666666666666666666500000
00000056666666666666666666666666666666666666666666666686666666444446666666866666666666666666666666666666666666666666666666500000
00000566666666666666666666666666666666666666666666666686666664444404666666866666666666666666666666666666666666666666666666650000
00000566666666666666666666666666666666666666666666666686666664444400666666866666666666666666666666666666666666666666666666650000
00000566666666666666666666666666666666666666666666666686666660004400666666866666666666666666666666666666666666666666666666650000
00005666666666666666666666666666666666666666666666666686666660004440666666866666666666666666666666666666666666666666666666665000
00005666666666666666666666666666666666666666666666666686666660004444666666866666666666666666666666666666666666666666666666665000
00005666666666666666666666666666666666666666666666666686666664004444666666866666666666666666666666666666666666666666666666665000
00056666666666666666666666666666666666666666666666666668666664044444666668666666666666666666666666666666666666666666666666666500
00056666666666666666666666666666666666666666666666666668666666444446666668666666666666666666666666666666666666666666666666666500
00056666666666666666666666666666666666666666666666666666866666444446666686666666666666666666666666666666666666666666666666666500
0005666666666666666666666666666666666666666666666666666668666666e666666866666666666666666666666666666666666666666666666666666500
0056666666666666666666666666666666666666666666666666666666866666e666668666666666666666666666666666666666666666666666666666666650
00566666666666666666666666666666666666666666666666666666666886666666886666666666666666666666666666666666666666666666666666666650
00566666666666666666666666666666666666666666666666666666ccccccc88888666666666666666666666666666666666666666666666666666666666650
005666666666666666666666666666666666666666666666666666cc6666666cc666666666666666666666666666666666666666666666666666666666666650
00566666666666666666666666666666666666666666666666666c66666666666c66666666666666666666666666666666666666666666666666666666666650
0056666666666666666666666666666666666666666666666666c6666666666666c6666666666666666666666666666666666666666666666666666666666650
056666666666666666666666666666666666666666666666666c666666666666666c666666666666666666666666666666666666666666666666666666666665
05666666666666666666666666666666666666666666666666c66666666666666666c66666666666666666666666666666666666666666666666666666666665
05666666666666666666666666666666666666666666666666c66666666666666666c66666666666666666666666666666666666666666666666666666666665
0566666666666666666666666666666666666666666666666c6666667777777666666c6666666666666666666666666666666666666666666666666666666665
0566666666666666666666666666666666666666666666666c6666777777777777666c6666666666666666666666666666666666666666666666666666666665
0566666666666666666666666666666666666666666666666c6666777777777707766c6666666666666666666666666666666666666666666666666666666665
0566666666666666666666666666666666666666666666666c66ee7777777777777e6c6666666666666666666666666666666666666666666666666666666665
0566666666666666666666666666666666666666666666666c6666777777777707766c6666666666666666666666666666666666666666666666666666666665
0566666666666666666666666666666666666666666666666c6666777777777777666c6666999999966666666666666666666666666666666666666666666665
0566666666666666666666666666666666666666666666666c6666667777777666666c6699666666699666666666666666666666666666666666666666666665
05666666666666666666666666666666666666666666666666c66666666666666666c66966666666666966666666666666666666666666666666666666666665
05666666666666666666666666666666666666666666666666c66666666666666666c696666666e6666696666666666666666666666666666666666666666665
056666666666666666666666666666666666666666666666666c666666666666666c6966666666e6666669666666666666666666666666666666666666666665
0566666666666666666666666666666666666666666666666666c6666666666666c6966666665555566666966666666666666666666666666666666666666665
05666666666666666666666666666666666666666666666666666c66666666666c66966666665575566666966666666666666666666666666666666666666665
005666666666666666666666666666666666666666666666666666cc6666666cc669666666655555556666696666666666666666666666666666666666666650
00566666666666666666666666666666666666666666666666666666ccccccc66669666666655755556666696666666666666666666666666666666666666650
00566666666666666666666666666666666666666666666666666666666666666669666666655555756666696666666666666666666666666666666666666650
00566666666666666666666666666666666666666666666666666666666666666669666666655555556666696666666666666666666666666666666666666650
00566666666666666666666666666666666666666666666666666666666666666669666666655555556666696666666666666666666666666666666666666650
00566666666666666666666666666666666666666666666666666666666666666669666666655555556666696666666666666666666666666666666666666650
00056666666666666666666666666666666666666666666666666666666666666669666666675575556666696666666666666666666666666666666666666500
00056666666666666666666666666666666666666666666666666666666666666666966666665555566666966666666666666666666666666666666666666500
00056666666666666666666666666666666666666666666666666666666666666666966666665050566666966666666666666666666666666666666666666500
00056666666666666666666666666666666666666666666666666666666666666666696666665555566669666666666666666666666666666666666666666500
00005666666666666666666666666666666666666666666666666666666666666666669666666555666696666666666666666666666666666666666666665000
000056666666666666666666666666666666666666666666666666666666666666666669666666e6666966666666666666666666666666666666666666665000
00005666666666666666666666666666666666666666666666666666666666666666666699666666699666666666666666666666666666666666666666665000
00000566666666666666666666666666666666666666666666666666666666666666666666999999966666666666666666666666666666666666666666650000
00000566666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666650000
00000566666666666666666666666666666666666666666663333333666666666666666666666666666666666666666666666666666666666666666666650000
00000056666666666666666666666666666666666666666336666666336666666666666666666666666666666666666666666666666666666666666666500000
00000056666666666666666666666666666666666666663666666666663666666666666666666666666666666666666666666666666666666666666666500000
00000005666666666666666666666666666666666666636666666666666366666666666666666666666666666666666666666666666666666666666665000000
00000005666666666666666666666666666666666666366666666666666e36666666666666666666666666666666666666666666666666666666666665000000
0000000056666666666666666666666666666666666366666666666666e663666666666666666666666666666666666666666666666666666666666650000000
000000005666666666666666666666666666666666636666666666ff4f6663666666666666666666666666666666666666666666666666666666666650000000
0000000005666666666666666666666666666666663666666666ffff446666366666666666666666666666666666666666666666666666666666666500000000
000000000566666666666666666666666666666666366666666ffff44f6666366666666666666666666666666666666666666666666666666666666500000000
00000000005666666666666666666666666666666636666666fffff44f6666366666666666666666666666666666666666666666666666666666665000000000
000000000056666666666666666666666666666666366666644ffff4f66666366666666666666666666666666666666666666666666666666666665000000000
00000000000566666666666666666666666666666636666644fffffff66666366666666666666666666666666666666666666666666666666666650000000000
00000000000056666666666666666666666666666636666fffffffff666666366666666666666666666666666666666666666666666666666666500000000000
00000000000056666666666666666666666666666636666f0fff44ff666666366666666666666666666666666666666666666666666666666666500000000000
00000000000005666666666666666666666666666663666fff0f44f6666663666666666666666666666666666666666666666666666666666665000000000000
00000000000000566666666666666666666666666663666ffffff666666663666666666666666666666666666666666666666666666666666650000000000000
00000000000000056666666666666666666666666666366efff66666666636666666666666666666666666666666666666666666666666666500000000000000
00000000000000056666666666666666666666666666636666666666666366666666666666666666666666666666666666666666666666666500000000000000
00000000000000005666666666666666666666666666663666666666663666666666666666666666666666666666666666666666666666665000000000000000
00000000000000000566666666666666666666666666666336666666336666666666666666666666666666666666666666666666666666650000000000000000
00000000000000000056666666666666666666666666666663333333666666666666666666666666666666666666666666666666666666500000000000000000
00000000000000000005666666666666666666666666666666666666666666666666666666666666666666666666666666666666666665000000000000000000
00000000000000000000566666666666666666666666666666666666666666666666666666666666666666666666666666666666666650000000000000000000
00000000000000000000056666666666666666666666666666666666666666666666666666666666666666666666666666666666666500000000000000000000
00000000000000000000005666666666666666666666666666666666666666666666666666666666666666666666666666666666665000000000000000000000
00000000000000000000000566666666666666666666666666666666666666666666666666666666666666666666666666666666650000000000000000000000
00000000000000000000000055666666666666666666666666666666666666666666666666666666666666666666666666666665500000000000000000000000
00000000000000000000000000566666666666666666666666666666666666666666666666666666666666666666666666666650000000000000000000000000
00000000000000000000000000056666666666666666666666666666666666666666666666666666666666666666666666666500000000000000000000000000
00000000000000000000000000005566666666666666666666666666666666666666666666666666666666666666666666655000000000000000000000000000
00000000000000000000000000000056666666666666666666666666666666666666666666666666666666666666666666500000000000000000000000000000
00000000000000000000000000000005566666666666666666666666666666666666666666666666666666666666666655000000000000000000000000000000
00000000000000000000000000000000055666666666666666666666666666666666666666666666666666666666665500000000000000000000000000000000
00000000000000000000000000000000000556666666666666666666666666666666666666666666666666666666550000000000000000000000000000000000
00000000000000000000000000000000000005566666666666666666666666666666666666666666666666666655000000000000000000000000000000000000
00000000000000000000000000000000000000055666666666666666666666666666666666666666666666665500000000000000000000000000000000000000
00000000000000000000000000000000000000000555666666666666666666666666666666666666666665550000000000000000000000000000000000000000
00000000000000000000000000000000000000000000555666666666666666666666666666666666665550000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000555566666666666666666666666666655550000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000055555566666666666666655555500000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000055555555555555500000000000000000000000000000000000000000000000000000000
