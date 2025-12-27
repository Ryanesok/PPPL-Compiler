from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class AccountState(Enum):
    """States for Account"""
    PENDING = "Pending"
    ACTIVE = "Active"
    FROZEN = "Frozen"
    CLOSED = "Closed"


@dataclass
class Account:
    """Rekening bank"""


    AccountID: UUID = field(default_factory=uuid4)
    AccountNumber: Optional[str] = None
    AccountType: Optional[str] = None
    Balance: str = "0.0"
    Currency: str = "USD"
    CreatedDate: Optional[datetime] = None
    Status: 'AccountState' = field(default_factory=lambda: AccountState.PENDING)

    # Relationships
    customer: Optional['Customer'] = None  # R1 (inverse): Customer owns many Accounts
    transactions: List['Transaction'] = field(default_factory=list)  # R2: Account has many Transactions


    def approve(self):
        """Handle approve event"""
        if self.Status == AccountState.PENDING:
            print(f"[LOG] Approving account {self.AccountNumber}")
            self.Status = AccountState.ACTIVE
            # On entry Active
            print(f"[LOG] Account activated")
            return True
        return False

    def freeze(self):
        """Handle freeze event"""
        if self.Status == AccountState.ACTIVE:
            print(f"[LOG] Freezing account due to: {reason}")
            self.Status = AccountState.FROZEN
            # On entry Frozen
            print(f"[LOG] Account frozen - no transactions allowed")
            return True
        return False

    def unfreeze(self):
        """Handle unfreeze event"""
        if self.Status == AccountState.FROZEN:
            print(f"[LOG] Unfreezing account")
            self.Status = AccountState.ACTIVE
            # On entry Active
            print(f"[LOG] Account activated")
            return True
        return False

    def close(self):
        """Handle close event"""
        if self.Status == AccountState.ACTIVE:
            self = "0.0"
            print(f"[LOG] Closing account - balance cleared")
            self.Status = AccountState.CLOSED
            # On entry Closed
            print(f"[LOG] Account closed permanently")
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
        """String representation of Account"""
        return f"Account(AccountID={self.AccountID}, AccountNumber={self.AccountNumber}, AccountType={self.AccountType})"
    def to_dict(self):
        """Convert Account to dictionary"""
        return {
            'AccountID': str(self.AccountID) if self.AccountID else None,
            'AccountNumber': self.AccountNumber,
            'AccountType': self.AccountType,
            'Balance': self.Balance,
            'Currency': self.Currency,
            'CreatedDate': self.CreatedDate.isoformat() if self.CreatedDate else None,
            'Status': self.Status.value if hasattr(self.Status, 'value') else str(self.Status),
        }
    def validate(self) -> bool:
        """Validate Account data"""
        # TODO: Add validation logic
        # Check required fields
        if self.AccountID is None:
            return False
        if self.AccountNumber is None:
            return False
        if self.AccountType is None:
            return False
        if self.CreatedDate is None:
            return False
        return True