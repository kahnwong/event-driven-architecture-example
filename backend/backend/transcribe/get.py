import pythainlp  # type: ignore

from backend.transcribe import speech_service


def remove_stopwords(text: str) -> str:
    stopwords = [
        "ครับ",
        "คะ",
        "คับ",
        "ค่ะ",
        "จีะ",
        "จ่ะ",
        "นะ",
        "นะคะ",
        "นะคับ",
        "นะค่ะ",
        "นะจีะ",
        "นี่",
        "หา",
        "หืม",
        "หือ",
        "ห๊ะ",
        "อืม",
        "อุ้ย",
        "อ่อ",
        "อ่ะ",
        "อ่า",
        "อ้อ",
        "อ๊ะ",
        "อ๋อ",
        "ฮะ",
        "เนอะ",
        "เนาะ",
        "เนี่ย",
        "เนี้ย",
        "เออ",
        "เอ่อ",
        "โอย",
    ]
    words = pythainlp.word_tokenize(text)
    filtered_words = [word for word in words if word not in stopwords]
    filtered_text = "".join(filtered_words)

    return filtered_text


def transcribe_to_text(
    operation_name: str, gcs_uri: str, speech_service=speech_service
) -> str:
    operation = speech_service.operations().get(name=operation_name).execute()

    # extract response
    response = operation["response"]  # raw response

    text = ""
    for i in response["results"][gcs_uri]["transcript"]["results"]:
        try:
            text = i["alternatives"][0]["transcript"]
            text = remove_stopwords(text)
        except Exception:
            pass

    return text
