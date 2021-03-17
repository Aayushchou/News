import scrapy
from scrapy.crawler import CrawlerProcess


class GeneralSpider(scrapy.Spider):
    """Parses the articles on the takefive homepage"""
    name = "general_spider"

    def __init__(self, link_css=None, header_css=None, date_css=None, text_xpath=None, urls=None):
        super(GeneralSpider).__init__()
        self.link_css = link_css
        self.header_css = header_css
        self.date_css = date_css
        self.text_xpath = text_xpath
        self.urls = urls

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """Parses the links for the articles from the homepage"""
        links = response.css(
            self.link_css
        ).extract()

        for link in links:
            yield response.follow(url=link, callback=self.parse_article)

    def parse_article(self, response):
        """Parses the header, date and text for each article"""
        header = response.css(self.header_css).extract()[-1].lower()
        date = response.css(self.date_css).extract()[-1].lower()
        text = (
            " ".join(
                t
                for t in response.xpath(
                    self.text_xpath
                ).extract()
                if t != "\n"
            )
                .strip("\n")
                .strip().lower()
        )
        yield {
            'header': header,
            'date': date,
            'text': text
        }


# "article:nth-child(n) > header > h2 > a::attr(href)"
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "general.json": {"format": "json"}
        },
    })
    config = {'link_css': "article:nth-child(n) > header > h2 > a::attr(href)",
              'header_css': "header > div > div > h1::text",
              'date_css': "article > div.post__date > time::text",
              'text_xpath': "//*[@id='content']/section/article/div[@class='entry-content stack']//text()"}

    process.crawl(GeneralSpider,
                  **config,
                  urls=["https://takefive-stopfraud.org.uk/news/"])
    process.start()
