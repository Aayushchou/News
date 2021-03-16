from scrapy.crawler import CrawlerProcess
import scrapy


class SpiderML(scrapy.Spider):
    name = "ml_spider"

    start_urls = ["https://takefive-stopfraud.org.uk/news/"]

    def parse(self, response, **kwargs):
        links = response.css(
            "article:nth-child(n) > header > h2 > a::attr(href)"
        ).extract()

        for link in links:
            yield response.follow(url=link, callback=self.parse_article)

    def parse_article(self, response):
        header = response.css("h1::text").extract()[-1]
        date = response.css("article > div.post__date > time::text").extract()[-1]
        text = (
            " ".join(
                t
                for t in response.xpath(
                    "//*[@id='content']/section/article/div[@class='entry-content stack']//text()"
                ).extract()
                if t != "\n"
            )
            .strip("\n")
            .strip()
        )
        yield {
            'header': header,
            'date': date,
            'text': text
        }


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "takefive.json": {"format": "json"}
        },
    })
    process.crawl(SpiderML)
    process.start()
