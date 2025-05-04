import os
import pandas as pd

def aggregate_metropolitan_data(root_dir: str, output_csv: str):
    """
    Traverse each subfolder in `root_dir` (named like '2018-01', ..., '2025-02'),
    find all CSV files containing 'metropolitan' in their filename (case-insensitive),
    concatenate them into one DataFrame, drop duplicate rows, and save to `output_csv`.
    """
    data_frames = []
    files_found = 0

    for subfolder in os.listdir(root_dir):
        subfolder_path = os.path.join(root_dir, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        for file_name in os.listdir(subfolder_path):
            if file_name.lower().endswith('.csv') and 'metropolitan' in file_name.lower():
                files_found += 1
                file_path = os.path.join(subfolder_path, file_name)
                try:
                    df = pd.read_csv(file_path)
                    data_frames.append(df)
                except Exception as e:
                    print(f"Warning: failed to read {file_path}: {e}")

    if not data_frames:
        print("No metropolitan CSV files found in the specified directory.")
        return

    merged_df = pd.concat(data_frames, ignore_index=True)
    before_count = len(merged_df)
    merged_df.drop_duplicates(inplace=True)
    after_count = len(merged_df)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    merged_df.to_csv(output_csv, index=False)

    print(f"Files processed: {files_found}")
    print(f"Rows before deduplication: {before_count}")
    print(f"Rows after deduplication:  {after_count}")
    print(f"Merged file saved to: {output_csv}")

if __name__ == "__main__":
    ROOT_DIR = "data/all_years_data"
    OUTPUT_CSV = "data/merged.csv"   
    aggregate_metropolitan_data(ROOT_DIR, OUTPUT_CSV)
