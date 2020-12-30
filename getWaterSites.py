#!/usr/bin/env python

import os
import sys
import urllib.request
import re
from bs4 import BeautifulSoup

# Configuration
url = "https://www.campadk.com/campsitephotos/campgrounds/Lincoln+Pond/choosesite"

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.33 Safari/537.36')

def send_results(hits):
    print("Found water sites:", hits)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def hasLetters(inputString):
    return any(char.isalpha() for char in inputString)

def run():
    print("SCRIPT STARTING")
    hits = []

    page = urllib.request.urlopen(url)

    # Scrape result
    soup = BeautifulSoup(page, "html.parser")
    sites = soup.findAll("a", {"class": "btn-onwater"})
    for site in sites:
        label = site.text.strip()
        clean_label = ''

        #check the site number has a number and a letter
        if hasNumbers(label) and hasLetters(label):
            #print('label has letters and numbers', label)
            label_list = re.split('(\d+)',label)
            #print(label_list)

            #if first item is a string
            if hasLetters(label_list[0]):
                clean_label = label_list[0] + label_list[1].zfill(3)
            if hasLetters(label_list[2]):
                clean_label = label_list[1].zfill(3) + label_list[2]

        #have regular number but we still need to pad
        else:
            clean_label = label.zfill(3)

        #print('label', label, bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', label)))
        if clean_label not in hits:
            hits.append(clean_label)

    if hits:
        send_results(hits)

if __name__ == '__main__':
    run()