#3

from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrap_e_tenders():
    url = 'https://etenders.gov.in/eprocure/app'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', {'class': "list_table"})
        table_headers = [x.text.strip() for x in table.find('tr', {'class': 'list_header'}).find_all('td')]
        
        rows_data = []
        for row in table.find_all('tr', {'class': ['even', 'odd']}):
            rows_data.append([x.text.strip() for x in row.find_all('td')])
            
        # Create dataframe
        df = pd.DataFrame(rows_data, columns=table_headers)
        
        return df

    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Test the function
e_tenders = scrap_e_tenders()
print(e_tenders)
