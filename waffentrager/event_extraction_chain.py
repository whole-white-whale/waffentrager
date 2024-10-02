from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

from waffentrager.event import EventList


PROMPT_TEMPLATE = """
You are an AI assistant.
Your task is to extract information about events from a message.

{format_instructions}

The message:

{message}

The message was received on {date}, at {time}.
"""


def create_event_extraction_chain(chat_model: BaseChatModel) -> Runnable:
    output_parser = PydanticOutputParser(pydantic_object=EventList)

    prompt_partial_variables = {
        "format_instructions": output_parser.get_format_instructions(),
    }

    prompt = PromptTemplate.from_template(
        PROMPT_TEMPLATE, partial_variables=prompt_partial_variables
    )

    return prompt | (chat_model | output_parser).with_retry()
