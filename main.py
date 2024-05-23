import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, request, url_for
from urllib.parse import urlparse
from dotenv import load_dotenv
import pyfile_web_scraping  # Ensure this is the correct import
import sentiment_analysis_youtube_comments  # Ensure this is the correct import
import pandas as pd

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.debug = True

def mailsend(emailto):
    emailfrom = os.getenv("EMAIL_FROM")
    file_to_send = ["Full Comments.csv", "Positive Comments.csv", "Negative Comments.csv"]
    username = os.getenv("GMAIL_USERNAME")
    password = os.getenv("GMAIL_PASSWORD")

    # Debug prints
    print(f"Email From: {emailfrom}")
    print(f"Username: {username}")
    print(f"Password: {password is not None}")  # Do not print the actual password

    # Check if any of the environment variables are None
    if emailfrom is None or username is None or password is None:
        raise ValueError("One or more environment variables are not set.")

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Your YouTube Comments Report"

    for f in file_to_send:
        with open(f, "r", encoding="utf-8") as fp:
            attachment = MIMEText(fp.read(), "csv", "utf-8")
        attachment.add_header("Content-Disposition", "attachment", filename=f)
        msg.attach(attachment)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(username, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap_comments():
    url = request.form.get('youtube_url')
    emailto = request.form.get('user_mail_id')

    try:
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL")
    except ValueError as e:
        return render_template("error.html", message="Invalid URL: " + str(e))

    try:
        validate_email(emailto)
    except EmailNotValidError as e:
        return render_template("error.html", message="Invalid email address: " + str(e))

    try:
        file_and_detail = pyfile_web_scraping.scrapfyt(url)
        sentiment = sentiment_analysis_youtube_comments.sepposnegcom("Full Comments.csv")
        mailsend(emailto)

        video_title, video_owner, video_comment_with_replies, video_comment_without_replies = file_and_detail[1:]
        pos_comments_csv, neg_comments_csv, video_posive_comments, video_negative_comments = sentiment
        pos_comments_csv = pd.read_csv('Positive Comments.csv')
        neg_comments_csv = pd.read_csv('Negative Comments.csv')

        after_complete_message = "Your file is ready and sent to your mail id"
        return render_template("index.html", after_complete_message=after_complete_message, title=video_title,
                               owner=video_owner, comment_w_replies=video_comment_with_replies,
                               comment_wo_replies=video_comment_without_replies,
                               positive_comment=video_posive_comments, negative_comment=video_negative_comments,
                               pos_comments_csv=[pos_comments_csv.to_html()], neg_comments_csv=[neg_comments_csv.to_html()])
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template("error.html", message="An error occurred: " + str(e))

if __name__ == "__main__":
    app.run()
