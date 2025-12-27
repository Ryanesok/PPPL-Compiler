from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class IngestionJobState(Enum):
    """States for IngestionJob"""
    CREATED = "Created"
    QUEUED = "Queued"
    PROCESSING = "Processing"
    VALIDATING = "Validating"
    EXTRACTING = "Extracting"
    COMPLETED = "Completed"
    FAILED = "Failed"
    ABANDONED = "Abandoned"


@dataclass
class IngestionJob:
    """Merepresentasikan job untuk memproses data yang diingest."""


    JobID: UUID = field(default_factory=uuid4)
    DataType: Optional[str] = None
    SourceUri: Optional[str] = None
    UserID: UUID = field(default_factory=uuid4)
    RetryCount: Optional[int] = None
    Status: 'IngestionJobState' = field(default_factory=lambda: IngestionJobState.CREATED)


    def addtoqueue(self):
        """Handle addToQueue event"""
        if self.Status == IngestionJobState.CREATED:
            # Unknown action type: update
            MessageQueue("this")
            print(f"[LOG] Job {self.JobID} added to queue.")
            self.Status = IngestionJobState.QUEUED
            return True
        return False

    def workerpicksup(self):
        """Handle workerPicksUp event"""
        if self.Status == IngestionJobState.QUEUED:
            # Unknown action type: update
            print(f"[LOG] Job {self.JobID} picked up by worker {workerID}.")
            self.Status = IngestionJobState.PROCESSING
            return True
        return False

    def checkintegrity(self):
        """Handle checkIntegrity event"""
        if self.Status == IngestionJobState.PROCESSING:
            # Unknown action type: update
            print(f"[LOG] Validating job {self.JobID}.")
            self.Status = IngestionJobState.VALIDATING
            return True
        return False

    def validationpassed(self):
        """Handle validationPassed event"""
        if self.Status == IngestionJobState.VALIDATING:
            # Unknown action type: update
            ExtractionWorker("this")
            self.Status = IngestionJobState.EXTRACTING
            return True
        return False

    def validationerror(self):
        """Handle validationError event"""
        if self.Status == IngestionJobState.VALIDATING:
            # Unknown action type: update
            print(f"[LOG] Job {self.JobID} validation failed: {errorDetails}")
            self.Status = IngestionJobState.FAILED
            return True
        return False

    def extractionsuccess(self):
        """Handle extractionSuccess event"""
        if self.Status == IngestionJobState.EXTRACTING:
            # Unknown action type: update
            NotificationService("this.UserID", "this.JobID")
            print(f"[LOG] Job {self.JobID} completed successfully.")
            self.Status = IngestionJobState.COMPLETED
            return True
        return False

    def extractionerror(self):
        """Handle extractionError event"""
        if self.Status == IngestionJobState.EXTRACTING:
            # Unknown action type: update
            print(f"[LOG] Job {self.JobID} extraction failed: {errorMessage}")
            self.Status = IngestionJobState.FAILED
            return True
        return False

    def retryjob(self):
        """Handle retryJob event"""
        if self.Status == IngestionJobState.FAILED:
            # Unknown action type: increment
            # Unknown action type: condition
            self.Status = IngestionJobState.QUEUED
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
        """String representation of IngestionJob"""
        return f"IngestionJob(JobID={self.JobID}, DataType={self.DataType}, SourceUri={self.SourceUri})"
    def to_dict(self):
        """Convert IngestionJob to dictionary"""
        return {
            'JobID': str(self.JobID) if self.JobID else None,
            'DataType': self.DataType,
            'SourceUri': self.SourceUri,
            'UserID': str(self.UserID) if self.UserID else None,
            'RetryCount': self.RetryCount,
            'Status': self.Status.value if hasattr(self.Status, 'value') else str(self.Status),
        }
    def validate(self) -> bool:
        """Validate IngestionJob data"""
        # TODO: Add validation logic
        # Check required fields
        if self.JobID is None:
            return False
        if self.DataType is None:
            return False
        if self.SourceUri is None:
            return False
        if self.UserID is None:
            return False
        if self.RetryCount is None:
            return False
        return True