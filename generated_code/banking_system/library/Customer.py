from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class Customer:
    """Nasabah bank"""


    CustomerID: UUID = field(default_factory=uuid4)
    FullName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    DateOfBirth: Optional[str] = None
    Address: Optional[str] = None
    KYCVerified: bool = False

    # Relationships
    accounts: List['Account'] = field(default_factory=list)  # R1: Customer owns many Accounts




    # Auto-generated methods
    def __str__(self):
        """String representation of Customer"""
        return f"Customer(CustomerID={self.CustomerID}, FullName={self.FullName}, Email={self.Email})"
    def to_dict(self):
        """Convert Customer to dictionary"""
        return {
            'CustomerID': str(self.CustomerID) if self.CustomerID else None,
            'FullName': self.FullName,
            'Email': self.Email,
            'Phone': self.Phone,
            'DateOfBirth': self.DateOfBirth,
            'Address': self.Address,
            'KYCVerified': self.KYCVerified,
        }
    def validate(self) -> bool:
        """Validate Customer data"""
        # TODO: Add validation logic
        # Check required fields
        if self.CustomerID is None:
            return False
        if self.FullName is None:
            return False
        if self.Email is None:
            return False
        if self.Phone is None:
            return False
        if self.DateOfBirth is None:
            return False
        if self.Address is None:
            return False
        return True