# Data and other OOP models here

import logging
import multiprocessing

from collections import defaultdict

import pandas as pd

from pydantic.dataclasses import dataclass
from pydantic import Field

from config import KMERS
from kmers_processing import kcounter, kcreator
from spacy_processing import simplify_line



logger = logging.getLogger(__name__)


@dataclass
class Book:
    title: str
    publication_year: int
    raw_text: str = Field(repr=False)
    book_tag: str = ""
    simplified: str = Field(default='', repr=False)
    simplified_punc_short: str = Field(default='', repr=False)
    kmers: dict[int, dict] = Field(default_factory=dict, repr=False)

    def simplify_file_poc_punc(self) -> None:
        self.simplified = simplify_line(self.raw_text)

    def simplify_file_poc_punc_short(self) -> None:
        text = self.simplified

        text = text.replace('ADJ', 'a')
        text = text.replace('ADP', 'b')
        text = text.replace('ADV', 'c')
        text = text.replace('AUX', 'd')
        text = text.replace('CCONJ', 'e')
        text = text.replace('DET', 'f')
        text = text.replace('INTJ', 'g')
        text = text.replace('NOUN', 'h')
        text = text.replace('NUM', 'i')
        text = text.replace('PART', 'j')
        text = text.replace('PRON', 'k')
        text = text.replace('PROPN', 'h')
        text = text.replace('SCONJ', 'm')
        text = text.replace('SYM', 'n')
        text = text.replace('VERB', 'o')
        text = text.replace('X', 'p')    

        text = text.replace('SPACE', '') 
        text = text.replace('PUNCT', '')
        text = text.replace(' ', '')
        text = text.replace('\n', 't')

        self.simplified_punc_short = text

    def process_with_kmer(self, kmer: int) -> None:
        """Create dict of kmers of given size"""
        kmer_result_dict = kcounter(kcreator(self.simplified_punc_short, kmer))
        self.kmers[kmer] = kmer_result_dict


def process_book(book: Book) -> Book:
    logger.info(f"Started processing {book.title}")
    
    book.simplify_file_poc_punc()
    book.simplify_file_poc_punc_short()

    for kmer in KMERS:
        book.process_with_kmer(kmer)

    logger.info(f"Processed {book.title}")

    return book

def process_books_parallel(book_list: list[Book], n_processes: int = 1):
    with multiprocessing.Pool(n_processes) as p:
        results = p.map(process_book, book_list)
    return results


