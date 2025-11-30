# markdown_table

Markdown preset - renders as proper table in markdown viewers

## Input (JSON)

```json
[
  {
    "project": "Phoenix",
    "status": "Active",
    "lead": "Jonas"
  },
  {
    "project": "Titan",
    "status": "Planning",
    "lead": "Sarah"
  },
  {
    "project": "Nebula",
    "status": "Complete",
    "lead": "Akira"
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
|Phoenix| Active| Jonas|
|Titan| Planning| Sarah|
|Nebula| Complete| Akira|
```

### Rendered

|project| status| lead|
|---| ---| ---|
|Phoenix| Active| Jonas|
|Titan| Planning| Sarah|
|Nebula| Complete| Akira|
