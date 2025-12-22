from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class MessageState(Enum):
    """States for Message"""
    DRAFT = "Draft"
    SENDING = "Sending"
    SENT = "Sent"
    DELIVERED = "Delivered"
    READ = "Read"
    FAILED = "Failed"


@dataclass
class Message:
    """Merepresentasikan pesan dalam chat antara user dan AI."""


    MessageID: UUID = field(default_factory=uuid4)
    Content: Optional[str] = None
    Sender: Optional[str] = None
    Timestamp: Optional[datetime] = None
    Type: Optional[str] = None
    Status: 'MessageState' = field(default_factory=lambda: MessageState.DRAFT)


    def userclickssend(self):
        """Handle userClicksSend event"""
        if self.Status == MessageState.DRAFT:
            self.Status = MessageState.SENDING
            return True
        return False

    def apicallsuccess(self):
        """Handle apiCallSuccess event"""
        if self.Status == MessageState.SENDING:
            self.Status = MessageState.SENT
            return True
        return False

    def networkerror(self):
        """Handle networkError event"""
        if self.Status == MessageState.SENDING:
            self.Status = MessageState.FAILED
            return True
        return False

    def retry(self):
        """Handle retry event"""
        if self.Status == MessageState.FAILED:
            self.Status = MessageState.SENDING
            return True
        return False

    def serverconfirms(self):
        """Handle serverConfirms event"""
        if self.Status == MessageState.SENT:
            self.Status = MessageState.DELIVERED
            return True
        return False

    def userviews(self):
        """Handle userViews event"""
        if self.Status == MessageState.DELIVERED:
            self.Status = MessageState.READ
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
        """String representation of Message"""
        return f"Message(MessageID={self.MessageID}, Content={self.Content}, Sender={self.Sender})"
    def to_dict(self):
        """Convert Message to dictionary"""
        return {
            'MessageID': str(self.MessageID) if self.MessageID else None,
            'Content': self.Content,
            'Sender': self.Sender,
            'Timestamp': self.Timestamp.isoformat() if self.Timestamp else None,
            'Type': self.Type,
            'Status': self.Status.value if hasattr(self.Status, 'value') else str(self.Status),
        }
    def validate(self) -> bool:
        """Validate Message data"""
        # TODO: Add validation logic
        # Check required fields
        if self.MessageID is None:
            return False
        if self.Content is None:
            return False
        if self.Sender is None:
            return False
        if self.Timestamp is None:
            return False
        if self.Type is None:
            return False
        return True