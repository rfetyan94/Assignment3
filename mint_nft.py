from web3 import Web3
import json
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import keccak

# === CONFIGURATION ===
RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545/"  # BNB Testnet
CONTRACT_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
PRIVATE_KEY_PATH = "secret_key.txt"
ABI_PATH = "NFT.abi"

# === LOAD PRIVATE KEY ===
with open(PRIVATE_KEY_PATH, 'r') as f:
    PRIVATE_KEY = f.read().strip()

# === SETUP WEB3 AND ACCOUNT ===
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(PRIVATE_KEY)
address = account.address
print("Using address:", address)

# === LOAD ABI AND CONTRACT ===
with open(ABI_PATH, 'r') as abi_file:
    abi = json.load(abi_file)
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# === PREPARE CLAIM ARGS ===
# The contract expects (address, bytes32 signature)
hash_msg = keccak(bytes.fromhex(address[2:]))
signed = Account.sign_hash(hash_msg, private_key=PRIVATE_KEY)
signature = signed.signature

# === BUILD TRANSACTION ===
try:
    txn = contract.functions.claim(address, signature).build_transaction({
        'from': address,
        'nonce': w3.eth.get_transaction_count(address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 97  # BNB Testnet
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent. Hash: {tx_hash.hex()}")
    print("Track it here: https://testnet.bscscan.com/tx/" + tx_hash.hex())

except Exception as e:
    print("Failed to send transaction:", e)
