# nested

Nested structures - dicts and lists within items

## Input (JSON)

```json
[
  {
    "id": "u1",
    "name": "Lukas",
    "location": {
      "office": "Kaunas HQ",
      "floor": 12
    },
    "skills": [
      "python",
      "kubernetes"
    ]
  },
  {
    "id": "u2",
    "name": "Emma",
    "location": {
      "office": "Boston Hub",
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
    "name": "Pierre",
    "location": {
      "office": "Paris Office",
      "floor": 3
    },
    "skills": [
      "rust"
    ]
  },
  {
    "id": "u4",
    "name": "Hana",
    "location": {
      "office": "Tokyo Tower",
      "floor": 15
    },
    "skills": [
      "go",
      "docker"
    ]
  },
  {
    "id": "u5",
    "name": "Wei",
    "location": {
      "office": "Taipei Center",
      "floor": 8
    },
    "skills": [
      "java",
      "spring"
    ]
  },
  {
    "id": "u6",
    "name": "Charlotte",
    "location": {
      "office": "London Bridge",
      "floor": 5
    },
    "skills": [
      "python",
      "django"
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
u1; Lukas; { Kaunas HQ; 12}; [ python; kubernetes]
u2; Emma; { Boston Hub; 7}; [ react; typescript; graphql]
u3; Pierre; { Paris Office; 3}; [ rust]
u4; Hana; { Tokyo Tower; 15}; [ go; docker]
u5; Wei; { Taipei Center; 8}; [ java; spring]
u6; Charlotte; { London Bridge; 5}; [ python; django]
```
