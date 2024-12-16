import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")
DB_DNS = os.getenv("DB_DSN")
ADMIN_ID = os.getenv("ADMIN_ID")

SUBSCRIPTION_CHANNEL_ID = os.getenv('SUBSCRIPTION_CHANNEL_ID')
