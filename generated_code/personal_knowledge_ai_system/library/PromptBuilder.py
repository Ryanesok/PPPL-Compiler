from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class PromptBuilder:
    """Builder untuk menyusun prompt RAG."""


    BuilderID: UUID = field(default_factory=uuid4)




    # Auto-generated methods
    def __str__(self):
        """String representation of PromptBuilder"""
        return f"PromptBuilder(BuilderID={self.BuilderID})"
    def to_dict(self):
        """Convert PromptBuilder to dictionary"""
        return {
            'BuilderID': str(self.BuilderID) if self.BuilderID else None,
        }
    def validate(self) -> bool:
        """Validate PromptBuilder data"""
        # TODO: Add validation logic
        # Check required fields
        if self.BuilderID is None:
            return False
        return True