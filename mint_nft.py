from web3 import Web3
import json
from eth_account import Account
from eth_account.messages import encode_defunct, defunct_hash_message
import sys

# === CONFIGURATION ===
NETWORKS = {
    "bsc": {
        "rpc_url": "https://data-seed-prebsc-1-s1.binance.org:8545/",
        "chain_id": 97,
        "explorer": "https://testnet.bscscan.com/tx/"
    },
    "avax": {
        "rpc_url": "https://api.avax-test.network/ext/bc/C/rpc",
        "chain_id": 43113,
        "explorer": "https://testnet.snowtrace.io/tx/"
    }
}

NETWORK = sys.argv[1] if len(sys.argv) > 1 else "bsc"  # default to BSC if no argument
if NETWORK not in NETWORKS:
    raise Exception(f"Unsupported network: {NETWORK}")

RPC_URL = NETWORKS[NETWORK]["rpc_url"]
CHAIN_ID = NETWORKS[NETWORK]["chain_id"]
EXPLORER = NETWORKS[NETWORK]["explorer"]

CONTRACT_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"  # MCIT Token Contract
PRIVATE_KEY_PATH = "secret_key.txt"
ABI_PATH = "NFT.abi"

# === LOAD PRIVATE KEY ===
with open(PRIVATE_KEY_PATH, 'r') as f:
    PRIVATE_KEY = f.read().strip()

# === SETUP WEB3 AND ACCOUNT ===
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(PRIVATE_KEY)
address = account.address
print(f"Using address: {address}")

# === LOAD CONTRACT ABI ===
with open(ABI_PATH, 'r') as abi_file:
    abi = json.load(abi_file)
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# === PREPARE MESSAGE AND SIGN ===
message = encode_defunct(text=address)
signed_message = Account.sign_message(message, private_key=PRIVATE_KEY)

# === MANUALLY COMPUTE messageHash FOR COMPATIBILITY ===
message_hash_bytes32 = defunct_hash_message(text=address)

# === BUILD TRANSACTION ===
try:
    txn = contract.functions.claim(address, message_hash_bytes32).build_transaction({
        'from': address,
        'nonce': w3.eth.get_transaction_count(address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'chainId': CHAIN_ID
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)

    # Ensure we have the raw transaction bytes
    raw_tx = getattr(signed_txn, 'rawTransaction', None)
    if raw_tx is None:
        raw_tx = getattr(signed_txn, 'raw_transaction', None)

    if raw_tx is None:
        raise Exception("rawTransaction not found in signed transaction")

    tx_hash = w3.eth.send_raw_transaction(raw_tx)

    print(f"Transaction sent! Hash: {tx_hash.hex()}")
    print(f"Track it here: {EXPLORER}{tx_hash.hex()}")

except Exception as e:
    print("Failed to send transaction:", str(e))
