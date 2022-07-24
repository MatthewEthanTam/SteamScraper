from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

my_settings = {
    ### dictionary of optional settings
}

if __name__ == '__main__':

    process = CrawlerProcess(get_project_settings())
    process.crawl('MyScraper',
                  custom_settings=my_settings,)
    process.start()
