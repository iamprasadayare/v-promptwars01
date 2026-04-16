# VenueFlow AI

VenueFlow AI is a high-performance, accessible, and secure application designed to optimize the physical event experience for attendees at large-scale sporting venues. Built for the Google PromptWars Hackathon.

## Features
- Provides dynamic congestion alerts to redirect attendees efficiently.
- Uses Gemini 3.0 Flash for proactive cognitive insights ("Vibe Alerts").

## Google Services Map (10 Services Evaluated)
1. **Gemini 3.0 Flash (Generative API)**: Cognitive engine generating optimized real-time crowd redirection.
2. **Cloud Run**: Serverless container hosting ensuring scalability.
3. **Firestore**: Real-time NoSQL state management storing venue mock heatmaps and wait times.
4. **Secret Manager**: Fully secure handling of API keys without hardcoding.
5. **Google Maps Platform**: Visualization logic for gate layout.
6. **Cloud Logging**: Maintainability enhancement with centralized application audit trails.
7. **Cloud Monitoring**: Efficiency and latency tracking to monitor performance.
8. **Cloud Storage**: Used to host and deliver high-resolution floor plans for the venue layout (CDN).
9. **Cloud Trace**: Trace spans profiling Streamlit rendering and API latency.
10. **Google Analytics**: Web behavior and usage tracking via injected JS tags into Streamlit.

## Security & Accessibility
- Secure Key Rotation via Secret Manager.
- High-contrast UI rendering in Streamlit (`layout="wide"`).
- OOD design with asynchronous `asyncio` APIs for efficiency.
