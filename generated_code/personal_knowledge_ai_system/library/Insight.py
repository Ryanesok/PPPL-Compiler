from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class InsightState(Enum):
    """States for Insight"""
    ANALYZING = "Analyzing"
    PATTERNDETECTED = "PatternDetected"
    NOPATTERN = "NoPattern"
    SCORING = "Scoring"
    HIGHPRIORITY = "HighPriority"
    LOWPRIORITY = "LowPriority"
    VALIDATING = "Validating"
    VALID = "Valid"
    INVALID = "Invalid"
    READYTONOTIFY = "ReadyToNotify"
    NOTIFYING = "Notifying"
    SENT = "Sent"
    FAILED = "Failed"
    ABANDONED = "Abandoned"
    VIEWED = "Viewed"
    EXPIRED = "Expired"
    ACKNOWLEDGED = "Acknowledged"
    DISMISSED = "Dismissed"
    ACTIONED = "Actioned"
    QUEUED = "Queued"
    DISCARDED = "Discarded"


@dataclass
class Insight:
    """Insight yang dihasilkan dari analisis proaktif."""


    InsightID: UUID = field(default_factory=uuid4)
    Title: Optional[str] = None
    Description: Optional[str] = None
    RelatedDocs: Optional[str] = None
    Priority: Optional[str] = None
    Score: Optional[float] = None
    UserID: UUID = field(default_factory=uuid4)
    Status: 'InsightState' = field(default_factory=lambda: InsightState.ANALYZING)


    def foundconnections(self):
        """Handle foundConnections event"""
        if self.Status == InsightState.ANALYZING:
            self.Status = InsightState.PATTERNDETECTED
            return True
        return False

    def noinsightsfound(self):
        """Handle noInsightsFound event"""
        if self.Status == InsightState.ANALYZING:
            self.Status = InsightState.NOPATTERN
            return True
        return False

    def calculatepriority(self):
        """Handle calculatePriority event"""
        if self.Status == InsightState.PATTERNDETECTED:
            self.Status = InsightState.SCORING
            return True
        return False

    def scoreabovethreshold(self):
        """Handle scoreAboveThreshold event"""
        if self.Status == InsightState.SCORING:
            self.Status = InsightState.HIGHPRIORITY
            return True
        return False

    def scorebelowthreshold(self):
        """Handle scoreBelowThreshold event"""
        if self.Status == InsightState.SCORING:
            self.Status = InsightState.LOWPRIORITY
            return True
        return False

    def checkrelevance(self):
        """Handle checkRelevance event"""
        if self.Status == InsightState.HIGHPRIORITY:
            self.Status = InsightState.VALIDATING
            return True
        return False

    def storeforlater(self):
        """Handle storeForLater event"""
        if self.Status == InsightState.LOWPRIORITY:
            self.Status = InsightState.QUEUED
            return True
        return False

    def passesvalidation(self):
        """Handle passesValidation event"""
        if self.Status == InsightState.VALIDATING:
            self.Status = InsightState.VALID
            return True
        return False

    def notrelevant(self):
        """Handle notRelevant event"""
        if self.Status == InsightState.VALIDATING:
            self.Status = InsightState.INVALID
            return True
        return False

    def preparenotification(self):
        """Handle prepareNotification event"""
        if self.Status == InsightState.VALID:
            self.Status = InsightState.READYTONOTIFY
            return True
        return False

    def discardinsight(self):
        """Handle discardInsight event"""
        if self.Status == InsightState.INVALID:
            self.Status = InsightState.DISCARDED
            return True
        return False

    def sendtouser(self):
        """Handle sendToUser event"""
        if self.Status == InsightState.READYTONOTIFY:
            self.Status = InsightState.NOTIFYING
            return True
        return False

    def deliverysuccess(self):
        """Handle deliverySuccess event"""
        if self.Status == InsightState.NOTIFYING:
            self.Status = InsightState.SENT
            return True
        return False

    def deliveryfailed(self):
        """Handle deliveryFailed event"""
        if self.Status == InsightState.NOTIFYING:
            self.Status = InsightState.FAILED
            return True
        return False

    def retry(self):
        """Handle retry event"""
        if self.Status == InsightState.FAILED:
            self.Status = InsightState.NOTIFYING
            return True
        return False

    def maxretries(self):
        """Handle maxRetries event"""
        if self.Status == InsightState.FAILED:
            self.Status = InsightState.ABANDONED
            return True
        return False

    def useropensnotification(self):
        """Handle userOpensNotification event"""
        if self.Status == InsightState.SENT:
            self.Status = InsightState.VIEWED
            return True
        return False

    def notviewedin7days(self):
        """Handle notViewedIn7Days event"""
        if self.Status == InsightState.SENT:
            self.Status = InsightState.EXPIRED
            return True
        return False

    def useracknowledges(self):
        """Handle userAcknowledges event"""
        if self.Status == InsightState.VIEWED:
            self.Status = InsightState.ACKNOWLEDGED
            return True
        return False

    def userdismisses(self):
        """Handle userDismisses event"""
        if self.Status == InsightState.VIEWED:
            self.Status = InsightState.DISMISSED
            return True
        return False

    def useractsoninsight(self):
        """Handle userActsOnInsight event"""
        if self.Status == InsightState.ACKNOWLEDGED:
            self.Status = InsightState.ACTIONED
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
        """String representation of Insight"""
        return f"Insight(InsightID={self.InsightID}, Title={self.Title}, Description={self.Description})"
    def to_dict(self):
        """Convert Insight to dictionary"""
        return {
            'InsightID': str(self.InsightID) if self.InsightID else None,
            'Title': self.Title,
            'Description': self.Description,
            'RelatedDocs': self.RelatedDocs,
            'Priority': self.Priority,
            'Score': self.Score,
            'UserID': str(self.UserID) if self.UserID else None,
            'Status': self.Status.value if hasattr(self.Status, 'value') else str(self.Status),
        }
    def validate(self) -> bool:
        """Validate Insight data"""
        # TODO: Add validation logic
        # Check required fields
        if self.InsightID is None:
            return False
        if self.Title is None:
            return False
        if self.Description is None:
            return False
        if self.RelatedDocs is None:
            return False
        if self.Priority is None:
            return False
        if self.Score is None:
            return False
        if self.UserID is None:
            return False
        return True