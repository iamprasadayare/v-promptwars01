import pytest
from unittest.mock import Mock, patch
from src.services.db_service import DBService
from src.services.secret_service import SecretService
from src.api.storage_service import StorageService
from src.api.gcp_observability import GCPObservability

def test_db_service_init():
    with patch('google.cloud.firestore.Client') as mock_client:
        service = DBService(project_id="test-project")
        assert service.project_id == "test-project"

def test_storage_service_init():
    with patch('google.cloud.storage.Client') as mock_client:
        service = StorageService(project_id="test-project")
        assert service.client is not None

def test_secret_service_init():
    with patch('google.cloud.secretmanager.SecretManagerServiceClient') as mock_client:
        service = SecretService(project_id="test-project")
        assert service.project_id == "test-project"

def test_observability_init():
    with patch('google.cloud.logging.Client') as mock_log:
        with patch('google.cloud.monitoring_v3.MetricServiceClient') as mock_mon:
            obs = GCPObservability(project_id="test-project")
            assert obs.project_id == "test-project"

@pytest.mark.asyncio
async def test_db_record_vibe_alert_mocked():
    with patch('google.cloud.firestore.Client') as mock_client:
        db = DBService(project_id="test-project")
        mock_db = Mock()
        db.db = mock_db
        
        # Test the active integration logic
        await db.record_vibe_alert("Test Insight")
        mock_db.collection.assert_called_with("vibe_history")
