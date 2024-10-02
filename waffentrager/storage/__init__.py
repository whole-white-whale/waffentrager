import abc

from typing import Optional

from waffentrager.event import Event


type EventId = str


class Storage(abc.ABC):
    @abc.abstractmethod
    def add_event(self, event: Event) -> EventId:
        pass

    @abc.abstractmethod
    def list_events(self) -> list[EventId]:
        pass

    @abc.abstractmethod
    def get_event(self, event_id: EventId) -> Optional[Event]:
        pass

    @abc.abstractmethod
    def remove_event(self, event_id: EventId):
        pass
