import logging 
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('pipeline.org'),
                        logging.StreamHandler()
                    ]
)

employees=[
    {'name':'Vinay','dept':'DE','salary':500000},
    {'name': 'Shreya', 'dept': 'ML', 'salary': 60000},
    {'name': 'Phani', 'dept': 'DE', 'salary': 54000},
    {'name': 'Priyaa', 'dept': 'DE', 'salary': 90000},
    {'name': 'Ravi', 'dept': 'BI', 'salary': None},  #bad data
]

def write_employees(data,filename):
    logging.info(f"Starting write operation to {filename}")
    try:
        with open(filename,'w') as f:
            for emp in data:
                f.write(f"{emp['name']},{emp['dept']},{emp['salary']}")
        logging.info(f"Successfully wrote {len(data)} records to {filename}")
    except Exception as e:
        logging.error(f"Failed to write file:{e}")
        
def read_employees(filename):
    logging.info(f"Reading file:{filename}")
    try:
        with open(filename,'r') as f:
            lines=f.readlines()
        logging.info(f"Successfully read {len(lines)} lines")
        return lines
    except FileNotFoundError:
        logging.error(f"File not found:{filename}")
        return []
    
def filter_departments(data,dept):
    logging.debug(f"Filtering for department:{dept}")
    filtered=[emp for emp in data if emp['dept']==dept]
    logging.info(f"Found {len(filtered)} employees in {dept} department")
    return filtered

def validate_salary(emp):
    if emp['salary'] is None:
        logging.warning(f"Missing salary for {emp['name']} — skipping")
        return False
    if emp['salary'] < 0:
        logging.warning(f"Invalid salary for {emp['name']} — skipping")
        return False
    return True

logging.info("Pipeline Started")

valid_employees=[emp for emp in employees if validate_salary(emp)]
logging.info(f"Valid records:{len(valid_employees)} out of {len(employees)}")


write_employees(valid_employees,'employees.txt')

lines=read_employees('employees.txt')

de_only=filter_departments(valid_employees,'DE')

write_employees(de_only, 'de_employees.txt')

logging.info("Pipeline finished successfully")