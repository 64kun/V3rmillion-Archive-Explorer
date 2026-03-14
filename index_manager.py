import os
import urllib.request
import zipfile

INDEX_URL = "https://github.com/64kun/V3rmillion-Archive-Explorer/releases/download/v1.0.0/index.zip"

INDEX_DIR = "index"
INDEX_FILE = os.path.join(INDEX_DIR, "index.json")
INDEX_ZIP = "index.zip"


def download_index():
    print("Index not found.")
    print("Downloading prebuilt index (~17MB)...")

    urllib.request.urlretrieve(INDEX_URL, INDEX_ZIP)

    print("Download complete. Extracting...")

    with zipfile.ZipFile(INDEX_ZIP, 'r') as zip_ref:
        zip_ref.extractall(".")

    os.remove(INDEX_ZIP)

    print("Index ready.")


def ensure_index():
    if not os.path.exists(INDEX_FILE):
        download_index()