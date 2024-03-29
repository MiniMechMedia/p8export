- [ ] Export submission.html
- [X] Export .p8
- [X] Export .p8.png - suppose I should reuse the .p8 thing from above
- [X] Export to itch
- [X] Export to git repo
- [X] Handle renames
- [ ] ~~Warn on renames~~
- [ ] ~~Create a working directory~~
- [ ] Ability to configure pico-8 working directory
- [X] Populate source code
- [X] Get rid of metavariables
- [X] Put ParsedLabelImage in ParsedContents instead of raw label image
- [X] Add concept of cart type (game, tweet, tweet-game, etc.)
- [X] Have cart type concept respected by compilation targets (i.e. choose the correct template)
- [X] Implement various subfolders of export
- [X] Implement README compilation target
- [X] Implement aggregate README compilation target
- [X] Deal with the gamename + gameauthor on the p8png (and p8)
- [X] Support rendering markdown to html
- [X] Add cleanup for when you are renaming a cart
- [X] Aggregate readme tests
- [ ] Add metadata for genre
- [ ] Populate genre on itch from metadata
- [ ] Lexaloffle compilation target
- [ ] Export to twitter
- [X] Support multiple controls to do the same action
- [ ] Auto-select the "Kind of project" field in itch
- [ ] Add in-band metadata like __instructions__ and __controls__
- [ ] Consume __instructions__ and __controls__ in pico8 template file
- [X] Pico8EduUrlCompilationTarget for automatically doing save @url
- [X] Jinja templating
- [X] Use metadata header
- [X] Option to process all
- [X] Add tests for each template
- [X] Add guard for acknowledgements
- [ ] Add test for acknowledgements
- [ ] Add test for no __gfx__ (but can assume __label__)
- [ ] Refactor templates so they all use the same About, Controls, etc.
- [X] Make a note that you can update the template test files with forceUpdateFiles()
- [X] Migrate all games over to new metadata
- [X] Migrate picoquarium
- [X] Number of players metadata
- [X] Add player info metadata to game.xml
- [X] Make single script on picade to consolidate all
- [ ] Refactor game.xml template to use jinja and escape formatters
- [ ] Add Mouse/Keyboard/Touch screen metadata (i.e. this game requires a mouse on picade)
- [X] Add export all option
- [X] Add test for export all
- [ ] Use ArgParser
- [X] Rebrand caterpillargames (test twitter handle)
- [X] Fix broken image in kaiju companions
- [X] Structure jam info
- [X] Add instructional image to cool cat cafe
- [X] Make cool cat cafe 2 player
- [X] Fix deal with shark shoot
- [ ] Convert controls to Flags and create a recognized group as left/right
- [ ] Fix the controls description in minigame mania (maybe a new construct)
- [X] Improvements for grow big
- [X] If theme is empty don't show it
- [X] Reupload all cover images
- [ ] Add music to shuriken
- [ ] Make music less duplicative
- [X] Fix broken link in health inspectre
- [X] Fix bug in unsigned hero
- [X] Add music to unsigned hero
- [ ] 2 player unsigned hero?
- [X] Fix link in kaiju
- [X] Add acknowledgements for fetch quest
- [ ] Autumn wind music to Drifting Keep?
- [X] Utility to add new metadata field
- [ ] Find a better song for tile isle (tropical)
- [X] Add html entity escaping
- [ ] Fix bug where jam_extra doesn't get markdowned correctly
- [ ] Add tests for html entity filter
- [X] Fix lack of .p8.png files
- [ ] Add tests for min-max
- [ ] Support up to 4 players for hamster slam
- [ ] Add metadata for left behinds
- [ ] Support keyboard for all games that support mouse
- [X] Migrate all metadata
- [X] Remove need for raw/
- [ ] Fix duplicating slug
- [ ] Populate pico8_url by using the decompressor library to get compressed png image
	- https://github.com/rvaccarim/p8png_decoder
	- https://robertovaccari.com/blog/2021_01_03_stegano_pico8/
