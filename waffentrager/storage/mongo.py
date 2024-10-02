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

    @property
    def event_collection(self) -> Collection:
        return self.database["events"]

    def add_event(self, event: Event) -> EventId:
        document = event.model_dump(mode="json")
        response = self.event_collection.insert_one(document)

        return str(response.inserted_id)

    def list_events(self) -> list[EventId]:
        event_ids = []

        for response in self.event_collection.find():
            event_id = str(response["_id"])
            event_ids.append(event_id)

        return event_ids

    def get_event(self, event_id: EventId) -> Optional[Event]:
        response = self.event_collection.find_one({"_id": ObjectId(event_id)})

        if response is not None:
            return Event.model_validate(response)

    def remove_event(self, event_id: EventId):
        self.event_collection.delete_one({"_id": ObjectId(event_id)})
