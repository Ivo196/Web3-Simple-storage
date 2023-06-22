from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# Compiler
install_solc("0.6.6")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.6",
)

with open("compiler_code.json", "w") as file:
    json.dump(compiled_sol, file)

# ABI
# BYTECODE

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]


##Connect with Ganache

w3 = Web3(
    Web3.HTTPProvider("https://sepolia.infura.io/v3/1e0a8901dcfd4ba087b5ab20be5978c1")
)
chain_id = 11155111
my_address = "0x940210a2adB073E8D38a1efF294d839e707c4271"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Nonce
nonce = w3.eth.get_transaction_count(my_address)
# 1. Construir la transaccion

transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# 2. Firmar la transaccion

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Enviar la transaccion

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt.contractAddress)

# Working with deployed contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call NoGas
# Transact with Gas spend
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,  # Nonce mustn't repeat
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
print("Updating stored value")

t_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(t_hash)
print(tx_receipt.transactionHash)
print(simple_storage.functions.retrieve().call())
