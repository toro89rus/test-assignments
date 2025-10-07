import asyncio  # noqa: F401

import pytest
from aioresponses import aioresponses

from matrix import (
    get_matrix,
    get_snail_ccw_path,
    parse_matrix_string,
)

MOKE_URL = "https://example.com/matrix.txt"

PARSED_MATRIX = [
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 100, 110, 120],
    [130, 140, 150, 160],
]

TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]


@pytest.fixture
def matrix_string():
    with open("tests/get_matrix/fixtures/matrix.txt", "r") as file:
        return file.read()


def test_parse_matrix_string(matrix_string):
    assert parse_matrix_string(matrix_string) == PARSED_MATRIX


def test_get_snail_ccw_path():
    assert get_snail_ccw_path([]) == []
    assert get_snail_ccw_path([[1]]) == [1]
    assert get_snail_ccw_path([[1, 2]]) == [1, 2]
    assert get_snail_ccw_path([[1], [2]]) == [1, 2]
    assert get_snail_ccw_path([[1, 2], [3, 4]]) == [1, 3, 4, 2]
    assert get_snail_ccw_path(PARSED_MATRIX) == TRAVERSAL


@pytest.mark.asyncio
async def test_get_matrix_mocked(matrix_string):
    with aioresponses() as mocked:
        mocked.get(MOKE_URL, status=200, body=matrix_string)
        result = await get_matrix(MOKE_URL)

    assert result == TRAVERSAL
