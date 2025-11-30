# uniform

All keys present in all items - clean tabular data (default preset)

## Input (JSON)

```json
[
  {
    "id": 101,
    "name": "Marta",
    "age": 29,
    "city": "Vilnius"
  },
  {
    "id": 102,
    "name": "James",
    "age": 34,
    "city": "Austin"
  },
  {
    "id": 103,
    "name": "Sophie",
    "age": 27,
    "city": "Lyon"
  },
  {
    "id": 104,
    "name": "Yuki",
    "age": 31,
    "city": "Osaka"
  },
  {
    "id": 105,
    "name": "Lin",
    "age": 28,
    "city": "Singapore"
  },
  {
    "id": 106,
    "name": "Oliver",
    "age": 35,
    "city": "Bristol"
  }
]
```

## Options

```python
minemize(data, preset=presets.default)
```

## Output

```
id; name; age; city
101; Marta; 29; Vilnius
102; James; 34; Austin
103; Sophie; 27; Lyon
104; Yuki; 31; Osaka
105; Lin; 28; Singapore
106; Oliver; 35; Bristol
```
