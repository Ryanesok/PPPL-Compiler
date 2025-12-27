from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class User:
    """User/Author dalam sistem blog"""


    UserID: UUID = field(default_factory=uuid4)
    Username: Optional[str] = None
    Email: Optional[str] = None
    FullName: Optional[str] = None
    Bio: Optional[str] = None
    ProfileImage: Optional[str] = None
    JoinedDate: Optional[datetime] = None

    # Relationships
    posts: List['Post'] = field(default_factory=list)  # R1: User creates many Posts




    # Auto-generated methods
    def __str__(self):
        """String representation of User"""
        return f"User(UserID={self.UserID}, Username={self.Username}, Email={self.Email})"
    def to_dict(self):
        """Convert User to dictionary"""
        return {
            'UserID': str(self.UserID) if self.UserID else None,
            'Username': self.Username,
            'Email': self.Email,
            'FullName': self.FullName,
            'Bio': self.Bio,
            'ProfileImage': self.ProfileImage,
            'JoinedDate': self.JoinedDate.isoformat() if self.JoinedDate else None,
        }
    def validate(self) -> bool:
        """Validate User data"""
        # TODO: Add validation logic
        # Check required fields
        if self.UserID is None:
            return False
        if self.Username is None:
            return False
        if self.Email is None:
            return False
        if self.FullName is None:
            return False
        if self.Bio is None:
            return False
        if self.ProfileImage is None:
            return False
        if self.JoinedDate is None:
            return False
        return True