# fakexrandr-background
## Background slideshow for virtual fakexrandr displays
Choses random pictures out of a folder and sets a different picture for every display every n-minutes.
Uses cv2 to generate the pictures and gsettings to set the background. Tested on Ubuntu 21.04.

### Install
1. Download the latest release from [here](https://github.com/Alwinator/fakexrandr-background/releases).
2. Extract the files
3. Make fakexrandr_background executable:
```
chmod +x fakexrandr_background
```
4. Run (1800 for a image change every 30 minutes [60 * 30])
```
/path/to/fakexrandr_background /path/to/pictures 1800
```
5. Add the run command to autostart:
Add the following line to `/home/user/.profile`
```
/path/to/fakexrandr_background /path/to/pictures 1800 --delay 4 &
```

### Pull Requests and Bug reports are welcome!
#### DEV Setup
1. Setup virtualenv with Python 3.9
2. `poetry install`
3. `python fakexrandr_background/main.py`
