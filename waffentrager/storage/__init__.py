import abc

from typing import NewType, Optional

from waffentrager.event import Event


EventId = NewType("EventId", str)


class Storage(abc.ABC):
    @abc.abstractmethod
    def list_users(self) -> list[str]:
        pass

    @abc.abstractmethod
    def add_event(self, user_name: str, event: Event) -> EventId:
        pass

    @abc.abstractmethod
    def list_events(self, user_name: str) -> list[EventId]:
        pass

    @abc.abstractmethod
    def get_event(self, user_name: str, event_id: EventId) -> Optional[Event]:
        pass

    @abc.abstractmethod
    def remove_event(self, user_name: str, event_id: EventId):
        pass
