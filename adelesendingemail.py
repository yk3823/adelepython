import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# set up the SMTP server
smtp_server = "smtp.gmail.com"
smtp_port = 587  # use 465 for SSL
username = "adelekeinan@gmail.com"
password = "iwuyzaacjyrgdhtk"

# set up the email content
from_addr = "adelekeinan@gmail.com"
to_addr = "adelkenan53@gmail.com"
subject = "Test email from Python"
message = """
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://localhost:5020/emailverified">Click Here</a> 
    </p>
  </body>
</html>
"""


msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject

msg.attach(MIMEText(message, 'html'))

# send the email
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # this is for security reasons, encrypts your login info
server.login(username, password)
text = msg.as_string()
server.sendmail(from_addr, to_addr, text)
server.quit()
