from summariser.base import BaseSummariser
import multiprocessing as mp
import nltk
nltk.download('punkt')


class TextRankSummariser(BaseSummariser):

    def __init__(self, filepath: str):
        super().__init__(filepath)

    @staticmethod
    def prepare(raw_text):
        return ''

    @staticmethod
    def summarise(cleaned_text):
        return ''

    def process(self, raw_text):
        return self.summarise(self.prepare(raw_text))

    def __call__(self):
        with mp.Pool(int(mp.cpu_count()/2)) as pool:
            summarised = pool.map(self.process, self.txt)
        pass


# Testing
if __name__ == '__main__':
    t = TextRankSummariser(filepath=r'/Users/aayush/Documents/LitGenie/scraper/newscrawl/output/home_treasury_gov.json')
    t()
