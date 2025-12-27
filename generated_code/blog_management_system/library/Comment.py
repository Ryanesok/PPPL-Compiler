from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class Comment:
    """Komentar pada post"""


    CommentID: UUID = field(default_factory=uuid4)
    PostID: UUID = field(default_factory=uuid4)
    UserID: UUID = field(default_factory=uuid4)
    Content: Optional[str] = None
    CreatedAt: Optional[datetime] = None
    IsApproved: bool = False

    # Relationships
    post: Optional['Post'] = None  # R2 (inverse): Post has many Comments




    # Auto-generated methods
    def __str__(self):
        """String representation of Comment"""
        return f"Comment(CommentID={self.CommentID}, PostID={self.PostID}, UserID={self.UserID})"
    def to_dict(self):
        """Convert Comment to dictionary"""
        return {
            'CommentID': str(self.CommentID) if self.CommentID else None,
            'PostID': str(self.PostID) if self.PostID else None,
            'UserID': str(self.UserID) if self.UserID else None,
            'Content': self.Content,
            'CreatedAt': self.CreatedAt.isoformat() if self.CreatedAt else None,
            'IsApproved': self.IsApproved,
        }
    def validate(self) -> bool:
        """Validate Comment data"""
        # TODO: Add validation logic
        # Check required fields
        if self.CommentID is None:
            return False
        if self.PostID is None:
            return False
        if self.UserID is None:
            return False
        if self.Content is None:
            return False
        if self.CreatedAt is None:
            return False
        return True