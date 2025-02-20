# magpi-download

This simple Python program downloads all the free PDFs of Raspberry Pi's [MagPi magazine](https://magpi.raspberrypi.com/).

## Getting started
To download all the MagPi magazines, make sure you have [Python](https://python.org) installed, then open a terminal window and run the following commands one after the other. The magazine PDFs will be downloaded to a folder called `MagPi` inside the cloned `magpi-download` folder.
1. `git clone https://github.com/weasdown/magpi-download.git`
2. `cd magpi-download`
3. `python -m venv .venv`
4. If on Windows: `./.venv/Scripts/activate.bat`, or on Linux/macOS: `source .venv/bin/activate`
5. `python -m pip install -U -r requirements.txt`
6. `python main.py`
