# Data-Engineering-ETL-Project-PostgreSQL-Airflow-Astronomer-Docker-Python-Google-Sheet-API

Authentication - To access spreadsheets via Google Sheets API, you can also go through this link - https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project

To access spreadsheets via Google Sheets API you need to authenticate and authorize your application.

If you plan to access spreadsheets on behalf of a bot account use Service Account.

If you’d like to access spreadsheets on behalf of end users (including yourself) use OAuth Client ID.

**Enable API Access for a Project**

Head to Google Developers Console and create a new project (or select the one you already have).
In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.
In the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it.
For Bots: Using Service Account

A service account is a special type of Google account intended to represent a non-human user that needs to authenticate and be authorized to access data in Google APIs [sic].

Since it’s a separate account, by default it does not have access to any spreadsheet until you share it with this account. Just like any other Google account.

**Here’s how to get one:**

Enable API Access for a Project if you haven’t done it yet.
Go to “APIs & Services > Credentials” and choose “Create credentials > Service account key”.
Fill out the form
Click “Create” and “Done”.
Press “Manage service accounts” above Service Accounts.
Press on ⋮ near recently created service account and select “Manage keys” and then click on “ADD KEY > Create new key”.
Select JSON key type and press “Create”

Remember the path to the downloaded credentials file. Also, in the next step you’ll need the value of client_email from this file.

Very important! Go to your spreadsheet and share it with a client_email from the step above. Just like you do with any other Google account. If you don’t do this, you’ll get a gspread.exceptions.SpreadsheetNotFound exception when trying to access this spreadsheet from your application or a script.
