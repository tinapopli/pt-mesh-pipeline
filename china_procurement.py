#2
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin

def china_procurement_1():
    base_url = 'http://en.chinabidding.mofcom.gov.cn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  #To Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_info = soup.find_all('ul', {'class': 'txt-02'})
        
        titles = []
        links = []
        dates = []
        for data in ul_info:
            titles.extend([x.text.strip() for x in data.find_all('a')])
            links.extend([urljoin(base_url, x['href']) for x in data.find_all('a')])
            dates.extend([x.text.strip() for x in data.find_all('span')])  # Assuming date is in a span tag
            
        # Creating the dataframe
        df = pd.DataFrame({
            'title': titles,
            'urls': links,
            'dates': dates
        })
        
        return df

    except requests.RequestException as e:
        print(f"Error fetching data from {base_url}: {e}")
        return None

# Test the function
china_procurement_df = china_procurement_1()
print(china_procurement_df)
