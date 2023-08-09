import get_all_URL
import make_folder
from make_folder import download_images_from_a_tags
from save_to_csv import save_to_csv, get_image_info
from page_pagination import generate_page_urls

main_url = "https://isorepublic.com/"

urls = generate_page_urls(main_url)
for url in urls:
    photo_urls = get_all_URL.get_all_photo_urls(url)
    # Convert set to list
    photo_urls = list(photo_urls)
    
    for url in photo_urls:
        title = make_folder.get_title_from_url(url)
        folder_name = make_folder.create_folder_with_title(title)
        download_images_from_a_tags(url, folder_name)
        # Get image information
        image_info = get_image_info(url)
        save_to_csv(image_info)
        print("Done")


# photo_urls = get_all_URL.get_all_photo_urls(main_url)
# # Convert set to list
# photo_urls = list(photo_urls)

# print("List of URLs:")
# for url in photo_urls:
#     print(url)

# for url in photo_urls:
#     title = make_folder.get_title_from_url(url)
#     folder_name = make_folder.create_folder_with_title(title)
#     download_images_from_a_tags(url, folder_name)
#     # Get image information
#     image_info = get_image_info(url)
#     print("Done")