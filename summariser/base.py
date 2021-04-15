from abc import ABC, abstractmethod
from uuid import uuid4
from typing import List
import json


class BaseSummariser(ABC):
    def __init__(self, file_path: str):
        """Base class handling text io and outlining functions required for summarisation models.
        A Summariser class will take as input a source path (news source) and create an object containing
        all the text for that source and corresponding summary"""

        self.id = uuid4().int
        assert file_path.split(".")[-1] in ["json"], (
            "Summariser currently only accepts json files with a text field"
            "for each article"
        )

        with open(file_path) as f:
            data = json.load(f)
        self.txt = [article["text"] for article in data]
        del data

    @staticmethod
    @abstractmethod
    def prepare(raw_text: str):
        """Each summariser model should have its own way of pre-processing text. It should take in a list of raw
        texts and return a list of pre-processed strings"""
        pass

    @staticmethod
    @abstractmethod
    def summarise(processed_tokens):
        """Each summariser would implement its main summarisation logic in this function. It should take in a list of
        preprocessed strings and return a list of summarised strings"""
        pass

    @staticmethod
    @abstractmethod
    def process(raw_text: str):
        """The process method calls both summarise and prepare methods and returns the summarised text from raw text"""
        pass

    @abstractmethod
    def __call__(self):
        """Each summariser would have a call function that processes a batch of texts. it should take in a list of
        raw strings and store store to a json a list of summarised strings"""
        pass
