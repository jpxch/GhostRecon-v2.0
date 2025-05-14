import os
import requests
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

def fetch_recent_txns(address: str, limit: int = 10) -> list:
    """
    Fetches resent normal transactions for a given address.
    Returns a list of transactions dicts.
    """
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()

        if data["status"] == "1" and data["result"]:
            return data["result"][:limit]
        else:
            print(f"No transactions found for {address}: {data['message']}")
            return []

    except Exception as e:
        print(f"Error fetching transactions for {address}: {e}")
        return []

if __name__ == "__main__":
    test_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    txns = fetch_recent_txns(test_address, limit=5)

    for i, tx in enumerate(txns, 1):
        print(f"[{i}] Hash: {tx['hash']} | From: {tx['from']} -> To: {tx['to']} | Value: {int(tx['value']) / 1e18} ETH")
