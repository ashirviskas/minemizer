# nested

Nested structures - dicts and lists within items

## Input (JSON)

```json
[
  {
    "id": "u1",
    "name": "Chen Wei",
    "location": {
      "office": "Shanghai HQ",
      "floor": 12
    },
    "skills": [
      "python",
      "kubernetes"
    ]
  },
  {
    "id": "u2",
    "name": "Fatima Al-Rashid",
    "location": {
      "office": "Dubai Tech Park",
      "floor": 7
    },
    "skills": [
      "react",
      "typescript",
      "graphql"
    ]
  },
  {
    "id": "u3",
    "name": "Oluwaseun Adeyemi",
    "location": {
      "office": "Lagos Hub",
      "floor": 3
    },
    "skills": [
      "rust"
    ]
  }
]
```

## Options

```python
minemize(data)
```

## Output

```
id; name; location{ office; floor}; skills[]
u1; Chen Wei; { Shanghai HQ; 12}; [ python; kubernetes]
u2; Fatima Al-Rashid; { Dubai Tech Park; 7}; [ react; typescript; graphql]
u3; Oluwaseun Adeyemi; { Lagos Hub; 3}; [ rust]
```
