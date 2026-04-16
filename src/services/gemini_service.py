import google.generativeai as genai
import asyncio

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Gemini 3.0 Flash is selected per the instructions for real-time cognitive insights
        self.model = genai.GenerativeModel("gemini-3.0-flash")

    async def generate_vibe_alerts(self, venue_data: dict) -> str:
        """
        Takes venue heatmap/congestion data and suggests actionable Vibe Alerts.
        Uses Async execution for non-blocking IO.
        """
        prompt = f"""
        You are 'VenueFlow AI', a real-time event coordinator.
        The current congestion data is:
        {venue_data}

        Generate a short 'Vibe Alert' to direct attendees to less crowded gates and concessions.
        Format it dynamically (e.g., 'Gate 4 is crowded; take the Scenic Bridge route to Gate 2 for a 5-minute faster entry').
        Make it high-energy and accessible. Keep it under 3 sentences.
        """
        # Execute asynchronously
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self.model.generate_content, prompt)
        return response.text
