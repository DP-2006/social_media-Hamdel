# apps/messaging/ai_client.py
import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model="gemma3:27b"):
        self.base_url = base_url
        self.model = model
        self.enabled = self._check_availability()
    
    def _check_availability(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def is_available(self):
        return self.enabled
    
    def generate(self, prompt, temperature=0.7, max_tokens=500):
        if not self.enabled:
            return {"success": False, "error": "Ollama not available"}
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response": response.json().get("response", "")
                }
            else:
                return {"success": False, "error": "Ollama error"}
        except Exception as e:
            return {"success": False, "error": str(e)}