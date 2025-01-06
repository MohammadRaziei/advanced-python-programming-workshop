def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        func(*args, **kwargs)
        print("After function call")
    return wrapper

def greet(name: str):
    print("Hello", name)
greet = my_decorator(greet)

greet("Mohammad")
# Output:
# Before function call
# Hello Mohammad
# After function call

@my_decorator
def greet(name: str):
    print("Hello", name)

greet("Mohammad")
# Output:
# Before function call
# Hello Mohammad
# After function call