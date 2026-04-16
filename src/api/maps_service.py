import asyncio

class MapsService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # We would use googlemaps python client here in prod
        # import googlemaps
        # self.gmaps = googlemaps.Client(key=self.api_key)

    async def get_walking_directions(self, origin: str, dest: str) -> dict:
        """Simulates calling Google Maps Directions API via asyncio."""
        await asyncio.sleep(0.05)
        # Mocking Maps API distance and duration calculation
        return {
            "origin": origin,
            "destination": dest,
            "duration": "5 mins",
            "distance": "0.3 miles",
            "steps": ["Walk straight 100 yds", "Take the Scenic Bridge"]
        }
