"""
llm_client.py — Cliente para modelos de lenguaje (LLM)
Autor conceptual: Copilot
"""

import os
import json
import requests

class LLMClient:
    """
    Cliente genérico para un LLM externo.
    Permite cambiar de proveedor sin tocar el resto del backend.
    """

    def __init__(self):
        # 1. Intentar cargar desde variables de entorno
        api_key = os.getenv("LLM_API_KEY")
        api_url = os.getenv("LLM_API_URL")

        # 2. Si no existen, intentar cargar config.json
        if not api_key or not api_url:
            try:
                with open("backend/config/config.json") as f:
                    cfg = json.load(f)
                    api_key = api_key or cfg.get("LLM_API_KEY")
                    api_url = api_url or cfg.get("LLM_API_URL")
            except FileNotFoundError:
                pass

        # 3. Si aún falta algo, error elegante
        if not api_key or not api_url:
            raise ValueError(
                "No se encontró configuración para el LLM. "
                "Crea backend/config/config.json o define variables de entorno."
            )

        self.api_key = api_key
        self.api_url = api_url

    def generate(self, system_prompt: str, user_message: str) -> str:
        """
        Envía un prompt al LLM y devuelve la respuesta generada.
        """

        payload = {
            "model": "llm-model-name",
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

