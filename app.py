import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import threading

visited_urls = set()
lock = threading.Lock()

def search_text_in_url(url, text_to_search, domain):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if text_to_search.lower() in soup.text.lower():
                print(f'Text found at: {url}')

            for link in soup.find_all('a', href=True):
                link_url = urljoin(url, link['href'])
                parsed_link_url = urlparse(link_url)
                if parsed_link_url.netloc == domain:
                    with lock:
                        if link_url not in visited_urls:
                            visited_urls.add(link_url)
                            threading.Thread(target=search_text_in_url, args=(link_url, text_to_search, domain)).start()

    except requests.RequestException as e:
        print(f'Failed to fetch {url}: {e}')

def main():
    start_url = input("Enter the website URL: ").strip()
    text_to_search = input("Enter the text to search for: ").strip()
    parsed_start_url = urlparse(start_url)
    domain = parsed_start_url.netloc

    with lock:
        visited_urls.add(start_url)
    search_text_in_url(start_url, text_to_search, domain)

if __name__ == "__main__":
    main()