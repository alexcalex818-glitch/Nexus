
import os
import requests


class NexusIntelligenceRouter:

    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.together_key = os.getenv("TOGETHER_API_KEY")

        self.gemini_model = os.getenv(
            "GEMINI_MODEL", "gemini-2.5-flash"
        )

        self.together_model = os.getenv(
            "TOGETHER_MODEL", "meta-llama/Llama-3.3-70B-Instruct-Turbo"
        )

    def choose_engine(self, task):
        complex_words = [
            "analyse approfondie",
            "raisonnement complexe",
            "compare",
            "stratégie",
            "étude détaillée"
        ]

        if any(word in task.lower() for word in complex_words):
            return "together"

        return "gemini"

    def ask_gemini(self, message):
        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.gemini_model}:generateContent"
        )

        response = requests.post(
            url,
            params={"key": self.gemini_key},
            json={
                "contents": [{
                    "parts": [{"text": message}]
                }]
            },
            timeout=45
        )

        response.raise_for_status()
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    def ask_together(self, message):
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.together_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.together_model,
                "messages": [
                    {"role": "user", "content": message}
                ]
            },
            timeout=45
        )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]

    def generate(self, message):
        primary = self.choose_engine(message)

        engines = (
            ["together", "gemini"]
            if primary == "together"
            else ["gemini", "together"]
        )

        for engine in engines:
            try:
                if engine == "gemini" and self.gemini_key:
                    answer = self.ask_gemini(message)
                    return {
                        "answer": answer,
                        "engine": "Gemini"
                    }

                if engine == "together" and self.together_key:
                    answer = self.ask_together(message)
                    return {
                        "answer": answer,
                        "engine": "Together AI"
                    }

            except (requests.RequestException, KeyError, IndexError, TypeError):
                continue

        return {
            "error": "Aucun moteur IA disponible pour le moment."
        }


nexus_router = NexusIntelligenceRouter()
