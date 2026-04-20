import os
from dotenv import load_dotenv

load_dotenv()

ASTRA_DB_TOKEN = os.getenv('ASTRA_DB_TOKEN')
ASTRA_DB_ID = os.getenv('ASTRA_DB_ID')
HF_API_KEY = os.getenv('HF_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')