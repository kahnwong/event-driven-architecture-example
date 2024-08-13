from google.cloud.speech_v2.types import cloud_speech

from backend.transcribe import PROJECT_ID
from backend.transcribe import speech_client
from backend.utils.log import init_logger

logger = init_logger(__name__)


def transcribe_request(
    request_id: str, gcs_uri: str, speech_client=speech_client, PROJECT_ID=PROJECT_ID
) -> str:
    logger.info(f"/submit - request_id: {request_id} - submit gcs_uri: {gcs_uri}")

    features = cloud_speech.RecognitionFeatures(
        enable_word_time_offsets=True,  # type: ignore
    )
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),  # type: ignore
        language_codes=["th-TH"],  # type: ignore
        model="latest_long",  # type: ignore
        features=features,  # type: ignore
    )
    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)  # type: ignore

    config_output = cloud_speech.RecognitionOutputConfig(
        inline_response_config=cloud_speech.InlineOutputConfig(),  # type: ignore
    )
    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",  # type: ignore
        config=config,  # type: ignore
        files=[file_metadata],  # type: ignore
        recognition_output_config=config_output,  # type: ignore
    )

    operation = speech_client.batch_recognize(request=request, timeout=60 * 60 * 8)

    return operation.operation.name
