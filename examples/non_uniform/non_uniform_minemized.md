# non_uniform

Sparse keys - some fields only present in some items

## Input (JSON)

```json
[
  {
    "id": 1,
    "name": "Erik",
    "department": "Engineering"
  },
  {
    "id": 2,
    "name": "Rachel",
    "department": "Design",
    "remote": true
  },
  {
    "id": 3,
    "name": "Hans"
  },
  {
    "id": 4,
    "name": "Kenji",
    "department": "Sales",
    "slack": "@kenji"
  },
  {
    "id": 5,
    "name": "Mai",
    "remote": true
  },
  {
    "id": 6,
    "name": "Tom",
    "department": "Engineering"
  }
]
```

## Options

```python
minemize(data, sparsity_threshold=0.5)
```

## Output

```
id; name; department
1; Erik; Engineering
2; Rachel; Design; remote:True
3; Hans; 
4; Kenji; Sales; slack:@kenji
5; Mai; ; remote:True
6; Tom; Engineering
```
