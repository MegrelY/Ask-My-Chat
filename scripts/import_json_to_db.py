import json
import psycopg2

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect("dbname=Chat_db user=postgres password=goory1985")
    cursor = conn.cursor()

    print("Connected to the database.")

    # Check if the table exists
    cursor.execute("SELECT to_regclass('public.web_data2')")
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        print("Table web_data2 does not exist. Creating the table...")
        cursor.execute("""
            CREATE TABLE web_data2 (
                id SERIAL PRIMARY KEY,
                json_data JSONB
            );
        """)
        conn.commit()
        print("Table web_data2 created successfully.")
    else:
        print("Table web_data2 exists.")

    # Load the JSON data from the file with UTF-8 encoding
    with open('D:/Coding/Ask_My_Chat/data-folder/scraped_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Insert each JSON object into the table
    for item in data:
        print("Inserting item:", item)  # Debugging: Print each JSON object before insertion
        cursor.execute(
            """
            INSERT INTO web_data2 (json_data)
            VALUES (%s)
            """,
            [json.dumps(item)]  # Convert the dictionary to a JSON string
        )

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print("Data successfully imported into the database.")

except Exception as e:
    print("An error occurred:", e)
