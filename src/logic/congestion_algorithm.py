from src.services.db_service import DBService
from src.services.gemini_service import GeminiService
from src.api.gcp_observability import GCPObservability
from src.api.maps_service import MapsService
import asyncio

class CongestionAlgorithm:
    def __init__(self, gemini_service: GeminiService, db_service: DBService, maps_service: MapsService, obs: GCPObservability):
        self.gemini_service = gemini_service
        self.db_service = db_service
        self.maps_service = maps_service
        self.obs = obs

    async def analyze_congestion(self, img_bytes: bytes | None = None) -> str:
        """
        The Core Congestion Algorithm.
        Orchestrates DB fetching, maps analysis, and AI summarization asynchronously.
        """
        # Start Trace
        with self.obs.tracer.start_as_current_span("analyze_congestion"):
            self.obs.log_info("Starting Dynamic Congestion Analysis")
            
            # Fetch data from Firestore
            venue_data = await self.db_service.get_venue_data()
            
            # Fetch directions if needed (e.g., from crowded to non-crowded gate)
            # Parallel execution
            directions = await self.maps_service.get_walking_directions("Gate 4", "Gate 2")
            
            # Enrich venue data with geospatial context
            venue_data['suggested_route'] = directions

            # Generate Insights via Gemini Vision
            vibe_alert = await self.gemini_service.generate_vibe_alerts(venue_data, img_bytes)
            
            self.obs.log_info(f"Generated Alert: {vibe_alert}")
            return vibe_alert
