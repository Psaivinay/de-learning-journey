import sys
sys.path.insert(0, '.')
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s- %(levelname)s - %(message)s')

class BasePipeline:
    def __init__(self,name,source,destination):
        self.name=name
        self.source=source
        self.destination=destination
        self.status="inactive"
        self.records_processed=0
    def connect(self):
        logging.info(f"Connecting to sorce{self.source}")
        return True
    
    def run(self):
        logging.info(f"BasePipeline {self.name} running")
        self.status="running"
        
    def complete(self):
        self.status="completed"
        logging.info(f"Pipeline{self.name} completed-"
                    f"{self.records_processed} records processed")
        
    def get_info(self):
        return (f"Pipeline: {self.name} | "
                f"Source: {self.source} | "
                f"Destination: {self.destination} | "
                f"Status: {self.status} | "
                f"Records: {self.records_processed}")
        
        
# ── CHILD CLASS 1: BronzePipeline ──
# Inherits BasePipeline — adds raw ingestion specific behaviour

class BronzePipeline(BasePipeline):
    def __init__(self,name,source,destination,file_format):
        super().__init__(name,source,destination)
        self.file_format=file_format
        
    def run(self):
        super().run()
        logging.info(f"Bronze layer :ingesting raw{self.file_format}files")
        self.records_processed=10000
        logging.info(f"Raw data landed to {self.destination}")
        
    def get_info(self):
        base_info = super().get_info()   # get parent info
        return f"{base_info} | Format: {self.file_format}"
    
# ── CHILD CLASS 2: SilverPipeline ──
# Inherits BasePipeline — adds cleaning and SCD2 behaviour

class SilverPipeline(BasePipeline):
    
    def __init__(self, name, source, destination, dq_rules):
        super().__init__(name, source, destination)
        self.dq_rules = dq_rules        # extra attribute
        self.failed_records = 0
    
    # Method overriding — Silver specific run
    def run(self):
        super().run()
        logging.info(f"Silver layer: applying {len(self.dq_rules)} DQ rules")
        for rule in self.dq_rules:
            logging.info(f"Applying rule: {rule}")
        self.records_processed = 9500
        self.failed_records = 500
        logging.info(f"Cleaned data written to {self.destination}")
    
    def get_info(self):
        base_info = super().get_info()
        return (f"{base_info} | "
                f"Failed records: {self.failed_records} | "
                f"DQ rules: {self.dq_rules}")

# ── CHILD CLASS 3: GoldPipeline ──
# Inherits BasePipeline — adds aggregation behaviour
class GoldPipeline(BasePipeline):
    
    def __init__(self, name, source, destination, kpis):
        super().__init__(name, source, destination)
        self.kpis = kpis                # list of KPIs to calculate
    
    # Method overriding — Gold specific run
    def run(self):
        super().run()
        logging.info(f"Gold layer: calculating {len(self.kpis)} KPIs")
        for kpi in self.kpis:
            logging.info(f"Computing KPI: {kpi}")
        self.records_processed = 100
        logging.info(f"Gold KPI table written to {self.destination}")
    
    def get_info(self):
        base_info = super().get_info()
        return f"{base_info} | KPIs: {self.kpis}"


# Bronze layer pipeline
bronze = BronzePipeline(
    name="NYC Taxi Bronze",
    source="S3://raw/nyc-taxi",
    destination="Delta://bronze/nyc_taxi",
    file_format="CSV"
)
bronze.connect()
bronze.run()
bronze.complete()
print(bronze.get_info())

print("-" * 60)

# Silver layer pipeline
silver = SilverPipeline(
    name="NYC Taxi Silver",
    source="Delta://bronze/nyc_taxi",
    destination="Delta://silver/nyc_taxi",
    dq_rules=["no_nulls_in_id", "trip_duration_positive", "valid_pickup_date"]
)
silver.connect()
silver.run()
silver.complete()
print(silver.get_info())

print("-" * 60)

# Gold layer pipeline
gold = GoldPipeline(
    name="NYC Taxi Gold",
    source="Delta://silver/nyc_taxi",
    destination="Delta://gold/daily_kpis",
    kpis=["daily_revenue", "avg_trip_duration", "total_trips"]
)
gold.connect()
gold.run()
gold.complete()
print(gold.get_info())

print("-" * 60)

# ── Prove inheritance ──
print("\nProving inheritance:")
print(f"Bronze IS-A BasePipeline: {isinstance(bronze, BasePipeline)}")
print(f"Silver IS-A BasePipeline: {isinstance(silver, BasePipeline)}")
print(f"Gold IS-A BasePipeline: {isinstance(gold, BasePipeline)}")