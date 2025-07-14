from web3 import Web3
import json
from eth_account import Account

# === CONFIGURATION ===
RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545/"  # BNB Testnet RPC
CONTRACT_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"  # MCIT Token Contract
CHAIN_ID = 97  # BNB Testnet
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

# === DETERMINE FUNCTION NAME (SAFETY CHECK) ===
if 'mint' not in contract.functions:
    print("Function 'mint' not found in ABI. Available functions:")
    print([fn.fn_name for fn in contract.functions])
    exit()

# === BUILD, SIGN AND SEND TRANSACTION ===
try:
    txn = contract.functions.mint().build_transaction({
        'from': address,
        'nonce': w3.eth.get_transaction_count(address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'chainId': CHAIN_ID
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent. Hash: {tx_hash.hex()}")
    print("Track it here: https://testnet.bscscan.com/tx/" + tx_hash.hex())

except Exception as e:
    print("Failed to send transaction:", e)
