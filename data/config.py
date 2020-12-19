import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")

host = 'localhost'
