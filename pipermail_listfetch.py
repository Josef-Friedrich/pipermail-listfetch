#!/usr/bin/env python3
# This script requires beautifulsoup4, requests, & lxml.
# The rest of the libraries used should be in Python3's standard library.

### Imports ###
import re
import bs4 as bs
import requests
import argparse
import os
from time import sleep
from urllib.parse import urlparse


def main():
    ### Argument parsing ###
    parser = argparse.ArgumentParser(
        description="Fetch mailing list archives.",
        epilog="MIT license. (C) 2022 Alinur.\nFull license text in LICENSE file.",
    )
    parser.add_argument(
        "webpage",
        help="Pipermail webpage to parse and fetch mailing list archives from.",
    )
    parser.add_argument(
        "--wait",
        type=float,
        metavar="s",
        default=1.5,
        help="Interval between downloading each mailing list archive (in seconds)"
        + "\nThis setting is for preventing overloading the server\n"
        + "or triggering website rate limits. Default is 1.5.",
    )

    args = parser.parse_args()
    interval = args.wait

    ### Webpage parsing ###
    page: str = requests.get(args.webpage).text
    soup = bs.BeautifulSoup(page, "lxml")

    all_links: list[str] = []
    for url in soup.find_all("a"):
        all_links.append(url.get("href"))

    archive_links: list[str] = []
    for link in all_links:
        link: str = link.replace(".gz", "")
        if link.endswith(".txt"):
            archive_links.append(link)

    ### Downloading ###
    downloaded = 0
    print(
        f"Downloaded {downloaded}/{str(len(archive_links))} mailing list archives\r",
        end="",
    )
    for archive in archive_links:
        ## Retrieve filename
        ## 2023-January.txt
        file_name = os.path.basename(urlparse(archive).path)

        if re.match(r"\d\d\d\d-\w+\.txt", file_name):
            for mount, number in {
                "January": "01",
                "February": "02",
                "March": "03",
                "April": "04",
                "May": "05",
                "June": "06",
                "July": "07",
                "August": "08",
                "September": "09",
                "October": "10",
                "November": "11",
                "December": "12",
            }.items():
                file_name: str = file_name.replace(mount, number)

            # 2022
            year: str = file_name[:4]

            # 12.txt
            file_name = file_name[5:]

            # 12.mbox
            file_name = file_name.replace('.txt', '.mbox')
            try:
                os.mkdir(year)
            except:
                pass
            rel_path: str = os.path.join(year, file_name)
        else:
            rel_path = file_name


        ## Download archive
        archived_mail: str = requests.get(args.webpage + archive).text

        final_text: str = archived_mail

        ## Save archive
        with open(rel_path, "w") as archive_file:
            archive_file.write(final_text)

        downloaded += 1
        print(
            f"Downloaded {downloaded}/{str(len(archive_links))} mailing list archives\r",
            end="",
        )
        sleep(interval)

    print(f"Finished downloading {str(len(archive_links))} mailing list archives.")
