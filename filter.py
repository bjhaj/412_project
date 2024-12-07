import pandas as pd

def sort_and_add_rank(file_path, output_file):
    try:
        # Load the CSV file with a generic delimiter (comma)
        df = pd.read_csv(file_path)

        # Sort the dataset based on the 'Goodlift' column in descending order
        df_sorted = df.sort_values(by='Goodlift', ascending=False)

        # Add a new column 'Rank' which is the row number
        df_sorted['Rank'] = range(1, len(df_sorted) + 1)

        # Save the sorted dataframe with rank to a new file
        df_sorted.to_csv(output_file, index=False)

        print(f"Sorted CSV with Rank saved to {output_file}")
    
    except pd.errors.ParserError as e:
        print(f"Parsing error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = '/Users/baazjhaj/Downloads/openipf-2024-10-05/openipf-2024-10-05-c40afca0.csv'
output_file = '/Users/baazjhaj/Downloads/openipf-2024-10-05/openipf.csv'
sort_and_add_rank(file_path, output_file)
