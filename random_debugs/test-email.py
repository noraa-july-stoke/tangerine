import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_content = "Hello, This is a simple mail"

# The mail addresses and password
sender_address = 'noraa-july-stoke@proton.me'
sender_pass = 'C4melz!!!!!'
receiver_address = 'noraa.july.stoke@gmail.com'

# Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'A test mail sent by Python. It has an attachment.'

# The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))

# Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.protonmail.com', 587)
session.starttls()
session.login(sender_address, sender_pass)
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()

print('Mail Sent')
