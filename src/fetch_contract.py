import os
import requests
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

def fetch_contract_source(address: str) -> dict:
    """
    Fetch verified source code for a contract from Etherscan.
    Returns a dict with keys: 'SourceCode', 'ABI', 'ContractName', etc.
    """
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": ETHERSCAN_API_KEY
    }
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()

        if data["status"] == "1" and data["result"]:
            return data["result"][0]
        else:
            print(f"Contract source not found for {address}: {data['message']}")
            return {}

    except Exception as e:
        print(f"Error fetching contract for {address}: {e}")
        return{}

    if __name__ == "__main__":
        test_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        contract_data = fetch_contract_source_code(test_address)

        if contract_data:
            print(f"Contract Name: {contract_data.get('ContractName')}")
            print("Source Code Snippet:")
            print(contract_data.get('SourceCode')[:300], "...")
