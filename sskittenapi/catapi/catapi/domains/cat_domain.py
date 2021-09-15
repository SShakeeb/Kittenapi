import logging
from typing import Optional

from catapi import dto, exceptions
from catapi.libs import dates
from catapi.models import cat_model

logger = logging.getLogger(__name__)


async def create_cat(new_cat: dto.UnsavedCat) -> dto.Cat:
    now = dates.get_utcnow()
    return await cat_model.create_cat(new_cat, now=now)


async def find_one(cat_filter: dto.CatFilter) -> Optional[dto.Cat]:
    return await cat_model.find_one(cat_filter=cat_filter)


async def find_many(
    cat_filter: Optional[dto.CatFilter] = None,
    cat_sort_params: Optional[dto.CatSortPredicates] = None,
    page: Optional[dto.Page] = None,
) -> dto.PagedResult[dto.CatSummary]:
    results = await cat_model.find_many(
        cat_filter=cat_filter,
        cat_sort_params=cat_sort_params,
        page=page,
    )
    return results


async def delete_cat(cat_id: dto.CatID) -> bool:
    deleted = await cat_model.delete_cat(cat_id)
    if not deleted:
        raise exceptions.CatNotFoundError(f"Cat {cat_id} does not exists.")
    return deleted


async def partial_update_cat(
    partial_update_cat: dto.PartialUpdateCat, cat_id: dto.CatID
) -> Optional[dto.Cat]:
    cat = await cat_model.partial_update_cat(
        partial_update_cat,
        cat_id,
    )
    return cat
