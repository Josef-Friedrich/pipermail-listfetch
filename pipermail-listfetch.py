#!/usr/bin/env python3
# This script requires beautifulsoup4, requests, & lxml.
# The rest of the libraries used should be in Python3's standard library.

### Imports ###
import bs4 as bs
import requests
import argparse
import os
from time import sleep
from urllib.parse import urlparse

### Argument parsing ###
parser = argparse.ArgumentParser(description="Fetch mailing list archives.",
    epilog="MIT license. (C) 2022 Alinur.\nFull license text in LICENSE file.")
parser.add_argument("webpage",
    help="Pipermail webpage to parse and fetch mailing list archives from.")
parser.add_argument("--wait", type=float, metavar="s", default=2.5,
    help="Interval between downloading each mailing list archive (in seconds)" +
         "\nThis setting is for preventing overloading the server\n" +
         "or triggering website rate limits. Default is 2.5.")

args = parser.parse_args()
interval = args.wait

### Webpage parsing ###
page = requests.get(args.webpage).text
soup = bs.BeautifulSoup(page,'lxml')

all_links=[]
for url in soup.find_all('a'):
    all_links.append(url.get('href'))

archive_links=[]
for link in all_links:
    link = link.replace(".gz",'')
    if link.endswith(".txt"):
        archive_links.append(link)

### Downloading ###
dled = 0
print(f"Downloaded {dled}/{str(len(archive_links))} mailing list archives\r",
        end="")
for archive in archive_links:
    ## Retrieve filename
    fname = os.path.basename(urlparse(archive).path)
    ## Download archive
    archived_mail = requests.get(args.webpage + archive).text
    
    final_text = archived_mail

    ## Save archive
    with open(fname, 'w') as archive_file:
        archive_file.write(final_text)

    dled += 1
    print(f"Downloaded {dled}/{str(len(archive_links))} mailing list archives\r",
            end="")
    sleep(interval)

print(f"Finished downloading {str(len(archive_links))} mailing list archives.")


