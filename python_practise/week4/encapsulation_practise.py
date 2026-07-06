import sys
sys.path.insert(0, '.')
import logging

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class DataPipelineConfig:
    
    def __init__(self, name, source, batch_size):
        self.name = name                    # public
        self._source = source               # protected
        self.__batch_size = batch_size      # private
        self._status = "inactive"           # protected
    
    # @property — getter for source
    @property
    def source(self):
        return self._source
    
    # @source.setter — setter with validation
    @source.setter
    def source(self, value):
        allowed_sources = ["S3", "API", "Database", "Kafka"]
        if value not in allowed_sources:
            raise ValueError(f"{value} is not a valid source. Use: {allowed_sources}")
        logging.info(f"Source changed to {value}")
        self._source = value
    
    # @property — getter for batch_size
    @property
    def batch_size(self):
        return self.__batch_size
    
    # @batch_size.setter — setter with validation
    @batch_size.setter
    def batch_size(self, value):
        if value <= 0:
            raise ValueError("Batch size must be greater than 0")
        if value > 100000:
            logging.warning(f"Large batch size {value} may cause memory issues")
        self.__batch_size = value
    
    # @property — read only, no setter
    @property
    def status(self):
        return self._status
    
    def activate(self):
        self._status = "active"
        logging.info(f"Pipeline {self.name} activated")
    
    def get_info(self):
        return (f"Pipeline: {self.name} | "
                f"Source: {self._source} | "
                f"Batch: {self.__batch_size} | "
                f"Status: {self._status}")


# ── Test 1: Normal usage ──
config = DataPipelineConfig("NYC Taxi Pipeline", "S3", 1000)
print(config.get_info())

# ── Test 2: Valid source change ──
config.source = "API"
print(f"Source updated to: {config.source}")

# ── Test 3: Invalid source — should raise error ──
try:
    config.source = "Excel"
except ValueError as e:
    logging.error(f"Validation failed: {e}")

# ── Test 4: Valid batch size change ──
config.batch_size = 5000
print(f"Batch size updated to: {config.batch_size}")

# ── Test 5: Invalid batch size ──
try:
    config.batch_size = -500
except ValueError as e:
    logging.error(f"Validation failed: {e}")

# ── Test 6: Large batch size — warning ──
config.batch_size = 99999

# ── Test 7: Status is read only ──
try:
    config.status = "inactive"  # should fail — no setter
except AttributeError as e:
    logging.error(f"Cannot set status directly: {e}")

# ── Test 8: Activate pipeline ──
config.activate()
print(config.get_info())