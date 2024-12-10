import os
from web3 import Web3
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration et connexion au réseau Ethereum
ALCHEMY_URL = os.getenv('ALCHEMY_URL')
MY_ADDRESS = os.getenv('MY_ADDRESS')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ABI = os.getenv('CONTRACT_ABI')
CONTRACT_BYTECODE = os.getenv('CONTRACT_BYTECODE')

# Vérifier les valeurs sensibles
if not ALCHEMY_URL or not MY_ADDRESS or not PRIVATE_KEY:
    raise ValueError("Assurez-vous que les variables ALCHEMY_URL, MY_ADDRESS et PRIVATE_KEY sont configurées.")

w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

if not w3.is_connected():
    raise ConnectionError("Impossible de se connecter au réseau Ethereum.")

print("Connecté avec succès au réseau Ethereum.")

# Fonctions utilitaires
def deploy_contract():
    """Déploie le contrat sur le réseau Ethereum."""
    contract = w3.eth.contract(abi=CONTRACT_ABI, bytecode=CONTRACT_BYTECODE)
    nonce = w3.eth.get_transaction_count(MY_ADDRESS)

    # Construire la transaction
    transaction = contract.constructor().build_transaction({
        'chainId': 11155111,  # Sepolia
        'gas': 2000000,
        'gasPrice': w3.to_wei('25', 'gwei'),
        'nonce': nonce
    })

    # Signer et envoyer la transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Déploiement en cours... Hash de la transaction : {tx_hash.hex()}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Contrat déployé à l'adresse : {tx_receipt.contractAddress}")
    return tx_receipt.contractAddress

def call_update_contract(contract_address, status, method):
    """Appelle la fonction `updateContract` du smart contract."""
    contract = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
    nonce = w3.eth.get_transaction_count(MY_ADDRESS)

    transaction = contract.functions.updateContract(status, method).build_transaction({
        'chainId': 11155111,
        'gas': 200000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': nonce
    })

    # Signer et envoyer la transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Appel en cours... Hash de la transaction : {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Appel confirmé. Transaction : {receipt.transactionHash.hex()}")

# Main
if __name__ == "__main__":
    try:
        # Déploiement du contrat
        contract_address = deploy_contract()

        # Exemple d'appel de fonction
        call_update_contract(contract_address, True, "GET")
    except Exception as e:
        print(f"Erreur : {e}")
