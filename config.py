import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL for the API
BASE_URL = "https://func-qatest-weu.azurewebsites.net"

API_KEY = os.getenv("API_KEY")
# Array of merchants from env file or default
MERCHANTS_ARRAY = os.getenv("MERCHANTS_ARRAY") or [
    "dell.com",
    "macys.com",
    "xbox.com",
    "nike.com",
    "asus.com",
    "michaelkors.com",
    "reebok.com",
    "ikea.com",
]

# Headers for API requests
HEADERS = {"apiKey": API_KEY}
