# csv_style

CSV preset - standard comma-separated values

## Input (JSON)

```json
[
  {
    "sku": "KB-2847",
    "item": "Mechanical Keyboard",
    "price": 149.99,
    "stock": 45
  },
  {
    "sku": "MS-1122",
    "item": "Ergonomic Mouse",
    "price": 79.5,
    "stock": 120
  },
  {
    "sku": "HC-9931",
    "item": "USB-C Hub 7-port",
    "price": 59.99,
    "stock": 67
  }
]
```

## Options

```python
minemize(data, preset=presets.csv)
```

## Output

```
sku,item,price,stock
KB-2847,Mechanical Keyboard,149.99,45
MS-1122,Ergonomic Mouse,79.5,120
HC-9931,USB-C Hub 7-port,59.99,67
```
