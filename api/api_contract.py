import os
from web3 import Web3
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration et connexion au réseau Ethereum
ALCHEMY_URL = os.getenv('ALCHEMY_URL')
MY_ADDRESS = os.getenv('MY_ADDRESS')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

# Adresse du contrat déployé
CONTRACT_ADDRESS = "0xd8b934580fcE35a11B58C6D73aDeE468a2833fa8"

# ABI du contrat
CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "apiContractDict",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "apiMethod",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "apiStatus",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "executionTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bool",
				"name": "_status",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "_method",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_executionTime",
				"type": "uint256"
			}
		],
		"name": "updateContract",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

# Vérifier les valeurs sensibles
if not ALCHEMY_URL or not MY_ADDRESS or not PRIVATE_KEY:
    raise ValueError("Assurez-vous que les variables ALCHEMY_URL, MY_ADDRESS et PRIVATE_KEY sont configurées.")

# Connexion au réseau Ethereum
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

if not w3.is_connected():
    raise ConnectionError("Impossible de se connecter au réseau Ethereum.")

print("\n \n Connecté avec succès au réseau Ethereum. \n \n")

# Fonctions utilitaires
def call_update_contract(contract_address, status, method, executionTime):
    """Appelle la fonction `updateContract` du smart contract."""
    contract = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
    nonce = w3.eth.get_transaction_count(MY_ADDRESS)

    # Estimation des frais
    gas_estimate = contract.functions.updateContract(status, method, executionTime).estimate_gas({
        'from': MY_ADDRESS,
    })
    print(f"\n \n Gas estimé : {gas_estimate} \n \n")

    gaz_price = w3.eth.gas_price
    new_gas_price = int(gaz_price * 1.1) # Ajout de 10 % pour la sécurité
    print(f"gaz_price : {gaz_price} \n \n New gas price : {new_gas_price} \n \n")

    # Construction de la transaction
    transaction = contract.functions.updateContract(status, method, executionTime).build_transaction({
        'chainId': 11155111,
        'gas': int(gas_estimate * 1.25),  # Ajout de 25 % pour la sécurité
        'gasPrice': new_gas_price, # w3.eth.gas_price | w3.to_wei('20', 'gwei') | new_gas_price,
        'nonce': nonce
    })

    # Signer et envoyer la transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"\n \n Appel en cours... Hash de la transaction : {tx_hash.hex()} \n \n")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"\n \n Appel confirmé. Transaction : {receipt.transactionHash.hex()} \n \n")

# Main
if __name__ == "__main__":
    try:
        # Exemple d'appel de fonction
        call_update_contract(CONTRACT_ADDRESS, True, "GET", 2)
        print("\n \n Appel ( call_update_contract ) effectué avec succès. \n \n")
    except Exception as e:
        print(f"Erreur : {e}")
