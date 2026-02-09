import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Configuration
BASE_URL = "http://www.chungwan.co.kr/"
OUTPUT_DIR = "assets"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
CONTENT_FILE = os.path.join(OUTPUT_DIR, "content.txt")

# Extensions to download
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif'}

# Visited URLs to avoid loops
visited_urls = set()

def create_directories():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print(f"Created directory: {IMAGE_DIR}")
    
    # Create content file (or clear it)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Scraped Content from {BASE_URL}\n")
        f.write("="*50 + "\n\n")

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and "chungwan.co.kr" in parsed.netloc

def download_image(img_url):
    try:
        if not img_url:
            return
            
        img_url = urljoin(BASE_URL, img_url)
        parsed = urlparse(img_url)
        filename = os.path.basename(parsed.path)
        
        if not filename or not any(filename.lower().endswith(ext) for ext in IMAGE_EXTS):
            return

        save_path = os.path.join(IMAGE_DIR, filename)
        
        if os.path.exists(save_path):
            return # Already downloaded

        print(f"Downloading image: {filename}")
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

def scrape_page(url, file_handle):
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    print(f"Scraping page: {url}")
    
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding # Handle Korean encoding
        
        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Save Text Content
        title = soup.title.string.strip() if soup.title else "No Title"
        file_handle.write(f"\nPage: {url}\n")
        file_handle.write(f"Title: {title}\n")
        file_handle.write("-" * 20 + "\n")
        
        # Extract main text (simple heuristic: all p and div text, or specific tags if known)
        # Trying to be general to catch body content
        body_text = soup.get_text(separator='\n', strip=True)
        # Limit the noise by taking chunks or just saving the raw text dumping
        # A cleaner way: specific containers if known, but generic for now:
        file_handle.write(body_text)
        file_handle.write("\n" + "="*50 + "\n")

        # 2. Download Images
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                download_image(src)

        # 3. Find Internal Links to crawl recursively
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(url, href)
            
            if is_valid_url(full_url) and full_url not in visited_urls:
                # Basic depth protection or just same domain
                scrape_page(full_url, file_handle)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

def main():
    create_directories()
    
    with open(CONTENT_FILE, 'a', encoding='utf-8') as f:
        scrape_page(BASE_URL, f)
        
    print("\nScraping Completed.")
    print(f"Images saved to: {IMAGE_DIR}")
    print(f"Content saved to: {CONTENT_FILE}")

if __name__ == "__main__":
    main()
