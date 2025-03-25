#!/usr/bin/env python3
from time import sleep
from json import load
from config import OUTPUT_FILE, FETCH_INTERVAL, FEEDS_FILE
from logging import basicConfig, getLogger, INFO
import requests
import xml.etree.ElementTree as ET


basicConfig(level=INFO)
logger = getLogger('rss_collector')

def parse_rss(url:str) -> list:
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Error fetching RSS feed: {response.status_code}")
        return []
    try:
        root = ET.fromstring(response.content)
        entries = []
    
        for item in root.findall('./channel/item'):
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            description = item.find('description').text if item.find('description') is not None else ''
            entries.append({'title': title, 'link': link, 'description': description})
    except Exception as e:
        logger.error(f"Error parsing RSS feed: {e}")
        logger.info(response.content)
    return entries

def fetch_rss_feeds(rss_feeds:list) -> list:
    combined_entries = []
    for feed_url in rss_feeds:
        logger.info(f"Fetching feed: {feed_url}")
        feed = parse_rss(feed_url)
        combined_entries.extend(feed)
    return combined_entries

def save_combined_feed(entries:list) -> None:
    with open(OUTPUT_FILE, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<rss version="2.0">\n')
        f.write('<channel>\n')
        for entry in entries:
            f.write('<item>\n')
            f.write(f"<title>{entry['title']}</title>\n")
            f.write(f"<link>{entry['link']}</link>\n")
            f.write(f"<description>{entry['description']}</description>\n")
            f.write('</item>\n')
        f.write('</channel>\n')
        f.write('</rss>\n')

    logger.info(f"Combined feed saved to {OUTPUT_FILE}")

def main() -> None:
    with open(FEEDS_FILE, 'r') as f:
        feeds = load(f)['feeds']

    logger.info(f"Starting RSS feed collector")
    logger.info(f"List of feeds: {feeds}")

    logger.info(f"Fetching feeds every {FETCH_INTERVAL} seconds")

    while True:
        logger.info(f"Fetching feeds")
        entries = fetch_rss_feeds(feeds)
        save_combined_feed(entries)
        sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()