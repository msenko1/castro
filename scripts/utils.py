import csv
from pathlib import Path
import json
import pandas as pd
import tfidf
import os
from collections import Counter

def convert_csv_to_json(input_csv_file, output_jsonl):
    #converts single csv to jsonl
    input_file = Path(input_csv_file)
    output_file = Path(output_jsonl)

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Iterate over all CSV files in the input directory
    with open(input_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for row in reader:
                json.dump(row, out_f)
                out_f.write('\n')

def add_categories_to_csv(csv):
    df_castro = pd.read_csv(csv)
    df_castro["category"] = df_castro["clean_response"].map(lookup_dict).fillna("other")
    df_castro.to_csv('csv_with_categories.csv', index=False)


def get_tf_df_matrix(input_csv, doc_output_dir, sim_matrix_output_dir, response_variable, use_order, use_idf):
    documents, document_titles = tfidf.prep_castro_docs(input_csv, response_variable, use_order)
    tfidf.save_docs_to_txt(documents, document_titles, doc_output_dir)
    _test_ir = tfidf.IRSystem()
    _test_ir.read_data(doc_output_dir)
    _test_ir.index()
    _test_ir.compute_tfidf(use_idf) # USING DF NOT IDF!!!
    _test_ir.compute_l2_norms()
    _test_ir.compute_all_dot_products()
    output_file = os.path.join(sim_matrix_output_dir, "similarity_matrix.csv")
    _test_ir.save_similarity_matrix_to_csv(output_file)

def get_counts(jsonl_file):
    with open(jsonl_file, 'r', encoding="utf-8") as jsonl:
        response_list = [json.loads(line)["clean_response"] for line in jsonl]
        response_counter = Counter(response_list)
    total_responses = sum(response_counter.values())
    one_count = 0
    running_count = 0
    for key, value in response_counter.items():
        if value >= 2:
            #print(f"{key}: {value}")
            running_count += value
        else:
            one_count += 1
    print(f"Total observations: {total_responses}")
    print(f"Non-one count: {running_count} Non-one proportion: {running_count/total_responses}")
    print(f"One count: {one_count} one proportion: {one_count/total_responses}")
    #print keys and values sorted by frequency
    sorted_responses = response_counter.most_common()
    for key, value in sorted_responses:
        if value == 1:
            print(f"{key}: {value}")