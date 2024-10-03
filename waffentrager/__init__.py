import datetime

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable

from waffentrager.event import Event
from waffentrager.event_extraction_chain import create_event_extraction_chain
from waffentrager.storage import EventId, Storage


class Waffentrager:
    event_extraction_chain: Runnable
    storage: Storage

    def __init__(self, chat_model: BaseChatModel, storage: Storage):
        self.event_extraction_chain = create_event_extraction_chain(chat_model)
        self.storage = storage

    def add_events_from_message(
        self, message: str, date: datetime.date, time: datetime.time
    ) -> dict[EventId, Event]:
        result = {}

        document = {
            "message": message,
            "date": date,
            "time": time,
        }

        event_list = self.event_extraction_chain.invoke(document)

        if event_list:
            for event in event_list.events:
                event_id = self.storage.add_event(event)
                result[event_id] = event

        return result

    def list_events(self) -> dict[EventId, Event]:
        result = {}

        for event_id in self.storage.list_events():
            event = self.storage.get_event(event_id)
            result[event_id] = event

        return result

    def remove_event(self, event_id: EventId):
        self.storage.remove_event(event_id)
