import scrapy


class GeneralSpider(scrapy.Spider):
    """Parses the articles on the takefive homepage"""
    name = "general_spider"

    def __init__(self, **kwargs):
        super(GeneralSpider).__init__()
        self.link_css = kwargs['link_css']
        self.header_css = kwargs['header_css']
        self.date_css = kwargs['date_css']
        self.text_xpath = kwargs['text_xpath']
        self.urls = kwargs['urls']

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


