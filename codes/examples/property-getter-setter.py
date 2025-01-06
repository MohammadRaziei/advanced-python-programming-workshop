class Circle:
    def __init__(self, radius: float):
        self._radius = radius  # Private attribute
    @property
    def radius(self):
        """Getter for radius."""
        return self._radius
    @radius.setter
    def radius(self, value: float):
        """Setter for radius."""
        if value < 0:
            raise ValueError("Radius cannot be negative!")
        self._radius = value
    @property
    def area(self):
        """Computed property."""
        return 3.14159 * self._radius**2
# Usage
circle = Circle(5)
print(circle.radius)  # Access the radius (Getter)
circle.radius = 10    # Update the radius (Setter)
print(circle.area)    # Compute t   he area (Read-only property)
circle.radius = -3    # Raises ValueError