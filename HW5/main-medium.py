import asyncio
import time

import aiofiles
import requests
from bs4 import BeautifulSoup

site_url = "https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=3&region=2&room1=1&room2=1"


def get_link_from_flat_card(flat_card):
    link_tag_name = "LinkArea"
    return flat_card.find_next(attrs={"data-name": link_tag_name}).a.get("href")


def get_flat_cards_from_soup(soup):
    return soup.find_all("article", attrs={"data-name": "CardComponent"})


def get_card_content(card):
    descr_tag_name = "Description"
    return card.find_next(attrs={"data-name": descr_tag_name}).text


async def save_card_to_file(card):
    card_link = get_link_from_flat_card(card)
    name = card_link.split("/")[-2]
    content = get_card_content(card)
    f_card = await aiofiles.open(name + ".txt", mode="w")
    await f_card.write(content)
    await f_card.close()


async def do_scrapping_async(flats):
    tasks = []

    for i in range(len(flats)):
        tasks.append(save_card_to_file(flats[i]))

    await asyncio.gather(*tasks)


def do_scrapping():
    headers = {
        'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 '
            'Safari/537.36 Edge/18.19582 '
    }
    response = requests.get(site_url, headers=headers)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    flats = soup.find_all("article", attrs={"data-name": "CardComponent"})

    asyncio.run(do_scrapping_async(flats))


if __name__ == '__main__':

    iter_count = 0
    while True and iter_count < 10:
        iter_count += 1
        do_scrapping()
        print(f"Done scrapping iter {iter_count}")
        time.sleep(60)
