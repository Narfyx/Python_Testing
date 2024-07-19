# commmande:
# locust --headless --users 6 --spawn-rate 1 -H http://127.0.0.1:5001
"""
GET /:
    # reqs: 37 (nombre de fois que la page d'accueil a été chargée).
    # fails: 0 (aucune requête échouée).
    Avg: 4 ms (temps de réponse moyen).
    Min: 3 ms (temps de réponse minimum).
    Max: 4 ms (temps de réponse maximum).
    Med: 4 ms (temps de réponse médian).
    req/s: 0.40 (taux de requêtes par seconde).

POST /showSummary:
    # reqs: 300 (nombre de fois que l'authentification a été testée).
    # fails: 0 (aucune requête échouée).
    Avg: 5 ms (temps de réponse moyen).
    Min: 4 ms (temps de réponse minimum).
    Max: 30 ms (temps de réponse maximum).
    Med: 5 ms (temps de réponse médian).
    req/s: 3.21 (taux de requêtes par seconde).

Aggregated:
    # reqs: 667 (nombre total de requêtes).
    # fails: 0 (aucune requête échouée).
    Avg: 5 ms (temps de réponse moyen pour toutes les requêtes).
    Min: 3 ms (temps de réponse minimum pour toutes les requêtes).
    Max: 30 ms (temps de réponse maximum pour toutes les requêtes).
    Med: 5 ms (temps de réponse médian pour toutes les requêtes).
    req/s: 7.13 (taux global de requêtes par seconde).
"""

from locust import HttpUser, task, between


class testPerf(HttpUser):
    wait_time = between(1, 2)

    @task(1)  # Cette tâche sera exécutée avec une pondération de 1
    def load_default_page(self):
        self.client.get("/")

    @task(3)  # Cette tâche sera exécutée avec une pondération de 3
    def login(self):
        response = self.client.post(
            "/showSummary", data={"email": "john@simplylift.co"}
        )
        if response.status_code == 200:
            self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task(2)  # Cette tâche sera exécutée avec une pondération de 2
    def purchase_places(self):
        # Login first
        response = self.client.post(
            "/showSummary", data={"email": "john@simplylift.co"}
        )
        if response.status_code == 200:
            # Simulate booking a place
            self.client.post(
                "/purchasePlaces",
                data={
                    "competition": "Spring Festival",
                    "club": "Simply Lift",
                    "places": "1",
                },
            )

    @task(4)  # Cette tâche sera exécutée avec une pondération de 4
    def load_summary_page(self):
        response = self.client.post(
            "/showSummary", data={"email": "john@simplylift.co"}
        )
        if response.status_code == 200:
            self.client.get("/showSummary")

    @task(1)  # Cette tâche sera exécutée avec une pondération de 1
    def logout(self):
        self.client.get("/logout")
