import scrapy

class TopSellersSpider(scrapy.Spider):
    name = 'top_seller'
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers']
    
    def parse(self, response):
        for item in response.css('a.search_result_row, a.ds_collapse_flag, a.app_impression_tracked'):
            price = ""
            if len(item.css('div.search_price::text').get().strip()) > 0 :
                price = item.css('div.search_price::text').get()[4:len(item.css('div.search_price::text').get())].strip()
            else:
                price = item.css('div.search_price.discounted::text').extract()[1].strip()
                
            yield {
                'name': item.css('span.title::text').get(),
                'price': price ,
                'discount': item.css('div.search_discount span::text').get()
            }
        # yield {
        #     'rep':response.css('a.search_result_row, a.ds_collapse_flag, a.app_impression_tracked').getall()
        # }
       