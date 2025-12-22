from typing import Dict, List

class StateMachineCompiler:
    """Compile state machines from PPPL model"""
    
    def __init__(self):
        self.states = []
        self.transitions = []
        self.initial_state = None
    
    def compile(self, state_machine: Dict) -> Dict:
        """Compile state machine to intermediate representation"""
        self.initial_state = state_machine.get('initial_state')
        self.states = state_machine.get('states', [])
        self.transitions = state_machine.get('transitions', [])
        
        return {
            'initial_state': self.initial_state,
            'states': self._compile_states(),
            'transitions': self._compile_transitions()
        }
    
    def _compile_states(self) -> List[Dict]:
        """Compile state definitions"""
        compiled_states = []
        
        for state in self.states:
            compiled_state = {
                'name': state['name'],
                'actions': self._extract_actions(state)
            }
            compiled_states.append(compiled_state)
        
        return compiled_states
    
    def _compile_transitions(self) -> List[Dict]:
        """Compile state transitions"""
        compiled_transitions = []
        
        for transition in self.transitions:
            compiled_transition = {
                'from': transition.get('from_state'),
                'to': transition.get('to_state'),
                'event': transition.get('event'),
                'condition': transition.get('condition'),
                'actions': self._extract_transition_actions(transition)
            }
            compiled_transitions.append(compiled_transition)
        
        return compiled_transitions
    
    def _extract_actions(self, state: Dict) -> List[str]:
        """Extract actions from state"""
        actions = []
        
        if 'on_entry' in state:
            actions.append(f"on_entry: {state['on_entry']}")
        
        if 'on_exit' in state:
            actions.append(f"on_exit: {state['on_exit']}")
        
        return actions
    
    def _extract_transition_actions(self, transition: Dict) -> List[str]:
        """Extract actions from transition"""
        actions = []
        
        if 'action' in transition:
            if isinstance(transition['action'], list):
                actions.extend(transition['action'])
            else:
                actions.append(transition['action'])
        
        return actions
    
    def validate(self) -> tuple[bool, List[str]]:
        """Validate state machine"""
        errors = []
        
        if not self.initial_state:
            errors.append("No initial state defined")
        
        if not self.states:
            errors.append("No states defined")
        
        # Check if initial state exists
        state_names = [s['name'] for s in self.states]
        if self.initial_state not in state_names:
            errors.append(f"Initial state '{self.initial_state}' not found in states")
        
        # Validate transitions
        for transition in self.transitions:
            from_state = transition.get('from_state')
            to_state = transition.get('to_state')
            
            if from_state not in state_names:
                errors.append(f"Transition from unknown state: {from_state}")
            
            if to_state not in state_names:
                errors.append(f"Transition to unknown state: {to_state}")
        
        return len(errors) == 0, errors
