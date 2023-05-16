import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import datetime

# Create a connection string
def conn_load_sql(df_cleaned):
    # SQL database details
    server = 'invoiceparser-sqlserver.database.windows.net'
    database = 'invoiceparser-sqldb'
    username = 'invoiceparser'
    password = "sU3g)2ZUG6FF,N',9u3r"
    conn_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    # Create a SQLAlchemy engine object
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_string))
    # Extracted data from docs
    df = df_cleaned.copy()
    df = df[["Attribute","Value"]]
    df = df.set_index("Attribute").T
    df = df[["InvoiceId","VendorName", "InvoiceDate", "InvoiceTotal"]]
    current_time = datetime.datetime.now()
    df.loc["Value","DateCreated"] = current_time
    new_order = ["InvoiceId","VendorName", "InvoiceDate", "InvoiceTotal", 'DateCreated']
    # Reorder the columns using reindex()
    df = df.reindex(columns=new_order)
    # Load the table into your Azure SQL database
    # Name of the existing table to append to
    existing_table = 'invoke_invoice_database'
    df_cleaned.to_sql(existing_table, engine, index=False, if_exists='append')
    engine.dispose()
    return df_cleaned

def dataframeSetup(updatedInfo):
    df = updatedInfo.copy()
    df = df[["Attribute","Value"]]
    df = df.set_index("Attribute").T
    df = df[["InvoiceId","VendorName", "InvoiceDate", "InvoiceTotal"]]
    current_time = datetime.datetime.now()
    df.loc["Value","DateCreated"] = current_time
    new_order = ["InvoiceId","VendorName", "InvoiceDate", "InvoiceTotal", 'DateCreated']
    # Reorder the columns using reindex()
    df_cleaned = df.reindex(columns=new_order)
    return df_cleaned

def parse_submitbutton():
    submitbutton = st.button(
        label="Save Document",
        key="parse_submitbutton", 
        help="Click to publish the document"
        )
    return submitbutton

def view_df():
    import pyodbc
    # SQL database details
    server = 'invoiceparser-sqlserver.database.windows.net'
    database = 'invoiceparser-sqldb'
    username = 'invoiceparser'
    password = "sU3g)2ZUG6FF,N',9u3r"
    cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    # Define the SQL query to retrieve the data from the table
    query = 'SELECT * FROM invoke_invoice_database'
    # Use pandas to read the data from the database into a DataFrame
    df_view = pd.read_sql(query, cnxn)
    return df_view