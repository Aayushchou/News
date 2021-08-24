import torch
import re
import nltk
import multiprocessing as mp
import json

from transformers import AutoModelForTokenClassification, AutoTokenizer
from ner.base import BaseNER


class EntityRecognizer(BaseNER):
    
    def __init__(self,
                 filepath,
                 model_name="dbmdz/bert-large-cased-finetuned-conll03-english",
                 tokenizer_name="bert-base-cased"
                 ):
        super().__init__(filepath)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def prepare(self, raw_text):
        raw_text = "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very" \
                   "close to the Manhattan Bridge."
        tokens = self.tokenizer.tokenize(self.tokenizer.decode(self.tokenizer.encode(raw_text)))
        inputs = self.tokenizer.encode(raw_text, return_tensors="pt")
        return tokens, inputs

    def predict(self, tokens, inputs):
        outputs = self.model(inputs)[0]
        predictions = torch.argmax(outputs, dim=2)

        entities = [(token, self.model.config.id2label[prediction])
                    for token, prediction in zip(tokens, predictions[0].tolist())
                    if prediction != 'O']
        return entities

    def process(self, sequence):
        chunks = self.text_splitter(sequence)
        entities = [self.predict(*self.prepare(chunk)) for chunk in chunks]
        return entities

    def __call__(self):
        with mp.Pool(int(mp.cpu_count() / 2)) as pool:
            entities = pool.map(self.process, self.txt)

        with open(self.filepath, "r") as jsonFile:
            data = json.load(jsonFile)

        for x, y in zip(data, entities):
            x['entities'] = y

        with open(self.filepath, 'w') as jsonFile:
            json.dump(data, jsonFile)

    @staticmethod
    def text_splitter(txt, n=200):
        txt = txt.split()
        return [' '.join(txt[i:i + n]) for i in range(0, len(txt), n)]


if __name__ == '__main__':
    ner = EntityRecognizer('/Users/aayush/Documents/LitGenie/scraper/newscrawl/output/home_treasury_gov.json')
    ner()
