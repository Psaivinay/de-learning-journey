import sys
sys.path.insert(0,'.')


class DataPipeline:
    total_pipelines=0
    
    
    def __init__(self,name,source,destination):
        self.name=name
        self.source=source
        self.destination=destination
        self.status="not started"
        DataPipeline.total_pipelines+=1
        
    def start(self):
        self.status="running"
        print(f"Pipeline {self.name} started {self.source} -> {self.destination}")
    
    def complete(self):
        self.status="completed"
        print(f"Pipeline {self.name} completed successfully")
    
    def get_info(self):
        return f"{self.name} | Status:{self.status} | {self.source}-> {self.destination}"
    
    
pipeline1=DataPipeline("NYC Taxi Ingestion","API","S3 Bronze")
pipeline2=DataPipeline("Weather Data Load","OpenWeatherMap","S3 Bronze")
pipeline3=DataPipeline("Silver Transform","S3 Bronze","S3 Silver")

pipeline1.start()
pipeline1.complete()
        

print(pipeline1.get_info())
print(pipeline2.get_info())
print(pipeline3.get_info())

print(f"Total pipelines created: {DataPipeline.total_pipelines}")
