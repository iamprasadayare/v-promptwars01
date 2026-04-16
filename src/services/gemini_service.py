import google.generativeai as genai
import asyncio

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # gemini-2.0-flash is selected as it is explicitly available in your hackathon environment
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def generate_vibe_alerts(self, venue_data: dict, img_bytes: bytes | None = None) -> str:
        """
        Takes venue heatmap/congestion data and suggests actionable Vibe Alerts.
        Uses Async execution for non-blocking IO.
        """
        try:
            prompt = f"""
            You are 'VenueFlow AI', a real-time event coordinator.
            The current congestion data is:
            {venue_data}

            Generate a short 'Vibe Alert' to direct attendees to less crowded gates and concessions.
            Format it dynamically (e.g., 'Gate 4 is crowded; take the Scenic Bridge route to Gate 2 for a 5-minute faster entry').
            If an image of the crowd is provided, heavily incorporate the visual density and safety context you see into your alert.
            Make it high-energy and accessible. Keep it under 3 sentences.
            """
            
            contents = [prompt]
            if img_bytes:
                import PIL.Image
                import io
                img = PIL.Image.open(io.BytesIO(img_bytes))
                contents.append(img)

            # Execute asynchronously
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.model.generate_content, contents)
            return response.text
        except Exception as e:
            raise Exception(f"Cognitive Analysis Failed: {str(e)}")
