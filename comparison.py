import pandas as pd
from datetime import datetime
import time

# Load the current and previous scrapes
current_scrape = pd.read_csv('/Users/christianburgin/Documents/scraping/dealerscrape/product_details2024-07-23.csv')
previous_scrape = pd.read_csv('/Users/christianburgin/Documents/scraping/dealerscrape/product_details2024-07-04.csv')

# Convert URLs to set for comparison
current_urls = set(current_scrape['url'])
previous_urls = set(previous_scrape['url'])

# Detect new machines
new_machines = current_urls - previous_urls

# Detect removed machines
removed_machines = previous_urls - current_urls

# Detect price changes
price_changes = []

for url in current_urls & previous_urls:
    current_price = current_scrape[current_scrape['url'] == url]['Prix'].values[0]
    previous_price = previous_scrape[previous_scrape['url'] == url]['Prix'].values[0]
    if current_price != previous_price:
        price_changes.append({
            'url': url,
            'old_price': previous_price,
            'new_price': current_price
        })

# Output results
# print(f"New machines: {new_machines}")
# print(f"Removed machines: {removed_machines}")
# print(f"Price changes: {price_changes}")

today_date = datetime.now().strftime("%Y-%m-%d")

changes_df = pd.DataFrame(price_changes)

# Optionally save changes to a CSV or Google Sheet

file_path = f'/Users/christianburgin/Documents/scraping/comparisonengine/results/results_{today_date}.csv'
changes_df.to_csv(file_path, index=False)

print(f"Changes saved to {file_path}")
# If using Google Sheets, use gspread or similar library to update the sheet
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Authenticate and initialize the Google Sheets API
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('/path/to/creds.json', scope)
# client = gspread.authorize(creds)

# # Open the Google Sheet
# sheet = client.open("Machine Listings Changes").sheet1

# # Clear the sheet and update with new data
# sheet.clear()
# sheet.update([changes_df.columns.values.tolist()] + changes_df.values.tolist())
