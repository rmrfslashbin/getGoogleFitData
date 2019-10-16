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

def clean(data):
    points = []
    for point in data["point"]:
        points.append({
            "timestamp": int(int(point["startTimeNanos"]) / 1000000),
            "value": int(point["value"][0]["fpVal"])
        })
    return {"rawdata": {"points": points}}
        
def sma(data, window):
    import pandas as pd
    df = pd.DataFrame(data)
    #df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    ma = df.value.rolling(window=window).mean().to_frame().dropna().to_dict()["value"]
    return {"sma": {"window": window, "points": [{"timestamp": i, "value": ma[i]} for i in ma]}}

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
    parser.add_argument("--sma", type=int, help="Simple moving average window (int)")

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
    data = clean(search(creds, args.start, args.end))

    # if sma...
    if args.sma:
        smaData = sma(data["rawdata"]["points"], args.sma)
        data = {**data, **smaData}


    # Write to output file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f)
            print(f"Wrote {len(data['rawdata']['points'])} points to {args.output}")
    # Otherwise, write to stdout
    else:
        print(json.dumps(data))
