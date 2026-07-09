import sys
sys.path.insert(0, '.')
import logging

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# ── CLASS 1: PipelineConfig ──
# Exists independently — does not need Pipeline to exist
class PipelineConfig:
    def __init__(self, source, destination, batch_size):
        self.source = source
        self.destination = destination
        self.batch_size = batch_size

    def get_config(self):
        return (f"Source: {self.source} | "
                f"Destination: {self.destination} | "
                f"Batch: {self.batch_size}")


# ── CLASS 2: DataQualityChecker ──
# Exists independently — can be used by any pipeline
class DataQualityChecker:
    def __init__(self, name):
        self.name = name

    def check_nulls(self, data):
        nulls = [row for row in data if None in row.values()]
        if nulls:
            logging.warning(f"{self.name}: Found {len(nulls)} rows with nulls")
            return False
        logging.info(f"{self.name}: No nulls found")
        return True

    def check_row_count(self, data, min_rows):
        if len(data) < min_rows:
            logging.error(f"{self.name}: Only {len(data)} rows, expected {min_rows}")
            return False
        logging.info(f"{self.name}: Row count OK — {len(data)} rows")
        return True


# ── CLASS 3: Pipeline ──
# AGGREGATION — Pipeline HAS-A PipelineConfig
# Config exists independently, Pipeline just uses it as component
class Pipeline:
    def __init__(self, name, config):
        self.name = name
        self.config = config        # HAS-A relationship — aggregation
        self.status = "inactive"

    def start(self):
        self.status = "running"
        logging.info(f"Pipeline {self.name} started")
        logging.info(f"Using config: {self.config.get_config()}")

    def get_info(self):
        return f"Pipeline: {self.name} | Status: {self.status}"


# ── CLASS 4: DataEngineer ──
# ASSOCIATION — DataEngineer USES-A Pipeline
# Pipeline exists independently, DE just uses it temporarily
class DataEngineer:
    def __init__(self, name, skill_level):
        self.name = name
        self.skill_level = skill_level

    # Association — DE uses pipeline but does not own it
    def run_pipeline(self, pipeline):
        logging.info(f"{self.name} is running pipeline: {pipeline.name}")
        pipeline.start()
        return f"{self.name} executed {pipeline.name} successfully"

    # Association — DE uses DQ checker but does not own it
    def check_data_quality(self, checker, data):
        logging.info(f"{self.name} running DQ checks using {checker.name}")
        null_check = checker.check_nulls(data)
        count_check = checker.check_row_count(data, min_rows=3)
        return null_check and count_check


# ══ MAIN EXECUTION ══

# Create Config independently
config1 = PipelineConfig("S3 Bronze", "S3 Silver", 1000)
print(f"Config created: {config1.get_config()}")

# Create Pipeline with Config — AGGREGATION
pipeline1 = Pipeline("NYC Taxi Transform", config1)
print(pipeline1.get_info())

# Create DataEngineer
engineer = DataEngineer("Vinay", "Junior DE")

# DataEngineer USES Pipeline — ASSOCIATION
result = engineer.run_pipeline(pipeline1)
print(result)

# Create DQ Checker independently
dq_checker = DataQualityChecker("Silver Layer DQ")

# Sample data with one null row
sample_data = [
    {"name": "Vinay", "dept": "DE", "salary": 50000},
    {"name": "Shreya", "dept": "ML", "salary": None},  # null here
    {"name": "Phani", "dept": "DE", "salary": 54000},
]

# DataEngineer USES DQ Checker — ASSOCIATION
quality_passed = engineer.check_data_quality(dq_checker, sample_data)
print(f"Data quality passed: {quality_passed}")

# ── Key demonstration ──
# Config still exists even if we delete pipeline — proves aggregation
del pipeline1
print(f"Pipeline deleted but config still exists: {config1.get_config()}")