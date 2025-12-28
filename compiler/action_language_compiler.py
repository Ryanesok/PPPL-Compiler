from typing import Dict, List, Any, Set

class ActionLanguageCompiler:
    """Compile action language to executable code"""
    
    def __init__(self, target_lang: str = "Python"):
        self.target_lang = target_lang
        self.indent_level = 2
        self.referenced_classes = set()  # Track classes referenced in OAL
        self.valid_classes = set()  # Classes that exist in the model
        
    def compile_action(self, action: Dict, class_name: str) -> str:
        """Compile a single action to code"""
        action_type = action.get('type', '')
        
        if action_type == 'create':
            return self._compile_create(action)
        elif action_type == 'update':
            return self._compile_update(action, class_name)
        elif action_type == 'assign':
            return self._compile_assign(action)
        elif action_type == 'call':
            return self._compile_call(action)
        elif action_type == 'generate':
            return self._compile_generate(action)
        elif action_type == 'log':
            return self._compile_log(action)
        elif action_type == 'transition':
            return self._compile_transition(action, class_name)
        elif action_type == 'select':
            return self._compile_select(action)
        elif action_type == 'delete':
            return self._compile_delete(action)
        elif action_type == 'relate':
            return self._compile_relate(action)
        elif action_type == 'unrelate':
            return self._compile_unrelate(action)
        elif action_type == 'if':
            return self._compile_if(action, class_name)
        elif action_type == 'while':
            return self._compile_while(action, class_name)
        elif action_type == 'for':
            return self._compile_for(action, class_name)
        elif action_type == 'return':
            return self._compile_return(action)
        elif action_type == 'break':
            return "break"
        elif action_type == 'continue':
            return "continue"
        else:
            return f"# Unknown action type: {action_type}"
    
    def compile_actions(self, actions: List[Dict], class_name: str) -> List[str]:
        """Compile multiple actions"""
        code_lines = []
        for action in actions:
            code = self.compile_action(action, class_name)
            if code:
                code_lines.append(code)
        return code_lines
    
    def _compile_create(self, action: Dict) -> str:
        """Compile create action"""
        entity = action.get('entity', '')
        var_name = action.get('variable', entity.lower())
        
        # Parse entity like "MSG:Message"
        if ':' in entity:
            _, class_name = entity.split(':')
        else:
            class_name = entity
        
        # Track referenced class
        if class_name:
            self.referenced_classes.add(class_name)
            # Check if class exists in model
            if self.valid_classes and class_name not in self.valid_classes:
                # Comment out creation of non-existent class
                return f"# TODO: {var_name} = {class_name}()  # Class not defined in model"
        
        return f"{var_name} = {class_name}()"
    
    def _compile_update(self, action: Dict, class_name: str) -> str:
        """Compile update action (attribute assignment)"""
        target = action.get('target', 'self')
        attribute = action.get('attribute', '')
        value = action.get('value', '')
        
        # Handle target
        if target == 'this' or target == 'self':
            target = 'self'
        
        # Handle value formatting
        if isinstance(value, str):
            # Check if it's a state value for state machine
            if attribute == 'Status' and not value.startswith('"'):
                # State transition - use enum
                state_value = value.replace(' ', '_').upper()
                code_value = f"{class_name}State.{state_value}"
            elif value.startswith('self.') or value.startswith('${'):
                # Variable reference or interpolation
                code_value = value.replace('${', '').replace('}', '')
            elif value in ['true', 'false']:
                # Boolean
                code_value = value.capitalize()
            elif value.startswith('"') or value.startswith("'"):
                # Already quoted string
                code_value = value
            else:
                # String value - quote it
                code_value = f'"{value}"'
        else:
            code_value = str(value)
        
        return f"{target}.{attribute} = {code_value}"
    
    def _compile_assign(self, action: Dict) -> str:
        """Compile assign action"""
        target = action.get('target', '')
        value = action.get('value', '')
        
        # Handle different value types
        if isinstance(value, str):
            if value.startswith('self.'):
                # Reference to attribute
                code_value = value
            elif value in ['true', 'false']:
                # Boolean
                code_value = value.capitalize()
            elif value.startswith('"') or value.startswith("'"):
                # String literal
                code_value = value
            else:
                # String value
                code_value = f'"{value}"'
        else:
            code_value = str(value)
        
        return f"{target} = {code_value}"
    
    def _compile_call(self, action: Dict) -> str:
        """Compile call action"""
        target = action.get('target', '')
        method = action.get('method', '')
        params = action.get('parameters', [])
        
        # Parse target.method format
        if '.' in target:
            obj, func = target.rsplit('.', 1)
            param_str = ', '.join([self._format_param(p) for p in params])
            return f"{obj}.{func}({param_str})"
        else:
            # Track class if it's a constructor call (capitalized name)
            if target and target[0].isupper() and target not in ['True', 'False', 'None']:
                self.referenced_classes.add(target)
                # Check if class exists in model
                if self.valid_classes and target not in self.valid_classes:
                    # Comment out call to non-existent class
                    param_str = ', '.join([self._format_param(p) for p in params])
                    return f"# TODO: {target}({param_str})  # Class not defined in model"
            param_str = ', '.join([self._format_param(p) for p in params])
            return f"{target}({param_str})"
    
    def _compile_generate(self, action: Dict) -> str:
        """Compile generate event"""
        event = action.get('event', '')
        target = action.get('target', 'self')
        
        # Generate event to state machine
        return f"{target}.handle_event('{event}')"
    
    def _compile_log(self, action: Dict) -> str:
        """Compile log action"""
        message = action.get('message', '')
        # Handle variable interpolation ${variable} -> {variable}
        import re
        # Replace ${self.attr} with {self.attr}
        message = re.sub(r'\$\{([^}]+)\}', r'{\1}', message)
        return f'print(f"[LOG] {message}")'  # Use f-string for interpolation
    
    def _compile_transition(self, action: Dict, class_name: str) -> str:
        """Compile state transition"""
        to_state = action.get('to_state', '')
        return f"self.Status = {class_name}State.{to_state.upper().replace(' ', '_')}"
    
    def _compile_select(self, action: Dict) -> str:
        """Compile select action (query/filter objects)
        Supports: select any/one/many from instances where ... related by ...
        """
        entity = action.get('entity', '')
        variable = action.get('variable', 'selected')
        where = action.get('where', '')
        cardinality = action.get('cardinality', 'many')  # any, one, many
        related_by = action.get('related_by', '')
        
        # Parse entity
        if ':' in entity:
            _, class_name = entity.split(':')
        else:
            class_name = entity
        
        # Build selection code
        if related_by:
            # Select related objects
            code = f"{variable} = self.{related_by.lower()}s"
        else:
            # Select from instances
            if where:
                # Filter with condition
                where_code = self._compile_expression(where)
                code = f"{variable} = [obj for obj in {class_name}.instances if {where_code}]"
            else:
                # All instances
                code = f"{variable} = {class_name}.instances"
        
        # Apply cardinality
        if cardinality == 'one' or cardinality == 'any':
            code = f"{variable} = {variable}[0] if {variable} else None"
        
        return code
    
    def _compile_delete(self, action: Dict) -> str:
        """Compile delete action (delete object instance)"""
        target = action.get('target', 'self')
        if target == 'self' or target == 'this':
            return "# TODO: Delete self from instances and cleanup relationships"
        return f"del {target}"
    
    def _compile_relate(self, action: Dict) -> str:
        """Compile relate action (establish relationship)
        Format: relate <from> to <to> across <relationship>
        """
        from_obj = action.get('from', 'self')
        to_obj = action.get('to', '')
        relationship = action.get('relationship', '')
        across = action.get('across', relationship)  # R1, R2, etc.
        
        # Generate bidirectional relationship code
        code_lines = []
        code_lines.append(f"# Relate {from_obj} to {to_obj} across {across}")
        
        # Determine relationship attribute names from relationship ID
        # For now, use simple naming convention
        to_attr = to_obj.lower() if to_obj else 'related_object'
        from_attr = from_obj.lower() if from_obj != 'self' else 'owner'
        
        code_lines.append(f"{from_obj}.{to_attr}s.append({to_obj})")
        code_lines.append(f"{to_obj}.{from_attr} = {from_obj}")
        
        return '\n'.join(code_lines)
    
    def _compile_unrelate(self, action: Dict) -> str:
        """Compile unrelate action (remove relationship)
        Format: unrelate <from> from <to> across <relationship>
        """
        from_obj = action.get('from', 'self')
        to_obj = action.get('to', '')
        relationship = action.get('relationship', '')
        across = action.get('across', relationship)
        
        code_lines = []
        code_lines.append(f"# Unrelate {from_obj} from {to_obj} across {across}")
        
        to_attr = to_obj.lower() if to_obj else 'related_object'
        from_attr = from_obj.lower() if from_obj != 'self' else 'owner'
        
        code_lines.append(f"if {to_obj} in {from_obj}.{to_attr}s:")
        code_lines.append(f"    {from_obj}.{to_attr}s.remove({to_obj})")
        code_lines.append(f"{to_obj}.{from_attr} = None")
        
        return '\n'.join(code_lines)
    
    def _compile_if(self, action: Dict, class_name: str) -> str:
        """Compile if-elif-else statement"""
        condition = action.get('condition', '')
        then_actions = action.get('then', [])
        elif_blocks = action.get('elif', [])
        else_actions = action.get('else', [])
        
        code_lines = []
        
        # If block
        cond_code = self._compile_expression(condition)
        code_lines.append(f"if {cond_code}:")
        for act in then_actions:
            act_code = self.compile_action(act, class_name)
            code_lines.append(f"    {act_code}")
        
        # Elif blocks
        for elif_block in elif_blocks:
            elif_cond = self._compile_expression(elif_block.get('condition', ''))
            code_lines.append(f"elif {elif_cond}:")
            for act in elif_block.get('then', []):
                act_code = self.compile_action(act, class_name)
                code_lines.append(f"    {act_code}")
        
        # Else block
        if else_actions:
            code_lines.append("else:")
            for act in else_actions:
                act_code = self.compile_action(act, class_name)
                code_lines.append(f"    {act_code}")
        
        return '\n'.join(code_lines)
    
    def _compile_while(self, action: Dict, class_name: str) -> str:
        """Compile while loop"""
        condition = action.get('condition', '')
        body = action.get('body', [])
        
        code_lines = []
        cond_code = self._compile_expression(condition)
        code_lines.append(f"while {cond_code}:")
        
        for act in body:
            act_code = self.compile_action(act, class_name)
            code_lines.append(f"    {act_code}")
        
        return '\n'.join(code_lines)
    
    def _compile_for(self, action: Dict, class_name: str) -> str:
        """Compile for loop"""
        variable = action.get('variable', 'item')
        iterable = action.get('iterable', '')
        body = action.get('body', [])
        
        code_lines = []
        code_lines.append(f"for {variable} in {iterable}:")
        
        for act in body:
            act_code = self.compile_action(act, class_name)
            code_lines.append(f"    {act_code}")
        
        return '\n'.join(code_lines)
    
    def _compile_return(self, action: Dict) -> str:
        """Compile return statement"""
        value = action.get('value', '')
        if value:
            return f"return {self._compile_expression(value)}"
        return "return"
    
    def _compile_expression(self, expr: str) -> str:
        """Compile expression with keyword support
        Handles: empty, not_empty, cardinality, and, or, not, true, false
        """
        if not isinstance(expr, str):
            return str(expr)
        
        # Replace xtUML keywords with Python equivalents
        replacements = [
            ('empty', 'not'),  # empty(list) -> not list
            ('not_empty', ''),  # not_empty(list) -> list
            ('cardinality', 'len'),  # cardinality(list) -> len(list)
            (' and ', ' and '),
            (' or ', ' or '),
            (' not ', ' not '),
            ('true', 'True'),
            ('false', 'False'),
            ('self.', 'self.'),
            ('${', ''),  # Remove ${} interpolation markers
            ('}', ''),
        ]
        
        result = expr
        for old, new in replacements:
            if old == 'empty':
                # empty(x) -> not x
                import re
                result = re.sub(r'empty\s*\(([^)]+)\)', r'not \1', result)
            elif old == 'not_empty':
                # not_empty(x) -> x
                import re
                result = re.sub(r'not_empty\s*\(([^)]+)\)', r'\1', result)
            elif old in result:
                result = result.replace(old, new)
        
        return result
    
    def _format_param(self, param: Any) -> str:
        """Format parameter for function call"""
        if isinstance(param, str):
            if param.startswith('self.') or param.startswith('param_'):
                return param
            else:
                return f'"{param}"'
        else:
            return str(param)
    
    def compile_state_entry_exit(self, state: Dict, class_name: str) -> Dict[str, List[str]]:
        """Compile state entry and exit actions"""
        result = {
            'on_entry': [],
            'on_exit': []
        }
        
        if 'on_entry' in state and state['on_entry']:
            for action in state['on_entry']:
                code = self.compile_action(action, class_name)
                if code:
                    result['on_entry'].append(code)
        
        if 'on_exit' in state and state['on_exit']:
            for action in state['on_exit']:
                code = self.compile_action(action, class_name)
                if code:
                    result['on_exit'].append(code)
        
        return result
    
    def get_referenced_classes(self) -> Set[str]:
        """Get all classes referenced in compiled OAL"""
        return self.referenced_classes.copy()
    
    def clear_referenced_classes(self):
        """Clear tracked referenced classes"""
        self.referenced_classes.clear()
    
    def set_valid_classes(self, classes: Set[str]):
        """Set list of classes that exist in the model"""
        self.valid_classes = classes
