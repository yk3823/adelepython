from sendemail import Email
import secrets
import databaseMain as db


class Message:

    def __init__(self,email,message):
        self.email = email
        self.message = message
        
    def getMessage(self):
        


        subject = "Test email from Python"
        message = f"""
        <html>
        <body>
            <p>Hi ADELE,<br>
            TEST FOR ME!<br>
                <a href="http://localhost:5020/emailverified/{self.email}">Click Here</a> 
            </p>
        </body>
        </html>
        """
        return {"subject":subject,"message":message}
###### Test ########
# a1 = Email("adelkenan53@gmail.com","adelekeinan@gmail.com","ukwdpyraorxbqcsr")
# a1.send_email(subject,message)

##### Test ######
# a1 = Message("yk3823@gmail.com","hekko").getMessage()
# print(a1)

