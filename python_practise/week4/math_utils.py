def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def calculate_bonus(salary, percentage=10):
    return salary * (percentage / 100)

if __name__ == '__main__':
    print("Testing math_utils directly...")
    print(add(2, 3))
    print(calculate_bonus(50000))