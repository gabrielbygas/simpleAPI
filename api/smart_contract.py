class APIContract:
    def __init__(self):
        """
        Initialisation des variables du smart contract.
        """
        self.api_status = False  # Status par défaut
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
