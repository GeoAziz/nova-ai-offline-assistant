"""
Example Calendar Plugin for Nova
"""
import os
from datetime import datetime
try:
    import icalendar
except ImportError:
    icalendar = None

def run(context):
    ics_path = os.path.expanduser("~/calendar.ics")
    if icalendar and os.path.exists(ics_path):
        try:
            with open(ics_path, "rb") as f:
                cal = icalendar.Calendar.from_ical(f.read())
            now = datetime.now()
            next_event = None
            for component in cal.walk():
                if component.name == "VEVENT":
                    dtstart = component.get("dtstart").dt
                    if isinstance(dtstart, datetime) and dtstart > now:
                        summary = component.get("summary")
                        next_event = f"{summary} at {dtstart.strftime('%Y-%m-%d %H:%M')}"
                        break
            if next_event:
                return f"Next event: {next_event}"
            else:
                return "No upcoming events found."
        except Exception as e:
            return f"Calendar error: {e}"
    else:
        return "Calendar integration not available. Install 'icalendar' and add ~/calendar.ics."
