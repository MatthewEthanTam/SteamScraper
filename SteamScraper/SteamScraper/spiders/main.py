from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.utils.project import get_project_settings
my_settings = {
    ### dictionary of optional settings
}

if __name__ == '__main__':

    process = CrawlerProcess(get_project_settings())
    # top_seller = Crawler('top_seller')
    # bundle = Crawler('bundle')
    # basegame = Crawler('basegame')
    # process.crawl('MyScraper',
    #               custom_settings=my_settings,)
    process.crawl('top_seller')
    process.crawl('bundle')
    process.crawl('basegame')
    process.start()
