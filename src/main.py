from web3 import Web3
from rich import print
import os, json

# Load environment
from dotenv import load_dotenv
load_dotenv()

#Connect to an Ethereum RPC
RPC_URL = os.getenv('RPC_URL', 'https://mainnet.infura.io/v3/0cb553bc283b4ecda7f62616c37d80c5')
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print('[green]Connected to Ethereum RPC[/green]')
else:
    print('[red]Failed to connect to RPC[/red]')
