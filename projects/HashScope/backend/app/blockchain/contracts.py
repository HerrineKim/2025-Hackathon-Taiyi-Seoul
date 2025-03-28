from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Web3 setup - HSK 네트워크 사용
WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI", "https://mainnet.hsk.xyz")
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

# Contract addresses
HSK_TOKEN_ADDRESS = os.getenv("HSK_TOKEN_ADDRESS", "0x0000000000000000000000000000000000000000")
DEPOSIT_CONTRACT_ADDRESS = os.getenv("DEPOSIT_CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")

# ERC-20 ABI (standard interface for tokens)
ERC20_ABI = json.loads('''
[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]
''')

# Deposit Contract ABI (simplified for example)
DEPOSIT_ABI = json.loads('''
[
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "user", "type": "address"},
            {"indexed": false, "name": "amount", "type": "uint256"}
        ],
        "name": "Deposit",
        "type": "event"
    },
    {
        "constant": false,
        "inputs": [{"name": "amount", "type": "uint256"}],
        "name": "deposit",
        "outputs": [],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getBalance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]
''')

# Initialize contract instances
hsk_token_contract = web3.eth.contract(address=HSK_TOKEN_ADDRESS, abi=ERC20_ABI)
deposit_contract = web3.eth.contract(address=DEPOSIT_CONTRACT_ADDRESS, abi=DEPOSIT_ABI)

def get_token_balance(wallet_address):
    """
    Get HSK token balance for a wallet address
    """
    try:
        balance = hsk_token_contract.functions.balanceOf(wallet_address).call()
        decimals = hsk_token_contract.functions.decimals().call()
        return balance / (10 ** decimals)
    except Exception as e:
        print(f"Error getting token balance: {e}")
        return 0

def get_deposit_balance(wallet_address):
    """
    Get deposited HSK token balance for a wallet address
    """
    try:
        balance = deposit_contract.functions.getBalance(wallet_address).call()
        decimals = hsk_token_contract.functions.decimals().call()
        return balance / (10 ** decimals)
    except Exception as e:
        print(f"Error getting deposit balance: {e}")
        return 0

def verify_deposit_transaction(tx_hash, wallet_address, expected_amount=None):
    """
    Verify a deposit transaction on the HSK blockchain
    """
    try:
        # Get transaction receipt
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        
        if not receipt or receipt['status'] != 1:
            return False, "Transaction failed or not found"
        
        # Check if the transaction was sent to the deposit contract
        if receipt['to'].lower() != DEPOSIT_CONTRACT_ADDRESS.lower():
            return False, "Transaction was not sent to the deposit contract"
        
        # Look for Deposit event
        deposit_event = deposit_contract.events.Deposit().process_receipt(receipt)
        
        if not deposit_event:
            return False, "No Deposit event found in transaction"
        
        # Verify the event data
        event_data = deposit_event[0]['args']
        user = event_data['user']
        amount = event_data['amount']
        
        # Check if the deposit was made by the correct user
        if user.lower() != wallet_address.lower():
            return False, "Deposit was made by a different user"
        
        # Check if the amount matches (if expected_amount is provided)
        if expected_amount is not None:
            decimals = hsk_token_contract.functions.decimals().call()
            expected_amount_wei = int(expected_amount * (10 ** decimals))
            if amount != expected_amount_wei:
                return False, f"Deposit amount does not match. Expected: {expected_amount}, Actual: {amount / (10 ** decimals)}"
        
        return True, amount
    except Exception as e:
        print(f"Error verifying deposit transaction: {e}")
        return False, str(e)
