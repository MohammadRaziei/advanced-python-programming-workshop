class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# Class using the Singleton metaclass
class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value

# Test
obj1 = Singleton(42)
obj2 = Singleton(99)
print(obj1 is obj2)  # Output: True (both are the same instance)
print(obj1.value)    # Output: 99 (shared instance updated)