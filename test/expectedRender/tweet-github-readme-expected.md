# Galaxy Tweet
Galaxy inspired by density wave theory


[![xxxx]()](https://caterpillargames.itch.io/galaxy-tweet)


Play it now on [itch.io](https://caterpillargames.itch.io/galaxy-tweet) or remix it on [pico-8-edu.com](https://www.pico-8-edu.com/?c=Y2xzKDcp&g=w-w-w-w1HQHw-w2Xw-w3Xw-w2HQH)


This cart is tweetable at just 277 characters.

<pre><code>::_::
cls()
srand()
for i = 1, 100 do
	pset(rnd(128),rnd(128),7)
end
for i = 1, 1800 do
	r=rnd(50)
	p=r/30
	a=rnd() - t()/(2+r*r/50)
	x = r*cos(a)
	y = r *1.3 * sin(a)
	pset(64 + x * cos(p) - y*sin(p), 64 + x * sin(p) + y * cos(p), rnd({7,7,7,7,7,7,7,15,10}))
end
flip()
goto _</code></pre>





## About
Created for [TriJam -1](https://itch.io/jam/trijam--1/entries)  
Theme: theme1, theme2, theme3  
Development Time: None  

Also submitted to [MiniJam]()  
Theme: blah  
Limitation: You are the bad guy  




Source code available on [GitHub](https://github.com/CaterpillarGames/pico8-games/tree/master/carts/galaxy-tweet)

