import sys
sys.path.insert(0,'.')
import logging
from abc import ABC,abstractmethod

logging.basicConfig(level=logging.INFO,format="%(asctime)s -%(levelname)s -%(message)s")

#Base Exception -parent of all pipeline exceptions:

class PipelineError(Exception):
    def __init__(self,message,pipeline_name):
        super().__init__(message)
        self.pipeline_name=pipeline_name
        self.message=message
        
    def __str__(self):
        return f"[{self.pipeline_name}] {self.message}"
    
#Specific exceptions -children of PipelineError

class ConnectionError(PipelineError):
    def __init__(self,pipeline_name,source):
        super().__init__(
            f"Failed to connect to source:{source}",
            pipeline_name
        )
        self.source=source

class ValidationError(PipelineError):
    def __init__(self, pipeline_name,field,reason):
        super().__init__(
            f"Validation failed on field '{field}' : {reason}"
            , pipeline_name
            )
        self.field=field
        self.reason=reason
        
class DataQualityError(PipelineError):
    def __init__(self, pipeline_name,failed_rows,total_rows):
        super().__init__(
            f"DQ failed:{failed_rows}/{total_rows} rows failed checks",
            pipeline_name
            )
        self.failed_rows=failed_rows
        self.total_rows=total_rows
        
class TransformError(PipelineError):
    def __init__(self,pipeline_name,step,reason):
        super().__init__(
            f"Tranform failed at step'{step}': {reason}",
            pipeline_name
        )
        self.step=step
        
class SilverPipeline:
    def __init__(self,name,source,destination):
        self.name=name
        self.source=source
        self.destination=destination
        self.is_connected=False
        
    def connect(self,should_fail=False):
        logging.info(f"Connecting to {self.source}")
        if should_fail:
            raise ConnectionError(self.name,self.source)
        self.is_connected=True
        logging.info("Connected successfully")
        
    def validate_config(self,config):
        logging.info("Validating pipeline config")
        if not  config.get("batch_size"):
            raise ValidationError(
                self.name,
                field="batch_size",
                reason="batch_size is required but missing"
            )
        if config["batch_size"]<=0:
            raise ValidationError(
                self.name,
                field="batch_size",
                reason="batch_size must be greater than 0"
            )
        logging.info("Config validation passed")
        
    def check_data_quality(self,data):
        logging.info(f"Running DQ checks on {len(data)} records")
        failed=[row for row in data if None in row.values()]
        if len(failed)>len(data)*0.1:
            raise DataQualityError(
                self.name,
                failed_rows=len(failed),
                total_rows=len(data)
            )
        logging.info(f"DQ passed - {len(failed)} failed rows within threshold")
        
    def transform(self,data,should_fail=False):
        logging.info("Running Silver transformations")
        if should_fail:
            raise TransformError(
                self.name,
                step="type_casting",
                reason="Cannot cast string 'abc' to integer "
            )
        transformed= []
        for row in data:
            if None not in row.values():
                transformed.append({
                    k:v for k,v in row.items()
                })
        logging.info(f"Transformed {len(transformed)} records")
        return transformed
    
pipeline=SilverPipeline(
    "NYC Taxi Silver",
    "Delta://bronze/nyc_taxi",
    "Delta://silver/nyc_taxi"
)

sample_data=[
    {"trip_id":1,"distance":5.2,"fare":15.0},
    {"trip_id":2,"distance":None,"fare":10.5},
    {"trip_id":3,"distance":8.4,"fare":25.0},
    {"trip_id":4,"distance":3.1,"fare":None},
    {"trip_id":5,"distance":6.0,"fare":18.0},
]

print("="*60)
print("TEST 1: Connection failure")
print("="*60)

try:
    pipeline.connect(should_fail=True)
except ConnectionError as e:
    logging.error(f"ConnectionError caught:{e}")
    
print("\n" + "=" * 60)
print("TEST 2: Validation failure")
print("=" * 60)

try:
    bad_config={"batch_size":-100}
    pipeline.validate_config(bad_config)
except ValidationError as e:
    logging.error(f"ValidationError caught :{e}")
    logging.error(f"Failed field: {e.field}")
    
    
print("\n" + "=" * 60)
print("TEST 3: Data quality failure")
print("=" * 60)

try:
    bad_data=[
        {"trip_id":1,"distance":None,"fare":None},
        {"trip_id":2,"distance":None,"fare":None},
        {"trip_id":3,"distance":None,"fare":None},
        {"trip_id":4,"distance":5.0,"fare":15.0},
        {"trip_id":5,"distance":6.0,"fare":18.0},
    ]
    pipeline.check_data_quality(bad_data)
except DataQualityError as e:
    logging.error(f"DataQualityError:{e}")
    logging.error(f"Failed: {e.failed_rows} rows out of {e.total_rows}")
    
print("\n" + "=" * 60)
print("TEST 4: Transform failure")
print("=" * 60)
try:
    pipeline.connect()
    pipeline.transform(sample_data, should_fail=True)
except TransformError as e:
    logging.error(f"TransformError caught: {e}")
    logging.error(f"Failed step: {e.step}")


print("\n" + "=" * 60)
print("TEST 5: Catch ALL pipeline errors with base exception")
print("=" * 60)
try:
    pipeline.connect(should_fail=True)
except PipelineError as e:
    logging.error(f"PipelineError caught: {e}")
    logging.error(f"Pipeline name: {e.pipeline_name}")

print("\n" + "=" * 60)
print("TEST 6: Full happy path — no errors")
print("=" * 60)
try:
    good_config = {"batch_size": 1000}
    pipeline.validate_config(good_config)
    pipeline.check_data_quality(sample_data)
    result = pipeline.transform(sample_data)
    print(f"Pipeline completed successfully — {len(result)} records")
except PipelineError as e:
    logging.error(f"Pipeline failed: {e}")