#!/usr/bin/env python

import os
import sys
import urllib.request
from bs4 import BeautifulSoup

# Configuration
url = "https://www.campadk.com/campsitephotos/campgrounds/Fish+Creek/choosesite"

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.33 Safari/537.36')

def send_results(hits):
    print("Found water sites:", hits)

def run():
    print("SCRIPT STARTING")
    hits = []

    page = urllib.request.urlopen(url)

    # Scrape result
    soup = BeautifulSoup(page, "html.parser")
    sites = soup.findAll("a", {"class": "btn-onwater"})
    for site in sites:
        label = site.text
        if label not in hits:
            hits.append(label)

    if hits:
        send_results(hits)

if __name__ == '__main__':
    run()