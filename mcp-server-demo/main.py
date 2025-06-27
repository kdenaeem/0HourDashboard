import datetime as dt
import os.path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import timezone, timedelta

from mcp.server.fastmcp import FastMCP

# Scopes for Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Initialize FastMCP server
mcp = FastMCP("google-calendar-mcp")

# Global calendar service
calendar_service = None


def initialize_calendar_service():
    """Initialize Google Calendar service with authentication"""
    global calendar_service

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    calendar_service = build("calendar", "v3", credentials=creds)


# Initialize service when module loads
initialize_calendar_service()


@mcp.tool()
def create_calendar_event(
    summary: str,
    description: str = "",
    location: str = "",
    start_datetime: str = "",
    end_datetime: str = "",
    duration_hours: int = 1,
) -> str:
    """Create a new calendar event

    Args:
        summary: Event title/summary
        description: Event description
        location: Event location
        start_datetime: Start datetime in ISO format (optional)
        end_datetime: End datetime in ISO format (optional)
        duration_hours: Duration in hours (default: 1)

    Returns:
        JSON string with result
    """
    try:
        # Handle datetime parsing
        if start_datetime:
            start_dt = dt.datetime.fromisoformat(
                start_datetime.replace("Z", "+00:00")
            )
        else:
            start_dt = dt.datetime.now(timezone.utc)

        if end_datetime:
            end_dt = dt.datetime.fromisoformat(
                end_datetime.replace("Z", "+00:00")
            )
        else:
            end_dt = start_dt + timedelta(hours=duration_hours)

        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "UTC",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 30},
                ],
            },
        }

        result = (
            calendar_service.events()
            .insert(calendarId="primary", body=event)
            .execute()
        )
        return f"✅ Event '{summary}' created successfully!\n📅 Event ID: {result.get('id')}\n🔗 Link: {result.get('htmlLink')}"

    except HttpError as error:
        return f"❌ Google Calendar API error: {error}"
    except Exception as error:
        return f"❌ Error creating event: {error}"


@mcp.tool()
def list_calendar_events(max_results: int = 10, days_ahead: int = 7) -> str:
    """List upcoming calendar events

    Args:
        max_results: Maximum number of events to return (default: 10)
        days_ahead: Number of days ahead to look (default: 7)

    Returns:
        Formatted list of upcoming events
    """
    try:
        now = dt.datetime.now(timezone.utc)
        end_time = now + timedelta(days=days_ahead)

        events_result = (
            calendar_service.events()
            .list(
                calendarId="primary",
                timeMin=now.isoformat(),
                timeMax=end_time.isoformat(),
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            return f"📅 No upcoming events found in the next {days_ahead} days."

        result = f"📅 **Upcoming Events ({len(events)} found):**\n\n"

        for event in events:
            summary = event.get("summary", "No title")
            start = event["start"].get("dateTime", event["start"].get("date"))
            location = event.get("location", "")
            description = event.get("description", "")

            # Parse and format the datetime
            if "T" in start:
                event_dt = dt.datetime.fromisoformat(
                    start.replace("Z", "+00:00")
                )
                formatted_time = event_dt.strftime("%a, %B %d at %I:%M %p")
            else:
                # All-day event
                event_dt = dt.datetime.fromisoformat(start + "T00:00:00+00:00")
                formatted_time = event_dt.strftime("%a, %B %d (All day)")

            result += f"🎯 **{summary}**\n"
            result += f"⏰ {formatted_time}\n"
            if location:
                result += f"📍 {location}\n"
            if description:
                result += f"📝 {description[:100]}{'...' if len(description) > 100 else ''}\n"
            result += f"🆔 ID: {event['id']}\n\n"

        return result

    except HttpError as error:
        return f"❌ Google Calendar API error: {error}"
    except Exception as error:
        return f"❌ Error listing events: {error}"


@mcp.tool()
def delete_calendar_event(event_id: str) -> str:
    """Delete a calendar event

    Args:
        event_id: ID of the event to delete

    Returns:
        Confirmation message
    """
    try:
        calendar_service.events().delete(
            calendarId="primary", eventId=event_id
        ).execute()
        return f"✅ Event {event_id} deleted successfully!"
    except HttpError as error:
        return f"❌ Google Calendar API error: {error}"
    except Exception as error:
        return f"❌ Error deleting event: {error}"


@mcp.tool()
def update_calendar_event(
    event_id: str,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    start_datetime: Optional[str] = None,
    end_datetime: Optional[str] = None,
) -> str:
    """Update an existing calendar event

    Args:
        event_id: ID of the event to update
        summary: New event title/summary
        description: New event description
        location: New event location
        start_datetime: New start datetime in ISO format
        end_datetime: New end datetime in ISO format

    Returns:
        Confirmation message
    """
    try:
        # Get the existing event
        event = (
            calendar_service.events()
            .get(calendarId="primary", eventId=event_id)
            .execute()
        )

        # Update only provided fields
        if summary is not None:
            event["summary"] = summary
        if description is not None:
            event["description"] = description
        if location is not None:
            event["location"] = location
        if start_datetime is not None:
            start_dt = dt.datetime.fromisoformat(
                start_datetime.replace("Z", "+00:00")
            )
            event["start"]["dateTime"] = start_dt.isoformat()
        if end_datetime is not None:
            end_dt = dt.datetime.fromisoformat(
                end_datetime.replace("Z", "+00:00")
            )
            event["end"]["dateTime"] = end_dt.isoformat()

        updated_event = (
            calendar_service.events()
            .update(calendarId="primary", eventId=event_id, body=event)
            .execute()
        )

        return (
            f"✅ Event '{event.get('summary', event_id)}' updated successfully!"
        )

    except HttpError as error:
        return f"❌ Google Calendar API error: {error}"
    except Exception as error:
        return f"❌ Error updating event: {error}"
