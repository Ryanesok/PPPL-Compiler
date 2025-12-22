from .parser import ModelParser
from .python_generator import PythonGenerator
from .java_generator import JavaGenerator
from typing import Dict, List
import os

class CompilerEngine:
    """Main compiler engine that orchestrates the compilation process"""
    
    def __init__(self):
        self.parser = ModelParser()
        self.generator = None
        self.errors = []
        self.warnings = []
        
    def compile(self, input_file: str, output_dir: str, 
                target_lang: str, options: Dict) -> tuple[bool, List[str]]:
        """
        Compile PPPL model to target language
        
        Returns: (success, generated_files)
        """
        try:
            # Step 1: Parse model
            self.parser.parse_file(input_file)
            
            # Step 2: Validate
            valid, errors = self.parser.validate()
            if not valid:
                self.errors.extend(errors)
                return False, []
            
            # Step 3: Get model name
            model_name = self.parser.model.get('system_name', 'system')
            
            # Step 4: Select generator
            self.generator = self._get_generator(target_lang, output_dir, options, model_name)
            if not self.generator:
                self.errors.append(f"Unsupported target language: {target_lang}")
                return False, []
            
            # Step 5: Generate code
            generated_files = self.generator.generate_project(self.parser)
            
            return True, generated_files
            
        except Exception as e:
            self.errors.append(f"Compilation error: {str(e)}")
            return False, []
    
    def _get_generator(self, target_lang: str, output_dir: str, options: Dict, model_name: str):
        """Get appropriate code generator for target language"""
        generators = {
            'Python': PythonGenerator,
            'Java': JavaGenerator,
            # Add more generators here
            # 'C#': CSharpGenerator,
            # 'TypeScript': TypeScriptGenerator,
            # 'Go': GoGenerator,
        }
        
        generator_class = generators.get(target_lang)
        if generator_class:
            return generator_class(output_dir, options, model_name)
        return None
    
    def get_errors(self) -> List[str]:
        """Get compilation errors"""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Get compilation warnings"""
        return self.warnings
