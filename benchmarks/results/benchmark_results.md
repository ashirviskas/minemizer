# Benchmark Results (Full Detail)

_Generated: 2025-11-30_

Tokenizers: gpt2, llama, qwen2.5, phi4

## complex_mixed.json

Original size (JSON pretty): **1320 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 1320 | 768 | 560 | 455 | 427 | 552.5 | 2.39 |
| JSON (min) | 760 | 224 | 284 | 246 | 218 | 243.0 | 5.43 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 818 | 374 | 338 | 306 | 278 | 324.0 | 4.07 |
| minemizer | 421 | 159 | 201 | 191 | 163 | 178.5 | 7.39 |
| minemizer (compact) | 364 | 173 | 214 | 191 | 163 | 185.2 | 7.13 |

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
      }
    },
    "tags": [
      "user"
    ],
    "metadata": {
      "created": "2024-02-20",
      "updated": "2024-03-10"
    }
  },
  {
    "id": 3,
    "profile": {
      "name": "Ivy",
      "location": {
        "city": "Tokyo",
        "country": "Japan"
      }
    },
    "tags": [
      "moderator",
      "verified",
      "premium"
    ],
    "metadata": {
      "created": "2024-01-05"
    }
  },
  {
    "id": 4,
    "profile": {
      "name": "Jack",
      "location": {
        "city": "Sydney",
        "country": "Australia"
      }
    },
    "tags": [
      "user",
      "new"
    ],
    "metadata": {
      "created": "2024-04-01"
    }
  },
  {
    "id": 5,
    "profile": {
      "name": "Kate",
      "location": {
        "city": "Berlin",
        "country": "Germany"
      }
    },
    "tags": [
      "admin"
    ],
    "metadata": {
      "created": "2023-12-01",
      "updated": "2024-02-15"
    }
  }
]
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
  profile:
    location:
      city: Tokyo
      country: Japan
    name: Ivy
  tags:
  - moderator
  - verified
  - premium
- id: 4
  metadata:
    created: '2024-04-01'
  profile:
    location:
      city: Sydney
      country: Australia
    name: Jack
  tags:
  - user
  - new
- id: 5
  metadata:
    created: '2023-12-01'
    updated: '2024-02-15'
  profile:
    location:
      city: Berlin
      country: Germany
    name: Kate
  tags:
  - admin
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

## lists_of_primitives.json

Original size (JSON pretty): **610 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 610 | 382 | 280 | 217 | 217 | 274.0 | 2.23 |
| JSON (min) | 330 | 115 | 125 | 103 | 103 | 111.5 | 5.47 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 341 | 153 | 157 | 149 | 149 | 152.0 | 4.01 |
| minemizer | 194 | 81 | 79 | 71 | 71 | 75.5 | 8.08 |
| minemizer (compact) | 165 | 83 | 83 | 70 | 70 | 76.5 | 7.97 |

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
      "groovy"
    ]
  },
  {
    "id": 4,
    "name": "David",
    "skills": [
      "c",
      "cpp"
    ]
  },
  {
    "id": 5,
    "name": "Eva",
    "skills": [
      "ruby",
      "elixir",
      "erlang"
    ]
  },
  {
    "id": 6,
    "name": "Frank",
    "skills": [
      "swift"
    ]
  }
]
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
  skills:
  - ruby
  - elixir
  - erlang
- id: 6
  name: Frank
  skills:
  - swift
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

## nested_objects.json

Original size (JSON pretty): **741 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 741 | 407 | 322 | 252 | 252 | 308.2 | 2.40 |
| JSON (min) | 470 | 143 | 159 | 127 | 127 | 139.0 | 5.33 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 463 | 195 | 182 | 158 | 158 | 173.2 | 4.28 |
| minemizer | 259 | 90 | 95 | 77 | 77 | 84.8 | 8.74 |
| minemizer (compact) | 232 | 95 | 100 | 78 | 78 | 87.8 | 8.44 |

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
  {
    "id": 4,
    "user": {
      "name": "David",
      "email": "david@example.com"
    },
    "status": "pending"
  },
  {
    "id": 5,
    "user": {
      "name": "Eva",
      "email": "eva@example.com"
    },
    "status": "active"
  },
  {
    "id": 6,
    "user": {
      "name": "Frank",
      "email": "frank@example.com"
    },
    "status": "active"
  }
]
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
- id: 6
  status: active
  user:
    email: frank@example.com
    name: Frank
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

## simple_flat.json

Original size (JSON pretty): **763 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 763 | 384 | 334 | 264 | 264 | 311.5 | 2.45 |
| JSON (min) | 522 | 152 | 165 | 137 | 137 | 147.8 | 5.16 |
| CSV | 234 | 95 | 101 | 77 | 77 | 87.5 | 8.72 |
| TSV | 234 | 95 | 101 | 77 | 77 | 87.5 | 8.72 |
| YAML | 489 | 163 | 180 | 169 | 169 | 170.2 | 4.48 |
| minemizer | 251 | 74 | 83 | 72 | 72 | 75.2 | 10.14 |
| minemizer (compact) | 224 | 85 | 91 | 77 | 77 | 82.5 | 9.25 |

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
  {
    "id": 5,
    "name": "Eva",
    "role": "Analyst",
    "department": "Data"
  },
  {
    "id": 6,
    "name": "Frank",
    "role": "Engineer",
    "department": "Backend"
  },
  {
    "id": 7,
    "name": "Grace",
    "role": "Designer",
    "department": "Mobile"
  },
  {
    "id": 8,
    "name": "Henry",
    "role": "Manager",
    "department": "Engineering"
  }
]
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
  id: 7
  name: Grace
  role: Designer
- department: Engineering
  id: 8
  name: Henry
  role: Manager
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

## sparse_data.json

Original size (JSON pretty): **589 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | phi4 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 589 | 318 | 278 | 224 | 224 | 261.0 | 2.26 |
| JSON (min) | 378 | 121 | 133 | 114 | 114 | 120.5 | 4.89 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 356 | 135 | 150 | 143 | 143 | 142.8 | 4.13 |
| minemizer | 232 | 79 | 87 | 77 | 77 | 80.0 | 7.36 |
| minemizer (compact) | 207 | 84 | 90 | 77 | 77 | 82.0 | 7.18 |

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
    "role": "Engineer",
    "remote": true,
    "team": "Platform"
  },
  {
    "id": 6,
    "name": "Henry",
    "role": "Analyst"
  },
  {
    "id": 7,
    "name": "Ivy"
  },
  {
    "id": 8,
    "name": "Jack",
    "department": "Sales",
    "remote": false
  }
]
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
  name: Jack
  remote: false
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
