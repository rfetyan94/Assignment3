from web3 import Web3
import json
from eth_account import Account
from eth_account.messages import encode_defunct

# === CONFIGURATION ===
RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545/"  # BNB Testnet
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

# Convert address to bytes32 using keccak (this simulates a hashed challenge message)
message_hash_bytes32 = Web3.keccak(text=address)

# === BUILD TRANSACTION ===
try:
    txn = contract.functions.claim(address, message_hash_bytes32).build_transaction({
        'from': address,
        'nonce': w3.eth.get_transaction_count(address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 97
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    raw_txn = signed_txn.rawTransaction
    tx_hash = w3.eth.send_raw_transaction(raw_txn)

    print(f"Transaction sent! Hash: {tx_hash.hex()}")
    print(f"Track it here: https://testnet.bscscan.com/tx/{tx_hash.hex()}")

except Exception as e:
    print("Failed to send transaction:", str(e))
