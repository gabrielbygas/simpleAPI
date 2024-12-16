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
from .api_contract import call_update_contract
from django.http import JsonResponse
import json

# Connexion au réseau Ethereum via Alchemy
# Initialisation de Web3 - copy here
w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/AGLtz5e1Ed_0bO4GssdONwnVUacPn3_x'))

# Adresse du contrat déployé - copy here
CONTRACT_ADDRESS = "0xd8b934580fcE35a11B58C6D73aDeE468a2833fa8"

# Instancier un contrat global (optionnel, pour persistance)
smart_contract = APIContract()

# Fichier de stockage des données
FILENAME = "summary.json"

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

            # Mettre à jour le smart contract
            request_id = f"GET-{pk}"
            execution_time = int((time.perf_counter() - start_time) * 1000000)
            print(f"\n avant save_to_file \n")
            smart_contract.save_to_file(FILENAME, request_id, "GET", execution_time)
            print(f"\n apres save_to_file \n")

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time} microsecondes"},
                status=status.HTTP_200_OK,
            )

        # Récupération de toutes les personnes
        persons = Persons.objects.all()
        serializer = PersonsSerializer(persons, many=True)

        # Mettre à jour le smart contract
        request_id = f"GET_ALL-{int(time.time() * 1000000)}"
        execution_time = int((time.perf_counter() - start_time) * 1000000)
        smart_contract.save_to_file(FILENAME, request_id, "GET_ALL", execution_time)

        return Response(
            {"data": serializer.data, "execution_time": f"{execution_time} microsecondes"},
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

            # Mettre à jour le smart contract
            request_id = f"POST-{serializer.data['id']}"
            execution_time = int((time.perf_counter() - start_time) * 1000000)
            smart_contract.save_to_file(FILENAME, request_id, "POST", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time} microsecondes"},
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
            
            # Mettre à jour le smart contract
            request_id = f"PUT-{serializer.data['id']}"
            execution_time = int((time.perf_counter() - start_time) * 1000000)
            smart_contract.save_to_file(FILENAME, request_id, "PUT", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time} microsecondes"},
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
        
        # Mettre à jour le smart contract
        request_id = f"DELETE-{pk}"
        execution_time = int((time.perf_counter() - start_time) * 1000000)
        smart_contract.save_to_file(FILENAME, request_id, "DELETE", execution_time)
        
        return Response(
            {"message": "Person deleted successfully.", "execution_time": f"{execution_time} microsecondes"},
            status=status.HTTP_204_NO_CONTENT,
        )
    
    
# Classe d'API pour récupérer le résumé des contrats dans le dictionnaire du smart contract.
class GetContractSummary(APIView):
    """
    Vue pour récupérer le résumé des contrats dans le dictionnaire du smart contract.
    """

    def get(self, request):
        try:
            # Ouvrir le fichier JSON et charger son contenu
            with open('summary.json') as json_file:
                data = json.load(json_file)

            if not data:
                return JsonResponse({"error": "No data found"}, status=404)
        
            # Retourner le contenu sous forme de réponse JSON
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

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
            call_update_contract(CONTRACT_ADDRESS, True, "GET", int((time.perf_counter() - start_time) * 1000000))
            execution_time = int((time.perf_counter() - start_time) * 1000000)
            smart_contract.save_to_file(FILENAME, request_id, "GET", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time} microsecondes"},
                status=status.HTTP_200_OK,
            )

        # Récupération de toutes les personnes
        persons = Persons.objects.all()
        serializer = PersonsSerializer(persons, many=True)

        # Mettre à jour le smart contract
        request_id = f"GET_ALL-{int(time.time() * 1000000)}"
        call_update_contract(CONTRACT_ADDRESS, True, "GET", int((time.perf_counter() - start_time) * 1000000))
        execution_time = int((time.perf_counter() - start_time) * 1000000)
        smart_contract.save_to_file(FILENAME, request_id, "GET_ALL with Smart Contract", execution_time)

        return Response(
            {"data": serializer.data, "execution_time": f"{execution_time} microsecondes"},
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
            call_update_contract(CONTRACT_ADDRESS, True, "POST", int((time.perf_counter() - start_time) * 1000000))
            execution_time = int((time.perf_counter() - start_time) * 1000000)
            smart_contract.save_to_file(FILENAME, request_id, "POST with Smart Contract", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time} microsecondes"},
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
            call_update_contract(CONTRACT_ADDRESS, True, "PUT", int((time.perf_counter() - start_time) * 1000000))
            execution_time = int((time.perf_counter() - start_time) * 1000000)
            smart_contract.save_to_file(FILENAME, request_id, "PUT with Smart Contract", execution_time)

            return Response(
                {"data": serializer.data, "execution_time": f"{execution_time} microsecondes"},
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
        call_update_contract(CONTRACT_ADDRESS, True, "GET", int((time.perf_counter() - start_time) * 1000000))
        execution_time = int((time.perf_counter() - start_time) * 1000000)
        smart_contract.save_to_file(FILENAME, request_id, "DELETE with Smart Contract", execution_time)

        return Response(
            {"message": "Person deleted successfully.", "execution_time": f"{execution_time} microsecondes"},
            status=status.HTTP_204_NO_CONTENT,
        )