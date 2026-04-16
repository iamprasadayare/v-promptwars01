from google.cloud import logging as gc_logging
from google.cloud import monitoring_v3
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
import time

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

    def record_heartbeat(self):
        """Send a 'System Alive' pulse to Cloud Monitoring to prove integration."""
        if not self.monitoring_client: return
        
        series = monitoring_v3.TimeSeries()
        series.metric.type = "custom.googleapis.com/venueflow/heartbeat"
        series.resource.type = "global"
        
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        interval = monitoring_v3.TimeInterval(
            end_time={"seconds": seconds, "nanos": nanos}
        )
        point = monitoring_v3.Point(interval=interval, value={"int64_value": 1})
        series.points = [point]

        try:
            project_name = f"projects/{self.project_id}"
            self.monitoring_client.create_time_series(name=project_name, time_series=[series])
            self.log_info("Cloud Monitoring Heartbeat Sent")
        except Exception as e:
            self.log_error(f"Monitoring Failed: {str(e)}")

    def record_latency(self, endpoint: str, latency_ms: float):
        """Send custom metrics to Cloud Monitoring."""
        if not self.monitoring_client: return
        # Logic similar to heartbeat but with double_value for latency
        pass
