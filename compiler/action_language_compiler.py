from typing import Dict, List, Any

class ActionLanguageCompiler:
    """Compile action language to executable code"""
    
    def __init__(self, target_lang: str = "Python"):
        self.target_lang = target_lang
        self.indent_level = 2
        
    def compile_action(self, action: Dict, class_name: str) -> str:
        """Compile a single action to code"""
        action_type = action.get('type', '')
        
        if action_type == 'create':
            return self._compile_create(action)
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
        
        return f"{var_name} = {class_name}()"
    
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
        return f'print("[LOG] {message}")'
    
    def _compile_transition(self, action: Dict, class_name: str) -> str:
        """Compile state transition"""
        to_state = action.get('to_state', '')
        return f"self.Status = {class_name}State.{to_state.upper().replace(' ', '_')}"
    
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
