from datasets import load_dataset
import os

def download_finance_datasets():

    # Create directories
    os.makedirs("data/finance", exist_ok=True)

    finqa = load_dataset("ibm-research/finqa")
    finqa.save_to_disk("data/finance/finqa")

    tat_qa = load_dataset("NExTplusplus/TAT-QA")
    tat_qa.save_to_disk("data/finance/tat-qa")

    print("Finance datasets downloaded and saved.")

if __name__ == "__main__":
    download_finance_datasets()