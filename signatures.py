from web3 import Web3
import eth_account
from eth_account.messages import encode_defunct
from eth_account import Account

def sign(m):
    w3 = Web3()
    
    assert isinstance(m, str), f"message {m} must be a string"

    # Create new Ethereum account
    account_object = eth_account.Account.create()
    private_key = account_object.address # Eth account public key
    public_key = account_object.key # Eth account private key

    # Prepare the message and sign it
    message = encode_defunct(text=m)
    signed_message = eth_account.Account.sign_message(message, private_key=private_key)


    """You can save the account public/private keypair that prints in the next section
     for use in future assignments. You will need a funded account to pay gas fees for 
     several upcoming assignments and the first step of funding an account is having 
     an account to send the funds too.
    """
    print('Account created:\n'
          f'private key={w3.to_hex(private_key)}\naccount={public_key}\n')
    assert isinstance(signed_message, eth_account.datastructures.SignedMessage)
    # print(f"signed message {signed_message}\nr= {signed_message.r}\ns= {signed_message.s}")

    return public_key, signed_message


def verify(m, public_key, signed_message):
    w3 = Web3()
    assert isinstance(m, str), f"message {m} must be a string"
    assert isinstance(public_key, str), f"public_key {public_key} must be a string"
    # TODO verify the 'signed_message' is valid given the original message 'm' and the signers 'public_key'
    message = encode_defunct(text=m)  # Encode the message
    signer = eth_account.Account.recover_message(message, signature=signed_message.signature)
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
