from __future__ import annotations

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]


def get_authenticated_service():
    client_secret_path = os.getenv("YOUTUBE_CLIENT_SECRET_PATH")
    token_path = os.getenv("YOUTUBE_TOKEN_PATH")

    if not client_secret_path:
        raise EnvironmentError("YOUTUBE_CLIENT_SECRET_PATH is required")
    if not token_path:
        raise EnvironmentError("YOUTUBE_TOKEN_PATH is required")

    client_secret_file = Path(client_secret_path).expanduser().resolve()
    token_file = Path(token_path).expanduser().resolve()

    if not client_secret_file.exists():
        raise FileNotFoundError(f"Client secret file not found: {client_secret_file}")

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secret_file), SCOPES
        )
        creds = flow.run_local_server(port=0)

    token_file.parent.mkdir(parents=True, exist_ok=True)
    token_file.write_text(creds.to_json(), encoding="utf-8")

    return build("youtube", "v3", credentials=creds)
