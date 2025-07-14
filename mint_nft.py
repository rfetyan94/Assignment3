from web3 import Web3
import json
from eth\_account import Account
from eth\_account.messages import encode\_defunct

# === CONFIGURATION ===

NETWORK = "bsc"  # Change to "avax" to target Fuji testnet

if NETWORK == "bsc":
RPC\_URL = "[https://data-seed-prebsc-1-s1.binance.org:8545/](https://data-seed-prebsc-1-s1.binance.org:8545/)"
CHAIN\_ID = 97
EXPLORER\_URL = "[https://testnet.bscscan.com/tx/](https://testnet.bscscan.com/tx/)"
elif NETWORK == "avax":
RPC\_URL = "[https://api.avax-test.network/ext/bc/C/rpc](https://api.avax-test.network/ext/bc/C/rpc)"
CHAIN\_ID = 43113
EXPLORER\_URL = "[https://testnet.snowtrace.io/tx/](https://testnet.snowtrace.io/tx/)"
else:
raise ValueError("Unsupported network")

CONTRACT\_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"  # MCIT Token Contract
PRIVATE\_KEY\_PATH = "secret\_key.txt"
ABI\_PATH = "NFT.abi"

# === LOAD PRIVATE KEY ===

with open(PRIVATE\_KEY\_PATH, 'r') as f:
PRIVATE\_KEY = f.read().strip()

# === SETUP WEB3 AND ACCOUNT ===

w3 = Web3(Web3.HTTPProvider(RPC\_URL))
account = Account.from\_key(PRIVATE\_KEY)
address = account.address
print(f"Using address: {address}")

# === LOAD CONTRACT ABI ===

with open(ABI\_PATH, 'r') as abi\_file:
abi = json.load(abi\_file)
contract = w3.eth.contract(address=Web3.to\_checksum\_address(CONTRACT\_ADDRESS), abi=abi)

# === PREPARE MESSAGE AND SIGN ===

challenge = encode\_defunct(text=address)
signed\_message = Account.sign\_message(challenge, private\_key=PRIVATE\_KEY)

# Generate challenge hash from the same signed body

message\_hash\_bytes32 = Web3.keccak(challenge.body)

# === BUILD TRANSACTION ===

try:
txn = contract.functions.claim(address, message\_hash\_bytes32).build\_transaction({
'from': address,
'nonce': w3.eth.get\_transaction\_count(address),
'gas': 300000,
'gasPrice': w3.eth.gas\_price,
'chainId': CHAIN\_ID
})

```
signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)

raw_tx = getattr(signed_txn, 'rawTransaction', None)
if raw_tx is None and hasattr(signed_txn, 'raw_transaction'):
    raw_tx = getattr(signed_txn, 'raw_transaction')

if raw_tx is None:
    raise Exception("rawTransaction not found in signed transaction")

tx_hash = w3.eth.send_raw_transaction(raw_tx)

print(f"Transaction sent! Hash: {tx_hash.hex()}")
print(f"Track it here: {EXPLORER_URL}{tx_hash.hex()}")
```

except Exception as e:
print("Failed to send transaction:", str(e))
