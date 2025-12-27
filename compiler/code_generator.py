from abc import ABC, abstractmethod
from typing import Dict, List, Any
import os
import re

class CodeGenerator(ABC):
    """Base class for code generators"""
    
    def __init__(self, output_dir: str, options: Dict[str, bool], model_name: str = "system"):
        self.output_dir = output_dir
        self.options = options
        self.model_name = self._sanitize_name(model_name)
        self.generated_files = []
        
        # Create model-specific directory structure
        self.model_dir = os.path.join(output_dir, self.model_name)
        self.library_dir = os.path.join(self.model_dir, "library")
        self.docs_dir = os.path.join(self.model_dir, "docs")
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize model name for folder name"""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', name)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.lower()
        
    @abstractmethod
    def generate_class(self, class_data: Dict, domain: str) -> str:
        """Generate code for a single class"""
        pass
    
    @abstractmethod
    def generate_state_machine(self, state_machine: Dict, class_name: str) -> str:
        """Generate state machine code"""
        pass
    
    @abstractmethod
    def generate_relationship(self, relationship: Dict) -> str:
        """Generate relationship code"""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Get file extension for target language"""
        pass
    
    def create_output_dir(self):
        """Create output directory structure if not exists"""
        # Create model directory
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        
        # Create library directory
        if not os.path.exists(self.library_dir):
            os.makedirs(self.library_dir)
        
        # Create docs directory if documentation enabled
        if self.options.get('generate_docs', False):
            if not os.path.exists(self.docs_dir):
                os.makedirs(self.docs_dir)
    
    def write_file(self, filename: str, content: str, is_library: bool = True):
        """Write generated code to file"""
        self.create_output_dir()
        
        # Determine target directory
        if is_library:
            target_dir = self.library_dir
        else:
            target_dir = self.model_dir
        
        filepath = os.path.join(target_dir, filename)
        
        # Create subdirectories if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.generated_files.append(filepath)
        return filepath
    
    def clean_output_dir(self):
        """Clean existing model output directory to avoid conflicts"""
        if os.path.exists(self.model_dir):
            import shutil
            shutil.rmtree(self.model_dir)
    
    def generate_project(self, parser) -> List[str]:
        """Generate complete project from parsed model"""
        # Store parser reference for relationship lookups
        if hasattr(self, 'parser'):
            self.parser = parser
        
        # Clean old output first (once at the start)
        self.clean_output_dir()
        
        # Create directory structure
        self.create_output_dir()
        
        # Generate classes in library folder
        for class_key, class_info in parser.get_classes().items():
            class_code = self.generate_class(
                class_info['class'], 
                class_info['domain']
            )
            
            class_name = class_info['class']['name']
            filename = f"{class_name}{self.get_file_extension()}"
            self.write_file(filename, class_code, is_library=True)
        
        # Generate __init__.py for library (Python specific)
        if self.get_file_extension() == ".py":
            init_code = self.generate_library_init(parser)
            self.write_file("__init__.py", init_code, is_library=True)
        
        # Generate main file in root model folder
        main_code = self.generate_main_file(parser)
        self.write_file(f"main{self.get_file_extension()}", main_code, is_library=False)
        # Generate documentation if enabled
        if self.options.get('generate_docs', False):
            from .documentation_generator import DocumentationGenerator
            doc_gen = DocumentationGenerator()
            doc_content = doc_gen.generate_documentation(parser, self.output_dir, self.model_name)
            doc_file = os.path.join(self.docs_dir, "API_DOCUMENTATION.md")
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(doc_content)
            self.generated_files.append(doc_file)
        
        
        # Generate README
        readme_code = self.generate_readme(parser)
        self.write_file("README.md", readme_code, is_library=False)
        
        return self.generated_files
    
    @abstractmethod
    def generate_main_file(self, parser) -> str:
        """Generate main entry point file"""
        pass
    
    def generate_library_init(self, parser) -> str:
        """Generate __init__.py for library (Python specific)"""
        return ""
    
    def generate_readme(self, parser) -> str:
        """Generate README file"""
        system_name = parser.model.get('system_name', 'System')
        version = parser.model.get('version', '1.0.0')
        
        readme = f"""# {system_name}

Version: {version}

## How to Run

```bash
python main{self.get_file_extension()}
```

## Project Structure

- `main{self.get_file_extension()}` - Main entry point
- `library/` - Generated classes and components

## Generated Files

"""
        for class_key, class_info in parser.get_classes().items():
            class_name = class_info['class']['name']
            readme += f"- {class_name}\n"
        
        return readme
