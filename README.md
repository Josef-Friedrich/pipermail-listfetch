# pipermail-listfetch
**pipermail-listfetch** is a Python script for downloading mailing list archives
 off pipermail.

## Prerequisites
- Python 3 *(You do not need latest 3.10, you should be able to use older versions without issues)*
- BeautifulSoup 4
- LXML
- Requests

You can install the needed libraries with pip3:
```
pip3 install -r requirements.txt
```

## Usage
*(arguments in [ ] are not required)*
```
./pipermail-listfetch.py mailing-list [--wait 1.5]
```
Example: `./pipermail-listfetch.py http://lists.dillo.org/pipermail/dillo-dev/ --wait 2.0`

## What's pipermail?
Pipermail is the default web archive interface for GNU Mailman, a mailing list 
software. With it, you can browse a mailing list with just your web browser.
