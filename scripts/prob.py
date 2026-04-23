import pandas as pd

pd.set_option("display.max_rows", None)

def forward_prob(df, w1_col="category1", w2_col="category2",
               target_fieldsite=None,target_r1_site=None,target_r2_site=None, count_filter=0,
               filter_fieldsite=True,
               ) -> pd.DataFrame:

    # P(w2 | w1) = count(w1, w2) / count(w1)

    #filter by fieldsite and response site
    if filter_fieldsite:
        df = df[df["fieldsite"] == target_fieldsite]
    df = df[df["response_site1"] == target_r1_site]
    df = df[df["response_site2"] == target_r2_site]

    # Count occurrences of w1 and (w1, w2) pairs
    w1_counts = df[w1_col].value_counts()
    pair_counts = df.groupby([w1_col, w2_col]).size()

    # Calculate probabilities
    prob_df = pair_counts.reset_index(name="count")
    if count_filter > 0:
        prob_df = prob_df[prob_df["count"] >= count_filter]
    prob_df["w1_count"] = prob_df[w1_col].map(w1_counts)
    prob_df["probability"] = prob_df["count"] / prob_df["w1_count"]

    #sort by w1 and then probability for easier reading     
    prob_df = prob_df.sort_values(by=[w1_col, "probability"])

    # Print
    if count_filter > 0:
        print(f"Forward probability of response2 given response1 for {target_fieldsite} participants with response_site1={target_r1_site} and response_site2={target_r2_site} (count filter >= {count_filter}):")
    else:
        print(f"Forward probability of response2 given response1 for {target_fieldsite} participants with response_site1={target_r1_site} and response_site2={target_r2_site}:")
    result = prob_df[[w1_col, w2_col, "count", "probability"]].copy()
    result["response_site1"] = target_r1_site
    result["response_site2"] = target_r2_site
    result = result[[w1_col, "response_site1", w2_col, "response_site2", "count", "probability"]]
    print(result)

    return result

def backward_prob(df, w1_col="category1", w2_col="category2",
               target_fieldsite=None,target_r1_site=None,target_r2_site=None, count_filter=0,
               filter_fieldsite=True) -> pd.DataFrame:

    # P(w1 | w2) = count(w1, w2) / count(w2)

    #filter by fieldsite and response site
    if filter_fieldsite:
        df = df[df["fieldsite"] == target_fieldsite]
    df = df[df["response_site1"] == target_r1_site]
    df = df[df["response_site2"] == target_r2_site]

    # Count occurrences of w2 and (w1, w2) pairs
    w2_counts = df[w2_col].value_counts()
    pair_counts = df.groupby([w1_col, w2_col]).size()

    # Calculate probabilities
    prob_df = pair_counts.reset_index(name="count")
    if count_filter > 0:
        prob_df = prob_df[prob_df["count"] >= count_filter]
    prob_df["w2_count"] = prob_df[w2_col].map(w2_counts)
    prob_df["probability"] = prob_df["count"] / prob_df["w2_count"]
    

    # Sort by w2 and then probability for easier reading
    prob_df = prob_df.sort_values(by=[w2_col, "probability"])

    # Print
    if count_filter > 0:
        print(f"Backward probability of response1 given response2 for {target_fieldsite} participants with response_site1={target_r1_site} and response_site2={target_r2_site} (count filter >= {count_filter}):")
    else:
        print(f"Backward probability of response1 given response2 for {target_fieldsite} participants with response_site1={target_r1_site} and response_site2={target_r2_site}:")
    result = prob_df[[w1_col, w2_col, "count", "probability"]].copy()
    result["response_site1"] = target_r1_site
    result["response_site2"] = target_r2_site
    result = result[[w1_col, "response_site1", w2_col, "response_site2", "count", "probability"]]
    print(result)

    return result

def single_word_prob(df, target_word, w1_col="category1", word_col="category2",
               target_fieldsite=None,target_r1_site=None,target_r2_site=None, count_filter=0) -> pd.DataFrame:

    # P(w1 | T) = count(w1, T) / count(T), where T is the target word

    #filter by fieldsite and response site
    df = df[df["fieldsite"] == target_fieldsite]
    df = df[df["response_site1"] == target_r1_site]
    df = df[df["response_site2"] == target_r2_site]

    # Count occurrences of w1 values among rows that match the target word
    target_df = df[df[word_col] == target_word]
    pair_counts = target_df.groupby(w1_col).size()
    target_count = len(target_df)

    #Calculate probabilities
    prob_df = pair_counts.reset_index(name="count")
    if count_filter > 0:
        prob_df = prob_df[prob_df["count"] >= count_filter]
    prob_df[word_col] = target_word
    prob_df["probability"] = prob_df["count"] / target_count

    #Print
    if count_filter > 0:
        print(f"Probability of {target_word} in position {word_col} for {target_fieldsite} participants with response_site1={target_r1_site} and response_site2={target_r2_site} (count filter >= {count_filter}):")
    else:
        print(f"Probability of {target_word} in position {word_col} for {target_fieldsite} participants with response_site1={target_r1_site} and response_site2={target_r2_site}:")
    print(prob_df[[w1_col, word_col, "count", "probability"]])

    #return prob_df


