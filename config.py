# config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define configuration variables
class Config:
    EMAIL_FROM = os.environ.get("EMAIL_FROM")
    GMAIL_USERNAME = os.environ.get("GMAIL_USERNAME")
    GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
