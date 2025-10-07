import asyncio

import aiohttp
from aiohttp import ClientSession

from get_matrix.exceptions import (
    MatrixConnectionError,
    MatrixContentTypeError,
    MatrixDownloadError,
    MatrixInvalidUrlError,
    MatrixServerError,
    MatrixTimeoutError,
)

EXCEPTION_MAP = {
    aiohttp.InvalidURL: MatrixInvalidUrlError,
    asyncio.TimeoutError: MatrixTimeoutError,
    aiohttp.ClientConnectorError: MatrixConnectionError,
    aiohttp.ContentTypeError: MatrixContentTypeError,
    aiohttp.ClientResponseError: MatrixServerError,
}


def parse_matrix_string(matrix_string: str) -> list[list[int]]:
    matrix_list = []
    for line in matrix_string.splitlines()[1::2]:  # skip borders
        # skip empty cells
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        matrix_row = [int(cell) for cell in cells]
        matrix_list.append(matrix_row)
    return matrix_list


def get_snail_ccw_path(matrix: list[list[int]]) -> list[int]:
    result = []

    while matrix:
        # rotate matrix clockwise
        matrix = [list(row)[::-1] for row in list(zip(*matrix))]
        # pop reversed first row for a counter-clockwise path
        result.extend(matrix.pop(0)[::-1])

    return result


async def get_matrix(url: str) -> list[int]:
    try:
        async with ClientSession() as session:
            async with session.get(url=url) as response:
                response.raise_for_status()
                matrix_string = await response.text()
        parsed_matrix = parse_matrix_string(matrix_string)
        return get_snail_ccw_path(parsed_matrix)
    except (EXCEPTION_MAP.keys()) as exc:
        raise EXCEPTION_MAP[type(exc)](str(exc))
    except Exception as exc:
        raise MatrixDownloadError(f"Unexpected error: {str(exc)}")
