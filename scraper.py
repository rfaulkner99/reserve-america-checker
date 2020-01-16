#!/usr/bin/env python

import os
import sys
import mechanize
from bs4 import BeautifulSoup
import config

# Configuration
date = "07/24/2020"
length_of_stay = "2"

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.33 Safari/537.36')

def sendEmail(text):
    #https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/

    # Python code to illustrate Sending mail with attachments 
    # from your Gmail account  

    # libraries to be imported 
    import smtplib 
    from email.mime.multipart import MIMEMultipart 
    from email.mime.text import MIMEText 
    from email.mime.base import MIMEBase 
    from email import encoders
    import secrets

    fromaddr = "martynjsmith@gmail.com"
    toaddr = "martynjsmith@gmail.com"

    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address   
    msg['From'] = fromaddr 

    # storing the receivers email address  
    msg['To'] = toaddr 

    # storing the subject  
    msg['Subject'] = "Waterfront Campsite Found "

    # string to store the body of the mail 
    body = text

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login(fromaddr, secrets.password) 

    # Converts the Multipart msg into a string 
    text = msg.as_string() 

    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 

    # terminating the session 
    s.quit() 

def send_results(result_date, name, hits):
    message = "On {}, found available waterfront sites at {}: {}".format(result_date, name,', '.join(hits))
    sendEmail(message)
    print(message)

def run():
    print("SCRIPT STARTING")

    for campground in config.campgrounds:
        print('Processing:', campground['name'])
        hits = []

        # Create browser
        br = mechanize.Browser()

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', USER_AGENT)]
        br.open(campground['ra_url'])

        # Fill out form
        br.select_form(name="unifSearchForm")
        br.form.set_all_readonly(False)  # allow changing the .value of all controls
        br.form["campingDate"] = date
        br.form["lengthOfStay"] = length_of_stay
        response = br.submit()

        # Scrape result
        soup = BeautifulSoup(response, "html.parser")
        table = soup.findAll("div", {"id": "shoppingitems"})

        if table:
            #print(table)
            rows = table[0].findAll("div", {"class": "br"})

            #loop over table, skipping first row (header)
            for row in rows[1:]:
                cells = row.findAll("div", {"class": "td"})
                l = len(cells)
                label = cells[0].findAll("div", {"class": "siteListLabel"})[0].text
                status = cells[l - 1].text
                if status.startswith('available') and label in campground['preferred_sites']:
                    hits.append(label)

        if hits:
            send_results(date, campground['name'], hits)
        else:
            message = 'No water sites found for date: ' + date
            #sendEmail(message)
            print(message)

if __name__ == '__main__':
    run()
