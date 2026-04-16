import streamlit as st
import asyncio
from src.services.gemini_service import GeminiService
from src.services.db_service import DBService
from src.services.secret_service import SecretService
from src.api.gcp_observability import GCPObservability
from src.api.maps_service import MapsService
from src.api.storage_service import StorageService
from src.logic.congestion_algorithm import CongestionAlgorithm

# Accessibility & Theming
st.set_page_config(page_title="VenueFlow AI", layout="wide", initial_sidebar_state="expanded")

# Inject Google Analytics Tag (mock component for metrics)
st.markdown("""
    <!-- Google Analytics Mock -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-XXXX');
    </script>
""", unsafe_allow_html=True)

def init_services() -> CongestionAlgorithm:
    # Init observabilty
    obs = GCPObservability(project_id="v-promptwars01")
    obs.log_info("Initializing VenueFlow AI Application")
    
    # Secrets & Config
    secrets = SecretService(project_id="v-promptwars01")
    gemini_key = secrets.get_secret("GEMINI_API_KEY")
    maps_key = secrets.get_secret("MAPS_API_KEY")
    
    # Intialize Services
    gemini = GeminiService(api_key=gemini_key)
    db = DBService()
    maps = MapsService(api_key=maps_key)
    
    # Build Logic Component
    return CongestionAlgorithm(gemini_service=gemini, db_service=db, maps_service=maps, obs=obs)

def get_logic():
    return init_services()

def main():
    st.title("🏟️ VenueFlow AI: Event Optimization")
    st.subheader("Ensure a seamless, high-vibe physical event experience.")
    
    algo = get_logic()
    storage = StorageService()
    floor_plan_url = storage.get_floor_plan_url("v-promptwars01-cdn", "floorplan.png")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("##### Venue Layout & Live Congestion")
        # High-contrast mapping visual representation
        st.markdown(
            f"""
            <div style="padding: 10px; border-radius: 10px; background-color: #1e1e1e; color: #fff;" aria-label="Venue Floor Plan Map">
                <center>
                <strong>Live Floor Plan</strong><br/>
                <img src="{floor_plan_url}" alt="Floor plan not found" style="max-height: 200px; opacity: 0.5;">
                <p style="font-size: 0.9em; color: #aaa;">(High-resolution map served via Cloud Storage CDN)</p>
                </center>
            </div>
            """, unsafe_allow_html=True
        )

        st.write("##### Live Crowd Camera (Optional)")
        uploaded_file = st.file_uploader("Upload live CCTV snapshot for AI Vision analysis", type=["jpg", "png", "jpeg"])

    with col2:
        st.write("##### ⚡ AI Vibe Alerts")
        if st.button("Generate Dynamic Redirection", help="Analyze real-time data to reroute crowds", type="primary"):
            with st.spinner("Analyzing heatmaps & visual footage with Gemini Vision..."):
                try:
                    img_bytes = uploaded_file.getvalue() if uploaded_file else None
                    # Run async task
                    vibe_alert = asyncio.run(algo.analyze_congestion(img_bytes))
                    st.success("Analysis Complete!")
                    st.info(f"🔊 **ALERT:** {vibe_alert}")
                    algo.obs.log_info("Successfully generated Vibe Alert on UI")
                except Exception as e:
                    st.error(f"Failed to generate insight: {e}")
                    algo.obs.log_error(f"UI Error: {e}")

if __name__ == "__main__":
    main()
