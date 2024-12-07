import psycopg2

# Function to update a user's lifts (bench, deadlift, squat) in the CompetitionLog table
def update_user_lifts(c_id, new_bench, new_deadlift, new_squat):
    try:
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect("dbname=liftmaster user=bj")
        
        # Create a cursor object
        cur = conn.cursor()

        # SQL query to update the user's lifts
        update_lifts_query = """
        UPDATE "CompetitionLog"
        SET "Bench" = %s, "Deadlift" = %s, "Squat" = %s, "Total" = %s
        WHERE "C_ID" = %s;
        """
        # Calculate the new total
        total = new_bench + new_deadlift + new_squat

        # Execute the query with the new values
        cur.execute(update_lifts_query, (new_bench, new_deadlift, new_squat, total, c_id))

        # Commit the transaction
        conn.commit()

        print(f"Lifts updated for user with C_ID {c_id}.")

    except Exception as e:
        print(f"An error occurred while updating lifts: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

# Function to delete a user from the database
def delete_user(c_id):
    try:
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect("dbname=liftmaster user=baazjhaj")
        
        # Create a cursor object
        cur = conn.cursor()

        # SQL queries to delete the user from the Users, Competitors, and CompetitionLog tables
        delete_from_users = 'DELETE FROM "Users" WHERE "C_ID" = %s;'
        delete_from_competitors = 'DELETE FROM "Competitors" WHERE "C_ID" = %s;'
        delete_from_competition_log = 'DELETE FROM "CompetitionLog" WHERE "C_ID" = %s;'

        # Execute the deletion queries
        cur.execute(delete_from_users, (c_id,))
        cur.execute(delete_from_competitors, (c_id,))
        cur.execute(delete_from_competition_log, (c_id,))

        # Commit the transaction
        conn.commit()

        print(f"User with C_ID {c_id} deleted successfully.")

    except Exception as e:
        print(f"An error occurred while deleting user: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

# Function to get user input for updating lifts
def get_update_input():
    c_id = input("Enter the C_ID of the user to update: ")
    new_bench = float(input("Enter new bench press weight (kg): "))
    new_deadlift = float(input("Enter new deadlift weight (kg): "))
    new_squat = float(input("Enter new squat weight (kg): "))
    return c_id, new_bench, new_deadlift, new_squat

# Function to get user input for deleting a user
def get_delete_input():
    c_id = input("Enter the C_ID of the user to delete: ")
    return c_id

# Main loop to update lifts or delete users
'''while True:
    action = input("Do you want to update lifts or delete a user? (update/delete/exit): ").lower()

    if action == 'update':
        user_data = get_update_input()
        update_user_lifts(*user_data)

    elif action == 'delete':
        c_id = get_delete_input()
        delete_user(c_id)

    elif action == 'exit':
        break

    else:
        print("Invalid action. Please enter 'update', 'delete', or 'exit'.")'''
