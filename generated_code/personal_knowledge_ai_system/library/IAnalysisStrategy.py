from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


@dataclass
class IAnalysisStrategy:
    """Interface untuk strategi analisis (e.g., ConnectionFinder)."""


    StrategyID: UUID = field(default_factory=uuid4)




    # Auto-generated methods
    def __str__(self):
        """String representation of IAnalysisStrategy"""
        return f"IAnalysisStrategy(StrategyID={self.StrategyID})"
    def to_dict(self):
        """Convert IAnalysisStrategy to dictionary"""
        return {
            'StrategyID': str(self.StrategyID) if self.StrategyID else None,
        }
    def validate(self) -> bool:
        """Validate IAnalysisStrategy data"""
        # TODO: Add validation logic
        # Check required fields
        if self.StrategyID is None:
            return False
        return True