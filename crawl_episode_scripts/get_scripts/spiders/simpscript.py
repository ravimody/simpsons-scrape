import scrapy
# from get_scripts.items import SimpItem


class SimpItem(scrapy.Item):
    ep_text = scrapy.Field()
    ep_url = scrapy.Field()



class SimpSpider(scrapy.Spider):
    name = "simp"
    allowed_domains = ["www.springfieldspringfield.co.uk"]
    start_urls = [
        "http://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-simpsons"
    ]

    def parse(self, response):
        for href in response.xpath('//a[@class="season-episode-title"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_ep_contents)            

    def parse_ep_contents(self, response):
        item = SimpItem()
        item['ep_text'] = response.xpath('//div[@class="scrolling-script-container"]/text()').extract()
        item['ep_url'] = response.url            
        return item
