import json
import os
from typing import Any
from typing import Dict

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_API_ENDPOINT = os.getenv("BACKEND_API_ENDPOINT").strip("/")


def create_auth_headers():
    return {
        "X-API-Key": os.getenv("BACKEND_API_KEY"),
        "Content-Type": "application/json",
    }


def get_item(request_id: str) -> Dict[str, Any]:
    r = requests.get(
        url=f"{BACKEND_API_ENDPOINT}/item?request_id={request_id}",
        headers=create_auth_headers(),
    )

    return r.json()


def submit_request(request_id: str, gcs_uri: str) -> Dict[str, Any]:
    r = requests.post(
        f"{BACKEND_API_ENDPOINT}/submit",
        headers=create_auth_headers(),
        data=json.dumps({"request_id": request_id, "gcs_uri": gcs_uri}),
    )

    return r.json()


def polling(request_id: str):
    r = requests.post(
        f"{BACKEND_API_ENDPOINT}/status",
        headers=create_auth_headers(),
        data=json.dumps({"request_id": request_id}),
    )

    return r.json()


# -------- page content -------- #
st.title("Frontend")

request_id = ""
gcs_uri = ""
submit_button = False
with st.sidebar:
    with st.form(key="request"):
        request_id = st.text_input(label="Request ID", key="request_id")
        gcs_uri = st.text_input(label="GCS URI", key="gcs_uri")

        submit_button = st.form_submit_button(label="Submit")

# check whether request_id exists
if submit_button:
    try:
        item = get_item(str(request_id))
    except Exception:  # request_id does not exist
        # st.write("Request ID does not exist in database")

        submit_response = submit_request(request_id, gcs_uri)
        st.write(submit_response)
    finally:
        polling(request_id)
        item = get_item(str(request_id))
        st.write(item)
