from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class StepItem(BaseModel):
    action: str = Field(..., description="Action to perform")
    expected_result: str = Field(..., description="Expected result for the action")


class QaseCase(BaseModel):
    suite: Optional[str] = None
    title: str
    description: Optional[str] = None
    preconditions: Optional[str] = None
    postconditions: Optional[str] = None
    priority: Optional[str] = None
    severity: Optional[str] = None
    type: Optional[str] = None
    layer: Optional[str] = None
    behavior: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    steps: List[StepItem] = Field(default_factory=list)
    source_files: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class QaseCaseCollection(BaseModel):
    test_cases: List[QaseCase] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)