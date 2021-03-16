import scrapy
from scrapy.crawler import CrawlerProcess


class TreasurySpider(scrapy.Spider):
    """Parses the articles on the takefive homepage"""
    name = "treasury_spider"

    start_urls = ["https://home.treasury.gov/news/press-releases"]

    def parse(self, response, **kwargs):
        """Parses the links for the articles from the homepage"""
        links = response.css(
            "div:nth-child(n) > h3 > a::attr(href)"
        ).extract()

        for link in links:
            yield response.follow(url=link, callback=self.parse_article)

    def parse_article(self, response):
        """Parses the header, date and text for each article"""
        header = response.css("h2 > span::text").extract()
        date = response.css("time::attr(datetime)").extract_first()
        text = (
            " ".join(
                t
                for t in response.xpath(
                    "//*[@id='block-hamilton-content']/article/div/div[2]//text()"
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


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "treasury.json": {"format": "json"}
        },
    })
    process.crawl(TreasurySpider)
    process.start()
