# Model Structure Documentation

## 📋 Panduan Struktur Model JSON untuk PPPL Compiler

Dokumen ini menjelaskan struktur lengkap file JSON model yang dapat digunakan dengan PPPL Compiler.

---

## 🎯 Struktur Dasar

Model JSON harus mengikuti struktur xtUML dengan format berikut:

```json
{
  "system_name": "Nama Sistem",
  "version": "1.0.0",
  "domains": [...]
}
```

### Root Level Properties

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `system_name` | string | ✅ Yes | Nama sistem yang akan di-generate |
| `version` | string | ⬜ No | Versi sistem (default: "1.0.0") |
| `domains` | array | ✅ Yes | Array berisi domain-domain dalam sistem |

---

## 🏢 Domain Structure

Domain adalah container untuk classes yang berkaitan secara logis.

```json
{
  "name": "Domain Name",
  "key_letter": "DN",
  "description": "Deskripsi domain",
  "classes": [...],
  "relationships": [...]
}
```

### Domain Properties

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `name` | string | ✅ Yes | Nama domain |
| `key_letter` | string | ✅ Yes | Singkatan 2-3 huruf (unique) |
| `description` | string | ⬜ No | Deskripsi domain |
| `classes` | array | ✅ Yes | Array berisi classes dalam domain |
| `relationships` | array | ⬜ No | Array berisi relationships antar classes |

---

## 📦 Class Structure

Class merepresentasikan entitas dalam sistem.

```json
{
  "entity_type": "class",
  "name": "ClassName",
  "key_letter": "CN",
  "description": "Deskripsi class",
  "attributes": [...],
  "state_machine": {...}
}
```

### Class Properties

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `entity_type` | string | ✅ Yes | Tipe entitas: `"class"` atau `"external_entity"` |
| `name` | string | ✅ Yes | Nama class (PascalCase) |
| `key_letter` | string | ✅ Yes | Singkatan 2-4 huruf (unique dalam domain) |
| `description` | string | ⬜ No | Deskripsi class |
| `attributes` | array | ✅ Yes | Array berisi attributes |
| `state_machine` | object | ⬜ No | State machine definition (untuk active classes) |

### Entity Types

- **`class`**: Class biasa dengan attributes dan methods
- **`external_entity`**: External entity (interface/service)

---

## 🏷️ Attribute Structure

Attributes adalah properties dari class.

```json
{
  "name": "AttributeName",
  "data_type": "string",
  "attribute_type": "descriptive",
  "default_value": "default"
}
```

### Attribute Properties

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `name` | string | ✅ Yes | Nama attribute (PascalCase atau camelCase) |
| `data_type` | string | ✅ Yes | Tipe data attribute |
| `attribute_type` | string | ✅ Yes | Tipe attribute: `naming`, `descriptive`, `referential` |
| `default_value` | any | ⬜ No | Nilai default |

### Supported Data Types

| Data Type | Python Type | Java Type | Deskripsi |
|-----------|-------------|-----------|-----------|
| `string` | `str` | `String` | Text/String |
| `integer` | `int` | `int` | Bilangan bulat |
| `float` | `float` | `double` | Bilangan desimal |
| `boolean` | `bool` | `boolean` | True/False |
| `datetime` | `datetime` | `Date` | Tanggal dan waktu |
| `uuid` | `UUID` | `UUID` | Unique identifier |
| `state` | `Enum` | `enum` | State machine state |
| `list` | `List` | `List` | Array/List |
| `dict` | `Dict` | `Map` | Dictionary/Map |

### Attribute Types

- **`naming`**: Identifier attribute (e.g., ID, Name)
- **`descriptive`**: Deskriptif attribute (e.g., Description, Status)
- **`referential`**: Foreign key reference ke class lain

---

## 🔄 State Machine Structure

State machine mendefinisikan behavior active class.

```json
{
  "initial_state": "InitialState",
  "states": [...],
  "transitions": [...]
}
```

### State Machine Properties

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `initial_state` | string | ✅ Yes | State awal saat object dibuat |
| `states` | array | ✅ Yes | Array berisi state definitions |
| `transitions` | array | ✅ Yes | Array berisi transitions |

### State Definition

```json
{
  "name": "StateName",
  "on_entry": [...],
  "on_exit": [...]
}
```

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `name` | string | ✅ Yes | Nama state |
| `on_entry` | array | ⬜ No | Actions saat masuk state |
| `on_exit` | array | ⬜ No | Actions saat keluar state |

### Transition Definition

```json
{
  "from_state": "StateA",
  "to_state": "StateB",
  "event": "eventName",
  "actionLanguage": {...}
}
```

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `from_state` | string | ✅ Yes | State asal |
| `to_state` | string | ✅ Yes | State tujuan |
| `event` | string | ✅ Yes | Event trigger |
| `actionLanguage` | object | ⬜ No | Action language operations |

---

## 💬 Action Language Structure

Action language mendefinisikan operations yang terjadi saat transition.

```json
{
  "operations": [
    {
      "name": "operationName",
      "parameters": [...],
      "steps": [...]
    }
  ]
}
```

### Operation Definition

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `name` | string | ✅ Yes | Nama operation |
| `parameters` | array | ⬜ No | Parameters untuk operation |
| `steps` | array | ✅ Yes | Array berisi action steps |

### Parameter Definition

```json
{
  "name": "paramName",
  "type": "string"
}
```

### Action Steps

#### 1. Create Action
Membuat instance baru dari class.

```json
{
  "type": "create",
  "class": "ClassName",
  "variable": "varName"
}
```

#### 2. Assign Action
Assignment nilai ke attribute.

```json
{
  "type": "assign",
  "target": "self",
  "attribute": "AttributeName",
  "value": "nilai"
}
```

atau dengan reference:

```json
{
  "type": "assign",
  "target": "self",
  "attribute": "AttributeName",
  "source": "variableName"
}
```

#### 3. Update Action
Update attribute (alias untuk assign).

```json
{
  "type": "update",
  "target": "this",
  "attribute": "Status",
  "value": "NewValue"
}
```

#### 4. Call Action
Memanggil method pada object.

```json
{
  "type": "call",
  "target": "objectName",
  "method": "methodName",
  "parameters": ["param1", "param2"]
}
```

#### 5. Generate Action
Generate event ke object lain.

```json
{
  "type": "generate",
  "target": "objectName",
  "event": "eventName"
}
```

#### 6. Log Action
Print log message.

```json
{
  "type": "log",
  "message": "Log message dengan ${variable}"
}
```

#### 7. Transition Action
Explicit state transition.

```json
{
  "type": "transition",
  "state": "NewState"
}
```

---

## 🔗 Relationship Structure

Relationships mendefinisikan hubungan antar classes.

```json
{
  "name": "R1",
  "type": "one_to_many",
  "from_class": "Class1",
  "to_class": "Class2",
  "from_domain": "Domain1",
  "to_domain": "Domain2",
  "description": "Class1 has many Class2"
}
```

### Relationship Properties

| Property | Type | Required | Deskripsi |
|----------|------|----------|-----------|
| `name` | string | ✅ Yes | Nama relationship (e.g., "R1", "R2") |
| `type` | string | ✅ Yes | Tipe relationship |
| `from_class` | string | ✅ Yes | Class sumber |
| `to_class` | string | ✅ Yes | Class tujuan |
| `from_domain` | string | ✅ Yes | Domain sumber |
| `to_domain` | string | ✅ Yes | Domain tujuan |
| `description` | string | ⬜ No | Deskripsi relationship |

### Relationship Types

| Type | Deskripsi | Contoh |
|------|-----------|--------|
| `one_to_one` | 1:1 | User has one Profile |
| `one_to_many` | 1:N | User has many Messages |
| `many_to_one` | N:1 | Many Orders belong to one Customer |
| `many_to_many` | N:M | Users have many Roles, Roles have many Users |

---

## 📝 Contoh Model Lengkap

### Contoh 1: Simple Model

```json
{
  "system_name": "Todo App",
  "version": "1.0.0",
  "domains": [
    {
      "name": "Task Management",
      "key_letter": "TM",
      "description": "Domain untuk manajemen task",
      "classes": [
        {
          "entity_type": "class",
          "name": "Task",
          "key_letter": "TSK",
          "description": "Representasi task dalam sistem",
          "attributes": [
            {
              "name": "TaskID",
              "data_type": "uuid",
              "attribute_type": "naming"
            },
            {
              "name": "Title",
              "data_type": "string",
              "attribute_type": "descriptive"
            },
            {
              "name": "Description",
              "data_type": "string",
              "attribute_type": "descriptive"
            },
            {
              "name": "Status",
              "data_type": "state",
              "attribute_type": "descriptive",
              "default_value": "Todo"
            }
          ],
          "state_machine": {
            "initial_state": "Todo",
            "states": [
              {"name": "Todo"},
              {"name": "InProgress"},
              {"name": "Done"}
            ],
            "transitions": [
              {
                "from_state": "Todo",
                "to_state": "InProgress",
                "event": "start",
                "actionLanguage": {
                  "operations": [
                    {
                      "name": "start",
                      "parameters": [],
                      "steps": [
                        {
                          "type": "log",
                          "message": "Task started"
                        }
                      ]
                    }
                  ]
                }
              },
              {
                "from_state": "InProgress",
                "to_state": "Done",
                "event": "complete",
                "actionLanguage": {
                  "operations": [
                    {
                      "name": "complete",
                      "parameters": [],
                      "steps": [
                        {
                          "type": "log",
                          "message": "Task completed"
                        }
                      ]
                    }
                  ]
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### Contoh 2: Model dengan Relationships

```json
{
  "system_name": "Blog System",
  "domains": [
    {
      "name": "Content Domain",
      "key_letter": "CD",
      "classes": [
        {
          "entity_type": "class",
          "name": "User",
          "key_letter": "USR",
          "attributes": [
            {"name": "UserID", "data_type": "uuid", "attribute_type": "naming"},
            {"name": "Username", "data_type": "string", "attribute_type": "descriptive"}
          ]
        },
        {
          "entity_type": "class",
          "name": "Post",
          "key_letter": "PST",
          "attributes": [
            {"name": "PostID", "data_type": "uuid", "attribute_type": "naming"},
            {"name": "Title", "data_type": "string", "attribute_type": "descriptive"},
            {"name": "AuthorID", "data_type": "uuid", "attribute_type": "referential"}
          ]
        }
      ],
      "relationships": [
        {
          "name": "R1",
          "type": "one_to_many",
          "from_class": "User",
          "to_class": "Post",
          "from_domain": "Content Domain",
          "to_domain": "Content Domain",
          "description": "User creates many Posts"
        }
      ]
    }
  ]
}
```

---

## ✅ Validation Rules

### Required Elements

1. **System Level**
   - ✅ Harus ada `system_name`
   - ✅ Harus ada minimal 1 domain

2. **Domain Level**
   - ✅ Harus ada `name`
   - ✅ Harus ada `key_letter` (unique)
   - ✅ Harus ada minimal 1 class

3. **Class Level**
   - ✅ Harus ada `name`
   - ✅ Harus ada `key_letter` (unique dalam domain)
   - ✅ Harus ada `entity_type`
   - ✅ Harus ada minimal 1 attribute

4. **Attribute Level**
   - ✅ Harus ada `name`
   - ✅ Harus ada `data_type`
   - ✅ Harus ada `attribute_type`

5. **State Machine Level** (jika ada)
   - ✅ Harus ada `initial_state`
   - ✅ Harus ada minimal 1 state
   - ✅ Initial state harus ada dalam daftar states
   - ✅ Attribute dengan `data_type: "state"` harus ada jika ada state machine

### Naming Conventions

- **System Name**: PascalCase atau Space-separated (e.g., "Personal Knowledge AI System")
- **Domain Name**: PascalCase atau Space-separated
- **Class Name**: PascalCase (e.g., "Message", "UserProfile")
- **Attribute Name**: PascalCase atau camelCase (e.g., "MessageID", "content")
- **State Name**: PascalCase atau Space-separated (e.g., "Draft", "In Progress")
- **Event Name**: camelCase (e.g., "userClicksSend", "apiCallSuccess")
- **Key Letter**: UPPERCASE 2-4 characters (e.g., "MSG", "UID")

---

## 🎯 Best Practices

### 1. Naming
- Gunakan nama yang deskriptif dan meaningful
- Konsisten dalam penamaan (PascalCase untuk classes, camelCase untuk methods)
- Gunakan key_letter yang mudah diingat dan relevan

### 2. Organization
- Kelompokkan classes yang related dalam satu domain
- Gunakan external_entity untuk services/interfaces
- Pisahkan concerns (UI, Business Logic, Data)

### 3. State Machines
- Gunakan untuk active classes yang memiliki lifecycle
- Definisikan all possible states dengan jelas
- Include action language untuk business logic

### 4. Relationships
- Definisikan relationships yang jelas dan meaningful
- Gunakan referential attributes untuk foreign keys
- Document cardinality dengan jelas

### 5. Action Language
- Keep operations simple and focused
- Use meaningful variable names
- Include log messages for debugging

### 6. Attributes
- Always include naming attribute (ID)
- Group related attributes
- Use appropriate data types
- Set meaningful defaults

---

## 🚨 Common Mistakes

❌ **Mistake 1**: Missing required fields
```json
{
  "name": "User"
  // Missing: entity_type, key_letter, attributes
}
```

✅ **Correct**:
```json
{
  "entity_type": "class",
  "name": "User",
  "key_letter": "USR",
  "attributes": [...]
}
```

---

❌ **Mistake 2**: Invalid data_type
```json
{
  "name": "Age",
  "data_type": "number"  // Should be "integer" or "float"
}
```

✅ **Correct**:
```json
{
  "name": "Age",
  "data_type": "integer",
  "attribute_type": "descriptive"
}
```

---

❌ **Mistake 3**: State machine without state attribute
```json
{
  "attributes": [
    {"name": "ID", "data_type": "uuid"}
    // Missing Status attribute with data_type: "state"
  ],
  "state_machine": {...}
}
```

✅ **Correct**:
```json
{
  "attributes": [
    {"name": "ID", "data_type": "uuid"},
    {"name": "Status", "data_type": "state", "default_value": "Initial"}
  ],
  "state_machine": {
    "initial_state": "Initial",
    ...
  }
}
```

---

## 📚 Resources

### Example Models
- `Model-personal-knowledge-ai.json` - Contoh lengkap dengan 30 classes, 5 state machines

### Documentation
- `README.md` - Dokumentasi compiler
- `docs/API_DOCUMENTATION.md` - Generated API documentation (setelah compile)

### Tools
- `compilerModel.py` - GUI compiler
- Model Analysis - Validasi dan scoring otomatis

---

## 🔍 Tips untuk Debugging

1. **Gunakan Model Analysis**
   - Enable "Model Analysis" saat compile
   - Review suggestions dan warnings

2. **Check Validation Messages**
   - Parser akan memberikan error spesifik
   - Fix errors secara bertahap

3. **Test Generated Code**
   - Gunakan "Test Run" untuk cek eksekusi
   - Review error messages

4. **Review Documentation**
   - Generate documentation untuk review struktur
   - Check class relationships dan methods

---

## 📞 Support

Jika ada pertanyaan tentang struktur model:
1. Review dokumentasi ini
2. Check contoh di `Model-personal-knowledge-ai.json`
3. Gunakan Model Analysis untuk validasi
4. Review generated documentation

---

**Selamat membuat model! 🎨**
