import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

BASE_URL = 'http://ufcstats.com/statistics/fighters'

def scrape_fighter_data():
    # List of characters to iterate over (A-Z)
    alphabet = [chr(i) for i in range(97, 123)]  # a-z
    all_fighters = []

    # Iterate over each letter in the alphabet
    for letter in alphabet:
        print(f"Scraping fighters whose last names start with '{letter.upper()}'...")

        # Iterate through the first 8 pages for each letter
        for current_page in range(1, 9):
            # Define the URL for UFC fighter stats, page by page for each letter
            url = f'{BASE_URL}?page={current_page}&char={letter}'
            print(f"Scraping page {current_page} for letter {letter.upper()}...")

            # Send a request to the URL
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the table containing the fighter data
            table = soup.find('table', {'class': 'b-statistics__table'})

            # If there's no table found, break the loop (no more pages)
            if table is None:
                print(f"No data found on page {current_page} for letter {letter.upper()}.")
                break

            # Extract the table rows
            rows = table.find_all('tr')

            # Loop over each row and extract relevant data
            for row in rows[1:]:  # Skip the header
                cols = row.find_all('td')
                if len(cols) > 1:  # Ensure the row has valid data
                    # Parsing first and last names from the full name
                    full_name = cols[0].text.strip()
                    name_parts = full_name.split(' ', 1)  # Split into First and Last name
                    first_name = name_parts[0]
                    last_name = name_parts[1] if len(name_parts) > 1 else ''

                    # Extract the additional columns
                    nickname = re.search(r'".*"', full_name)  # Extract nickname (if any) between quotes
                    nickname = nickname.group(0) if nickname else ''

                    height = cols[1].text.strip()  # Ht.
                    weight = cols[2].text.strip()  # Wt.
                    reach = cols[3].text.strip()  # Reach
                    stance = cols[4].text.strip()  # Stance
                    wins = cols[5].text.strip()  # W
                    losses = cols[6].text.strip()  # L
                    draws = cols[7].text.strip()  # D

                    # Check for belt status (e.g., 'Champion')
                    belt = 'Champion' if 'Champion' in full_name else ''

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

    return df
