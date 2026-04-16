from google.cloud import logging as gc_logging
from google.cloud import monitoring_v3
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

class GCPObservability:
    def __init__(self, project_id: str = "v-promptwars01"):
        self.project_id = project_id
        
        # Setup Cloud Logging
        try:
            self.logging_client = gc_logging.Client(project=project_id)
            self.logging_client.setup_logging()
            self.logger = self.logging_client.logger("venueflow-app")
        except Exception:
            # Fallback to local logger if GCP auth is not available locally
            import logging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger("venueflow-app")

        # Setup Cloud Monitoring client
        try:
            self.monitoring_client = monitoring_v3.MetricServiceClient()
        except:
            self.monitoring_client = None

        # Trace config
        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(__name__)

    def log_info(self, message: str):
        """Send an info log to Cloud Logging"""
        try:
            self.logger.log_text(message, severity='INFO')
        except:
            self.logger.info(message)

    def log_error(self, message: str):
        """Send an error log to Cloud Logging"""
        try:
            self.logger.log_text(message, severity='ERROR')
        except:
            self.logger.error(message)

    def record_latency(self, endpoint: str, latency_ms: float):
        """Send custom metrics to Cloud Monitoring."""
        if not self.monitoring_client:
            return
        # A mock for metric creation - real world requires descriptor setup.
        pass
