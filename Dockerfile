FROM quay.io/astronomer/astro-runtime:9.4.0
# Install necessary Python libraries
RUN pip install gspread oauth2client pandas