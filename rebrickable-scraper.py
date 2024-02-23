import os
import requests
from bs4 import BeautifulSoup


def download_file(url, subfolder):
    local_filename = url.split("/")[-1].split("?")[0]
    os.makedirs(subfolder, exist_ok=True)
    print(f"Downloading {url}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(os.path.join(subfolder, local_filename), "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Successfully downloaded {local_filename} to {subfolder}")
    return local_filename


def scrape_files(webpage_url, extensions):
    print(f"Scraping {webpage_url} for files with extensions {extensions}...")
    response = requests.get(webpage_url)
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a"):
        url = link.get("href")
        if url:
            clean_url = url.split("?")[0]
            if any(clean_url.endswith(ext) for ext in extensions):
                ext = [ext for ext in extensions if clean_url.endswith(ext)][0]
                subfolder = ext.strip(".")
                download_file(url, subfolder)
    print("Finished scraping.")


webpage_url = "https://rebrickable.com/downloads/"
extensions = [".zip", ".csv.gz"]
scrape_files(webpage_url, extensions)
