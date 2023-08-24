#1
from bs4 import BeautifulSoup
import requests
import pandas as pd

def fetch_html_content(url, headers):
    """
    Fetching the HTML content of the provided URL.
    
    Parameters:
    - url (str): Target website URL.
    - headers (dict): Request headers.
    
    Returns:
    - BeautifulSoup object: Parsed HTML content.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def extract_world_bank_data(soup):
    """
    Extracting data from the World Bank's evaluation and ratings table.
    
    Parameters:
    - soup (BeautifulSoup object): Parsed HTML content of the target page.
    
    Returns:
    - DataFrame: Extracted data organized in a DataFrame.
    """
    table_info = soup.find('table')
    data = []
    
    for index, tr in enumerate(table_info.find_all('tr')):
        title_data = [x.text.strip() for x in tr.find_all('h3')]
        desc_data = [x.text.strip() for x in tr.find_all('p') if x.text.strip()]
        
        if title_data:
            # If there are multiple descriptions, take the last one
            description = desc_data[-1] if desc_data else None
            data.append({
                'title': title_data[0],
                'description': description
            })
    
    return pd.DataFrame(data)

def main():
    """
    Main function to orchestrate the web scraping of World Bank's evaluation and ratings data.
    """
    URL = 'https://ieg.worldbankgroup.org/data'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # Fetching the HTML content
    soup = fetch_html_content(URL, HEADERS)
    if soup:
        # Extracting the data and print the DataFrame
        df = extract_world_bank_data(soup)
        print(df)

if __name__ == "__main__":
    main()
