from get_all_URL import send_request,requests,BeautifulSoup

def get_page_numbers(main_url):
    try:
        response = send_request(main_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            a_tags = soup.find_all('a', class_='page-numbers')
            page_numbers = [int(a_tag.text.strip()) for a_tag in a_tags if a_tag.text.strip().isdigit()]
            return page_numbers
        else:
            print(f"Failed to fetch URL. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


def generate_page_urls(main_url):
    page_numbers = get_page_numbers(main_url)
    biggest_number = max(page_numbers)
    print(f"Last Page Number: {biggest_number}")
    
    urls = [main_url]
    
    for num in range(2, biggest_number + 1):
        url = f"{main_url}page/{num}/"
        urls.append(url)
        
    return urls

# main_url = 'https://isorepublic.com/'
# urls = generate_page_urls(main_url)

# print("List of URLs:")
# for url in urls:
#     print(url)