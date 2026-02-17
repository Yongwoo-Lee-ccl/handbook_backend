import os
import requests

SAMPLES = [
    {
        "name": "attention_is_all_you_need.pdf",
        "url": "https://arxiv.org/pdf/1706.03762.pdf"
    },
    {
        "name": "resnet.pdf",
        "url": "https://arxiv.org/pdf/1512.03385.pdf"
    },
    {
        "name": "dilithium.pdf",
        "url": "https://eprint.iacr.org/2017/633.pdf"
    }
]

DATA_DIR = "data/samples"

def download_samples():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for sample in SAMPLES:
        path = os.path.join(DATA_DIR, sample["name"])
        if os.path.exists(path):
            with open(path, "rb") as f:
                if f.read(4) == b"%PDF":
                    print(f"Skipping {sample['name']}, already exists and is a PDF.")
                    continue
                else:
                    print(f"{sample['name']} exists but is not a PDF, redownloading...")
                    os.remove(path)
            
        print(f"Downloading {sample['name']} from {sample['url']}...")
        try:
            response = requests.get(sample["url"], stream=True, timeout=30, headers=headers)
            response.raise_for_status()
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verify PDF
            with open(path, "rb") as f:
                if f.read(4) != b"%PDF":
                    print(f"Warning: {sample['name']} is NOT a PDF!")
                else:
                    print(f"Saved to {path}")
        except Exception as e:
            print(f"Failed to download {sample['name']}: {e}")

if __name__ == "__main__":
    download_samples()
