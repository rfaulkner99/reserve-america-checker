#!/usr/bin/env python

import os
import sys
import mechanize
from bs4 import BeautifulSoup
import config

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.33 Safari/537.36')

def sendEmail(subject, text):
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

    fromaddr = secrets.email
    toaddr = secrets.email

    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address   
    msg['From'] = fromaddr 

    # storing the receivers email address  
    msg['To'] = toaddr 

    # storing the subject  
    msg['Subject'] = subject

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

def send_results(result_date, name, hits, ra_url):
    message = "On {}, found available sites at {}: {}  \r\nBook now at: {}".format(result_date, name,', '.join(hits), ra_url)
    subject = name + " " + result_date + " Campsite Found"
    # for site in hits:
    #     message += "\r\nCampsite Photos: " + campadk_url + site.lstrip("0")
    sendEmail(subject, message)
    print(subject)

def run():
    print("SCRIPT STARTING")

    def parse_page(page):

        # Scrape result
        soup = BeautifulSoup(page, "html.parser")
        table = soup.findAll("div", {"id": "shoppingitems"})

        if table:
            found_unavailable = False

            #print(table)
            rows = table[0].findAll("div", {"class": "br"})

            #loop over table, skipping first row (header)
            for row in rows[1:]:
                cells = row.findAll("div", {"class": "td"})
                l = len(cells)
                
                label = cells[0].findAll("div", {"class": "siteListLabel"})[0].text

                siteType = cells[2].text

                #could have string like: '15 Back-In'
                equip_length_driveway = cells[4].text

                length = 0
                driveway = ''

                if len(equip_length_driveway) > 1 and ' ' not in equip_length_driveway:
                    length = equip_length_driveway

                if ' ' in equip_length_driveway:
                    length = equip_length_driveway.split(' ')[0]
                    driveway = equip_length_driveway.split(' ')[1]

                status = cells[l - 1].text

                #make sure we store any available 'not available' sites
                available = False

                #print('sitetype:', label, siteType, length, driveway)

                if status.startswith('available') and siteType != 'Tent Only' and int(length) > config.rv_length:
                #if status.startswith('available'):
                    #print('sitetype:', label, siteType, length, driveway)
                    available = True
                else:
                    found_unavailable = True
                
                if available:

                    #if there are preferred sites defined:
                    if 'preferred_sites' in campground:

                        #print('found available site:', label)
                        if label in campground['preferred_sites']:
                            #print('found preferred site:', label, len(total_hits))
                            total_hits.append(label)

                    else:
                        total_hits.append(label)

            #if we found any unavailable sites then were done, because its sorted by availability
            if found_unavailable:
                print('Were done here')
            else:
                print('Additional work to do looking through next pages')

                for link in br.links():
                    #print(link)

                    attrs = dict(link.attrs) 
                    if 'id' in attrs:
                        
                        if (attrs['id'] == 'resultNext_top'):
                            #print('has id:', attrs)
                            response = br.follow_link(link)

                            #recursively call self
                            parse_page(response)


    for campground in config.campgrounds:
        total_hits = []

        # Create browser
        br = mechanize.Browser()

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', USER_AGENT)]
        html = br.open(campground['ra_url'])

        #get campground name
        page = BeautifulSoup(html, "html.parser")
        span = page.find('span', id='cgroundName')
        name = span.text
        page.decompose()
        
        # Fill out form
        br.select_form(name="unifSearchForm")
        br.form.set_all_readonly(False)  # allow changing the .value of all controls
        br.form["campingDate"] = config.date
        br.form["lengthOfStay"] = config.length_of_stay
        response = br.submit()

        #initial kickoff
        print('Processing:', name)
        parse_page(response)

        if len(total_hits) > 0:
            print(config.date, name, total_hits, campground['ra_url'])

            if config.email:
                send_results(config.date, name, total_hits, campground['ra_url'])
        else:
            message = 'No sites found for date: ' + config.date
            #sendEmail(message)
            print(message)

if __name__ == '__main__':
    run()
