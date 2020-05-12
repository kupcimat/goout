import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import Tag

sleep_time = 5
restaurant_url = "https://goout.net/cs/restaurace/la-degustation-boheme-bourgeoise/owee/"
logging.basicConfig(level=logging.DEBUG)


def normalize(string: str) -> str:
    # trim and replace non-breaking space
    return string.strip().replace("\xa0", " ")


def parse_event(event: Tag) -> dict:
    date = event.find("div", class_="timestamp").time.string
    # button is sometimes parsed as an anchor element
    status = event.find("div", class_="bottom").find(class_="btn").string
    return {"date": normalize(date), "status": normalize(status)}


def parse_events(html: str) -> list:
    tree = BeautifulSoup(html, "html.parser")
    events = tree.find_all("div", class_="eventCard")
    return [parse_event(event) for event in events]


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            html = await fetch(session, restaurant_url)
            events = parse_events(html)
            logging.info(f"component=worker action=get-events events={events}")
            await asyncio.sleep(sleep_time)


asyncio.run(main())
