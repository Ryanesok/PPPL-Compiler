# PPPL Compiler - Model-to-Code Generator

## 📖 Deskripsi

PPPL Compiler adalah sebuah compiler yang mengkonversi model xtUML dalam format JSON menjadi kode program yang dapat dijalankan. Compiler ini dikembangkan sebagai bagian dari tugas akhir mata kuliah Perancangan dan Pengembangan Perangkat Lunak (PPPL).

### Fitur Utama

✅ **Multi-Language Support**: Generate kode dalam Python dan Java  
✅ **State Machine Compilation**: Mendukung state machine dengan event handling  
✅ **Action Language Translation**: Konversi action language (OAL) ke kode executable  
✅ **Auto-Generated Methods**: Otomatis membuat CRUD operations dan utility methods  
✅ **Comprehensive Documentation**: Generate dokumentasi API lengkap  
✅ **Model Analysis**: Analisis kualitas model dengan scoring system  
✅ **Test Run Workflow**: Testing otomatis terhadap kode yang dihasilkan  
✅ **GUI Interface**: Antarmuka grafis yang user-friendly  

---

## 🚀 Instalasi

### Prerequisites

- Python 3.8 atau lebih tinggi
- tkinter (biasanya sudah terinstall dengan Python)

### Cara Menggunakan

1. Clone atau download repository ini
2. Pastikan Python sudah terinstall
3. Jalankan compiler dengan perintah:

```bash
python compilerModel.py
```

---

## 📚 Cara Penggunaan

### 1. Menggunakan GUI

#### Langkah-langkah:

1. **Buka Compiler**
   ```bash
   python compilerModel.py
   ```

2. **Load Model JSON**
   - Klik tombol **"Browse Model"**
   - Pilih file JSON model Anda
   - Model akan divalidasi secara otomatis

3. **Pilih Target Language**
   - Pilih **Python** atau **Java** dari dropdown
   - Python: Full support (state machines, action language, OAL)
   - Java: Basic support (classes dan methods)

4. **Opsi Tambahan**
   - ☑ **Generate Documentation**: Membuat dokumentasi API lengkap
   - ☑ **Enable Model Analysis**: Analisis kualitas model sebelum compile

5. **Compile Model**
   - Klik tombol **"Compile Model"**
   - Tunggu proses kompilasi selesai
   - Lihat output di console area

6. **Test Run (Opsional)**
   - Klik tombol **"Test Run"**
   - Menjalankan kode yang telah di-generate
   - Melihat hasil eksekusi dan analisis

7. **Save Log**
   - Klik **"Save Log"** untuk menyimpan hasil kompilasi
   - File log akan disimpan dengan timestamp

### 2. Struktur Output

Kode yang dihasilkan akan tersimpan dalam struktur folder berikut:

```
generated_code/
└── [model_name]/
    ├── main.py                    # Entry point aplikasi
    ├── README.md                  # Dokumentasi dasar
    ├── library/                   # Library classes
    │   ├── __init__.py
    │   ├── Class1.py
    │   ├── Class2.py
    │   └── ...
    └── docs/                      # Dokumentasi (jika enabled)
        └── API_DOCUMENTATION.md   # Dokumentasi API lengkap
```

---

## 🏗️ Arsitektur Compiler

### Komponen Utama

```
┌─────────────────────────────────────────────────────────┐
│                    GUI (compilerModel.py)                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Compiler Engine (compiler_engine.py)        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬───────────────┐
        ▼            ▼            ▼               ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐
   │ Parser  │  │ Code    │  │ State   │  │ Action   │
   │         │  │ Gen     │  │ Machine │  │ Language │
   └─────────┘  └─────────┘  └─────────┘  └──────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌──────────┐
   │ Python  │  │ Java    │  │ OAL      │
   │ Gen     │  │ Gen     │  │ Gen      │
   └─────────┘  └─────────┘  └──────────┘
        │            │            │
        └────────────┴────────────┘
                     │
                     ▼
   ┌──────────────────────────────────────┐
   │     Documentation Generator          │
   └──────────────────────────────────────┘
```

### Modul-Modul

#### 1. **parser.py**
- Membaca dan memvalidasi file JSON model
- Ekstraksi domains, classes, dan relationships
- Validasi struktur model

#### 2. **compiler_engine.py**
- Orchestrator utama kompilasi
- Koordinasi antara parser dan generator
- Error handling

#### 3. **code_generator.py**
- Base class untuk semua generator
- Manajemen struktur folder output
- Abstraksi untuk multi-language support

#### 4. **python_generator.py**
- Generate kode Python dari model
- Support untuk dataclasses
- Implementasi state machines
- Integration dengan OAL generator

#### 5. **java_generator.py**
- Generate kode Java dari model
- POJOs dengan getters/setters

#### 6. **state_machine_compiler.py**
- Kompilasi state machine definitions
- Generate event handlers
- State transition logic

#### 7. **action_language_compiler.py**
- Translate action language steps ke kode
- Support untuk: create, assign, call, generate, log, transition

#### 8. **oal_generator.py**
- Auto-generate CRUD operations
- Generate utility methods (__str__, to_dict, validate)
- Generate workflow demonstrations

#### 9. **documentation_generator.py**
- Generate comprehensive API documentation
- System overview dan architecture stats
- Class reference dan relationship diagrams

#### 10. **model_analyzer.py**
- Analisis kualitas model (scoring 0-100)
- Deteksi issues dan suggestions
- Test execution dan reporting

---

## 🎯 Fitur Detail

### 1. State Machine Compilation

Compiler mendukung state machine lengkap dengan:
- **Initial State**: State awal saat object dibuat
- **States**: Daftar semua state yang mungkin
- **Transitions**: Event-driven state transitions
- **On Entry/Exit Actions**: Actions saat masuk/keluar state
- **Event Handling**: Automatic event dispatcher

**Contoh Output:**
```python
class MessageState(Enum):
    DRAFT = "Draft"
    SENDING = "Sending"
    SENT = "Sent"

class Message:
    Status: MessageState = field(default_factory=lambda: MessageState.DRAFT)
    
    def userclickssend(self):
        """Handle userClicksSend event"""
        if self.Status == MessageState.DRAFT:
            self.Status = MessageState.SENDING
            return True
        return False
    
    def handle_event(self, event_name: str) -> bool:
        """Handle any event by dispatching to appropriate method"""
        event_method = event_name.lower().replace(' ', '_')
        if hasattr(self, event_method):
            method = getattr(self, event_method)
            return method()
        return False
```

### 2. Action Language Translation

Support untuk berbagai tipe action:

| Action Type | Deskripsi | Contoh |
|-------------|-----------|--------|
| **create** | Membuat instance baru | `new_obj = ClassName()` |
| **assign** | Assignment nilai | `self.attribute = value` |
| **call** | Memanggil method | `object.method(params)` |
| **generate** | Generate event | `object.handle_event('event')` |
| **log** | Print log message | `print("message")` |
| **transition** | State transition | `self.Status = NewState` |

### 3. Auto-Generated OAL Methods

Setiap class otomatis mendapat methods:

```python
def __str__(self):
    """String representation"""
    return f"ClassName(attr1={self.attr1}, attr2={self.attr2})"

def to_dict(self):
    """Convert to dictionary"""
    return {
        'attr1': self.attr1,
        'attr2': self.attr2
    }

def validate(self) -> bool:
    """Validate object data"""
    if self.required_attr is None:
        return False
    return True
```

### 4. Documentation Generation

Generate dokumentasi markdown lengkap dengan:
- System Overview
- Architecture Statistics
- Domain Descriptions
- Class Reference (attributes & methods)
- Relationships Diagram
- State Machine Documentation
- API Quick Reference
- Usage Examples

### 5. Model Analysis & Scoring

Sistem scoring 0-100 berdasarkan:
- **Completeness** (30%): Kelengkapan model
- **Complexity** (20%): Kompleksitas yang sesuai
- **Documentation** (20%): Kualitas deskripsi
- **State Machines** (15%): Implementasi state machines
- **Relationships** (15%): Kualitas relationships

**Rating Categories:**
- 90-100: Excellent
- 75-89: Good
- 60-74: Fair
- 0-59: Needs Improvement

---

## 🔧 Troubleshooting

### Error: "Model validation failed"
- Pastikan file JSON valid
- Cek struktur model sesuai dokumentasi MODEL_STRUCTURE.md
- Pastikan semua required fields ada

### Error: "No classes found in model"
- Pastikan model memiliki minimal 1 domain
- Pastikan domain memiliki minimal 1 class

### Error: "AttributeError: object has no attribute 'handle_event'"
- Recompile model dengan versi compiler terbaru
- Pastikan class memiliki state machine

### Generated code tidak jalan
- Cek error message di console
- Gunakan fitur "Test Run" untuk debugging
- Lihat Model Analysis untuk suggestions

---

## 📊 Contoh Penggunaan

### Example 1: Simple Class Model

```json
{
  "system_name": "Simple System",
  "domains": [{
    "name": "Main Domain",
    "classes": [{
      "entity_type": "class",
      "name": "User",
      "attributes": [
        {"name": "UserID", "data_type": "uuid", "attribute_type": "naming"},
        {"name": "Name", "data_type": "string", "attribute_type": "descriptive"}
      ]
    }]
  }]
}
```

**Output**: Generate User class dengan attributes dan auto-generated methods.

### Example 2: State Machine Model

Lihat file `Model-personal-knowledge-ai.json` untuk contoh lengkap model dengan:
- 6 Domains
- 30 Classes
- 5 State Machines
- Multiple Relationships
- Action Language operations

---

## 🎓 Credits

**Developed by**: Kelompok 4  
**Course**: Perancangan dan Pengembangan Perangkat Lunak (PPPL)  
**Institution**: UIN Sunan Kalijaga  
**Year**: 2025  

---

## 📄 License

This project is developed for academic purposes.

---

## 📞 Support

Untuk pertanyaan atau issues, silakan refer ke dokumentasi:
- **README.md** - Dokumentasi compiler
- **MODEL_STRUCTURE.md** - Dokumentasi struktur model
- **docs/API_DOCUMENTATION.md** - Dokumentasi API (generated)

---

## 🔄 Version History

### v1.0.0 (December 2025)
- ✅ Initial release
- ✅ Python & Java code generation
- ✅ State machine compilation
- ✅ Action language translation
- ✅ Auto-generated OAL methods
- ✅ Documentation generation
- ✅ Model analysis & testing
- ✅ GUI interface

---

**Happy Compiling! 🚀**
