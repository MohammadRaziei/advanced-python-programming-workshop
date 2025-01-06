class MyClass:
    class_variable = 0

    @classmethod  # Decorator for class-level methods
    def increment_class_var(cls):
        cls.class_variable += 1
        print(f"Class variable: {cls.class_variable}")

    @staticmethod  # Decorator for utility methods
    def greet(message: str):
        print(f"Static Method says: {message}")

# Usage
MyClass.increment_class_var()  # Updates and prints class_variable
MyClass.greet("Hello!")        # Prints: Static Method says: Hello!