import gspread
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Connect to PostgreSQL
postgres_hook = PostgresHook(postgres_conn_id='postgres_connection')
connection = postgres_hook.get_conn()
cursor = connection.cursor()

def read_google_sheet_data():

    """
    Read data from a Google Sheet and return it as a DataFrame.

    This function uses the gspread library to connect to the Google Sheet and retrieve data.
    The retrieved data is then converted into a DataFrame, and some data cleaning and formatting are applied.
    """
    try:
        # Google Sheet and tab names
        GSHEET_NAME = 'Spotify Revenue and Cost Analysis'
        TAB_NAME = 'Quarterly Financial Data'

        # Authenticate with the Google Sheets API using service account credentials
        gc = gspread.service_account(filename='secrets/airflow-poc-403917-e3d99f34c1f6.json')

        # Open the specified Google Sheet by its name & access the tab within the gsheet
        sh = gc.open(GSHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)
        
        # Retrieve data and format
        df = pd.DataFrame(worksheet.get_all_records())
        df.columns = df.columns.str.lower()
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        df.columns = df.columns.str.replace(' ', '_')

        print("Data from Google Sheet read successfully.")

        return df
    
    except Exception as e:
        raise Exception(f"Error reading Google Sheet data: {e}")

def get_postgres_data_type(series):
    """
    Get the PostgreSQL data type based on a Pandas series.
    """
    dtype = series.dtype
    if dtype == 'int64':
        return 'INTEGER'
    elif dtype == 'float64':
        return 'DECIMAL(10, 2)'  
    elif dtype == 'bool':
        return 'BOOLEAN'
    elif dtype == 'datetime64[ns]':
        return 'DATE'  
    else:
        return 'TEXT' 

def  create_postgres_table():

    """
    Create a PostgreSQL table named spotify_revenue if it doesn't already exist.

    This function defines the schema of the table and executes a SQL query to create it.
    """

    try:

        df = read_google_sheet_data()
        table_name = 'spotify_revenue'

        # Create the table with inferred schema using the DataFrame's data types
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                "date" DATE PRIMARY KEY,  -- Date column as primary key
            {', '.join([f'"{col}" {get_postgres_data_type(df[col])}' for col in df.columns if col != 'date'])}
            )
        """
         # Execute the query
        cursor.execute(create_table_query)
        connection.commit()
        
        print("Table 'spotify_revenue' created.")
        
    except Exception as e:
        raise Exception(f"Error creating table: {e}")

def upsert_to_postgres_table():

    """
    Insert or update data from a DataFrame into the spotify_revenue table in PostgreSQL.

    This function retrieves data from the Google Sheet using read_google_sheet_data function
    and inserts or updates records in the spotify_revenue table based on the date column.
    """
    try:
        df = read_google_sheet_data()
        
        for index, row in df.iterrows():
                # Check if a row with the same date exists in the table
                cursor.execute("SELECT * FROM spotify_revenue WHERE date = %s", (row['date'], ))
                existing_row = cursor.fetchone()

                if existing_row:
                    # Compare the columns to determine if any value is different
                    is_different = any(existing_row[i] != row[i] for i in range(len(row)))

                    if is_different:
                        # If any value is different, update the entire row
                        update_statement = f"""
                            UPDATE spotify_revenue
                            SET {', '.join([f"{col} = %s" for col in row.index])}
                            WHERE date = %s;
                        """
                        cursor.execute(update_statement, (*row.values, row['date']))
                    # If all values are the same, do nothing (no update is needed)
                else:
                    # If no row with the same date exists, insert a new row
                    insert_statement = f"""
                        INSERT INTO spotify_revenue (
                            {', '.join(row.index)}
                        ) VALUES (
                            {', '.join(['%s'] * len(row))}
                        );
                    """
                    cursor.execute(insert_statement, row)

        print("Data inserted/updated in 'spotify_revenue' table.")

    except Exception as e:
            # Log the error message
            raise Exception(f"Error inserting/updating row: {e}")

def write_gsheet_data_to_postgres():

    """
    Main function to create table, read data, insert into database, commit, and close connection.
    """
    create_postgres_table()
    upsert_to_postgres_table()
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    write_gsheet_data_to_postgres()