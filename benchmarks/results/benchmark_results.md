# Benchmark Results (Full Detail)

_Generated: 2025-12-01_

Tokenizers: gpt2, llama, qwen2.5, phi4

## simple_flat.json

Original size (JSON pretty): **763 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 763 | 384 | 334 | 264 | 264 | 311.5 | 2.4 |
| JSON (min) | 522 | 152 | 165 | 137 | 137 | 147.8 | 5.2 |
| CSV | 234 | 95 | 101 | 77 | 77 | 87.5 | 8.7 |
| TSV | 234 | 95 | 101 | 77 | 77 | 87.5 | 8.7 |
| YAML | 489 | 163 | 180 | 169 | 169 | 170.2 | 4.5 |
| TOON | 246 | 98 | 103 | 96 | 96 | 98.2 | 7.8 |
| TSON | 229 | 90 | 95 | 80 | 80 | 86.2 | 8.8 |
| minemizer | 251 | 74 | 83 | 72 | 72 | 75.2 | 10.1 |
| minemizer (compact) | 224 | 85 | 91 | 77 | 77 | 82.5 | 9.2 |

### Serialized outputs

**JSON (pretty)** (763 chars, 312 tokens):
```json
[
  {
    "id": 1,
    "name": "Alice",
    "role": "Engineer",
    "department": "Backend"
  },
  {
    "id": 2,
    "name": "Bob",
    "role": "Designer",
    "department": "Frontend"
  },
  {
    "id": 3,
    "name": "Carol",
    "role": "Manager",
    "department": "Product"
  },
  {
    "id": 4,
    "name": "David",
    "role": "Engineer",
    "department": "Infrastructure"
  },
... (truncated)
```

**JSON (min)** (522 chars, 148 tokens):
```json
[{"id":1,"name":"Alice","role":"Engineer","department":"Backend"},{"id":2,"name":"Bob","role":"Designer","department":"Frontend"},{"id":3,"name":"Carol","role":"Manager","department":"Product"},{"id":4,"name":"David","role":"Engineer","department":"Infrastructure"},{"id":5,"name":"Eva","role":"Analyst","department":"Data"},{"id":6,"name":"Frank","role":"Engineer","department":"Backend"},{"id":7,"name":"Grace","role":"Designer","department":"Mobile"},{"id":8,"name":"Henry","role":"Manager","department":"Engineering"}]
```

**CSV** (234 chars, 88 tokens):
```csv
id,name,role,department
1,Alice,Engineer,Backend
2,Bob,Designer,Frontend
3,Carol,Manager,Product
4,David,Engineer,Infrastructure
5,Eva,Analyst,Data
6,Frank,Engineer,Backend
7,Grace,Designer,Mobile
8,Henry,Manager,Engineering
```

**TSV** (234 chars, 88 tokens):
```tsv
id	name	role	department
1	Alice	Engineer	Backend
2	Bob	Designer	Frontend
3	Carol	Manager	Product
4	David	Engineer	Infrastructure
5	Eva	Analyst	Data
6	Frank	Engineer	Backend
7	Grace	Designer	Mobile
8	Henry	Manager	Engineering
```

**YAML** (489 chars, 170 tokens):
```yaml
- department: Backend
  id: 1
  name: Alice
  role: Engineer
- department: Frontend
  id: 2
  name: Bob
  role: Designer
- department: Product
  id: 3
  name: Carol
  role: Manager
- department: Infrastructure
  id: 4
  name: David
  role: Engineer
- department: Data
  id: 5
  name: Eva
  role: Analyst
- department: Backend
  id: 6
  name: Frank
  role: Engineer
- department: Mobile
... (truncated)
```

**TOON** (246 chars, 98 tokens):
```toon
[8]{id,name,role,department}:
  1,Alice,Engineer,Backend
  2,Bob,Designer,Frontend
  3,Carol,Manager,Product
  4,David,Engineer,Infrastructure
  5,Eva,Analyst,Data
  6,Frank,Engineer,Backend
  7,Grace,Designer,Mobile
  8,Henry,Manager,Engineering
```

**TSON** (229 chars, 86 tokens):
```tson
{@id,name,role,department#8|1,Alice,Engineer,Backend|2,Bob,Designer,Frontend|3,Carol,Manager,Product|4,David,Engineer,Infrastructure|5,Eva,Analyst,Data|6,Frank,Engineer,Backend|7,Grace,Designer,Mobile|8,Henry,Manager,Engineering}
```

**minemizer** (251 chars, 75 tokens):
```txt
id; name; role; department
1; Alice; Engineer; Backend
2; Bob; Designer; Frontend
3; Carol; Manager; Product
4; David; Engineer; Infrastructure
5; Eva; Analyst; Data
6; Frank; Engineer; Backend
7; Grace; Designer; Mobile
8; Henry; Manager; Engineering
```

**minemizer (compact)** (224 chars, 82 tokens):
```txt
id;name;role;department
1;Alice;Engineer;Backend
2;Bob;Designer;Frontend
3;Carol;Manager;Product
4;David;Engineer;Infrastructure
5;Eva;Analyst;Data
6;Frank;Engineer;Backend
7;Grace;Designer;Mobile
8;Henry;Manager;Engineering
```

---

## nested_objects.json

Original size (JSON pretty): **741 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 741 | 407 | 322 | 252 | 252 | 308.2 | 2.4 |
| JSON (min) | 470 | 143 | 159 | 127 | 127 | 139.0 | 5.3 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 463 | 195 | 182 | 158 | 158 | 173.2 | 4.3 |
| TOON | 527 | 252 | 191 | 166 | 166 | 193.8 | 3.8 |
| TSON | 249 | 101 | 104 | 75 | 75 | 88.8 | 8.3 |
| minemizer | 259 | 90 | 95 | 77 | 77 | 84.8 | 8.7 |
| minemizer (compact) | 232 | 95 | 100 | 78 | 78 | 87.8 | 8.4 |

### Serialized outputs

**JSON (pretty)** (741 chars, 308 tokens):
```json
[
  {
    "id": 1,
    "user": {
      "name": "Alice",
      "email": "alice@example.com"
    },
    "status": "active"
  },
  {
    "id": 2,
    "user": {
      "name": "Bob",
      "email": "bob@example.com"
    },
    "status": "inactive"
  },
  {
    "id": 3,
    "user": {
      "name": "Carol",
      "email": "carol@example.com"
    },
    "status": "active"
  },
... (truncated)
```

**JSON (min)** (470 chars, 139 tokens):
```json
[{"id":1,"user":{"name":"Alice","email":"alice@example.com"},"status":"active"},{"id":2,"user":{"name":"Bob","email":"bob@example.com"},"status":"inactive"},{"id":3,"user":{"name":"Carol","email":"carol@example.com"},"status":"active"},{"id":4,"user":{"name":"David","email":"david@example.com"},"status":"pending"},{"id":5,"user":{"name":"Eva","email":"eva@example.com"},"status":"active"},{"id":6,"user":{"name":"Frank","email":"frank@example.com"},"status":"active"}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (463 chars, 173 tokens):
```yaml
- id: 1
  status: active
  user:
    email: alice@example.com
    name: Alice
- id: 2
  status: inactive
  user:
    email: bob@example.com
    name: Bob
- id: 3
  status: active
  user:
    email: carol@example.com
    name: Carol
- id: 4
  status: pending
  user:
    email: david@example.com
    name: David
- id: 5
  status: active
  user:
    email: eva@example.com
    name: Eva
... (truncated)
```

**TOON** (527 chars, 194 tokens):
```toon
[6]:
  - id: 1
    user:
      name: Alice
      email: alice@example.com
    status: active
  - id: 2
    user:
      name: Bob
      email: bob@example.com
    status: inactive
  - id: 3
    user:
      name: Carol
      email: carol@example.com
    status: active
  - id: 4
    user:
      name: David
      email: david@example.com
    status: pending
  - id: 5
    user:
      name: Eva
      email: eva@example.com
... (truncated)
```

**TSON** (249 chars, 89 tokens):
```tson
{@id,user(@name,email),status#6|1,{Alice,"alice@example.com"},active|2,{Bob,"bob@example.com"},inactive|3,{Carol,"carol@example.com"},active|4,{David,"david@example.com"},pending|5,{Eva,"eva@example.com"},active|6,{Frank,"frank@example.com"},active}
```

**minemizer** (259 chars, 85 tokens):
```txt
id; user{ name; email}; status
1; { Alice; alice@example.com}; active
2; { Bob; bob@example.com}; inactive
3; { Carol; carol@example.com}; active
4; { David; david@example.com}; pending
5; { Eva; eva@example.com}; active
6; { Frank; frank@example.com}; active
```

**minemizer (compact)** (232 chars, 88 tokens):
```txt
id;user{ name;email};status
1;{Alice;alice@example.com};active
2;{Bob;bob@example.com};inactive
3;{Carol;carol@example.com};active
4;{David;david@example.com};pending
5;{Eva;eva@example.com};active
6;{Frank;frank@example.com};active
```

---

## lists_of_primitives.json

Original size (JSON pretty): **610 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 610 | 382 | 280 | 217 | 217 | 274.0 | 2.2 |
| JSON (min) | 330 | 115 | 125 | 103 | 103 | 111.5 | 5.5 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 341 | 153 | 157 | 149 | 149 | 152.0 | 4.0 |
| TOON | 339 | 161 | 141 | 137 | 137 | 144.0 | 4.2 |
| TSON | 168 | 80 | 79 | 65 | 65 | 72.2 | 8.4 |
| minemizer | 194 | 81 | 79 | 71 | 71 | 75.5 | 8.1 |
| minemizer (compact) | 165 | 83 | 83 | 70 | 70 | 76.5 | 8.0 |

### Serialized outputs

**JSON (pretty)** (610 chars, 274 tokens):
```json
[
  {
    "id": 1,
    "name": "Alice",
    "skills": [
      "python",
      "go",
      "rust"
    ]
  },
  {
    "id": 2,
    "name": "Bob",
    "skills": [
      "javascript",
      "typescript"
    ]
  },
  {
    "id": 3,
    "name": "Carol",
    "skills": [
      "java",
      "kotlin",
      "scala",
... (truncated)
```

**JSON (min)** (330 chars, 112 tokens):
```json
[{"id":1,"name":"Alice","skills":["python","go","rust"]},{"id":2,"name":"Bob","skills":["javascript","typescript"]},{"id":3,"name":"Carol","skills":["java","kotlin","scala","groovy"]},{"id":4,"name":"David","skills":["c","cpp"]},{"id":5,"name":"Eva","skills":["ruby","elixir","erlang"]},{"id":6,"name":"Frank","skills":["swift"]}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (341 chars, 152 tokens):
```yaml
- id: 1
  name: Alice
  skills:
  - python
  - go
  - rust
- id: 2
  name: Bob
  skills:
  - javascript
  - typescript
- id: 3
  name: Carol
  skills:
  - java
  - kotlin
  - scala
  - groovy
- id: 4
  name: David
  skills:
  - c
  - cpp
- id: 5
  name: Eva
... (truncated)
```

**TOON** (339 chars, 144 tokens):
```toon
[6]:
  - id: 1
    name: Alice
    skills[3]: python,go,rust
  - id: 2
    name: Bob
    skills[2]: javascript,typescript
  - id: 3
    name: Carol
    skills[4]: java,kotlin,scala,groovy
  - id: 4
    name: David
    skills[2]: c,cpp
  - id: 5
    name: Eva
    skills[3]: ruby,elixir,erlang
  - id: 6
    name: Frank
    skills[1]: swift
```

**TSON** (168 chars, 72 tokens):
```tson
{@id,name,skills#6|1,Alice,[python,go,rust]|2,Bob,[javascript,typescript]|3,Carol,[java,kotlin,scala,groovy]|4,David,[c,cpp]|5,Eva,[ruby,elixir,erlang]|6,Frank,[swift]}
```

**minemizer** (194 chars, 76 tokens):
```txt
id; name; skills[]
1; Alice; [ python; go; rust]
2; Bob; [ javascript; typescript]
3; Carol; [ java; kotlin; scala; groovy]
4; David; [ c; cpp]
5; Eva; [ ruby; elixir; erlang]
6; Frank; [ swift]
```

**minemizer (compact)** (165 chars, 76 tokens):
```txt
id;name;skills[]
1;Alice;[python;go;rust]
2;Bob;[javascript;typescript]
3;Carol;[java;kotlin;scala;groovy]
4;David;[c;cpp]
5;Eva;[ruby;elixir;erlang]
6;Frank;[swift]
```

---

## sparse_data.json

Original size (JSON pretty): **589 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 589 | 318 | 278 | 224 | 224 | 261.0 | 2.3 |
| JSON (min) | 378 | 121 | 133 | 114 | 114 | 120.5 | 4.9 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 356 | 135 | 150 | 143 | 143 | 142.8 | 4.1 |
| TOON | 414 | 184 | 161 | 153 | 153 | 162.8 | 3.6 |
| TSON | 300 | 136 | 133 | 109 | 109 | 121.8 | 4.8 |
| minemizer | 232 | 79 | 87 | 77 | 77 | 80.0 | 7.4 |
| minemizer (compact) | 207 | 84 | 90 | 77 | 77 | 82.0 | 7.2 |

### Serialized outputs

**JSON (pretty)** (589 chars, 261 tokens):
```json
[
  {
    "id": 1,
    "name": "Carol",
    "role": "Manager"
  },
  {
    "id": 2,
    "name": "Dave",
    "remote": true
  },
  {
    "id": 3,
    "name": "Eve",
    "role": "Designer",
    "team": "UX"
  },
  {
    "id": 4,
    "name": "Frank",
    "department": "Engineering"
  },
  {
    "id": 5,
    "name": "Grace",
... (truncated)
```

**JSON (min)** (378 chars, 120 tokens):
```json
[{"id":1,"name":"Carol","role":"Manager"},{"id":2,"name":"Dave","remote":true},{"id":3,"name":"Eve","role":"Designer","team":"UX"},{"id":4,"name":"Frank","department":"Engineering"},{"id":5,"name":"Grace","role":"Engineer","remote":true,"team":"Platform"},{"id":6,"name":"Henry","role":"Analyst"},{"id":7,"name":"Ivy"},{"id":8,"name":"Jack","department":"Sales","remote":false}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (356 chars, 143 tokens):
```yaml
- id: 1
  name: Carol
  role: Manager
- id: 2
  name: Dave
  remote: true
- id: 3
  name: Eve
  role: Designer
  team: UX
- department: Engineering
  id: 4
  name: Frank
- id: 5
  name: Grace
  remote: true
  role: Engineer
  team: Platform
- id: 6
  name: Henry
  role: Analyst
- id: 7
  name: Ivy
- department: Sales
  id: 8
... (truncated)
```

**TOON** (414 chars, 163 tokens):
```toon
[8]:
  - id: 1
    name: Carol
    role: Manager
  - id: 2
    name: Dave
    remote: true
  - id: 3
    name: Eve
    role: Designer
    team: UX
  - id: 4
    name: Frank
    department: Engineering
  - id: 5
    name: Grace
    role: Engineer
    remote: true
    team: Platform
  - id: 6
    name: Henry
    role: Analyst
  - id: 7
    name: Ivy
  - id: 8
... (truncated)
```

**TSON** (300 chars, 122 tokens):
```tson
[{@id,name,role|1,Carol,Manager},{@id,name,remote|2,Dave,true},{@id,name,role,team|3,Eve,Designer,UX},{@id,name,department|4,Frank,Engineering},{@id,name,role,remote,team|5,Grace,Engineer,true,Platform},{@id,name,role|6,Henry,Analyst},{@id,name|7,Ivy},{@id,name,department,remote|8,Jack,Sales,false}]
```

**minemizer** (232 chars, 80 tokens):
```txt
id; name; role
1; Carol; Manager
2; Dave; ; remote:True
3; Eve; Designer; team:UX
4; Frank; ; department:Engineering
5; Grace; Engineer; remote:True; team:Platform
6; Henry; Analyst
7; Ivy; 
8; Jack; ; department:Sales; remote:False
```

**minemizer (compact)** (207 chars, 82 tokens):
```txt
id;name;role
1;Carol;Manager
2;Dave;;remote:True
3;Eve;Designer;team:UX
4;Frank;;department:Engineering
5;Grace;Engineer;remote:True;team:Platform
6;Henry;Analyst
7;Ivy;
8;Jack;;department:Sales;remote:False
```

---

## coingecko_coins.json

Original size (JSON pretty): **1611780 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 1611780 | 862469 | 749813 | 611575 | 609227 | 708271.0 | 2.3 |
| JSON (min) | 1147811 | 400135 | 422810 | 361897 | 359549 | 386097.8 | 4.2 |
| CSV | 603635 | 282641 | 303115 | 228404 | 227103 | 260315.8 | 6.2 |
| TSV | 603601 | 282672 | 303547 | 224078 | 222774 | 258267.8 | 6.2 |
| YAML | 1048449 | 429115 | 454247 | 409204 | 407827 | 425098.2 | 3.8 |
| TOON | 623383 | 279372 | 301477 | 245044 | 243750 | 267410.8 | 6.0 |
| TSON | 603594 | 271823 | 293257 | 232225 | 230921 | 257056.5 | 6.3 |
| minemizer | 622925 | 258209 | 282585 | 237950 | 236563 | 253826.8 | 6.3 |
| minemizer (compact) | 584259 | 263320 | 285149 | 237554 | 236253 | 255569.0 | 6.3 |

### Serialized outputs

**JSON (pretty)** (1611780 chars, 708271 tokens):
```json
[
  {
    "id": "_",
    "symbol": "gib",
    "name": "\u0f3c \u3064 \u25d5_\u25d5 \u0f3d\u3064"
  },
  {
    "id": "000-capital",
    "symbol": "000",
    "name": "000 Capital"
  },
  {
    "id": "01111010011110000110001001110100-token",
    "symbol": "01111010011110000110001001110100",
    "name": "01111010011110000110001001110100"
  },
  {
    "id": "01-token",
    "symbol": "01",
    "name": "01"
  },
  {
    "id": "0chain",
    "symbol": "zcn",
    "name": "Zus"
... (truncated)
```

**JSON (min)** (1147811 chars, 386098 tokens):
```json
[{"id":"_","symbol":"gib","name":"\u0f3c \u3064 \u25d5_\u25d5 \u0f3d\u3064"},{"id":"000-capital","symbol":"000","name":"000 Capital"},{"id":"01111010011110000110001001110100-token","symbol":"01111010011110000110001001110100","name":"01111010011110000110001001110100"},{"id":"01-token","symbol":"01","name":"01"},{"id":"0chain","symbol":"zcn","name":"Zus"},{"id":"0vix-protocol","symbol":"vix","name":"0VIX Protocol"},{"id":"0x","symbol":"zrx","name":"0x Protocol"},{"id":"0x0-ai-ai-smart-contract","symbol":"0x0","name":"0x0.ai: AI Smart Contract"},{"id":"0x678-landwolf-1933","symbol":"wolf","name":"Landwolf"},{"id":"0xgasless-2","symbol":"0xgas","name":"0xGasless"},{"id":"0xgen","symbol":"xgn","name":"0xGen"},{"id":"0x-leverage","symbol":"oxl","name":"0x Leverage"},{"id":"0xlsd","symbol":"0xlsd","name":"0xLSD"},{"id":"0xmonk","symbol":"monk","name":"0xMonk by Virtuals"},{"id":"0x-protocol-avalanche-bridged-zrx-e","symbol":"zrx.e","name":"Avalanche Bridged ZRX (Avalanche)"},{"id":"0xshadow","symbol":"0xs","name":"0xShadow"},{"id":"0xsim-by-virtuals","symbol":"sage","name":"0xsim by Virtuals"},{"id":"0xy","symbol":"0xy","name":"0xy"},{"id":"-10","symbol":"loong","name":"\u9f99"},{"id":"1000bonk","symbol":"1000bonk","name":"1000BONK"},{"id":"1000btt","symbol":"1000btt","name":"1000BTT"},{"id":"1000cat","symbol":"1000cat","name":"1000CAT"},{"id":"1000chems","symbol":"1000cheems","name":"1000CHEMS"},{"id":"1000mog","symbol":"1000mog","name":"1000MOG"},{"id":"1000rats","symbol":"1000rats","name":"1000RATS"},{"id":"1000sats-ordinals","symbol":"1000sats","name":"1000SATS (Ordinals)"},{"id":"1000shib","symbol":"1000shib","name":"1000SHIB"},{"id":"1000x-by-virtuals","symbol":"1000x","name":"1000x by Virtuals"},{"id":"100-token","symbol":"100\u00a5","name":"100\u00a5"},{"id":"100xdarren","symbol":"100x","name":"100xDarren"},{"id":"10-figs","symbol":"figs","name":"10 figs"},{"id":"-11","symbol":"\u8d75\u957f\u5a25","name":"\u8d75\u957f\u5a25"},{"id":"11am","symbol":"11am","name":"11am"},{"id":"1984-token","symbol":"1984","name":"1984"},{"id":"1art","symbol":"1art","name":"OneArt"},{"id":"1-coin-can-change-your-life","symbol":"1-coin-can-change-your-life","name":"1 Coin Can Change Your Life"},{"id":"1-community-can-change-your-life","symbol":"community","name":"1 community can change your life"},{"id":"1dev","symbol":"1dev","name":"1DEV"},{"id":"1-dog-can-change-your-life","symbol":"1dog","name":"1 dog can change your life"},{"id":"1-dollar-sol-coin","symbol":"$1","name":"$1"},{"id":"1guy","symbol":"1guy","name":"1GUY"},{"id":"1hive-water","symbol":"water","name":"1Hive Water"},{"id":"1hub-ai","symbol":"1hub","name":"1Hub.ai"},{"id":"1inch","symbol":"1inch","name":"1INCH"},{"id":"1inch-yvault","symbol":"yv1inch","name":"1INCH yVault"},{"id":"1intro","symbol":"chef","name":"CoinChef"},{"id":"1mbabydoge","symbol":"1mbabydoge","name":"1MBABYDOGE"},{"id":"1million-nfts","symbol":"1mil","name":"1MillionNFTs"},{"id":"1move-token","symbol":"1mt","name":"1Move Token"},{"id":"1-narrative-can-change-your-life","symbol":"narrative","name":"1 narrative can change your life"},{"id":"1-one","symbol":"one","name":"1 (one)"},{"id":"1-percent","symbol":"1%","name":"1%"},{"id":"1rus-btc25","symbol":"@btc25","name":"@BTC25"},{"id":"1rus-dao","symbol":"1rusd","name":"1RUS DAO"},{"id":"1-squirrel","symbol":"peanut","name":"OG Peanut"},{"id":"1-token","symbol":"1","name":"1"},{"id":"2004-pepe","symbol":"bog","name":"2004 PEPE"},{"id":"2025-token","symbol":"2025","name":"2025 TOKEN"},{"id":"2077-code","symbol":"2077","name":"2077 CODE"},{"id":"2080","symbol":"2080","name":"2080"},{"id":"21million","symbol":"21m","name":"21Million"},{"id":"23-turtles","symbol":"ai23t","name":"23 Turtles"},{"id":"2-3-years-and-forget","symbol":"23","name":"2-3 years and forget"},{"id":"24k-gold-pepe","symbol":"goldpepe","name":"24K Gold PEPE"},{"id":"2dai-io","symbol":"2dai","name":"2DAI.io[Old]"},{"id":"2dai-io-2","symbol":"2dai","name":"2DAI.io"},{"id":"2g-carbon-coin","symbol":"2gcc","name":"2G Carbon Coin"},{"id":"2moon","symbol":"moon","name":"2MOON"},{"id":"2-token","symbol":"2","name":"2"},{"id":"-3","symbol":"meow","name":"Meow Meow Coin"},{"id":"3000-token","symbol":"3000","name":"3000"},{"id":"360noscope420blazeit","symbol":"mlg","name":"360noscope420blazeit"},{"id":"375ai","symbol":"eat","name":"375ai"},{"id":"39a-fun","symbol":"39a","name":"39a.fun"},{"id":"3a-lending-protocol","symbol":"a3a","name":"3A"},{"id":"3bubu","symbol":"3bubu","name":"3BuBu"},{"id":"3dpass","symbol":"p3d","name":"3DPass"},{"id":"3space-art","symbol":"pace","name":"3SPACE ART"},{"id":"4","symbol":"four","name":"4"},{"id":"401jk","symbol":"401jk","name":"401jK"},{"id":"401k","symbol":"401k","name":"401K"},{"id":"404-gen","symbol":"sn17","name":"404\u2014GEN"},{"id":"4-2","symbol":"4","name":"4"},{"id":"42069coin","symbol":"42069coin","name":"42069COIN"},{"id":"4-2-aminoethyl-benzene-1-2-diol","symbol":"dopamine","name":"4-(2-Aminoethyl)benzene-1,2-diol"},{"id":"42-coin","symbol":"
... (truncated)
```

**CSV** (603635 chars, 260316 tokens):
```csv
id,symbol,name
_,gib,༼ つ ◕_◕ ༽つ
000-capital,000,000 Capital
01111010011110000110001001110100-token,01111010011110000110001001110100,01111010011110000110001001110100
01-token,01,01
0chain,zcn,Zus
0vix-protocol,vix,0VIX Protocol
0x,zrx,0x Protocol
0x0-ai-ai-smart-contract,0x0,0x0.ai: AI Smart Contract
0x678-landwolf-1933,wolf,Landwolf
0xgasless-2,0xgas,0xGasless
0xgen,xgn,0xGen
0x-leverage,oxl,0x Leverage
0xlsd,0xlsd,0xLSD
0xmonk,monk,0xMonk by Virtuals
0x-protocol-avalanche-bridged-zrx-e,zrx.e,Avalanche Bridged ZRX (Avalanche)
0xshadow,0xs,0xShadow
0xsim-by-virtuals,sage,0xsim by Virtuals
0xy,0xy,0xy
-10,loong,龙
1000bonk,1000bonk,1000BONK
1000btt,1000btt,1000BTT
1000cat,1000cat,1000CAT
1000chems,1000cheems,1000CHEMS
1000mog,1000mog,1000MOG
... (truncated)
```

**TSV** (603601 chars, 258268 tokens):
```tsv
id	symbol	name
_	gib	༼ つ ◕_◕ ༽つ
000-capital	000	000 Capital
01111010011110000110001001110100-token	01111010011110000110001001110100	01111010011110000110001001110100
01-token	01	01
0chain	zcn	Zus
0vix-protocol	vix	0VIX Protocol
0x	zrx	0x Protocol
0x0-ai-ai-smart-contract	0x0	0x0.ai: AI Smart Contract
0x678-landwolf-1933	wolf	Landwolf
0xgasless-2	0xgas	0xGasless
0xgen	xgn	0xGen
0x-leverage	oxl	0x Leverage
0xlsd	0xlsd	0xLSD
0xmonk	monk	0xMonk by Virtuals
0x-protocol-avalanche-bridged-zrx-e	zrx.e	Avalanche Bridged ZRX (Avalanche)
0xshadow	0xs	0xShadow
0xsim-by-virtuals	sage	0xsim by Virtuals
0xy	0xy	0xy
-10	loong	龙
1000bonk	1000bonk	1000BONK
1000btt	1000btt	1000BTT
1000cat	1000cat	1000CAT
1000chems	1000cheems	1000CHEMS
1000mog	1000mog	1000MOG
... (truncated)
```

**YAML** (1048449 chars, 425098 tokens):
```yaml
- id: _
  name: ༼ つ ◕_◕ ༽つ
  symbol: gib
- id: 000-capital
  name: 000 Capital
  symbol: '000'
- id: 01111010011110000110001001110100-token
  name: '01111010011110000110001001110100'
  symbol: '01111010011110000110001001110100'
- id: 01-token
  name: '01'
  symbol: '01'
- id: 0chain
  name: Zus
  symbol: zcn
- id: 0vix-protocol
  name: 0VIX Protocol
  symbol: vix
- id: 0x
  name: 0x Protocol
  symbol: zrx
- id: 0x0-ai-ai-smart-contract
  name: '0x0.ai: AI Smart Contract'
  symbol: '0x0'
- id: 0x678-landwolf-1933
... (truncated)
```

**TOON** (623383 chars, 267411 tokens):
```toon
[19332]{id,symbol,name}:
  _,gib,༼ つ ◕_◕ ༽つ
  000-capital,"000",000 Capital
  01111010011110000110001001110100-token,"01111010011110000110001001110100","01111010011110000110001001110100"
  01-token,"01","01"
  0chain,zcn,Zus
  0vix-protocol,vix,0VIX Protocol
  0x,zrx,0x Protocol
  0x0-ai-ai-smart-contract,0x0,"0x0.ai: AI Smart Contract"
  0x678-landwolf-1933,wolf,Landwolf
  0xgasless-2,0xgas,0xGasless
  0xgen,xgn,0xGen
  0x-leverage,oxl,0x Leverage
  0xlsd,0xlsd,0xLSD
  0xmonk,monk,0xMonk by Virtuals
  0x-protocol-avalanche-bridged-zrx-e,zrx.e,Avalanche Bridged ZRX (Avalanche)
  0xshadow,0xs,0xShadow
  0xsim-by-virtuals,sage,0xsim by Virtuals
  0xy,0xy,0xy
  "-10",loong,龙
  1000bonk,1000bonk,1000BONK
  1000btt,1000btt,1000BTT
  1000cat,1000cat,1000CAT
  1000chems,1000cheems,1000CHEMS
  1000mog,1000mog,1000MOG
... (truncated)
```

**TSON** (603594 chars, 257056 tokens):
```tson
{@id,symbol,name#19332|_,gib,"༼ つ ◕_◕ ༽つ"|000-capital,"000","000 Capital"|01111010011110000110001001110100-token,"01111010011110000110001001110100","01111010011110000110001001110100"|01-token,"01","01"|0chain,zcn,Zus|0vix-protocol,vix,"0VIX Protocol"|0x,zrx,"0x Protocol"|0x0-ai-ai-smart-contract,0x0,"0x0.ai: AI Smart Contract"|0x678-landwolf-1933,wolf,Landwolf|0xgasless-2,0xgas,0xGasless|0xgen,xgn,0xGen|0x-leverage,oxl,"0x Leverage"|0xlsd,0xlsd,0xLSD|0xmonk,monk,"0xMonk by Virtuals"|0x-protocol-avalanche-bridged-zrx-e,zrx.e,"Avalanche Bridged ZRX (Avalanche)"|0xshadow,0xs,0xShadow|0xsim-by-virtuals,sage,"0xsim by Virtuals"|0xy,0xy,0xy|"-10",loong,龙|1000bonk,1000bonk,1000BONK|1000btt,1000btt,1000BTT|1000cat,1000cat,1000CAT|1000chems,1000cheems,1000CHEMS|1000mog,1000mog,1000MOG|1000rats,1000rats,1000RATS|1000sats-ordinals,1000sats,"1000SATS (Ordinals)"|1000shib,1000shib,1000SHIB|1000x-by-virtuals,1000x,"1000x by Virtuals"|100-token,100¥,100¥|100xdarren,100x,100xDarren|10-figs,figs,"10 figs"|"-11",赵长娥,赵长娥|11am,11am,11am|1984-token,"1984","1984"|1art,1art,OneArt|1-coin-can-change-your-life,1-coin-can-change-your-life,"1 Coin Can Change Your Life"|1-community-can-change-your-life,community,"1 community can change your life"|1dev,1dev,1DEV|1-dog-can-change-your-life,1dog,"1 dog can change your life"|1-dollar-sol-coin,$1,$1|1guy,1guy,1GUY|1hive-water,water,"1Hive Water"|1hub-ai,1hub,1Hub.ai|1inch,1inch,1INCH|1inch-yvault,yv1inch,"1INCH yVault"|1intro,chef,CoinChef|1mbabydoge,1mbabydoge,1MBABYDOGE|1million-nfts,1mil,1MillionNFTs|1move-token,1mt,"1Move Token"|1-narrative-can-change-your-life,narrative,"1 narrative can change your life"|1-one,one,"1 (one)"|1-percent,1%,1%|1rus-btc25,"@btc25","@BTC25"|1rus-dao,1rusd,"1RUS DAO"|1-squirrel,peanut,"OG Peanut"|1-token,"1","1"|2004-pepe,bog,"2004 PEPE"|2025-token,"2025","2025 TOKEN"|2077-code,"2077","2077 CODE"|"2080","2080","2080"|21million,21m,21Million|23-turtles,ai23t,"23 Turtles"|2-3-years-and-forget,"23","2-3 years and forget"|24k-gold-pepe,goldpepe,"24K Gold PEPE"|2dai-io,2dai,"2DAI.io[Old]"|2dai-io-2,2dai,2DAI.io|2g-carbon-coin,2gcc,"2G Carbon Coin"|2moon,moon,2MOON|2-token,"2","2"|"-3",meow,"Meow Meow Coin"|3000-token,"3000","3000"|360noscope420blazeit,mlg,360noscope420blazeit|375ai,eat,375ai|39a-fun,39a,39a.fun|3a-lending-protocol,a3a,3A|3bubu,3bubu,3BuBu|3dpass,p3d,3DPass|3space-art,pace,"3SPACE ART"|"4",four,"4"|401jk,401jk,401jK|401k,401k,401K|404-gen,sn17,404—GEN|4-2,"4","4"|42069coin,42069coin,42069COIN|4-2-aminoethyl-benzene-1-2-diol,dopamine,"4-(2-Aminoethyl)benzene-1,2-diol"|42-coin,"42",42-coin|4444-token,"4444","4444"|4444-token-3,"4444","4444"|4547-token,"4547","4547"|47th-potus,trump47,"47th POTUS"|4chan,4chan,4Chan|4everland,4ever,4EVERLAND|4gentic,4gs,4GENTIC|4-next-unicorn,nxtu,"4 Next Unicorn"|4nonswap,4non,4nonSwap|4tb-coin,4tb,"4TB Coin"|4tool-ai,4tool,4TOOL.ai|4trump,4win,4TRUMP|4-way-mirror-money,4wmm,"4-Way Mirror Money"|"-5",🟥🟩,🟥🟪🟦🟩🟨🟧|500m-piece-of-paper,paper,"$500M piece of paper"|501-token,"501","501"|589-token,"589","589"|5ire,5ire,5ire|5mc,5mc,5mc|5tars,5tars,5TARS|5th-scape,$5scape,"5th Scape"|"-6","　","　"|666-token,"666","666"|67coin,"67",67COIN|"69420","69420","69420"|6chicken9,pop,6Chicken9|6ixrooms,6ixrooms,6ixROOMS|"-7",∅,Voidify|717ai-by-virtuals,wire,"717ai by Virtuals"|777fuckilluminatiworldwid,fiw,777FuckIlluminatiWorldwid|"-8",🔶,🔶|8004-dog,dog8004,"8004 Dog"|8008-token,"8008","8008"|888coin,發發發,888Coin|888-token,"888","888"|88mph,mph,88mph|8-ball,sn125,"8 Ball"|8-bit-coin,coin,"8-Bit Coin"|8chan,8chan,8chan|8pay,8pay,8Pay|8-token,"8","8"|"-9",∑,∑|9-5,9-5,9to5|99-bitcoins,99btc,"99 Bitcoins"|99starz,stz,99Starz|9inch,9inch,9inch|9mm,9mm,9mm|9to5io,9to5,9to5io|a0x,a0x,A0x|a16gems,a16g,a16gems|a16z-ai-dog,tilly,"a16z AI Dog"|a51-finance,a51,"A51 Finance"|a7a5,a7a5,A7A5|aaa-cat,aaa,"aaa cat"|aaai_agent-by-virtuals,aaai,"AAAI_agent by Virtuals"|aada-finance,lenfi,Lenfi|aadex-finance,ade,"AADex Finance"|aagent-ai,aai,Aagent.ai|aag-ventures,aag,AAG|aardvark-2,vark,Aardvark|aark-digital,aark,"Aark Digital"|aarna-afi-802v2,"afi 802v2","aarna afi 802v2"|aarna-atv111,atv111,"aarna atv111"|aarna-atv111-arbitrum,atv111,"aarna atv111 (Arbitrum)"|aarna-atv111-sonic,atv111,"aarna atv111 (Sonic)"|aarna-atv-808,atv808,"aarna atv 808"|aarna-atv-usdc,atvusdc,"aarna atv USDC (Arbitrum)"|aarna-atv-usdc-ethereum,atvusdc,"aarna atv USDC (Ethereum)"|aastoken,aast,AASToken|aave,aave,Aave|aave-aave,aaave,"Aave AAVE"|aave-amm-bptbalweth,aammbptbalweth,"Aave AMM BptBALWETH"|aave-amm-bptwbtcweth,aammbptwbtcweth,"Aave AMM BptWBTCWETH"|aave-amm-dai,aammdai,"Aave AMM DAI"|aave-amm-uniaaveweth,aammuniaaveweth,"Aave AMM UniAAVEWETH"|aave-amm-unibatweth,aammunibatweth,"Aave AMM UniBATWETH"|aave-amm-unicrvweth,aammunicrvweth,"Aave AMM UniCRVWETH"|aave-amm-unidaiusdc,aammunidaiusdc,"Aave AMM UniDAIUSDC"|aave-amm-unidaiweth,aammunidaiweth,"Aave AMM UniDAIWETH"|aave-amm-unilinkweth,aammunilinkweth,"Aave AMM UniLINKWETH"|aave-amm-unimkrweth,aammunimkrweth,"Aave AMM 
... (truncated)
```

**minemizer** (622925 chars, 253827 tokens):
```txt
id; symbol; name
_; gib; ༼ つ ◕_◕ ༽つ
000-capital; 000; 000 Capital
01111010011110000110001001110100-token; 01111010011110000110001001110100; 01111010011110000110001001110100
01-token; 01; 01
0chain; zcn; Zus
0vix-protocol; vix; 0VIX Protocol
0x; zrx; 0x Protocol
0x0-ai-ai-smart-contract; 0x0; 0x0.ai: AI Smart Contract
0x678-landwolf-1933; wolf; Landwolf
0xgasless-2; 0xgas; 0xGasless
0xgen; xgn; 0xGen
0x-leverage; oxl; 0x Leverage
0xlsd; 0xlsd; 0xLSD
0xmonk; monk; 0xMonk by Virtuals
0x-protocol-avalanche-bridged-zrx-e; zrx.e; Avalanche Bridged ZRX (Avalanche)
0xshadow; 0xs; 0xShadow
0xsim-by-virtuals; sage; 0xsim by Virtuals
0xy; 0xy; 0xy
-10; loong; 龙
1000bonk; 1000bonk; 1000BONK
1000btt; 1000btt; 1000BTT
1000cat; 1000cat; 1000CAT
1000chems; 1000cheems; 1000CHEMS
1000mog; 1000mog; 1000MOG
... (truncated)
```

**minemizer (compact)** (584259 chars, 255569 tokens):
```txt
id;symbol;name
_;gib;༼ つ ◕_◕ ༽つ
000-capital;000;000 Capital
01111010011110000110001001110100-token;01111010011110000110001001110100;01111010011110000110001001110100
01-token;01;01
0chain;zcn;Zus
0vix-protocol;vix;0VIX Protocol
0x;zrx;0x Protocol
0x0-ai-ai-smart-contract;0x0;0x0.ai: AI Smart Contract
0x678-landwolf-1933;wolf;Landwolf
0xgasless-2;0xgas;0xGasless
0xgen;xgn;0xGen
0x-leverage;oxl;0x Leverage
0xlsd;0xlsd;0xLSD
0xmonk;monk;0xMonk by Virtuals
0x-protocol-avalanche-bridged-zrx-e;zrx.e;Avalanche Bridged ZRX (Avalanche)
0xshadow;0xs;0xShadow
0xsim-by-virtuals;sage;0xsim by Virtuals
0xy;0xy;0xy
-10;loong;龙
1000bonk;1000bonk;1000BONK
1000btt;1000btt;1000BTT
1000cat;1000cat;1000CAT
1000chems;1000cheems;1000CHEMS
1000mog;1000mog;1000MOG
... (truncated)
```

---

## complex_mixed.json

Original size (JSON pretty): **1320 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 1320 | 768 | 560 | 455 | 427 | 552.5 | 2.4 |
| JSON (min) | 760 | 224 | 284 | 246 | 218 | 243.0 | 5.4 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 818 | 374 | 338 | 306 | 278 | 324.0 | 4.1 |
| TOON | 881 | 434 | 329 | 304 | 276 | 335.8 | 3.9 |
| TSON | 453 | 207 | 237 | 203 | 175 | 205.5 | 6.4 |
| minemizer | 421 | 159 | 201 | 191 | 163 | 178.5 | 7.4 |
| minemizer (compact) | 364 | 173 | 214 | 191 | 163 | 185.2 | 7.1 |

### Serialized outputs

**JSON (pretty)** (1320 chars, 552 tokens):
```json
[
  {
    "id": 1,
    "profile": {
      "name": "Grace",
      "location": {
        "city": "NYC",
        "country": "USA"
      }
    },
    "tags": [
      "admin",
      "verified"
    ],
    "metadata": {
      "created": "2024-01-15"
    }
  },
  {
    "id": 2,
    "profile": {
      "name": "Henry",
      "location": {
        "city": "London",
        "country": "UK"
... (truncated)
```

**JSON (min)** (760 chars, 243 tokens):
```json
[{"id":1,"profile":{"name":"Grace","location":{"city":"NYC","country":"USA"}},"tags":["admin","verified"],"metadata":{"created":"2024-01-15"}},{"id":2,"profile":{"name":"Henry","location":{"city":"London","country":"UK"}},"tags":["user"],"metadata":{"created":"2024-02-20","updated":"2024-03-10"}},{"id":3,"profile":{"name":"Ivy","location":{"city":"Tokyo","country":"Japan"}},"tags":["moderator","verified","premium"],"metadata":{"created":"2024-01-05"}},{"id":4,"profile":{"name":"Jack","location":{"city":"Sydney","country":"Australia"}},"tags":["user","new"],"metadata":{"created":"2024-04-01"}},{"id":5,"profile":{"name":"Kate","location":{"city":"Berlin","country":"Germany"}},"tags":["admin"],"metadata":{"created":"2023-12-01","updated":"2024-02-15"}}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (818 chars, 324 tokens):
```yaml
- id: 1
  metadata:
    created: '2024-01-15'
  profile:
    location:
      city: NYC
      country: USA
    name: Grace
  tags:
  - admin
  - verified
- id: 2
  metadata:
    created: '2024-02-20'
    updated: '2024-03-10'
  profile:
    location:
      city: London
      country: UK
    name: Henry
  tags:
  - user
- id: 3
  metadata:
    created: '2024-01-05'
... (truncated)
```

**TOON** (881 chars, 336 tokens):
```toon
[5]:
  - id: 1
    profile:
      name: Grace
      location:
        city: NYC
        country: USA
    tags[2]: admin,verified
    metadata:
      created: 2024-01-15
  - id: 2
    profile:
      name: Henry
      location:
        city: London
        country: UK
    tags[1]: user
    metadata:
      created: 2024-02-20
      updated: 2024-03-10
  - id: 3
    profile:
      name: Ivy
      location:
        city: Tokyo
... (truncated)
```

**TSON** (453 chars, 206 tokens):
```tson
{@id,profile(@name,location),tags,metadata#5|1,{Grace,{@city,country|NYC,USA}},[admin,verified],{@created|2024-01-15}|2,{Henry,{@city,country|London,UK}},[user],{@created,updated|2024-02-20,2024-03-10}|3,{Ivy,{@city,country|Tokyo,Japan}},[moderator,verified,premium],{@created|2024-01-05}|4,{Jack,{@city,country|Sydney,Australia}},[user,new],{@created|2024-04-01}|5,{Kate,{@city,country|Berlin,Germany}},[admin],{@created,updated|2023-12-01,2024-02-15}}
```

**minemizer** (421 chars, 178 tokens):
```txt
id; profile{ name; location{ city; country}}; tags[]; metadata{ created; ...}
1; { Grace; { NYC; USA}}; [ admin; verified]; { 2024-01-15}
2; { Henry; { London; UK}}; [ user]; { 2024-02-20; updated:2024-03-10}
3; { Ivy; { Tokyo; Japan}}; [ moderator; verified; premium]; { 2024-01-05}
4; { Jack; { Sydney; Australia}}; [ user; new]; { 2024-04-01}
5; { Kate; { Berlin; Germany}}; [ admin]; { 2023-12-01; updated:2024-02-15}
```

**minemizer (compact)** (364 chars, 185 tokens):
```txt
id;profile{ name;location{ city;country}};tags[];metadata{ created;...}
1;{Grace;{NYC;USA}};[admin;verified];{2024-01-15}
2;{Henry;{London;UK}};[user];{2024-02-20;updated:2024-03-10}
3;{Ivy;{Tokyo;Japan}};[moderator;verified;premium];{2024-01-05}
4;{Jack;{Sydney;Australia}};[user;new];{2024-04-01}
5;{Kate;{Berlin;Germany}};[admin];{2023-12-01;updated:2024-02-15}
```

---
