
class NexusCore:

    def __init__(self):
        self.name = "NEXUS CORE"
        self.version = "0.1"

        self.categories = {
            "income": [
                "emploi", "travail", "argent",
                "revenu", "commerce", "client"
            ],
            "food": [
                "nourriture", "manger", "repas",
                "aliment", "agriculture"
            ],
            "education": [
                "formation", "apprendre", "cours",
                "étude", "éducation"
            ],
            "support": [
                "aide", "accompagnement",
                "soutien", "assistance"
            ]
        }

    def analyze_need(self, message):

        text = message.lower()
        scores = {}

        for category, keywords in self.categories.items():
            scores[category] = sum(
                1 for word in keywords if word in text
            )

        best_category = max(scores, key=scores.get)

        if scores[best_category] == 0:
            best_category = "general"

        return {
            "need": message,
            "category": best_category,
            "scores": scores,
            "engine": self.name,
            "version": self.version
        }


nexus_core = NexusCore()
