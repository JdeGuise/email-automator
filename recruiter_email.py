from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPRecipientsRefused

from Config import config
from Config import recruiterconfig

import smtplib
import getpass
import os
import sys

def prompt_for_details():
	email_details = dict()

	to_email = input('Inbound email address: ')
	subject = input('Subject: ')
	typeOfEmail = input('Email type? (recruiter, other): ')

	email_details['To'] = to_email
	email_details['Subject'] = subject
	email_details['Type'] = typeOfEmail

	return email_details

# Assumption: from_email is same as gmail login
def send_email(to_email, subject, from_email=None, password=None, message='None', signature=None):

	msg = MIMEMultipart()

	msg['From'] = from_email
	msg['To'] = to_email
	msg['Subject'] = subject

	message = message + "\n\n" + signature
	msg.attach(MIMEText(message))

	mailserver = smtplib.SMTP('smtp.gmail.com' ,587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()

	try:
		mailserver.login(from_email, password)
		mailserver.sendmail(from_email, to_email, msg.as_string())
	except smtplib.SMTPRecipientsRefused:
		print('\nInvalid Inbound Emails. Exiting.')
		sys.exit()
	finally:
		mailserver.quit()

if __name__ == '__main__':
	email_details = prompt_for_details()
	send_email(
		from_email = config.gmail_creds['user'],
		to_email = email_details['To'],
		subject = email_details['Subject'],
		message = recruiterconfig.recruiter_config['rc_msg'],
		password = config.gmail_creds['pwd'],
		signature = config.gmail_creds['signature']
	)
