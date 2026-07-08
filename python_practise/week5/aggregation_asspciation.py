import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s -%(message)s')

# ── ASSOCIATION example: Driver and Car interact, no stored link ──

class Driver:
    def __init__(self,name,license_number):
        self.name=name
        self.license_number=license_number
        
class Car:
    def __init__(self,model):
        self.model=model
        
def drive(driver,car):
    logging.info(f"{driver.name} (License:{driver.license_number}) is driving {car.model}")
    
    
# ── AGGREGATION example: DataPipeline HAS-A list of DataSource objects ──

class DataSource:
    def __init__(self,name,source_type):
        self.name=name
        self.source_type=source_type
    def get_info(self):
        return f"{self.name}({self.source_type})"
    
class DataPipeline:
    def __init__(self,pipeline_name):
        self.pipeline_name=pipeline_name
        self.sources=[]
    def add_source(self,source):
        self.sources.append(source)
        logging.info(f"Added source {source.name} to pipeline {self.pipeline_name}")
        
    def list_sources(self):
        for src in self.sources:
            print(f"-{src.get_info()}")
            
# ── Test 1: Association ──
driver1 = Driver("Vinay", "DL1234")
car1 = Car("Swift")
drive(driver1, car1)

# ── Test 2: Aggregation ──
s3_source = DataSource("RawSalesData", "S3")
kafka_source = DataSource("ClickStream", "Kafka")


pipeline = DataPipeline("ETL_Pipeline_1")
pipeline.add_source(s3_source)
pipeline.add_source(kafka_source)

print(f"\nSources in {pipeline.pipeline_name}:")
pipeline.list_sources()

# ── Test 3: Prove independence — delete pipeline, sources still exist ──
del pipeline
print(f"\nAfter deleting pipeline, source still exists: {s3_source.get_info()}")

# ── Test 4: Same DataSource reused in another pipeline (aggregation in action) ──
pipeline2 = DataPipeline("ETL_Pipeline_2")
pipeline2.add_source(s3_source)   # reusing the SAME object — not a copy
pipeline2.list_sources()