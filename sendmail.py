import smtplib

sender = 'ashraf.asif664@gmail.com'
receivers = ['ashraf.asif663@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('gmail.com', 25)
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except:
   print "Error: unable to send email"