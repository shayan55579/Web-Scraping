import os
from get_all_URL import send_request,requests,BeautifulSoup

def get_title_from_url(url):
    try:
        response = send_request(url)
        if response is not None:
            soup = BeautifulSoup(response.content, 'html.parser')
            a_tag = soup.find('a', class_='media-author')
            if a_tag:
                title = a_tag.get('title')
            else:
                print("Failed to fetch title ")
        else:
            print(f"Failed to fetch URL: {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    return title

def create_folder_with_title(title):
    try:
        folder_name = title.replace('/', '_')  # Replace any '/' characters with underscores
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name
    except OSError as e:
        print(f"Error occurred while creating folder: {e}")
        return None



def download_images_from_a_tags(url, folder_name):
    try:
        response = send_request(url)
        if response is not None:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract the title from the h1 tag within the left-wrap div
            div_element = soup.find('div', class_='left-wrap')
            if div_element:
                h1_tag = div_element.find('h1')
                title = h1_tag.text.strip() if h1_tag else ""
                
                a_tags = soup.find_all('a', class_='btn btn-lg btn-download')
                for a_tag in a_tags:
                    img_url = a_tag['href']
                    img_data = send_request(img_url)
                    if img_data and img_data.status_code == 200:
                        filename = img_url.split('/')[-1]
                        # Use the title to create the filename
                        file_title = title.replace(" ", "_")
                        new_filename = f"{file_title}.jpg"
                        
                        file_path = os.path.join(folder_name, new_filename)
                        
                        with open(file_path, 'wb') as f:
                            f.write(img_data.content)
            else:
                print("No title found in the provided URL.")
        else:
            print(f"Failed to fetch URL: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")


# url =  'https://isorepublic.com/photo/train-tracks-people/'
# folder_name = create_folder_with_title(get_title_from_url(url))
# download_images_from_a_tags(url, folder_name)