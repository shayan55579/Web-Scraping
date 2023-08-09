import os
import csv
from get_all_URL import send_request,requests,BeautifulSoup
from make_folder import get_title_from_url, create_folder_with_title



def save_to_csv(data_list, csv_filename):
    try:
        if not os.path.exists(csv_filename):
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Title', 'Keywords', 'Photographer', 'Image Link', 'Web Page Link']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

        with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
            existing_titles = set()
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_titles.add(row['Title'])

        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Keywords', 'Photographer', 'Image Link', 'Web Page Link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for data in data_list:
                if data['Title'] not in existing_titles:
                    writer.writerow(data)
                    existing_titles.add(data['Title'])

    except Exception as e:
        print(f"Error occurred while saving to CSV: {e}")

def get_image_info(url):
    try:
        response = send_request(url)
        if response is not None:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract the title from the h1 tag within the left-wrap div
            div_element = soup.find('div', class_='left-wrap')
            if div_element:
                h1_tag = div_element.find('h1')
                title = h1_tag.text.strip() if h1_tag else ""
                
                # Extract keywords from li tags within keyword-tags ul
                ul_keyword_tags = soup.find('ul', class_='keyword-tags')
                if ul_keyword_tags:
                    li_tags = ul_keyword_tags.find_all('li')
                    keywords = [li.text.strip() for li in li_tags]
                else:
                    keywords = []
                
                photographer = get_title_from_url(url) 
                
                div_media_content = soup.find('div', class_='media-content')
                if div_media_content:
                    img_tags = div_media_content.find_all('img', src=True, attrs={'data-src': True})
                    image_links = [img['data-src'] for img in img_tags]
                    
                    data_list = []
                    for img_link in image_links:
                        data = {
                            'Title': title,
                            'Keywords': ', '.join(keywords),
                            'Photographer': photographer,
                            'Image Link': img_link,
                            'Web Page Link': url
                        }
                        data_list.append(data)
                    
                    csv_filename = 'image_info.csv'  # Use a single CSV file for all information
                    save_to_csv(data_list, csv_filename)
                    
                    return data_list
                else:
                    print("No images found in the provided URL.")
                    return None
            else:
                print("No title found in the provided URL.")
                return None
        else:
            print(f"Failed to fetch URL: {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

# url = 'https://isorepublic.com/photo/ocean-water-sunrise/'

# # Get image information
# image_info = get_image_info(url)

# csv_filename = f"{image_info[0]['Title']}.csv"
# # Save image info to CSV
# save_to_csv(image_info, csv_filename)
