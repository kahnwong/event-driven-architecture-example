import os

from dotenv import load_dotenv
from google.cloud.speech_v2 import SpeechClient
from googleapiclient import discovery  # type: ignore

from backend.utils.log import init_logger

load_dotenv()

logger = init_logger(__name__)
speech_service = discovery.build("speech", "v1")

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
speech_client = SpeechClient()


def transcribe_status(operation_name: str) -> int:
    operation = speech_service.operations().get(name=operation_name).execute()

    progress = 0
    try:
        progress = operation["metadata"]["progressPercent"]
    except Exception:
        pass

    return progress
