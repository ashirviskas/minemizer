# uniform

All keys present in all items - clean tabular data (default preset)

## Input (JSON)

```json
[
  {
    "id": 101,
    "name": "Yuki Tanaka",
    "age": 29,
    "city": "Tokyo"
  },
  {
    "id": 102,
    "name": "Priya Sharma",
    "age": 34,
    "city": "Mumbai"
  },
  {
    "id": 103,
    "name": "Lucas Silva",
    "age": 27,
    "city": "S\u00e3o Paulo"
  },
  {
    "id": 104,
    "name": "Emma Nielsen",
    "age": 31,
    "city": "Copenhagen"
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
101; Yuki Tanaka; 29; Tokyo
102; Priya Sharma; 34; Mumbai
103; Lucas Silva; 27; São Paulo
104; Emma Nielsen; 31; Copenhagen
```
