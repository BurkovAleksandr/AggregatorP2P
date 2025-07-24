import os
from dotenv import load_dotenv

load_dotenv(".env")
SESSIONS_PATH = os.getenv("SESSIONS_PATH")
