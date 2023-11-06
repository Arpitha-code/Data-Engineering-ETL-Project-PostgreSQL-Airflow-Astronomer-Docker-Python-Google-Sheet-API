# Data Engineering ETL Project with PostgreSQL, Airflow, Astronomer, Docker, Python, and Google Sheets API

## Prerequisites

Before you begin setting up this Data Engineering ETL project, ensure you have the following prerequisites in place:

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed.
- Docker extension installed in Visual Studio Code.
- [Astro CLI](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart) installed. You can use the following command to install it:

  ```bash
  brew install astro

To verify that the correct Astro CLI version was installed, run:

astro version

create a folder where you wnat the astro project set up and run the below command

astro dev init

to spin up the airflow run the below code 
astro dev start

## Setting Up PostgreSQL in Airflow

1. Open the Airflow web UI.

2. In the Airflow UI, navigate to the "Admin" tab located in the top menu.

3. From the dropdown menu under "Admin," select "Connections."

4. On the Connections page, click the "Create" button to add a new connection.

5. In the "Conn Id" field, fill protgres_connection as this ID is referenced in the connection in the DAGs and scripts.

6. Choose "Postgres" from the "Conn Type" dropdown to specify that this connection is for PostgreSQL.

7. Fill in the necessary connection details:
   - **Host**: **Host.docker.internal**
   - **Schema**: The default schema to use when interacting with the database.
   - **Login**: Your PostgreSQL username.
   - **Password**: Your PostgreSQL password.
   - **Port**: 5432(default for postgres)

8. After filling in the connection details, click the "Save" button to create the connection.

PostgreSQL database connection is now set up in Airflow


Authentication - To access google sheets via Google Sheets API, follow the steps in the link - https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project

Upload the JSON file details obtain after completing the steps through the link to secrets/airflow-poc-403917-e3d99f34c1f6.json file

