from typing import Dict, List

class OALGenerator:
    """Auto-generate Object Action Language for common operations"""
    
    def __init__(self, target_lang: str = "Python"):
        self.target_lang = target_lang
        
    def generate_crud_operations(self, class_data: Dict, relationships: List[Dict]) -> List[str]:
        """Generate CRUD operations for a class"""
        operations = []
        class_name = class_data['name']
        
        # Generate relationship navigation methods
        for rel in relationships:
            nav_methods = self._generate_relationship_navigation(class_name, rel)
            operations.extend(nav_methods)
        
        # Generate utility methods
        operations.extend(self._generate_utility_methods(class_data))
        
        return operations
    
    def _generate_relationship_navigation(self, class_name: str, relationship: Dict) -> List[str]:
        """Generate methods to navigate relationships"""
        methods = []
        
        # Parse relationship
        rel_id = relationship.get('relationship_id', '')
        from_class = relationship.get('from', {})
        to_class = relationship.get('to', {})
        rel_type = relationship.get('type', 'association')
        
        # Check if this class is involved
        from_name = from_class.get('class', '')
        to_name = to_class.get('class', '')
        
        if from_name == class_name:
            # Generate method to get related objects
            method = self._create_navigation_method(
                from_name, to_name, rel_id, 
                from_class.get('multiplicity', '1'),
                to_class.get('multiplicity', '1')
            )
            methods.append(method)
        
        if to_name == class_name and rel_type != 'aggregation':
            # Generate reverse navigation
            method = self._create_navigation_method(
                to_name, from_name, rel_id,
                to_class.get('multiplicity', '1'),
                from_class.get('multiplicity', '1'),
                reverse=True
            )
            methods.append(method)
        
        return methods
    
    def _create_navigation_method(self, from_class: str, to_class: str, 
                                   rel_id: str, from_mult: str, to_mult: str,
                                   reverse: bool = False) -> str:
        """Create relationship navigation method"""
        if self.target_lang == "Python":
            # Determine return type based on multiplicity
            is_many = to_mult in ['*', 'M', '0..*', '1..*']
            
            method_name = f"get_{to_class.lower()}{'s' if is_many else ''}"
            if reverse:
                method_name += f"_via_{rel_id}"
            
            code = []
            code.append(f"    def {method_name}(self):")
            code.append(f'        """Navigate {rel_id}: Get related {to_class}(s)"""')
            
            if is_many:
                code.append(f"        # TODO: Implement relationship navigation")
                code.append(f"        # return [obj for obj in {to_class}.instances if obj.relates_to(self)]")
                code.append(f"        return []")
            else:
                code.append(f"        # TODO: Implement relationship navigation")
                code.append(f"        # return {to_class}.find_related(self)")
                code.append(f"        return None")
            
            return "\n".join(code)
        
        return ""
    
    def _generate_utility_methods(self, class_data: Dict) -> List[str]:
        """Generate utility methods for class"""
        methods = []
        class_name = class_data['name']
        
        if self.target_lang == "Python":
            # Generate __str__ method
            attributes = class_data.get('attributes', [])
            key_attrs = [attr['name'] for attr in attributes[:3]]  # First 3 attributes
            
            code = []
            code.append("    def __str__(self):")
            code.append(f'        """String representation of {class_name}"""')
            
            if key_attrs:
                attr_repr = ", ".join([f"{attr}={{self.{attr}}}" for attr in key_attrs])
                code.append(f'        return f"{class_name}({attr_repr})"')
            else:
                code.append(f'        return f"{class_name}()"')
            
            methods.append("\n".join(code))
            
            # Generate to_dict method for serialization
            code = []
            code.append("    def to_dict(self):")
            code.append(f'        """Convert {class_name} to dictionary"""')
            code.append("        return {")
            
            for attr in attributes:
                attr_name = attr['name']
                data_type = attr.get('data_type', 'string')
                
                if data_type == 'state':
                    code.append(f"            '{attr_name}': self.{attr_name}.value if hasattr(self.{attr_name}, 'value') else str(self.{attr_name}),")
                elif data_type == 'datetime':
                    code.append(f"            '{attr_name}': self.{attr_name}.isoformat() if self.{attr_name} else None,")
                elif data_type == 'uuid':
                    code.append(f"            '{attr_name}': str(self.{attr_name}) if self.{attr_name} else None,")
                else:
                    code.append(f"            '{attr_name}': self.{attr_name},")
            
            code.append("        }")
            
            methods.append("\n".join(code))
            
            # Generate validate method
            code = []
            code.append("    def validate(self) -> bool:")
            code.append(f'        """Validate {class_name} data"""')
            code.append("        # TODO: Add validation logic")
            
            # Basic validation for required fields
            required_attrs = [attr for attr in attributes if not attr.get('default_value')]
            if required_attrs:
                code.append("        # Check required fields")
                for attr in required_attrs:
                    code.append(f"        if self.{attr['name']} is None:")
                    code.append(f"            return False")
            
            code.append("        return True")
            
            methods.append("\n".join(code))
        
        return methods
    
    def generate_main_workflow(self, parser) -> str:
        """Generate main workflow demonstrating system usage"""
        if self.target_lang == "Python":
            code = []
            code.append("def demonstrate_workflow():")
            code.append('    """Demonstrate complete system workflow"""')
            code.append('    print("\\n" + "="*60)')
            code.append('    print("WORKFLOW DEMONSTRATION")')
            code.append('    print("="*60 + "\\n")')
            code.append("")
            
            # Get active classes
            active_classes = []
            for class_key, class_info in parser.get_classes().items():
                if class_info['class'].get('entity_type') == 'class':
                    active_classes.append(class_info['class'])
            
            if active_classes:
                # Demonstrate first active class workflow
                first_class = active_classes[0]
                class_name = first_class['name']
                
                code.append(f'    print("1. Creating {class_name} instance...")')
                code.append(f'    obj = {class_name}()')
                code.append(f'    print(f"   Created: {{obj}}")')
                code.append('    print("")')
                
                # If has state machine, demonstrate transitions
                if 'state_machine' in first_class:
                    sm = first_class['state_machine']
                    transitions = sm.get('transitions', [])
                    
                    if transitions:
                        code.append('    print("2. Triggering state transitions...")')
                        
                        # Get first few transitions
                        for i, trans in enumerate(transitions[:3], 1):
                            event = trans.get('event', '')
                            if event:
                                method_name = event.lower().replace(' ', '_')
                                code.append(f'    print(f"   {{i}}. Triggering: {event}")')
                                code.append(f'    obj.{method_name}()')
                                code.append(f'    print(f"      Status: {{obj.Status.value}}")')
                        
                        code.append('    print("")')
                
                code.append('    print("3. Validating instance...")')
                code.append('    if obj.validate():')
                code.append('        print("   ✓ Validation passed")')
                code.append('    else:')
                code.append('        print("   ✗ Validation failed")')
                code.append('    print("")')
                
                code.append('    print("4. Serializing to dictionary...")')
                code.append('    data = obj.to_dict()')
                code.append('    print(f"   Keys: {list(data.keys())}")')
                code.append('    print("")')
            
            code.append('    print("="*60)')
            code.append('    print("Workflow demonstration complete!")')
            code.append('    print("="*60)')
            
            return "\n".join(code)
        
        return ""
