import requests
from bs4 import BeautifulSoup

def get_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if an unsuccessful status code is returned

        # Using lxml parser for faster parsing
        soup = BeautifulSoup(response.text, 'lxml')
        
        title = soup.title.string if soup.title else 'No title found'
        
        print("Got title:")
        print(title)
        return title

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
