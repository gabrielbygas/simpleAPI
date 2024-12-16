import json
from datetime import datetime

class APIContract:
    def __init__(self):
        """
        Initialisation des variables du smart contract.
        """
        self.api_status = False  # Status par défaut
        self.request_id = ""
        self.api_method = None   # Méthode utilisée (GET, POST, etc.)
        self.connection_time = 0  # Temps de connexion (en microsecondes)
        self.api_contract_dict = {}  # Dictionnaire des appels précédents

    def update_contract(self, request_id, method, execution_time):
        """
        Met à jour les variables du contrat après un appel réussi.
        :param request_id: ID ou adresse unique de la requête
        :param method: Méthode HTTP utilisée (GET, POST, etc.)
        :param execution_time: Temps d'exécution de la requête
        """
        self.api_status = True  # L'appel est réussi
        self.api_method = method
        self.connection_time = execution_time

        # Ajouter les données au dictionnaire
        self.api_contract_dict[request_id] = {
            "method": method,
            "execution_time": execution_time
        }

    def view_contract_dict(self):
        """
        Retourne le dictionnaire des appels sous forme de tableau.
        """
        print("APIContractDict:")
        print(f"{'Request ID':<15} {'Method':<10} {'Execution Time (microsecondes)':<20}")
        print("-" * 50)
        for request_id, details in self.api_contract_dict.items():
            print(f"{request_id:<15} {details['method']:<10} {details['execution_time']:<20}")

    def save_to_file(self, fichier, request_id, method, execution_time):
        
        today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Obtenir la date du jour
        self.request_id = request_id
        self.api_status = True  # Status par défaut
        self.api_method = method   # Méthode utilisée (GET, POST, etc.)
        self.connection_time = execution_time  # Temps de connexion (en microsecondes)

        # execution_time = execution_time / 1000000
        
        # Créer un dictionnaire avec les données
        new_data = {
            "date": today_date,
            "request_id": request_id,
            "method": method,
            "status": self.api_status,
            "execution_time": str(execution_time) + " microsecondes"
        }
        
        # Lire les données existantes
        try:
            with open(fichier, 'r') as fichier_json:
                 # Check if file is empty
                if fichier_json.read().strip() == "":
                    previous_data = []
                else:
                    fichier_json.seek(0)  # Reset the file pointer
                    previous_data = json.load(fichier_json)
        except (FileNotFoundError, json.JSONDecodeError):
            previous_data = []

        # Ajouter les nouvelles données
        previous_data.append(new_data)
        
        # Écrire les données mises à jour dans le fichier
        with open(fichier, 'w') as fichier_json:
            json.dump(previous_data, fichier_json, indent=4)
        
        print("Données enregistrées avec succès!")
