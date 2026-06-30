double =lambda x:x*2

add=lambda x,y:x+y

names=['Vinay','Sai','Punnamaraju']
sorted_names=sorted(names,key=lambda x:len(x))

numbers=[1,2,3,4,5,5,6]
evens=list(filter(lambda x:x%2==0,numbers))

print(double(5))
print(add(2,3))
print(sorted_names)
print(evens)    