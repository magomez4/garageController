import imaplib
import smtplib
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import email
import time
# import RPi.GPIO as GPIO


# doorOpen = GPIO.HIGH
# doorClosed = GPIO.LOW
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

# class RelayController:
# 	signalPin = 0
# 	def __init__(self, sigPin):
# 		self.signalPin = sigPin
# 		GPIO.setup(self.signalPin, GPIO.OUT)
		
# 	def closeRelay(self):
# 		if GPIO.input(self.signalPin):
# 			#print("Relay is closed")
# 			print(" ")
# 		else:
# 			GPIO.output(self.signalPin, GPIO.HIGH)
	
# 	def openRelay(self):
# 		GPIO.output(self.signalPin, GPIO.LOW)
		
# 	def closeAndOpen(self):
# 		GPIO.output(self.signalPin, GPIO.HIGH)
# 		time.sleep(0.2)
# 		GPIO.output(self.signalPin, GPIO.LOW)

# relay = RelayController(23)

# IMAP server settings (example using example.com)
IMAP_SERVER = "imap.gmail.com"



# SMTP server settings (example using example.com)
SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 465
SMTP_PORT = 587
SMTP_USERNAME = USERNAME
SMTP_PASSWORD = PASSWORD

while True:
    # Connect to the IMAP server
    imap_server = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap_server.login(USERNAME, PASSWORD)
    imap_server.select("inbox")

    # Connect to the SMTP server
    smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)

    # Search for emails containing the keyword
    # status, email_ids = imap_server.search(None, 'BODY "message"')
    status, email_ids = imap_server.search(None, 'BODY "doorctrl:"')

    if status == "OK":
        email_ids = email_ids[0].split()
        for email_id in email_ids:
            status, email_data = imap_server.fetch(email_id, "(RFC822 FLAGS)")
            if status == "OK":
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Handle multipart message
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            # if re.search(r'\bmessage\b', body, re.IGNORECASE):
                            if re.search(r'\bopendoor\b', body, re.IGNORECASE):
                                # relay.closeAndOpen()
                                response_subject = "Re: " + msg["Subject"]
                                response_body = "Message received"
                                
                                response_msg = MIMEMultipart()
                                response_msg["Subject"] = response_subject
                                response_msg["From"] = SMTP_USERNAME
                                response_msg["To"] = msg["From"]
                                
                                text_part = MIMEText(response_body)
                                response_msg.attach(text_part)
                                
                                smtp_server.sendmail(SMTP_USERNAME, [msg["From"]], response_msg.as_string())
                                
                                print("Response sent")
                            
                                # Delete the received email
                                imap_server.store(email_id, '+FLAGS', '\\Deleted')
                                imap_server.expunge()
                                print("Received email deleted")
                            break  # Only process the first text/plain part
            else:
                print("Error fetching email data")
    else:
        print("Error searching for emails")

    # Logout and close the connections
    imap_server.logout()
    smtp_server.quit()
    time.sleep(60)