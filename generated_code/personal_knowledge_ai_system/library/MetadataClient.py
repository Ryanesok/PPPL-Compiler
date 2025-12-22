from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class MetadataClient:
    """Client untuk menyimpan metadata dokumen."""


    ClientID: UUID = field(default_factory=uuid4)
    DatabaseUrl: Optional[str] = None




    # Auto-generated methods
    def __str__(self):
        """String representation of MetadataClient"""
        return f"MetadataClient(ClientID={self.ClientID}, DatabaseUrl={self.DatabaseUrl})"
    def to_dict(self):
        """Convert MetadataClient to dictionary"""
        return {
            'ClientID': str(self.ClientID) if self.ClientID else None,
            'DatabaseUrl': self.DatabaseUrl,
        }
    def validate(self) -> bool:
        """Validate MetadataClient data"""
        # TODO: Add validation logic
        # Check required fields
        if self.ClientID is None:
            return False
        if self.DatabaseUrl is None:
            return False
        return True