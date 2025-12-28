import json
from typing import Dict, List, Any

class ModelParser:
    """Parse PPPL Model JSON files"""
    
    def __init__(self):
        self.model = None
        self.domains = []
        self.classes = {}
        self.relationships = {}
    
    def reset(self):
        """Reset parser state for fresh compilation"""
        self.model = None
        self.domains = []
        self.classes = {}
        self.relationships = {}
        
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Load and parse JSON model file"""
        # Reset state before parsing new file
        self.reset()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            self.model = json.load(f)
        
        self._extract_domains()
        self._extract_classes()
        self._extract_relationships()
        
        return self.model
    
    def _extract_domains(self):
        """Extract all domains from model"""
        if 'domains' in self.model:
            self.domains = self.model['domains']
    
    def _extract_classes(self):
        """Extract all classes from domains"""
        for domain in self.domains:
            domain_key = domain.get('key_letter', '')
            if 'classes' in domain:
                for cls in domain['classes']:
                    class_key = cls.get('key_letter', '')
                    full_key = f"{domain_key}.{class_key}"
                    self.classes[full_key] = {
                        'domain': domain['name'],
                        'class': cls
                    }
    
    def _extract_relationships(self):
        """Extract all relationships from domains"""
        for domain in self.domains:
            domain_key = domain.get('key_letter', '')
            if 'relationships' in domain:
                for rel in domain['relationships']:
                    # Support both old (relationship_id) and new (name) formats
                    rel_id = rel.get('name', rel.get('relationship_id', ''))
                    if rel_id:  # Only add if ID exists
                        self.relationships[rel_id] = {
                            'domain': domain['name'],
                            'relationship': rel
                        }
    
    def get_domains(self) -> List[Dict]:
        return self.domains
    
    def get_classes(self) -> Dict:
        return self.classes
    
    def get_relationships(self) -> Dict:
        return self.relationships
    
    def get_relationships_for_class(self, class_name: str, domain_name: str = None) -> List[Dict]:
        """Get all relationships involving a specific class"""
        result = []
        
        for domain in self.domains:
            # Filter by domain if specified
            if domain_name and domain.get('name') != domain_name:
                continue
            
            if 'relationships' in domain:
                for rel in domain['relationships']:
                    from_class = rel.get('from_class', '')
                    to_class = rel.get('to_class', '')
                    
                    # Include if this class is involved in the relationship
                    if from_class == class_name or to_class == class_name:
                        result.append(rel)
        
        return result
    
    def validate(self) -> tuple[bool, List[str]]:
        """Validate model structure"""
        errors = []
        
        if not self.model:
            errors.append("Model not loaded")
            return False, errors
        
        if 'domains' not in self.model:
            errors.append("No domains found in model")
        
        for domain in self.domains:
            if 'name' not in domain:
                errors.append(f"Domain missing name")
            if 'key_letter' not in domain:
                errors.append(f"Domain {domain.get('name', 'Unknown')} missing key_letter")
            
            if 'classes' in domain:
                for cls in domain['classes']:
                    if 'name' not in cls:
                        errors.append(f"Class in domain {domain.get('name')} missing name")
                    if 'key_letter' not in cls:
                        errors.append(f"Class {cls.get('name', 'Unknown')} missing key_letter")
        
        return len(errors) == 0, errors
