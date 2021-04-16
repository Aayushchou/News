from summariser.base import BaseSummariser
import multiprocessing as mp
import nltk
import re
from nltk.tokenize import sent_tokenize
import heapq
import json

nltk.download("punkt")
nltk.download("stopwords")


class WordFreqSummariser(BaseSummariser):
    def __init__(self, filepath: str, language: str = "english", n_sentences=5):
        super().__init__(filepath)
        self.lang = language
        self.n_sentences = n_sentences

    @staticmethod
    def prepare(raw_text):
        """Text cleaning process: remove extra spaces and digits"""
        # cleaned = re.sub(r"[^a-zA-Z]", " ", raw_text)
        cleaned = re.sub(r"\s+", " ", raw_text)
        tokens = sent_tokenize(raw_text)
        return cleaned, tokens

    def summarise(self, cleaned_text, tokens):
        """Function summarising cleaned input text to n sentences"""
        word_frequencies = self.get_word_frequencies(cleaned_text)
        sent_scores = self.get_sentence_scores(tokens, word_frequencies)
        summary_sentences = heapq.nlargest(
            self.n_sentences, sent_scores, key=sent_scores.get
        )
        summary = " ".join(summary_sentences)

        return summary

    @staticmethod
    def get_sentence_scores(sentence_list, word_frequencies):
        """Function to get scores for each sentence, based on word frequencies"""
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(" ")) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        return sentence_scores

    def get_word_frequencies(self, cleaned_text):
        """Function to get word frequencies"""
        stopwords = nltk.corpus.stopwords.words(self.lang)
        word_frequencies = {}
        for word in nltk.word_tokenize(cleaned_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / maximum_frequncy
        return word_frequencies

    def process(self, raw_text):
        """Wrapper function, converting raw text to summarised text"""
        return self.summarise(*self.prepare(raw_text))

    def __call__(self):
        """Main entry-point, outputs summarised text to json"""
        with mp.Pool(int(mp.cpu_count() / 2)) as pool:
            summarised = pool.map(self.process, self.txt)

        with open(self.filepath, "r") as jsonFile:
            data = json.load(jsonFile)

        for x, y in zip(data, summarised):
            x['summary'] = y

        with open(self.filepath, 'w') as jsonFile:
            json.dump(data, jsonFile)


# Testing
if __name__ == "__main__":
    t = WordFreqSummariser(
        filepath=r"/Users/aayush/Documents/LitGenie/scraper/newscrawl/output/home_treasury_gov.json"
    )
    t()
