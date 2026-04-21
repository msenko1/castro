import tfidf
from collections import Counter
import os
import json
import utils as util
from category_lists import lookup_dict
import pandas as pd
import revert_unigram_pairs as rup

def main():
    input_csv = "/Users/senko/Desktop/castro/data/processed/clean_unigram.csv"
    output_path = "/Users/senko/Desktop/castro/data/processed/clean_bigram.csv"
    df = pd.read_csv(input_csv)
    df = rup.widen_pair_rows(df)
    # only keep clean_response1,clean_response2,fieldsite,response_site1,response_site2 date,collect_time,slow1,slow2
    df = df[["fieldsite","clean_response1", "clean_response2", "response_site1", "response_site2", "slow1", "slow2", "date", "collect_time"]]

    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()
