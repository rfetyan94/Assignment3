from web3 import Web3
import json
from eth_account import Account
from eth_account.messages import encode_defunct

# === CONFIGURATION ===
RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545/"  # BNB Testnet
CONTRACT_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"  # MCIT token contract address
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

# === SIGN AND MINT ===
try:
    # Prepare the message and hash
    message = encode_defunct(text=address)
    signed_message = Account.sign_message(message, private_key=PRIVATE_KEY)

    # Use r, s, v from the signature
    sig_bytes = signed_message.signature
    sig_hash = Web3.to_hex(sig_bytes)

    # Get nonce and build the transaction
    nonce = w3.eth.get_transaction_count(address)
    txn = contract.functions.claim(address, sig_bytes).build_transaction({
        'from': address,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 97
    })

    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent. Hash: {tx_hash.hex()}")
    print("Track it here: https://testnet.bscscan.com/tx/" + tx_hash.hex())

except Exception as e:
    print("Failed to send transaction:", e)
