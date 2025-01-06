from typing import Dict, List, Union, Optional

class Employee:
  def __init__(self, name: str, age: int, skills: List[str],
        details: Optional[Dict[str, Union[str, int]]] = None):
    self.name: str = name
    self.age: int = age
    self.skills: List[str] = skills
    self.details: Optional[Dict[str, Union[str, int]]] = details

# Example usage
employee = Employee(
  name="John Doe",
  age=30,
  skills=["Python", "Data Analysis"],
  details={"department": "IT", "years_experience": 5}
)