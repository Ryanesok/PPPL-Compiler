from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class ApiClient:
    """Menangani komunikasi HTTP ke backend."""


    ClientID: UUID = field(default_factory=uuid4)
    BaseUrl: Optional[str] = None




    # Auto-generated methods
    def __str__(self):
        """String representation of ApiClient"""
        return f"ApiClient(ClientID={self.ClientID}, BaseUrl={self.BaseUrl})"
    def to_dict(self):
        """Convert ApiClient to dictionary"""
        return {
            'ClientID': str(self.ClientID) if self.ClientID else None,
            'BaseUrl': self.BaseUrl,
        }
    def validate(self) -> bool:
        """Validate ApiClient data"""
        # TODO: Add validation logic
        # Check required fields
        if self.ClientID is None:
            return False
        if self.BaseUrl is None:
            return False
        return True