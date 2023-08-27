
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Step 1: Send a GET request and save the HTML data
url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"'
response = requests.get(url)
html_data = response.text

# Step 2: Parse the HTML data using Beautiful Soup
soup = BeautifulSoup(html_data, 'html.parser')

# Step 3: Extract the table with Tesla Quarterly Revenue and create a DataFrame
tesla_revenue = None

tables = soup.find_all('table')
for table in tables:
    if "Tesla Quarterly Revenue" in str(table):
        tesla_revenue = pd.read_html(str(table))[0]

if tesla_revenue is not None:
    # Rename columns and clean the Revenue column
    tesla_revenue.columns = ["Date", "Revenue"]
    tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace('$', '').str.replace(',', '').astype(float)

    # Step 4: Clean rows with empty strings or NaN in Revenue column
    tesla_revenue = tesla_revenue.dropna(subset=["Revenue"])

    # Step 6: Insert data into SQLite
    conn = sqlite3.connect("Tesla.db")
    cursor = conn.cursor()

    data_to_insert = [tuple(x) for x in tesla_revenue.values]
    cursor.executemany("INSERT INTO tesla_revenue (Date, Revenue) VALUES (?, ?)", data_to_insert)

    conn.commit()
    conn.close()

    # Step 7: Connect to SQLite (not mentioned in your steps, but assumed)
    conn = sqlite3.connect("Tesla.db")
    cursor = conn.cursor()

    # Step 9: Retrieve data from the database
    cursor.execute("SELECT * FROM tesla_revenue")
    retrieved_data = cursor.fetchall()

    # Step 10: Create a plot to visualize the data
    retrieved_df = pd.DataFrame(retrieved_data, columns=["Date", "Revenue"])
    plt.figure(figsize=(10, 6))
    plt.plot(retrieved_df["Date"], retrieved_df["Revenue"], marker='o')
    plt.title("Tesla Quarterly Revenue")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    conn.close()
else:
    print("No Tesla Quarterly Revenue table found.")
