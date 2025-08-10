import logging
import multiprocessing
from collections import defaultdict
from pathlib import Path

from book import Book
from pydantic.dataclasses import dataclass
from pydantic.dataclasses import Field

import pandas as pd
import numpy as np

from utils import convert_kmer_dict_to_pd_dataframe
from config import KMERS, RESULT_DIR
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

@dataclass
class Pair:
    first_book: Book
    second_book: Book
    jaccard_indexes: dict[int, float] = Field(default_factory=dict, repr=False)

    def calculate_jaccard_index(self, kmer: int) -> float:
        """Calculate jaccard index for pair"""
        if self.first_book.title == self.second_book.title:
            jaccard_index = 1.0
        else:
            first = convert_kmer_dict_to_pd_dataframe(self.first_book.kmers[kmer])
            second = convert_kmer_dict_to_pd_dataframe(self.second_book.kmers[kmer])


            first_kmers = set(first["kmer"])
            second_kmers = set(second["kmer"])

            intersection = first_kmers & second_kmers
            second_only = second_kmers - first_kmers

            # Calculate intersection sum
            intersection_sum_list = []
            for kmer_sequence in intersection:
                f_freq = first[first["kmer"] == kmer_sequence]["freq"].item()
                s_freq = second[second["kmer"] == kmer_sequence]["freq"].item()

                intersection_sum_list.append(min(f_freq, s_freq))
            intersection_sum = sum(intersection_sum_list)

            # Get union sum
            f_sum = sum(first["freq"])
            s_only_sum = sum(second[second["kmer"].isin(second_only)]["freq"].to_list())

            jaccard_index = intersection_sum / (f_sum + s_only_sum)
        
        self.jaccard_indexes[kmer] = jaccard_index


    def calculate_jaccard_indexes(self, kmers: list[int] = KMERS) -> float:
        logger.info(f"Processing pair: {self.first_book.title, self.second_book.title}")
        for kmer in kmers:
            self.calculate_jaccard_index(kmer)


def process_pair(pair: Pair) -> Pair:
    pair.calculate_jaccard_indexes()
    logger.info(f"Processed pair: {pair.first_book.title, pair.second_book.title}")
    logger.debug(f"Indexes: {pair.jaccard_indexes}")
    return pair

def process_pairs_parallel(pairs_list: list[Pair], n_processes: int = 1):
    with multiprocessing.Pool(n_processes) as p:
        results = p.map(process_pair, pairs_list)
    return results

def collect_kmers_to_dict(pairs_list: list[Pair]):
    kmer_dict = defaultdict(list)
    for pair in pairs_list:
        for kmer in pair.jaccard_indexes:
            j_index = pair.jaccard_indexes[kmer]
            kmer_dict[kmer].append([pair.first_book.title, pair.second_book.title, j_index])

    return dict(kmer_dict)

def intersect_two_sets(kmer_dict: dict[int, tuple[str, str, float]]) -> list[pd.DataFrame]:
    matrices_list = []

    heatmap_dir = Path(RESULT_DIR, "heatmaps")
    heatmap_dir.mkdir(exist_ok=True, parents=True)

    for kmer in kmer_dict:
        kmer_list = kmer_dict[kmer]
        tags = []
        for t1, t2, _ in kmer_list:
            tags += [t1, t2]
        tags = index = columns = sorted(list(set(tags)))
        tags = dict((t, i) for i, t in enumerate(tags))

        matrix = np.identity(len(tags))

        for t1, t2, j_index in kmer_list:
            matrix[tags[t1]][tags[t2]] = j_index
            matrix[tags[t2]][tags[t1]] = j_index

        df = pd.DataFrame(matrix, index=index, columns=columns)
        matrices_list.append([kmer, df])

        matrix_name = f"kmer_{kmer}.csv"

        df.to_csv(Path(heatmap_dir, matrix_name))

        print(f"Saved to {str(Path(heatmap_dir, matrix_name))}")

    return matrices_list


def plot_heatmap(matrix_data: tuple[int, pd.DataFrame]) -> None:
    # Plot tree
    kmer, df = matrix_data
    plot_dir = Path(RESULT_DIR, "plots")
    plot_dir.mkdir(exist_ok=True, parents=True)

    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    df = df.apply(pd.to_numeric)     

    df = df.apply(pd.to_numeric)

    dist_df = 1 - df

    condensed = sch.distance.squareform(dist_df.values)

    linkage_matrix = sch.linkage(condensed, method='average')


    plt.figure(figsize=(30, 20))
    sch.dendrogram(linkage_matrix, labels=df.index)
    plt.savefig(Path(plot_dir, f"dendro_kmer_{kmer}.png"))

    # Plot heatmap
    sns.heatmap(df, cmap='coolwarm')
    plt.savefig(Path(plot_dir, f"heatmap_kmer_{kmer}.png"))


def plot_heatmaps(matrix_data_list: tuple[int, pd.DataFrame]) -> None:
    for matrix_data in matrix_data_list:
        plot_heatmap(matrix_data)