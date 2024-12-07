import psycopg2
import bcrypt
import math
import random

# Dictionary to store coefficients based on sex and competition type
coefficients = {
    'M': {
        'equipped_powerlifting': (1236.25115, 1449.21864, 0.01644),
        'classic_powerlifting': (1199.72839, 1025.18162, 0.00921),
        'equipped_bench_press': (381.22073, 733.79378, 0.02398),
        'classic_bench_press': (320.98041, 281.40258, 0.01008),
    },
    'F': {
        'equipped_powerlifting': (758.63878, 949.31382, 0.02435),
        'classic_powerlifting': (610.32796, 1045.59282, 0.03048),
        'equipped_bench_press': (221.82209, 357.00377, 0.02937),
        'classic_bench_press': (142.40398, 442.52671, 0.04724),
    }
}

# Function to calculate GLP using provided code
def calculate_glp(sex, competition_type, body_weight, result):
    A, B, C = coefficients[sex][competition_type]
    exponent = 100 / (A - (B * math.exp(C * -1 * body_weight)))
    return round(result * exponent, 6)

# Function to generate a unique C_ID starting with "user" for the Users table
def generate_user_cid(cur):
    while True:
        # Generate a C_ID in the format 'userXXXX' where XXXX is a random number between 1000 and 9999
        user_cid = "user" + str(random.randint(1000, 9999))
        
        # Check if this C_ID already exists in the Users table
        cur.execute('SELECT COUNT(*) FROM "Users" WHERE "C_ID" = %s', (user_cid,))
        result = cur.fetchone()
        
        if result[0] == 0:  # If no rows were returned, this C_ID is unique
            return user_cid

# Function to insert a user and their competition data
def insert_user(username, password, sex, competition_type, body_weight, deadlift, bench, squat, weight_class, federation):
    try:
        # Hash the password

        # Calculate the total lift and GLP
        total = deadlift + bench + squat
        print("total is ", total)
        glp = calculate_glp(sex, competition_type, body_weight, total)
        print("glp is ", glp)
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect("dbname=liftmaster user=baazjhaj")

        # Create a cursor object
        cur = conn.cursor()

        # Step 1: Generate a unique C_ID that starts with "user"
        c_id = generate_user_cid(cur)

        # Step 2: Insert the competitor into the Competitors table
        insert_competitor_query = """
        INSERT INTO "Competitors" 
        ("C_ID", "Country", "WeightClass", "Sex", "Name", "age")
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_competitor_query, (c_id, 'Unknown', weight_class, sex, username, 25))  # Example data

        # Step 3: Insert competition data into the CompetitionLog table using the unique C_ID
        insert_competition_query = """
        INSERT INTO "CompetitionLog" 
        ("C_ID", "Rank", "Equipped", "Date", "Deadlift", "Bench", "Squat", "WeightClass", "Total", "GLP", "FEDERATION_NAME")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_competition_query, (c_id, 1, competition_type, '2024-12-01', deadlift, bench, squat, weight_class, total, glp, federation))

        # Step 4: Insert user into the Users table with Password, Username, and C_ID
        insert_user_query = """
        INSERT INTO "Users" 
        ("Username", "Password", "C_ID")
        VALUES (%s, %s, %s);
        """
        cur.execute(insert_user_query, (
            username, password, c_id
        ))

        # Commit the transaction
        conn.commit()

        print(f"User '{username}' inserted successfully with C_ID {c_id} and calculated GLP of {glp}.")
        return c_id, username
    except Exception as e:
        print(f"An error occurred: {e}")

    

# Function to get user input dynamically
def get_user_input():
    username = input("Enter username: ")
    password = input("Enter password: ")
    sex = input("Enter sex (M/F): ")
    competition_type = input("Enter competition type (e.g., classic_powerlifting, equipped_powerlifting): ")
    body_weight = float(input("Enter body weight (kg): "))
    deadlift = float(input("Enter deadlift weight (kg): "))
    bench = float(input("Enter bench press weight (kg): "))
    squat = float(input("Enter squat weight (kg): "))
    weight_class = input("Enter weight class (e.g., '85'): ")
    federation = input("Enter federation (e.g., 'IPF'): ")

    return username, password, sex, competition_type, body_weight, deadlift, bench, squat, weight_class, federation

# Main loop to insert users dynamically
'''while True:
    # Get input data from user
    user_data = get_user_input()

    # Insert the user into the database
    insert_user(*user_data)

    # Ask if they want to add another user
    if input("Do you want to add another user? (yes/no): ").lower() != 'yes':
        break'''
