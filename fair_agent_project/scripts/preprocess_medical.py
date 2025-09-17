from datasets import load_dataset
import os

def download_medical_datasets():
    os.makedirs("data/medicine", exist_ok=True)

    mimic_iv = load_dataset("physionet/mimiciv")
    mimic_iv.save_to_disk("data/medicine/mimiciv")

    pubmed_qa = load_dataset("pubmedqa/pubmedqa")
    pubmed_qa.save_to_disk("data/medicine/pubmedqa")

    print("Medical datasets downloaded and saved.")

if __name__ == "__main__":
    download_medical_datasets()