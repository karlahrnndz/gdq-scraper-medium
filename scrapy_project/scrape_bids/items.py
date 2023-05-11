# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BidItem(scrapy.Item):
    name = scrapy.Field()  # Scraped from event bids table
    run = scrapy.Field()  # Scraped from event bids table
    description = scrapy.Field()  # Scraped event from bids table
    amount = scrapy.Field()  # Scraped from event bids table
    goal = scrapy.Field()  # Scraped from event bids table
    bid_id = scrapy.Field()  # Additional desired field
    is_child = scrapy.Field()  # Additional desired field
    parent_bid_id = scrapy.Field()  # Additional desired field
    event = scrapy.Field()  # Additional desired field