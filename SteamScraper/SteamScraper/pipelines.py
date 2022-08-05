# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import json

class SteamscraperPipeline:
    def __init__(self) :
        self.con = sqlite3.connect('steam.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Games (
            name TEXT,
            price FLOAT,
            discount INTEGER,
            href TEXT
        )
        """)
    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO games VALUES (?, ?, ?, ?)
        """, (item['name'], item['price'], item['discount'], item['href']))
        self.con.commit()
        return item

class GameBundlePipeline:
    def __init__(self) :
        self.con = sqlite3.connect('steam.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Bundles (
            name TEXT,
            genres TEXT,
            developers TEXT,
            publishers TEXT,
            href TEXT
        )
        """)
    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO Bundles VALUES (?, ?, ?, ?, ?)
        """, (item['name'], json.dumps(item['genres']), json.dumps(item['developers']), json.dumps(item['publishers']), item['href']))
        self.con.commit()
        return item
class BaseGamePipeline:
    def __init__(self) :
        self.con = sqlite3.connect('steam.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS BaseGames (
            name TEXT,
            tags TEXT,
            genre TEXT,
            developer TEXT,
            publisher TEXT,
            release TEXT,
            recientReviewType TEXT,
            recientReviewAmount INTEGER,
            allTimeType TEXT,
            allTimeAmount INTEGER,
            href TEXT
        )
        """)
    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO Basegames VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (item['name'], json.dumps(item['tags']), json.dumps(item['genre']), item['developer'], item['publisher'], item['release'], item['recientReviewType'], item['recientReviewAmount'], item['allTimeType'], item['allTimeAmount'], item['href']))
        self.con.commit()
        return item
    
                         
                         
