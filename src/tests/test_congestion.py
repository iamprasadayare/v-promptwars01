import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from src.logic.congestion_algorithm import CongestionAlgorithm
from src.services.db_service import DBService
from src.services.gemini_service import GeminiService
from src.api.maps_service import MapsService
from src.api.gcp_observability import GCPObservability

@pytest.fixture
def mock_services():
    gemini = Mock(spec=GeminiService)
    gemini.generate_vibe_alerts = AsyncMock(return_value="Route through Gate 2 for better entry.")

    db = Mock(spec=DBService)
    db.get_venue_data = AsyncMock(return_value={"gates": {"Gate 4": {"congestion": "High"}}})
    db.record_vibe_alert = AsyncMock()

    maps = Mock(spec=MapsService)
    maps.get_walking_directions = AsyncMock(return_value={"duration": "5 mins"})

    obs = Mock(spec=GCPObservability)
    # mock tracing context manager
    span_mock = Mock()
    span_mock.__enter__ = Mock(return_value=span_mock)
    span_mock.__exit__ = Mock(return_value=False)
    
    tracer_mock = Mock()
    tracer_mock.start_as_current_span.return_value = span_mock
    obs.tracer = tracer_mock

    return gemini, db, maps, obs

@pytest.mark.asyncio
async def test_analyze_congestion(mock_services):
    gemini, db, maps, obs = mock_services
    algo = CongestionAlgorithm(gemini, db, maps, obs)
    
    result = await algo.analyze_congestion()
    
    assert "Route through Gate 2" in result
    db.get_venue_data.assert_called_once()
    db.record_vibe_alert.assert_called_once_with(result)
    maps.get_walking_directions.assert_called_once_with("Gate 4", "Gate 2")
    gemini.generate_vibe_alerts.assert_called_once()
