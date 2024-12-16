# SimpleAPI
- Project_Name: SimpleAPI
- Project_Description: Simple API with SmartContract
- Project_Type: Django, Django Rest Framework
- Project_URL: https://github.com/gabrielbygas/simpleAPI
- Author: Gabriel Kalala && Benedicte Olish
- Author_Email: dev@gabrielkalala.com

SimpleAPI is a simple API built with Django Rest Framework. It allows you to create, read, update, and delete data using CRUD operations. The API also includes a Smart Contract that can be used to track the execution time of each operation.

## Features
- CRUD operations for Persons
- Smart Contract for tracking execution time
- API endpoints for Smart Contract
- API endpoints for Persons
- API endpoints for Persons with Smart Contract
- API endpoints for Persons with Smart Contract and execution time
- API endpoints for Persons with Smart Contract and execution time with Contract Summary
- API endpoints for Persons with Smart Contract and execution time with Contract Summary and Contract Data
- - The Smart Contract is used to track the execution time of each operation.
- The Smart Contract is used to store the execution time of each operation and the corresponding request ID.
- The Smart Contract is used to store the execution time of each operation and the corresponding request ID.

## Requirements
- Python
- Django
- Django Rest Framework
- Faker
- Web3
- Python-dotenv

## Installation
1. Clone the repository:
```bash
git clone https://github.com/gabrielbygas/simpleAPI.git
```
2. Navigate to the project directory:
```bash
cd simpleAPI
```
3. Create a virtual environment:
```bash
python -m venv venv
```
4. Install the required packages:
```bash
pip install -r requirements.txt
```
5. Activate the virtual environment:
```bash
source venv/bin/activate
```
6. Migrate the database:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
7. Create fake data:
```bash
python manage.py generate_fake_data
```
8. Create the smart contract on [remix.ethereum.org](https://remix.ethereum.org/):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract APIContract {
    // Déclare les variables publiques
    bool public apiStatus;          // Stocke le statut de l'API
    string public apiMethod;        // Stocke la méthode de l'API (GET, POST, etc.)
    uint256 public executionTime;   // Stocke le temps d'exécution
    mapping(address => uint256) public apiContractDict; // Associe les adresses au timestamp

    // Fonction pour mettre à jour les variables
    function updateContract(bool _status, string memory _method, uint256 _executionTime) public {
        apiStatus = _status;
        apiMethod = _method;
        executionTime = _executionTime;
        apiContractDict[msg.sender] = block.timestamp; // Enregistre l'appelant et le temps
    }
}
```
9. Deploy the smart contract on [remix.ethereum.org](https://remix.ethereum.org/): 
    - Copy __CONTRACT_BYTECODE__ & __CONTRACT_ADDRESS__  to __.env__.
    - Copy __CONTRACT_ABI__ & __CONTRACT_ADDRESS__ to __api/api_contract.py__.
    - Copy __ALCHEMY_URL__ & __CONTRACT_ADDRESS__ to __api/views.py__.
10. READ carefully the __Important Notes__ below before Running the development server:
```bash
python manage.py runserver
```
1.  Open your web browser and navigate to http://127.0.0.1:8000/api/persons/ to access the API endpoints.


## Usage
### CRUD Operations

1. Retrieve all persons:
```bash
curl http://127.0.0.1:8000/api/persons/
```
2. Retrieve a specific person:
```bash
curl http://127.0.0.1:8000/api/persons/1/
```
3. Update a person (If necessary, replace the address with your own):
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"firstname": "John", "lastname": "Doe", "sex": "M", "email": "john.doe@example.com", "phone": "1234567890", "city": "New York", "country": "USA", "age": 30}' http://127.0.0.1:8000/api/persons/1/
```
4. Delete a person:
```bash
curl -X DELETE http://127.0.0.1:8000/api/persons/1/
```

### Smart Contract
1. __Retrieve the Contract Summary__:
```bash
curl http://127.0.0.1:8000/api/summary/
```
2. Retrieve the Contract Data:
```bash
curl http://127.0.0.1:8000/api/persons/contract/
```

## Importants Notes:

- The Smart Contract is deployed on the __Sepolia Testnet__.
- Create an [Alchemy account](https://www.alchemy.com/) , choose __Ethereum__ and __Sepolia Testnet__.
- create a __.env__ file and add your own values for the following variables:
```txt
    - ALCHEMY_URL (Your Alchemy URL)
    - MY_ADDRESS (Your Ethereum or Sepolia Address)
    - PRIVATE_KEY (Your Private Key)
    - CONTRACT_BYTECODE (Your Smart Contract Bytecode)
    - CONTRACT_ADDRESS (Your Smart Contract Address)
```
- The Smart Contract is deployed on [remix.ethereum.org](https://remix.ethereum.org/). After deploying the smart contract the following parameters will be available:
```txt
    - Sepolia Testnet
    - CONTRACT_BYTECODE (Your Smart Contract Bytecode)
    - CONTRACT_ADDRESS (Your Smart Contract Address)
    - CONTRACT_ABI (Your Smart Contract ABI)
```
- The estimated gas fee and the estimted gas price is calculated automatically. However, if you want to change the gas fee or the gas price, you can do it in __api/api_contract.py__.
  
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)