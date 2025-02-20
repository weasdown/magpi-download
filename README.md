# magpi-download

This simple Python program downloads all the free PDFs of Raspberry Pi's [MagPi magazine](https://magpi.raspberrypi.com/).

## How to use
### 
Firstly, make sure you have [Python](https://python.org) installed, then open a terminal window and run the following commands one after the other.
1. `git clone https://github.com/weasdown/magpi-download.git`
2. `cd magpi-download`
3. `python -m venv .venv`
4. If on Windows: `./.venv/Scripts/activate.bat`, or on Linux/macOS: `source .venv/bin/activate`
5. `python -m pip install -U -r requirements.txt`
6. `python main.py`

To view available commands, run: `python main.py -h` or `python main.py --help`.

### Downloading magazines
The magazine PDFs will be downloaded to a folder called `MagPis` inside the cloned `magpi-download` folder.
- To download all the MagPi magazines, run: `python main.py`.
- To download a single issue, specify its number with the `-i` parameter, run: `python main.py -i 150`.
- To set the folder that the magazines will download to (`MagPis` by default), use the `-p` parameter, being sure to   wrap the folder name in quotes. For examples, to download to a folder called "issues", run: `python main.py -p "issues"`.

More than one argument can be specified. For example, to download issue 100 to a folder called "magazines", run: `python main.py -i 100 -p "magazines"`.
