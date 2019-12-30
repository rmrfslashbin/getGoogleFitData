#!/usr/bin/env python3

import json
from dateutil.parser import parse
from googleapiclient.discovery import build
from auth import connect
from lib import scopes


def search(creds, dataTypeName, dataSourceId, start, end, bucketByTime = 86400000):
    googleFit = build('fitness', 'v1', credentials=creds)

    # Start/End times
    startTime = parse(start)
    endTime = parse(end)

    # Convert to nanoseconds
    startID = int(startTime.timestamp() * 1000.0)
    endID = int(endTime.timestamp() * 1000.0)

    # Go get the data!
    data = googleFit.users().dataset().aggregate(
        userId="me",
        body={
            "aggregateBy": [{
                "dataTypeName": dataTypeName,
                "dataSourceId": dataSourceId
            }],
            "bucketByTime": { "durationMillis": bucketByTime }, # One day = 86400000
            "startTimeMillis": startID,
            "endTimeMillis": endID
        }).execute()
    return data

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

    dataGroup = parser.add_mutually_exclusive_group(required=True)
    dataGroup.add_argument("--steps", action="store_true", help="Get steps")
    dataGroup.add_argument("--cals", action="store_true", help="Get calories (kcal)")
    dataGroup.add_argument("--dist", action="store_true", help="Get distance (meters)")

    args = parser.parse_args()

    # Do OAuth...
    creds = connect(scopes, args.google_token, args.auth_pickle)

    # Set up data source
    dataTypeName = None
    dataSourceId = None
    
    if args.steps:
        dataTypeName = "com.google.step_count.delta",
        dataSourceId = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
   
    elif args.cals:
        dataTypeName = "com.google.calories.expended",
        dataSourceId = "derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended"

    elif args.dist:
        dataTypeName = "com.google.distance.delta"
        dataSourceId = "derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta"

    # Fetch data
    data = search(creds, dataTypeName, dataSourceId, args.start, args.end)


    # Write to output file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f)
            print(f"Wrote {len(data['rawdata']['points'])} points to {args.output}")
    # Otherwise, write to stdout
    else:
        print(json.dumps(data, indent=4))
