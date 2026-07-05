import sys
sys.path.insert(0, '.')

class DataEngineer:
    
    # Class variable
    team = "Data Engineering"
    
    def __init__(self, name, experience_years, skills):
        self.name = name
        self.experience_years = experience_years
        self.skills = skills
    
    # Regular method — knows about instance (self)
    def introduce(self):
        return f"I am {self.name}, {self.experience_years} years exp, skills: {self.skills}"
    
    # @classmethod — alternative constructor
    # Creates object from a string instead of separate parameters
    @classmethod
    def from_string(cls, engineer_string):
        # engineer_string format: "Vinay-2-Python,PySpark,SQL"
        name, exp, skills = engineer_string.split('-')
        return cls(name, int(exp), skills)
    
    # @classmethod — knows about class variable
    @classmethod
    def get_team(cls):
        return f"Team: {cls.team}"
    
    # @staticmethod — utility function, no self or cls needed
    # Just checks if experience is junior or senior
    @staticmethod
    def check_level(experience_years):
        if experience_years < 2:
            return "Junior"
        elif experience_years < 5:
            return "Mid-level"
        else:
            return "Senior"

# ── Regular way to create object ──
eng1 = DataEngineer("Vinay", 1, "Python,SQL,PySpark")
print(eng1.introduce())

# ── @classmethod — create object from a string ──
eng2 = DataEngineer.from_string("Shreya-3-Python,dbt,Snowflake")
print(eng2.introduce())

# ── @classmethod — access class variable ──
print(DataEngineer.get_team())

# ── @staticmethod — utility, called on class directly ──
print(DataEngineer.check_level(1))
print(DataEngineer.check_level(3))
print(DataEngineer.check_level(6))

# ── Key point: staticmethod does not need an object ──
# You can call it without creating any instance
print(DataEngineer.check_level(eng1.experience_years))