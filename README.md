# PPPL Compiler - xtUML Model-to-Code Generator

Compiler yang mengkonversi model xtUML (JSON) menjadi source code executable dengan support lengkap untuk state machines, action language, dan relationships.

## 🚀 Quick Start

```bash
# 1. Copy template
cp models/MODEL_TEMPLATE.json models/my-system/Model-my-system.json

# 2. Edit model sesuai kebutuhan (template sudah ada contoh lengkap)

# 3. Run compiler
python compilerModel.py
```

## ✨ Fitur Utama

- ✅ **Code Generation** - Python & Java
- ✅ **State Machine** - Lifecycle management dengan event-driven transitions
- ✅ **Action Language (OAL)** - Support 13+ action types (update, call, select, if/else, loops, dll)
- ✅ **Relationships** - one_to_one, one_to_many, many_to_one, many_to_many
- ✅ **Auto Documentation** - API docs + class diagrams
- ✅ **Model Analysis** - Validasi & quality scoring (0-100)
- ✅ **Auto Test** - Test run otomatis setelah compilation
- ✅ **GUI Interface** - User-friendly compiler interface

## 📋 Cara Penggunaan

### 1. Membuat Model Baru

**Gunakan template yang sudah disediakan:**

```bash
# Copy template
cp models/MODEL_TEMPLATE.json models/my-system/Model-my-system.json
```

Template sudah lengkap dengan:
- ✓ Contoh struktur domain, class, state machine, relationships
- ✓ Penjelasan lengkap untuk setiap field
- ✓ Semua action language types yang didukung
- ✓ Tips dan best practices

**Baca section `_PETUNJUK_PENGGUNAAN` di dalam template!**

### 2. Compile Model

1. Jalankan: `python compilerModel.py`
2. Klik **"Browse Model"** → pilih file `Model-*.json`
3. Klik **"Browse Output"** → pilih folder output
4. Pilih bahasa: **Python** atau Java
5. Klik **"Compile Model"**
6. Log otomatis tersimpan di `logs/`

### 3. Struktur Output

```
generated_code/
└── [system_name]/
    ├── main.py              # Main program dengan test
    ├── README.md            # Panduan penggunaan
    ├── library/
    │   ├── __init__.py
    │   ├── Class1.py        # Generated classes
    │   ├── Class2.py
    │   └── ...
    └── docs/
        └── API_DOCUMENTATION.md  # Dokumentasi API lengkap
```

## 🎯 Action Language Types

Compiler mendukung 13+ action types:

| Type | Deskripsi | Contoh JSON |
|------|-----------|-------------|
| **update** | Update attribute | `{"type": "update", "target": "self", "attribute": "Status", "value": "Active"}` |
| **call** | Panggil method/class | `{"type": "call", "target": "ClassName", "method": "methodName", "parameters": []}` |
| **log** | Logging message | `{"type": "log", "message": "Processing ${self.ID}"}` |
| **create** | Buat object baru | `{"type": "create", "entity": "ClassName", "variable": "obj"}` |
| **select** | Query objects | `{"type": "select", "entity": "ClassName", "variable": "result", "where": "condition"}` |
| **delete** | Hapus object | `{"type": "delete", "target": "self"}` |
| **relate** | Hubungkan objects | `{"type": "relate", "from": "self", "to": "object", "across": "R1"}` |
| **unrelate** | Putus hubungan | `{"type": "unrelate", "from": "self", "to": "object", "across": "R1"}` |
| **if** | Conditional logic | `{"type": "if", "condition": "expr", "then": [], "else": []}` |
| **while** | Loop dengan kondisi | `{"type": "while", "condition": "expr", "body": []}` |
| **for** | Iterasi | `{"type": "for", "variable": "item", "iterable": "list", "body": []}` |
| **return** | Return value | `{"type": "return", "value": "result"}` |
| **break/continue** | Loop control | `{"type": "break"}` / `{"type": "continue"}` |

## 🔗 Relationship Types

| Type | Deskripsi | Format |
|------|-----------|--------|
| **one_to_one** | 1:1 relationship | User ↔ Profile |
| **one_to_many** | 1:N relationship | Customer → Orders |
| **many_to_one** | N:1 relationship | Orders → Customer |
| **many_to_many** | N:M relationship | Students ↔ Courses |

**Format JSON:**
```json
{
  "name": "R1",
  "type": "one_to_many",
  "from_class": "Customer",
  "to_class": "Order",
  "from_domain": "Sales Domain",
  "to_domain": "Sales Domain",
  "description": "Customer dapat memiliki banyak Order"
}
```

## 📊 Model Analysis

Compiler otomatis menganalisis model dan memberikan:

- **Model Statistics** - Jumlah domains, classes, state machines, relationships
- **Active vs Passive Classes** - Class dengan/tanpa state machine
- **Issues Detection** - Missing state machines, unreachable states, dll
- **Quality Score** - 0-100 berdasarkan completeness
- **Suggestions** - Rekomendasi improvement

## 🏗️ Arsitektur Compiler

```
GUI (compilerModel.py)
    ↓
Compiler Engine
    ↓
Parser → Validate JSON → Extract Domains/Classes/Relationships
    ↓
Code Generator
    ├── Python Generator → State Machines → OAL Compiler
    └── Java Generator
    ↓
Documentation Generator → API Docs + Diagrams
    ↓
Model Analyzer → Quality Report + Test Results
```

### Modul Utama

| Modul | Fungsi |
|-------|--------|
| **compilerModel.py** | GUI utama dengan auto-test dan auto-save log |
| **parser.py** | Parse & validate JSON model, extract entities |
| **compiler_engine.py** | Orchestrator kompilasi |
| **python_generator.py** | Generate Python code + dataclasses |
| **java_generator.py** | Generate Java code + POJOs |
| **state_machine_compiler.py** | Compile state machines → event handlers |
| **action_language_compiler.py** | Translate OAL → Python/Java code |
| **oal_generator.py** | Auto-generate CRUD + utility methods |
| **documentation_generator.py** | Generate API docs + diagrams |
| **model_analyzer.py** | Model validation + quality scoring |

## 🛠️ Troubleshooting

**Error saat compile:**
- Cek format JSON di MODEL_TEMPLATE.json
- Pastikan semua required fields ada
- Periksa log di console/folder `logs/`

**Test run gagal:**
- Missing dependencies → Cek imports di generated code
- State machine error → Validasi initial_state dan transitions
- Relationship error → Pastikan from_class/to_class valid

**Relationship tidak terbaca:**
- Parser mendukung 2 format: `relationship_id` (lama) dan `name` (baru)
- Pastikan minimal salah satu ada

## 📝 Best Practices

1. **Mulai dari Template** - Jangan buat JSON dari nol
2. **Baca _PETUNJUK_PENGGUNAAN** - Ada di MODEL_TEMPLATE.json
3. **Test Incrementally** - Compile dan test setelah setiap perubahan besar
4. **Use State Machines** - Untuk class yang punya lifecycle
5. **Document Relationships** - Tulis deskripsi yang jelas
6. **Validate Early** - Gunakan model analyzer sebelum compile

## 📚 Referensi

- **Template**: `models/MODEL_TEMPLATE.json` - Contoh lengkap + dokumentasi inline
- **Petunjuk**: `petunjuk-penggunaan.txt` - Quick reference
- **Logs**: `logs/` - Compilation history & debugging
- **Examples**: `generated_code/` - Sample outputs (banking, e-commerce, blog, dll)

## 🔄 Backward Compatibility

Parser mendukung model format lama:
- `relationship_id` dan `name` untuk relationships
- `participants` dan `from_class/to_class` untuk relationship endpoints
- Otomatis detect dan convert

## 🎓 Credits

**Kelompok 4** - PPPL UIN Sunan Kalijaga 2025

---

**Latest Version**: v2.0 - Full xtUML support dengan template system  
**License**: Educational Use  
**Last Updated**: 2024

**Happy Compiling! 🚀**
