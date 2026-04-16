from google.cloud import secretmanager

class SecretService:
    def __init__(self, project_id: str = "v-promptwars01"):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str) -> str:
        """Fetch secret payload from Google Cloud Secret Manager."""
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            # Fallback for local testing or if secret is missing but injected via env vars
            import os
            return os.getenv(secret_id, "")
