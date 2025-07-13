from web3 import Web3
import eth_account
from eth_account.messages import encode_defunct
from eth_account import Account

def sign(m):
    w3 = Web3()

    assert isinstance(m, str), f"message {m} must be a string"

    # Convert message to bytes if needed
    if isinstance(m, str):
        m = m.encode("utf-8")
    message = encode_defunct(m)

    # Create new Ethereum account
    account_object = Account.create()
    private_key = account_object.key.hex()  # Eth account private key
    public_key = account_object.address      # Eth account public key

    # Sign the message
    signed_message = Account.sign_message(message, private_key)

    print('Account created:\n'
          f'private key={w3.to_hex(private_key)}\naccount={public_key}\n')
    assert isinstance(signed_message, eth_account.datastructures.SignedMessage)

    return public_key, signed_message

def verify(m, public_key, signed_message):
    w3 = Web3()
    assert isinstance(m, str), f"message {m} must be a string"
    assert isinstance(public_key, str), f"public_key {public_key} must be a string"

    if isinstance(m, str):
        m = m.encode("utf-8")
    message = encode_defunct(m)

    signer = Account.recover_message(message, signature=signed_message.signature)
    valid_signature = signer == public_key
    assert isinstance(valid_signature, bool), "verify should return a boolean value"
    return valid_signature

if __name__ == "__main__":
    import random
    import string

    for i in range(10):
        m = "".join([random.choice(string.ascii_letters) for _ in range(20)])

        pub_key, signature = sign(m)

        # Modifies every other message so that the signature fails to verify
        if i % 2 == 0:
            m = m + 'a'

        if verify(m, pub_key, signature):
            print("Signed Message Verified")
        else:
            print("Signed Message Failed to Verify")
