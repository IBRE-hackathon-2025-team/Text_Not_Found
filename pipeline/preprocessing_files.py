"""Scripts for preprocessing"""

from pathlib import Path
from book import Book
import pandas as pd


def read_data_from_csv(path_to_csv: Path) -> list[Book]:
    """Function to read data from csv and return list of Book obj"""
    book_list = []
    input_list = list(pd.read_csv(path_to_csv).to_dict(orient="index").values())

    for book_data in input_list:
        with open(book_data["path_to_book"], "r") as file:
            raw_text = file.read()

        book_list.append(Book(**book_data, raw_text=raw_text))

    return book_list






