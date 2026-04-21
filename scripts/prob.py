import pandas as pd


def micro_prob(df, w1_col="category1", w2_col="category2",
               target_fieldsite=None,target_r1_site=None,target_r2_site=None) -> pd.DataFrame:

    # P(w2 | w1) = count(w1, w2) / count(w1)

    #filter by fieldsite and response site
    df = df[df["fieldsite"] == target_fieldsite]
    df = df[df["response_site1"] == target_r1_site]
    df = df[df["response_site2"] == target_r2_site]

    # Count occurrences of w1 and (w1, w2) pairs
    w1_counts = df[w1_col].value_counts()
    pair_counts = df.groupby([w1_col, w2_col]).size()

    # Calculate probabilities
    prob_df = pair_counts.reset_index(name="count")
    prob_df["w1_count"] = prob_df[w1_col].map(w1_counts)
    prob_df["probability"] = prob_df["count"] / prob_df["w1_count"]

    # Print
    print(f"Probability of response2 given response1 for {target_fieldsite} participants with response_site1={target_r1_site} and response_site2={target_r2_site}:")
    print(prob_df[[w1_col, w2_col, "probability"]])