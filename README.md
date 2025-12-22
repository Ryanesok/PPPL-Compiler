# PPPL Compiler - Model-to-Code Generator

Compiler yang mengkonversi model xtUML (JSON) menjadi source code executable.

## Fitur

- ✅ Generate Python & Java code
- ✅ State machine compilation
- ✅ Auto-generated CRUD methods
- ✅ Documentation generator
- ✅ Model analysis & validation
- ✅ GUI interface

## Instalasi

Jalankan:
```bash
python compilerModel.py
```

## Cara Penggunaan

**Sebelum menggunakan:** Pastikan model dalam format JSON sesuai struktur di `models/MODEL_STRUCTURE.md`

### Langkah-langkah:

1. **Buka** `compilerModel.py`
2. **Import Model** - Klik "Import Model" dan pilih file `.json`
3. **Pilih Target Language** - Python (recommended) atau Java
4. **Compile** - Klik tombol "🚀 Compile Model"
5. **Test Run** - Klik "Test Run" untuk verifikasi
6. **Selesai** - Source code tersimpan di `generated_code/`

### Struktur Output

```
generated_code/
└── [system_name]/
    ├── main.py
    ├── README.md
    ├── library/
    │   ├── __init__.py
    │   └── *.py
    └── docs/
        └── API_DOCUMENTATION.md
```

## Troubleshooting

**Gagal saat compile:**
- Model tidak sesuai struktur → Cek `models/MODEL_STRUCTURE.md`
- Periksa log di console compiler

**Test run error:**
- Model kekurangan atribut/modul → Lengkapi model JSON
- Class tanpa state machine → Tambahkan state machine untuk active class

## Arsitektur

```
GUI → Compiler Engine → Parser → Code Generator
                              ↓
                     Python / Java / OAL Generator
                              ↓
                     Documentation Generator
```

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

## Modul Compiler

- **parser.py** - Parse & validasi JSON model
- **compiler_engine.py** - Orchestrator kompilasi
- **python_generator.py** - Generate Python code
- **java_generator.py** - Generate Java code
- **state_machine_compiler.py** - Compile state machines
- **action_language_compiler.py** - Translate action language
- **oal_generator.py** - Generate OAL methods
- **documentation_generator.py** - Generate docs

## Contoh Model

Lihat folder `models/` untuk contoh:
- `banking-system/` - Sistem perbankan
- `e-commerce/` - Toko online
- `blog-system/` - Platform blog
- `personal-ai-knowledge/` - AI knowledge management

Struktur lengkap di `models/MODEL_STRUCTURE.md`

## Credits

**Kelompok 4** - PPPL UIN Sunan Kalijaga 2025

## Dokumentasi Lengkap

- `README.md` - Petunjuk compiler
- `models/MODEL_STRUCTURE.md` - Format model JSON
- `BUGFIX_SUMMARY.md` - Log bug fixes
- `generated_code/*/docs/` - API documentation

---

**Happy Compiling! 🚀**
