from summariser.base import BaseSummariser


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
        pass
