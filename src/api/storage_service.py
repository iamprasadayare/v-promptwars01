from google.cloud import storage

class StorageService:
    def __init__(self, project_id: str = "v-promptwars01"):
        try:
            self.client = storage.Client(project=project_id)
        except Exception:
            self.client = None

    def get_floor_plan_image_bytes(self, bucket_name: str, blob_name: str) -> bytes | None:
        """Downloads high-resolution venue assets as raw bytes via Cloud Storage CDN."""
        if not self.client: return None
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            return blob.download_as_bytes()
        except Exception:
            # Fallback for hackathon demo if bucket doesn't exist
            return None
