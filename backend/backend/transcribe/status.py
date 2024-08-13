from backend.transcribe import speech_service


def transcribe_status(operation_name: str, speech_service=speech_service) -> int:
    operation = speech_service.operations().get(name=operation_name).execute()

    progress = 0
    try:
        progress = operation["metadata"]["progressPercent"]
    except Exception:
        pass

    return progress
