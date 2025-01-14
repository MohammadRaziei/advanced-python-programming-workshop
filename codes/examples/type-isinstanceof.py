class Parent:
    pass

class Child(Parent):
    pass

# Create objects
obj1 = Parent()
obj2 = Child()
obj3 = Parent()

# Using type
print(type(obj1))  # Output: <class '__main__.Parent'>
print(type(obj2))  # Output: <class '__main__.Child'>

# Comparing types
print(type(obj1) == type(obj2))  # Output: False
print(type(obj1) == type(obj3))  # Output: True

# Using isinstance
print(isinstance(obj1, Parent))  # Output: True
print(isinstance(obj2, Parent))  # Output: True (Child is a subclass of Parent)
print(isinstance(obj1, Child))  # Output: False