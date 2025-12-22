from .code_generator import CodeGenerator
from .action_language_compiler import ActionLanguageCompiler
from .oal_generator import OALGenerator
from typing import Dict, List
import textwrap

class PythonGenerator(CodeGenerator):
    """Generate Python code from PPPL model"""
    
    def __init__(self, output_dir: str, options: Dict, model_name: str = "system"):
        super().__init__(output_dir, options, model_name)
        self.action_compiler = ActionLanguageCompiler("Python")
        self.oal_generator = OALGenerator("Python")
    
    def get_file_extension(self) -> str:
        return ".py"
    
    def generate_class(self, class_data: Dict, domain: str) -> str:
        """Generate Python class code"""
        class_name = class_data['name']
        entity_type = class_data.get('entity_type', 'class')
        description = class_data.get('description', '')
        attributes = class_data.get('attributes', [])
        state_machine = class_data.get('state_machine', None)
        
        code = []
        
        # Imports
        code.append("from dataclasses import dataclass, field")
        code.append("from typing import Optional, List")
        code.append("from datetime import datetime")
        code.append("from uuid import uuid4, UUID")
        code.append("from enum import Enum")
        code.append("\n")
        
        # Generate state enum if state machine exists
        if state_machine and self.options.get('include_state_machines', True):
            code.append(self._generate_state_enum(class_name, state_machine))
            code.append("\n")
        
        # Class definition
        code.append("@dataclass")
        code.append(f"class {class_name}:")
        code.append(f'    """{description}"""')
        code.append("\n")
        
        # Generate attributes
        for attr in attributes:
            attr_code = self._generate_attribute(attr, class_name, state_machine)
            code.append(f"    {attr_code}")
        
        if not attributes:
            code.append("    pass")
        
        code.append("\n")
        
        # Generate methods
        if state_machine and self.options.get('include_state_machines', True):
            state_methods = self._generate_state_methods(class_name, state_machine)
            code.append(state_methods)
        
        # Generate auto-generated OAL methods
        relationships = self._get_class_relationships(class_name, domain)
        auto_methods = self.oal_generator.generate_crud_operations(class_data, relationships)
        if auto_methods:
            code.append("\n")
            code.append("    # Auto-generated methods")
            for method in auto_methods:
                code.append(method)
        
        return "\n".join(code)
    
    def _generate_attribute(self, attr: Dict, class_name: str = None, state_machine: Dict = None) -> str:
        """Generate attribute code"""
        name = attr['name']
        data_type = attr['data_type']
        default_value = attr.get('default_value', None)
        
        # Sanitize attribute name (remove special characters, spaces, etc)
        sanitized_name = self._sanitize_identifier(name)
        
        # Map PPPL types to Python types
        type_mapping = {
            'string': 'str',
            'integer': 'int',
            'float': 'float',
            'boolean': 'bool',
            'datetime': 'datetime',
            'uuid': 'UUID',
            'state': 'str'
        }
        
        py_type = type_mapping.get(data_type, 'str')
        
        # Special handling for state attributes
        if data_type == 'state' and class_name and state_machine:
            if default_value:
                state_enum_value = self._sanitize_identifier(default_value).upper()
                if not state_enum_value:
                    state_enum_value = 'UNKNOWN_STATE'
                return f"{sanitized_name}: '{class_name}State' = field(default_factory=lambda: {class_name}State.{state_enum_value})"
            else:
                initial_state = state_machine.get('initial_state', '')
                if initial_state:
                    state_enum_value = self._sanitize_identifier(initial_state).upper()
                    if not state_enum_value:
                        state_enum_value = 'UNKNOWN_STATE'
                    return f"{sanitized_name}: '{class_name}State' = field(default_factory=lambda: {class_name}State.{state_enum_value})"
        
        if default_value:
            if py_type == 'UUID':
                return f"{sanitized_name}: {py_type} = field(default_factory=uuid4)"
            elif py_type == 'str':
                # Escape special characters in string
                escaped_value = str(default_value).replace('\\', '\\\\').replace('"', '\\"')
                return f'{sanitized_name}: {py_type} = "{escaped_value}"'
            elif py_type == 'bool':
                # Convert JSON boolean to Python boolean
                py_bool = 'True' if str(default_value).lower() in ['true', '1'] else 'False'
                return f"{sanitized_name}: {py_type} = {py_bool}"
            else:
                return f"{sanitized_name}: {py_type} = {default_value}"
        else:
            if py_type == 'UUID':
                return f"{sanitized_name}: {py_type} = field(default_factory=uuid4)"
            else:
                return f"{sanitized_name}: Optional[{py_type}] = None"
    
    def _sanitize_identifier(self, name: str) -> str:
        """Sanitize identifier to be valid Python name"""
        import re
        import keyword
        # Replace spaces, dashes, dots with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Remove leading digits
        sanitized = re.sub(r'^[0-9]+', '', sanitized)
        # Ensure not empty
        if not sanitized:
            sanitized = 'attribute'
        # Avoid Python keywords
        if keyword.iskeyword(sanitized):
            sanitized = sanitized + '_'
        return sanitized
    
    def _generate_state_enum(self, class_name: str, state_machine: Dict) -> str:
        """Generate state enum"""
        states = state_machine.get('states', [])
        
        code = [f"class {class_name}State(Enum):"]
        code.append(f'    """States for {class_name}"""')
        
        for state in states:
            state_name_raw = state.get('name', '')
            if not state_name_raw or not state_name_raw.strip():
                # Skip empty or whitespace-only state names
                continue
            
            # Sanitize state name for enum key
            state_name_sanitized = self._sanitize_identifier(state_name_raw).upper()
            
            # Ensure unique and valid
            if not state_name_sanitized:
                state_name_sanitized = 'UNKNOWN_STATE'
            
            code.append(f'    {state_name_sanitized} = "{state_name_raw}"')
        
        return "\n".join(code)
    
    def _generate_state_methods(self, class_name: str, state_machine: Dict) -> str:
        """Generate state transition methods"""
        code = []
        transitions = state_machine.get('transitions', [])
        states = state_machine.get('states', [])
        
        # Generate event handler methods for each transition
        event_methods = {}
        for transition in transitions:
            event = transition.get('event', '')
            if event and event not in event_methods:
                event_methods[event] = []
            
            if event:
                event_methods[event].append(transition)
        
        # Generate methods for each unique event
        for event, trans_list in event_methods.items():
            method_name = self._sanitize_identifier(event).lower()
            if not method_name:
                method_name = 'unknown_event'
            code.append(f"    def {method_name}(self):")
            code.append(f'        """Handle {event} event"""')
            
            # Generate state transition logic
            for trans in trans_list:
                from_state = trans.get('from_state', '')
                to_state = trans.get('to_state', '')
                actions = trans.get('actions', [])
                
                from_state_var = self._sanitize_identifier(from_state).upper()
                if not from_state_var:
                    from_state_var = 'UNKNOWN_STATE'
                to_state_var = self._sanitize_identifier(to_state).upper()
                if not to_state_var:
                    to_state_var = 'UNKNOWN_STATE'
                
                code.append(f"        if self.Status == {class_name}State.{from_state_var}:")
                
                # Execute transition actions
                if actions:
                    for action in actions:
                        action_code = self.action_compiler.compile_action(action, class_name)
                        if action_code:
                            code.append(f"            {action_code}")
                
                # Transition to new state
                code.append(f"            self.Status = {class_name}State.{to_state_var}")
                
                # Execute on_exit of old state
                old_state = next((s for s in states if s['name'] == from_state), None)
                if old_state and old_state.get('on_exit'):
                    code.append(f"            # On exit {from_state}")
                    for action in old_state['on_exit']:
                        action_code = self.action_compiler.compile_action(action, class_name)
                        if action_code:
                            code.append(f"            {action_code}")
                
                # Execute on_entry of new state
                new_state = next((s for s in states if s['name'] == to_state), None)
                if new_state and new_state.get('on_entry'):
                    code.append(f"            # On entry {to_state}")
                    for action in new_state['on_entry']:
                        action_code = self.action_compiler.compile_action(action, class_name)
                        if action_code:
                            code.append(f"            {action_code}")
                
                code.append(f"            return True")
            
            code.append("        return False")
            code.append("")
        
        # Generate generic handle_event dispatcher method
        if event_methods:
            code.append("    def handle_event(self, event_name: str) -> bool:")
            code.append('        """Handle any event by dispatching to appropriate method"""')
            code.append("        import re")
            code.append("        event_method = re.sub(r'[^a-zA-Z0-9_]', '_', event_name).lower()")
            code.append("        if hasattr(self, event_method):")
            code.append("            method = getattr(self, event_method)")
            code.append("            return method()")
            code.append("        return False")
            code.append("")
        
        return "\n".join(code)
    
    def generate_state_machine(self, state_machine: Dict, class_name: str) -> str:
        """Generate state machine code"""
        return "# State machine generated inline with class"
    
    def generate_relationship(self, relationship: Dict) -> str:
        """Generate relationship code"""
        rel_id = relationship['relationship_id']
        description = relationship['description']
        
        return f"# Relationship {rel_id}: {description}"
    
    def generate_main_file(self, parser) -> str:
        """Generate main.py entry point"""
        code = []
        
        system_name = parser.model.get('system_name', 'System')
        
        code.append('"""')
        code.append(f"{system_name}")
        code.append(f"Generated by PPPL Model Compiler")
        code.append('"""')
        code.append("\n")
        
        # Import all generated classes from library
        code.append("# Import from library")
        for class_key, class_info in parser.get_classes().items():
            class_name = class_info['class']['name']
            code.append(f"from library.{class_name} import {class_name}")
        
        code.append("\n")
        code.append("def main():")
        code.append('    """Main entry point"""')
        code.append(f'    print("="*60)')
        code.append(f'    print("{system_name}")')
        code.append(f'    print("="*60)')
        code.append('    print("")')
        code.append("\n")
        code.append('    # Initialize system components')
        code.append('    print("Initializing active classes with state machines...")')
        code.append('    print("")')
        
        # Create instances for active classes
        instances = []
        for class_key, class_info in parser.get_classes().items():
            class_name = class_info['class']['name']
            entity_type = class_info['class'].get('entity_type', 'class')
            has_state_machine = 'state_machine' in class_info['class']
            
            if entity_type == 'class' and has_state_machine:
                var_name = class_name.lower()
                instances.append((var_name, class_name, class_info))
                code.append(f'    print("Creating {class_name}...")')
                code.append(f'    {var_name} = {class_name}()')
                code.append(f'    print(f"  Status: {{{var_name}.Status.value}}")')
                code.append('    print("")')
        
        # Demo state transitions
        if instances:
            code.append('    # Demo: Trigger some state transitions')
            code.append('    print("Testing state transitions...")')
            code.append('    print("")')
            
            # Get first instance with transitions
            if instances:
                var_name, class_name, class_info = instances[0]
                state_machine = class_info['class'].get('state_machine', {})
                transitions = state_machine.get('transitions', [])
                if transitions:
                    # Get first event
                    first_event = transitions[0].get('event', '')
                    if first_event:
                        code.append(f"    print('Triggering event: {first_event}')")
                        code.append(f"    {var_name}.handle_event('{first_event}')")
        
        code.append('    print("System running successfully!")')
        code.append('    print("All state machines are operational.")')
        
        # Add workflow demonstration
        workflow_code = self.oal_generator.generate_main_workflow(parser)
        if workflow_code:
            code.append("\n")
            code.append(workflow_code)
            code.append("\n")
            code.append("    # Run workflow demonstration")
            code.append("    demonstrate_workflow()")
        
        code.append("\n")
        code.append('if __name__ == "__main__":')
        code.append("    main()")
        
        return "\n".join(code)
    
    def _get_class_relationships(self, class_name: str, domain: str) -> List[Dict]:
        """Get relationships involving this class"""
        # This will be populated by parser, for now return empty
        return []
    
    def generate_library_init(self, parser) -> str:
        """Generate __init__.py for library"""
        code = []
        code.append('"""Generated library package"""')
        code.append("\n")
        
        # Import all classes
        for class_key, class_info in parser.get_classes().items():
            class_name = class_info['class']['name']
            code.append(f"from .{class_name} import {class_name}")
        
        code.append("\n")
        code.append("__all__ = [")
        for class_key, class_info in parser.get_classes().items():
            class_name = class_info['class']['name']
            code.append(f'    "{class_name}",')
        code.append("]")
        
        return "\n".join(code)
