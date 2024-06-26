# Data Warehouse For Tesla Stock Price Prediction
![image](https://github.com/wdh70743/Data-System_Project/assets/80554373/2accef2c-67e1-449f-b2dd-be433cd17b05)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a Windows/Linux/Mac machine.
- You have installed Python 3.12.
- You have an internet connection.
- You have a SQL database on Azure

## Installing the ODBC Driver for SQL Server

1. Download the ODBC Driver for SQL Server from the [official Microsoft website](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16&redirectedfrom=MSDN).
2. Follow the installation instructions provided on the website to install the driver on your machine.

## Installing Requirements

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/wdh70743/Data-System_Project.git
2. Navigate to the project directory:
   ```bash
   cd your-repository
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt

## Setting Up Environment Variables
1. Create a .streamlit file in the project directory
2. Create the secrets.toml file in a text editor and add the necessary environment variables. For example:
   ```bash
   DB_USERNAME=
   DB_PASSWORD=
   DB_HOST=
   DATABASE=
   
## Running the Application

```bash
streamlit run app.py

