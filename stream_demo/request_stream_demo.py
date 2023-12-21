import asyncio
import httpx
import json

url = "http://localhost:8009/stream-pipe"

params = {
    "stream_url": "https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web",
    "source_language": "de",
    "target_language": "en"
}

headers = {
    "Content-Type": "application/json"
}

async def process_stream_response(response):
    async for chunk in response.aiter_bytes():
        if chunk:
            try:
                data = json.loads(chunk.decode("utf-8"))
                print(data)
            except json.JSONDecodeError as json_err:
                print(f"Error decoding JSON: {json_err}")

async def make_httpx_request():
    timeout = httpx.Timeout(60.0)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        if response.is_error:
            print(f"HTTP error: {response.status_code}")
            return
        await process_stream_response(response)

# Create an event loop and run the coroutine
loop = asyncio.get_event_loop()
loop.run_until_complete(make_httpx_request())