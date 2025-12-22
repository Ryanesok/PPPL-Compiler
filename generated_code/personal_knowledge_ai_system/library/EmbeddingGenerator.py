from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class EmbeddingGenerator:
    """Generator untuk membuat vector embedding dari teks."""


    GeneratorID: UUID = field(default_factory=uuid4)
    ModelName: Optional[str] = None




    # Auto-generated methods
    def __str__(self):
        """String representation of EmbeddingGenerator"""
        return f"EmbeddingGenerator(GeneratorID={self.GeneratorID}, ModelName={self.ModelName})"
    def to_dict(self):
        """Convert EmbeddingGenerator to dictionary"""
        return {
            'GeneratorID': str(self.GeneratorID) if self.GeneratorID else None,
            'ModelName': self.ModelName,
        }
    def validate(self) -> bool:
        """Validate EmbeddingGenerator data"""
        # TODO: Add validation logic
        # Check required fields
        if self.GeneratorID is None:
            return False
        if self.ModelName is None:
            return False
        return True