from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class Category:
    """Kategori untuk post"""


    CategoryID: UUID = field(default_factory=uuid4)
    Name: Optional[str] = None
    Description: Optional[str] = None
    Slug: Optional[str] = None

    # Relationships
    posts: List['Post'] = field(default_factory=list)  # R3 (inverse): Posts belong to many Categories




    # Auto-generated methods
    def __str__(self):
        """String representation of Category"""
        return f"Category(CategoryID={self.CategoryID}, Name={self.Name}, Description={self.Description})"
    def to_dict(self):
        """Convert Category to dictionary"""
        return {
            'CategoryID': str(self.CategoryID) if self.CategoryID else None,
            'Name': self.Name,
            'Description': self.Description,
            'Slug': self.Slug,
        }
    def validate(self) -> bool:
        """Validate Category data"""
        # TODO: Add validation logic
        # Check required fields
        if self.CategoryID is None:
            return False
        if self.Name is None:
            return False
        if self.Description is None:
            return False
        if self.Slug is None:
            return False
        return True