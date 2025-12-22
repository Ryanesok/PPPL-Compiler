from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class AnswerState(Enum):
    """States for Answer"""
    RECEIVED = "Received"
    RETRIEVINGCONTEXT = "RetrievingContext"
    CONTEXTFOUND = "ContextFound"
    NOCONTEXT = "NoContext"
    BUILDINGPROMPT = "BuildingPrompt"
    GENERATINGANSWER = "GeneratingAnswer"
    STREAMING = "Streaming"
    PARTIALANSWER = "PartialAnswer"
    COMPLETE = "Complete"
    FORMATTINGRESPONSE = "FormattingResponse"
    READYTOSEND = "ReadyToSend"
    SENT = "Sent"
    FAILED = "Failed"
    ERRORRESPONSE = "ErrorResponse"


@dataclass
class Answer:
    """Jawaban yang dihasilkan oleh AI untuk query pengguna."""


    AnswerID: UUID = field(default_factory=uuid4)
    QueryText: Optional[str] = None
    AnswerText: Optional[str] = None
    Sources: Optional[str] = None
    Confidence: Optional[float] = None
    Status: 'AnswerState' = field(default_factory=lambda: AnswerState.RECEIVED)


    def searchrelevantdocs(self):
        """Handle searchRelevantDocs event"""
        if self.Status == AnswerState.RECEIVED:
            self.Status = AnswerState.RETRIEVINGCONTEXT
            return True
        return False

    def docsretrieved(self):
        """Handle docsRetrieved event"""
        if self.Status == AnswerState.RETRIEVINGCONTEXT:
            self.Status = AnswerState.CONTEXTFOUND
            return True
        return False

    def nodocsfound(self):
        """Handle noDocsFound event"""
        if self.Status == AnswerState.RETRIEVINGCONTEXT:
            self.Status = AnswerState.NOCONTEXT
            return True
        return False

    def prepareprompt(self):
        """Handle preparePrompt event"""
        if self.Status == AnswerState.CONTEXTFOUND:
            self.Status = AnswerState.BUILDINGPROMPT
            return True
        return False

    def usefallbackprompt(self):
        """Handle useFallbackPrompt event"""
        if self.Status == AnswerState.NOCONTEXT:
            self.Status = AnswerState.BUILDINGPROMPT
            return True
        return False

    def sendtollm(self):
        """Handle sendToLLM event"""
        if self.Status == AnswerState.BUILDINGPROMPT:
            self.Status = AnswerState.GENERATINGANSWER
            return True
        return False

    def startstreaming(self):
        """Handle startStreaming event"""
        if self.Status == AnswerState.GENERATINGANSWER:
            self.Status = AnswerState.STREAMING
            return True
        return False

    def chunksreceived(self):
        """Handle chunksReceived event"""
        if self.Status == AnswerState.STREAMING:
            self.Status = AnswerState.PARTIALANSWER
            return True
        return False

    def continuestreaming(self):
        """Handle continueStreaming event"""
        if self.Status == AnswerState.PARTIALANSWER:
            self.Status = AnswerState.STREAMING
            return True
        return False

    def streamfinished(self):
        """Handle streamFinished event"""
        if self.Status == AnswerState.PARTIALANSWER:
            self.Status = AnswerState.COMPLETE
            return True
        return False

    def llmerror(self):
        """Handle llmError event"""
        if self.Status == AnswerState.GENERATINGANSWER:
            self.Status = AnswerState.FAILED
            return True
        return False

    def retrywithfallback(self):
        """Handle retryWithFallback event"""
        if self.Status == AnswerState.FAILED:
            self.Status = AnswerState.GENERATINGANSWER
            return True
        return False

    def maxretriesexceeded(self):
        """Handle maxRetriesExceeded event"""
        if self.Status == AnswerState.FAILED:
            self.Status = AnswerState.ERRORRESPONSE
            return True
        return False

    def formatanswer(self):
        """Handle formatAnswer event"""
        if self.Status == AnswerState.COMPLETE:
            self.Status = AnswerState.FORMATTINGRESPONSE
            return True
        return False

    def formattingcomplete(self):
        """Handle formattingComplete event"""
        if self.Status == AnswerState.FORMATTINGRESPONSE:
            self.Status = AnswerState.READYTOSEND
            return True
        return False

    def delivertouser(self):
        """Handle deliverToUser event"""
        if self.Status == AnswerState.READYTOSEND:
            self.Status = AnswerState.SENT
            return True
        return False

    def senderrormessage(self):
        """Handle sendErrorMessage event"""
        if self.Status == AnswerState.ERRORRESPONSE:
            self.Status = AnswerState.SENT
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
        """String representation of Answer"""
        return f"Answer(AnswerID={self.AnswerID}, QueryText={self.QueryText}, AnswerText={self.AnswerText})"
    def to_dict(self):
        """Convert Answer to dictionary"""
        return {
            'AnswerID': str(self.AnswerID) if self.AnswerID else None,
            'QueryText': self.QueryText,
            'AnswerText': self.AnswerText,
            'Sources': self.Sources,
            'Confidence': self.Confidence,
            'Status': self.Status.value if hasattr(self.Status, 'value') else str(self.Status),
        }
    def validate(self) -> bool:
        """Validate Answer data"""
        # TODO: Add validation logic
        # Check required fields
        if self.AnswerID is None:
            return False
        if self.QueryText is None:
            return False
        if self.AnswerText is None:
            return False
        if self.Sources is None:
            return False
        if self.Confidence is None:
            return False
        return True