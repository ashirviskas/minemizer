# markdown_table

Markdown preset - renders as proper table in markdown viewers

## Input (JSON)

```json
[
  {
    "project": "Phoenix",
    "status": "Active",
    "lead": "Maria Santos"
  },
  {
    "project": "Titan",
    "status": "Planning",
    "lead": "James Okonkwo"
  },
  {
    "project": "Nebula",
    "status": "Complete",
    "lead": "Anika Patel"
  }
]
```

## Options

```python
minemize(data, preset=presets.markdown)
```

## Output

### Raw

```
|project| status| lead|
|---| ---| ---|
|Phoenix| Active| Maria Santos|
|Titan| Planning| James Okonkwo|
|Nebula| Complete| Anika Patel|
```

### Rendered

|project| status| lead|
|---| ---| ---|
|Phoenix| Active| Maria Santos|
|Titan| Planning| James Okonkwo|
|Nebula| Complete| Anika Patel|
