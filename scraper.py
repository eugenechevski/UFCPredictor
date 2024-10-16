import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import logging as log

# Define the base URL for UFC fighter stats
BASE_URL = 'http://ufcstats.com/statistics/fighters'

# Set up logging
logger = log.getLogger(__name__)
log.basicConfig(filename='scraping.log', level=log.INFO)

# Clean previous log file
open('scraping.log', 'w').close()

def scrape_fighter_data():
    print("Scraping fighter data...")
    logger.info("Scraping UFC fighter data...")
    
    # List of characters to iterate over (A-Z)
    alphabet = [chr(i) for i in range(97, 123)]  # a-z
    all_fighters = []

    # Iterate over each letter in the alphabet
    for letter in alphabet:
        logger.info(f"Scraping fighters whose last names start with '{letter.upper()}'...")

        # Define the URL for UFC fighter stats for each letter
        url = f'{BASE_URL}?page=all&char={letter}'
        
        # Send a request to the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table containing the fighter data
        table = soup.find('table', {'class': 'b-statistics__table'})
        
        # If there's no table found, break the loop (no more pages)
        if table is None:
            logger.info(f"No data found for letter {letter.upper()}.")
            break
        
        # Extract the table rows
        rows = table.find_all('tr')
        
        # Loop over each row and extract relevant data
        for row in rows[1:]:  # Skip the header
            cols = row.find_all('td')
            if len(cols) > 1:  # Ensure the row has valid data
                # Parsing first and last names from the full name
                # td > a > text
                
                first_name = cols[0].find('a').text.strip()
                last_name = cols[1].find('a').text.strip()
                nickname = cols[2].find('a').text.strip()
                
                # Extract the additional columns
                height = cols[3].text.strip()  # Ht.
                weight = cols[4].text.strip()  # Wt.
                reach = cols[5].text.strip()  # Reach
                stance = cols[6].text.strip()  # Stance
                wins = cols[7].text.strip()  # W
                losses = cols[8].text.strip()  # L
                draws = cols[9].text.strip()  # D
                belt = 'Champion' if cols[10].find('img') else 'Non-Champion'
                
                # Store the extracted information
                fighter_info = {
                    'First': first_name,
                    'Last': last_name,
                    'Nickname': nickname,
                    'Ht.': height,
                    'Wt.': weight,
                    'Reach': reach,
                    'Stance': stance,
                    'W': wins,
                    'L': losses,
                    'D': draws,
                    'Belt': belt
                }
                all_fighters.append(fighter_info)
    
    # Convert the list to a DataFrame
    df = pd.DataFrame(all_fighters)

    # Save the data to the 'data' directory
    df.to_csv('data/fighters_stats.csv', index=False)
    
    logger.info("Scraping complete. Fighter data saved to data/fighters_stats.csv")    

    return df

