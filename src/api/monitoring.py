import logging
from prometheus_client import Counter, Histogram
import time

# Метрики Prometheus
REQUESTS = Counter('food_calorie_requests_total', 'Total requests')
PREDICTIONS = Counter('food_calorie_predictions_total', 'Total predictions')
ERRORS = Counter('food_calorie_errors_total', 'Total errors')
PROCESSING_TIME = Histogram('food_calorie_processing_seconds', 'Time spent processing request')

class Monitoring:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
    
    def log_request(self, request_data):
        REQUESTS.inc()
        self.logger.info(f"New request received: {request_data}")
    
    def log_prediction(self, prediction_result):
        PREDICTIONS.inc()
        self.logger.info(f"Prediction made: {prediction_result}")
    
    def log_error(self, error):
        ERRORS.inc()
        self.logger.error(f"Error occurred: {error}")
    
    @PROCESSING_TIME.time()
    def measure_processing_time(self, func):
        return func() 