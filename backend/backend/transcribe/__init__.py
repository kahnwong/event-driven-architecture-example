import os

from dotenv import load_dotenv
from google.cloud.speech_v2 import SpeechClient

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
speech_client = SpeechClient()
