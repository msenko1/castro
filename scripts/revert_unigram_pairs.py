from pathlib import Path
import pandas as pd

def widen_pair_rows(df: pd.DataFrame, pair_key: str = "pair_id", order_key: str = "order") -> pd.DataFrame:
    required_columns = {pair_key, order_key}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing_list}")

    wide_rows = []
    preserved_columns = [column for column in df.columns if column not in {pair_key, order_key}]

    for pair_id, group in df.groupby(pair_key, sort=True):
        ordered_group = group.sort_values(order_key, kind="stable")
        if len(ordered_group) != 2:
            raise ValueError(f"Expected exactly 2 rows for pair_id={pair_id}, found {len(ordered_group)}")

        ordered_records = ordered_group.to_dict(orient="records")
        pair_row = {pair_key: pair_id}

        for column in preserved_columns:
            column_values = ordered_group[column]
            if column_values.nunique(dropna=False) == 1:
                pair_row[column] = column_values.iloc[0]
            else:
                for index, record in enumerate(ordered_records, start=1):
                    pair_row[f"{column}{index}"] = record[column]

        wide_rows.append(pair_row)

    return pd.DataFrame(wide_rows)


def convert_file(input_path: Path, output_path: Path) -> Path:
    df = pd.read_csv(input_path)
    wide_df = widen_pair_rows(df)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wide_df.to_csv(output_path, index=False)
    return output_path
