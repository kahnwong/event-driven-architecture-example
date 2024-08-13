from googleapiclient import discovery  # type: ignore


def transcribe_status(operation_name: str) -> int:
    speech_service = discovery.build("speech", "v1")
    operation = speech_service.operations().get(name=operation_name).execute()

    progress = 0
    try:
        progress = operation["metadata"]["progressPercent"]
    except Exception:
        pass

    return progress
