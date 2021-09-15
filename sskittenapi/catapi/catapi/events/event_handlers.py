import asyncio
import logging
from typing import Callable, Mapping

from catapi import dto
from catapi.domains import cat_domain
from catapi.exceptions import CatNotFoundError, EventException

logger = logging.getLogger(__name__)


def handle_ping(data: dto.JSON) -> None:
    """
    All consumers listen to `ping` event.

    Event payload schema is:

    {
        "event_id": <event correlation id>
    }
    """
    event_id = data.get("event_id")

    logger.info(f"[{event_id}] pong")


def handle_cat_created(data: dto.JSON) -> None:
    event_id = data.get("event_id")
    cat_id = data.get("cat_id")
    required_keys = {"cat_id"}

    if not all(key in data for key in required_keys):
        exception_message = (
            f"Cannot process event: missing required keys. "
            f"Got: {', '.join(data.keys())}. Expected: {', '.join(required_keys)}"
        )
        logger.exception(f"[{event_id}] {exception_message}")
        raise EventException(exception_message)

    logger.info(f"[{event_id}] Cat {cat_id} has been created")
    # TODO: Handle the async postprocessing of a created Cat here.
    
    cat_partial_update = dto.PartialUpdateCat(url=["http://placekitten.com/200/300"])
    cat_filter = dto.CatFilter(cat_id=data["cat_id"])
    print("Iam",cat_partial_update)
    loop = asyncio.get_event_loop()
    updated_cat = cat_domain.partial_update_cat(cat_partial_update, cat_filter)
    loop.run_until_complete(updated_cat)
    if not updated_cat:
        exception_message = f"Cannot find cat: {updated_cat}"
        raise CatNotFoundError(exception_message)
    return None


EVENT_HANDLERS: Mapping[str, Callable] = {
    "ping": handle_ping,
    "catapi-ping": handle_ping,
    "cat.created": handle_cat_created,
}
