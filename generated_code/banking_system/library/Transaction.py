from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class TransactionState(Enum):
    """States for Transaction"""
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REVERSED = "Reversed"


@dataclass
class Transaction:
    """Transaksi keuangan"""


    TransactionID: UUID = field(default_factory=uuid4)
    AccountID: UUID = field(default_factory=uuid4)
    Type: Optional[str] = None
    Amount: Optional[str] = None
    Description: Optional[str] = None
    Timestamp: Optional[datetime] = None
    Status: 'TransactionState' = field(default_factory=lambda: TransactionState.PENDING)


    def process(self):
        """Handle process event"""
        if self.Status == TransactionState.PENDING:
            self.Status = TransactionState.PROCESSING
            return True
        return False

    def complete(self):
        """Handle complete event"""
        if self.Status == TransactionState.PROCESSING:
            self.Status = TransactionState.COMPLETED
            return True
        return False

    def fail(self):
        """Handle fail event"""
        if self.Status == TransactionState.PROCESSING:
            self.Status = TransactionState.FAILED
            return True
        return False

    def reverse(self):
        """Handle reverse event"""
        if self.Status == TransactionState.COMPLETED:
            self.Status = TransactionState.REVERSED
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
        """String representation of Transaction"""
        return f"Transaction(TransactionID={self.TransactionID}, AccountID={self.AccountID}, Type={self.Type})"
    def to_dict(self):
        """Convert Transaction to dictionary"""
        return {
            'TransactionID': str(self.TransactionID) if self.TransactionID else None,
            'AccountID': str(self.AccountID) if self.AccountID else None,
            'Type': self.Type,
            'Amount': self.Amount,
            'Description': self.Description,
            'Timestamp': self.Timestamp.isoformat() if self.Timestamp else None,
            'Status': self.Status.value if hasattr(self.Status, 'value') else str(self.Status),
        }
    def validate(self) -> bool:
        """Validate Transaction data"""
        # TODO: Add validation logic
        # Check required fields
        if self.TransactionID is None:
            return False
        if self.AccountID is None:
            return False
        if self.Type is None:
            return False
        if self.Amount is None:
            return False
        if self.Description is None:
            return False
        if self.Timestamp is None:
            return False
        return True