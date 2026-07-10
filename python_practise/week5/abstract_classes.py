import sys
sys.path.insert(0,'.')
import logging

from abc import ABC,abstractmethod


logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s -%(message)s')

class DataSource(ABC):
    def __init__(self,name,connection_string):
        self.name=name
        self.connection_string=connection_string
        self.is_connected=False
        
    @abstractmethod
    def connect(self):
        pass
        
    @abstractmethod
    def extract(self):
        pass
    
    @abstractmethod
    def validate_connection(self):
        pass
    
    def disconnect(self):
        self.is_connected=False
        logging.info(f"{self.name}: Disconnected")
        
    def get_status(self):
        status="connected" if self.is_connected else "disconnected"
        return f"{self.name} | Status: {status}"
    
    
class S3DataSource(DataSource):
    
    def __init__(self,name,connection_string,bucket,prefix):
        super().__init__(name,connection_string)
        self.bucket=bucket
        self.prefix=prefix
        
    def connect(self):
        logging.info(f"S3: Connecting to bucket {self.bucket}")
        self.is_connected=True
        logging.info(f"S3: Connected successfully")
        
    def extract(self):
        if not self.is_connected:
            raise ConnectionError("Must connect before extracting")
        logging.info(f"S3:Extracting files from S3://{self.bucket}/{self.prefix}")
        return [
            {"trip_id":1,"distance":5.2,"fare":15.0},
            {"trip_id":2,"distance":3.1,"fare":10.5},
            {"trip_id":3,"distance":8.4,"fare":25.0}
        ]
    
    def validate_connection(self):
        if self.bucket and self.prefix:
            logging.info(f"S3: Connection valid — bucket and prefix set")
            return True
        logging.error(f"S3: Invalid connection — missing bucket or prefix")
        return False
    
    

# ── CHILD 2: APIDataSource ──
class APIDataSource(DataSource):
    
    def __init__(self, name, connection_string, api_key, endpoint):
        super().__init__(name, connection_string)
        self.api_key = api_key
        self.endpoint = endpoint
    
    def connect(self):
        logging.info(f"API: Connecting to {self.endpoint}")
        self.is_connected = True
        logging.info(f"API: Connected successfully")
    
    def extract(self):
        if not self.is_connected:
            raise ConnectionError("Must connect before extracting")
        logging.info(f"API: Fetching data from {self.endpoint}")
        return [
            {"city": "Mysore", "temp": 28.5, "humidity": 65},
            {"city": "Bangalore", "temp": 24.0, "humidity": 70},
        ]
    
    def validate_connection(self):
        if self.api_key and self.endpoint:
            logging.info(f"API: Connection valid — key and endpoint set")
            return True
        logging.error(f"API: Invalid — missing api_key or endpoint")
        return False
    

# ── CHILD 3: DatabaseDataSource ──
class DatabaseDataSource(DataSource):
    
    def __init__(self, name, connection_string, db_name, table):
        super().__init__(name, connection_string)
        self.db_name = db_name
        self.table = table
    
    def connect(self):
        logging.info(f"DB: Connecting to {self.db_name}")
        self.is_connected = True
        logging.info(f"DB: Connected successfully")
    
    def extract(self):
        if not self.is_connected:
            raise ConnectionError("Must connect before extracting")
        logging.info(f"DB: Running SELECT * FROM {self.table}")
        return [
            {"emp_id": 1, "name": "Vinay", "dept": "DE"},
            {"emp_id": 2, "name": "Shreya", "dept": "ML"},
        ]
    
    def validate_connection(self):
        if self.db_name and self.table:
            logging.info(f"DB: Connection valid")
            return True
        logging.error(f"DB: Invalid — missing db_name or table")
        return False

print("=" * 60)
print("ABSTRACT CLASS DEMO — MULTIPLE DATA SOURCES")
print("=" * 60)

# Create all 3 sources
s3_source = S3DataSource(
    "NYC Taxi S3", "aws://us-east-1",
    bucket="nyc-taxi-raw", prefix="2025/01/"
)

api_source = APIDataSource(
    "Weather API", "https://api.openweathermap.org",
    api_key="abc123key", endpoint="/data/2.5/weather"
)

db_source = DatabaseDataSource(
    "Employee DB", "postgresql://localhost:5432",
    db_name="hr_database", table="employees"
)

# Process all sources the same way
# This is POLYMORPHISM — same code works for all 3 different sources
sources = [s3_source, api_source, db_source]

for source in sources:
    print(f"\nProcessing: {source.name}")
    source.validate_connection()
    source.connect()
    data = source.extract()
    print(f"Extracted {len(data)} records")
    print(source.get_status())
    source.disconnect()

print("\n" + "=" * 60)

# ── Prove you cannot instantiate abstract class directly ──
print("Trying to create DataSource directly:")
try:
    base = DataSource("test", "test://connection")
except TypeError as e:
    logging.error(f"Cannot instantiate abstract class: {e}")