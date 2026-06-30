with open('test_output.txt','w') as f:
    f.write("Testing context manager\n")
    f.write("This file will auto-close")
    
print("File written and closed automatically")

with open('test_output.txt','r') as f:
    content=f.read()
    print(content)  