import pandas as pd
import psycopg2
def clear_all_tables(conn):
    """
    Clears all values from the tables in the database.
    """
    cur = conn.cursor()

    # SQL commands to truncate all tables
    truncate_competition_log = 'TRUNCATE TABLE "CompetitionLog" CASCADE;'
    truncate_competitors = 'TRUNCATE TABLE "Competitors" CASCADE;'
    truncate_federations = 'TRUNCATE TABLE "Federations" CASCADE;'
    truncate_users = 'TRUNCATE TABLE "Users" CASCADE;'

    try:
        # Execute the truncate table commands
        cur.execute(truncate_competition_log)
        cur.execute(truncate_competitors)
        cur.execute(truncate_federations)
        cur.execute(truncate_users)
        conn.commit()
        print("All tables cleared successfully.")
    except Exception as e:
        print(f"Error clearing tables: {e}")
        conn.rollback()
    finally:
        cur.close()

def load_csv_to_postgres(file_path, conn):
    # Load the CSV into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Clean the data to match the SQL schema
    df['Sex'] = df['Sex'].astype(str).str[0]  # Get the first character for sex (M, F)
    df['WeightClassKg'].fillna(0, inplace=True)  # Handle missing data in WeightClass
    df['Age'].fillna(0, inplace=True)            # Handle missing data in Age

    cur = conn.cursor()

    # Insert data into Competitors table
    for index, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO "Competitors" ("Country", "WeightClass", "Sex", "Name", "C_ID", "age")
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT ("C_ID") DO NOTHING;
                """, (row['Country'], row['WeightClassKg'], row['Sex'], row['Name'], index + 1, row['Age']))
        except Exception as e:
            print(f"Error inserting into Competitors on row {index} with data {row}: {e}")
            conn.rollback()  # Rollback the transaction to avoid blocking other inserts

    # Insert data into CompetitionLog table
    for index, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO "CompetitionLog" ("C_ID", "Rank", "Equipped", "Date", "Deadlift", "Bench", "Squat", "WeightClass", "Total", "GLP", "FEDERATION_NAME")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (index + 1, row['Rank'], row['Equipment'], row['Date'], row['Best3DeadliftKg'], row['Best3BenchKg'], row['Best3SquatKg'], row['WeightClassKg'], row['TotalKg'], row['Goodlift'], row["Federation"]))
        except Exception as e:
            print(f"Error inserting into CompetitionLog on row {index} with data {row}: {e}")
            conn.rollback()  # Rollback the transaction

    # Commit changes and close cursor
    conn.commit()
    cur.close()

    print("Data inserted successfully.")

# Example of an existing connection to the PostgreSQL database
conn = psycopg2.connect("dbname=liftmaster user=baazjhaj")
clear_all_tables(conn)
# Specify the path to your CSV file
file_path = '/Users/baazjhaj/Downloads/openipf-2024-10-05/openipf.csv'

# Call the function to load the data using the active connection
load_csv_to_postgres(file_path, conn)

# Close the connection when done
conn.close()
