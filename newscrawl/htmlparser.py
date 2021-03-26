from newscrawl.spiders.general_spider import GeneralSpider
from scrapy.crawler import CrawlerProcess
import argparse
import pandas as pd
from urllib.parse import urlparse


def main(url=None):
    web_config = pd.read_csv('webconfig/webconfig.csv', index_col=0)
    domain = urlparse(url).netloc
    try:
        config = web_config.loc[domain, :].to_dict()
    except KeyError as e:
        print(f"Website {domain} is not currently supported: {e}")
        exit()

    process = CrawlerProcess(settings={
        "FEEDS": {
            f"output/{domain.replace('.', '_')}.json": {"format": "json"}
        },
    })

    process.crawl(GeneralSpider,
                  **config,
                  urls=[url])
    process.start()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=False, help="URL of the website we want to parse", default='https://www.dfsa.ae/news')
    args = vars(parser.parse_args())
    main(url=args.get('url'))
