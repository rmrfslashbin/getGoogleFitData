#!/usr/bin/env python3

import json
from dateutil.parser import parse
from googleapiclient.discovery import build
from auth import connect

SCOPES = [
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.body.read"
]


def search(creds):
    googleFit = build('fitness', 'v1', credentials=creds)

    # Get the user
    me = googleFit.users().dataSources().list(userId="me").execute()
    return me


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Get Fit data")
    parser.add_argument(
        "--google-token",
        type=str,
        default="./token-for-google.json",
        help="Path to google OAuth token (default= './token-for-google.json'")
    parser.add_argument(
        "--auth-pickle",
        type=str,
        default="./token.pickle",
        help="Path to pickle containing google OAuth session (default= './token.pickle'")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=False,
        help="Ouput json file")
    args = parser.parse_args()

    creds = connect(SCOPES, args.google_token, args.auth_pickle)
    data = search(creds)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f)
            print(f"Wrote data to {args.output}")
    else:
        print(json.dumps(data))
