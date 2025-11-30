# minemizer
Minimize your stuff

## Using minemizer

```python
from minemizer import minemize

some_data_simple = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35},
]
minemized_string_simple = minemize(some_data_simple)
print(minemized_string_simple)

# Prints
#  id; age; name
#  1; 30; Alice
#  2; 25; Bob
#  3; 35; Charlie

some_data_nested = [
    {"id": 1, "name": "Alice", "address": {"street": "123 Main St", "city": "Boston"}},
    {"id": 2, "name": "Bob", "address": {"street": "456 Oak Ave", "city": "NYC"}},
]

minemized_string_nested = minemize(some_data_nested)
print(minemized_string_nested)
# Prints
#  id; name; address{ city; street}
#  1; Alice; { Boston; 123 Main St}
#  2; Bob; { NYC; 456 Oak Ave}

```

## Installation