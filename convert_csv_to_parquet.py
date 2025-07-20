
import pandas as pd

def convert_csv_to_parquet(csv_path, parquet_path):
    """
    Converts a CSV file to a Parquet file.

    Args:
        csv_path (str): The path to the input CSV file.
        parquet_path (str): The path to the output Parquet file.
    """
    print(f"Reading CSV file from: {csv_path}")
    # Specify dtype='unicode' to handle mixed type columns
    df = pd.read_csv(csv_path, dtype='unicode', low_memory=False)
    print(f"Writing Parquet file to: {parquet_path}")
    df.to_parquet(parquet_path, engine='pyarrow')
    print("Conversion complete.")

if __name__ == "__main__":
    # Define the input and output file paths
    input_csv = 'all_news.csv'
    output_parquet = 'merged_all_news.parquet'

    # Perform the conversion
    convert_csv_to_parquet(input_csv, output_parquet)
