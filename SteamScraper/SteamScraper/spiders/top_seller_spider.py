import json
from pickle import NONE
import scrapy
from ..items import BundleItem, GameItem, InGameItem
urls = ['https://store.steampowered.com/search/?filter=topsellers&start=0&count=100',
        'https://store.steampowered.com/search/?filter=topsellers&start=101&count=200',
        'https://store.steampowered.com/search/?filter=topsellers&start=201&count=300',
        'https://store.steampowered.com/search/?filter=topsellers&start=301&count=400',
        'https://store.steampowered.com/search/?filter=topsellers&start=401&count=500',
        'https://store.steampowered.com/search/?filter=topsellers&start=501&count=600']
class BundleSpider(scrapy.Spider):
    name = 'bundle'
    custom_settings = {
            'ITEM_PIPELINES': {
                'SteamScraper.pipelines.GameBundlePipeline': 400
            }
    }
    start_urls = urls
    
    
    def parse(self, response):
        game_page = response.css('a.search_result_row.ds_collapse_flag::attr(href)').getall()
        if game_page is not None:
            yield from response.follow_all(game_page, self.parseGame)
            
    def parseGame(self, response):
        if 'bundle' in response.url or '/sub/' in response.url:
            title = response.css('h2.pageheader::text').get()
            genre = response.css('div.details_block').css('p').css('span')[0].css('a::text').getall()
            developers = response.css('div.details_block').css('p').css('span')[1].css('a::text').getall()
            publishers = response.css('div.details_block').css('p').css('span')[2].css('a::text').getall()
            bundle = BundleItem()
            bundle['name'] = title
            bundle['genres'] = genre
            bundle['developers'] = developers
            bundle['publishers'] = publishers
            bundle['href'] = response.url[:len(response.url)-21]
            yield bundle
        else:
            return None
class BaseGameSpider(scrapy.Spider):
    name = 'basegame'
    custom_settings = {
            'ITEM_PIPELINES': {
                'SteamScraper.pipelines.BaseGamePipeline': 400
            }
    }
    start_urls = urls
    
    
    def parse(self, response):
        game_page = response.css('a.search_result_row.ds_collapse_flag::attr(href)').getall()
        if game_page is not None:
            yield from response.follow_all(game_page, self.parseGame)
    
    def parseGame(self,response):
        if '/agecheck/app' in response.url:
            formdata = {
                'ageDay': '1',
                'ageMonth': '1',
                'ageYear': '1955'
            }

            yield scrapy.FormRequest(
                url=response.url,
                method='POST',
                formdata=formdata,
                callback=self.parseGame,
            )
        elif '/bundle/' in response.url or '/sub/' in response.url:
            return None
        else :
            tagList = []
            genre = ""
            if len(response.css('a.app_tag::text').getall()) != 0:
                tagList = response.css('a.app_tag::text').getall()
                for i in tagList:
                    tagList[tagList.index(i)] = i.strip().replace("\n", "").replace("\t", "").replace("\r", "")
            else:
                tagList = None
            block = response.css('#genresAndManufacturer')
            
            genre = block.css('span a::text').extract()
            devAndBlock = block.css('div.dev_row a::text').extract()
            href = response.css('link[rel="canonical"]::attr(href)').get()
            alltext = block.css('#genresAndManufacturer::text').extract()
            if alltext :
                title = alltext[1]
            else:
                title = None
            release = ""
            
            for item in alltext[2:]:
                if "\n" not in item and "\r" not in item and "\t" not in item and " " != item:
                    release = item
                    break
            if not href:
                href = response.url
            
            if devAndBlock:
                dev = devAndBlock[0]
                if (len(devAndBlock) > 1):
                    pub = devAndBlock[1]
                else:
                    pub = None
            else:
                dev = None
                pub = None
            reviewBlock = response.css('div.summary')
            recientReview = reviewBlock.css('span::text').getall()
            reviews = response.css('span.responsive_hidden::text').getall()
            counter = 0
            for i in recientReview:
                recientReview[counter] = i.replace("\r", "").replace("\n","").replace("\t","")
                counter += 1
            size = len(recientReview)
            recent = ""
            allReviews = ""
            recenttype = ""
            alltype = ""
            if size >14:
                recenttype = recientReview[0]
                alltype = recientReview[4]
            elif size==14:
                recenttype = recientReview[0]
                alltype = recientReview[3]
            elif size == 7:
                alltype = recientReview[0]
            if len(reviews) == 3:
                recent = reviews[0].replace("\r", "").replace("\n","").replace("\t","").replace("(","").replace(")","").replace(",","")
                allReviews = reviews[1].replace("\r", "").replace("\n","").replace("\t","").replace("(","").replace(")","").replace(",","")
            elif len(reviews) == 2:
                allReviews = reviews[0].replace("\r", "").replace("\n","").replace("\t","").replace("(","").replace(")","").replace(",","")
            if not title :
                return None
            inGameItem = InGameItem()
            inGameItem['name'] = title[1:]
            inGameItem['tags'] = tagList
            inGameItem['genre'] = genre
            inGameItem['developer'] = dev
            inGameItem['publisher'] = pub
            inGameItem['release'] = release
            inGameItem['recientReviewType'] = recenttype
            inGameItem['recientReviewAmount'] = recent
            inGameItem['allTimeType'] = alltype
            inGameItem['allTimeAmount'] = allReviews
            inGameItem['href'] = href
            yield inGameItem    
    
class TopSellersSpider(scrapy.Spider):
    name = 'top_seller'
    start_urls = urls
    custom_settings = {
            'ITEM_PIPELINES': {
                'SteamScraper.pipelines.SteamscraperPipeline': 300,
            }
    }
    
    
    def parse(self, response):
        
        for item in response.css('a.search_result_row, a.ds_collapse_flag, a.app_impression_tracked'):
            price = ""
            if len(item.css('div.search_price::text').get().strip()) > 0 :
                price = item.css('div.search_price::text').get()[4:len(item.css('div.search_price::text').get())].strip()
            else:
                price = item.css('div.search_price.discounted::text').extract()[1].strip()

            discount = 0
            if item.css('div.search_discount span::text').get() is not None:
                discount = int(item.css('div.search_discount span::text').get()[:len(item.css('div.search_discount span::text').get())-1])
            else:
                discount = None
            
            gameItem = GameItem()
            gameItem['name'] = item.css('span.title::text').get()
            gameItem['price'] = price
            gameItem['discount'] = discount
            gameItem['href'] = item.css('a::attr(href)').get()[:item.css('a::attr(href)').get().index("?")]

            yield gameItem
 