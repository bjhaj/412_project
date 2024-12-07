import psycopg2

# Database connection setup
def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database.
    
    Returns:
        psycopg2.extensions.connection: A database connection object.
    """
    try:
        connection = psycopg2.connect("dbname=liftmaster user=baazjhaj")
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

def execute_query(query, params=None):
    """
    Executes a SQL query on the PostgreSQL database.
    
    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters for the query.
    
    Returns:
        list: Query results as a list of tuples, or None if an error occurs.
    """
    connection = connect_to_db()
    if not connection:
        return None
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
    
        cursor.close()
        connection.close()
        return result
    except Exception as e:
        print("Error executing query:", e)
        return None

import psycopg2
from psycopg2.extensions import AsIs

def fetch_comparison_results(user_id):
    """
    Fetches the comparison results for a given user ID.

    Args:
        user_id (str): The ID of the target user.

    Returns:
        list: Query results as a list of tuples, or None if an error occurs.
    """
    # Construct the query using an f-string
    comparison_query = f"""
    (SELECT *
     FROM "CompetitionLog"
     WHERE "GLP" < (SELECT "GLP" FROM "CompetitionLog" WHERE "C_ID" = '{user_id}')
       AND "C_ID" NOT LIKE 'user%'
       AND "GLP" IS NOT NULL
     ORDER BY "GLP" DESC
     LIMIT 5)
    UNION ALL
    (SELECT *
     FROM "CompetitionLog"
     WHERE "C_ID" = '{user_id}')
    UNION ALL
    (SELECT *
     FROM "CompetitionLog"
     WHERE "GLP" > (SELECT "GLP" FROM "CompetitionLog" WHERE "C_ID" = '{user_id}')
       AND "C_ID" NOT LIKE 'user%'
       AND "GLP" IS NOT NULL
     ORDER BY "GLP" ASC
     LIMIT 5)
    ORDER BY "GLP" DESC;
    """
    try:
        # Establish database connection
        conn = psycopg2.connect("dbname=liftmaster user=baazjhaj")
        cur = conn.cursor()

        # Debugging: Print the query being executed
        print("Query to Execute:", comparison_query)

        # Execute the query
        cur.execute(comparison_query)
        results = cur.fetchall()

        # Print results
        print("Results:", results)

        # Close resources
        cur.close()
        conn.close()

        return results
    except Exception as e:
        print("Error executing query:", e)
        return None




def fetch_highest_total():
    """
    Fetches the competitor with the highest total score.
    
    Returns:
        list: Query results as a list of tuples, or None if an error occurs.
    """
    highest_total_query = """
    SELECT "CompetitionLog"."C_ID", "Competitors"."Name", MAX("CompetitionLog"."Total") AS "Total"
    FROM "CompetitionLog"
    JOIN "Competitors" ON "CompetitionLog"."C_ID" = "Competitors"."C_ID"
    WHERE "CompetitionLog"."C_ID" NOT LIKE 'user%' AND "CompetitionLog"."Total" IS NOT NULL
    GROUP BY "CompetitionLog"."C_ID", "Competitors"."Name"
    ORDER BY "Total" DESC
    LIMIT 1;
    """
    return execute_query(highest_total_query)

def fetch_lifter_stats(user_id):
    """
    Fetches the lifter stats for a given user ID.
    
    Args:
        user_id (str): The ID of the target user.
    
    Returns:
        list: Query results as a list of tuples, or None if an error occurs.
    """
    lifter_stats_query = """
    SELECT "Bench", "Deadlift", "Squat"
    FROM "CompetitionLog"
    WHERE "C_ID" = %s;
    """
    return execute_query(lifter_stats_query, (user_id,))
