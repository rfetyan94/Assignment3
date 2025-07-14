from web3 import Web3
import json
from eth_account import Account

RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545/"  # BNB Testnet RPC
CHAIN_ID = 97  # BNB Testnet chain ID
CONTRACT_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"  # MCIT NFT Contract
PRIVATE_KEY_PATH = "secret_key.txt"
ABI_PATH = "NFT.abi"

with open(PRIVATE_KEY_PATH, 'r') as f:
    PRIVATE_KEY = f.read().strip()

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(PRIVATE_KEY)
address = account.address

with open(ABI_PATH, 'r') as abi_file:
    abi = json.load(abi_file)
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

try:
    print(f"Using address: {address}")
    nonce = w3.eth.get_transaction_count(address)

    txn = contract.functions.mint().build_transaction({
        'from': address,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'chainId': CHAIN_ID
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(f"Transaction sent! Hash: {tx_hash.hex()}")
    print(f"Track it here: https://testnet.bscscan.com/tx/{tx_hash.hex()}")

except Exception as e:
    print("Failed to send transaction:", e)
