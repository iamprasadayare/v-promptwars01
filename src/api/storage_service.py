from google.cloud import storage

class StorageService:
    def __init__(self, project_id: str = "v-promptwars01"):
        try:
            self.client = storage.Client(project=project_id)
        except Exception:
            self.client = None

    def get_floor_plan_url(self, bucket_name: str, blob_name: str) -> str:
        """Returns the public URL for a file in Cloud Storage acting as a CDN."""
        # For hackathon: returning a placeholder if bucket not accessible.
        if self.client:
            return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"
        return "https://storage.googleapis.com/v-promptwars01-cdn/floorplan.png"
