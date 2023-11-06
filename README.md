# Data Engineering ETL Project with PostgreSQL, Airflow, Astronomer, Docker, Python, and Google Sheets API

## Prerequisites

Before you begin setting up this Data Engineering ETL project, ensure you have the following prerequisites in place:

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed.
- Docker extension installed in Visual Studio Code.
- [Astro CLI](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart) installed. You can use the following command to install it:

  ```bash
  brew install astro
  ```

To verify that you have installed the correct version of Astro CLI, run the following command:

```bash
astro version
```

Create a dedicated folder where you want to set up your Astro project and initialize it by running the following command:

```bash
astro dev init

To start Airflow within the Astro project, use the following command:

```bash
astro dev start

## Setting Up PostgreSQL in Airflow

Open the Airflow web UI.
Navigate to the "Admin" tab located in the top menu of the Airflow UI.
Under the "Admin" tab, select "Connections" from the dropdown menu.
On the Connections page, click the "Create" button to add a new connection.
In the "Conn Id" field, use "postgres_connection" as this ID is referenced in the DAGs and scripts.
Choose "Postgres" from the "Conn Type" dropdown to specify that this connection is for PostgreSQL.
Fill in the necessary connection details:
Host: Use Host.docker.internal
Schema: The default schema to use when interacting with the database.
Login: Your PostgreSQL username.
Password: Your PostgreSQL password.
Port: Use 5432 (default for PostgreSQL).

8. After filling in the connection details, click the "Save" button to create the connection.

PostgreSQL database connection is now set up in Airflow

To access Google Sheets via the Google Sheets API, follow these steps:

Refer to the official documentation at this link to enable API access for your project.
Obtain the JSON file with authentication details after completing the steps in the link.
Upload the JSON file to the following location: secrets/airflow-poc-403917-e3d99f34c1f6.json.

