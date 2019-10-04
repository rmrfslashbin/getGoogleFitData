#!/usr/bin/env python3

import json
from dateutil.parser import parse
from googleapiclient.discovery import build
from auth import connect

# Google API Scopes
SCOPES = [
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.body.read"
]


def search(creds, start, end):
    googleFit = build('fitness', 'v1', credentials=creds)

    # Start/End times
    startTime = parse(start)
    endTime = parse(end)
    # Convert to nanoseconds
    startID = int(startTime.timestamp() * 1000000000)
    endID = int(endTime.timestamp() * 1000000000)

    # Go get the data!
    bpm = googleFit.users().dataSources().datasets().get(
        userId="me",
        dataSourceId="derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm",
        datasetId=f"{startID}-{endID}").execute()

    return bpm


if __name__ == '__main__':
    # Since the app is running, check the args
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
    parser.add_argument("--start", type=str, required=True, help="Start Time")
    parser.add_argument("--end", type=str, required=True, help="End Time")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=False,
        help="Ouput json file")
    args = parser.parse_args()

    # Do OAuth...
    creds = connect(SCOPES, args.google_token, args.auth_pickle)
    # Fetch data
    data = search(creds, args.start, args.end)

    # Write to output file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f)
            print(f"Wrote {len(data['point'])} points to {args.output}")
    # Otherwise, write to stdout
    else:
        print(json.dumps(data))
