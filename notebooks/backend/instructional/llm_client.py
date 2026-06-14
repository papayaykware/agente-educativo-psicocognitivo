"""
llm_client.py — Cliente para modelos de lenguaje (LLM)
Autor conceptual: Copilot
"""

import os
import requests

class LLMClient:
    """
    Cliente genérico para un LLM externo.
    Permite cambiar de proveedor sin tocar el resto del backend.
    """

    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.api_url = os.getenv("LLM_API_URL", "")

        if not self.api_key or not self.api_url:
            raise ValueError("Faltan variables de entorno: LLM_API_KEY o LLM_API_URL")

    def generate(self, system_prompt: str, user_message: str) -> str:
        """
        Envía un prompt al LLM y devuelve la respuesta generada.
        """

        payload = {
            "model": "llm-model-name",  # sustituible
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.4
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.api_url, json=payload, headers=headers)

        if response.status_code != 200:
            return f"Error del LLM: {response.text}"

        data = response.json()
        return data["choices"][0]["message"]["content"]
