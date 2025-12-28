import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import sys
import json

# Add compiler package to path
sys.path.insert(0, os.path.dirname(__file__))

from compiler.compiler_engine import CompilerEngine
from compiler.model_analyzer import ModelAnalyzer
from compiler.parser import ModelParser

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PPPL Model Compiler")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.target_lang = tk.StringVar(value="Python")
        self.selected_model = tk.StringVar()
        self.model_analyzer = ModelAnalyzer()
        self.last_compiled_model_dir = None
        self.models_dir = os.path.join(os.path.dirname(__file__), "models")
        
        # Compiler engine
        self.compiler_engine = CompilerEngine()
        
        self.create_widgets()
        self.scan_models_folder()
        
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PPPL Model Compiler", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Model Selection Section
        ttk.Label(main_frame, text="Select Model:", 
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        model_frame = ttk.Frame(main_frame)
        model_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.model_combo = ttk.Combobox(model_frame, textvariable=self.selected_model, 
                                        width=50, state="readonly")
        self.model_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.model_combo.bind('<<ComboboxSelected>>', self.on_model_selected)
        
        ttk.Button(model_frame, text="Import Model", 
                  command=self.import_model).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(model_frame, text="Refresh", 
                  command=self.scan_models_folder).pack(side=tk.LEFT, padx=(5, 0))
        
        # Display selected file path
        ttk.Label(main_frame, text="Model Path:", 
                 font=('Arial', 9)).grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        
        path_entry = ttk.Entry(main_frame, textvariable=self.input_file, width=60, state="readonly")
        path_entry.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Output Directory Section
        ttk.Label(main_frame, text="Output Directory:", 
                 font=('Arial', 10, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=5)
        
        output_entry = ttk.Entry(main_frame, textvariable=self.output_dir, width=60)
        output_entry.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        browse_output_btn = ttk.Button(main_frame, text="Browse", 
                                        command=self.browse_output_dir)
        browse_output_btn.grid(row=6, column=2, padx=(5, 0), pady=5)
        
        # Target Language Section
        ttk.Label(main_frame, text="Target Language:", 
                 font=('Arial', 10, 'bold')).grid(row=7, column=0, sticky=tk.W, pady=5)
        
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=8, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        languages = ["Python", "Java", "C#", "TypeScript", "Go"]
        for lang in languages:
            ttk.Radiobutton(lang_frame, text=lang, value=lang, 
                           variable=self.target_lang).pack(side=tk.LEFT, padx=10)
        
        # Set all compiler options to True by default (no UI needed)
        self.generate_tests = tk.BooleanVar(value=True)
        self.generate_docs = tk.BooleanVar(value=True)
        self.verbose_mode = tk.BooleanVar(value=True)
        self.include_state_machines = tk.BooleanVar(value=True)
        
        # Compile Button
        compile_btn = ttk.Button(main_frame, text="🚀 Compile Model", 
                                command=self.compile_model, 
                                style='Accent.TButton')
        compile_btn.grid(row=9, column=0, columnspan=3, pady=20)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=400)
        self.progress.grid(row=10, column=0, columnspan=3, pady=5)
        
        # Console Output Section
        ttk.Label(main_frame, text="Console Output:", 
                 font=('Arial', 10, 'bold')).grid(row=11, column=0, sticky=tk.W, pady=(10, 5))
        
        self.console = scrolledtext.ScrolledText(main_frame, height=15, width=100, 
                                                  bg='#1e1e1e', fg='#d4d4d4',
                                                  font=('Consolas', 9))
        self.console.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(12, weight=1)
        
        # Button Frame at bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=13, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Log", 
                  command=self.save_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="About", 
                  command=self.show_about).pack(side=tk.LEFT, padx=5)
        
        # Initial console message
        self.log_message("PPPL Model Compiler v1.0.0")
        self.log_message("Ready to compile your models...")
        self.log_message("-" * 80)
        
    def scan_models_folder(self):
        """Scan models folder for available models"""
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
            self.log_message(f"Created models directory: {self.models_dir}")
            return
        
        models = []
        try:
            # Scan for model folders
            for item in os.listdir(self.models_dir):
                item_path = os.path.join(self.models_dir, item)
                
                # Skip MODEL_STRUCTURE.md
                if os.path.isfile(item_path):
                    continue
                
                # Check if it's a directory
                if os.path.isdir(item_path):
                    # Look for JSON files in the folder
                    json_files = [f for f in os.listdir(item_path) if f.endswith('.json')]
                    if json_files:
                        models.append(item)
            
            if models:
                self.model_combo['values'] = models
                self.log_message(f"Found {len(models)} model(s) in models folder")
                if models:
                    self.model_combo.current(0)
                    self.on_model_selected(None)
            else:
                self.model_combo['values'] = []
                self.log_message("No models found in models folder")
                
        except Exception as e:
            self.log_message(f"Error scanning models folder: {str(e)}")
    
    def on_model_selected(self, event):
        """Handle model selection from dropdown"""
        model_name = self.selected_model.get()
        if not model_name:
            return
        
        model_folder = os.path.join(self.models_dir, model_name)
        
        # Find JSON file in the model folder
        try:
            json_files = [f for f in os.listdir(model_folder) if f.endswith('.json')]
            if json_files:
                # Use the first JSON file found
                model_file = os.path.join(model_folder, json_files[0])
                self.input_file.set(model_file)
                self.log_message(f"Selected model: {model_name} ({json_files[0]})")
                
                # Auto-set unique output directory per model
                model_output = self._get_model_output_dir(model_name)
                self.output_dir.set(model_output)
                self.log_message(f"Output directory: {model_output}")
            else:
                self.log_message(f"No JSON file found in model folder: {model_name}")
        except Exception as e:
            self.log_message(f"Error loading model: {str(e)}")
    
    def import_model(self):
        """Import a model JSON file into models folder"""
        filename = filedialog.askopenfilename(
            title="Import Model JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            # Read and validate the JSON file
            with open(filename, 'r', encoding='utf-8') as f:
                model_data = json.load(f)
            
            # Extract model name from JSON or filename
            model_name = model_data.get('model_name')
            if not model_name:
                # Try to get from filename
                base_name = os.path.basename(filename)
                if base_name.startswith('Model-') and base_name.endswith('.json'):
                    model_name = base_name[6:-5]  # Remove 'Model-' prefix and '.json' suffix
                else:
                    model_name = os.path.splitext(base_name)[0]
            
            # Sanitize model name for folder
            model_name = model_name.replace(' ', '-').lower()
            
            # Create model folder
            model_folder = os.path.join(self.models_dir, model_name)
            os.makedirs(model_folder, exist_ok=True)
            
            # Copy JSON file to model folder
            dest_filename = f"Model-{model_name}.json"
            dest_path = os.path.join(model_folder, dest_filename)
            
            # Copy the file
            import shutil
            shutil.copy2(filename, dest_path)
            
            # Show success notification
            self.log_message("=" * 80)
            self.log_message(f"✅ Model imported successfully!")
            self.log_message(f"   Model Name: {model_name}")
            self.log_message(f"   Location: {model_folder}")
            self.log_message(f"   File: {dest_filename}")
            self.log_message("=" * 80)
            
            messagebox.showinfo("Import Successful", 
                              f"Model '{model_name}' has been imported successfully!\n\n"
                              f"Location: models/{model_name}/")
            
            # Refresh models list
            self.scan_models_folder()
            
            # Auto-select the imported model
            self.selected_model.set(model_name)
            self.on_model_selected(None)
            
            # Set unique output directory
            model_output = self._get_model_output_dir(model_name)
            self.output_dir.set(model_output)
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON file: {str(e)}"
            self.log_message(f"❌ Import failed: {error_msg}")
            messagebox.showerror("Import Failed", error_msg)
        except Exception as e:
            error_msg = f"Failed to import model: {str(e)}"
            self.log_message(f"❌ Import failed: {error_msg}")
            messagebox.showerror("Import Failed", error_msg)
    
    def _get_model_output_dir(self, model_name):
        """Generate unique output directory for a model"""
        # Return base generated_code directory
        # Compiler engine will create model-specific subfolder based on system_name in JSON
        return os.path.join(os.path.dirname(__file__), "generated_code")
    
    def browse_input_file(self):
        """Browse for model JSON file"""
        # Start browsing from models directory if it exists
        initial_dir = self.models_dir if os.path.exists(self.models_dir) else os.path.dirname(__file__)
        
        filename = filedialog.askopenfilename(
            title="Select Model JSON File",
            initialdir=initial_dir,
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            
            # Extract model name from path if it's in models folder
            if filename.startswith(self.models_dir):
                rel_path = os.path.relpath(filename, self.models_dir)
                model_name = rel_path.split(os.sep)[0]
                self.selected_model.set(model_name)
                self.log_message(f"Selected model: {model_name}")
            else:
                self.log_message(f"Selected file: {filename}")
            
            # Auto-suggest output directory
            if not self.output_dir.get():
                output = os.path.join(os.path.dirname(filename), "generated_code")
                self.output_dir.set(output)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
            self.log_message(f"Selected output directory: {directory}")
    
    def compile_model(self):
        # Validation
        if not self.input_file.get():
            messagebox.showwarning("Warning", "Please select an input model file!")
            return
        
        if not self.output_dir.get():
            messagebox.showwarning("Warning", "Please select an output directory!")
            return
        
        # Clear console for fresh compilation (Bug Fix #2)
        self.console.delete(1.0, tk.END)
        
        # Reset model analyzer for fresh analysis (Bug Fix #2)
        self.model_analyzer = ModelAnalyzer()
        
        # Reset compiler engine untuk clear state (Bug Fix #1)
        self.compiler_engine = CompilerEngine()
        
        self.log_message("-" * 80)
        self.log_message("Starting compilation process...")
        self.log_message(f"Input: {self.input_file.get()}")
        self.log_message(f"Output: {self.output_dir.get()}")
        self.log_message(f"Target Language: {self.target_lang.get()}")
        self.log_message("-" * 80)
        
        # Start progress bar
        self.progress.start(10)
        self.root.update()
        
        try:
            # Prepare options
            options = {
                'generate_tests': self.generate_tests.get(),
                'generate_docs': self.generate_docs.get(),
                'verbose_mode': self.verbose_mode.get(),
                'include_state_machines': self.include_state_machines.get()
            }
            
            # Run compilation
            self.log_message("[INFO] Parsing model file...")
            self.root.update()
            
            success, generated_files = self.compiler_engine.compile(
                self.input_file.get(),
                self.output_dir.get(),
                self.target_lang.get(),
                options
            )
            
            if success:
                self.log_message("[SUCCESS] Compilation completed successfully!")
                self.log_message(f"Generated {len(generated_files)} files:")
                for file in generated_files:
                    self.log_message(f"  - {file}")
                
                # Store model directory for test run (root model folder, not library)
                if generated_files:
                    # Find main file to get correct directory
                    main_file = next((f for f in generated_files if 'main.py' in f or 'main.java' in f), None)
                    if main_file:
                        self.last_compiled_model_dir = os.path.dirname(main_file)
                    else:
                        # Fallback: go up one level from library
                        first_file_dir = os.path.dirname(generated_files[0])
                        if first_file_dir.endswith('library'):
                            self.last_compiled_model_dir = os.path.dirname(first_file_dir)
                        else:
                            self.last_compiled_model_dir = first_file_dir
                
                # Run analysis
                self.log_message("")
                self.log_message("[INFO] Analyzing model quality...")
                analysis = self.model_analyzer.analyze_model(self.compiler_engine.parser)
                report = self.model_analyzer.generate_report(analysis)
                self.log_message(report)
                
                self.log_message("-" * 80)
                
                # Auto-run test (Bug Fix: Auto test after compile)
                self.log_message("")
                self._run_test()
                
                messagebox.showinfo("Success", f"Compilation successful!\n{len(generated_files)} files generated.\n\nCheck console for test results.")
            else:
                self.log_message("[ERROR] Compilation failed!")
                for error in self.compiler_engine.get_errors():
                    self.log_message(f"[ERROR] {error}")
                self.log_message("-" * 80)
                messagebox.showerror("Error", "Compilation failed! Check console for details.")
                
        except Exception as e:
            self.log_message(f"[FATAL] {str(e)}")
            messagebox.showerror("Fatal Error", str(e))
        finally:
            # Stop progress bar
            self.progress.stop()
    
    def log_message(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.update()
    
    def clear_console(self):
        self.console.delete(1.0, tk.END)
        self.log_message("Console cleared.")
    
    def save_log(self):
        """Save log dengan auto-naming: nama_model-log.txt"""
        # Ambil nama model dari last compiled atau selected model
        model_name = None
        if self.last_compiled_model_dir:
            # Ambil nama folder terakhir dari path
            model_name = os.path.basename(self.last_compiled_model_dir)
        elif self.selected_model.get():
            # Gunakan selected model
            model_name = self.selected_model.get()
        
        if not model_name:
            messagebox.showwarning("Warning", "No model compiled or selected.\nPlease compile a model first.")
            return
        
        # Buat nama file log
        logs_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        base_filename = f"{model_name}-log.txt"
        log_filepath = os.path.join(logs_dir, base_filename)
        
        # Cek jika file sudah ada
        if os.path.exists(log_filepath):
            # Tanya user: replace atau buat duplikat
            response = messagebox.askyesnocancel(
                "File Already Exists",
                f"Log file '{base_filename}' already exists.\n\n" +
                "Yes = Replace existing file\n" +
                "No = Create duplicate with version suffix (v2, v3, etc.)\n" +
                "Cancel = Abort save"
            )
            
            if response is None:  # Cancel
                return
            elif response is False:  # No - create duplicate
                # Cari versi yang belum ada
                version = 2
                while True:
                    versioned_filename = f"{model_name}-log-v{version}.txt"
                    versioned_filepath = os.path.join(logs_dir, versioned_filename)
                    if not os.path.exists(versioned_filepath):
                        log_filepath = versioned_filepath
                        break
                    version += 1
            # Jika Yes, gunakan log_filepath yang sudah ada (akan di-replace)
        
        # Simpan log
        try:
            with open(log_filepath, 'w', encoding='utf-8') as f:
                f.write(self.console.get(1.0, tk.END))
            self.log_message(f"Log saved to: {log_filepath}")
            messagebox.showinfo("Success", f"Log saved to:\n{os.path.basename(log_filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log:\n{str(e)}")
    
    def _run_test(self):
        """Internal test run method (auto-called after compile)"""
        if not self.last_compiled_model_dir:
            return
        
        if not os.path.exists(self.last_compiled_model_dir):
            return
        
        self.log_message("-" * 80)
        self.log_message("🧪 TEST RUN - Executing compiled model...")
        self.log_message(f"Model directory: {self.last_compiled_model_dir}")
        self.log_message("-" * 80)
        
        # Start progress bar
        self.progress.start(10)
        self.root.update()
        
        try:
            # Execute compiled code
            success, stdout, stderr = self.model_analyzer.test_run_compiled_code(
                self.last_compiled_model_dir,
                self.target_lang.get()
            )
            
            # Display execution output
            self.log_message("")
            self.log_message("📤 EXECUTION OUTPUT:")
            self.log_message("-" * 70)
            if stdout:
                for line in stdout.split('\n'):
                    self.log_message(f"  {line}")
            
            if stderr:
                self.log_message("")
                self.log_message("❌ ERRORS:")
                self.log_message("-" * 70)
                for line in stderr.split('\n'):
                    if line.strip():
                        self.log_message(f"  {line}")
            
            # Analyze execution
            self.log_message("")
            self.log_message("-" * 70)
            execution_analysis = self.model_analyzer.analyze_execution_output(stdout, stderr)
            
            if execution_analysis['execution_success']:
                self.log_message("✅ Test run completed successfully!")
            else:
                self.log_message("❌ Test run encountered errors")
            
            self.log_message("")
            
            if execution_analysis['observations']:
                self.log_message("📋 OBSERVATIONS:")
                for obs in execution_analysis['observations']:
                    self.log_message(f"  • {obs}")
                self.log_message("")
            
            if execution_analysis['recommendations']:
                self.log_message("💡 RECOMMENDATIONS:")
                for rec in execution_analysis['recommendations']:
                    self.log_message(f"  • {rec}")
                self.log_message("")
            
            self.log_message("-" * 80)
            
            if success:
                messagebox.showinfo("Test Run Complete", "Test run completed successfully!\nCheck console for detailed analysis.")
            else:
                messagebox.showwarning("Test Run Issues", "Test run completed with issues.\nCheck console for details.")
                
        except Exception as e:
            self.log_message(f"[ERROR] Test run failed: {str(e)}")
            messagebox.showerror("Test Run Error", str(e))
        finally:
            self.progress.stop()
    
    def show_about(self):
        about_text = """PPPL Model Compiler
Version 1.0.0

A tool to compile PPPL model JSON files into 
executable source code.

Features:
• Multi-language code generation
• State machine compilation
• Action language translation
• Model quality analysis
• Test run workflow

Supports: Python, Java, C#, TypeScript, Go

Developed for PPPL Course Project
"""
        messagebox.showinfo("About", about_text)

def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()