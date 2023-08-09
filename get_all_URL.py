import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin



def get_random_user_agent():
    user_agents = [
        # Add more user agents here
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        # Add more user agents here
    ]
    return random.choice(user_agents)

def send_request(url):
    retries = 3
    delay = 2

    headers = {
        "User-Agent": get_random_user_agent()
    }

    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException:
            pass

        time.sleep(delay)

    return None

photo_urls = set()
def get_all_photo_urls(main_url):
    try:
        response = send_request(main_url)
        if response is not None:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(main_url, link['href'])
                if re.match(r'^https://isorepublic\.com/photo/', absolute_url):
                    photo_urls.add(absolute_url)
            return photo_urls
        else:
            print(f"Failed to fetch URL: {main_url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

  