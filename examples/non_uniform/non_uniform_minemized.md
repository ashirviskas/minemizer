# non_uniform

Sparse keys - some fields only present in some items

## Input (JSON)

```json
[
  {
    "id": 1,
    "name": "Kenji Watanabe",
    "department": "Engineering"
  },
  {
    "id": 2,
    "name": "Sofia Rodriguez",
    "department": "Design",
    "remote": true
  },
  {
    "id": 3,
    "name": "Ahmed Hassan"
  },
  {
    "id": 4,
    "name": "Ingrid Larsson",
    "department": "Sales",
    "slack": "@ingrid"
  }
]
```

## Options

```python
minemize(data, threshold=0.5)
```

## Output

```
id; name; department
1; Kenji Watanabe; Engineering
2; Sofia Rodriguez; Design; remote:True
3; Ahmed Hassan; 
4; Ingrid Larsson; Sales; slack:@ingrid
```
