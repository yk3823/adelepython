
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:
     # use 465 for SSL
    def __init__(self, to_addr, username, password,smtp_port =587 ,smtp_server="smtp.gmail.com"):
        self.to_addr = to_addr
        self.username = username
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        


    def send_email(self, subject, message):
        try:
            from_addr = self.username
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = self.to_addr
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'html'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.set_debuglevel(1)  # This line will print out the entire SMTP conversation to the console
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(from_addr, self.to_addr, text)
            server.quit()

        except Exception as e:
            print(f"An error occurred: {e}")
#### Test ####
# a1 = Email("adelkenan53@gmail.com","adelekeinan@gmail.com","ukwdpyraorxbqcsr")
# a1.send_email("subject","hello")

     

