from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class LLMClient:
    """Client untuk berkomunikasi dengan Large Language Model."""


    ClientID: UUID = field(default_factory=uuid4)
    ModelName: Optional[str] = None




    # Auto-generated methods
    def __str__(self):
        """String representation of LLMClient"""
        return f"LLMClient(ClientID={self.ClientID}, ModelName={self.ModelName})"
    def to_dict(self):
        """Convert LLMClient to dictionary"""
        return {
            'ClientID': str(self.ClientID) if self.ClientID else None,
            'ModelName': self.ModelName,
        }
    def validate(self) -> bool:
        """Validate LLMClient data"""
        # TODO: Add validation logic
        # Check required fields
        if self.ClientID is None:
            return False
        if self.ModelName is None:
            return False
        return True