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
    config_takefive = {'link_css': "article:nth-child(n) > header > h2 > a::attr(href)",
              'header_css': "header > div > div > h1::text",
              'date_css': "article > div.post__date > time::text",
              'text_xpath': "//*[@id='content']/section/article/div[@class='entry-content stack']//text()"}

    config_treasury = {'link_css': "div:nth-child(n) > h3 > a::attr(href)",
                       'header_css': "h2 > span::text",
                       'date_css': "time::attr(datetime)",
                       'text_xpath': "//*[@id='block-hamilton-content']/article/div/div[2]//text()"}

    config_fca = {'link_css': "body > div.dialog-off-canvas-main-canvas > div > "
                              "section > div.region.region-content > article > div > "
                              "section.component.content-feed.feed--news > div > div > "
                              "div.view.view-warnings-feed.view-id-warnings_feed.view-display-id-warnings.js-view-dom-id-0b209a27a978c106625ac5dac195348e90c403c713b1ea17cec4fa5ebabb748e "
                              "> div > div > div:nth-child(n) > a::attr(href)",
                       'header_css': "body > div.dialog-off-canvas-main-canvas "
                                     "> div.main-container.js-quickedit-main-content "
                                     "> section > div.region.region-content "
                                     "> div:nth-child(n) > div > header > h1 > span::text",
                       'date_css': "body > div.dialog-off-canvas-main-canvas > div.main-container.js-quickedit-main-content > section > div.region.region-content > div:nth-child(1) > div > header > div > span:nth-child(2) > time",
                       'text_xpath': "/html/body/div[2]/div[2]/section/div[2]/div[2]/div/article/div//text()"}

    config_dfsa = {'link_css': "body > div > div > div > div > div > a:nth-child(n)::attr(href)",
                       'header_css': "body > div > div > div > div > div > div > h1::text",
                       'date_css': "body > div > div > div > div > div > div > h6::text",
                       'text_xpath': "/html/body/div[2]/div[2]/div/div[3]/div/div/div//text()"}

    process.crawl(GeneralSpider,
                  **config_dfsa,
                  urls=["https://www.dfsa.ae/news"])
    process.start()
