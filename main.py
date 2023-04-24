import imaplib
import email
import re

IMAPserver = "<--imap-server-->"
IMAPuser = "<--imap-username-->"
IMAPpassword = "<--imap-password-->"
IMAPfolderName= "URLs" # Set this to a folder you which to target, e.g. it could be Inbox

# Connect to an IMAP server
def connect(server, user, password):
    try: 
      m = imaplib.IMAP4_SSL(server)
      m.login(user, password)
    except Exception as e:
      print(str(e))
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
    print("Found",len(urls),"URLs in e-mail",emailid)
    if len(urls) > 0:
        result = set(urls) # remove duplicates by changing from list to set as we're looking at both 'text/plain' and 'text/html'
    else:
        result = {}
    
    return result

def get_unseen_emails(imapserver:str=IMAPserver,username:str=IMAPuser,password:str=IMAPpassword):
    emailResults = {}
    con = connect(imapserver,username,password)
    resp, items = con.search(None, "UnSeen")
    
    items = items[0].split()
    print("Found",len(items),"unseen e-mails")

    for emailid in items:
        emailResults[emailid] = scrape_email_for_URLs(con, emailid)
    
    con.close
    return emailResults

print(get_unseen_emails())





