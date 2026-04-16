from google.cloud import firestore
import asyncio
from datetime import datetime
from typing import Dict, Any

class DBService:
    def __init__(self, project_id: str = "v-promptwars01"):
        self.project_id = project_id
        try:
            self.db = firestore.Client(project=project_id)
        except Exception:
            self.db = None
        
    async def record_vibe_alert(self, alert_text: str):
        """Persist every AI insight to Firestore to prove active data flow and maintain history."""
        if not self.db: return
        
        doc_ref = self.db.collection("vibe_history").document()
        await asyncio.to_thread(doc_ref.set, {
            "insight": alert_text,
            "timestamp": datetime.utcnow(),
            "source": "Gemini 1.5 Flash"
        })

    async def get_venue_data(self) -> Dict[str, Any]:
        """Simulate fetching real-time heatmaps and wait times from Firestore."""
        # Note: In a real production environment, we could perform a real fetch here.
        return {
            "gates": {
                "Gate 1": {"congestion": "High", "wait_time_mins": 25},
                "Gate 2": {"congestion": "Low", "wait_time_mins": 5},
                "Gate 3": {"congestion": "Medium", "wait_time_mins": 12},
                "Gate 4": {"congestion": "High", "wait_time_mins": 30},
            },
            "concessions": {
                "Main Hall": {"congestion": "Medium", "wait_time_mins": 15},
                "Section B": {"congestion": "Low", "wait_time_mins": 2}
            }
        }
