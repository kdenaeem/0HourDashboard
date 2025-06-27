# server.py
from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server
mcp = FastMCP("AI Sticky Notes")

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")


def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")


@mcp.tool()
def add_notes(message: str):
    """
    Append a new note to the sticky notes file.

    Args:
        message (str): The note content to be added

    Returns:
        str: Confirmation message indicating the note was saved
    """
    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note added successfully."


@mcp.tool()
def read_notes():
    """
    Read all notes from the sticky notes file.

    Returns:
        str: The content of the sticky notes file
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        notes = f.read()
    return notes if notes else "No notes found."


@mcp.resource("notes://latest")
def get_latest_notes():
    """
    Get the latest notes from the sticky notes file.

    Returns:
        str: The content of the sticky notes file
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1] if lines else ["No notes found."]


@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt for summarizing the notes.
    Returns:
        str: A prompt asking to summarize the notes
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        notes = f.read().strip()

    if not notes:
        return "No notes found"
    return f"Summarize the following notes:\n{notes}"
