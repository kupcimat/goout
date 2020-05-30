import os
from typing import Tuple

import aiohttp
import pytest


@pytest.mark.asyncio
async def test_basic_workflow():
    # get upload url
    status, json = await post_json("/api/files")
    assert status == 201
    assert "id" in json["file"]
    assert "uploadUrl" in json["file"]
    assert "uploadCurl" in json["file"]

    # upload file
    curl_cmd = json["file"]["uploadCurl"].replace("my-file", "test/test.txt")
    assert os.system(curl_cmd) == 0

    # create task
    file_id = json["file"]["id"]
    status, json = await post_json(f"/api/files/{file_id}/tasks")
    assert status == 201
    assert "id" in json["task"]

    # get task result
    task_id = json["task"]["id"]
    status, json = await get_json(f"/api/files/{file_id}/tasks/{task_id}")
    assert status == 200
    assert "id" in json["task"]
    assert "result" in json["task"]
    # TODO download result


async def get(uri: str) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get(localhost(uri)) as response:
            await response.read()
            return response


async def get_json(uri: str) -> Tuple[int, dict]:
    response = await get(uri)
    return response.status, await response.json()


async def post(uri: str) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.post(localhost(uri)) as response:
            await response.read()
            return response


async def post_json(uri: str) -> Tuple[int, dict]:
    response = await post(uri)
    return response.status, await response.json()


def localhost(uri: str) -> str:
    return f"http://localhost:8080{uri}"
