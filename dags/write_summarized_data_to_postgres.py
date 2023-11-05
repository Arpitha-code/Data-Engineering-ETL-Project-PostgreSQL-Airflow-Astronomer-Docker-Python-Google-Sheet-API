import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Connect to PostgreSQL
postgres_hook = PostgresHook(postgres_conn_id='postgres_connection')
connection = postgres_hook.get_conn()
cursor = connection.cursor()

def calculate_return_metrics():

    """
    This function retrieves data from the 'spotify_revenue' table, calculates return metrics,
    and returns the summary as a DataFrame.
    """
    try:
        # Query to extract data from PostgreSQL
        query = """
        SELECT * 
        FROM spotify_revenue
        """
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Get column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Extract the data into a DataFrame and set column headers
        df = pd.DataFrame(result, columns=column_names)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        # Extract the year from the 'Date' column
        df['year'] = df['date'].dt.year

        # Group by 'Year' and calculate sum and mean of columns
        summary_df= df.groupby('year').agg({
        'total_revenue': 'sum',
        'cost_of_revenue': 'sum',
        'gross_profit': 'sum',
        'premium_arpu': 'mean',
        'sales_and_marketing_cost':'sum',
        'research_and_development_cost':'sum',
        'general_and_administrative_cost':'sum'
        }).reset_index()

        # Calculate 'Overhead Costs' as the sum of Sales and Marketing Cost, Research and Development Cost, and General and Administrative Cost
        summary_df['overhead_costs'] = summary_df['sales_and_marketing_cost'] + summary_df['research_and_development_cost'] + summary_df['general_and_administrative_cost']

        # Calculate 'Net Profit' as the difference between 'Gross Profit' and 'Overhead Costs'
        summary_df['net_profit'] = summary_df['gross_profit'] - summary_df['overhead_costs']

        # Calculate ROI - (Net Profit / Cost of Revenue) x 100
        summary_df['return_of_investment'] = (summary_df['net_profit'] / summary_df['cost_of_revenue']) * 100

        # Calculate the return over time (year-over-year percentage change in total revenue)
        summary_df['return_over_time'] = (summary_df['total_revenue'].pct_change() * 100).fillna(0)

        summary_df['return_of_investment'] = summary_df['return_of_investment'].apply(lambda x: f'{x:.2f}%')
        summary_df['return_over_time'] = summary_df['return_over_time'].apply(lambda x: f'{x:.2f}%')

        print("'Return Metrics' calculated successfully.")
        return summary_df
    
    except Exception as e:
        # Handle the exception
        raise Exception(f"Error calculating Return Metrics: {e}")

def write_to_sheet():

    """
    Writes summary data to Google Sheets.

    This function retrieves summary data using 'calculate_return_metrics' function,
    writes it to a specified Google Sheet tab
    """
    try:
        GSHEET_NAME = 'Spotify Revenue and Cost Analysis'
        gc = gspread.service_account(filename='secrets/airflow-poc-403917-e3d99f34c1f6.json')
        sh = gc.open(GSHEET_NAME)

        # Write summary data to the first Google Sheet tab
        TAB_NAME = 'Return Metrics'
        df = calculate_return_metrics()
        worksheet = sh.worksheet(TAB_NAME)
        worksheet.clear()
        set_with_dataframe(worksheet, df, include_column_header=True)

        # Write summary data to the second Google Sheet tab
        GSHEET_NAME = 'Arpitha - BI Engineer Technical Exercise (FINAL)'
        sh = gc.open(GSHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)
        worksheet.clear()
        set_with_dataframe(worksheet, df, include_column_header=True)
    
        print("Summary data written to Google Sheets.")

    except Exception as e:
        raise Exception(f"Error writing to Google Sheets: {e}")

def write_summarized_data_to_google_sheet():
    
    """
    Orchestrates writing summarized data to Google Sheets.
    """
    write_to_sheet()
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    write_summarized_data_to_google_sheet()