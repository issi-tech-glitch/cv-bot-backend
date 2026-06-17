import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('GOOGLE_API_KEY'), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
CV_PATH = os.environ.get("CV_PATH", "cv/cv.pdf")
MODEL = "gemini-2.5-flash"
MAX_ROUNDS = 5
NAME = "Clarissa"
NAME_ASSISTANT = "Pia"

N8N_WEBHOOK_URL = os.environ["N8N_WEBHOOK_URL"]
N8N_WEBHOOK_SECRET = os.environ["N8N_WEBHOOK_SECRET"]
