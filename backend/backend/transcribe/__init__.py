import os

from dotenv import load_dotenv
from google.cloud.speech_v2 import SpeechClient
from googleapiclient import discovery  # type: ignore

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

speech_client = SpeechClient()
speech_service = discovery.build("speech", "v1")
