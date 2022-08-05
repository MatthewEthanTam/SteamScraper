# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class GameItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    href = scrapy.Field()

class InGameItem(scrapy.Item):
    name = scrapy.Field()
    tags = scrapy.Field()
    genre = scrapy.Field()
    developer = scrapy.Field()
    publisher = scrapy.Field()
    release = scrapy.Field()
    recientReviewType = scrapy.Field()
    recientReviewAmount = scrapy.Field()
    allTimeType = scrapy.Field()
    allTimeAmount = scrapy.Field()
    href = scrapy.Field()

class BundleItem(scrapy.Item):
    name = scrapy.Field()
    genres = scrapy.Field()
    developers = scrapy.Field()
    publishers = scrapy.Field()
    href = scrapy.Field()
