import pandas as pd


def convert_kmer_dict_to_pd_dataframe(d: dict) -> pd.DataFrame:
    v = list(d.values())
    k = list(d.keys())

    df = pd.DataFrame()
    df["kmer"] = k
    df["freq"] = v

    return df