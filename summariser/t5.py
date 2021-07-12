from summariser.base import BaseSummariser
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import multiprocessing as mp
import json

class T5Summariser(BaseSummariser):

    def __init__(self,
                 filepath,
                 model_name='t5-base',
                 tokenizer_name='t5-base',
                 **kwargs):
        super().__init__(filepath)
        self.kwargs = kwargs
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def prepare(self, raw_text):
        if 't5' in self.tokenizer_name:
            inputs = self.tokenizer.encode('summarize: ' + raw_text,
                                           return_tensors="pt",
                                           max_length=512,
                                           truncation=True)
        else:
            inputs = self.tokenizer.encode(raw_text,
                                           return_tensors="pt",
                                           max_length=512,
                                           truncation=True)
        return inputs

    def summarise(self, tokens):
        outputs = self.model.generate(tokens, **self.kwargs)
        return self.tokenizer.decode(outputs[0])

    def process(self, raw_text):
        return self.summarise(self.prepare(raw_text))

    def __call__(self):
        with mp.Pool(int(mp.cpu_count() / 2)) as pool:
            summarised = pool.map(self.process, self.txt)

        with open(self.filepath, "r") as jsonFile:
            data = json.load(jsonFile)

        for x, y in zip(data, summarised):
            x['summary'] = y.lstrip('<pad> ').rstrip(' </s>')

        with open(self.filepath, 'w') as jsonFile:
            json.dump(data, jsonFile)


if __name__ == '__main__':
    t5 = T5Summariser(
        filepath=r"/Users/aayush/Documents/LitGenie/scraper/newscrawl/output/home_treasury_gov.json",
        max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    t5()