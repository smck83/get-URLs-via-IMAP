import imaplib
import email
import re
import sys
#import socket
import requests
import time
import os

#socket.setdefaulttimeout(4) # Set socket default timeout

if 'IMAP_SERVER' in os.environ:
    IMAPserver = os.environ['IMAP_SERVER']
if 'IMAP_USERNAME' in os.environ:
    IMAPuser = os.environ['IMAP_USERNAME']
if 'IMAP_PASSWORD' in os.environ:
    IMAPpassword = os.environ['IMAP_PASSWORD']
if 'DELAY' in os.environ:
    delay = int(os.environ['DELAY'])
else:
   delay = 30
if 'IMAP_FOLDER' in os.environ:
    IMAPfolderName = os.environ['IMAP_FOLDER']
else:
   IMAPfolderName = 'Inbox'

# Connect to an IMAP server
def connect(server, user, password):
    try: 
      m = imaplib.IMAP4_SSL(server)
      m.login(user, password)
    except Exception as e:
      print("IMAP Connection Error:",str(e).replace("b'",""))
      sys.exit()
    else:
      print("connected sucessfully, scraping email")
      m.select(IMAPfolderName) # Look at e-mails in folder URLs
   
    return m

def scrape_email_for_URLs(con,emailid):
    result = []
    resp, data = con.fetch(emailid, "(BODY.PEEK[])")

    email_body = data[0][1]
    mail = email.message_from_bytes(email_body)

    for part in mail.walk():
        if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
            email_text_body=(part.get_payload(decode=True)) # prints the raw text


    urlRegex = "https?:\/\/[A-z-./&?=0-9]{0,2048}"

    urls = re.findall(urlRegex, str(email_text_body),re.IGNORECASE|re.MULTILINE)
    for url in urls:
      print(url)
      try:
        webrequest = requests.get(url)
      except Exception as e:
         print(url,e)
      else:
        print(url,":",webrequest.status_code)


def get_unseen_emails(imapserver:str=IMAPserver,username:str=IMAPuser,password:str=IMAPpassword):
    emailResults = {}
    con = connect(imapserver,username,password)
    resp, items = con.search(None, "UnSeen")
    
    items = items[0].split()
    print("Found",len(items),"unseen e-mails in IMAP folder",f"\{IMAPfolderName}:")

    for emailid in items:
        con.store(emailid, '+FLAGS', '(\\Seen)')  ## Mark the e-mail as read so it won't be printed again
        emailResults[emailid.decode('utf-8')] = scrape_email_for_URLs(con, emailid)

    con.close
    # return emailResults

while 1 != 0:
    get_unseen_emails()
    print("Sleeping for",delay,"seconds")
    time.sleep(delay)

