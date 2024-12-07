import pandas as pd

# Load the CSV file
df = pd.read_csv('/Users/baazjhaj/Downloads/openipf-2024-10-05/openipf.csv')

# Get the first 5 rows
first_five_rows = df.head()

# Write the first 5 rows to a text file
with open('ipfoutput.txt', 'w') as file:
    file.write(first_five_rows.to_string(index=False))

