# Benchmark Results (Full Detail)

_Generated: 2025-12-01_

Tokenizers: gpt2, llama, qwen2.5, Deepseek-V3.2

## simple_flat.json

Original size (JSON pretty): **763 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 763 | 384 | 334 | 264 | 269 | 312.8 | 2.4 |
| JSON (min) | 522 | 152 | 165 | 137 | 149 | 150.8 | 5.1 |
| CSV | 234 | 95 | 101 | 77 | 90 | 90.8 | 8.4 |
| TSV | 234 | 95 | 101 | 77 | 91 | 91.0 | 8.4 |
| YAML | 489 | 163 | 180 | 169 | 171 | 170.8 | 4.5 |
| TOON | 246 | 98 | 103 | 96 | 92 | 97.2 | 7.8 |
| TSON | 229 | 90 | 95 | 80 | 85 | 87.5 | 8.7 |
| minemizer | 251 | 74 | 83 | 72 | 74 | 75.8 | 10.1 |
| minemizer (compact) | 224 | 85 | 91 | 77 | 82 | 83.8 | 9.1 |

### Serialized outputs

**JSON (pretty)** (763 chars, 313 tokens):
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

**JSON (min)** (522 chars, 151 tokens):
```json
[{"id":1,"name":"Alice","role":"Engineer","department":"Backend"},{"id":2,"name":"Bob","role":"Designer","department":"Frontend"},{"id":3,"name":"Carol","role":"Manager","department":"Product"},{"id":4,"name":"David","role":"Engineer","department":"Infrastructure"},{"id":5,"name":"Eva","role":"Analyst","department":"Data"},{"id":6,"name":"Frank","role":"Engineer","department":"Backend"},{"id":7,"name":"Grace","role":"Designer","department":"Mobile"},{"id":8,"name":"Henry","role":"Manager","department":"Engineering"}]
```

**CSV** (234 chars, 91 tokens):
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

**TSV** (234 chars, 91 tokens):
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

**YAML** (489 chars, 171 tokens):
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

**TOON** (246 chars, 97 tokens):
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

**TSON** (229 chars, 88 tokens):
```tson
{@id,name,role,department#8|1,Alice,Engineer,Backend|2,Bob,Designer,Frontend|3,Carol,Manager,Product|4,David,Engineer,Infrastructure|5,Eva,Analyst,Data|6,Frank,Engineer,Backend|7,Grace,Designer,Mobile|8,Henry,Manager,Engineering}
```

**minemizer** (251 chars, 76 tokens):
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

**minemizer (compact)** (224 chars, 84 tokens):
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

Original size (JSON pretty): **1039 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 1039 | 590 | 435 | 348 | 348 | 430.2 | 2.4 |
| JSON (min) | 618 | 188 | 211 | 174 | 186 | 189.8 | 5.5 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 629 | 264 | 246 | 229 | 227 | 241.5 | 4.3 |
| TOON | 675 | 315 | 238 | 223 | 223 | 249.8 | 4.2 |
| TSON | 306 | 136 | 141 | 110 | 123 | 127.5 | 8.1 |
| minemizer | 325 | 126 | 132 | 121 | 119 | 124.5 | 8.3 |
| minemizer (compact) | 290 | 132 | 139 | 117 | 118 | 126.5 | 8.2 |

### Serialized outputs

**JSON (pretty)** (1039 chars, 430 tokens):
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
... (truncated)
```

**JSON (min)** (618 chars, 190 tokens):
```json
[{"id":"u1","name":"Lukas","location":{"office":"Kaunas HQ","floor":12},"skills":["python","kubernetes"]},{"id":"u2","name":"Emma","location":{"office":"Boston Hub","floor":7},"skills":["react","typescript","graphql"]},{"id":"u3","name":"Pierre","location":{"office":"Paris Office","floor":3},"skills":["rust"]},{"id":"u4","name":"Hana","location":{"office":"Tokyo Tower","floor":15},"skills":["go","docker"]},{"id":"u5","name":"Wei","location":{"office":"Taipei Center","floor":8},"skills":["java","spring"]},{"id":"u6","name":"Charlotte","location":{"office":"London Bridge","floor":5},"skills":["python","django"]}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (629 chars, 242 tokens):
```yaml
- id: u1
  location:
    floor: 12
    office: Kaunas HQ
  name: Lukas
  skills:
  - python
  - kubernetes
- id: u2
  location:
    floor: 7
    office: Boston Hub
  name: Emma
  skills:
  - react
  - typescript
  - graphql
- id: u3
  location:
    floor: 3
    office: Paris Office
  name: Pierre
  skills:
  - rust
- id: u4
... (truncated)
```

**TOON** (675 chars, 250 tokens):
```toon
[6]:
  - id: u1
    name: Lukas
    location:
      office: Kaunas HQ
      floor: 12
    skills[2]: python,kubernetes
  - id: u2
    name: Emma
    location:
      office: Boston Hub
      floor: 7
    skills[3]: react,typescript,graphql
  - id: u3
    name: Pierre
    location:
      office: Paris Office
      floor: 3
    skills[1]: rust
  - id: u4
    name: Hana
    location:
      office: Tokyo Tower
      floor: 15
    skills[2]: go,docker
... (truncated)
```

**TSON** (306 chars, 128 tokens):
```tson
{@id,name,location(@office,floor),skills#6|u1,Lukas,{"Kaunas HQ",12},[python,kubernetes]|u2,Emma,{"Boston Hub",7},[react,typescript,graphql]|u3,Pierre,{"Paris Office",3},[rust]|u4,Hana,{"Tokyo Tower",15},[go,docker]|u5,Wei,{"Taipei Center",8},[java,spring]|u6,Charlotte,{"London Bridge",5},[python,django]}
```

**minemizer** (325 chars, 124 tokens):
```txt
id; name; location{ office; floor}; skills[]
u1; Lukas;{ Kaunas HQ; 12};[ python; kubernetes]
u2; Emma;{ Boston Hub; 7};[ react; typescript; graphql]
u3; Pierre;{ Paris Office; 3};[ rust]
u4; Hana;{ Tokyo Tower; 15};[ go; docker]
u5; Wei;{ Taipei Center; 8};[ java; spring]
u6; Charlotte;{ London Bridge; 5};[ python; django]
```

**minemizer (compact)** (290 chars, 126 tokens):
```txt
id;name;location{office;floor};skills[]
u1;Lukas;{Kaunas HQ;12};[python;kubernetes]
u2;Emma;{Boston Hub;7};[react;typescript;graphql]
u3;Pierre;{Paris Office;3};[rust]
u4;Hana;{Tokyo Tower;15};[go;docker]
u5;Wei;{Taipei Center;8};[java;spring]
u6;Charlotte;{London Bridge;5};[python;django]
```

---

## lists_of_primitives.json

Original size (JSON pretty): **610 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 610 | 382 | 280 | 217 | 222 | 275.2 | 2.2 |
| JSON (min) | 330 | 115 | 125 | 103 | 114 | 114.2 | 5.3 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 341 | 153 | 157 | 149 | 151 | 152.5 | 4.0 |
| TOON | 339 | 161 | 141 | 137 | 141 | 145.0 | 4.2 |
| TSON | 168 | 80 | 79 | 65 | 77 | 75.2 | 8.1 |
| minemizer | 188 | 81 | 79 | 71 | 67 | 74.5 | 8.2 |
| minemizer (compact) | 165 | 83 | 83 | 70 | 70 | 76.5 | 8.0 |

### Serialized outputs

**JSON (pretty)** (610 chars, 275 tokens):
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

**JSON (min)** (330 chars, 114 tokens):
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

**TOON** (339 chars, 145 tokens):
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

**TSON** (168 chars, 75 tokens):
```tson
{@id,name,skills#6|1,Alice,[python,go,rust]|2,Bob,[javascript,typescript]|3,Carol,[java,kotlin,scala,groovy]|4,David,[c,cpp]|5,Eva,[ruby,elixir,erlang]|6,Frank,[swift]}
```

**minemizer** (188 chars, 74 tokens):
```txt
id; name; skills[]
1; Alice;[ python; go; rust]
2; Bob;[ javascript; typescript]
3; Carol;[ java; kotlin; scala; groovy]
4; David;[ c; cpp]
5; Eva;[ ruby; elixir; erlang]
6; Frank;[ swift]
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

Original size (JSON pretty): **611 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 611 | 323 | 285 | 227 | 228 | 265.8 | 2.3 |
| JSON (min) | 400 | 131 | 146 | 121 | 125 | 130.8 | 4.7 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 384 | 145 | 158 | 149 | 149 | 150.2 | 4.1 |
| TOON | 438 | 190 | 167 | 159 | 159 | 168.8 | 3.6 |
| TSON | 328 | 146 | 145 | 113 | 116 | 130.0 | 4.7 |
| minemizer | 207 | 78 | 85 | 75 | 75 | 78.2 | 7.8 |
| minemizer (compact) | 184 | 85 | 91 | 74 | 76 | 81.5 | 7.5 |

### Serialized outputs

**JSON (pretty)** (611 chars, 266 tokens):
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
    "slack": "@kenji",
    "remote": false
  },
  {
    "id": 5,
... (truncated)
```

**JSON (min)** (400 chars, 131 tokens):
```json
[{"id":1,"name":"Erik","department":"Engineering"},{"id":2,"name":"Rachel","department":"Design","remote":true},{"id":3,"name":"Hans"},{"id":4,"name":"Kenji","department":"Sales","slack":"@kenji","remote":false},{"id":5,"name":"Mai","remote":true},{"id":6,"name":"Tom","department":"Engineering"},{"id":7,"name":"Priya","slack":"@priya","remote":true},{"id":8,"name":"Nina","department":"Marketing"}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (384 chars, 150 tokens):
```yaml
- department: Engineering
  id: 1
  name: Erik
- department: Design
  id: 2
  name: Rachel
  remote: true
- id: 3
  name: Hans
- department: Sales
  id: 4
  name: Kenji
  remote: false
  slack: '@kenji'
- id: 5
  name: Mai
  remote: true
- department: Engineering
  id: 6
  name: Tom
- id: 7
  name: Priya
  remote: true
  slack: '@priya'
- department: Marketing
... (truncated)
```

**TOON** (438 chars, 169 tokens):
```toon
[8]:
  - id: 1
    name: Erik
    department: Engineering
  - id: 2
    name: Rachel
    department: Design
    remote: true
  - id: 3
    name: Hans
  - id: 4
    name: Kenji
    department: Sales
    slack: @kenji
    remote: false
  - id: 5
    name: Mai
    remote: true
  - id: 6
    name: Tom
    department: Engineering
  - id: 7
    name: Priya
    slack: @priya
    remote: true
... (truncated)
```

**TSON** (328 chars, 130 tokens):
```tson
[{@id,name,department|1,Erik,Engineering},{@id,name,department,remote|2,Rachel,Design,true},{@id,name|3,Hans},{@id,name,department,slack,remote|4,Kenji,Sales,"@kenji",false},{@id,name,remote|5,Mai,true},{@id,name,department|6,Tom,Engineering},{@id,name,slack,remote|7,Priya,"@priya",true},{@id,name,department|8,Nina,Marketing}]
```

**minemizer** (207 chars, 78 tokens):
```txt
id; name; department; remote
1; Erik; Engineering; 
2; Rachel; Design;true
3; Hans;; 
4; Kenji; Sales;false; slack: @kenji
5; Mai;;true
6; Tom; Engineering; 
7; Priya;;true; slack: @priya
8; Nina; Marketing;
```

**minemizer (compact)** (184 chars, 82 tokens):
```txt
id;name;department;remote
1;Erik;Engineering;
2;Rachel;Design;true
3;Hans;;
4;Kenji;Sales;false;slack:@kenji
5;Mai;;true
6;Tom;Engineering;
7;Priya;;true;slack:@priya
8;Nina;Marketing;
```

---

## complex_mixed.json

Original size (JSON pretty): **1320 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 1320 | 768 | 560 | 455 | 427 | 552.5 | 2.4 |
| JSON (min) | 760 | 224 | 284 | 246 | 238 | 248.0 | 5.3 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 818 | 374 | 338 | 306 | 278 | 324.0 | 4.1 |
| TOON | 881 | 434 | 329 | 304 | 278 | 336.2 | 3.9 |
| TSON | 453 | 207 | 237 | 203 | 193 | 210.0 | 6.3 |
| minemizer | 403 | 157 | 203 | 193 | 160 | 178.2 | 7.4 |
| minemizer (compact) | 361 | 173 | 214 | 190 | 158 | 183.8 | 7.2 |

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

**JSON (min)** (760 chars, 248 tokens):
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

**TSON** (453 chars, 210 tokens):
```tson
{@id,profile(@name,location),tags,metadata#5|1,{Grace,{@city,country|NYC,USA}},[admin,verified],{@created|2024-01-15}|2,{Henry,{@city,country|London,UK}},[user],{@created,updated|2024-02-20,2024-03-10}|3,{Ivy,{@city,country|Tokyo,Japan}},[moderator,verified,premium],{@created|2024-01-05}|4,{Jack,{@city,country|Sydney,Australia}},[user,new],{@created|2024-04-01}|5,{Kate,{@city,country|Berlin,Germany}},[admin],{@created,updated|2023-12-01,2024-02-15}}
```

**minemizer** (403 chars, 178 tokens):
```txt
id; profile{ name; location{ city; country}}; tags[]; metadata{ created; ...}
1;{ Grace;{ NYC; USA}};[ admin; verified];{ 2024-01-15}
2;{ Henry;{ London; UK}};[ user];{ 2024-02-20; updated: 2024-03-10}
3;{ Ivy;{ Tokyo; Japan}};[ moderator; verified; premium];{ 2024-01-05}
4;{ Jack;{ Sydney; Australia}};[ user; new];{ 2024-04-01}
5;{ Kate;{ Berlin; Germany}};[ admin];{ 2023-12-01; updated: 2024-02-15}
```

**minemizer (compact)** (361 chars, 184 tokens):
```txt
id;profile{name;location{city;country}};tags[];metadata{created;...}
1;{Grace;{NYC;USA}};[admin;verified];{2024-01-15}
2;{Henry;{London;UK}};[user];{2024-02-20;updated:2024-03-10}
3;{Ivy;{Tokyo;Japan}};[moderator;verified;premium];{2024-01-05}
4;{Jack;{Sydney;Australia}};[user;new];{2024-04-01}
5;{Kate;{Berlin;Germany}};[admin];{2023-12-01;updated:2024-02-15}
```

---

## books.json

Original size (JSON pretty): **27902 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 27902 | 12188 | 11626 | 9434 | 8954 | 10550.5 | 2.6 |
| JSON (min) | 22501 | 7103 | 8035 | 6637 | 6165 | 6985.0 | 4.0 |
| CSV | 14071 | 5354 | 6151 | 4799 | 4462 | 5191.5 | 5.4 |
| TSV | 14057 | 5564 | 6360 | 4883 | 4679 | 5371.5 | 5.2 |
| YAML | 22400 | 8081 | 8859 | 7605 | 7158 | 7925.8 | 3.5 |
| TOON | 14277 | 5388 | 6172 | 4866 | 4434 | 5215.0 | 5.4 |
| TSON | 14448 | 5433 | 6229 | 4845 | 4483 | 5247.5 | 5.3 |
| minemizer | 14460 | 5154 | 6044 | 4976 | 4519 | 5173.2 | 5.4 |
| minemizer (compact) | 13755 | 5262 | 6058 | 4847 | 4386 | 5138.2 | 5.4 |

### Serialized outputs

**JSON (pretty)** (27902 chars, 10550 tokens):
```json
[
  {
    "author": "Chinua Achebe",
    "country": "Nigeria",
    "imageLink": "images/things-fall-apart.jpg",
    "language": "English",
    "link": "https://en.wikipedia.org/wiki/Things_Fall_Apart\n",
    "pages": 209,
    "title": "Things Fall Apart",
    "year": 1958
  },
  {
    "author": "Hans Christian Andersen",
    "country": "Denmark",
    "imageLink": "images/fairy-tales.jpg",
    "language": "Danish",
    "link": "https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.\n",
    "pages": 784,
    "title": "Fairy tales",
    "year": 1836
  },
  {
    "author": "Dante Alighieri",
    "country": "Italy",
    "imageLink": "images/the-divine-comedy.jpg",
... (truncated)
```

**JSON (min)** (22501 chars, 6985 tokens):
```json
[{"author":"Chinua Achebe","country":"Nigeria","imageLink":"images/things-fall-apart.jpg","language":"English","link":"https://en.wikipedia.org/wiki/Things_Fall_Apart\n","pages":209,"title":"Things Fall Apart","year":1958},{"author":"Hans Christian Andersen","country":"Denmark","imageLink":"images/fairy-tales.jpg","language":"Danish","link":"https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.\n","pages":784,"title":"Fairy tales","year":1836},{"author":"Dante Alighieri","country":"Italy","imageLink":"images/the-divine-comedy.jpg","language":"Italian","link":"https://en.wikipedia.org/wiki/Divine_Comedy\n","pages":928,"title":"The Divine Comedy","year":1315},{"author":"Unknown","country":"Sumer and Akkadian Empire","imageLink":"images/the-epic-of-gilgamesh.jpg","language":"Akkadian","link":"https://en.wikipedia.org/wiki/Epic_of_Gilgamesh\n","pages":160,"title":"The Epic Of Gilgamesh","year":-1700},{"author":"Unknown","country":"Achaemenid Empire","imageLink":"images/the-book-of-job.jpg","language":"Hebrew","link":"https://en.wikipedia.org/wiki/Book_of_Job\n","pages":176,"title":"The Book Of Job","year":-600},{"author":"Unknown","country":"India/Iran/Iraq/Egypt/Tajikistan","imageLink":"images/one-thousand-and-one-nights.jpg","language":"Arabic","link":"https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights\n","pages":288,"title":"One Thousand and One Nights","year":1200},{"author":"Unknown","country":"Iceland","imageLink":"images/njals-saga.jpg","language":"Old Norse","link":"https://en.wikipedia.org/wiki/Nj%C3%A1ls_saga\n","pages":384,"title":"Nj\u00e1l's Saga","year":1350},{"author":"Jane Austen","country":"United Kingdom","imageLink":"images/pride-and-prejudice.jpg","language":"English","link":"https://en.wikipedia.org/wiki/Pride_and_Prejudice\n","pages":226,"title":"Pride and Prejudice","year":1813},{"author":"Honor\u00e9 de Balzac","country":"France","imageLink":"images/le-pere-goriot.jpg","language":"French","link":"https://en.wikipedia.org/wiki/Le_P%C3%A8re_Goriot\n","pages":443,"title":"Le P\u00e8re Goriot","year":1835},{"author":"Samuel Beckett","country":"Republic of Ireland","imageLink":"images/molloy-malone-dies-the-unnamable.jpg","language":"French, English","link":"https://en.wikipedia.org/wiki/Molloy_(novel)\n","pages":256,"title":"Molloy, Malone Dies, The Unnamable, the trilogy","year":1952},{"author":"Giovanni Boccaccio","country":"Italy","imageLink":"images/the-decameron.jpg","language":"Italian","link":"https://en.wikipedia.org/wiki/The_Decameron\n","pages":1024,"title":"The Decameron","year":1351},{"author":"Jorge Luis Borges","country":"Argentina","imageLink":"images/ficciones.jpg","language":"Spanish","link":"https://en.wikipedia.org/wiki/Ficciones\n","pages":224,"title":"Ficciones","year":1965},{"author":"Emily Bront\u00eb","country":"United Kingdom","imageLink":"images/wuthering-heights.jpg","language":"English","link":"https://en.wikipedia.org/wiki/Wuthering_Heights\n","pages":342,"title":"Wuthering Heights","year":1847},{"author":"Albert Camus","country":"Algeria, French Empire","imageLink":"images/l-etranger.jpg","language":"French","link":"https://en.wikipedia.org/wiki/The_Stranger_(novel)\n","pages":185,"title":"The Stranger","year":1942},{"author":"Paul Celan","country":"Romania, France","imageLink":"images/poems-paul-celan.jpg","language":"German","link":"\n","pages":320,"title":"Poems","year":1952},{"author":"Louis-Ferdinand C\u00e9line","country":"France","imageLink":"images/voyage-au-bout-de-la-nuit.jpg","language":"French","link":"https://en.wikipedia.org/wiki/Journey_to_the_End_of_the_Night\n","pages":505,"title":"Journey to the End of the Night","year":1932},{"author":"Miguel de Cervantes","country":"Spain","imageLink":"images/don-quijote-de-la-mancha.jpg","language":"Spanish","link":"https://en.wikipedia.org/wiki/Don_Quixote\n","pages":1056,"title":"Don Quijote De La Mancha","year":1610},{"author":"Geoffrey Chaucer","country":"England","imageLink":"images/the-canterbury-tales.jpg","language":"English","link":"https://en.wikipedia.org/wiki/The_Canterbury_Tales\n","pages":544,"title":"The Canterbury Tales","year":1450},{"author":"Anton Chekhov","country":"Russia","imageLink":"images/stories-of-anton-chekhov.jpg","language":"Russian","link":"https://en.wikipedia.org/wiki/List_of_short_stories_by_Anton_Chekhov\n","pages":194,"title":"Stories","year":1886},{"author":"Joseph Conrad","country":"United Kingdom","imageLink":"images/nostromo.jpg","language":"English","link":"https://en.wikipedia.org/wiki/Nostromo\n","pages":320,"title":"Nostromo","year":1904},{"author":"Charles Dickens","country":"United Kingdom","imageLink":"images/great-expectations.jpg","language":"English","link":"https://en.wikipedia.org/wiki/Great_Expectations\n","pages":194,"title":"Great Expectations","year":1861},{"author":"Denis Diderot","country":"France","imageLink":"images/jacques-the-fatalist.jpg","language":"French","link":"https://en.wikipedia.org/wiki/Jacques_the_Fatalis
... (truncated)
```

**CSV** (14071 chars, 5192 tokens):
```csv
author,country,imageLink,language,link,pages,title,year
Chinua Achebe,Nigeria,images/things-fall-apart.jpg,English,"https://en.wikipedia.org/wiki/Things_Fall_Apart
",209,Things Fall Apart,1958
Hans Christian Andersen,Denmark,images/fairy-tales.jpg,Danish,"https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.
",784,Fairy tales,1836
Dante Alighieri,Italy,images/the-divine-comedy.jpg,Italian,"https://en.wikipedia.org/wiki/Divine_Comedy
",928,The Divine Comedy,1315
Unknown,Sumer and Akkadian Empire,images/the-epic-of-gilgamesh.jpg,Akkadian,"https://en.wikipedia.org/wiki/Epic_of_Gilgamesh
",160,The Epic Of Gilgamesh,-1700
Unknown,Achaemenid Empire,images/the-book-of-job.jpg,Hebrew,"https://en.wikipedia.org/wiki/Book_of_Job
",176,The Book Of Job,-600
Unknown,India/Iran/Iraq/Egypt/Tajikistan,images/one-thousand-and-one-nights.jpg,Arabic,"https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights
",288,One Thousand and One Nights,1200
Unknown,Iceland,images/njals-saga.jpg,Old Norse,"https://en.wikipedia.org/wiki/Nj%C3%A1ls_saga
",384,Njál's Saga,1350
Jane Austen,United Kingdom,images/pride-and-prejudice.jpg,English,"https://en.wikipedia.org/wiki/Pride_and_Prejudice
",226,Pride and Prejudice,1813
Honoré de Balzac,France,images/le-pere-goriot.jpg,French,"https://en.wikipedia.org/wiki/Le_P%C3%A8re_Goriot
",443,Le Père Goriot,1835
Samuel Beckett,Republic of Ireland,images/molloy-malone-dies-the-unnamable.jpg,"French, English","https://en.wikipedia.org/wiki/Molloy_(novel)
",256,"Molloy, Malone Dies, The Unnamable, the trilogy",1952
Giovanni Boccaccio,Italy,images/the-decameron.jpg,Italian,"https://en.wikipedia.org/wiki/The_Decameron
",1024,The Decameron,1351
Jorge Luis Borges,Argentina,images/ficciones.jpg,Spanish,"https://en.wikipedia.org/wiki/Ficciones
",224,Ficciones,1965
... (truncated)
```

**TSV** (14057 chars, 5372 tokens):
```tsv
author	country	imageLink	language	link	pages	title	year
Chinua Achebe	Nigeria	images/things-fall-apart.jpg	English	"https://en.wikipedia.org/wiki/Things_Fall_Apart
"	209	Things Fall Apart	1958
Hans Christian Andersen	Denmark	images/fairy-tales.jpg	Danish	"https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.
"	784	Fairy tales	1836
Dante Alighieri	Italy	images/the-divine-comedy.jpg	Italian	"https://en.wikipedia.org/wiki/Divine_Comedy
"	928	The Divine Comedy	1315
Unknown	Sumer and Akkadian Empire	images/the-epic-of-gilgamesh.jpg	Akkadian	"https://en.wikipedia.org/wiki/Epic_of_Gilgamesh
"	160	The Epic Of Gilgamesh	-1700
Unknown	Achaemenid Empire	images/the-book-of-job.jpg	Hebrew	"https://en.wikipedia.org/wiki/Book_of_Job
"	176	The Book Of Job	-600
Unknown	India/Iran/Iraq/Egypt/Tajikistan	images/one-thousand-and-one-nights.jpg	Arabic	"https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights
"	288	One Thousand and One Nights	1200
Unknown	Iceland	images/njals-saga.jpg	Old Norse	"https://en.wikipedia.org/wiki/Nj%C3%A1ls_saga
"	384	Njál's Saga	1350
Jane Austen	United Kingdom	images/pride-and-prejudice.jpg	English	"https://en.wikipedia.org/wiki/Pride_and_Prejudice
"	226	Pride and Prejudice	1813
Honoré de Balzac	France	images/le-pere-goriot.jpg	French	"https://en.wikipedia.org/wiki/Le_P%C3%A8re_Goriot
"	443	Le Père Goriot	1835
Samuel Beckett	Republic of Ireland	images/molloy-malone-dies-the-unnamable.jpg	French, English	"https://en.wikipedia.org/wiki/Molloy_(novel)
"	256	Molloy, Malone Dies, The Unnamable, the trilogy	1952
Giovanni Boccaccio	Italy	images/the-decameron.jpg	Italian	"https://en.wikipedia.org/wiki/The_Decameron
"	1024	The Decameron	1351
Jorge Luis Borges	Argentina	images/ficciones.jpg	Spanish	"https://en.wikipedia.org/wiki/Ficciones
"	224	Ficciones	1965
... (truncated)
```

**YAML** (22400 chars, 7926 tokens):
```yaml
- author: Chinua Achebe
  country: Nigeria
  imageLink: images/things-fall-apart.jpg
  language: English
  link: 'https://en.wikipedia.org/wiki/Things_Fall_Apart

    '
  pages: 209
  title: Things Fall Apart
  year: 1958
- author: Hans Christian Andersen
  country: Denmark
  imageLink: images/fairy-tales.jpg
  language: Danish
  link: 'https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.

    '
  pages: 784
  title: Fairy tales
  year: 1836
- author: Dante Alighieri
  country: Italy
  imageLink: images/the-divine-comedy.jpg
  language: Italian
  link: 'https://en.wikipedia.org/wiki/Divine_Comedy
... (truncated)
```

**TOON** (14277 chars, 5215 tokens):
```toon
[100]{author,country,imageLink,language,link,pages,title,year}:
  Chinua Achebe,Nigeria,images/things-fall-apart.jpg,English,"https://en.wikipedia.org/wiki/Things_Fall_Apart\n",209,Things Fall Apart,1958
  Hans Christian Andersen,Denmark,images/fairy-tales.jpg,Danish,"https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.\n",784,Fairy tales,1836
  Dante Alighieri,Italy,images/the-divine-comedy.jpg,Italian,"https://en.wikipedia.org/wiki/Divine_Comedy\n",928,The Divine Comedy,1315
  Unknown,Sumer and Akkadian Empire,images/the-epic-of-gilgamesh.jpg,Akkadian,"https://en.wikipedia.org/wiki/Epic_of_Gilgamesh\n",160,The Epic Of Gilgamesh,-1700
  Unknown,Achaemenid Empire,images/the-book-of-job.jpg,Hebrew,"https://en.wikipedia.org/wiki/Book_of_Job\n",176,The Book Of Job,-600
  Unknown,India/Iran/Iraq/Egypt/Tajikistan,images/one-thousand-and-one-nights.jpg,Arabic,"https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights\n",288,One Thousand and One Nights,1200
  Unknown,Iceland,images/njals-saga.jpg,Old Norse,"https://en.wikipedia.org/wiki/Nj%C3%A1ls_saga\n",384,Njál's Saga,1350
  Jane Austen,United Kingdom,images/pride-and-prejudice.jpg,English,"https://en.wikipedia.org/wiki/Pride_and_Prejudice\n",226,Pride and Prejudice,1813
  Honoré de Balzac,France,images/le-pere-goriot.jpg,French,"https://en.wikipedia.org/wiki/Le_P%C3%A8re_Goriot\n",443,Le Père Goriot,1835
  Samuel Beckett,Republic of Ireland,images/molloy-malone-dies-the-unnamable.jpg,"French, English","https://en.wikipedia.org/wiki/Molloy_(novel)\n",256,"Molloy, Malone Dies, The Unnamable, the trilogy",1952
  Giovanni Boccaccio,Italy,images/the-decameron.jpg,Italian,"https://en.wikipedia.org/wiki/The_Decameron\n",1024,The Decameron,1351
  Jorge Luis Borges,Argentina,images/ficciones.jpg,Spanish,"https://en.wikipedia.org/wiki/Ficciones\n",224,Ficciones,1965
  Emily Brontë,United Kingdom,images/wuthering-heights.jpg,English,"https://en.wikipedia.org/wiki/Wuthering_Heights\n",342,Wuthering Heights,1847
  Albert Camus,"Algeria, French Empire",images/l-etranger.jpg,French,"https://en.wikipedia.org/wiki/The_Stranger_(novel)\n",185,The Stranger,1942
  Paul Celan,"Romania, France",images/poems-paul-celan.jpg,German,"\n",320,Poems,1952
  Louis-Ferdinand Céline,France,images/voyage-au-bout-de-la-nuit.jpg,French,"https://en.wikipedia.org/wiki/Journey_to_the_End_of_the_Night\n",505,Journey to the End of the Night,1932
  Miguel de Cervantes,Spain,images/don-quijote-de-la-mancha.jpg,Spanish,"https://en.wikipedia.org/wiki/Don_Quixote\n",1056,Don Quijote De La Mancha,1610
  Geoffrey Chaucer,England,images/the-canterbury-tales.jpg,English,"https://en.wikipedia.org/wiki/The_Canterbury_Tales\n",544,The Canterbury Tales,1450
  Anton Chekhov,Russia,images/stories-of-anton-chekhov.jpg,Russian,"https://en.wikipedia.org/wiki/List_of_short_stories_by_Anton_Chekhov\n",194,Stories,1886
  Joseph Conrad,United Kingdom,images/nostromo.jpg,English,"https://en.wikipedia.org/wiki/Nostromo\n",320,Nostromo,1904
  Charles Dickens,United Kingdom,images/great-expectations.jpg,English,"https://en.wikipedia.org/wiki/Great_Expectations\n",194,Great Expectations,1861
  Denis Diderot,France,images/jacques-the-fatalist.jpg,French,"https://en.wikipedia.org/wiki/Jacques_the_Fatalist\n",596,Jacques the Fatalist,1796
  Alfred Döblin,Germany,images/berlin-alexanderplatz.jpg,German,"https://en.wikipedia.org/wiki/Berlin_Alexanderplatz\n",600,Berlin Alexanderplatz,1929
  Fyodor Dostoevsky,Russia,images/crime-and-punishment.jpg,Russian,"https://en.wikipedia.org/wiki/Crime_and_Punishment\n",551,Crime and Punishment,1866
... (truncated)
```

**TSON** (14448 chars, 5248 tokens):
```tson
{@author,country,imageLink,language,link,pages,title,year#100|"Chinua Achebe",Nigeria,images/things-fall-apart.jpg,English,"https://en.wikipedia.org/wiki/Things_Fall_Apart\n",209,"Things Fall Apart",1958|"Hans Christian Andersen",Denmark,images/fairy-tales.jpg,Danish,"https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.\n",784,"Fairy tales",1836|"Dante Alighieri",Italy,images/the-divine-comedy.jpg,Italian,"https://en.wikipedia.org/wiki/Divine_Comedy\n",928,"The Divine Comedy",1315|Unknown,"Sumer and Akkadian Empire",images/the-epic-of-gilgamesh.jpg,Akkadian,"https://en.wikipedia.org/wiki/Epic_of_Gilgamesh\n",160,"The Epic Of Gilgamesh",-1700|Unknown,"Achaemenid Empire",images/the-book-of-job.jpg,Hebrew,"https://en.wikipedia.org/wiki/Book_of_Job\n",176,"The Book Of Job",-600|Unknown,India/Iran/Iraq/Egypt/Tajikistan,images/one-thousand-and-one-nights.jpg,Arabic,"https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights\n",288,"One Thousand and One Nights",1200|Unknown,Iceland,images/njals-saga.jpg,"Old Norse","https://en.wikipedia.org/wiki/Nj%C3%A1ls_saga\n",384,"Njál's Saga",1350|"Jane Austen","United Kingdom",images/pride-and-prejudice.jpg,English,"https://en.wikipedia.org/wiki/Pride_and_Prejudice\n",226,"Pride and Prejudice",1813|"Honoré de Balzac",France,images/le-pere-goriot.jpg,French,"https://en.wikipedia.org/wiki/Le_P%C3%A8re_Goriot\n",443,"Le Père Goriot",1835|"Samuel Beckett","Republic of Ireland",images/molloy-malone-dies-the-unnamable.jpg,"French, English","https://en.wikipedia.org/wiki/Molloy_(novel)\n",256,"Molloy, Malone Dies, The Unnamable, the trilogy",1952|"Giovanni Boccaccio",Italy,images/the-decameron.jpg,Italian,"https://en.wikipedia.org/wiki/The_Decameron\n",1024,"The Decameron",1351|"Jorge Luis Borges",Argentina,images/ficciones.jpg,Spanish,"https://en.wikipedia.org/wiki/Ficciones\n",224,Ficciones,1965|"Emily Brontë","United Kingdom",images/wuthering-heights.jpg,English,"https://en.wikipedia.org/wiki/Wuthering_Heights\n",342,"Wuthering Heights",1847|"Albert Camus","Algeria, French Empire",images/l-etranger.jpg,French,"https://en.wikipedia.org/wiki/The_Stranger_(novel)\n",185,"The Stranger",1942|"Paul Celan","Romania, France",images/poems-paul-celan.jpg,German,"\n",320,Poems,1952|"Louis-Ferdinand Céline",France,images/voyage-au-bout-de-la-nuit.jpg,French,"https://en.wikipedia.org/wiki/Journey_to_the_End_of_the_Night\n",505,"Journey to the End of the Night",1932|"Miguel de Cervantes",Spain,images/don-quijote-de-la-mancha.jpg,Spanish,"https://en.wikipedia.org/wiki/Don_Quixote\n",1056,"Don Quijote De La Mancha",1610|"Geoffrey Chaucer",England,images/the-canterbury-tales.jpg,English,"https://en.wikipedia.org/wiki/The_Canterbury_Tales\n",544,"The Canterbury Tales",1450|"Anton Chekhov",Russia,images/stories-of-anton-chekhov.jpg,Russian,"https://en.wikipedia.org/wiki/List_of_short_stories_by_Anton_Chekhov\n",194,Stories,1886|"Joseph Conrad","United Kingdom",images/nostromo.jpg,English,"https://en.wikipedia.org/wiki/Nostromo\n",320,Nostromo,1904|"Charles Dickens","United Kingdom",images/great-expectations.jpg,English,"https://en.wikipedia.org/wiki/Great_Expectations\n",194,"Great Expectations",1861|"Denis Diderot",France,images/jacques-the-fatalist.jpg,French,"https://en.wikipedia.org/wiki/Jacques_the_Fatalist\n",596,"Jacques the Fatalist",1796|"Alfred Döblin",Germany,images/berlin-alexanderplatz.jpg,German,"https://en.wikipedia.org/wiki/Berlin_Alexanderplatz\n",600,"Berlin Alexanderplatz",1929|"Fyodor Dostoevsky",Russia,images/crime-and-punishment.jpg,Russian,"https://en.wikipedia.org/wiki/Crime_and_Punishment\n",551,"Crime and Punishment",1866|"Fyodor Dostoevsky",Russia,images/the-idiot.jpg,Russian,"https://en.wikipedia.org/wiki/The_Idiot\n",656,"The Idiot",1869|"Fyodor Dostoevsky",Russia,images/the-possessed.jpg,Russian,"https://en.wikipedia.org/wiki/Demons_(Dostoyevsky_novel)\n",768,"The Possessed",1872|"Fyodor Dostoevsky",Russia,images/the-brothers-karamazov.jpg,Russian,"https://en.wikipedia.org/wiki/The_Brothers_Karamazov\n",824,"The Brothers Karamazov",1880|"George Eliot","United Kingdom",images/middlemarch.jpg,English,"https://en.wikipedia.org/wiki/Middlemarch\n",800,Middlemarch,1871|"Ralph Ellison","United States",images/invisible-man.jpg,English,"https://en.wikipedia.org/wiki/Invisible_Man\n",581,"Invisible Man",1952|Euripides,Greece,images/medea.jpg,Greek,"https://en.wikipedia.org/wiki/Medea_(play)\n",104,Medea,-431|"William Faulkner","United States",images/absalom-absalom.jpg,English,"https://en.wikipedia.org/wiki/Absalom,_Absalom!\n",313,"Absalom, Absalom!",1936|"William Faulkner","United States",images/the-sound-and-the-fury.jpg,English,"https://en.wikipedia.org/wiki/The_Sound_and_the_Fury\n",326,"The Sound and the Fury",1929|"Gustave Flaubert",France,images/madame-bovary.jpg,French,"https://en.wikipedia.org/wiki/Madame_Bovary\n",528,"Madame Bovary",1857|"Gustave Flaubert",France,images/l-education-sentimentale.jpg,French,"https://en.wikipedia.org/wiki/Sen
... (truncated)
```

**minemizer** (14460 chars, 5173 tokens):
```txt
author; country; imageLink; language; link; pages; title; year
Chinua Achebe; Nigeria; images/things-fall-apart.jpg; English; https://en.wikipedia.org/wiki/Things_Fall_Apart
; 209; Things Fall Apart; 1958
Hans Christian Andersen; Denmark; images/fairy-tales.jpg; Danish; https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.
; 784; Fairy tales; 1836
Dante Alighieri; Italy; images/the-divine-comedy.jpg; Italian; https://en.wikipedia.org/wiki/Divine_Comedy
; 928; The Divine Comedy; 1315
Unknown; Sumer and Akkadian Empire; images/the-epic-of-gilgamesh.jpg; Akkadian; https://en.wikipedia.org/wiki/Epic_of_Gilgamesh
; 160; The Epic Of Gilgamesh; -1700
Unknown; Achaemenid Empire; images/the-book-of-job.jpg; Hebrew; https://en.wikipedia.org/wiki/Book_of_Job
; 176; The Book Of Job; -600
Unknown; India/Iran/Iraq/Egypt/Tajikistan; images/one-thousand-and-one-nights.jpg; Arabic; https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights
; 288; One Thousand and One Nights; 1200
Unknown; Iceland; images/njals-saga.jpg; Old Norse; https://en.wikipedia.org/wiki/Nj%C3%A1ls_saga
; 384; Njál's Saga; 1350
Jane Austen; United Kingdom; images/pride-and-prejudice.jpg; English; https://en.wikipedia.org/wiki/Pride_and_Prejudice
; 226; Pride and Prejudice; 1813
Honoré de Balzac; France; images/le-pere-goriot.jpg; French; https://en.wikipedia.org/wiki/Le_P%C3%A8re_Goriot
; 443; Le Père Goriot; 1835
Samuel Beckett; Republic of Ireland; images/molloy-malone-dies-the-unnamable.jpg; French, English; https://en.wikipedia.org/wiki/Molloy_(novel)
; 256; Molloy, Malone Dies, The Unnamable, the trilogy; 1952
Giovanni Boccaccio; Italy; images/the-decameron.jpg; Italian; https://en.wikipedia.org/wiki/The_Decameron
; 1024; The Decameron; 1351
Jorge Luis Borges; Argentina; images/ficciones.jpg; Spanish; https://en.wikipedia.org/wiki/Ficciones
; 224; Ficciones; 1965
... (truncated)
```

**minemizer (compact)** (13755 chars, 5138 tokens):
```txt
author;country;imageLink;language;link;pages;title;year
Chinua Achebe;Nigeria;images/things-fall-apart.jpg;English;https://en.wikipedia.org/wiki/Things_Fall_Apart
;209;Things Fall Apart;1958
Hans Christian Andersen;Denmark;images/fairy-tales.jpg;Danish;https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.
;784;Fairy tales;1836
Dante Alighieri;Italy;images/the-divine-comedy.jpg;Italian;https://en.wikipedia.org/wiki/Divine_Comedy
;928;The Divine Comedy;1315
Unknown;Sumer and Akkadian Empire;images/the-epic-of-gilgamesh.jpg;Akkadian;https://en.wikipedia.org/wiki/Epic_of_Gilgamesh
;160;The Epic Of Gilgamesh;-1700
Unknown;Achaemenid Empire;images/the-book-of-job.jpg;Hebrew;https://en.wikipedia.org/wiki/Book_of_Job
;176;The Book Of Job;-600
Unknown;India/Iran/Iraq/Egypt/Tajikistan;images/one-thousand-and-one-nights.jpg;Arabic;https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights
;288;One Thousand and One Nights;1200
Unknown;Iceland;images/njals-saga.jpg;Old Norse;https://en.wikipedia.org/wiki/Nj%C3%A1ls_saga
;384;Njál's Saga;1350
Jane Austen;United Kingdom;images/pride-and-prejudice.jpg;English;https://en.wikipedia.org/wiki/Pride_and_Prejudice
;226;Pride and Prejudice;1813
Honoré de Balzac;France;images/le-pere-goriot.jpg;French;https://en.wikipedia.org/wiki/Le_P%C3%A8re_Goriot
;443;Le Père Goriot;1835
Samuel Beckett;Republic of Ireland;images/molloy-malone-dies-the-unnamable.jpg;French, English;https://en.wikipedia.org/wiki/Molloy_(novel)
;256;Molloy, Malone Dies, The Unnamable, the trilogy;1952
Giovanni Boccaccio;Italy;images/the-decameron.jpg;Italian;https://en.wikipedia.org/wiki/The_Decameron
;1024;The Decameron;1351
Jorge Luis Borges;Argentina;images/ficciones.jpg;Spanish;https://en.wikipedia.org/wiki/Ficciones
;224;Ficciones;1965
... (truncated)
```

---

## countries.json

Original size (JSON pretty): **1133948 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 1133948 | 677260 | 565880 | 474014 | 402625 | 529944.8 | 2.1 |
| JSON (min) | 787962 | 339487 | 425660 | 365037 | 304092 | 358569.0 | 3.2 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 641939 | 345580 | 251610 | 219269 | 206630 | 255772.2 | 4.4 |
| TOON | 691140 | 397301 | 246360 | 215450 | 202874 | 265496.2 | 4.3 |
| TSON | 423383 | 210056 | 196499 | 158349 | 158553 | 180864.2 | 6.3 |
| minemizer | 323130 | 166573 | 152369 | 133672 | 120114 | 143182.0 | 7.9 |
| minemizer (compact) | 299485 | 170841 | 156354 | 133597 | 124199 | 146247.8 | 7.8 |

### Serialized outputs

**JSON (pretty)** (1133948 chars, 529945 tokens):
```json
[
  {
    "name": {
      "common": "Aruba",
      "official": "Aruba",
      "native": {
        "nld": {
          "official": "Aruba",
          "common": "Aruba"
        },
        "pap": {
          "official": "Aruba",
          "common": "Aruba"
        }
      }
    },
    "tld": [
      ".aw"
    ],
    "cca2": "AW",
    "ccn3": "533",
    "cca3": "ABW",
    "cioc": "ARU",
    "independent": false,
    "status": "officially-assigned",
... (truncated)
```

**JSON (min)** (787962 chars, 358569 tokens):
```json
[{"name":{"common":"Aruba","official":"Aruba","native":{"nld":{"official":"Aruba","common":"Aruba"},"pap":{"official":"Aruba","common":"Aruba"}}},"tld":[".aw"],"cca2":"AW","ccn3":"533","cca3":"ABW","cioc":"ARU","independent":false,"status":"officially-assigned","unMember":false,"unRegionalGroup":"","currencies":{"AWG":{"name":"Aruban florin","symbol":"\u0192"}},"idd":{"root":"+2","suffixes":["97"]},"capital":["Oranjestad"],"altSpellings":["AW"],"region":"Americas","subregion":"Caribbean","languages":{"nld":"Dutch","pap":"Papiamento"},"translations":{"ara":{"official":"\u0623\u0631\u0648\u0628\u0627","common":"\u0623\u0631\u0648\u0628\u0627"},"bre":{"official":"Aruba","common":"Aruba"},"ces":{"official":"Aruba","common":"Aruba"},"deu":{"official":"Aruba","common":"Aruba"},"est":{"official":"Aruba","common":"Aruba"},"fin":{"official":"Aruba","common":"Aruba"},"fra":{"official":"Aruba","common":"Aruba"},"hrv":{"official":"Aruba","common":"Aruba"},"hun":{"official":"Aruba","common":"Aruba"},"ita":{"official":"Aruba","common":"Aruba"},"jpn":{"official":"\u30a2\u30eb\u30d0","common":"\u30a2\u30eb\u30d0"},"kor":{"official":"\uc544\ub8e8\ubc14","common":"\uc544\ub8e8\ubc14"},"nld":{"official":"Aruba","common":"Aruba"},"per":{"official":"\u0622\u0631\u0648\u0628\u0627","common":"\u0622\u0631\u0648\u0628\u0627"},"pol":{"official":"Aruba","common":"Aruba"},"por":{"official":"Aruba","common":"Aruba"},"rus":{"official":"\u0410\u0440\u0443\u0431\u0430","common":"\u0410\u0440\u0443\u0431\u0430"},"slk":{"official":"Aruba","common":"Aruba"},"spa":{"official":"Aruba","common":"Aruba"},"srp":{"official":"Aruba","common":"Aruba"},"swe":{"official":"Aruba","common":"Aruba"},"tur":{"official":"Aruba","common":"Aruba"},"urd":{"official":"\u0627\u0631\u0648\u0628\u0627","common":"\u0627\u0631\u0648\u0628\u0627"},"zho":{"official":"\u963f\u9c81\u5df4","common":"\u963f\u9c81\u5df4"}},"latlng":[12.5,-69.96666666],"landlocked":false,"borders":[],"area":180,"flag":"\ud83c\udde6\ud83c\uddfc","demonyms":{"eng":{"f":"Aruban","m":"Aruban"},"fra":{"f":"Arubaise","m":"Arubais"}}},{"name":{"common":"Afghanistan","official":"Islamic Republic of Afghanistan","native":{"prs":{"official":"\u062c\u0645\u0647\u0648\u0631\u06cc \u0627\u0633\u0644\u0627\u0645\u06cc \u0627\u0641\u063a\u0627\u0646\u0633\u062a\u0627\u0646","common":"\u0627\u0641\u063a\u0627\u0646\u0633\u062a\u0627\u0646"},"pus":{"official":"\u062f \u0627\u0641\u063a\u0627\u0646\u0633\u062a\u0627\u0646 \u0627\u0633\u0644\u0627\u0645\u064a \u062c\u0645\u0647\u0648\u0631\u06cc\u062a","common":"\u0627\u0641\u063a\u0627\u0646\u0633\u062a\u0627\u0646"},"tuk":{"official":"Owganystan Yslam Respublikasy","common":"Owganystan"}}},"tld":[".af"],"cca2":"AF","ccn3":"004","cca3":"AFG","cioc":"AFG","independent":true,"status":"officially-assigned","unMember":true,"unRegionalGroup":"Asia and the Pacific Group","currencies":{"AFN":{"name":"Afghan afghani","symbol":"\u060b"}},"idd":{"root":"+9","suffixes":["3"]},"capital":["Kabul"],"altSpellings":["AF","Af\u0121\u0101nist\u0101n"],"region":"Asia","subregion":"Southern Asia","languages":{"prs":"Dari","pus":"Pashto","tuk":"Turkmen"},"translations":{"ara":{"official":"\u062c\u0645\u0647\u0648\u0631\u064a\u0629 \u0623\u0641\u0641\u0627\u0646\u0633\u062a\u0627\u0646 \u0627\u0644\u0625\u0633\u0644\u0627\u0645\u064a\u0629","common":"\u0623\u0641\u063a\u0627\u0646\u0633\u062a\u0627\u0646"},"bre":{"official":"Republik Islamek Afghanistan","common":"Afghanistan"},"ces":{"official":"Afgh\u00e1nsk\u00e1 isl\u00e1msk\u00e1 republika","common":"Afgh\u00e1nist\u00e1n"},"deu":{"official":"Islamische Republik Afghanistan","common":"Afghanistan"},"est":{"official":"Afganistani Islamivabariik","common":"Afganistan"},"fin":{"official":"Afganistanin islamilainen tasavalta","common":"Afganistan"},"fra":{"official":"R\u00e9publique islamique d'Afghanistan","common":"Afghanistan"},"hrv":{"official":"Islamska Republika Afganistan","common":"Afganistan"},"hun":{"official":"Afganiszt\u00e1ni Iszl\u00e1m K\u00f6zt\u00e1rsas\u00e1g","common":"Afganiszt\u00e1n"},"ita":{"official":"Repubblica islamica dell'Afghanistan","common":"Afghanistan"},"jpn":{"official":"\u30a2\u30d5\u30ac\u30cb\u30b9\u30bf\u30f3\u30fb\u30a4\u30b9\u30e9\u30e0\u5171\u548c\u56fd","common":"\u30a2\u30d5\u30ac\u30cb\u30b9\u30bf\u30f3"},"kor":{"official":"\uc544\ud504\uac00\ub2c8\uc2a4\ud0c4 \uc774\uc2ac\ub78c \uacf5\ud654\uad6d","common":"\uc544\ud504\uac00\ub2c8\uc2a4\ud0c4"},"nld":{"official":"Islamitische Republiek Afghanistan","common":"Afghanistan"},"per":{"official":"\u062c\u0645\u0647\u0648\u0631\u06cc \u0627\u0633\u0644\u0627\u0645\u06cc \u0627\u0641\u063a\u0627\u0646\u0633\u062a\u0627\u0646","common":"\u0627\u0641\u063a\u0627\u0646\u0633\u062a\u0627\u0646"},"pol":{"official":"Islamska Republika Afganistanu","common":"Afganistan"},"por":{"official":"Rep\u00fablica Isl\u00e2mica do Afeganist\u00e3o","common":"Afeganist\u00e3o"},"rus":{"official":"\u0418\u0441\u043b\u0430\u043c\u0441\u043a\u0430\u044f \u0420\
... (truncated)
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (641939 chars, 255772 tokens):
```yaml
- altSpellings:
  - AW
  area: 180
  borders: []
  capital:
  - Oranjestad
  cca2: AW
  cca3: ABW
  ccn3: '533'
  cioc: ARU
  currencies:
    AWG:
      name: Aruban florin
      symbol: ƒ
  demonyms:
    eng:
      f: Aruban
      m: Aruban
    fra:
      f: Arubaise
      m: Arubais
  flag: 🇦🇼
  idd:
    root: '+2'
    suffixes:
... (truncated)
```

**TOON** (691140 chars, 265496 tokens):
```toon
[250]:
  -
    name:
      common: Aruba
      official: Aruba
      native:
        nld:
          official: Aruba
          common: Aruba
        pap:
          official: Aruba
          common: Aruba
    tld[1]: .aw
    cca2: AW
    ccn3: "533"
    cca3: ABW
    cioc: ARU
    independent: false
    status: officially-assigned
    unMember: false
    unRegionalGroup: ""
    currencies:
      AWG:
        name: Aruban florin
        symbol: ƒ
... (truncated)
```

**TSON** (423383 chars, 180864 tokens):
```tson
{@name(@common,official,native),tld,cca2,ccn3,cca3,cioc,independent,status,unMember,unRegionalGroup,currencies,idd(@root,suffixes),capital,altSpellings,region,subregion,languages,translations(@ara,bre,ces,deu,est,fin,fra,hrv,hun,ita,jpn,kor,nld,per,pol,por,rus,slk,spa,srp,swe,tur,urd,zho),latlng,landlocked,borders,area,flag,demonyms(@eng,fra)#250|{Aruba,Aruba,{@nld,pap|{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba}}},[.aw],AW,"533",ABW,ARU,false,officially-assigned,false,"",{@AWG|{@name,symbol|"Aruban florin",ƒ}},{"+2",["97"]},[Oranjestad],[AW],Americas,Caribbean,{@nld,pap|Dutch,Papiamento},{{@official,common|أروبا,أروبا},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|アルバ,アルバ},{@official,common|아루바,아루바},{@official,common|Aruba,Aruba},{@official,common|آروبا,آروبا},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Аруба,Аруба},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|Aruba,Aruba},{@official,common|اروبا,اروبا},{@official,common|阿鲁巴,阿鲁巴}},[12.5,-69.96666666],false,[],180,🇦🇼,{{@f,m|Aruban,Aruban},{@f,m|Arubaise,Arubais}}|{Afghanistan,"Islamic Republic of Afghanistan",{@prs,pus,tuk|{@official,common|"جمهوری اسلامی افغانستان",افغانستان},{@official,common|"د افغانستان اسلامي جمهوریت",افغانستان},{@official,common|"Owganystan Yslam Respublikasy",Owganystan}}},[.af],AF,"004",AFG,AFG,true,officially-assigned,true,"Asia and the Pacific Group",{@AFN|{@name,symbol|"Afghan afghani",؋}},{"+9",["3"]},[Kabul],[AF,Afġānistān],Asia,"Southern Asia",{@prs,pus,tuk|Dari,Pashto,Turkmen},{{@official,common|"جمهورية أففانستان الإسلامية",أفغانستان},{@official,common|"Republik Islamek Afghanistan",Afghanistan},{@official,common|"Afghánská islámská republika",Afghánistán},{@official,common|"Islamische Republik Afghanistan",Afghanistan},{@official,common|"Afganistani Islamivabariik",Afganistan},{@official,common|"Afganistanin islamilainen tasavalta",Afganistan},{@official,common|"République islamique d'Afghanistan",Afghanistan},{@official,common|"Islamska Republika Afganistan",Afganistan},{@official,common|"Afganisztáni Iszlám Köztársaság",Afganisztán},{@official,common|"Repubblica islamica dell'Afghanistan",Afghanistan},{@official,common|アフガニスタン・イスラム共和国,アフガニスタン},{@official,common|"아프가니스탄 이슬람 공화국",아프가니스탄},{@official,common|"Islamitische Republiek Afghanistan",Afghanistan},{@official,common|"جمهوری اسلامی افغانستان",افغانستان},{@official,common|"Islamska Republika Afganistanu",Afganistan},{@official,common|"República Islâmica do Afeganistão",Afeganistão},{@official,common|"Исламская Республика Афганистан",Афганистан},{@official,common|"Afgánsky islamský štát",Afganistan},{@official,common|"República Islámica de Afganistán",Afganistán},{@official,common|"Islamska Republika Avganistan",Avganistan},{@official,common|"Islamiska republiken Afghanistan",Afghanistan},{@official,common|"Afganistan İslam Cumhuriyeti",Afganistan},{@official,common|"اسلامی جمہوریہ افغانستان",افغانستان},{@official,common|阿富汗伊斯兰共和国,阿富汗}},[33,65],true,[IRN,PAK,TKM,UZB,TJK,CHN],652230,🇦🇫,{{@f,m|Afghan,Afghan},{@f,m|Afghane,Afghan}}|{Angola,"Republic of Angola",{@por|{@official,common|"República de Angola",Angola}}},[.ao],AO,"024",AGO,ANG,true,officially-assigned,true,"African Group",{@AOA|{@name,symbol|"Angolan kwanza",Kz}},{"+2",["44"]},[Luanda],[AO,"República de Angola","ʁɛpublika de an'ɡɔla"],Africa,"Middle Africa",{@por|Portuguese},{{@official,common|أنغولا,"جمهورية أنغولا"},{@official,common|"Republik Angola",Angola},{@official,common|"Angolská republika",Angola},{@official,common|"Republik Angola",Angola},{@official,common|"Angola Vabariik",Angola},{@official,common|"Angolan tasavalta",Angola},{@official,common|"République d'Angola",Angola},{@official,common|"Republika Angola",Angola},{@official,common|Angola,Angola},{@official,common|"Repubblica dell'Angola",Angola},{@official,common|アンゴラ共和国,アンゴラ},{@official,common|"앙골라 공화국",앙골라},{@official,common|"Republiek Angola",Angola},{@official,common|"جمهوری آنگولا",آنگولا},{@official,common|"Republika Angoli",Angola},{@official,common|"República de Angola",Angola},{@official,common|"Республика Ангола",Ангола},{@official,common|"Angolská republika",Angola},{@official,common|"República de Angola",Angola},{@official,common|"Republika Angola",Angola},{@official,common|"Republiken Angola",Angola},{@official,common|"Angola Cumhuriyeti",Angola},{@official,common|"جمہوریہ انگولہ",انگولہ},{@official,common|安哥拉共和国,安哥拉}},[-12.5,18.5],false,[COG,COD,ZMB,NAM],1246700,🇦🇴,{{@f,m|Angolan,Angolan},{@f,m|Angolaise,Angolais}}|{Anguilla,Anguilla,{@eng|{@official,common|Anguilla,Anguilla}}},[.ai],AI,"660",AIA,"",false,officially-assigned,false,"",{@XCD
... (truncated)
```

**minemizer** (323130 chars, 143182 tokens):
```txt
name{ common; official; native{ ...}}; tld[]; cca2; ccn3; cca3; cioc; independent; status; unMember; unRegionalGroup; currencies{ ...}; idd{ root; suffixes[]}; capital[]; altSpellings[]; region; subregion; languages{ ...}; translations{ ara{ official; common}; bre{ official; common}; ces{ official; common}; deu{ official; common}; est{ official; common}; fin{ official; common}; fra{ official; common}; hrv{ official; common}; hun{ official; common}; ita{ official; common}; jpn{ official; common}; kor{ official; common}; nld{ official; common}; per{ official; common}; pol{ official; common}; por{ official; common}; rus{ official; common}; slk{ official; common}; spa{ official; common}; srp{ official; common}; swe{ official; common}; tur{ official; common}; urd{ official; common}; zho{ official; common}}; latlng[]; landlocked; borders[]; area; flag; demonyms{ eng{ f; m}; fra{ f; m}}
{ Aruba; Aruba;{ nld:{ official: Aruba; common: Aruba}; pap:{ official: Aruba; common: Aruba}}};[ .aw]; AW; 533; ABW; ARU;false; officially-assigned;false;;{ AWG:{ name: Aruban florin; symbol: ƒ}};{ +2;[ 97]};[ Oranjestad];[ AW]; Americas; Caribbean;{ nld: Dutch; pap: Papiamento};{{ أروبا; أروبا};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ アルバ; アルバ};{ 아루바; 아루바};{ Aruba; Aruba};{ آروبا; آروبا};{ Aruba; Aruba};{ Aruba; Aruba};{ Аруба; Аруба};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ Aruba; Aruba};{ اروبا; اروبا};{ 阿鲁巴; 阿鲁巴}};[ 12.5; -69.96666666];false;[]; 180; 🇦🇼;{{ Aruban; Aruban};{ Arubaise; Arubais}}
{ Afghanistan; Islamic Republic of Afghanistan;{ prs:{ official: جمهوری اسلامی افغانستان; common: افغانستان}; pus:{ official: د افغانستان اسلامي جمهوریت; common: افغانستان}; tuk:{ official: Owganystan Yslam Respublikasy; common: Owganystan}}};[ .af]; AF; 004; AFG; AFG;true; officially-assigned;true; Asia and the Pacific Group;{ AFN:{ name: Afghan afghani; symbol: ؋}};{ +9;[ 3]};[ Kabul];[ AF; Afġānistān]; Asia; Southern Asia;{ prs: Dari; pus: Pashto; tuk: Turkmen};{{ جمهورية أففانستان الإسلامية; أفغانستان};{ Republik Islamek Afghanistan; Afghanistan};{ Afghánská islámská republika; Afghánistán};{ Islamische Republik Afghanistan; Afghanistan};{ Afganistani Islamivabariik; Afganistan};{ Afganistanin islamilainen tasavalta; Afganistan};{ République islamique d'Afghanistan; Afghanistan};{ Islamska Republika Afganistan; Afganistan};{ Afganisztáni Iszlám Köztársaság; Afganisztán};{ Repubblica islamica dell'Afghanistan; Afghanistan};{ アフガニスタン・イスラム共和国; アフガニスタン};{ 아프가니스탄 이슬람 공화국; 아프가니스탄};{ Islamitische Republiek Afghanistan; Afghanistan};{ جمهوری اسلامی افغانستان; افغانستان};{ Islamska Republika Afganistanu; Afganistan};{ República Islâmica do Afeganistão; Afeganistão};{ Исламская Республика Афганистан; Афганистан};{ Afgánsky islamský štát; Afganistan};{ República Islámica de Afganistán; Afganistán};{ Islamska Republika Avganistan; Avganistan};{ Islamiska republiken Afghanistan; Afghanistan};{ Afganistan İslam Cumhuriyeti; Afganistan};{ اسلامی جمہوریہ افغانستان; افغانستان};{ 阿富汗伊斯兰共和国; 阿富汗}};[ 33; 65];true;[ IRN; PAK; TKM; UZB; TJK; CHN]; 652230; 🇦🇫;{{ Afghan; Afghan};{ Afghane; Afghan}}
{ Angola; Republic of Angola;{ por:{ official: República de Angola; common: Angola}}};[ .ao]; AO; 024; AGO; ANG;true; officially-assigned;true; African Group;{ AOA:{ name: Angolan kwanza; symbol: Kz}};{ +2;[ 44]};[ Luanda];[ AO; República de Angola; ʁɛpublika de an'ɡɔla]; Africa; Middle Africa;{ por: Portuguese};{{ أنغولا; جمهورية أنغولا};{ Republik Angola; Angola};{ Angolská republika; Angola};{ Republik Angola; Angola};{ Angola Vabariik; Angola};{ Angolan tasavalta; Angola};{ République d'Angola; Angola};{ Republika Angola; Angola};{ Angola; Angola};{ Repubblica dell'Angola; Angola};{ アンゴラ共和国; アンゴラ};{ 앙골라 공화국; 앙골라};{ Republiek Angola; Angola};{ جمهوری آنگولا; آنگولا};{ Republika Angoli; Angola};{ República de Angola; Angola};{ Республика Ангола; Ангола};{ Angolská republika; Angola};{ República de Angola; Angola};{ Republika Angola; Angola};{ Republiken Angola; Angola};{ Angola Cumhuriyeti; Angola};{ جمہوریہ انگولہ; انگولہ};{ 安哥拉共和国; 安哥拉}};[ -12.5; 18.5];false;[ COG; COD; ZMB; NAM]; 1246700; 🇦🇴;{{ Angolan; Angolan};{ Angolaise; Angolais}}
{ Anguilla; Anguilla;{ eng:{ official: Anguilla; common: Anguilla}}};[ .ai]; AI; 660; AIA;;false; officially-assigned;false;;{ XCD:{ name: Eastern Caribbean dollar; symbol: $}};{ +1;[ 264]};[ The Valley];[ AI]; Americas; Caribbean;{ eng: English};{{ أنغويلا; أنغويلا};{ Anguilla; Anguilla};{ Anguilla; Anguilla};{ Anguilla; Anguilla};{ Anguilla; Anguilla};{ Anguilla; Anguilla};{ Anguilla; Anguilla};{ Anguilla; Angvila};{ Anguilla; Anguilla};{ Anguilla; Anguilla};{ アンギラ; アンギラ};{ 앵귈라; 앵귈라};{ Anguilla; Anguilla};{ آنگویلا; آنگویلا};{ Anguilla; Anguilla};{ Anguilla; Anguilla};{ Ангилья; Ангилья};{ Anguilla; Anguilla};{ Anguila; Anguilla};{ Angvila; Angvila};{ Anguilla; Anguilla};{ Anguilla; Anguilla};{ اینگویلا; اینگویلا};{ 安圭拉; 安圭拉}};[ 18.25; -63.16666666];false;[]; 91; 🇦🇮;{{ Anguillian; Anguillian};{ Anguillane; Anguillan}}
{ Åland Islands; Åland Islands;{ swe:{ official: Landskapet Åland; common: Åland}}};[ .ax]; AX; 248; ALA;;false; officially-assigned;false;;{ EUR:{ name: Euro; symbol: €}};{ +3;[ 5818]};[ Mariehamn];[ AX; Aaland; Aland; Ahvenanmaa]; Europe; Northern Europe;{ swe: Swedish};{{ جزر أولاند; جزر أولاند};{ Inizi Åland; Åland};{ Ålandské ostrovy; Ålandy};{ Åland-Inseln; Åland};{ Ahvenamaa maakond; Ahvenamaa};{ Ahvenanmaan maakunta; Ahvenanmaa};{ Ahvenanmaa; Ahvenanmaa};{ Aland Islands; Ålandski otoci};{ Åland-szigetek; Åland-szigetek};{ Isole Åland; Isole Aland};{ オーランド諸島; オーランド};{ 올란드 제도; 올란드 제도};{ Åland eilanden; Ålandeilanden};{ جزایر الند; جزایر الند};{ Wyspy Alandzkie; Wyspy Alandzkie};{ Ilhas Åland; Alândia};{ Аландские острова; Аландские острова};{ Alandské ostrovy; Alandy};{ Islas Åland; Alandia};{ Olandska Ostrva; Olandska Ostrva};{ Åland; Åland};{ Åland Adaları; Åland};{ جزائر اولند; جزائر اولند};{ 奥兰群岛; 奥兰群岛}};[ 60.116667; 19.9];false;[]; 1580; 🇦🇽;{{ Ålandish; Ålandish};{ Ålandaise; Ålandais}}
{ Albania; Republic of Albania;{ sqi:{ official: Republika e Shqipërisë; common: Shqipëria}}};[ .al]; AL; 008; ALB; ALB;true; officially-assigned;true; Eastern European Group;{ ALL:{ name: Albanian lek; symbol: L}};{ +3;[ 55]};[ Tirana];[ AL; Shqipëri; Shqipëria; Shqipnia]; Europe; Southeast Europe;{ sqi: Albanian};{{ جمهورية ألبانيا; ألبانيا};{ Republik Albania; Albania};{ Albánská republika; Albánie};{ Republik Albanien; Albanien};{ Albaania Vabariik; Albaania};{ Albanian tasavalta; Albania};{ République d'Albanie; Albanie};{ Republika Albanija; Albanija};{ Albán Köztársaság; Albánia};{ Repubblica d'Albania; Albania};{ アルバニア共和国; アルバニア};{ 알바니아 공화국; 알바니아};{ Republiek Albanië; Albanië};{ جمهوری آلبانی; آلبانی};{ Republika Albanii; Albania};{ República da Albânia; Albânia};{ Республика Албания; Албания};{ Albánska republika; Albánsko};{ República de Albania; Albania};{ Republika Albanija; Albanija};{ Republiken Albanien; Albanien};{ Arnavutluk Cumhuriyeti; Arnavutluk};{ جمہوریہ البانیا; البانیا};{ 阿尔巴尼亚共和国; 阿尔巴尼亚}};[ 41; 20];false;[ MNE; GRC; MKD; UNK]; 28748; 🇦🇱;{{ Albanian; Albanian};{ Albanaise; Albanais}}
{ Andorra; Principality of Andorra;{ cat:{ official: Principat d'Andorra; common: Andorra}}};[ .ad]; AD; 020; AND; AND;true; officially-assigned;true; Western European and Others Group;{ EUR:{ name: Euro; symbol: €}};{ +3;[ 76]};[ Andorra la Vella];[ AD; Principality of Andorra; Principat d'Andorra]; Europe; Southern Europe;{ cat: Catalan};{{ إمارة أندورا; أندورا};{ Priñselezh Andorra; Andorra};{ Andorrské knížectví; Andorra};{ Fürstentum Andorra; Andorra};{ Andorra Vürstiriik; Andorra};{ Andorran ruhtinaskunta; Andorra};{ Principauté d'Andorre; Andorre};{ Kneževina Andora; Andora};{ Andorra; Andorra};{ Principato di Andorra; Andorra};{ アンドラ公国; アンドラ};{ 안도라 공국; 안도라};{ Prinsdom Andorra; Andorra};{ شاهزاده‌نشین آندورا; آندورا};{ Księstwo Andory; Andora};{ Principado de Andorra; Andorra};{ Княжество Андорра; Андорра};{ Andorrské kniežatstvo; Andorra};{ Principado de Andorra; Andorra};{ Kneževina Andora; Andora};{ Furstendömet Andorra; Andorra};{ Andorra Prensliği; Andorra};{ اماراتِ انڈورا; انڈورا};{ 安道尔公国; 安道尔}};[ 42.5; 1.5];true;[ FRA; ESP]; 468; 🇦🇩;{{ Andorran; Andorran};{ Andorrane; Andorran}}
{ United Arab Emirates; United Arab Emirates;{ ara:{ official: الإمارات العربية المتحدة; common: الإمارات}}};[ .ae; امارات.]; AE; 784; ARE; UAE;true; officially-assigned;true; Asia and the Pacific Group;{ AED:{ name: United Arab Emirates dirham; symbol: د.إ}};{ +9;[ 71]};[ Abu Dhabi];[ AE; UAE; Emirates]; Asia; Western Asia;{ ara: Arabic};{{ الإمارات العربية المتحدة; الإمارات};{ Emirelezhioù Arab Unanet; Emirelezhioù Arab Unanet};{ Spojené arabské emiráty; Spojené arabské emiráty};{ Vereinigte Arabische Emirate; Vereinigte Arabische Emirate};{ Araabia Ühendemiraadid; Araabia Ühendemiraadid};{ Yhdistyneet arabiemiirikunnat; Arabiemiraatit};{ Émirats arabes unis; Émirats arabes unis};{ Ujedinjeni Arapski Emirati; Ujedinjeni Arapski Emirati};{ Egyesült Arab Emírségek; Egyesült Arab Emírségek};{ Emirati Arabi Uniti; Emirati Arabi Uniti};{ アラブ首長国連邦; UAE};{ 아랍 토후국 연방; 아랍에미리트};{ Verenigde Arabische Emiraten; Verenigde Arabische Emiraten};{ امارات متحده عربی; امارات};{ Zjednoczone Emiraty Arabskie; Zjednoczone Emiraty Arabskie};{ Emirados Árabes Unidos; Emirados Árabes Unidos};{ Объединенные Арабские Эмираты; Объединённые Арабские Эмираты};{ Spojené arabské emiráty; Spojené arabské emiráty};{ Emiratos Árabes Unidos; Emiratos Árabes Unidos};{ Ujedinjeni Arapski Emirati; Ujedinjeni Arapski Emirati};{ Förenade Arabemiraten; Förenade Arabemiraten};{ Birleşik Arap Emirlikleri; Birleşik Arap Emirlikleri};{ متحدہ عرب امارات; متحدہ عرب امارات};{ 阿拉伯联合酋长国; 阿拉伯联合酋长国}};[ 24; 54];false;[ OMN; SAU]; 83600; 🇦🇪;{{ Emirati; Emirati};{ Emirienne; Emirien}}
{ Argentina; Argentine Republic;{ grn:{ official: Argentine Republic; common: Argentina}; spa:{ official: República Argentina; common: Argentina}}};[ .ar]; AR; 032; ARG; ARG;true; officially-assigned;true; Latin American and Caribbean Group;{ ARS:{ name: Argentine peso; symbol: $}};{ +5;[ 4]};[ Buenos Aires];[ AR; Argentine Republic; República Argentina]; Americas; South America;{ grn: Guaraní; spa: Spanish};{{ جمهورية الأرجنتين; الأرجنتين};{ Republik Arc'hantina; Arc'hantina};{ Argentinská republika; Argentina};{ Argentinische Republik; Argentinien};{ Argentina Vabariik; Argentina};{ Argentiinan tasavalta; Argentiina};{ République argentine; Argentine};{ Argentinski Republika; Argentina};{ Argentin Köztársaság; Argentína};{ Repubblica Argentina; Argentina};{ アルゼンチン共和国; アルゼンチン};{ 아르헨티나 공화국; 아르헨티나};{ Argentijnse Republiek; Argentinië};{ جمهوری آرژانتین; آرژانتین};{ Republika Argentyńska; Argentyna};{ República Argentina; Argentina};{ Аргентинская Республика; Аргентина};{ Argentínska republika; Argentína};{ República Argentina; Argentina};{ Republika Argentina; Argentina};{ Republiken Argentina; Argentina};{ Arjantin Cumhuriyeti; Arjantin};{ جمہوریہ ارجنٹائن; ارجنٹائن};{ 阿根廷共和国; 阿根廷}};[ -34; -64];false;[ BOL; BRA; CHL; PRY; URY]; 2780400; 🇦🇷;{{ Argentine; Argentine};{ Argentine; Argentin}}
{ Armenia; Republic of Armenia;{ hye:{ official: Հայաստանի Հանրապետություն; common: Հայաստան}}};[ .am]; AM; 051; ARM; ARM;true; officially-assigned;true; Eastern European Group;{ AMD:{ name: Armenian dram; symbol: ֏}};{ +3;[ 74]};[ Yerevan];[ AM; Hayastan; Republic of Armenia; Հայաստանի Հանրապետություն]; Asia; Western Asia;{ hye: Armenian};{{ جمهورية أرمينيا; أرمينيا};{ Republik Armenia; Armenia};{ Arménská republika; Arménie};{ Republik Armenien; Armenien};{ Armeenia Vabariik; Armeenia};{ Armenian tasavalta; Armenia};{ République d'Arménie; Arménie};{ Republika Armenija; Armenija};{ Örményország; Örményország};{ Repubblica di Armenia; Armenia};{ アルメニア共和国; アルメニア};{ 아르메니아 공화국; 아르메니아};{ Republiek Armenië; Armenië};{ جمهوری ارمنستان; ارمنستان};{ Republika Armenii; Armenia};{ República da Arménia; Arménia};{ Республика Армения; Армения};{ Arménska republika; Arménsko};{ República de Armenia; Armenia};{ Republika Jermenija; Jermenija};{ Republiken Armenien; Armenien};{ Ermenistan Cumhuriyeti; Ermenistan};{ جمہوریہ آرمینیا; آرمینیا};{ 亚美尼亚共和国; 亚美尼亚}};[ 40; 45];true;[ AZE; GEO; IRN; TUR]; 29743; 🇦🇲;{{ Armenian; Armenian};{ Arménienne; Arménien}}
{ American Samoa; American Samoa;{ eng:{ official: American Samoa; common: American Samoa}; smo:{ official: Sāmoa Amelika; common: Sāmoa Amelika}}};[ .as]; AS; 016; ASM; ASA;false; officially-assigned;false;;{ USD:{ name: United States dollar; symbol: $}};{ +1;[ 684]};[ Pago Pago];[ AS; Amerika Sāmoa; Amelika Sāmoa; Sāmoa Amelika]; Oceania; Polynesia;{ eng: English; smo: Samoan};{{ ساموا الأمريكية; ساموا الأمريكية};{ Samoa Amerikan; Samoa Amerikan};{ Americká Samoa; Americká Samoa};{ Amerikanisch-Samoa; Amerikanisch-Samoa};{ Ameerika Samoa; Ameerika Samoa};{ Amerikan Samoa; Amerikan Samoa};{ Samoa américaines; Samoa américaines};{ američka Samoa; Američka Samoa};{ Szamoa; Szamoa};{ Samoa americane; Samoa Americane};{ 米領サモア; アメリカ領サモア};{ 아메리칸사모아; 아메리칸사모아};{ Amerikaans Samoa; Amerikaans Samoa};{ ساموآی آمریکا; ساموآی آمریکا};{ Samoa Amerykańskie; Samoa Amerykańskie};{ Samoa americana; Samoa Americana};{ американское Самоа; Американское Самоа};{ Americká Samoa; Americká Samoa};{ Samoa Americana; Samoa Americana};{ Američka Samoa; Američka Samoa};{ Amerikanska Samoa; Amerikanska Samoa};{ Amerikan Samoası; Amerikan Samoası};{ امریکی سمووا; امریکی سمووا};{ 美属萨摩亚; 美属萨摩亚}};[ -14.33333333; -170];false;[]; 199; 🇦🇸;{{ American Samoan; American Samoan};{ Samoane; Samoan}}
{ Antarctica; Antarctica;{}};[ .aq]; AQ; 010; ATA;;false; officially-assigned;false;;{};{;[]};[];[ AQ]; Antarctic;;{};{{ أنتارتيكا; أنتارتيكا};{ Antarktika; Antarktika};{ Antarktida; Antarktida};{ Antarktika; Antarktis};{ Antarktika; Antarktika};{ Etelämanner; Etelämanner};{ Antarctique; Antarctique};{ Antarktika; Antarktika};{ Antarktisz; Antarktisz};{ Antartide; Antartide};{ 南極; 南極大陸};{ 남극; 남극};{ Antarctica; Antarctica};{ جنوبگان; جنوبگان};{ Antarktyka; Antarktyka};{ Antártica; Antártida};{ Антарктида; Антарктида};{ Antarktída; Antarktída};{ Antártida; Antártida};{ Antarktik; Antarktik};{ Antarktis; Antarktis};{ Antarktika; Antarktika};{ انٹارکٹکا; انٹارکٹکا};{ 南极洲; 南极洲}};[ -90; 0];false;[]; 14000000; 🇦🇶;{{ Antarctican; Antarctican};{ Antarcticaine; Antarcticain}}
{ French Southern and Antarctic Lands; Territory of the French Southern and Antarctic Lands;{ fra:{ official: Territoire des Terres australes et antarctiques françaises; common: Terres australes et antarctiques françaises}}};[ .tf]; TF; 260; ATF;;false; officially-assigned;false;;{ EUR:{ name: Euro; symbol: €}};{ +2;[ 62]};[ Port-aux-Français];[ TF; French Southern Territories]; Antarctic;;{ fra: French};{{ مقاطعات وأقاليم ما وراء البحار الفرنسية; أراض فرنسية جنوبية وأنتارتيكية};{ Tiriad Douaroù Aostral hag Antarktikel Frañs; Douaroù Aostral hag Antarktikel Frañs};{ Teritorium Francouzská jižní a antarktická území; Francouzská jižní a antarktická území};{ Gebiet der Französisch Süd- und Antarktisgebiete; Französische Süd- und Antarktisgebiete};{ Prantsuse Lõunaalad; Prantsuse Lõunaalad};{ Ranskan eteläiset ja antarktiset alueet; Ranskan eteläiset ja antarktiset alueet};{ Territoire des Terres australes et antarctiques françaises; Terres australes et antarctiques françaises};{ Teritoriju Francuski južni i antarktički teritoriji; Francuski južni i antarktički teritoriji};{ Francia déli és antarktiszi területek; Francia déli és antarktiszi területek};{ Territorio della australi e antartiche francesi Terre; Territori Francesi del Sud};{ フランス領極南諸島; フランス領南方・南極地域};{ 프랑스령 남부와 남극 지역; 프랑스령 남부와 남극 지역};{ Grondgebied van de Franse Zuidelijke en Antarctische gebieden; Franse Gebieden in de zuidelijke Indische Oceaan};{ سرزمین‌های جنوبی و جنوبگانی فرانسه; سرزمین‌های جنوبی و جنوبگانی فرانسه};{ Francuskie Terytoria Południowe i Antarktyczne; Francuskie Terytoria Południowe i Antarktyczne};{ Território do Sul e Antártica Francesa; Terras Austrais e Antárticas Francesas};{ Территория Французские Южные и Антарктические земли; Французские Южные и Антарктические территории};{ Francúzske južné a antarktické územia; Francúzske juŽné a antarktické územia};{ Territorio del Francés Tierras australes y antárticas; Tierras Australes y Antárticas Francesas};{ Francuske južne i antarktičke zemlje; Francuske južne i antarktičke zemlje};{ Franska syd- och Antarktisterritorierna; Franska södra territorierna};{ Fransız Güney ve Antarktika Toprakları; Fransız Güney ve Antarktika Toprakları};{ سرزمینِ جنوبی فرانسیسیہ و انٹارکٹیکہ; سرزمین جنوبی فرانسیسیہ و انٹارکٹیکا};{ 法国南部和南极土地; 法国南部和南极土地}};[ -49.25; 69.167];false;[]; 7747; 🇹🇫;{{ French; French};{ Française; Français}}
{ Antigua and Barbuda; Antigua and Barbuda;{ eng:{ official: Antigua and Barbuda; common: Antigua and Barbuda}}};[ .ag]; AG; 028; ATG; ANT;true; officially-assigned;true; Latin American and Caribbean Group;{ XCD:{ name: Eastern Caribbean dollar; symbol: $}};{ +1;[ 268]};[ Saint John's];[ AG]; Americas; Caribbean;{ eng: English};{{ أنتيغوا وباربودا; أنتيغوا وباربودا};{ Antigua ha Barbuda; Antigua ha Barbuda};{ Antigua a Barbuda; Antigua a Barbuda};{ Antigua und Barbuda; Antigua und Barbuda};{ Antigua ja Barbuda; Antigua ja Barbuda};{ Antigua ja Barbuda; Antigua ja Barbuda};{ Antigua -et-Barbuda; Antigua-et-Barbuda};{ Antigva i Barbuda; Antigva i Barbuda};{ Antigua és Barbuda; Antigua és Barbuda};{ Antigua e Barbuda; Antigua e Barbuda};{ アンティグア・バーブーダ; アンティグア・バーブーダ};{ 앤티가 바부다; 앤티가 바부다};{ Antigua en Barbuda; Antigua en Barbuda};{ آنتیگوا و باربودا; آنتیگوا و باربودا};{ Antigua i Barbuda; Antigua i Barbuda};{ Antigua e Barbuda; Antígua e Barbuda};{ Антигуа и Барбуда; Антигуа и Барбуда};{ Antigua a Barbuda; Antigua a Barbuda};{ Antigua y Barbuda; Antigua y Barbuda};{ Antigva i Barbuda; Antigva i Barbuda};{ Antigua och Barbuda; Antigua och Barbuda};{ Antigua ve Barbuda; Antigua ve Barbuda};{ اینٹیگوا و باربوڈا; اینٹیگوا و باربوڈا};{ 安提瓜和巴布达; 安提瓜和巴布达}};[ 17.05; -61.8];false;[]; 442; 🇦🇬;{{ Antiguan, Barbudan; Antiguan, Barbudan};{ Antiguaise et barbudienne; Antiguaise et barbudien}}
{ Australia; Commonwealth of Australia;{ eng:{ official: Commonwealth of Australia; common: Australia}}};[ .au]; AU; 036; AUS; AUS;true; officially-assigned;true; Western European and Others Group;{ AUD:{ name: Australian dollar; symbol: $}};{ +6;[ 1]};[ Canberra];[ AU]; Oceania; Australia and New Zealand;{ eng: English};{{ كومونولث أستراليا; أستراليا};{ Kenglad Aostralia; Aostralia};{ Australské společenství; Austrálie};{ Commonwealth Australien; Australien};{ Austraalia Ühendus; Austraalia};{ Australian liittovaltio; Australia};{ Australie; Australie};{ Commonwealth of Australia; Australija};{ Ausztrál Államszövetség; Ausztrália};{ Commonwealth dell'Australia; Australia};{ オーストラリア連邦; オーストラリア};{ 오스트레일리아 연방; 호주};{ Gemenebest van Australië; Australië};{ قلمرو همسود استرالیا; استرالیا};{ Związek Australijski; Australia};{ Comunidade da Austrália; Austrália};{ Содружество Австралии; Австралия};{ Austrálsky zväz; Austrália};{ Mancomunidad de Australia; Australia};{ Komonvelt Australija; Australija};{ Australiska statsförbundet; Australien};{ Avustralya Federal Devleti; Avustralya};{ دولتِ مشترکہ آسٹریلیا; آسٹریلیا};{ 澳大利亚联邦; 澳大利亚}};[ -27; 133];false;[]; 7692024; 🇦🇺;{{ Australian; Australian};{ Australienne; Australien}}
{ Austria; Republic of Austria;{ bar:{ official: Republik Österreich; common: Österreich}}};[ .at]; AT; 040; AUT; AUT;true; officially-assigned;true; Western European and Others Group;{ EUR:{ name: Euro; symbol: €}};{ +4;[ 3]};[ Vienna];[ AT; Osterreich; Oesterreich]; Europe; Central Europe;{ bar: Austro-Bavarian German};{{ جمهورية النمسا; النمسا};{ Republik Aostria; Aostria};{ Rakouská republika; Rakousko};{ Republik Österreich; Österreich};{ Austria Vabariik; Austria};{ Itävallan tasavalta; Itävalta};{ République d'Autriche; Autriche};{ Republika Austrija; Austrija};{ Ausztria; Ausztria};{ Repubblica d'Austria; Austria};{ オーストリア共和国; オーストリア};{ 오스트리아 공화국; 오스트리아};{ Republiek Oostenrijk; Oostenrijk};{ جمهوری اتریش; اتریش};{ Republika Austrii; Austria};{ República da Áustria; Áustria};{ Австрийская Республика; Австрия};{ Rakúska republika; Rakúsko};{ República de Austria; Austria};{ Republika Austrija; Austrija};{ Republiken Österrike; Österrike};{ Avusturya Cumhuriyeti; Avusturya};{ جمہوریہ آسٹریا; آسٹریا};{ 奥地利共和国; 奥地利}};[ 47.33333333; 13.33333333];true;[ CZE; DEU; HUN; ITA; LIE; SVK; SVN; CHE]; 83871; 🇦🇹;{{ Austrian; Austrian};{ Autrichienne; Autrichien}}
{ Azerbaijan; Republic of Azerbaijan;{ aze:{ official: Azərbaycan Respublikası; common: Azərbaycan}; rus:{ official: Азербайджанская Республика; common: Азербайджан}}};[ .az]; AZ; 031; AZE; AZE;true; officially-assigned;true; Eastern European Group;{ AZN:{ name: Azerbaijani manat; symbol: ₼}};{ +9;[ 94]};[ Baku];[ AZ; Republic of Azerbaijan; Azərbaycan Respublikası]; Asia; Western Asia;{ aze: Azerbaijani; rus: Russian};{{ جمهورية أذربيجان; أذربيجان};{ Republik Azerbaidjan; Azerbaidjan};{ Ázerbájdžánská republika; Ázerbájdžán};{ Republik Aserbaidschan; Aserbaidschan};{ Aserbaidžaani Vabariik; Aserbaidžaan};{ Azerbaidzanin tasavalta; Azerbaidzan};{ République d'Azerbaïdjan; Azerbaïdjan};{ Republika Azerbajdžan; Azerbajdžan};{ Azerbajdzsán; Azerbajdzsán};{ Repubblica dell'Azerbaigian; Azerbaijan};{ アゼルバイジャン共和国; アゼルバイジャン};{ 아제르바이잔 공화국; 아제르바이잔};{ Republiek Azerbeidzjan; Azerbeidzjan};{ جمهوری آذربایجان; جمهوری آذربایجان};{ Republika Azerbejdżanu; Azerbejdżan};{ República do Azerbaijão; Azerbeijão};{ Азербайджанская Республика; Азербайджан};{ Azerbajǆanská republika; AzerbajǇan};{ República de Azerbaiyán; Azerbaiyán};{ Republika Azerbejdžan; Azerbejdžan};{ Republiken Azerbajdzjan; Azerbajdzjan};{ Azerbaycan Cumhuriyeti; Azerbaycan};{ جمہوریہ آذربائیجان; آذربائیجان};{ 阿塞拜疆共和国; 阿塞拜疆}};[ 40.5; 47.5];true;[ ARM; GEO; IRN; RUS; TUR]; 86600; 🇦🇿;{{ Azerbaijani; Azerbaijani};{ Azerbaïdjanaise; Azerbaïdjanais}}
{ Burundi; Republic of Burundi;{ fra:{ official: République du Burundi; common: Burundi}; run:{ official: Republika y'Uburundi ; common: Uburundi}}};[ .bi]; BI; 108; BDI; BDI;true; officially-assigned;true; African Group;{ BIF:{ name: Burundian franc; symbol: Fr}};{ +2;[ 57]};[ Gitega];[ BI; Republic of Burundi; Republika y'Uburundi; République du Burundi]; Africa; Eastern Africa;{ fra: French; run: Kirundi};{{ جمهورية بوروندي; بوروندي};{ Republik Burundi; Burundi};{ Burundská republika; Burundi};{ Republik Burundi; Burundi};{ Burundi Vabariik; Burundi};{ Burundin tasavalta; Burundi};{ République du Burundi; Burundi};{ Burundi; Burundi};{ Burundi; Burundi};{ Repubblica del Burundi; Burundi};{ ブルンジ共和国; ブルンジ};{ 부룬디; 부룬디};{ Republiek Burundi; Burundi};{ جمهوری بوروندی; بوروندی};{ Republika Burundi; Burundi};{ República do Burundi; Burundi};{ Республика Бурунди; Бурунди};{ Burundská republika; Burundi};{ República de Burundi; Burundi};{ Republika Burundi; Burundi};{ Republiken Burundi; Burundi};{ Burundi Cumhuriyeti; Burundi};{ جمہوریہ برونڈی; برونڈی};{ 布隆迪共和国; 布隆迪}};[ -3.5; 30];true;[ COD; RWA; TZA]; 27834; 🇧🇮;{{ Burundian; Burundian};{ Burundaise; Burundais}}
{ Belgium; Kingdom of Belgium;{ deu:{ official: Königreich Belgien; common: Belgien}; fra:{ official: Royaume de Belgique; common: Belgique}; nld:{ official: Koninkrijk België; common: België}}};[ .be]; BE; 056; BEL; BEL;true; officially-assigned;true; Western European and Others Group;{ EUR:{ name: Euro; symbol: €}};{ +3;[ 2]};[ Brussels];[ BE; België; Belgie; Belgien; Belgique; Kingdom of Belgium; Koninkrijk België; Royaume de Belgique; Königreich Belgien]; Europe; Western Europe;{ deu: German; fra: French; nld: Dutch};{{ مملكة بلجيكا; بلجيكا};{ Rouantelezh Belgia; Belgia};{ Belgické království; Belgie};{ Königreich Belgien; Belgien};{ Belgia Kuningriik; Belgia};{ Belgian kuningaskunta; Belgia};{ Royaume de Belgique; Belgique};{ Kraljevina Belgija; Belgija};{ Belga Királyság; Belgium};{ Regno del Belgio; Belgio};{ ベルギー王国; ベルギー};{ 벨기에 왕국; 벨기에};{ Koninkrijk België; België};{ پادشاهی بلژیک; بلژیک};{ Królestwo Belgii; Belgia};{ Reino da Bélgica; Bélgica};{ Королевство Бельгия; Бельгия};{ Belgické kráľovstvo; Belgicko};{ Reino de Bélgica; Bélgica};{ Kraljevina Belgija; Belgija};{ Konungariket Belgien; Belgien};{ Belçika Krallığı; Belçika};{ مملکتِ بلجئیم; بلجئیم};{ 比利时王国; 比利时}};[ 50.83333333; 4];false;[ FRA; DEU; LUX; NLD]; 30528; 🇧🇪;{{ Belgian; Belgian};{ Belge; Belge}}
{ Benin; Republic of Benin;{ fra:{ official: République du Bénin; common: Bénin}}};[ .bj]; BJ; 204; BEN; BEN;true; officially-assigned;true; African Group;{ XOF:{ name: West African CFA franc; symbol: Fr}};{ +2;[ 29]};[ Porto-Novo];[ BJ; Republic of Benin; République du Bénin]; Africa; Western Africa;{ fra: French};{{ جمهورية بنين; بنين};{ Republik Benin; Benin};{ Beninská republika; Benin};{ Republik Benin; Benin};{ Benini Vabariik; Benin};{ Beninin tasavalta; Benin};{ République du Bénin; Bénin};{ Republika Benin; Benin};{ Benini Köztársaság; Benin};{ Repubblica del Benin; Benin};{ ベナン共和国; ベナン};{ 베냉 공화국; 베냉};{ Republiek Benin; Benin};{ جمهوری بنین; بنین};{ Benin; Benin};{ República do Benin; Benin};{ Республика Бенин; Бенин};{ Beninská republika; Benin};{ República de Benin; Benín};{ Republika Benin; Benin};{ Republiken Benin; Benin};{ Benin Cumhuriyeti; Benin};{ جمہوریہ بینن; بینن};{ 贝宁共和国; 贝宁}};[ 9.5; 2.25];false;[ BFA; NER; NGA; TGO]; 112622; 🇧🇯;{{ Beninese; Beninese};{ Béninoise; Béninois}}
{ Burkina Faso; Burkina Faso;{ fra:{ official: République du Burkina; common: Burkina Faso}}};[ .bf]; BF; 854; BFA; BUR;true; officially-assigned;true; African Group;{ XOF:{ name: West African CFA franc; symbol: Fr}};{ +2;[ 26]};[ Ouagadougou];[ BF]; Africa; Western Africa;{ fra: French};{{ بوركينا فاسو; بوركينا فاسو};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ République du Burkina; Burkina Faso};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina};{ Burkina Faso; Burkina Faso};{ ブルキナファソ; ブルキナファソ};{ 부르키나파소; 부르키나파소};{ Burkina Faso; Burkina Faso};{ بورکینافاسو; بورکینافاسو};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ Буркина -Фасо; Буркина-Фасо};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ Burkina Faso; Burkina Faso};{ برکینا فاسو; برکینا فاسو};{ 布基纳法索; 布基纳法索}};[ 13; -2];true;[ BEN; CIV; GHA; MLI; NER; TGO]; 272967; 🇧🇫;{{ Burkinabe; Burkinabe};{ Burkinabée; Burkinabé}}
{ Bangladesh; People's Republic of Bangladesh;{ ben:{ official: বাংলাদেশ গণপ্রজাতন্ত্রী; common: বাংলাদেশ}}};[ .bd]; BD; 050; BGD; BAN;true; officially-assigned;true; Asia and the Pacific Group;{ BDT:{ name: Bangladeshi taka; symbol: ৳}};{ +8;[ 80]};[ Dhaka];[ BD; People's Republic of Bangladesh; Gônôprôjatôntri Bangladesh]; Asia; Southern Asia;{ ben: Bengali};{{ جمهورية بنغلاديش الشعبية; بنغلاديش};{ Republik pobl Bangladesh; Bangladesh};{ Bangladéšská lidová republika; Bangladéš};{ Volksrepublik Bangladesch; Bangladesch};{ Bangladeshi Rahvavabariik; Bangladesh};{ Bangladeshin kansantasavalta; Bangladesh};{ La République populaire du Bangladesh; Bangladesh};{ Narodna Republika Bangladeš; Bangladeš};{ Banglades; Banglades};{ Repubblica popolare del Bangladesh; Bangladesh};{ バングラデシュ人民共和国; バングラデシュ};{ 방글라데시 인민 공화국; 방글라데시};{ Volksrepubliek Bangladesh; Bangladesh};{ جمهوری خلق بنگلادش; بنگلادش};{ Ludowa Republika Bangladeszu; Bangladesz};{ República Popular do Bangladesh; Bangladesh};{ Народная Республика Бангладеш; Бангладеш};{ Bangladéšska ľudová republika; Bangladéš};{ República Popular de Bangladesh; Bangladesh};{ Narodna Republika Bangladeš; Bangladeš};{ Folkrepubliken Bangladesh; Bangladesh};{ Bangladeş Halk Cumhuriyeti; Bangladeş};{ عوامی جمہوریہ بنگلہ دیش; بنگلہ دیش};{ 孟加拉人民共和国; 孟加拉国}};[ 24; 90];false;[ MMR; IND]; 147570; 🇧🇩;{{ Bangladeshi; Bangladeshi};{ Bangladaise; Bangladais}}
{ Bulgaria; Republic of Bulgaria;{ bul:{ official: Република България; common: България}}};[ .bg]; BG; 100; BGR; BUL;true; officially-assigned;true; Eastern European Group;{ BGN:{ name: Bulgarian lev; symbol: лв}};{ +3;[ 59]};[ Sofia];[ BG; Republic of Bulgaria; Република България]; Europe; Southeast Europe;{ bul: Bulgarian};{{ جمهورية بلغاريا; بلغاريا};{ Republik Bulgaria; Bulgaria};{ Bulharská republika; Bulharsko};{ Republik Bulgarien; Bulgarien};{ Bulgaaria Vabariik; Bulgaaria};{ Bulgarian tasavalta; Bulgaria};{ République de Bulgarie; Bulgarie};{ Republika Bugarska; Bugarska};{ Bolgár Köztársaság; Bulgária};{ Repubblica di Bulgaria; Bulgaria};{ ブルガリア共和国; ブルガリア};{ 불가리아 공화국; 불가리아};{ Republiek Bulgarije; Bulgarije};{ جمهوری بلغارستان; بلغارستان};{ Republika Bułgarii; Bułgaria};{ República da Bulgária; Bulgária};{ Республика Болгария; Болгария};{ Bulharská republika; Bulharsko};{ República de Bulgaria; Bulgaria};{ Republika Bugarska; Bugarska};{ Republiken Bulgarien; Bulgarien};{ Bulgaristan Cumhuriyeti; Bulgaristan};{ جمہوریہ بلغاریہ; بلغاریہ};{ 保加利亚共和国; 保加利亚}};[ 43; 25];false;[ GRC; MKD; ROU; SRB; TUR]; 110879; 🇧🇬;{{ Bulgarian; Bulgarian};{ Bulgare; Bulgare}}
{ Bahrain; Kingdom of Bahrain;{ ara:{ official: مملكة البحرين; common: البحرين}}};[ .bh]; BH; 048; BHR; BRN;true; officially-assigned;true; Asia and the Pacific Group;{ BHD:{ name: Bahraini dinar; symbol: .د.ب}};{ +9;[ 73]};[ Manama];[ BH; Kingdom of Bahrain; Mamlakat al-Baḥrayn]; Asia; Western Asia;{ ara: Arabic};{{ مملكة البحرين; البحرين};{ Rouantelezh Bahrein; Bahrein};{ Království Bahrajn; Bahrajn};{ Königreich Bahrain; Bahrain};{ Bahreini Kuningriik; Bahrein};{ Bahrainin kuningaskunta; Bahrain};{ Royaume de Bahreïn; Bahreïn};{ Kraljevina Bahrein; Bahrein};{ Bahreini Királyság; Bahrein};{ Regno del Bahrain; Bahrein};{ バーレーン王国; バーレーン};{ 바레인 왕국; 바레인};{ Koninkrijk Bahrein; Bahrein};{ پادشاهی بحرین; بحرین};{ Królestwo Bahrajnu; Bahrajn};{ Reino do Bahrein; Bahrein};{ Королевство Бахрейн; Бахрейн};{ Bahrajnské kráľovstvo; Bahrajn};{ Reino de Bahrein; Bahrein};{ Kraljevina Bahrein; Bahrein};{ Konungariket Bahrain; Bahrain};{ Bahreyn Krallığı; Bahreyn};{ مملکتِ بحرین; بحرین};{ 巴林王国; 巴林}};[ 26; 50.55];false;[]; 765; 🇧🇭;{{ Bahraini; Bahraini};{ Bahreïnienne; Bahreïnien}}
... (truncated)
```

**minemizer (compact)** (299485 chars, 146248 tokens):
```txt
name{common;official;native{...}};tld[];cca2;ccn3;cca3;cioc;independent;status;unMember;unRegionalGroup;currencies{...};idd{root;suffixes[]};capital[];altSpellings[];region;subregion;languages{...};translations{ara{official;common};bre{official;common};ces{official;common};deu{official;common};est{official;common};fin{official;common};fra{official;common};hrv{official;common};hun{official;common};ita{official;common};jpn{official;common};kor{official;common};nld{official;common};per{official;common};pol{official;common};por{official;common};rus{official;common};slk{official;common};spa{official;common};srp{official;common};swe{official;common};tur{official;common};urd{official;common};zho{official;common}};latlng[];landlocked;borders[];area;flag;demonyms{eng{f;m};fra{f;m}}
{Aruba;Aruba;{nld:{official:Aruba;common:Aruba};pap:{official:Aruba;common:Aruba}}};[.aw];AW;533;ABW;ARU;false;officially-assigned;false;;{AWG:{name:Aruban florin;symbol:ƒ}};{+2;[97]};[Oranjestad];[AW];Americas;Caribbean;{nld:Dutch;pap:Papiamento};{{أروبا;أروبا};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{アルバ;アルバ};{아루바;아루바};{Aruba;Aruba};{آروبا;آروبا};{Aruba;Aruba};{Aruba;Aruba};{Аруба;Аруба};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{Aruba;Aruba};{اروبا;اروبا};{阿鲁巴;阿鲁巴}};[12.5;-69.96666666];false;[];180;🇦🇼;{{Aruban;Aruban};{Arubaise;Arubais}}
{Afghanistan;Islamic Republic of Afghanistan;{prs:{official:جمهوری اسلامی افغانستان;common:افغانستان};pus:{official:د افغانستان اسلامي جمهوریت;common:افغانستان};tuk:{official:Owganystan Yslam Respublikasy;common:Owganystan}}};[.af];AF;004;AFG;AFG;true;officially-assigned;true;Asia and the Pacific Group;{AFN:{name:Afghan afghani;symbol:؋}};{+9;[3]};[Kabul];[AF;Afġānistān];Asia;Southern Asia;{prs:Dari;pus:Pashto;tuk:Turkmen};{{جمهورية أففانستان الإسلامية;أفغانستان};{Republik Islamek Afghanistan;Afghanistan};{Afghánská islámská republika;Afghánistán};{Islamische Republik Afghanistan;Afghanistan};{Afganistani Islamivabariik;Afganistan};{Afganistanin islamilainen tasavalta;Afganistan};{République islamique d'Afghanistan;Afghanistan};{Islamska Republika Afganistan;Afganistan};{Afganisztáni Iszlám Köztársaság;Afganisztán};{Repubblica islamica dell'Afghanistan;Afghanistan};{アフガニスタン・イスラム共和国;アフガニスタン};{아프가니스탄 이슬람 공화국;아프가니스탄};{Islamitische Republiek Afghanistan;Afghanistan};{جمهوری اسلامی افغانستان;افغانستان};{Islamska Republika Afganistanu;Afganistan};{República Islâmica do Afeganistão;Afeganistão};{Исламская Республика Афганистан;Афганистан};{Afgánsky islamský štát;Afganistan};{República Islámica de Afganistán;Afganistán};{Islamska Republika Avganistan;Avganistan};{Islamiska republiken Afghanistan;Afghanistan};{Afganistan İslam Cumhuriyeti;Afganistan};{اسلامی جمہوریہ افغانستان;افغانستان};{阿富汗伊斯兰共和国;阿富汗}};[33;65];true;[IRN;PAK;TKM;UZB;TJK;CHN];652230;🇦🇫;{{Afghan;Afghan};{Afghane;Afghan}}
{Angola;Republic of Angola;{por:{official:República de Angola;common:Angola}}};[.ao];AO;024;AGO;ANG;true;officially-assigned;true;African Group;{AOA:{name:Angolan kwanza;symbol:Kz}};{+2;[44]};[Luanda];[AO;República de Angola;ʁɛpublika de an'ɡɔla];Africa;Middle Africa;{por:Portuguese};{{أنغولا;جمهورية أنغولا};{Republik Angola;Angola};{Angolská republika;Angola};{Republik Angola;Angola};{Angola Vabariik;Angola};{Angolan tasavalta;Angola};{République d'Angola;Angola};{Republika Angola;Angola};{Angola;Angola};{Repubblica dell'Angola;Angola};{アンゴラ共和国;アンゴラ};{앙골라 공화국;앙골라};{Republiek Angola;Angola};{جمهوری آنگولا;آنگولا};{Republika Angoli;Angola};{República de Angola;Angola};{Республика Ангола;Ангола};{Angolská republika;Angola};{República de Angola;Angola};{Republika Angola;Angola};{Republiken Angola;Angola};{Angola Cumhuriyeti;Angola};{جمہوریہ انگولہ;انگولہ};{安哥拉共和国;安哥拉}};[-12.5;18.5];false;[COG;COD;ZMB;NAM];1246700;🇦🇴;{{Angolan;Angolan};{Angolaise;Angolais}}
{Anguilla;Anguilla;{eng:{official:Anguilla;common:Anguilla}}};[.ai];AI;660;AIA;;false;officially-assigned;false;;{XCD:{name:Eastern Caribbean dollar;symbol:$}};{+1;[264]};[The Valley];[AI];Americas;Caribbean;{eng:English};{{أنغويلا;أنغويلا};{Anguilla;Anguilla};{Anguilla;Anguilla};{Anguilla;Anguilla};{Anguilla;Anguilla};{Anguilla;Anguilla};{Anguilla;Anguilla};{Anguilla;Angvila};{Anguilla;Anguilla};{Anguilla;Anguilla};{アンギラ;アンギラ};{앵귈라;앵귈라};{Anguilla;Anguilla};{آنگویلا;آنگویلا};{Anguilla;Anguilla};{Anguilla;Anguilla};{Ангилья;Ангилья};{Anguilla;Anguilla};{Anguila;Anguilla};{Angvila;Angvila};{Anguilla;Anguilla};{Anguilla;Anguilla};{اینگویلا;اینگویلا};{安圭拉;安圭拉}};[18.25;-63.16666666];false;[];91;🇦🇮;{{Anguillian;Anguillian};{Anguillane;Anguillan}}
{Åland Islands;Åland Islands;{swe:{official:Landskapet Åland;common:Åland}}};[.ax];AX;248;ALA;;false;officially-assigned;false;;{EUR:{name:Euro;symbol:€}};{+3;[5818]};[Mariehamn];[AX;Aaland;Aland;Ahvenanmaa];Europe;Northern Europe;{swe:Swedish};{{جزر أولاند;جزر أولاند};{Inizi Åland;Åland};{Ålandské ostrovy;Ålandy};{Åland-Inseln;Åland};{Ahvenamaa maakond;Ahvenamaa};{Ahvenanmaan maakunta;Ahvenanmaa};{Ahvenanmaa;Ahvenanmaa};{Aland Islands;Ålandski otoci};{Åland-szigetek;Åland-szigetek};{Isole Åland;Isole Aland};{オーランド諸島;オーランド};{올란드 제도;올란드 제도};{Åland eilanden;Ålandeilanden};{جزایر الند;جزایر الند};{Wyspy Alandzkie;Wyspy Alandzkie};{Ilhas Åland;Alândia};{Аландские острова;Аландские острова};{Alandské ostrovy;Alandy};{Islas Åland;Alandia};{Olandska Ostrva;Olandska Ostrva};{Åland;Åland};{Åland Adaları;Åland};{جزائر اولند;جزائر اولند};{奥兰群岛;奥兰群岛}};[60.116667;19.9];false;[];1580;🇦🇽;{{Ålandish;Ålandish};{Ålandaise;Ålandais}}
{Albania;Republic of Albania;{sqi:{official:Republika e Shqipërisë;common:Shqipëria}}};[.al];AL;008;ALB;ALB;true;officially-assigned;true;Eastern European Group;{ALL:{name:Albanian lek;symbol:L}};{+3;[55]};[Tirana];[AL;Shqipëri;Shqipëria;Shqipnia];Europe;Southeast Europe;{sqi:Albanian};{{جمهورية ألبانيا;ألبانيا};{Republik Albania;Albania};{Albánská republika;Albánie};{Republik Albanien;Albanien};{Albaania Vabariik;Albaania};{Albanian tasavalta;Albania};{République d'Albanie;Albanie};{Republika Albanija;Albanija};{Albán Köztársaság;Albánia};{Repubblica d'Albania;Albania};{アルバニア共和国;アルバニア};{알바니아 공화국;알바니아};{Republiek Albanië;Albanië};{جمهوری آلبانی;آلبانی};{Republika Albanii;Albania};{República da Albânia;Albânia};{Республика Албания;Албания};{Albánska republika;Albánsko};{República de Albania;Albania};{Republika Albanija;Albanija};{Republiken Albanien;Albanien};{Arnavutluk Cumhuriyeti;Arnavutluk};{جمہوریہ البانیا;البانیا};{阿尔巴尼亚共和国;阿尔巴尼亚}};[41;20];false;[MNE;GRC;MKD;UNK];28748;🇦🇱;{{Albanian;Albanian};{Albanaise;Albanais}}
{Andorra;Principality of Andorra;{cat:{official:Principat d'Andorra;common:Andorra}}};[.ad];AD;020;AND;AND;true;officially-assigned;true;Western European and Others Group;{EUR:{name:Euro;symbol:€}};{+3;[76]};[Andorra la Vella];[AD;Principality of Andorra;Principat d'Andorra];Europe;Southern Europe;{cat:Catalan};{{إمارة أندورا;أندورا};{Priñselezh Andorra;Andorra};{Andorrské knížectví;Andorra};{Fürstentum Andorra;Andorra};{Andorra Vürstiriik;Andorra};{Andorran ruhtinaskunta;Andorra};{Principauté d'Andorre;Andorre};{Kneževina Andora;Andora};{Andorra;Andorra};{Principato di Andorra;Andorra};{アンドラ公国;アンドラ};{안도라 공국;안도라};{Prinsdom Andorra;Andorra};{شاهزاده‌نشین آندورا;آندورا};{Księstwo Andory;Andora};{Principado de Andorra;Andorra};{Княжество Андорра;Андорра};{Andorrské kniežatstvo;Andorra};{Principado de Andorra;Andorra};{Kneževina Andora;Andora};{Furstendömet Andorra;Andorra};{Andorra Prensliği;Andorra};{اماراتِ انڈورا;انڈورا};{安道尔公国;安道尔}};[42.5;1.5];true;[FRA;ESP];468;🇦🇩;{{Andorran;Andorran};{Andorrane;Andorran}}
{United Arab Emirates;United Arab Emirates;{ara:{official:الإمارات العربية المتحدة;common:الإمارات}}};[.ae;امارات.];AE;784;ARE;UAE;true;officially-assigned;true;Asia and the Pacific Group;{AED:{name:United Arab Emirates dirham;symbol:د.إ}};{+9;[71]};[Abu Dhabi];[AE;UAE;Emirates];Asia;Western Asia;{ara:Arabic};{{الإمارات العربية المتحدة;الإمارات};{Emirelezhioù Arab Unanet;Emirelezhioù Arab Unanet};{Spojené arabské emiráty;Spojené arabské emiráty};{Vereinigte Arabische Emirate;Vereinigte Arabische Emirate};{Araabia Ühendemiraadid;Araabia Ühendemiraadid};{Yhdistyneet arabiemiirikunnat;Arabiemiraatit};{Émirats arabes unis;Émirats arabes unis};{Ujedinjeni Arapski Emirati;Ujedinjeni Arapski Emirati};{Egyesült Arab Emírségek;Egyesült Arab Emírségek};{Emirati Arabi Uniti;Emirati Arabi Uniti};{アラブ首長国連邦;UAE};{아랍 토후국 연방;아랍에미리트};{Verenigde Arabische Emiraten;Verenigde Arabische Emiraten};{امارات متحده عربی;امارات};{Zjednoczone Emiraty Arabskie;Zjednoczone Emiraty Arabskie};{Emirados Árabes Unidos;Emirados Árabes Unidos};{Объединенные Арабские Эмираты;Объединённые Арабские Эмираты};{Spojené arabské emiráty;Spojené arabské emiráty};{Emiratos Árabes Unidos;Emiratos Árabes Unidos};{Ujedinjeni Arapski Emirati;Ujedinjeni Arapski Emirati};{Förenade Arabemiraten;Förenade Arabemiraten};{Birleşik Arap Emirlikleri;Birleşik Arap Emirlikleri};{متحدہ عرب امارات;متحدہ عرب امارات};{阿拉伯联合酋长国;阿拉伯联合酋长国}};[24;54];false;[OMN;SAU];83600;🇦🇪;{{Emirati;Emirati};{Emirienne;Emirien}}
{Argentina;Argentine Republic;{grn:{official:Argentine Republic;common:Argentina};spa:{official:República Argentina;common:Argentina}}};[.ar];AR;032;ARG;ARG;true;officially-assigned;true;Latin American and Caribbean Group;{ARS:{name:Argentine peso;symbol:$}};{+5;[4]};[Buenos Aires];[AR;Argentine Republic;República Argentina];Americas;South America;{grn:Guaraní;spa:Spanish};{{جمهورية الأرجنتين;الأرجنتين};{Republik Arc'hantina;Arc'hantina};{Argentinská republika;Argentina};{Argentinische Republik;Argentinien};{Argentina Vabariik;Argentina};{Argentiinan tasavalta;Argentiina};{République argentine;Argentine};{Argentinski Republika;Argentina};{Argentin Köztársaság;Argentína};{Repubblica Argentina;Argentina};{アルゼンチン共和国;アルゼンチン};{아르헨티나 공화국;아르헨티나};{Argentijnse Republiek;Argentinië};{جمهوری آرژانتین;آرژانتین};{Republika Argentyńska;Argentyna};{República Argentina;Argentina};{Аргентинская Республика;Аргентина};{Argentínska republika;Argentína};{República Argentina;Argentina};{Republika Argentina;Argentina};{Republiken Argentina;Argentina};{Arjantin Cumhuriyeti;Arjantin};{جمہوریہ ارجنٹائن;ارجنٹائن};{阿根廷共和国;阿根廷}};[-34;-64];false;[BOL;BRA;CHL;PRY;URY];2780400;🇦🇷;{{Argentine;Argentine};{Argentine;Argentin}}
{Armenia;Republic of Armenia;{hye:{official:Հայաստանի Հանրապետություն;common:Հայաստան}}};[.am];AM;051;ARM;ARM;true;officially-assigned;true;Eastern European Group;{AMD:{name:Armenian dram;symbol:֏}};{+3;[74]};[Yerevan];[AM;Hayastan;Republic of Armenia;Հայաստանի Հանրապետություն];Asia;Western Asia;{hye:Armenian};{{جمهورية أرمينيا;أرمينيا};{Republik Armenia;Armenia};{Arménská republika;Arménie};{Republik Armenien;Armenien};{Armeenia Vabariik;Armeenia};{Armenian tasavalta;Armenia};{République d'Arménie;Arménie};{Republika Armenija;Armenija};{Örményország;Örményország};{Repubblica di Armenia;Armenia};{アルメニア共和国;アルメニア};{아르메니아 공화국;아르메니아};{Republiek Armenië;Armenië};{جمهوری ارمنستان;ارمنستان};{Republika Armenii;Armenia};{República da Arménia;Arménia};{Республика Армения;Армения};{Arménska republika;Arménsko};{República de Armenia;Armenia};{Republika Jermenija;Jermenija};{Republiken Armenien;Armenien};{Ermenistan Cumhuriyeti;Ermenistan};{جمہوریہ آرمینیا;آرمینیا};{亚美尼亚共和国;亚美尼亚}};[40;45];true;[AZE;GEO;IRN;TUR];29743;🇦🇲;{{Armenian;Armenian};{Arménienne;Arménien}}
{American Samoa;American Samoa;{eng:{official:American Samoa;common:American Samoa};smo:{official:Sāmoa Amelika;common:Sāmoa Amelika}}};[.as];AS;016;ASM;ASA;false;officially-assigned;false;;{USD:{name:United States dollar;symbol:$}};{+1;[684]};[Pago Pago];[AS;Amerika Sāmoa;Amelika Sāmoa;Sāmoa Amelika];Oceania;Polynesia;{eng:English;smo:Samoan};{{ساموا الأمريكية;ساموا الأمريكية};{Samoa Amerikan;Samoa Amerikan};{Americká Samoa;Americká Samoa};{Amerikanisch-Samoa;Amerikanisch-Samoa};{Ameerika Samoa;Ameerika Samoa};{Amerikan Samoa;Amerikan Samoa};{Samoa américaines;Samoa américaines};{američka Samoa;Američka Samoa};{Szamoa;Szamoa};{Samoa americane;Samoa Americane};{米領サモア;アメリカ領サモア};{아메리칸사모아;아메리칸사모아};{Amerikaans Samoa;Amerikaans Samoa};{ساموآی آمریکا;ساموآی آمریکا};{Samoa Amerykańskie;Samoa Amerykańskie};{Samoa americana;Samoa Americana};{американское Самоа;Американское Самоа};{Americká Samoa;Americká Samoa};{Samoa Americana;Samoa Americana};{Američka Samoa;Američka Samoa};{Amerikanska Samoa;Amerikanska Samoa};{Amerikan Samoası;Amerikan Samoası};{امریکی سمووا;امریکی سمووا};{美属萨摩亚;美属萨摩亚}};[-14.33333333;-170];false;[];199;🇦🇸;{{American Samoan;American Samoan};{Samoane;Samoan}}
{Antarctica;Antarctica;{}};[.aq];AQ;010;ATA;;false;officially-assigned;false;;{};{;[]};[];[AQ];Antarctic;;{};{{أنتارتيكا;أنتارتيكا};{Antarktika;Antarktika};{Antarktida;Antarktida};{Antarktika;Antarktis};{Antarktika;Antarktika};{Etelämanner;Etelämanner};{Antarctique;Antarctique};{Antarktika;Antarktika};{Antarktisz;Antarktisz};{Antartide;Antartide};{南極;南極大陸};{남극;남극};{Antarctica;Antarctica};{جنوبگان;جنوبگان};{Antarktyka;Antarktyka};{Antártica;Antártida};{Антарктида;Антарктида};{Antarktída;Antarktída};{Antártida;Antártida};{Antarktik;Antarktik};{Antarktis;Antarktis};{Antarktika;Antarktika};{انٹارکٹکا;انٹارکٹکا};{南极洲;南极洲}};[-90;0];false;[];14000000;🇦🇶;{{Antarctican;Antarctican};{Antarcticaine;Antarcticain}}
{French Southern and Antarctic Lands;Territory of the French Southern and Antarctic Lands;{fra:{official:Territoire des Terres australes et antarctiques françaises;common:Terres australes et antarctiques françaises}}};[.tf];TF;260;ATF;;false;officially-assigned;false;;{EUR:{name:Euro;symbol:€}};{+2;[62]};[Port-aux-Français];[TF;French Southern Territories];Antarctic;;{fra:French};{{مقاطعات وأقاليم ما وراء البحار الفرنسية;أراض فرنسية جنوبية وأنتارتيكية};{Tiriad Douaroù Aostral hag Antarktikel Frañs;Douaroù Aostral hag Antarktikel Frañs};{Teritorium Francouzská jižní a antarktická území;Francouzská jižní a antarktická území};{Gebiet der Französisch Süd- und Antarktisgebiete;Französische Süd- und Antarktisgebiete};{Prantsuse Lõunaalad;Prantsuse Lõunaalad};{Ranskan eteläiset ja antarktiset alueet;Ranskan eteläiset ja antarktiset alueet};{Territoire des Terres australes et antarctiques françaises;Terres australes et antarctiques françaises};{Teritoriju Francuski južni i antarktički teritoriji;Francuski južni i antarktički teritoriji};{Francia déli és antarktiszi területek;Francia déli és antarktiszi területek};{Territorio della australi e antartiche francesi Terre;Territori Francesi del Sud};{フランス領極南諸島;フランス領南方・南極地域};{프랑스령 남부와 남극 지역;프랑스령 남부와 남극 지역};{Grondgebied van de Franse Zuidelijke en Antarctische gebieden;Franse Gebieden in de zuidelijke Indische Oceaan};{سرزمین‌های جنوبی و جنوبگانی فرانسه;سرزمین‌های جنوبی و جنوبگانی فرانسه};{Francuskie Terytoria Południowe i Antarktyczne;Francuskie Terytoria Południowe i Antarktyczne};{Território do Sul e Antártica Francesa;Terras Austrais e Antárticas Francesas};{Территория Французские Южные и Антарктические земли;Французские Южные и Антарктические территории};{Francúzske južné a antarktické územia;Francúzske juŽné a antarktické územia};{Territorio del Francés Tierras australes y antárticas;Tierras Australes y Antárticas Francesas};{Francuske južne i antarktičke zemlje;Francuske južne i antarktičke zemlje};{Franska syd- och Antarktisterritorierna;Franska södra territorierna};{Fransız Güney ve Antarktika Toprakları;Fransız Güney ve Antarktika Toprakları};{سرزمینِ جنوبی فرانسیسیہ و انٹارکٹیکہ;سرزمین جنوبی فرانسیسیہ و انٹارکٹیکا};{法国南部和南极土地;法国南部和南极土地}};[-49.25;69.167];false;[];7747;🇹🇫;{{French;French};{Française;Français}}
{Antigua and Barbuda;Antigua and Barbuda;{eng:{official:Antigua and Barbuda;common:Antigua and Barbuda}}};[.ag];AG;028;ATG;ANT;true;officially-assigned;true;Latin American and Caribbean Group;{XCD:{name:Eastern Caribbean dollar;symbol:$}};{+1;[268]};[Saint John's];[AG];Americas;Caribbean;{eng:English};{{أنتيغوا وباربودا;أنتيغوا وباربودا};{Antigua ha Barbuda;Antigua ha Barbuda};{Antigua a Barbuda;Antigua a Barbuda};{Antigua und Barbuda;Antigua und Barbuda};{Antigua ja Barbuda;Antigua ja Barbuda};{Antigua ja Barbuda;Antigua ja Barbuda};{Antigua -et-Barbuda;Antigua-et-Barbuda};{Antigva i Barbuda;Antigva i Barbuda};{Antigua és Barbuda;Antigua és Barbuda};{Antigua e Barbuda;Antigua e Barbuda};{アンティグア・バーブーダ;アンティグア・バーブーダ};{앤티가 바부다;앤티가 바부다};{Antigua en Barbuda;Antigua en Barbuda};{آنتیگوا و باربودا;آنتیگوا و باربودا};{Antigua i Barbuda;Antigua i Barbuda};{Antigua e Barbuda;Antígua e Barbuda};{Антигуа и Барбуда;Антигуа и Барбуда};{Antigua a Barbuda;Antigua a Barbuda};{Antigua y Barbuda;Antigua y Barbuda};{Antigva i Barbuda;Antigva i Barbuda};{Antigua och Barbuda;Antigua och Barbuda};{Antigua ve Barbuda;Antigua ve Barbuda};{اینٹیگوا و باربوڈا;اینٹیگوا و باربوڈا};{安提瓜和巴布达;安提瓜和巴布达}};[17.05;-61.8];false;[];442;🇦🇬;{{Antiguan, Barbudan;Antiguan, Barbudan};{Antiguaise et barbudienne;Antiguaise et barbudien}}
{Australia;Commonwealth of Australia;{eng:{official:Commonwealth of Australia;common:Australia}}};[.au];AU;036;AUS;AUS;true;officially-assigned;true;Western European and Others Group;{AUD:{name:Australian dollar;symbol:$}};{+6;[1]};[Canberra];[AU];Oceania;Australia and New Zealand;{eng:English};{{كومونولث أستراليا;أستراليا};{Kenglad Aostralia;Aostralia};{Australské společenství;Austrálie};{Commonwealth Australien;Australien};{Austraalia Ühendus;Austraalia};{Australian liittovaltio;Australia};{Australie;Australie};{Commonwealth of Australia;Australija};{Ausztrál Államszövetség;Ausztrália};{Commonwealth dell'Australia;Australia};{オーストラリア連邦;オーストラリア};{오스트레일리아 연방;호주};{Gemenebest van Australië;Australië};{قلمرو همسود استرالیا;استرالیا};{Związek Australijski;Australia};{Comunidade da Austrália;Austrália};{Содружество Австралии;Австралия};{Austrálsky zväz;Austrália};{Mancomunidad de Australia;Australia};{Komonvelt Australija;Australija};{Australiska statsförbundet;Australien};{Avustralya Federal Devleti;Avustralya};{دولتِ مشترکہ آسٹریلیا;آسٹریلیا};{澳大利亚联邦;澳大利亚}};[-27;133];false;[];7692024;🇦🇺;{{Australian;Australian};{Australienne;Australien}}
{Austria;Republic of Austria;{bar:{official:Republik Österreich;common:Österreich}}};[.at];AT;040;AUT;AUT;true;officially-assigned;true;Western European and Others Group;{EUR:{name:Euro;symbol:€}};{+4;[3]};[Vienna];[AT;Osterreich;Oesterreich];Europe;Central Europe;{bar:Austro-Bavarian German};{{جمهورية النمسا;النمسا};{Republik Aostria;Aostria};{Rakouská republika;Rakousko};{Republik Österreich;Österreich};{Austria Vabariik;Austria};{Itävallan tasavalta;Itävalta};{République d'Autriche;Autriche};{Republika Austrija;Austrija};{Ausztria;Ausztria};{Repubblica d'Austria;Austria};{オーストリア共和国;オーストリア};{오스트리아 공화국;오스트리아};{Republiek Oostenrijk;Oostenrijk};{جمهوری اتریش;اتریش};{Republika Austrii;Austria};{República da Áustria;Áustria};{Австрийская Республика;Австрия};{Rakúska republika;Rakúsko};{República de Austria;Austria};{Republika Austrija;Austrija};{Republiken Österrike;Österrike};{Avusturya Cumhuriyeti;Avusturya};{جمہوریہ آسٹریا;آسٹریا};{奥地利共和国;奥地利}};[47.33333333;13.33333333];true;[CZE;DEU;HUN;ITA;LIE;SVK;SVN;CHE];83871;🇦🇹;{{Austrian;Austrian};{Autrichienne;Autrichien}}
{Azerbaijan;Republic of Azerbaijan;{aze:{official:Azərbaycan Respublikası;common:Azərbaycan};rus:{official:Азербайджанская Республика;common:Азербайджан}}};[.az];AZ;031;AZE;AZE;true;officially-assigned;true;Eastern European Group;{AZN:{name:Azerbaijani manat;symbol:₼}};{+9;[94]};[Baku];[AZ;Republic of Azerbaijan;Azərbaycan Respublikası];Asia;Western Asia;{aze:Azerbaijani;rus:Russian};{{جمهورية أذربيجان;أذربيجان};{Republik Azerbaidjan;Azerbaidjan};{Ázerbájdžánská republika;Ázerbájdžán};{Republik Aserbaidschan;Aserbaidschan};{Aserbaidžaani Vabariik;Aserbaidžaan};{Azerbaidzanin tasavalta;Azerbaidzan};{République d'Azerbaïdjan;Azerbaïdjan};{Republika Azerbajdžan;Azerbajdžan};{Azerbajdzsán;Azerbajdzsán};{Repubblica dell'Azerbaigian;Azerbaijan};{アゼルバイジャン共和国;アゼルバイジャン};{아제르바이잔 공화국;아제르바이잔};{Republiek Azerbeidzjan;Azerbeidzjan};{جمهوری آذربایجان;جمهوری آذربایجان};{Republika Azerbejdżanu;Azerbejdżan};{República do Azerbaijão;Azerbeijão};{Азербайджанская Республика;Азербайджан};{Azerbajǆanská republika;AzerbajǇan};{República de Azerbaiyán;Azerbaiyán};{Republika Azerbejdžan;Azerbejdžan};{Republiken Azerbajdzjan;Azerbajdzjan};{Azerbaycan Cumhuriyeti;Azerbaycan};{جمہوریہ آذربائیجان;آذربائیجان};{阿塞拜疆共和国;阿塞拜疆}};[40.5;47.5];true;[ARM;GEO;IRN;RUS;TUR];86600;🇦🇿;{{Azerbaijani;Azerbaijani};{Azerbaïdjanaise;Azerbaïdjanais}}
{Burundi;Republic of Burundi;{fra:{official:République du Burundi;common:Burundi};run:{official:Republika y'Uburundi ;common:Uburundi}}};[.bi];BI;108;BDI;BDI;true;officially-assigned;true;African Group;{BIF:{name:Burundian franc;symbol:Fr}};{+2;[57]};[Gitega];[BI;Republic of Burundi;Republika y'Uburundi;République du Burundi];Africa;Eastern Africa;{fra:French;run:Kirundi};{{جمهورية بوروندي;بوروندي};{Republik Burundi;Burundi};{Burundská republika;Burundi};{Republik Burundi;Burundi};{Burundi Vabariik;Burundi};{Burundin tasavalta;Burundi};{République du Burundi;Burundi};{Burundi;Burundi};{Burundi;Burundi};{Repubblica del Burundi;Burundi};{ブルンジ共和国;ブルンジ};{부룬디;부룬디};{Republiek Burundi;Burundi};{جمهوری بوروندی;بوروندی};{Republika Burundi;Burundi};{República do Burundi;Burundi};{Республика Бурунди;Бурунди};{Burundská republika;Burundi};{República de Burundi;Burundi};{Republika Burundi;Burundi};{Republiken Burundi;Burundi};{Burundi Cumhuriyeti;Burundi};{جمہوریہ برونڈی;برونڈی};{布隆迪共和国;布隆迪}};[-3.5;30];true;[COD;RWA;TZA];27834;🇧🇮;{{Burundian;Burundian};{Burundaise;Burundais}}
{Belgium;Kingdom of Belgium;{deu:{official:Königreich Belgien;common:Belgien};fra:{official:Royaume de Belgique;common:Belgique};nld:{official:Koninkrijk België;common:België}}};[.be];BE;056;BEL;BEL;true;officially-assigned;true;Western European and Others Group;{EUR:{name:Euro;symbol:€}};{+3;[2]};[Brussels];[BE;België;Belgie;Belgien;Belgique;Kingdom of Belgium;Koninkrijk België;Royaume de Belgique;Königreich Belgien];Europe;Western Europe;{deu:German;fra:French;nld:Dutch};{{مملكة بلجيكا;بلجيكا};{Rouantelezh Belgia;Belgia};{Belgické království;Belgie};{Königreich Belgien;Belgien};{Belgia Kuningriik;Belgia};{Belgian kuningaskunta;Belgia};{Royaume de Belgique;Belgique};{Kraljevina Belgija;Belgija};{Belga Királyság;Belgium};{Regno del Belgio;Belgio};{ベルギー王国;ベルギー};{벨기에 왕국;벨기에};{Koninkrijk België;België};{پادشاهی بلژیک;بلژیک};{Królestwo Belgii;Belgia};{Reino da Bélgica;Bélgica};{Королевство Бельгия;Бельгия};{Belgické kráľovstvo;Belgicko};{Reino de Bélgica;Bélgica};{Kraljevina Belgija;Belgija};{Konungariket Belgien;Belgien};{Belçika Krallığı;Belçika};{مملکتِ بلجئیم;بلجئیم};{比利时王国;比利时}};[50.83333333;4];false;[FRA;DEU;LUX;NLD];30528;🇧🇪;{{Belgian;Belgian};{Belge;Belge}}
{Benin;Republic of Benin;{fra:{official:République du Bénin;common:Bénin}}};[.bj];BJ;204;BEN;BEN;true;officially-assigned;true;African Group;{XOF:{name:West African CFA franc;symbol:Fr}};{+2;[29]};[Porto-Novo];[BJ;Republic of Benin;République du Bénin];Africa;Western Africa;{fra:French};{{جمهورية بنين;بنين};{Republik Benin;Benin};{Beninská republika;Benin};{Republik Benin;Benin};{Benini Vabariik;Benin};{Beninin tasavalta;Benin};{République du Bénin;Bénin};{Republika Benin;Benin};{Benini Köztársaság;Benin};{Repubblica del Benin;Benin};{ベナン共和国;ベナン};{베냉 공화국;베냉};{Republiek Benin;Benin};{جمهوری بنین;بنین};{Benin;Benin};{República do Benin;Benin};{Республика Бенин;Бенин};{Beninská republika;Benin};{República de Benin;Benín};{Republika Benin;Benin};{Republiken Benin;Benin};{Benin Cumhuriyeti;Benin};{جمہوریہ بینن;بینن};{贝宁共和国;贝宁}};[9.5;2.25];false;[BFA;NER;NGA;TGO];112622;🇧🇯;{{Beninese;Beninese};{Béninoise;Béninois}}
{Burkina Faso;Burkina Faso;{fra:{official:République du Burkina;common:Burkina Faso}}};[.bf];BF;854;BFA;BUR;true;officially-assigned;true;African Group;{XOF:{name:West African CFA franc;symbol:Fr}};{+2;[26]};[Ouagadougou];[BF];Africa;Western Africa;{fra:French};{{بوركينا فاسو;بوركينا فاسو};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{République du Burkina;Burkina Faso};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina};{Burkina Faso;Burkina Faso};{ブルキナファソ;ブルキナファソ};{부르키나파소;부르키나파소};{Burkina Faso;Burkina Faso};{بورکینافاسو;بورکینافاسو};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{Буркина -Фасо;Буркина-Фасо};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{Burkina Faso;Burkina Faso};{برکینا فاسو;برکینا فاسو};{布基纳法索;布基纳法索}};[13;-2];true;[BEN;CIV;GHA;MLI;NER;TGO];272967;🇧🇫;{{Burkinabe;Burkinabe};{Burkinabée;Burkinabé}}
{Bangladesh;People's Republic of Bangladesh;{ben:{official:বাংলাদেশ গণপ্রজাতন্ত্রী;common:বাংলাদেশ}}};[.bd];BD;050;BGD;BAN;true;officially-assigned;true;Asia and the Pacific Group;{BDT:{name:Bangladeshi taka;symbol:৳}};{+8;[80]};[Dhaka];[BD;People's Republic of Bangladesh;Gônôprôjatôntri Bangladesh];Asia;Southern Asia;{ben:Bengali};{{جمهورية بنغلاديش الشعبية;بنغلاديش};{Republik pobl Bangladesh;Bangladesh};{Bangladéšská lidová republika;Bangladéš};{Volksrepublik Bangladesch;Bangladesch};{Bangladeshi Rahvavabariik;Bangladesh};{Bangladeshin kansantasavalta;Bangladesh};{La République populaire du Bangladesh;Bangladesh};{Narodna Republika Bangladeš;Bangladeš};{Banglades;Banglades};{Repubblica popolare del Bangladesh;Bangladesh};{バングラデシュ人民共和国;バングラデシュ};{방글라데시 인민 공화국;방글라데시};{Volksrepubliek Bangladesh;Bangladesh};{جمهوری خلق بنگلادش;بنگلادش};{Ludowa Republika Bangladeszu;Bangladesz};{República Popular do Bangladesh;Bangladesh};{Народная Республика Бангладеш;Бангладеш};{Bangladéšska ľudová republika;Bangladéš};{República Popular de Bangladesh;Bangladesh};{Narodna Republika Bangladeš;Bangladeš};{Folkrepubliken Bangladesh;Bangladesh};{Bangladeş Halk Cumhuriyeti;Bangladeş};{عوامی جمہوریہ بنگلہ دیش;بنگلہ دیش};{孟加拉人民共和国;孟加拉国}};[24;90];false;[MMR;IND];147570;🇧🇩;{{Bangladeshi;Bangladeshi};{Bangladaise;Bangladais}}
{Bulgaria;Republic of Bulgaria;{bul:{official:Република България;common:България}}};[.bg];BG;100;BGR;BUL;true;officially-assigned;true;Eastern European Group;{BGN:{name:Bulgarian lev;symbol:лв}};{+3;[59]};[Sofia];[BG;Republic of Bulgaria;Република България];Europe;Southeast Europe;{bul:Bulgarian};{{جمهورية بلغاريا;بلغاريا};{Republik Bulgaria;Bulgaria};{Bulharská republika;Bulharsko};{Republik Bulgarien;Bulgarien};{Bulgaaria Vabariik;Bulgaaria};{Bulgarian tasavalta;Bulgaria};{République de Bulgarie;Bulgarie};{Republika Bugarska;Bugarska};{Bolgár Köztársaság;Bulgária};{Repubblica di Bulgaria;Bulgaria};{ブルガリア共和国;ブルガリア};{불가리아 공화국;불가리아};{Republiek Bulgarije;Bulgarije};{جمهوری بلغارستان;بلغارستان};{Republika Bułgarii;Bułgaria};{República da Bulgária;Bulgária};{Республика Болгария;Болгария};{Bulharská republika;Bulharsko};{República de Bulgaria;Bulgaria};{Republika Bugarska;Bugarska};{Republiken Bulgarien;Bulgarien};{Bulgaristan Cumhuriyeti;Bulgaristan};{جمہوریہ بلغاریہ;بلغاریہ};{保加利亚共和国;保加利亚}};[43;25];false;[GRC;MKD;ROU;SRB;TUR];110879;🇧🇬;{{Bulgarian;Bulgarian};{Bulgare;Bulgare}}
{Bahrain;Kingdom of Bahrain;{ara:{official:مملكة البحرين;common:البحرين}}};[.bh];BH;048;BHR;BRN;true;officially-assigned;true;Asia and the Pacific Group;{BHD:{name:Bahraini dinar;symbol:.د.ب}};{+9;[73]};[Manama];[BH;Kingdom of Bahrain;Mamlakat al-Baḥrayn];Asia;Western Asia;{ara:Arabic};{{مملكة البحرين;البحرين};{Rouantelezh Bahrein;Bahrein};{Království Bahrajn;Bahrajn};{Königreich Bahrain;Bahrain};{Bahreini Kuningriik;Bahrein};{Bahrainin kuningaskunta;Bahrain};{Royaume de Bahreïn;Bahreïn};{Kraljevina Bahrein;Bahrein};{Bahreini Királyság;Bahrein};{Regno del Bahrain;Bahrein};{バーレーン王国;バーレーン};{바레인 왕국;바레인};{Koninkrijk Bahrein;Bahrein};{پادشاهی بحرین;بحرین};{Królestwo Bahrajnu;Bahrajn};{Reino do Bahrein;Bahrein};{Королевство Бахрейн;Бахрейн};{Bahrajnské kráľovstvo;Bahrajn};{Reino de Bahrein;Bahrein};{Kraljevina Bahrein;Bahrein};{Konungariket Bahrain;Bahrain};{Bahreyn Krallığı;Bahreyn};{مملکتِ بحرین;بحرین};{巴林王国;巴林}};[26;50.55];false;[];765;🇧🇭;{{Bahraini;Bahraini};{Bahreïnienne;Bahreïnien}}
... (truncated)
```

---

## large_non_uniform_nested_mixed.json

Original size (JSON pretty): **2402 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 2402 | 1292 | 1003 | 816 | 801 | 978.0 | 2.5 |
| JSON (min) | 1500 | 446 | 522 | 449 | 456 | 468.2 | 5.1 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 1573 | 661 | 617 | 559 | 532 | 592.2 | 4.1 |
| TOON | 1766 | 841 | 625 | 572 | 544 | 645.5 | 3.7 |
| TSON | 1275 | 525 | 560 | 462 | 488 | 508.8 | 4.7 |
| minemizer | 1203 | 383 | 452 | 400 | 388 | 405.8 | 5.9 |
| minemizer (compact) | 1072 | 409 | 462 | 382 | 384 | 409.2 | 5.9 |

### Serialized outputs

**JSON (pretty)** (2402 chars, 978 tokens):
```json
[
  {
    "id": 1,
    "name": "Alice",
    "work": {
      "title": "Senior Engineer",
      "years": 5,
      "remote": true,
      "team": "Platform"
    },
    "contact": {
      "email": "alice@co.com"
    }
  },
  {
    "id": 2,
    "profile": {
      "age": 28,
      "city": "NYC",
      "verified": true
    },
    "status": "active",
    "permissions": {
      "admin": false,
      "editor": true
... (truncated)
```

**JSON (min)** (1500 chars, 468 tokens):
```json
[{"id":1,"name":"Alice","work":{"title":"Senior Engineer","years":5,"remote":true,"team":"Platform"},"contact":{"email":"alice@co.com"}},{"id":2,"profile":{"age":28,"city":"NYC","verified":true},"status":"active","permissions":{"admin":false,"editor":true}},{"id":3,"name":"Charlie","contact":{"email":"c@example.com","preferred":"email","phone":"555-0103"},"metadata":{"created":"2019-06-10"}},{"id":4,"user":{"username":"diana","role":"admin","level":5},"metadata":{"created":"2020-09-01","updated":"2024-01-20"},"settings":{"theme":"dark"}},{"id":5,"employee":{"name":"Eve Adams","department":"Sales"},"performance":{"score":85,"reviews":3},"contact":{"email":"eve@co.com","slack":"@eve"}},{"id":6,"name":"Frank","work":{"title":"Product Manager","years":8,"remote":false,"team":"Growth"},"contact":{"email":"frank@co.com","phone":"555-0106"}},{"id":7,"profile":{"age":35,"city":"LA","verified":false},"status":"inactive","permissions":{"admin":true,"editor":false},"metadata":{"created":"2018-03-15"}},{"id":8,"name":"Grace","contact":{"email":"grace@example.org","preferred":"slack","slack":"@grace"},"settings":{"theme":"light","notifications":true}},{"id":9,"user":{"username":"henry","role":"viewer","level":2},"employee":{"name":"Henry Wilson","department":"Marketing"},"performance":{"score":72,"reviews":5}},{"id":10,"name":"Iris","work":{"title":"Designer","years":3,"remote":true,"team":"Creative"},"profile":{"age":26,"city":"Austin","verified":true},"contact":{"email":"iris@co.com"}}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (1573 chars, 592 tokens):
```yaml
- contact:
    email: alice@co.com
  id: 1
  name: Alice
  work:
    remote: true
    team: Platform
    title: Senior Engineer
    years: 5
- id: 2
  permissions:
    admin: false
    editor: true
  profile:
    age: 28
    city: NYC
    verified: true
  status: active
- contact:
    email: c@example.com
    phone: 555-0103
    preferred: email
  id: 3
  metadata:
    created: '2019-06-10'
... (truncated)
```

**TOON** (1766 chars, 646 tokens):
```toon
[10]:
  - id: 1
    name: Alice
    work:
      title: Senior Engineer
      years: 5
      remote: true
      team: Platform
    contact:
      email: alice@co.com
  - id: 2
    profile:
      age: 28
      city: NYC
      verified: true
    status: active
    permissions:
      admin: false
      editor: true
  - id: 3
    name: Charlie
    contact:
      email: c@example.com
      preferred: email
      phone: 555-0103
... (truncated)
```

**TSON** (1275 chars, 509 tokens):
```tson
[{@id,name,work,contact|1,Alice,{@title,years,remote,team|"Senior Engineer",5,true,Platform},{@email|"alice@co.com"}},{@id,profile,status,permissions|2,{@age,city,verified|28,NYC,true},active,{@admin,editor|false,true}},{@id,name,contact,metadata|3,Charlie,{@email,preferred,phone|"c@example.com",email,555-0103},{@created|2019-06-10}},{@id,user,metadata,settings|4,{@username,role,level|diana,admin,5},{@created,updated|2020-09-01,2024-01-20},{@theme|dark}},{@id,employee,performance,contact|5,{@name,department|"Eve Adams",Sales},{@score,reviews|85,3},{@email,slack|"eve@co.com","@eve"}},{@id,name,work,contact|6,Frank,{@title,years,remote,team|"Product Manager",8,false,Growth},{@email,phone|"frank@co.com",555-0106}},{@id,profile,status,permissions,metadata|7,{@age,city,verified|35,LA,false},inactive,{@admin,editor|true,false},{@created|2018-03-15}},{@id,name,contact,settings|8,Grace,{@email,preferred,slack|"grace@example.org",slack,"@grace"},{@theme,notifications|light,true}},{@id,user,employee,performance|9,{@username,role,level|henry,viewer,2},{@name,department|"Henry Wilson",Marketing},{@score,reviews|72,5}},{@id,name,work,profile,contact|10,Iris,{@title,years,remote,team|Designer,3,true,Creative},{@age,city,verified|26,Austin,true},{@email|"iris@co.com"}}]
```

**minemizer** (1203 chars, 406 tokens):
```txt
id; name; contact{ email; ...}
1; Alice;{ alice@co.com}; work{ title: Senior Engineer; years: 5; remote:true; team: Platform}
2;;; profile{ age: 28; city: NYC; verified:true}; status: active; permissions{ admin:false; editor:true}
3; Charlie;{ c@example.com; preferred: email; phone: 555-0103}; metadata{ created: 2019-06-10}
4;;; user{ username: diana; role: admin; level: 5}; metadata{ created: 2020-09-01; updated: 2024-01-20}; settings{ theme: dark}
5;;{ eve@co.com; slack: @eve}; employee{ name: Eve Adams; department: Sales}; performance{ score: 85; reviews: 3}
6; Frank;{ frank@co.com; phone: 555-0106}; work{ title: Product Manager; years: 8; remote:false; team: Growth}
7;;; profile{ age: 35; city: LA; verified:false}; status: inactive; permissions{ admin:true; editor:false}; metadata{ created: 2018-03-15}
8; Grace;{ grace@example.org; preferred: slack; slack: @grace}; settings{ theme: light; notifications:true}
9;;; user{ username: henry; role: viewer; level: 2}; employee{ name: Henry Wilson; department: Marketing}; performance{ score: 72; reviews: 5}
10; Iris;{ iris@co.com}; work{ title: Designer; years: 3; remote:true; team: Creative}; profile{ age: 26; city: Austin; verified:true}
```

**minemizer (compact)** (1072 chars, 409 tokens):
```txt
id;name;contact{email;...}
1;Alice;{alice@co.com};work{title:Senior Engineer;years:5;remote:true;team:Platform}
2;;;profile{age:28;city:NYC;verified:true};status:active;permissions{admin:false;editor:true}
3;Charlie;{c@example.com;preferred:email;phone:555-0103};metadata{created:2019-06-10}
4;;;user{username:diana;role:admin;level:5};metadata{created:2020-09-01;updated:2024-01-20};settings{theme:dark}
5;;{eve@co.com;slack:@eve};employee{name:Eve Adams;department:Sales};performance{score:85;reviews:3}
6;Frank;{frank@co.com;phone:555-0106};work{title:Product Manager;years:8;remote:false;team:Growth}
7;;;profile{age:35;city:LA;verified:false};status:inactive;permissions{admin:true;editor:false};metadata{created:2018-03-15}
8;Grace;{grace@example.org;preferred:slack;slack:@grace};settings{theme:light;notifications:true}
9;;;user{username:henry;role:viewer;level:2};employee{name:Henry Wilson;department:Marketing};performance{score:72;reviews:5}
10;Iris;{iris@co.com};work{title:Designer;years:3;remote:true;team:Creative};profile{age:26;city:Austin;verified:true}
```

---

## large_non_uniform_nested_numerical.json

Original size (JSON pretty): **2947 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 2947 | 1718 | 1542 | 1332 | 1169 | 1440.2 | 2.0 |
| JSON (min) | 1873 | 755 | 976 | 884 | 748 | 840.8 | 3.5 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 2085 | 1033 | 1171 | 1077 | 893 | 1043.5 | 2.8 |
| TOON | 2318 | 1249 | 1178 | 1090 | 905 | 1105.5 | 2.7 |
| TSON | 1642 | 823 | 993 | 907 | 746 | 867.2 | 3.4 |
| minemizer | 1534 | 632 | 940 | 883 | 698 | 788.2 | 3.7 |
| minemizer (compact) | 1361 | 676 | 875 | 809 | 641 | 750.2 | 3.9 |

### Serialized outputs

**JSON (pretty)** (2947 chars, 1440 tokens):
```json
[
  {
    "id": 1,
    "metrics": {
      "views": 15420,
      "clicks": 842,
      "ctr": 0.0546,
      "bounce_rate": 0.32
    },
    "revenue": {
      "amount": 12499.99,
      "currency_rate": 1.0
    },
    "timestamp": "2024-01-15T09:30:00Z"
  },
  {
    "id": 2,
    "metrics": {
      "views": 8923,
      "clicks": 156,
      "ctr": 0.0175,
      "bounce_rate": 0.67
    },
    "stats": {
      "avg_time": 45.7,
... (truncated)
```

**JSON (min)** (1873 chars, 841 tokens):
```json
[{"id":1,"metrics":{"views":15420,"clicks":842,"ctr":0.0546,"bounce_rate":0.32},"revenue":{"amount":12499.99,"currency_rate":1.0},"timestamp":"2024-01-15T09:30:00Z"},{"id":2,"metrics":{"views":8923,"clicks":156,"ctr":0.0175,"bounce_rate":0.67},"stats":{"avg_time":45.7,"pages_per_session":2.3,"return_rate":0.15},"timestamp":"2024-01-16T14:22:33Z"},{"id":3,"revenue":{"amount":8750.5,"tax":700.04,"net":8050.46,"currency_rate":0.92},"inventory":{"count":342,"reserved":28,"available":314}},{"id":4,"metrics":{"views":52100,"clicks":3891,"ctr":0.0747,"bounce_rate":0.21},"performance":{"latency_ms":127.5,"uptime":0.9987,"errors":3},"timestamp":"2024-01-17T08:00:00Z"},{"id":5,"stats":{"avg_time":128.9,"pages_per_session":5.7,"return_rate":0.42},"scores":{"quality":94,"relevance":87,"engagement":0.78},"dates":{"start":"2023-06-01","end":"2024-01-31"}},{"id":6,"inventory":{"count":1205,"reserved":89,"available":1116,"reorder_point":200},"pricing":{"cost":24.99,"markup":0.35,"price":33.74},"timestamp":"2024-01-18T11:45:12Z"},{"id":7,"metrics":{"views":3156,"clicks":98,"ctr":0.031,"bounce_rate":0.55},"revenue":{"amount":2150.0,"tax":172.0,"net":1978.0},"performance":{"latency_ms":89.2,"uptime":0.9995,"errors":0}},{"id":8,"scores":{"quality":78,"relevance":92,"engagement":0.65,"nps":45},"dates":{"start":"2022-11-15","end":"2024-02-28","renewal":"2024-03-01"},"budget":{"allocated":50000,"spent":42350.75,"remaining":7649.25}},{"id":9,"pricing":{"cost":149.99,"markup":0.28,"price":191.99,"discount":0.1},"inventory":{"count":56,"reserved":12,"available":44},"timestamp":"2024-01-19T16:30:45Z"},{"id":10,"metrics":{"views":128750,"clicks":9823,"ctr":0.0763,"bounce_rate":0.18},"stats":{"avg_time":312.4,"pages_per_session":8.2,"return_rate":0.58},"budget":{"allocated":125000,"spent":98420.33,"remaining":26579.67},"dates":{"start":"2023-01-01","end":"2024-12-31"}}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (2085 chars, 1044 tokens):
```yaml
- id: 1
  metrics:
    bounce_rate: 0.32
    clicks: 842
    ctr: 0.0546
    views: 15420
  revenue:
    amount: 12499.99
    currency_rate: 1.0
  timestamp: '2024-01-15T09:30:00Z'
- id: 2
  metrics:
    bounce_rate: 0.67
    clicks: 156
    ctr: 0.0175
    views: 8923
  stats:
    avg_time: 45.7
    pages_per_session: 2.3
    return_rate: 0.15
  timestamp: '2024-01-16T14:22:33Z'
- id: 3
  inventory:
    available: 314
    count: 342
... (truncated)
```

**TOON** (2318 chars, 1106 tokens):
```toon
[10]:
  - id: 1
    metrics:
      views: 15420
      clicks: 842
      ctr: 0.0546
      bounce_rate: 0.32
    revenue:
      amount: 12499.99
      currency_rate: 1.0
    timestamp: "2024-01-15T09:30:00Z"
  - id: 2
    metrics:
      views: 8923
      clicks: 156
      ctr: 0.0175
      bounce_rate: 0.67
    stats:
      avg_time: 45.7
      pages_per_session: 2.3
      return_rate: 0.15
    timestamp: "2024-01-16T14:22:33Z"
  - id: 3
    revenue:
      amount: 8750.5
... (truncated)
```

**TSON** (1642 chars, 867 tokens):
```tson
[{@id,metrics,revenue,timestamp|1,{@views,clicks,ctr,bounce_rate|15420,842,0.0546,0.32},{@amount,currency_rate|12499.99,1.0},2024-01-15T09:30:00Z},{@id,metrics,stats,timestamp|2,{@views,clicks,ctr,bounce_rate|8923,156,0.0175,0.67},{@avg_time,pages_per_session,return_rate|45.7,2.3,0.15},2024-01-16T14:22:33Z},{@id,revenue,inventory|3,{@amount,tax,net,currency_rate|8750.5,700.04,8050.46,0.92},{@count,reserved,available|342,28,314}},{@id,metrics,performance,timestamp|4,{@views,clicks,ctr,bounce_rate|52100,3891,0.0747,0.21},{@latency_ms,uptime,errors|127.5,0.9987,3},2024-01-17T08:00:00Z},{@id,stats,scores,dates|5,{@avg_time,pages_per_session,return_rate|128.9,5.7,0.42},{@quality,relevance,engagement|94,87,0.78},{@start,end|2023-06-01,2024-01-31}},{@id,inventory,pricing,timestamp|6,{@count,reserved,available,reorder_point|1205,89,1116,200},{@cost,markup,price|24.99,0.35,33.74},2024-01-18T11:45:12Z},{@id,metrics,revenue,performance|7,{@views,clicks,ctr,bounce_rate|3156,98,0.031,0.55},{@amount,tax,net|2150.0,172.0,1978.0},{@latency_ms,uptime,errors|89.2,0.9995,0}},{@id,scores,dates,budget|8,{@quality,relevance,engagement,nps|78,92,0.65,45},{@start,end,renewal|2022-11-15,2024-02-28,2024-03-01},{@allocated,spent,remaining|50000,42350.75,7649.25}},{@id,pricing,inventory,timestamp|9,{@cost,markup,price,discount|149.99,0.28,191.99,0.1},{@count,reserved,available|56,12,44},2024-01-19T16:30:45Z},{@id,metrics,stats,budget,dates|10,{@views,clicks,ctr,bounce_rate|128750,9823,0.0763,0.18},{@avg_time,pages_per_session,return_rate|312.4,8.2,0.58},{@allocated,spent,remaining|125000,98420.33,26579.67},{@start,end|2023-01-01,2024-12-31}}]
```

**minemizer** (1534 chars, 788 tokens):
```txt
id; metrics{ views; clicks; ctr; bounce_rate}; timestamp
1;{ 15420; 842; 0.0546; 0.32}; 2024-01-15T09:30:00Z; revenue{ amount: 12499.99; currency_rate: 1.0}
2;{ 8923; 156; 0.0175; 0.67}; 2024-01-16T14:22:33Z; stats{ avg_time: 45.7; pages_per_session: 2.3; return_rate: 0.15}
3;;; revenue{ amount: 8750.5; tax: 700.04; net: 8050.46; currency_rate: 0.92}; inventory{ count: 342; reserved: 28; available: 314}
4;{ 52100; 3891; 0.0747; 0.21}; 2024-01-17T08:00:00Z; performance{ latency_ms: 127.5; uptime: 0.9987; errors: 3}
5;;; stats{ avg_time: 128.9; pages_per_session: 5.7; return_rate: 0.42}; scores{ quality: 94; relevance: 87; engagement: 0.78}; dates{ start: 2023-06-01; end: 2024-01-31}
6;; 2024-01-18T11:45:12Z; inventory{ count: 1205; reserved: 89; available: 1116; reorder_point: 200}; pricing{ cost: 24.99; markup: 0.35; price: 33.74}
7;{ 3156; 98; 0.031; 0.55};; revenue{ amount: 2150.0; tax: 172.0; net: 1978.0}; performance{ latency_ms: 89.2; uptime: 0.9995; errors: 0}
8;;; scores{ quality: 78; relevance: 92; engagement: 0.65; nps: 45}; dates{ start: 2022-11-15; end: 2024-02-28; renewal: 2024-03-01}; budget{ allocated: 50000; spent: 42350.75; remaining: 7649.25}
9;; 2024-01-19T16:30:45Z; pricing{ cost: 149.99; markup: 0.28; price: 191.99; discount: 0.1}; inventory{ count: 56; reserved: 12; available: 44}
10;{ 128750; 9823; 0.0763; 0.18};; stats{ avg_time: 312.4; pages_per_session: 8.2; return_rate: 0.58}; budget{ allocated: 125000; spent: 98420.33; remaining: 26579.67}; dates{ start: 2023-01-01; end: 2024-12-31}
```

**minemizer (compact)** (1361 chars, 750 tokens):
```txt
id;metrics{views;clicks;ctr;bounce_rate};timestamp
1;{15420;842;0.0546;0.32};2024-01-15T09:30:00Z;revenue{amount:12499.99;currency_rate:1.0}
2;{8923;156;0.0175;0.67};2024-01-16T14:22:33Z;stats{avg_time:45.7;pages_per_session:2.3;return_rate:0.15}
3;;;revenue{amount:8750.5;tax:700.04;net:8050.46;currency_rate:0.92};inventory{count:342;reserved:28;available:314}
4;{52100;3891;0.0747;0.21};2024-01-17T08:00:00Z;performance{latency_ms:127.5;uptime:0.9987;errors:3}
5;;;stats{avg_time:128.9;pages_per_session:5.7;return_rate:0.42};scores{quality:94;relevance:87;engagement:0.78};dates{start:2023-06-01;end:2024-01-31}
6;;2024-01-18T11:45:12Z;inventory{count:1205;reserved:89;available:1116;reorder_point:200};pricing{cost:24.99;markup:0.35;price:33.74}
7;{3156;98;0.031;0.55};;revenue{amount:2150.0;tax:172.0;net:1978.0};performance{latency_ms:89.2;uptime:0.9995;errors:0}
8;;;scores{quality:78;relevance:92;engagement:0.65;nps:45};dates{start:2022-11-15;end:2024-02-28;renewal:2024-03-01};budget{allocated:50000;spent:42350.75;remaining:7649.25}
9;;2024-01-19T16:30:45Z;pricing{cost:149.99;markup:0.28;price:191.99;discount:0.1};inventory{count:56;reserved:12;available:44}
10;{128750;9823;0.0763;0.18};;stats{avg_time:312.4;pages_per_session:8.2;return_rate:0.58};budget{allocated:125000;spent:98420.33;remaining:26579.67};dates{start:2023-01-01;end:2024-12-31}
```

---

## large_non_uniform_nested_text.json

Original size (JSON pretty): **4214 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 4214 | 1498 | 1268 | 997 | 985 | 1187.0 | 3.6 |
| JSON (min) | 3359 | 658 | 792 | 634 | 646 | 682.5 | 6.2 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 3387 | 818 | 843 | 716 | 702 | 769.8 | 5.5 |
| TOON | 3534 | 974 | 846 | 718 | 704 | 810.5 | 5.2 |
| TSON | 3173 | 721 | 831 | 644 | 688 | 721.0 | 5.8 |
| minemizer | 2809 | 522 | 619 | 510 | 499 | 537.5 | 7.8 |
| minemizer (compact) | 2694 | 565 | 672 | 534 | 526 | 574.2 | 7.3 |

### Serialized outputs

**JSON (pretty)** (4214 chars, 1187 tokens):
```json
[
  {
    "id": 1,
    "title": "Introduction to Machine Learning",
    "author": {
      "name": "Dr. Sarah Chen",
      "affiliation": "Stanford University",
      "department": "Computer Science"
    },
    "abstract": "A comprehensive overview of modern machine learning techniques and applications",
    "tags": [
      "AI",
      "ML",
      "deep learning"
    ]
  },
  {
    "id": 2,
    "title": "Climate Change Impact Assessment",
    "content": {
      "summary": "Analysis of rising sea levels and temperature patterns",
      "methodology": "longitudinal study with satellite imagery",
      "conclusion": "significant acceleration observed since 2010"
    },
    "category": "Environmental Science"
... (truncated)
```

**JSON (min)** (3359 chars, 682 tokens):
```json
[{"id":1,"title":"Introduction to Machine Learning","author":{"name":"Dr. Sarah Chen","affiliation":"Stanford University","department":"Computer Science"},"abstract":"A comprehensive overview of modern machine learning techniques and applications","tags":["AI","ML","deep learning"]},{"id":2,"title":"Climate Change Impact Assessment","content":{"summary":"Analysis of rising sea levels and temperature patterns","methodology":"longitudinal study with satellite imagery","conclusion":"significant acceleration observed since 2010"},"category":"Environmental Science"},{"id":3,"author":{"name":"Marcus Williams","affiliation":"MIT Media Lab","role":"Principal Researcher"},"publication":{"journal":"Nature Communications","volume":"fifteen","status":"peer-reviewed"},"keywords":"quantum computing, error correction, fault tolerance"},{"id":4,"title":"Urban Planning Strategies for Sustainable Cities","abstract":"Examining green infrastructure and mixed-use development patterns","content":{"summary":"Case studies from Copenhagen, Singapore, and Portland","methodology":"comparative analysis with community surveys","findings":"walkability correlates strongly with resident satisfaction"},"tags":["urban design","sustainability","planning"]},{"id":5,"publication":{"journal":"The Lancet","volume":"four hundred two","issue":"special edition","status":"published"},"content":{"summary":"Global health outcomes following pandemic response measures","conclusion":"early intervention strategies proved most effective"},"category":"Public Health"},{"id":6,"title":"Advances in Natural Language Processing","author":{"name":"Dr. James Rodriguez","affiliation":"Google Research","department":"Language Understanding"},"abstract":"Survey of transformer architectures and attention mechanisms in modern NLP systems","keywords":"transformers, attention, language models, BERT, GPT"},{"id":7,"content":{"summary":"Historical analysis of economic policy shifts in emerging markets","methodology":"archival research combined with econometric modeling","findings":"trade liberalization showed mixed results across regions","limitations":"data availability constraints for pre-1990 period"},"category":"Economics","tags":["policy","trade","development"]},{"id":8,"title":"Biodiversity Conservation in Tropical Rainforests","author":{"name":"Dr. Ana Costa","affiliation":"Brazilian Institute for Amazonian Research","role":"Lead Ecologist"},"publication":{"journal":"Conservation Biology","status":"under review"},"abstract":"Mapping species distribution patterns and identifying critical habitat corridors"},{"id":9,"title":"Behavioral Economics and Consumer Decision Making","content":{"summary":"Experimental studies on cognitive biases in purchasing behavior","methodology":"randomized controlled trials with eye-tracking technology","conclusion":"anchoring effects persist even with expert consumers"},"keywords":"behavioral economics, decision theory, consumer psychology","category":"Psychology"},{"id":10,"author":{"name":"Prof. Michael Thompson","affiliation":"Oxford University","department":"Engineering Science","role":"Department Chair"},"publication":{"journal":"Advanced Materials","volume":"thirty-six","status":"accepted"},"abstract":"Novel synthesis methods for high-performance ceramic composites","tags":["materials science","ceramics","nanotechnology"]}]
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (3387 chars, 770 tokens):
```yaml
- abstract: A comprehensive overview of modern machine learning techniques and applications
  author:
    affiliation: Stanford University
    department: Computer Science
    name: Dr. Sarah Chen
  id: 1
  tags:
  - AI
  - ML
  - deep learning
  title: Introduction to Machine Learning
- category: Environmental Science
  content:
    conclusion: significant acceleration observed since 2010
    methodology: longitudinal study with satellite imagery
    summary: Analysis of rising sea levels and temperature patterns
  id: 2
  title: Climate Change Impact Assessment
- author:
    affiliation: MIT Media Lab
    name: Marcus Williams
    role: Principal Researcher
  id: 3
  keywords: quantum computing, error correction, fault tolerance
  publication:
... (truncated)
```

**TOON** (3534 chars, 810 tokens):
```toon
[10]:
  - id: 1
    title: Introduction to Machine Learning
    author:
      name: Dr. Sarah Chen
      affiliation: Stanford University
      department: Computer Science
    abstract: A comprehensive overview of modern machine learning techniques and applications
    tags[3]: AI,ML,deep learning
  - id: 2
    title: Climate Change Impact Assessment
    content:
      summary: Analysis of rising sea levels and temperature patterns
      methodology: longitudinal study with satellite imagery
      conclusion: significant acceleration observed since 2010
    category: Environmental Science
  - id: 3
    author:
      name: Marcus Williams
      affiliation: MIT Media Lab
      role: Principal Researcher
    publication:
      journal: Nature Communications
      volume: fifteen
      status: peer-reviewed
... (truncated)
```

**TSON** (3173 chars, 721 tokens):
```tson
[{@id,title,author,abstract,tags|1,"Introduction to Machine Learning",{@name,affiliation,department|"Dr. Sarah Chen","Stanford University","Computer Science"},"A comprehensive overview of modern machine learning techniques and applications",[AI,ML,"deep learning"]},{@id,title,content,category|2,"Climate Change Impact Assessment",{@summary,methodology,conclusion|"Analysis of rising sea levels and temperature patterns","longitudinal study with satellite imagery","significant acceleration observed since 2010"},"Environmental Science"},{@id,author,publication,keywords|3,{@name,affiliation,role|"Marcus Williams","MIT Media Lab","Principal Researcher"},{@journal,volume,status|"Nature Communications",fifteen,peer-reviewed},"quantum computing, error correction, fault tolerance"},{@id,title,abstract,content,tags|4,"Urban Planning Strategies for Sustainable Cities","Examining green infrastructure and mixed-use development patterns",{@summary,methodology,findings|"Case studies from Copenhagen, Singapore, and Portland","comparative analysis with community surveys","walkability correlates strongly with resident satisfaction"},["urban design",sustainability,planning]},{@id,publication,content,category|5,{@journal,volume,issue,status|"The Lancet","four hundred two","special edition",published},{@summary,conclusion|"Global health outcomes following pandemic response measures","early intervention strategies proved most effective"},"Public Health"},{@id,title,author,abstract,keywords|6,"Advances in Natural Language Processing",{@name,affiliation,department|"Dr. James Rodriguez","Google Research","Language Understanding"},"Survey of transformer architectures and attention mechanisms in modern NLP systems","transformers, attention, language models, BERT, GPT"},{@id,content,category,tags|7,{@summary,methodology,findings,limitations|"Historical analysis of economic policy shifts in emerging markets","archival research combined with econometric modeling","trade liberalization showed mixed results across regions","data availability constraints for pre-1990 period"},Economics,[policy,trade,development]},{@id,title,author,publication,abstract|8,"Biodiversity Conservation in Tropical Rainforests",{@name,affiliation,role|"Dr. Ana Costa","Brazilian Institute for Amazonian Research","Lead Ecologist"},{@journal,status|"Conservation Biology","under review"},"Mapping species distribution patterns and identifying critical habitat corridors"},{@id,title,content,keywords,category|9,"Behavioral Economics and Consumer Decision Making",{@summary,methodology,conclusion|"Experimental studies on cognitive biases in purchasing behavior","randomized controlled trials with eye-tracking technology","anchoring effects persist even with expert consumers"},"behavioral economics, decision theory, consumer psychology",Psychology},{@id,author,publication,abstract,tags|10,{@name,affiliation,department,role|"Prof. Michael Thompson","Oxford University","Engineering Science","Department Chair"},{@journal,volume,status|"Advanced Materials",thirty-six,accepted},"Novel synthesis methods for high-performance ceramic composites",["materials science",ceramics,nanotechnology]}]
```

**minemizer** (2809 chars, 538 tokens):
```txt
id; title; author{ name; affiliation; department; role}; abstract; content{ summary; methodology; conclusion; ...}
1; Introduction to Machine Learning;{ Dr. Sarah Chen; Stanford University; Computer Science;}; A comprehensive overview of modern machine learning techniques and applications;; tags[ AI; ML; deep learning]
2; Climate Change Impact Assessment;;;{ Analysis of rising sea levels and temperature patterns; longitudinal study with satellite imagery; significant acceleration observed since 2010}; category: Environmental Science
3;;{ Marcus Williams; MIT Media Lab;; Principal Researcher};;; publication{ journal: Nature Communications; volume: fifteen; status: peer-reviewed}; keywords: quantum computing, error correction, fault tolerance
4; Urban Planning Strategies for Sustainable Cities;; Examining green infrastructure and mixed-use development patterns;{ Case studies from Copenhagen, Singapore, and Portland; comparative analysis with community surveys;; findings: walkability correlates strongly with resident satisfaction}; tags[ urban design; sustainability; planning]
5;;;;{ Global health outcomes following pandemic response measures;; early intervention strategies proved most effective}; publication{ journal: The Lancet; volume: four hundred two; issue: special edition; status: published}; category: Public Health
6; Advances in Natural Language Processing;{ Dr. James Rodriguez; Google Research; Language Understanding;}; Survey of transformer architectures and attention mechanisms in modern NLP systems;; keywords: transformers, attention, language models, BERT, GPT
7;;;;{ Historical analysis of economic policy shifts in emerging markets; archival research combined with econometric modeling;; findings: trade liberalization showed mixed results across regions; limitations: data availability constraints for pre-1990 period}; category: Economics; tags[ policy; trade; development]
8; Biodiversity Conservation in Tropical Rainforests;{ Dr. Ana Costa; Brazilian Institute for Amazonian Research;; Lead Ecologist}; Mapping species distribution patterns and identifying critical habitat corridors;; publication{ journal: Conservation Biology; status: under review}
9; Behavioral Economics and Consumer Decision Making;;;{ Experimental studies on cognitive biases in purchasing behavior; randomized controlled trials with eye-tracking technology; anchoring effects persist even with expert consumers}; keywords: behavioral economics, decision theory, consumer psychology; category: Psychology
10;;{ Prof. Michael Thompson; Oxford University; Engineering Science; Department Chair}; Novel synthesis methods for high-performance ceramic composites;; publication{ journal: Advanced Materials; volume: thirty-six; status: accepted}; tags[ materials science; ceramics; nanotechnology]
```

**minemizer (compact)** (2694 chars, 574 tokens):
```txt
id;title;author{name;affiliation;department;role};abstract;content{summary;methodology;conclusion;...}
1;Introduction to Machine Learning;{Dr. Sarah Chen;Stanford University;Computer Science;};A comprehensive overview of modern machine learning techniques and applications;;tags[AI;ML;deep learning]
2;Climate Change Impact Assessment;;;{Analysis of rising sea levels and temperature patterns;longitudinal study with satellite imagery;significant acceleration observed since 2010};category:Environmental Science
3;;{Marcus Williams;MIT Media Lab;;Principal Researcher};;;publication{journal:Nature Communications;volume:fifteen;status:peer-reviewed};keywords:quantum computing, error correction, fault tolerance
4;Urban Planning Strategies for Sustainable Cities;;Examining green infrastructure and mixed-use development patterns;{Case studies from Copenhagen, Singapore, and Portland;comparative analysis with community surveys;;findings:walkability correlates strongly with resident satisfaction};tags[urban design;sustainability;planning]
5;;;;{Global health outcomes following pandemic response measures;;early intervention strategies proved most effective};publication{journal:The Lancet;volume:four hundred two;issue:special edition;status:published};category:Public Health
6;Advances in Natural Language Processing;{Dr. James Rodriguez;Google Research;Language Understanding;};Survey of transformer architectures and attention mechanisms in modern NLP systems;;keywords:transformers, attention, language models, BERT, GPT
7;;;;{Historical analysis of economic policy shifts in emerging markets;archival research combined with econometric modeling;;findings:trade liberalization showed mixed results across regions;limitations:data availability constraints for pre-1990 period};category:Economics;tags[policy;trade;development]
8;Biodiversity Conservation in Tropical Rainforests;{Dr. Ana Costa;Brazilian Institute for Amazonian Research;;Lead Ecologist};Mapping species distribution patterns and identifying critical habitat corridors;;publication{journal:Conservation Biology;status:under review}
9;Behavioral Economics and Consumer Decision Making;;;{Experimental studies on cognitive biases in purchasing behavior;randomized controlled trials with eye-tracking technology;anchoring effects persist even with expert consumers};keywords:behavioral economics, decision theory, consumer psychology;category:Psychology
10;;{Prof. Michael Thompson;Oxford University;Engineering Science;Department Chair};Novel synthesis methods for high-performance ceramic composites;;publication{journal:Advanced Materials;volume:thirty-six;status:accepted};tags[materials science;ceramics;nanotechnology]
```

---

## mcp_tools_list.json

Original size (JSON pretty): **51663 chars**

| Format | Chars | gpt2 | llama | qwen2.5 | Deepseek-V3.2 | Avg Tokens | Orig/Token |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 51663 | 27574 | 13539 | 11210 | 11302 | 15906.2 | 3.2 |
| JSON (min) | 30724 | 6840 | 7315 | 6368 | 6976 | 6874.8 | 7.5 |
| CSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| TSV | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| YAML | 38139 | 16770 | 8915 | 7927 | 7996 | 10402.0 | 5.0 |
| TOON | 38376 | 17296 | 8649 | 7670 | 7766 | 10345.2 | 5.0 |
| TSON | 25878 | 7318 | 7045 | 5889 | 6730 | 6745.5 | 7.7 |
| minemizer | 23383 | 5559 | 5767 | 5319 | 5341 | 5496.5 | 9.4 |
| minemizer (compact) | 21912 | 5672 | 5726 | 5112 | 5215 | 5431.2 | 9.5 |

### Serialized outputs

**JSON (pretty)** (51663 chars, 15906 tokens):
```json
[
  {
    "inputSchema": {
      "json": {
        "properties": {
          "body": {
            "description": "Comment content",
            "type": "string"
          },
          "issue_number": {
            "description": "Issue number to comment on",
            "type": "number"
          },
          "owner": {
            "description": "Repository owner",
            "type": "string"
          },
          "repo": {
            "description": "Repository name",
            "type": "string"
          }
        },
        "required": [
          "owner",
          "repo",
... (truncated)
```

**JSON (min)** (30724 chars, 6875 tokens):
```json
[{"inputSchema":{"json":{"properties":{"body":{"description":"Comment content","type":"string"},"issue_number":{"description":"Issue number to comment on","type":"number"},"owner":{"description":"Repository owner","type":"string"},"repo":{"description":"Repository name","type":"string"}},"required":["owner","repo","issue_number","body"],"type":"object"}},"name":"add_issue_comment","description":"Add a comment to a specific issue in a GitHub repository."},{"inputSchema":{"json":{"properties":{"body":{"description":"The text of the review comment","type":"string"},"line":{"description":"The line of the blob in the pull request diff that the comment applies to. For multi-line comments, the last line of the range","type":"number"},"owner":{"description":"Repository owner","type":"string"},"path":{"description":"The relative path to the file that necessitates a comment","type":"string"},"pullNumber":{"description":"Pull request number","type":"number"},"repo":{"description":"Repository name","type":"string"},"side":{"description":"The side of the diff to comment on. LEFT indicates the previous state, RIGHT indicates the new state","enum":["LEFT","RIGHT"],"type":"string"},"startLine":{"description":"For multi-line comments, the first line of the range that the comment applies to","type":"number"},"startSide":{"description":"For multi-line comments, the starting side of the diff that the comment applies to. LEFT indicates the previous state, RIGHT indicates the new state","enum":["LEFT","RIGHT"],"type":"string"},"subjectType":{"description":"The level at which the comment is targeted","enum":["FILE","LINE"],"type":"string"}},"required":["owner","repo","pullNumber","path","body","subjectType"],"type":"object"}},"name":"add_pull_request_review_comment_to_pending_review","description":"Add a comment to the requester's latest pending pull request review, a pending review needs to already exist to call this (check with the user if not sure)."},{"inputSchema":{"json":{"properties":{"issueNumber":{"description":"Issue number","type":"number"},"owner":{"description":"Repository owner","type":"string"},"repo":{"description":"Repository name","type":"string"}},"required":["owner","repo","issueNumber"],"type":"object"}},"name":"assign_copilot_to_issue","description":"Assign Copilot to a specific issue in a GitHub repository.\n\nThis tool can help with the following outcomes:\n- a Pull Request created with source code changes to resolve the issue\n\n\nMore information can be found at:\n- https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks/about-assigning-tasks-to-copilot\n"},{"inputSchema":{"json":{"properties":{"body":{"description":"Review comment text","type":"string"},"commitID":{"description":"SHA of commit to review","type":"string"},"event":{"description":"Review action to perform","enum":["APPROVE","REQUEST_CHANGES","COMMENT"],"type":"string"},"owner":{"description":"Repository owner","type":"string"},"pullNumber":{"description":"Pull request number","type":"number"},"repo":{"description":"Repository name","type":"string"}},"required":["owner","repo","pullNumber","body","event"],"type":"object"}},"name":"create_and_submit_pull_request_review","description":"Create and submit a review for a pull request without review comments."},{"inputSchema":{"json":{"properties":{"branch":{"description":"Name for new branch","type":"string"},"from_branch":{"description":"Source branch (defaults to repo default)","type":"string"},"owner":{"description":"Repository owner","type":"string"},"repo":{"description":"Repository name","type":"string"}},"required":["owner","repo","branch"],"type":"object"}},"name":"create_branch","description":"Create a new branch in a GitHub repository"},{"inputSchema":{"json":{"properties":{"assignees":{"description":"Usernames to assign to this issue","items":{"type":"string"},"type":"array"},"body":{"description":"Issue body content","type":"string"},"labels":{"description":"Labels to apply to this issue","items":{"type":"string"},"type":"array"},"milestone":{"description":"Milestone number","type":"number"},"owner":{"description":"Repository owner","type":"string"},"repo":{"description":"Repository name","type":"string"},"title":{"description":"Issue title","type":"string"}},"required":["owner","repo","title"],"type":"object"}},"name":"create_issue","description":"Create a new issue in a GitHub repository."},{"inputSchema":{"json":{"properties":{"branch":{"description":"Branch to create/update the file in","type":"string"},"content":{"description":"Content of the file","type":"string"},"message":{"description":"Commit message","type":"string"},"owner":{"description":"Repository owner (username or organization)","type":"string"},"path":{"description":"Path where to create/update the file","type":"string"},"repo":{"description":"Repository name","type":"string"},"sha":{"description":"SHA of file being replaced (for updates)","type":"string"}},"required":["ow
... (truncated)
```

**CSV:** N/A
```
N/A - format cannot represent this data
```

**TSV:** N/A
```
N/A - format cannot represent this data
```

**YAML** (38139 chars, 10402 tokens):
```yaml
- description: Add a comment to a specific issue in a GitHub repository.
  inputSchema:
    json:
      properties:
        body:
          description: Comment content
          type: string
        issue_number:
          description: Issue number to comment on
          type: number
        owner:
          description: Repository owner
          type: string
        repo:
          description: Repository name
          type: string
      required:
      - owner
      - repo
      - issue_number
      - body
      type: object
  name: add_issue_comment
- description: Add a comment to the requester's latest pending pull request review,
    a pending review needs to already exist to call this (check with the user if not
... (truncated)
```

**TOON** (38376 chars, 10345 tokens):
```toon
[51]:
  -
    inputSchema:
      json:
        properties:
          body:
            description: Comment content
            type: string
          issue_number:
            description: Issue number to comment on
            type: number
          owner:
            description: Repository owner
            type: string
          repo:
            description: Repository name
            type: string
        required[4]: owner,repo,issue_number,body
        type: object
    name: add_issue_comment
    description: Add a comment to a specific issue in a GitHub repository.
  -
    inputSchema:
      json:
        properties:
... (truncated)
```

**TSON** (25878 chars, 6746 tokens):
```tson
{@inputSchema(@json),name,description#51|{{@properties,required,type|{@body,issue_number,owner,repo|{@description,type|"Comment content",string},{@description,type|"Issue number to comment on",number},{@description,type|"Repository owner",string},{@description,type|"Repository name",string}},[owner,repo,issue_number,body],object}},add_issue_comment,"Add a comment to a specific issue in a GitHub repository."|{{@properties,required,type|{@body,line,owner,path,pullNumber,repo,side,startLine,startSide,subjectType|{@description,type|"The text of the review comment",string},{@description,type|"The line of the blob in the pull request diff that the comment applies to. For multi-line comments, the last line of the range",number},{@description,type|"Repository owner",string},{@description,type|"The relative path to the file that necessitates a comment",string},{@description,type|"Pull request number",number},{@description,type|"Repository name",string},{@description,enum,type|"The side of the diff to comment on. LEFT indicates the previous state, RIGHT indicates the new state",[LEFT,RIGHT],string},{@description,type|"For multi-line comments, the first line of the range that the comment applies to",number},{@description,enum,type|"For multi-line comments, the starting side of the diff that the comment applies to. LEFT indicates the previous state, RIGHT indicates the new state",[LEFT,RIGHT],string},{@description,enum,type|"The level at which the comment is targeted",[FILE,LINE],string}},[owner,repo,pullNumber,path,body,subjectType],object}},add_pull_request_review_comment_to_pending_review,"Add a comment to the requester's latest pending pull request review, a pending review needs to already exist to call this (check with the user if not sure)."|{{@properties,required,type|{@issueNumber,owner,repo|{@description,type|"Issue number",number},{@description,type|"Repository owner",string},{@description,type|"Repository name",string}},[owner,repo,issueNumber],object}},assign_copilot_to_issue,"Assign Copilot to a specific issue in a GitHub repository.\n\nThis tool can help with the following outcomes:\n- a Pull Request created with source code changes to resolve the issue\n\n\nMore information can be found at:\n- https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks/about-assigning-tasks-to-copilot\n"|{{@properties,required,type|{@body,commitID,event,owner,pullNumber,repo|{@description,type|"Review comment text",string},{@description,type|"SHA of commit to review",string},{@description,enum,type|"Review action to perform",[APPROVE,REQUEST_CHANGES,COMMENT],string},{@description,type|"Repository owner",string},{@description,type|"Pull request number",number},{@description,type|"Repository name",string}},[owner,repo,pullNumber,body,event],object}},create_and_submit_pull_request_review,"Create and submit a review for a pull request without review comments."|{{@properties,required,type|{@branch,from_branch,owner,repo|{@description,type|"Name for new branch",string},{@description,type|"Source branch (defaults to repo default)",string},{@description,type|"Repository owner",string},{@description,type|"Repository name",string}},[owner,repo,branch],object}},create_branch,"Create a new branch in a GitHub repository"|{{@properties,required,type|{@assignees,body,labels,milestone,owner,repo,title|{@description,items,type|"Usernames to assign to this issue",{@type|string},array},{@description,type|"Issue body content",string},{@description,items,type|"Labels to apply to this issue",{@type|string},array},{@description,type|"Milestone number",number},{@description,type|"Repository owner",string},{@description,type|"Repository name",string},{@description,type|"Issue title",string}},[owner,repo,title],object}},create_issue,"Create a new issue in a GitHub repository."|{{@properties,required,type|{@branch,content,message,owner,path,repo,sha|{@description,type|"Branch to create/update the file in",string},{@description,type|"Content of the file",string},{@description,type|"Commit message",string},{@description,type|"Repository owner (username or organization)",string},{@description,type|"Path where to create/update the file",string},{@description,type|"Repository name",string},{@description,type|"SHA of file being replaced (for updates)",string}},[owner,repo,path,content,message,branch],object}},create_or_update_file,"Create or update a single file in a GitHub repository. If updating, you must provide the SHA of the file you want to update."|{{@properties,required,type|{@commitID,owner,pullNumber,repo|{@description,type|"SHA of commit to review",string},{@description,type|"Repository owner",string},{@description,type|"Pull request number",number},{@description,type|"Repository name",string}},[owner,repo,pullNumber],object}},create_pending_pull_request_review,"Create a pending review for a pull request. Call this first before attempting to add comments to a pending review, and ultimately submitting it
... (truncated)
```

**minemizer** (23383 chars, 5496 tokens):
```txt
inputSchema{ json{ properties{ owner{ description; type}; repo{ description; type}; ...}; required[]; type}}; name; description
{{ {{ Repository owner; string};{ Repository name; string}; body:{ description: Comment content; type: string}; issue_number:{ description: Issue number to comment on; type: number}};[ owner; repo; issue_number; body]; object}}; add_issue_comment; Add a comment to a specific issue in a GitHub repository.
{{ {{ Repository owner; string};{ Repository name; string}; body:{ description: The text of the review comment; type: string}; line:{ description: The line of the blob in the pull request diff that the comment applies to. For multi-line comments, the last line of the range; type: number}; path:{ description: The relative path to the file that necessitates a comment; type: string}; pullNumber:{ description: Pull request number; type: number}; side:{ description: The side of the diff to comment on. LEFT indicates the previous state, RIGHT indicates the new state; enum:[ LEFT; RIGHT]; type: string}; startLine:{ description: For multi-line comments, the first line of the range that the comment applies to; type: number}; startSide:{ description: For multi-line comments, the starting side of the diff that the comment applies to. LEFT indicates the previous state, RIGHT indicates the new state; enum:[ LEFT; RIGHT]; type: string}; subjectType:{ description: The level at which the comment is targeted; enum:[ FILE; LINE]; type: string}};[ owner; repo; pullNumber; path; body; subjectType]; object}}; add_pull_request_review_comment_to_pending_review; Add a comment to the requester's latest pending pull request review, a pending review needs to already exist to call this (check with the user if not sure).
{{ {{ Repository owner; string};{ Repository name; string}; issueNumber:{ description: Issue number; type: number}};[ owner; repo; issueNumber]; object}}; assign_copilot_to_issue; Assign Copilot to a specific issue in a GitHub repository.

This tool can help with the following outcomes:
- a Pull Request created with source code changes to resolve the issue


More information can be found at:
- https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks/about-assigning-tasks-to-copilot

{{ {{ Repository owner; string};{ Repository name; string}; body:{ description: Review comment text; type: string}; commitID:{ description: SHA of commit to review; type: string}; event:{ description: Review action to perform; enum:[ APPROVE; REQUEST_CHANGES; COMMENT]; type: string}; pullNumber:{ description: Pull request number; type: number}};[ owner; repo; pullNumber; body; event]; object}}; create_and_submit_pull_request_review; Create and submit a review for a pull request without review comments.
{{ {{ Repository owner; string};{ Repository name; string}; branch:{ description: Name for new branch; type: string}; from_branch:{ description: Source branch (defaults to repo default); type: string}};[ owner; repo; branch]; object}}; create_branch; Create a new branch in a GitHub repository
{{ {{ Repository owner; string};{ Repository name; string}; assignees:{ description: Usernames to assign to this issue; items:{ type: string}; type: array}; body:{ description: Issue body content; type: string}; labels:{ description: Labels to apply to this issue; items:{ type: string}; type: array}; milestone:{ description: Milestone number; type: number}; title:{ description: Issue title; type: string}};[ owner; repo; title]; object}}; create_issue; Create a new issue in a GitHub repository.
{{ {{ Repository owner (username or organization); string};{ Repository name; string}; branch:{ description: Branch to create/update the file in; type: string}; content:{ description: Content of the file; type: string}; message:{ description: Commit message; type: string}; path:{ description: Path where to create/update the file; type: string}; sha:{ description: SHA of file being replaced (for updates); type: string}};[ owner; repo; path; content; message; branch]; object}}; create_or_update_file; Create or update a single file in a GitHub repository. If updating, you must provide the SHA of the file you want to update.
{{ {{ Repository owner; string};{ Repository name; string}; commitID:{ description: SHA of commit to review; type: string}; pullNumber:{ description: Pull request number; type: number}};[ owner; repo; pullNumber]; object}}; create_pending_pull_request_review; Create a pending review for a pull request. Call this first before attempting to add comments to a pending review, and ultimately submitting it. A pending pull request review means a pull request review, it is pending because you create it first and submit it later, and the PR author will not see it until it is submitted.
{{ {{ Repository owner; string};{ Repository name; string}; base:{ description: Branch to merge into; type: string}; body:{ description: PR description; type: string}; draft:{ description: Create as draft PR; type: boolean}; head:{ description: Branch containing changes; type: string}; maintainer_can_modify:{ description: Allow maintainer edits; type: boolean}; title:{ description: PR title; type: string}};[ owner; repo; title; head; base]; object}}; create_pull_request; Create a new pull request in a GitHub repository.
{{ {;; autoInit:{ description: Initialize with README; type: boolean}; description:{ description: Repository description; type: string}; name:{ description: Repository name; type: string}; private:{ description: Whether repo should be private; type: boolean}};[ name]; object}}; create_repository; Create a new GitHub repository in your account
{{ {{ Repository owner (username or organization); string};{ Repository name; string}; branch:{ description: Branch to delete the file from; type: string}; message:{ description: Commit message; type: string}; path:{ description: Path to the file to delete; type: string}};[ owner; repo; path; message; branch]; object}}; delete_file; Delete a file from a GitHub repository
{{ {{ Repository owner; string};{ Repository name; string}; pullNumber:{ description: Pull request number; type: number}};[ owner; repo; pullNumber]; object}}; delete_pending_pull_request_review; Delete the requester's latest pending pull request review. Use this after the user decides not to submit a pending review, if you don't know if they already created one then check first.
{{ {;; state:{ description: The new state of the notification (read/done); enum:[ read; done]; type: string}; threadID:{ description: The ID of the notification thread; type: string}};[ threadID]; object}}; dismiss_notification; Dismiss a notification by marking it as read or done
{{ {{ Repository owner; string};{ Repository name; string}; organization:{ description: Organization to fork to; type: string}};[ owner; repo]; object}}; fork_repository; Fork a GitHub repository to your account or specified organization
{{ {{ The owner of the repository.; string};{ The name of the repository.; string}; alertNumber:{ description: The number of the alert.; type: number}};[ owner; repo; alertNumber]; object}}; get_code_scanning_alert; Get details of a specific code scanning alert in a GitHub repository.
{{ {{ Repository owner; string};{ Repository name; string}; page:{ description: Page number for pagination (min 1); minimum: 1; type: number}; perPage:{ description: Results per page for pagination (min 1, max 100); maximum: 100; minimum: 1; type: number}; sha:{ description: Commit SHA, branch name, or tag name; type: string}};[ owner; repo; sha]; object}}; get_commit; Get details for a commit from a GitHub repository
... (truncated)
```

**minemizer (compact)** (21912 chars, 5431 tokens):
```txt
inputSchema{json{properties{owner{description;type};repo{description;type};...};required[];type}};name;description
{{{{Repository owner;string};{Repository name;string};body:{description:Comment content;type:string};issue_number:{description:Issue number to comment on;type:number}};[owner;repo;issue_number;body];object}};add_issue_comment;Add a comment to a specific issue in a GitHub repository.
{{{{Repository owner;string};{Repository name;string};body:{description:The text of the review comment;type:string};line:{description:The line of the blob in the pull request diff that the comment applies to. For multi-line comments, the last line of the range;type:number};path:{description:The relative path to the file that necessitates a comment;type:string};pullNumber:{description:Pull request number;type:number};side:{description:The side of the diff to comment on. LEFT indicates the previous state, RIGHT indicates the new state;enum:[LEFT;RIGHT];type:string};startLine:{description:For multi-line comments, the first line of the range that the comment applies to;type:number};startSide:{description:For multi-line comments, the starting side of the diff that the comment applies to. LEFT indicates the previous state, RIGHT indicates the new state;enum:[LEFT;RIGHT];type:string};subjectType:{description:The level at which the comment is targeted;enum:[FILE;LINE];type:string}};[owner;repo;pullNumber;path;body;subjectType];object}};add_pull_request_review_comment_to_pending_review;Add a comment to the requester's latest pending pull request review, a pending review needs to already exist to call this (check with the user if not sure).
{{{{Repository owner;string};{Repository name;string};issueNumber:{description:Issue number;type:number}};[owner;repo;issueNumber];object}};assign_copilot_to_issue;Assign Copilot to a specific issue in a GitHub repository.

This tool can help with the following outcomes:
- a Pull Request created with source code changes to resolve the issue


More information can be found at:
- https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks/about-assigning-tasks-to-copilot

{{{{Repository owner;string};{Repository name;string};body:{description:Review comment text;type:string};commitID:{description:SHA of commit to review;type:string};event:{description:Review action to perform;enum:[APPROVE;REQUEST_CHANGES;COMMENT];type:string};pullNumber:{description:Pull request number;type:number}};[owner;repo;pullNumber;body;event];object}};create_and_submit_pull_request_review;Create and submit a review for a pull request without review comments.
{{{{Repository owner;string};{Repository name;string};branch:{description:Name for new branch;type:string};from_branch:{description:Source branch (defaults to repo default);type:string}};[owner;repo;branch];object}};create_branch;Create a new branch in a GitHub repository
{{{{Repository owner;string};{Repository name;string};assignees:{description:Usernames to assign to this issue;items:{type:string};type:array};body:{description:Issue body content;type:string};labels:{description:Labels to apply to this issue;items:{type:string};type:array};milestone:{description:Milestone number;type:number};title:{description:Issue title;type:string}};[owner;repo;title];object}};create_issue;Create a new issue in a GitHub repository.
{{{{Repository owner (username or organization);string};{Repository name;string};branch:{description:Branch to create/update the file in;type:string};content:{description:Content of the file;type:string};message:{description:Commit message;type:string};path:{description:Path where to create/update the file;type:string};sha:{description:SHA of file being replaced (for updates);type:string}};[owner;repo;path;content;message;branch];object}};create_or_update_file;Create or update a single file in a GitHub repository. If updating, you must provide the SHA of the file you want to update.
{{{{Repository owner;string};{Repository name;string};commitID:{description:SHA of commit to review;type:string};pullNumber:{description:Pull request number;type:number}};[owner;repo;pullNumber];object}};create_pending_pull_request_review;Create a pending review for a pull request. Call this first before attempting to add comments to a pending review, and ultimately submitting it. A pending pull request review means a pull request review, it is pending because you create it first and submit it later, and the PR author will not see it until it is submitted.
{{{{Repository owner;string};{Repository name;string};base:{description:Branch to merge into;type:string};body:{description:PR description;type:string};draft:{description:Create as draft PR;type:boolean};head:{description:Branch containing changes;type:string};maintainer_can_modify:{description:Allow maintainer edits;type:boolean};title:{description:PR title;type:string}};[owner;repo;title;head;base];object}};create_pull_request;Create a new pull request in a GitHub repository.
{{{;;autoInit:{description:Initialize with README;type:boolean};description:{description:Repository description;type:string};name:{description:Repository name;type:string};private:{description:Whether repo should be private;type:boolean}};[name];object}};create_repository;Create a new GitHub repository in your account
{{{{Repository owner (username or organization);string};{Repository name;string};branch:{description:Branch to delete the file from;type:string};message:{description:Commit message;type:string};path:{description:Path to the file to delete;type:string}};[owner;repo;path;message;branch];object}};delete_file;Delete a file from a GitHub repository
{{{{Repository owner;string};{Repository name;string};pullNumber:{description:Pull request number;type:number}};[owner;repo;pullNumber];object}};delete_pending_pull_request_review;Delete the requester's latest pending pull request review. Use this after the user decides not to submit a pending review, if you don't know if they already created one then check first.
{{{;;state:{description:The new state of the notification (read/done);enum:[read;done];type:string};threadID:{description:The ID of the notification thread;type:string}};[threadID];object}};dismiss_notification;Dismiss a notification by marking it as read or done
{{{{Repository owner;string};{Repository name;string};organization:{description:Organization to fork to;type:string}};[owner;repo];object}};fork_repository;Fork a GitHub repository to your account or specified organization
{{{{The owner of the repository.;string};{The name of the repository.;string};alertNumber:{description:The number of the alert.;type:number}};[owner;repo;alertNumber];object}};get_code_scanning_alert;Get details of a specific code scanning alert in a GitHub repository.
{{{{Repository owner;string};{Repository name;string};page:{description:Page number for pagination (min 1);minimum:1;type:number};perPage:{description:Results per page for pagination (min 1, max 100);maximum:100;minimum:1;type:number};sha:{description:Commit SHA, branch name, or tag name;type:string}};[owner;repo;sha];object}};get_commit;Get details for a commit from a GitHub repository
... (truncated)
```

---
