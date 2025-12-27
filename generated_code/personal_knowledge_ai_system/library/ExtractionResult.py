from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class ExtractionResultState(Enum):
    """States for ExtractionResult"""
    PENDING = "Pending"
    EXTRACTING = "Extracting"
    TEXTEXTRACTED = "TextExtracted"
    VALIDATING = "Validating"
    VALID = "Valid"
    INVALID = "Invalid"
    METADATAENRICHED = "MetadataEnriched"
    READYFORSTORAGE = "ReadyForStorage"
    STORING = "Storing"
    STORED = "Stored"
    STORAGEFAILED = "StorageFailed"
    FAILED = "Failed"


@dataclass
class ExtractionResult:
    """Hasil dari proses ekstraksi teks."""


    ResultID: UUID = field(default_factory=uuid4)
    JobID: UUID = field(default_factory=uuid4)
    ExtractedText: Optional[str] = None
    Metadata: Optional[str] = None
    Status: 'ExtractionResultState' = field(default_factory=lambda: ExtractionResultState.PENDING)


    def startextraction(self):
        """Handle startExtraction event"""
        if self.Status == ExtractionResultState.PENDING:
            # Unknown action type: update
            print(f"[LOG] Starting extraction for result {self.ResultID}.")
            self.Status = ExtractionResultState.EXTRACTING
            return True
        return False

    def extractioncomplete(self):
        """Handle extractionComplete event"""
        if self.Status == ExtractionResultState.EXTRACTING:
            # Unknown action type: update
            # Unknown action type: update
            print(f"[LOG] Text extracted for result {self.ResultID}.")
            self.Status = ExtractionResultState.TEXTEXTRACTED
            return True
        return False

    def validatecontent(self):
        """Handle validateContent event"""
        if self.Status == ExtractionResultState.TEXTEXTRACTED:
            # Unknown action type: update
            self.Status = ExtractionResultState.VALIDATING
            return True
        return False

    def contentisvalid(self):
        """Handle contentIsValid event"""
        if self.Status == ExtractionResultState.VALIDATING:
            # Unknown action type: update
            self.Status = ExtractionResultState.VALID
            return True
        return False

    def contentisinvalid(self):
        """Handle contentIsInvalid event"""
        if self.Status == ExtractionResultState.VALIDATING:
            # Unknown action type: update
            print(f"[LOG] Content invalid for result {self.ResultID}: {reason}")
            self.Status = ExtractionResultState.INVALID
            return True
        return False

    def markasfailed(self):
        """Handle markAsFailed event"""
        if self.Status == ExtractionResultState.INVALID:
            # Unknown action type: update
            self.Status = ExtractionResultState.FAILED
            return True
        return False

    def addmetadata(self):
        """Handle addMetadata event"""
        if self.Status == ExtractionResultState.VALID:
            # Unknown action type: update
            # Unknown action type: update
            self.Status = ExtractionResultState.METADATAENRICHED
            return True
        return False

    def prepareforstorage(self):
        """Handle prepareForStorage event"""
        if self.Status == ExtractionResultState.METADATAENRICHED:
            # Unknown action type: update
            self.Status = ExtractionResultState.READYFORSTORAGE
            return True
        return False

    def sendtostorage(self):
        """Handle sendToStorage event"""
        if self.Status == ExtractionResultState.READYFORSTORAGE:
            # Unknown action type: update
            StorageService("this")
            self.Status = ExtractionResultState.STORING
            return True
        return False

    def storagesuccess(self):
        """Handle storageSuccess event"""
        if self.Status == ExtractionResultState.STORING:
            # Unknown action type: update
            print(f"[LOG] Result {self.ResultID} stored successfully.")
            self.Status = ExtractionResultState.STORED
            return True
        return False

    def storageerror(self):
        """Handle storageError event"""
        if self.Status == ExtractionResultState.STORING:
            # Unknown action type: update
            print(f"[LOG] Storage failed for result {self.ResultID}: {errorMessage}")
            self.Status = ExtractionResultState.STORAGEFAILED
            return True
        return False

    def retrystorage(self):
        """Handle retryStorage event"""
        if self.Status == ExtractionResultState.STORAGEFAILED:
            # Unknown action type: update
            print(f"[LOG] Retrying storage for result {self.ResultID}.")
            self.Status = ExtractionResultState.STORING
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
        """String representation of ExtractionResult"""
        return f"ExtractionResult(ResultID={self.ResultID}, JobID={self.JobID}, ExtractedText={self.ExtractedText})"
    def to_dict(self):
        """Convert ExtractionResult to dictionary"""
        return {
            'ResultID': str(self.ResultID) if self.ResultID else None,
            'JobID': str(self.JobID) if self.JobID else None,
            'ExtractedText': self.ExtractedText,
            'Metadata': self.Metadata,
            'Status': self.Status.value if hasattr(self.Status, 'value') else str(self.Status),
        }
    def validate(self) -> bool:
        """Validate ExtractionResult data"""
        # TODO: Add validation logic
        # Check required fields
        if self.ResultID is None:
            return False
        if self.JobID is None:
            return False
        if self.ExtractedText is None:
            return False
        if self.Metadata is None:
            return False
        return True