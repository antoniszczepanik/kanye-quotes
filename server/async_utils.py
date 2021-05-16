from __future__ import annotations
import asyncio
import concurrent.futures
import functools
import requests


def get_responses(request_number, *args, **kwargs):
    """
    Asynchronusly get request_number of responses.
    *args and **kwargs are passed to requests call.
    """
    async def make_async_get_requests(request_number, *args, **kwargs):
        with concurrent.futures.ThreadPoolExecutor(max_workers=request_number) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(
                    executor,
                    requests.get,
                    *args,
                    **kwargs
                )
                for _ in range(request_number)
            ]
            return await asyncio.gather(*futures)

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(make_async_get_requests(request_number, *args, **kwargs))

def get_unique_responses_async(target_response_number, *args, **kwargs):
    """
    Asynchronusly get responses until target_response_number of them
    are unique. Performs "rounds" of async requests. At each round tries to
    get the difference between currently unique responses and target.
    Returns only response.text values.
    """
    unique = set()
    while len(unique) < target_response_number:
        left = target_response_number - len(unique)
        result = get_responses(left, *args, **kwargs)
        [unique.add(r.text) for r in result]
    return list(unique)

def post_data_async(data_to_post: list[dict], *args, **kwargs):
    """
    Sends async POST request with each of data_to_post values as json payload.
    """
    async def make_async_post_requests(data_to_post, *args, **kwargs):
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(data_to_post)) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(
                    executor,
                    functools.partial(requests.post, *args, json=data, **kwargs)
                )
                for data in data_to_post
            ]
            return await asyncio.gather(*futures)

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(make_async_post_requests(data_to_post, *args, **kwargs))
