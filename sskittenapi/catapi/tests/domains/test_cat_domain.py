from datetime import datetime, timezone
from unittest import mock

import pytest

from catapi import dto, exceptions
from catapi.domains import cat_domain
from tests import conftest

UTC = timezone.utc


@pytest.mark.parametrize(
    "new_cat, expected_cat",
    [
        (
            dto.UnsavedCat(
                name="Sammybridge Cat",
            ),
            dto.Cat(
                id=dto.CatID("000000000000000000000101"),
                name="Sammybridge Cat",
                ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            ),
        )
    ],
)
@mock.patch("catapi.models.cat_model.create_cat")
@mock.patch("catapi.libs.dates.get_utcnow")
@conftest.async_test
async def test_create_cat(
    mock_utcnow: mock.Mock,
    mock_cat_model_create_cat: mock.Mock,
    new_cat: dto.UnsavedCat,
    expected_cat: dto.Cat,
) -> None:
    mock_utcnow.return_value = datetime(2019, 1, 1, 23, 59, tzinfo=UTC)
    mock_cat_model_create_cat.return_value = expected_cat

    result = await cat_domain.create_cat(new_cat)

    assert result == expected_cat
    mock_cat_model_create_cat.assert_called_once_with(
        new_cat, now=datetime(2019, 1, 1, 23, 59, tzinfo=UTC)
    )


@pytest.mark.parametrize(
    "cat_filter",
    [
        dto.CatFilter(
            cat_id=dto.CatID("000000000000000000000101"),
            name="Sammybridge Cat",
        )
    ],
)
@mock.patch("catapi.models.cat_model.find_one")
@conftest.async_test
async def test_find_one(mock_cat_model_find_one: mock.Mock, cat_filter: dto.CatFilter) -> None:
    await cat_domain.find_one(cat_filter)

    mock_cat_model_find_one.assert_called_once_with(cat_filter=cat_filter)


@pytest.mark.parametrize(
    "cat_filter, cat_sort_params, page",
    [
        (
            dto.CatFilter(
                cat_id=dto.CatID("000000000000000000000101"),
                name="Sammybridge Cat",
            ),
            [
                dto.CatSortPredicate(key=dto.CatSortKey.id, order=dto.SortOrder.asc),
                dto.CatSortPredicate(key=dto.CatSortKey.name, order=dto.SortOrder.desc),
            ],
            dto.Page(number=2, size=30),
        )
    ],
)
@mock.patch("catapi.models.cat_model.find_many")
@conftest.async_test
async def test_find_many(
    mock_cat_model_find_many: mock.Mock,
    cat_filter: dto.CatFilter,
    cat_sort_params: dto.CatSortPredicates,
    page: dto.Page,
) -> None:
    await cat_domain.find_many(
        cat_filter=cat_filter,
        cat_sort_params=cat_sort_params,
        page=page,
    )

    mock_cat_model_find_many.assert_called_once_with(
        cat_filter=cat_filter,
        cat_sort_params=cat_sort_params,
        page=page,
    )


@mock.patch("catapi.models.cat_model.delete_cat")
@conftest.async_test
async def test_delete_cat_success(mock_cat_model_delete_cat: mock.Mock) -> None:

    cat_id = dto.CatID("000000000000000000000101")
    mock_cat_model_delete_cat.return_value = True

    actual = await cat_domain.delete_cat(cat_id)
    assert actual is True
    mock_cat_model_delete_cat.assert_called_once_with(cat_id)


@mock.patch("catapi.models.cat_model.delete_cat")
@conftest.async_test
async def test_delete_cat_error_entity_not_found(mock_cat_model_delete_cat: mock.Mock) -> None:

    cat_id = dto.CatID("000000000000000000000101")
    mock_cat_model_delete_cat.return_value = False
    with pytest.raises(exceptions.CatNotFoundError):
        await cat_domain.delete_cat(cat_id)
    mock_cat_model_delete_cat.assert_called_once_with(cat_id)


@pytest.mark.parametrize(
    "partial_update_cat, cat_id",
    [
        (
            dto.PartialUpdateCat(
                url="http://placekitten.com/200/300",
            ),
            dto.CatID("1"),
        ),
        (
            dto.PartialUpdateCat(
                url="http://placekitten.com/300/400",
            ),
            dto.CatID("2"),
        ),
    ],
)
@mock.patch("catapi.models.cat_model.partial_update_cat")
@conftest.async_test
async def test_partial_update_cat(
    mock_cat_model_partial_update_cat: mock.Mock,
    partial_update_cat: dto.PartialUpdateCat,
    cat_id: dto.CatID,
) -> None:
    excepted_cat = dto.Cat
    mock_cat_model_partial_update_cat.return_value = excepted_cat
    result = await cat_domain.partial_update_cat(partial_update_cat, cat_id)
    assert result == excepted_cat
    mock_cat_model_partial_update_cat.assert_called_once_with(partial_update_cat, cat_id)
