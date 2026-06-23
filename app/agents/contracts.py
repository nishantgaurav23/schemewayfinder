from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.schemes import CitizenProfile, MatchResult

# Output keys for ADK coordination steps
PROFILE_KEY = "citizen_profile"
MATCHES_KEY = "matches"
CHECKLIST_KEY = "checklist"
DRAFT_KEY = "application_draft"
AUDIT_KEY = "rejection_risk_audit"
REJECTED_MATCHES_KEY = "rejected_matches"
EXPLANATION_KEY = "explanation"


class SessionState(BaseModel):
    citizen_profile: Optional[CitizenProfile] = None
    matches: List[MatchResult] = Field(default_factory=list)
    checklist: List[str] = Field(default_factory=list)
    application_draft: Optional[str] = None
    rejection_risk_audit: Optional[dict] = None
    rejected_matches: List[dict] = Field(default_factory=list)
    explanation: Optional[str] = None
