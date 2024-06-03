import os
import re
import requests
from urllib.parse import urljoin, urlparse

def download_image(image_url, directory='C:\\Users\\jeetg\\code\\image downloader', image_name=None):
    if not os.path.exists(directory):
        os.makedirs(directory)

    if image_name is None:
        image_name = os.path.basename(urlparse(image_url).path)
    
    file_path = os.path.join(directory, image_name)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(image_url, headers=headers, stream=True)
        response.raise_for_status()
        
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Downloaded {image_url} as {file_path}")
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")

def scrape_and_download_images(page_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(page_url, headers=headers)
    if response.status_code != 200:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

    text = response.text

    pattern = r'<img.*?src="(.*?)"[^\>]*>'
    img_addrs = re.findall(pattern, text)

    if not img_addrs:
        return "No images found."

    for i, img_addr in enumerate(img_addrs, start=1):
        img_url = urljoin(page_url, img_addr)
        download_image(img_url, image_name=f'image_{i}.jpg')

    return "DONE"

def ImageDownloader(url):
    parsed_url = urlparse(url)
    if parsed_url.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
        download_image(url)
    else:
        scrape_and_download_images(url)

# USAGE
print("Hey!! Welcome to the Image downloader...")
link = input("Please enter the URL from where you want to download the images: ")
result = ImageDownloader(link)
print(result)
