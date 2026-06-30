employees=[
    {'name':'Vinay','dept':'DE','salary':50000},
    {'name':'Shreya','dept':'ML','salary':60000},
    {'name':'Phani','dept':'DE','salary':54000},
    {'name':'Priyaa','dept':'DE','salary':90000}
]

with open('employees.txt','w') as f:
    for emp in employees:
        f.write(f"{emp['name']},{emp['dept']},{emp['salary']}\n")
        
print("Written employees.txt")

with open('employees.txt','r') as f:
    for line in f:
        print(line.strip())
        
de_employees=[emp for emp in employees if emp['dept']=='DE']

with open('de_employees.txt','w') as f:
    for emp in de_employees:
        f.write(f"{emp['name']},{emp['dept']},{emp['salary']}\n")
        
print(f"Written {len(de_employees)} records to de_employees.txt")