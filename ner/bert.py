import torch
import re
import nltk

from transformers import AutoModelForTokenClassification, AutoTokenizer
from nltk.tokenize import sent_tokenize

nltk.download("punkt")
nltk.download("stopwords")


class EntityRecognizer(object):
    
    def __init__(self,
                 filepath,
                 model_name,
                 tokenizer_name
                 ):
        self.filepath = filepath
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def prepare(self, raw_text):
        cleaned = re.sub(r"\s+", " ", raw_text)
        tokens = sent_tokenize(cleaned)
        return tokens

    def predict(self, sequence):
        tokens = self.tokenizer.tokenize(self.tokenizer.decode(self.tokenizer.encode(sequence)))
        inputs = self.tokenizer.encode(sequence, return_tensors="pt")

        outputs = self.model(inputs).logits
        predictions = torch.argmax(outputs, dim=2)

        entities = [(token, self.model.config.id2label(prediction))
                    for token, prediction in zip(tokens, predictions[0].numpy())
                    if prediction != 'O']
        return entities

    def process(self, sequence):
        self.predict(*self.prepare(sequence))

    def __call__(self):
        pass


if __name__ == '__main__':
    pass