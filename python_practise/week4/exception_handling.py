import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
employees = [
    {'name': 'Vinay', 'dept': 'DE', 'salary': 50000},
    {'name': 'Shreya', 'dept': 'ML', 'salary': 60000},
    {'name': 'Phani', 'dept': 'DE', 'salary': 54000},
]

def read_file_safely(filename):
    try:
        with open(filename,'r') as f:
            content=f.read()
            return content
    except FileNotFoundError:
        logging.error(f"File {filename} not  found")
        return None
    finally:
        logging.info("File read attempt finished")

result=read_file_safely('does_not_exist.txt')
print("Result:",result)

def calculate_bonus(salary):
    try:
        bonus = float(salary) * 0.1
        return bonus
    except ValueError:
        logging.error(f"Cannot calculate bonus for invalid salary: {salary}")
        return 0

print(calculate_bonus(50000))      
print(calculate_bonus("abc"))  

class InvalidDepartmentError(Exception):
    pass

def validate_department(dept):
    valid_depts=['DE','ML','BI']
    if dept not in valid_depts:
        raise InvalidDepartmentError(f"{dept} is not a valid department")
    return True

try:
    validate_department('DE')
    print('DE is valid')
    validate_department('AI')
except InvalidDepartmentError as e:
    logging.error(f"Validation failed:{e}")