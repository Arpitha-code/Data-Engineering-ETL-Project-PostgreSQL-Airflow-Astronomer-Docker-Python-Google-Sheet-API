# Data Engineering ETL Project with PostgreSQL, Airflow, Astronomer, Docker, Python, and Google Sheets API

## Prerequisites

## Setting up Apache Airflow project through Astronomer

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
  ```

To start Airflow within the Astro project, use the following command:

  ```bash
  astro dev start
  ```

## Setting Up PostgreSQL in Airflow

1. Open the Airflow web UI.
2. Navigate to the "Admin" tab located in the top menu of the Airflow UI.
3. Under the "Admin" tab, select "Connections" from the dropdown menu.
4. On the Connections page, click the "Create" button to add a new connection.
5. In the "Conn Id" field, use "**postgres_connection**" as this ID is referenced in the DAGs and scripts.
6. Choose "Postgres" from the "Conn Type" dropdown to specify that this connection is for PostgreSQL.
7. Fill in the necessary connection details:
  -Host: Use host.docker.internal
  -Schema: The default schema to use when interacting with the database
  -Login: Your PostgreSQL username
  -Password: Your PostgreSQL password
  -Port: Use 5432 (default for PostgreSQL)

8. After filling in the connection details, click the "Save" button to create the connection.

PostgreSQL database connection is now set up in Airflow

## To access Google Sheets via service account, follow these steps:

## Enable API Access for a Project

1. Head to Google Developers Console and create a new project (or select the one you already have).
2. In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.
3. In the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it.

A service account is a special type of Google account intended to represent a non-human user that needs to authenticate and be authorized to access data in Google APIs.

Since it’s a separate account, by default it does not have access to any spreadsheet until you share it with this account. Just like any other Google account.

**Here’s how to get one:**

1. Enable API Access for a Project if you haven’t done it yet.
2. Go to “APIs & Services > Credentials” and choose “Create credentials > Service account key”.
3. Fill out the form
4. Click “Create” and “Done”.
5. Press “Manage service accounts” above Service Accounts.
6. Press on ⋮ near recently created service account and select “Manage keys” and then click on “ADD KEY > Create new key”.
7. Select JSON key type and press “Create”.
   
You will automatically download a JSON file with credentials. It may look like this:

8. Upload the downloaded JSON file to the following location in the project folder: **secrets/airflow-poc-403917-e3d99f34c1f6.json **, Also, in the next step you’ll need the value of client_email from this file.
9. Very important! Go to your spreadsheet and share it with a client_email from the step above. Just like you do with any other Google account. If you don’t do this, you’ll get a gspread.exceptions.SpreadsheetNotFound exception when trying to access this spreadsheet from your application or a script.

For more details refer to the official documentation at this [link](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project) 
