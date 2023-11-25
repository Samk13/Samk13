from bs4 import BeautifulSoup
import requests
import os
import re

def valid_filename(name):
    """ Create a valid filename from a string """
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_svgs(html_file_path, save_folder):
    """Fetch all svgs and save them into save_folder"""
    # Ensure the save folder exists
    os.makedirs(save_folder, exist_ok=True)

    # Read and parse the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    for index, img in enumerate(img_tags):
        img_url = img.get('src')
        if img_url and img_url.endswith('.svg'):  # Check if the src is an SVG
            # Use alt text if available, otherwise default to 'default-logo'
            alt_text = img.get('alt', f'default-logo-{index}')
            # Ensure the file name is valid
            img_name = valid_filename(alt_text) + '.svg'

            response = requests.get(img_url)
            if response.status_code == 200:
                with open(os.path.join(save_folder, img_name), 'wb') as file:
                    file.write(response.content)
                print(f'Downloaded: {img_name}')
            else:
                print(f'Failed to download: {img_url}')

if __name__ == "__main__":
    # Path to HTML file
    html_file_path = './test.html'

    # Folder to save SVG images
    save_folder = './data/'

    download_svgs(html_file_path, save_folder)
