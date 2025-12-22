from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class ExtractionWorker:
    """Worker yang memproses job ekstraksi."""


    WorkerID: UUID = field(default_factory=uuid4)




    # Auto-generated methods
    def __str__(self):
        """String representation of ExtractionWorker"""
        return f"ExtractionWorker(WorkerID={self.WorkerID})"
    def to_dict(self):
        """Convert ExtractionWorker to dictionary"""
        return {
            'WorkerID': str(self.WorkerID) if self.WorkerID else None,
        }
    def validate(self) -> bool:
        """Validate ExtractionWorker data"""
        # TODO: Add validation logic
        # Check required fields
        if self.WorkerID is None:
            return False
        return True