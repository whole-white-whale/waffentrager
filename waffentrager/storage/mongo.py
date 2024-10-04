from typing import Optional

from bson import ObjectId

from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database

from waffentrager.event import Event
from waffentrager.storage import EventId, Storage


class MongoStorage(Storage):
    client: MongoClient
    database_name: str

    def __init__(self, host: str, port: int, database_name: str):
        self.client = MongoClient(host, port)
        self.database_name = database_name

    @property
    def database(self) -> Database:
        return self.client[self.database_name]

    def add_event(self, user_name: str, event: Event) -> EventId:
        document = event.model_dump(mode="json")
        response = self.database[user_name].insert_one(document)

        return EventId(str(response.inserted_id))

    def list_events(self, user_name: str) -> list[EventId]:
        event_ids = []

        for response in self.database[user_name].find():
            event_id = str(response["_id"])
            event_ids.append(event_id)

        return event_ids

    def get_event(self, user_name: str, event_id: EventId) -> Optional[Event]:
        response = self.database[user_name].find_one({"_id": ObjectId(event_id)})

        if response is not None:
            return Event.model_validate(response)

    def remove_event(self, user_name: str, event_id: EventId):
        self.database[user_name].delete_one({"_id": ObjectId(event_id)})
