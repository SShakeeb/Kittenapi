from catapi import dto
from catapi.events.event_handlers import handle_cat_created


def test_handle_cat_created() -> None:
    data: dto.JSON = {
        "cat_id": "000000000000000000000101",
        "partial_update_cat": {"url": "http://placekitten.com/200/300"},
    }

    handle_cat_created(data)
