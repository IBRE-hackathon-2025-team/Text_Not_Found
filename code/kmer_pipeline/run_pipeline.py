import logging

from pathlib import Path
from itertools import combinations_with_replacement

from preprocessing_files import read_data_from_csv
from config_logging import setup_logging
from book import process_books_parallel
from pair_processing import Pair, process_pairs_parallel, collect_kmers_to_dict, intersect_two_sets, plot_heatmaps

from config import N_PROCESSES


# Read the data

def run(path_to_csv: Path):
    """Executes the pipeline"""
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info(f"Reading data from csv...")
    book_list = read_data_from_csv(path_to_csv)
    logger.info(f"Managed to find {len(book_list)} books")

    preprocessed_books = process_books_parallel(book_list, N_PROCESSES)

    logger.info(f"Finished books preprocessing...")
    logger.info(f"Generating pairs...")
    book_pairs = [Pair(*pair) for pair in list(combinations_with_replacement(preprocessed_books, 2))]

    logger.info(f"Processing pairs...")
    processed_pairs = process_pairs_parallel(book_pairs, N_PROCESSES)

    kmer_dict = collect_kmers_to_dict(processed_pairs)
    matrices_list = intersect_two_sets(kmer_dict)
    plot_heatmaps(matrices_list)



if __name__=="__main__":
    path_to_csv = Path("/home/team/for_repo/pipeline_input_table_subset.csv")

    run(path_to_csv)