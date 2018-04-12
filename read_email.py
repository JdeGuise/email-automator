
from sys import path
path.append('Config/')
import config

import smtplib
import time
import imaplib
import email

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

mail = imaplib.IMAP4_SSL("imap.gmail.com")

# logging into gmail inbox
def mailbox_login():
    FROM_EMAIL  = config.gmail_creds['user']
    FROM_PWD    = config.gmail_creds['pwd']

    mail.login(FROM_EMAIL, FROM_PWD)

# logic for parsing mailbox in display_mailbox_names
def parse_mailbox(data):
    flags, b, c = data.partition(' ')
    separator, b, name = c.partition(' ')

    return (flags, separator.replace('"', ''), name.replace('"', ''))

# parsing and displaying mailbox names
def display_mailbox_names():
    resp, data = mail.list('""', '*')
    mailbox_names = set()

    if resp == 'OK':
        for mbox in data:
            flags, separator, name = parse_mailbox(bytes.decode(mbox))
            mailbox_names.add(name)

    loop_printer(mailbox_names)

# generic looping printer
def loop_printer(what_to_loop_over):
    for i in what_to_loop_over:
        print i

# select mailbox and get id_list of emails in that mailbox
def init_mailbox(mailbox_name):
    mail.select(mailbox_name)

    typ, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()

    return id_list

# logic for parsing emails out of raw 'from' data
def parse_emails(msgs):
    recruiter_emails = set()
    for i in msgs:
        found_lt = False
        email_address = ""
        for j in range(0, len(i)):
            if i[j] == "<":
                found_lt = True
                continue;

            if found_lt:
                if i[j] == ">":
                    recruiter_emails.add(email_address)
                    continue;
                else:
                    email_address = email_address + i[j]
    return recruiter_emails

# 'main'
def read_gmail():
    msgs = set()

    try:
        mailbox_login()
        display_mailbox_names()

        mailbox_name = raw_input("\nSelect mailbox from the above list: ")
        id_list = init_mailbox(mailbox_name)
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        print("Looping over emails in mailbox '" + mailbox_name + "'")
        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msgs.add(
                        email.message_from_string(response_part[1])['from']
                    )
        print("Done looping over emails.\n")

        print("Stripping emails from email records...")
        recruiter_emails = parse_emails(msgs)
        print("Done stripping emails from email records.\n")

        print("Listing emails stripped from email records: ")
        loop_printer(recruiter_emails)
        print("Done listing email addresses from mailbox '" + mailbox_name + "'")
        # email_subject = msg['subject']
        # email_from = msg['from'
    except Exception, e:
        print str(e)
        print 'Exiting.'

if __name__ == '__main__':
    read_gmail()