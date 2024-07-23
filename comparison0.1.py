import pandas as pd
from datetime import datetime


# Load the current and previous scrapes
current_scrape = pd.read_csv('/Users/christianburgin/Documents/scraping/dealerscrape/product_details2024-07-23.csv')
previous_scrape = pd.read_csv('/Users/christianburgin/Documents/scraping/dealerscrape/product_details2024-07-04.csv')

# Generate today's date string
today_date = datetime.now().strftime("%Y%m%d")

# Convert URLs to set for comparison
current_urls = set(current_scrape['url'])
previous_urls = set(previous_scrape['url'])

# Detect new machines
new_machines = current_urls - previous_urls

# Detect removed machines
removed_machines = previous_urls - current_urls

# Detect price changes and add additional column data
price_changes = []
for url in current_urls & previous_urls:
    current_row = current_scrape[current_scrape['url'] == url]
    previous_row = previous_scrape[previous_scrape['url'] == url]
    
    current_price = current_row['Prix'].values[0]
    previous_price = previous_row['Prix'].values[0]
    
    if current_price != previous_price:
        change_info = {
            'url': url,
            'old_price': previous_price,
            'new_price': current_price,
            'Marque': current_row['Marque'].values[0],
            'Modèle': current_row['Modèle'].values[0],
            'Année': current_row['Année'].values[0],
            'Disponible chez': current_row['Disponible chez'].values[0],
            'Nombre d\'heures moteur': current_row['Nombre d\'heures moteur'].values[0],
            'Nombre d\'heures batteur': current_row['Nombre d\'heures batteur'].values[0],
            'Nombre de secoueurs': current_row['Nombre de secoueurs'].values[0],
            'Puissance': current_row['Puissance'].values[0]
        }
        price_changes.append(change_info)

# Create DataFrame for the price changes
changes_df = pd.DataFrame(price_changes)

# Authenticate and initialize the Google Sheets API
file_path = f'/Users/christianburgin/Documents/scraping/comparisonengine/results/results_{today_date}.csv'
changes_df.to_csv(file_path, index=False)

print(f"Changes saved to {file_path}")
