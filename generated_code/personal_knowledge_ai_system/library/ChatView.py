from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class ChatView:
    """Komponen UI utama untuk menampilkan chat."""


    ViewID: UUID = field(default_factory=uuid4)
    UserID: UUID = field(default_factory=uuid4)




    # Auto-generated methods
    def __str__(self):
        """String representation of ChatView"""
        return f"ChatView(ViewID={self.ViewID}, UserID={self.UserID})"
    def to_dict(self):
        """Convert ChatView to dictionary"""
        return {
            'ViewID': str(self.ViewID) if self.ViewID else None,
            'UserID': str(self.UserID) if self.UserID else None,
        }
    def validate(self) -> bool:
        """Validate ChatView data"""
        # TODO: Add validation logic
        # Check required fields
        if self.ViewID is None:
            return False
        if self.UserID is None:
            return False
        return True