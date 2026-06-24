from typing import List, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class EligibilityRule(BaseModel):
    field: str
    operator: str
    value: Any
    explanation: str

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, v: str) -> str:
        valid_operators = {">=", "<=", "==", "in", "contains"}
        if v not in valid_operators:
            raise ValueError(f"Unsupported operator '{v}'. Must be one of {valid_operators}")
        return v


class Scheme(BaseModel):
    id: str
    name: str
    description: str
    level: str  # "central" or "state"
    state: Optional[str] = None
    eligibility_rules: List[EligibilityRule] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    apply_url: Optional[str] = None

    @model_validator(mode="after")
    def validate_state_and_level(self) -> "Scheme":
        if self.level == "state":
            if not self.state:
                raise ValueError("State name is required for state-level schemes")
        elif self.level == "central":
            if self.state:
                raise ValueError("Central schemes should not have a state assigned")
        else:
            raise ValueError("Level must be either 'central' or 'state'")
        return self


class CitizenProfile(BaseModel):
    age: int = Field(gt=0, description="Age must be greater than 0")
    income: float = Field(ge=0.0, description="Income must be non-negative")
    state: str
    category: str
    disability: bool
    occupation: Optional[str] = None
    source_language: str = Field(
        default="en", description="The original language of the user's input"
    )


class MatchResult(BaseModel):
    scheme_id: str
    is_eligible: bool
    matched_rules: List[EligibilityRule] = Field(default_factory=list)
    failed_rules: List[EligibilityRule] = Field(default_factory=list)
    overall_score: float = Field(
        ge=0.0, le=1.0, description="Overall match score must be between 0.0 and 1.0"
    )
