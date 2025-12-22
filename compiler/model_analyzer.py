from typing import Dict, List, Tuple
import subprocess
import sys
import os

class ModelAnalyzer:
    """Analyze compiled model and provide suggestions"""
    
    def __init__(self):
        self.issues = []
        self.suggestions = []
        self.stats = {}
        
    def analyze_model(self, parser) -> Dict:
        """Analyze model completeness and quality"""
        self.issues = []
        self.suggestions = []
        
        model = parser.model
        domains = parser.get_domains()
        classes = parser.get_classes()
        relationships = parser.get_relationships()
        
        # Statistics
        self.stats = {
            'total_domains': len(domains),
            'total_classes': len(classes),
            'total_relationships': len(relationships),
            'active_classes': 0,
            'passive_classes': 0,
            'classes_with_state_machines': 0,
            'total_states': 0,
            'total_transitions': 0,
            'total_actions': 0
        }
        
        # Analyze classes
        for class_key, class_info in classes.items():
            cls = class_info['class']
            entity_type = cls.get('entity_type', 'class')
            
            if entity_type == 'class':
                self.stats['active_classes'] += 1
            else:
                self.stats['passive_classes'] += 1
            
            # Check state machine
            if 'state_machine' in cls:
                self.stats['classes_with_state_machines'] += 1
                sm = cls['state_machine']
                self.stats['total_states'] += len(sm.get('states', []))
                self.stats['total_transitions'] += len(sm.get('transitions', []))
                
                # Count actions
                for state in sm.get('states', []):
                    if 'on_entry' in state:
                        self.stats['total_actions'] += len(state['on_entry'])
                    if 'on_exit' in state:
                        self.stats['total_actions'] += len(state['on_exit'])
                
                for transition in sm.get('transitions', []):
                    if 'actions' in transition:
                        self.stats['total_actions'] += len(transition['actions'])
                
                # Validate state machine
                self._validate_state_machine(cls['name'], sm)
            else:
                if entity_type == 'class':
                    self.issues.append(f"Active class '{cls['name']}' has no state machine")
                    self.suggestions.append(f"Add state machine to '{cls['name']}' to define its behavior")
            
            # Check attributes
            if not cls.get('attributes'):
                self.issues.append(f"Class '{cls['name']}' has no attributes")
                self.suggestions.append(f"Define attributes for '{cls['name']}' to store data")
        
        # Analyze relationships
        if not relationships:
            self.issues.append("Model has no relationships defined")
            self.suggestions.append("Add relationships between classes to model associations")
        
        # Quality checks
        if self.stats['active_classes'] == 0:
            self.issues.append("No active classes with behavior")
            self.suggestions.append("Define at least one active class with state machine")
        
        if self.stats['total_actions'] == 0:
            self.suggestions.append("Add action language to states and transitions for executable behavior")
        
        return {
            'stats': self.stats,
            'issues': self.issues,
            'suggestions': self.suggestions
        }
    
    def _validate_state_machine(self, class_name: str, state_machine: Dict):
        """Validate state machine completeness"""
        states = state_machine.get('states', [])
        transitions = state_machine.get('transitions', [])
        initial_state = state_machine.get('initial_state')
        
        if not initial_state:
            self.issues.append(f"{class_name}: No initial state defined")
        
        if len(states) < 2:
            self.suggestions.append(f"{class_name}: State machine has only {len(states)} state(s). Consider adding more states for richer behavior")
        
        if len(transitions) == 0:
            self.issues.append(f"{class_name}: State machine has no transitions")
            self.suggestions.append(f"{class_name}: Add transitions between states to enable state changes")
        
        # Check unreachable states
        reachable = {initial_state} if initial_state else set()
        for trans in transitions:
            to_state = trans.get('to_state')
            if to_state:
                reachable.add(to_state)
        
        state_names = {s['name'] for s in states}
        unreachable = state_names - reachable
        if unreachable:
            self.suggestions.append(f"{class_name}: States {unreachable} are unreachable from initial state")
    
    def test_run_compiled_code(self, model_dir: str, target_lang: str) -> Tuple[bool, str, str]:
        """Execute compiled code and capture output"""
        if target_lang == "Python":
            main_file = os.path.join(model_dir, "main.py")
            if not os.path.exists(main_file):
                return False, "", "main.py not found"
            
            try:
                result = subprocess.run(
                    [sys.executable, main_file],
                    cwd=model_dir,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                success = result.returncode == 0
                return success, result.stdout, result.stderr
                
            except subprocess.TimeoutExpired:
                return False, "", "Execution timeout (10s)"
            except Exception as e:
                return False, "", str(e)
        
        elif target_lang == "Java":
            return False, "", "Java execution not implemented yet"
        
        return False, "", f"Unsupported language: {target_lang}"
    
    def analyze_execution_output(self, stdout: str, stderr: str) -> Dict:
        """Analyze execution output and provide feedback"""
        feedback = {
            'execution_success': len(stderr) == 0,
            'observations': [],
            'recommendations': []
        }
        
        if stderr:
            feedback['observations'].append(f"Errors detected: {stderr[:200]}")
            feedback['recommendations'].append("Fix runtime errors in generated code")
        
        if "Status:" in stdout:
            feedback['observations'].append("State machines initialized successfully")
        
        if "Testing state transitions" in stdout:
            feedback['observations'].append("State transitions are operational")
            feedback['recommendations'].append("Consider testing more complex transition scenarios")
        
        if stdout.count("Creating") > 3:
            feedback['observations'].append(f"Multiple classes instantiated successfully")
        
        # Check for completeness
        if "TODO" in stdout or "TODO" in stderr:
            feedback['recommendations'].append("Implementation contains TODO items - complete them for full functionality")
        
        if len(stdout.split('\n')) < 10:
            feedback['recommendations'].append("Output is minimal - consider adding more demonstration logic in main.py")
        
        return feedback
    
    def generate_report(self, analysis: Dict, execution: Dict = None) -> str:
        """Generate comprehensive analysis report"""
        lines = []
        
        lines.append("=" * 70)
        lines.append("MODEL ANALYSIS REPORT")
        lines.append("=" * 70)
        lines.append("")
        
        # Statistics
        lines.append("📊 MODEL STATISTICS")
        lines.append("-" * 70)
        stats = analysis['stats']
        lines.append(f"  Domains:              {stats['total_domains']}")
        lines.append(f"  Total Classes:        {stats['total_classes']}")
        lines.append(f"    - Active Classes:   {stats['active_classes']}")
        lines.append(f"    - Passive Classes:  {stats['passive_classes']}")
        lines.append(f"  State Machines:       {stats['classes_with_state_machines']}")
        lines.append(f"  Total States:         {stats['total_states']}")
        lines.append(f"  Total Transitions:    {stats['total_transitions']}")
        lines.append(f"  Total Actions:        {stats['total_actions']}")
        lines.append(f"  Relationships:        {stats['total_relationships']}")
        lines.append("")
        
        # Issues
        if analysis['issues']:
            lines.append("⚠️  ISSUES FOUND")
            lines.append("-" * 70)
            for i, issue in enumerate(analysis['issues'], 1):
                lines.append(f"  {i}. {issue}")
            lines.append("")
        
        # Suggestions
        if analysis['suggestions']:
            lines.append("💡 SUGGESTIONS FOR IMPROVEMENT")
            lines.append("-" * 70)
            for i, suggestion in enumerate(analysis['suggestions'], 1):
                lines.append(f"  {i}. {suggestion}")
            lines.append("")
        
        # Execution results
        if execution:
            lines.append("🚀 EXECUTION TEST RESULTS")
            lines.append("-" * 70)
            
            if execution.get('execution_success'):
                lines.append("  ✅ Code executed successfully")
            else:
                lines.append("  ❌ Code execution failed")
            
            lines.append("")
            
            if execution.get('observations'):
                lines.append("  Observations:")
                for obs in execution['observations']:
                    lines.append(f"    • {obs}")
                lines.append("")
            
            if execution.get('recommendations'):
                lines.append("  Recommendations:")
                for rec in execution['recommendations']:
                    lines.append(f"    • {rec}")
                lines.append("")
        
        # Overall assessment
        lines.append("📋 OVERALL ASSESSMENT")
        lines.append("-" * 70)
        
        score = 0
        max_score = 100
        
        # Scoring
        if stats['active_classes'] > 0:
            score += 20
        if stats['classes_with_state_machines'] > 0:
            score += 20
        if stats['total_transitions'] > 0:
            score += 15
        if stats['total_actions'] > 0:
            score += 15
        if stats['total_relationships'] > 0:
            score += 10
        if len(analysis['issues']) == 0:
            score += 10
        if execution and execution.get('execution_success'):
            score += 10
        
        lines.append(f"  Model Completeness Score: {score}/{max_score}")
        lines.append("")
        
        if score >= 80:
            lines.append("  ✅ Excellent! Your model is well-structured and comprehensive.")
        elif score >= 60:
            lines.append("  ✔️  Good model. Consider addressing suggestions for improvement.")
        elif score >= 40:
            lines.append("  ⚠️  Model needs improvement. Review issues and suggestions.")
        else:
            lines.append("  ❌ Model is incomplete. Significant work needed.")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
