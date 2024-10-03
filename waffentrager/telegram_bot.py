import datetime
import logging
import os

from logging.config import dictConfig
from typing import cast

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from confuse import Configuration
from langchain_ollama.chat_models import ChatOllama

from waffentrager import Waffentrager
from waffentrager.event import Event
from waffentrager.storage import EventId
from waffentrager.storage.mongo import MongoStorage


configuration = Configuration("waffentrager")
telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]

dictConfig(config=cast(dict, configuration["logging"].get(dict)))

chat_model = ChatOllama(
    model=cast(str, configuration["chat_model"]["ollama"]["model_name"].get(str))
)

storage = MongoStorage(
    host=cast(str, configuration["storage"]["mongo"]["host"].get(str)),
    port=cast(int, configuration["storage"]["mongo"]["port"].get(int)),
    database_name=cast(
        str, configuration["storage"]["mongo"]["database_name"].get(str)
    ),
)

waffentrager = Waffentrager(chat_model, storage)
dispatcher = Dispatcher()


@dispatcher.message(Command("list"))
async def list_events(message: Message):
    logging.info("Listing events")

    result = waffentrager.list_events()

    for event_id, event in result.items():
        await answer_event(message, event_id, event)


@dispatcher.message()
async def add_events_from_message(message: Message):
    if message.text is None:
        return

    logging.info("Adding events from a message: %s", message.text)

    now = datetime.datetime.now()

    result = waffentrager.add_events_from_message(
        message=message.text, date=now.date(), time=now.time()
    )

    for event_id, event in result.items():
        await answer_event(message, event_id, event)


@dispatcher.callback_query()
async def remove_event(query: CallbackQuery):
    event_id = query.data

    if event_id is None:
        return

    logging.info("Removing an event: %s", event_id)

    waffentrager.remove_event(event_id)

    await query.answer("The event has been removed.")


async def answer_event(message: Message, event_id: EventId, event: Event):
    inline_keyboard_button = InlineKeyboardButton(text="Remove", callback_data=event_id)

    inline_keyboard = [
        [inline_keyboard_button],
    ]

    inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    text = format_event(event)

    await message.answer(text, reply_markup=inline_keyboard_markup)


def format_event(event: Event) -> str:
    result = event.date.strftime("%Y-%m-%d")

    if event.time is not None:
        result += " " + event.time.strftime("%H:%M")

    result += " " + event.name

    if event.location is not None:
        result += "\n" + event.location

    if event.description is not None:
        result += "\n\n" + event.description

    return result


async def main():
    bot = Bot(token=telegram_bot_token)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
