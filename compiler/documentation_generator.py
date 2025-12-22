from typing import Dict, List
from datetime import datetime

class DocumentationGenerator:
    """Auto-generate documentation for compiled models"""
    
    def __init__(self):
        self.doc_content = []
        
    def generate_documentation(self, parser, output_dir: str, model_name: str) -> str:
        """Generate comprehensive documentation"""
        model = parser.model
        domains = parser.get_domains()
        classes = parser.get_classes()
        relationships = parser.get_relationships()
        
        doc = []
        
        # Title
        system_name = model.get('system_name', 'System')
        version = model.get('version', '1.0.0')
        
        doc.append(f"# {system_name}")
        doc.append(f"**Version**: {version}")
        doc.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.append("")
        doc.append("---")
        doc.append("")
        
        # System Description
        if 'description' in model:
            doc.append("## System Description")
            doc.append("")
            doc.append(model['description'])
            doc.append("")
        
        # Architecture Overview
        doc.append("## Architecture Overview")
        doc.append("")
        doc.append(f"- **Total Domains**: {len(domains)}")
        doc.append(f"- **Total Classes**: {len(classes)}")
        doc.append(f"- **Total Relationships**: {len(relationships)}")
        doc.append("")
        
        # Domains
        doc.append("## Domains")
        doc.append("")
        for domain in domains:
            domain_name = domain.get('name', 'Unknown')
            domain_desc = domain.get('description', 'No description')
            doc.append(f"### {domain_name}")
            doc.append(f"**Key Letter**: {domain.get('key_letter', 'N/A')}")
            doc.append("")
            doc.append(domain_desc)
            doc.append("")
            
            # List classes in this domain
            domain_classes = [c for ck, c in classes.items() if c['domain'] == domain_name]
            if domain_classes:
                doc.append(f"**Classes in {domain_name}**:")
                for cls_info in domain_classes:
                    cls = cls_info['class']
                    entity_type = cls.get('entity_type', 'class')
                    icon = "🔄" if entity_type == "class" else "📦"
                    doc.append(f"- {icon} **{cls['name']}**: {cls.get('description', 'No description')[:80]}")
                doc.append("")
        
        # Classes Detail
        doc.append("---")
        doc.append("")
        doc.append("## Class Reference")
        doc.append("")
        
        for class_key, class_info in classes.items():
            cls = class_info['class']
            doc.extend(self._generate_class_documentation(cls))
        
        # Relationships
        doc.append("---")
        doc.append("")
        doc.append("## Relationships")
        doc.append("")
        
        for rel_id, rel_info in relationships.items():
            rel = rel_info['relationship']
            doc.extend(self._generate_relationship_documentation(rel))
        
        # State Machines
        doc.append("---")
        doc.append("")
        doc.append("## State Machines")
        doc.append("")
        
        for class_key, class_info in classes.items():
            cls = class_info['class']
            if 'state_machine' in cls:
                doc.extend(self._generate_state_machine_documentation(cls['name'], cls['state_machine']))
        
        # API Quick Reference
        doc.append("---")
        doc.append("")
        doc.append("## API Quick Reference")
        doc.append("")
        
        doc.append("### Active Classes (with State Machines)")
        doc.append("")
        doc.append("| Class | Initial State | Available Events |")
        doc.append("|-------|---------------|------------------|")
        
        for class_key, class_info in classes.items():
            cls = class_info['class']
            if cls.get('entity_type') == 'class' and 'state_machine' in cls:
                sm = cls['state_machine']
                initial = sm.get('initial_state', 'N/A')
                
                # Get unique events
                events = list(set([t.get('event', '') for t in sm.get('transitions', []) if t.get('event')]))
                events_str = ', '.join([f"`{e}`" for e in events[:3]])
                if len(events) > 3:
                    events_str += f" (+{len(events)-3} more)"
                
                doc.append(f"| **{cls['name']}** | {initial} | {events_str} |")
        
        doc.append("")
        
        # Usage Examples
        doc.append("---")
        doc.append("")
        doc.append("## Usage Examples")
        doc.append("")
        doc.append("### Basic Usage")
        doc.append("")
        doc.append("```python")
        doc.append("from library import *")
        doc.append("")
        
        # Example for first active class
        for class_key, class_info in classes.items():
            cls = class_info['class']
            if cls.get('entity_type') == 'class':
                class_name = cls['name']
                doc.append(f"# Create {class_name} instance")
                doc.append(f"obj = {class_name}()")
                doc.append(f"print(obj.Status)")
                
                if 'state_machine' in cls:
                    sm = cls['state_machine']
                    transitions = sm.get('transitions', [])
                    if transitions:
                        event = transitions[0].get('event', '')
                        if event:
                            method_name = event.lower().replace(' ', '_')
                            doc.append("")
                            doc.append(f"# Trigger event: {event}")
                            doc.append(f"obj.{method_name}()")
                            doc.append(f"print(obj.Status)")
                
                doc.append("")
                doc.append("# Validate and serialize")
                doc.append("if obj.validate():")
                doc.append("    data = obj.to_dict()")
                doc.append("    print(data)")
                doc.append("```")
                break
        
        doc.append("")
        
        return "\n".join(doc)
    
    def _generate_class_documentation(self, cls: Dict) -> List[str]:
        """Generate documentation for a single class"""
        doc = []
        
        class_name = cls['name']
        description = cls.get('description', 'No description')
        entity_type = cls.get('entity_type', 'class')
        
        doc.append(f"### {class_name}")
        doc.append("")
        doc.append(f"**Type**: {entity_type}")
        doc.append("")
        doc.append(description)
        doc.append("")
        
        # Attributes
        attributes = cls.get('attributes', [])
        if attributes:
            doc.append("**Attributes**:")
            doc.append("")
            doc.append("| Name | Type | Description |")
            doc.append("|------|------|-------------|")
            
            for attr in attributes:
                name = attr['name']
                dtype = attr.get('data_type', 'string')
                desc = attr.get('description', '-')
                doc.append(f"| `{name}` | {dtype} | {desc} |")
            
            doc.append("")
        
        # Methods (if has state machine)
        if 'state_machine' in cls:
            sm = cls['state_machine']
            transitions = sm.get('transitions', [])
            
            if transitions:
                doc.append("**Methods**:")
                doc.append("")
                
                # Get unique events
                events = {}
                for trans in transitions:
                    event = trans.get('event', '')
                    if event and event not in events:
                        from_state = trans.get('from_state', '')
                        to_state = trans.get('to_state', '')
                        events[event] = (from_state, to_state)
                
                for event, (from_st, to_st) in events.items():
                    method_name = event.lower().replace(' ', '_')
                    doc.append(f"- `{method_name}()`: Transition from *{from_st}* to *{to_st}*")
                
                doc.append("")
        
        # Auto-generated methods
        doc.append("**Auto-generated Methods**:")
        doc.append("")
        doc.append("- `__str__()`: String representation")
        doc.append("- `to_dict()`: Serialize to dictionary")
        doc.append("- `validate()`: Validate instance data")
        doc.append("")
        
        return doc
    
    def _generate_relationship_documentation(self, rel: Dict) -> List[str]:
        """Generate documentation for a relationship"""
        doc = []
        
        rel_id = rel.get('relationship_id', 'Unknown')
        description = rel.get('description', 'No description')
        rel_type = rel.get('type', 'association')
        
        from_class = rel.get('from', {})
        to_class = rel.get('to', {})
        
        from_name = from_class.get('class', 'Unknown')
        to_name = to_class.get('class', 'Unknown')
        from_mult = from_class.get('multiplicity', '1')
        to_mult = to_class.get('multiplicity', '1')
        
        doc.append(f"### {rel_id}: {from_name} ↔ {to_name}")
        doc.append("")
        doc.append(f"**Type**: {rel_type}")
        doc.append("")
        doc.append(description)
        doc.append("")
        doc.append(f"- **{from_name}** [{from_mult}] {from_class.get('role', '')} ← **{to_name}** [{to_mult}] {to_class.get('role', '')}")
        doc.append("")
        
        return doc
    
    def _generate_state_machine_documentation(self, class_name: str, sm: Dict) -> List[str]:
        """Generate state machine documentation"""
        doc = []
        
        doc.append(f"### {class_name} State Machine")
        doc.append("")
        doc.append(f"**Initial State**: {sm.get('initial_state', 'N/A')}")
        doc.append("")
        
        # States
        states = sm.get('states', [])
        doc.append("**States**:")
        doc.append("")
        for state in states:
            state_name = state['name']
            state_desc = state.get('description', 'No description')
            doc.append(f"- **{state_name}**: {state_desc}")
        
        doc.append("")
        
        # Transitions
        transitions = sm.get('transitions', [])
        if transitions:
            doc.append("**State Transitions**:")
            doc.append("")
            doc.append("```")
            for trans in transitions:
                from_st = trans.get('from_state', '')
                to_st = trans.get('to_state', '')
                event = trans.get('event', '')
                doc.append(f"{from_st} --[{event}]--> {to_st}")
            doc.append("```")
            doc.append("")
        
        return doc
