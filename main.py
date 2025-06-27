import datetime as dt
import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import timezone

scopes = ["https://www.googleapis.com/auth/calendar"]


def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", scopes
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        events = {
            "summary": "Test Event",
            "location": "123 Test St, Test City, TC 12345",
            "description": "This is a test event created by the Google Calendar API.",
            "colorId": "1",
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 30},
                ],
            },
            "start": {
                "dateTime": dt.datetime.now(timezone.utc).isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": (dt.datetime.now(timezone.utc) + dt.timedelta(hours=1)).isoformat(),
                "timeZone": "UTC",
            },
        }

        event = service.events().insert(calendarId="primary", body=events).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()


# This script requires the Google Calendar API to be enabled and the credentials.json file to be present
# in the same directory. The first time you run it, it will prompt you to authorize access to your Google Calendar.
# After authorization, it will save the credentials in token.json for future use.
# Make sure to install the required libraries using:
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# You can find the credentials.json file by creating a project in the Google Cloud Console and enabling the Calendar API.
# Follow the instructions here: https://developers.google.com/calendar/quickstart
