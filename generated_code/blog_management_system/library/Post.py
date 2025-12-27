from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class PostState(Enum):
    """States for Post"""
    DRAFT = "Draft"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"


@dataclass
class Post:
    """Blog post/artikel"""


    PostID: UUID = field(default_factory=uuid4)
    AuthorID: UUID = field(default_factory=uuid4)
    Title: Optional[str] = None
    Content: Optional[str] = None
    Excerpt: Optional[str] = None
    PublishedAt: Optional[datetime] = None
    ViewCount: int = 0
    Status: 'PostState' = field(default_factory=lambda: PostState.DRAFT)

    # Relationships
    user: Optional['User'] = None  # R1 (inverse): User creates many Posts
    comments: List['Comment'] = field(default_factory=list)  # R2: Post has many Comments
    categorys: List['Category'] = field(default_factory=list)  # R3: Posts belong to many Categories


    def publish(self):
        """Handle publish event"""
        if self.Status == PostState.DRAFT:
            print(f"[LOG] Publishing post: {self.Title}")
            self.Status = PostState.PUBLISHED
            return True
        return False

    def archive(self):
        """Handle archive event"""
        if self.Status == PostState.PUBLISHED:
            print(f"[LOG] Archiving post")
            self.Status = PostState.ARCHIVED
            return True
        return False

    def handle_event(self, event_name: str) -> bool:
        """Handle any event by dispatching to appropriate method"""
        import re
        event_method = re.sub(r'[^a-zA-Z0-9_]', '_', event_name).lower()
        if hasattr(self, event_method):
            method = getattr(self, event_method)
            return method()
        return False



    # Auto-generated methods
    def __str__(self):
        """String representation of Post"""
        return f"Post(PostID={self.PostID}, AuthorID={self.AuthorID}, Title={self.Title})"
    def to_dict(self):
        """Convert Post to dictionary"""
        return {
            'PostID': str(self.PostID) if self.PostID else None,
            'AuthorID': str(self.AuthorID) if self.AuthorID else None,
            'Title': self.Title,
            'Content': self.Content,
            'Excerpt': self.Excerpt,
            'PublishedAt': self.PublishedAt.isoformat() if self.PublishedAt else None,
            'ViewCount': self.ViewCount,
            'Status': self.Status.value if hasattr(self.Status, 'value') else str(self.Status),
        }
    def validate(self) -> bool:
        """Validate Post data"""
        # TODO: Add validation logic
        # Check required fields
        if self.PostID is None:
            return False
        if self.AuthorID is None:
            return False
        if self.Title is None:
            return False
        if self.Content is None:
            return False
        if self.Excerpt is None:
            return False
        if self.PublishedAt is None:
            return False
        return True