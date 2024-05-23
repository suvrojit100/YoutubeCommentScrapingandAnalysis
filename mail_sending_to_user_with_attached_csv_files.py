import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.text import MIMEText

def mailsend(emailto):
    emailfrom = "ytscrapercommentps@gmail.com"
    fileToSend = ["Full Comments.csv", "Positive Comments.csv", "Negative Comments.csv"]
    username = "ytscrapercommentps@gmail.com"
    password = "PASSWORD"  # Update with your actual password

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Hi, your YouTube comments excel file is here - Youtube Comment Scraper"

    for f in fileToSend:
        fp = open(f, "rb")
        attachment = MIMEText(fp.read(), "csv", "utf-8")
        fp.close()
        attachment.add_header("Content-Disposition", "attachment", filename=f)
        msg.attach(attachment)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(username, password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
