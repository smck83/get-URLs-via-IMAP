# get-URLs-via-IMAP
This sample python script will connect to an IMAP mailbox and collect all URL's from Unseen e-mails in the 'URLs' folder


Run this script against an IMAP mailbox.

Sample output

````
Connected sucessfully, scraping email
Found 4 unseen e-mails
Found 5 URLs in e-mail b'1'
Found 0 URLs in e-mail b'2'
Found 23 URLs in e-mail b'3'
Found 3 URLs in e-mail b'4'
{b'1': {'https://protect-eu.mimecast.com/s/abcdefg123', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd', 'https://eu-api.mimecast.com/branding/mime-sample/NOTIFICATION_LOGO_ID', 'https://static-uk.mimecast.com/mimecast/resources/images/notifications/powered-mimecast-logo-278x28.png', 'http://www.w3.org/1999/xhtml'}, b'2': {}, b'4': {'http://yahoo.com', 'https://www.news.com.au', 'https://google.com'}}

````
