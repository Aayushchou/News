from abc import ABC, abstractmethod
from uuid import uuid4
import json
from typing import List


class BaseNER(ABC):
    def __init__(self, file_path: str):
        """Base class handling text io and outlining functions required for entity recognition models.
        A Summariser class will take as input a source path (news source) and create an object containing
        all the text for that source and corresponding summary"""

        self.id = uuid4().int
        self.filepath = file_path
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
    def prepare(raw_text: str) -> (str, List[str]):
        """Each summariser model should have its own way of pre-processing text. It should take in a list of raw
        texts and return a list of pre-processed strings"""
        pass

    @staticmethod
    @abstractmethod
    def predict(tokens: List[str], inputs : List[str]) -> List[tuple]:
        """Each entity recognizer would implement main entity recognition logic in this function. It should take in a
        list of preprocessed tokens and return a list of summarised strings"""
        pass

    @staticmethod
    @abstractmethod
    def process(raw_text: str) -> str:
        """The process method calls both predict and prepare methods and returns the entities from raw text"""
        pass

    @abstractmethod
    def __call__(self):
        """Each summariser would have a call function that processes a batch of texts. it should take in a list of
        raw strings and store store to a json a list of entities"""
        pass
