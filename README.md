# Set Up
Install chromium web driver (latest stable) and make a note of the path.
Create a `.env` file of the form
```text
PICO8EXE=<absolute_path_to_pico8_exe>
ITCH_USERNAME=<username>
ITCH_PASSWORD=<password>
CHROMEEXE=<absolute_path_to_chrome_driver>
GAME_AUTHOR=<title to put on cartridges>
```

# Usage
`python p8export.py /path/to/pico8_file.p8`
