import datetime

from typing import Optional

from pydantic import BaseModel, Field


class Event(BaseModel):
    name: str = Field(description="A short and descriptive name of the event")

    description: Optional[str] = Field(
        default=None, description="A full and detailed description of the event"
    )

    date: datetime.date = Field(description="A date of the event")

    time: Optional[datetime.time] = Field(
        default=None, description="A time of the event"
    )

    location: Optional[str] = Field(default=None, description="A location of the event")


class EventList(BaseModel):
    events: list[Event] = Field(description="A list of the events")
