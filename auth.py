import os.path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def connect(scopes, jsonToken, sessionPickle):
    creds = None
    # The file pickle stores the user's access and refresh tokens
    if os.path.exists(sessionPickle):
        with open(sessionPickle, 'rb') as token:
            try:
                creds = pickle.load(token)
            except:
                creds = None
    # If valid credentials are  available, start OAuth session
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                jsonToken, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(sessionPickle, 'wb') as token:
            pickle.dump(creds, token)

    return creds
