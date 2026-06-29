# STRINGS
name = "vinay"
print(name.upper())
print(name.replace("vinay", "data engineer"))
print(f"My name is {name} and I am learning DE")

# LISTS
tools = ["python", "pyspark", "delta lake", "sql"]
tools.append("databricks")
print(tools)
print(tools[0])
tools.remove("sql")
print(tools)

# DICTIONARY
profile = {
    "name": "Vinay",
    "role": "Data Engineer",
    "skills": ["python", "sql", "pyspark"]
}
print(profile["name"])
print(profile["skills"])
profile["experience"] = "1 year"
print(profile)

# FUNCTIONS
def greet_engineer(name, role="Data Engineer"):
    return f"Hello {name}, welcome to {role}"

print(greet_engineer("Vinay"))
print(greet_engineer("Amit", "ML Engineer"))