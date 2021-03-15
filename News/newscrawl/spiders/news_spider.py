from scrapy.crawler import CrawlerProcess
import scrapy


class SpiderML(scrapy.Spider):
    name = "ml_spider"

    start_urls = [
        'https://takefive-stopfraud.org.uk/news/'
    ]

    def parse(self, response, **kwargs):
        all_text = ' '.join(response.xpath("//body//text()").extract()).strip()
        pass

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SpiderML)
    process.start()


