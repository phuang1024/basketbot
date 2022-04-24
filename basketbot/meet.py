from datetime import datetime
from typing import Set

DATE_PATTERN = "%m/%d %H:%M"


class Meet:
    """
    Represents one place and time to meet.
    """
    location: str
    time: datetime
    alerted: bool
    people: Set[str]
    channel: "Channel"

    def __init__(self, location: str, time: str):
        self.location = location.strip()
        self.time = datetime.strptime(time, DATE_PATTERN)
        self.time = self.time.replace(year=datetime.now().year)
        self.alerted = False
        self.people = set()

    def __repr__(self):
        return f"Meet(location=\"{self.location}\", time={self.time})"

    def __eq__(self, other):
        return self.location.lower() == other.location.lower() and self.time == other.time

    def as_str(self):
        """
        Human readable.
        """
        s = f"\"{self.location}\", \"{self.time.strftime(DATE_PATTERN)}\""
        return s
