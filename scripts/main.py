import tfidf
from collections import Counter
import os
import json
import utils as util
from category_lists import lookup_dict
import pandas as pd
import revert_unigram_pairs as rup
import prob

def main():
    input_csv = "/Users/senko/Desktop/castro/data/processed/micro_unigram.csv"
    output_csv = "/Users/senko/Desktop/castro/data/processed/all_bigram.csv"

    df = pd.read_csv(input_csv)
    df = rup.widen_pair_rows(df)
    df.info()
    df = df[["pair_id", "fieldsite","clean_response1","category1", "response_site1", "clean_response2", "category2",  "response_site2", "date", "collect_time"]]
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    main()
