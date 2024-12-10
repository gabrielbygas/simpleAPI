import time
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Persons
from .serializers import PersonsSerializer
from .smart_contract import APIContract  # Importer la classe du smart contract
from web3 import Web3


# Connexion au réseau Ethereum via Alchemy
# Initialisation de Web3
w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/AGLtz5e1Ed_0bO4GssdONwnVUacPn3_x'))
"""
Uncomment this line: 
contract_address = '0xYourContractAddressHere' 
"""
# contract_address = '0xYourContractAddressHere' # Uncomment this line.


abi = [
    # Insère l'ABI ici
]

"""
Uncomment this line: 
contract = w3.eth.contract(address=contract_address, abi=abi)
"""
# contract = w3.eth.contract(address=contract_address, abi=abi) # Uncomment this line.

# Instancier un contrat global (optionnel, pour persistance)
smart_contract = APIContract()

# Classe d'API pour les opérations CRUD sur les personnes avec calcul du temps d'exécution sans Smart Contract.
class PersonsAPIView(APIView):
    """
    API pour les opérations CRUD sur les personnes avec calcul du temps d'exécution.
    """

    def get(self, request, pk=None, *args, **kwargs):
        """
        Gère les requêtes GET avec calcul du temps d'exécution.
        """
        start_time = time.perf_counter()

        if pk is not None:
            # Récupération d'une seule personne
            person = get_object_or_404(Persons, pk=pk)
            serializer = PersonsSerializer(person)
            execution_time = (time.perf_counter() - start_time) * 1000

             # Mettre à jour le smart contract
            request_id = f"GET-{pk}"
            smart_contract.update_contract(request_id, "GET", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time:.2f} ms"},
                status=status.HTTP_200_OK,
            )

        # Récupération de toutes les personnes
        persons = Persons.objects.all()
        serializer = PersonsSerializer(persons, many=True)
        execution_time = (time.perf_counter() - start_time) * 1000

        # Mettre à jour le smart contract
        request_id = f"GET_ALL-{int(time.time() * 1000)}"
        smart_contract.update_contract(request_id, "GET", execution_time)

        return Response(
            {"data": serializer.data, "execution_time": f"{execution_time:.2f} ms"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        """
        Gère les requêtes POST avec calcul du temps d'exécution.
        """
        start_time = time.perf_counter()

        serializer = PersonsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            execution_time = (time.perf_counter() - start_time) * 1000

             # Mettre à jour le smart contract
            request_id = f"POST-{serializer.data['id']}"
            smart_contract.update_contract(request_id, "POST", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time:.2f} ms"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        """
        Gère les requêtes PUT (mise à jour complète) avec calcul du temps d'exécution.
        """
        start_time = time.perf_counter()

        person = get_object_or_404(Persons, pk=pk)
        serializer = PersonsSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            execution_time = (time.perf_counter() - start_time) * 1000
            
            # Mettre à jour le smart contract
            request_id = f"PUT-{serializer.data['id']}"
            smart_contract.update_contract(request_id, "PUT", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time:.2f} ms"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Gère les requêtes DELETE avec calcul du temps d'exécution.
        """
        start_time = time.perf_counter()

        person = get_object_or_404(Persons, pk=pk)
        person.delete()
        execution_time = (time.perf_counter() - start_time) * 1000

        # Mettre à jour le smart contract
        request_id = f"DELETE-{pk}"
        smart_contract.update_contract(request_id, "DELETE", execution_time)
        
        return Response(
            {"message": "Person deleted successfully.", "execution_time": f"{execution_time:.2f} ms"},
            status=status.HTTP_204_NO_CONTENT,
        )
    
    def get_contract_summary(self, request, *args, **kwargs):
        """
        Affiche le contenu du dictionnaire du smart contract.
        """
        contract_data = smart_contract.api_contract_dict
        return Response(contract_data, status=status.HTTP_200_OK)
    
# Classe d'API pour récupérer le résumé des contrats dans le dictionnaire du smart contract.
class GetContractSummary(APIView):
    """
    Vue pour récupérer le résumé des contrats dans le dictionnaire du smart contract.
    """

    def get(self, request, *args, **kwargs):
        """
        Gérer les requêtes GET pour renvoyer le résumé des contrats.
        """
        return Response(
            smart_contract.api_contract_dict,
            status=status.HTTP_200_OK
        )

# Fonction utilitaire pour interagir avec le smart contract
def update_contract_data(request_id, method, execution_time):
    """
    Met à jour les données dans le smart contract.

    :param request_id: Identifiant de la requête (ex. : GET-123).
    :param method: Méthode HTTP utilisée (GET, POST, etc.).
    :param execution_time: Temps d'exécution de l'opération (en ms).
    """
    try:
        tx = contract.functions.updateContractData(
            request_id,
            True,  # Statut (par défaut, succès)
            method,
            w3.eth.default_account  # Remplace par ton adresse Ethereum
        ).build_transaction({
            'from': '0xYourAddressHere',
            'gas': 3000000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': w3.eth.get_transaction_count('0xYourAddressHere'),
        })

        # Signer et envoyer la transaction
        private_key = 'YourPrivateKeyHere'
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Attendre la confirmation
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction confirmée : {receipt.transactionHash.hex()}")
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour du smart contract : {e}")
        return False
    
# Classe CRUD API avec interaction avec le smart contract
class PersonsContractAPIView(APIView):
    """
    API pour les opérations CRUD sur les personnes avec interaction avec un smart contract.
    """

    def get(self, request, pk=None, *args, **kwargs):
        """
        Récupère une ou plusieurs personnes et met à jour le smart contract.
        """
        start_time = time.perf_counter()

        if pk is not None:
            # Récupération d'une seule personne
            person = get_object_or_404(Persons, pk=pk)
            serializer = PersonsSerializer(person)

            # Mettre à jour le smart contract
            request_id = f"GET-{pk}"
            execution_time = (time.perf_counter() - start_time) * 1000
            update_contract_data(request_id, "GET", execution_time)
            smart_contract.update_contract(request_id, "GET with Smart Contract", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time:.2f} ms"},
                status=status.HTTP_200_OK,
            )

        # Récupération de toutes les personnes
        persons = Persons.objects.all()
        serializer = PersonsSerializer(persons, many=True)

        # Mettre à jour le smart contract
        request_id = f"GET_ALL-{int(time.time() * 1000)}"
        execution_time = (time.perf_counter() - start_time) * 1000
        update_contract_data(request_id, "GET", execution_time)
        smart_contract.update_contract(request_id, "GET_ALL with Smart Contract", execution_time)

        return Response(
            {"data": serializer.data, "execution_time": f"{execution_time:.2f} ms"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        """
        Crée une nouvelle personne et met à jour le smart contract.
        """
        start_time = time.perf_counter()

        serializer = PersonsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Mettre à jour le smart contract
            request_id = f"POST-{serializer.data['id']}"
            execution_time = (time.perf_counter() - start_time) * 1000
            update_contract_data(request_id, "POST", execution_time)
            smart_contract.update_contract(request_id, "POST with Smart Contract", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time:.2f} ms"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        """
        Met à jour une personne existante et met à jour le smart contract.
        """
        start_time = time.perf_counter()

        person = get_object_or_404(Persons, pk=pk)
        serializer = PersonsSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Mettre à jour le smart contract
            request_id = f"PUT-{serializer.data['id']}"
            execution_time = (time.perf_counter() - start_time) * 1000
            update_contract_data(request_id, "PUT", execution_time)
            smart_contract.update_contract(request_id, "PUT with Smart Contract", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time:.2f} ms"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Supprime une personne et met à jour le smart contract.
        """
        start_time = time.perf_counter()

        person = get_object_or_404(Persons, pk=pk)
        person.delete()

        # Mettre à jour le smart contract
        request_id = f"DELETE-{pk}"
        execution_time = (time.perf_counter() - start_time) * 1000
        update_contract_data(request_id, "DELETE", execution_time)
        smart_contract.update_contract(request_id, "DELETE with Smart Contract", execution_time)

        return Response(
            {"message": "Person deleted successfully.", "execution_time": f"{execution_time:.2f} ms"},
            status=status.HTTP_204_NO_CONTENT,
        )