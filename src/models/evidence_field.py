"""
Evidence-based field models for explainable extraction.

These models implement the evidence-based extraction pattern where every extracted
value includes confidence scores and evidence spans (direct quotes from source documents)
to ensure transparency and prevent hallucination.
"""

from typing import List, Optional, Generic, TypeVar, Union
from datetime import date

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# GENERIC EVIDENCE FIELD MODEL
# ============================================================================

T = TypeVar("T")  # Type variable for generic evidence fields


class EvidenceField(BaseModel, Generic[T]):
    """
    Generic evidence-based field that wraps any value with confidence and evidence.

    This is the core pattern for explainable extraction - every extracted value
    includes its confidence score and the evidence (direct quotes) that support it.

    Example:
        email_field = EvidenceField(
            value="john.doe@example.com",
            confidence=1.0,
            evidence_spans=["Contact: john.doe@example.com"]
        )
    """

    value: T = Field(..., description="The extracted or inferred value")

    confidence: float = Field(
        ...,
        description="Confidence score (0.0 = no confidence, 1.0 = certain)",
        ge=0.0,
        le=1.0,
    )

    evidence_spans: List[str] = Field(
        default_factory=list,
        description="Direct quotes from source document that support this value",
    )

    inferred: bool = Field(
        default=False,
        description="Whether value was inferred rather than explicitly stated",
    )

    extraction_method: Optional[str] = Field(
        None,
        description="Method used for extraction (e.g., 'regex', 'llm', 'rule-based')",
    )

    context: Optional[str] = Field(
        None,
        description="Additional context about the extraction",
        max_length=500,
    )

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0 and 1"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v

    def is_high_confidence(self, threshold: float = 0.8) -> bool:
        """Check if confidence exceeds threshold"""
        return self.confidence >= threshold

    def is_low_confidence(self, threshold: float = 0.5) -> bool:
        """Check if confidence is below threshold"""
        return self.confidence < threshold

    def has_evidence(self) -> bool:
        """Check if evidence spans exist"""
        return len(self.evidence_spans) > 0

    def get_primary_evidence(self) -> Optional[str]:
        """Get the first (primary) evidence span"""
        return self.evidence_spans[0] if self.evidence_spans else None


# ============================================================================
# SPECIFIC EVIDENCE FIELD TYPES
# ============================================================================

class EvidenceString(EvidenceField[str]):
    """Evidence-based string field"""

    pass


class EvidenceFloat(EvidenceField[float]):
    """Evidence-based float field"""

    pass


class EvidenceInt(EvidenceField[int]):
    """Evidence-based integer field"""

    pass


class EvidenceBool(EvidenceField[bool]):
    """Evidence-based boolean field"""

    pass


class EvidenceDate(EvidenceField[date]):
    """Evidence-based date field"""

    pass


class EvidenceList(EvidenceField[List[str]]):
    """Evidence-based list field"""

    pass


# ============================================================================
# DOMAIN-SPECIFIC EVIDENCE MODELS
# ============================================================================

class EvidenceSkill(BaseModel):
    """
    Skill with evidence-based extraction.

    Each skill includes not just the name but also evidence from the CV,
    confidence in the extraction, and optional proficiency level.
    """

    name: str = Field(..., description="Skill name")

    confidence: float = Field(
        ...,
        description="Confidence that candidate has this skill (0-1)",
        ge=0.0,
        le=1.0,
    )

    evidence_spans: List[str] = Field(
        default_factory=list,
        description="Direct quotes showing this skill",
    )

    proficiency_level: Optional[str] = Field(
        None,
        description="Proficiency level (e.g., 'beginner', 'expert')",
    )

    proficiency_confidence: Optional[float] = Field(
        None,
        description="Confidence in proficiency assessment (0-1)",
        ge=0.0,
        le=1.0,
    )

    years_of_experience: Optional[float] = Field(
        None,
        description="Years of experience with this skill (if extractable)",
        ge=0,
    )

    last_used: Optional[str] = Field(
        None,
        description="When skill was last used (if mentioned)",
    )

    inferred: bool = Field(
        default=False,
        description="Whether skill was inferred vs explicitly stated",
    )

    source_context: Optional[str] = Field(
        None,
        description="Context where skill was found (e.g., 'work_experience', 'skills_section')",
    )

    def is_verified(self, min_confidence: float = 0.7) -> bool:
        """Check if skill extraction is verified (high confidence + evidence)"""
        return self.confidence >= min_confidence and len(self.evidence_spans) > 0


class EvidenceWorkExperience(BaseModel):
    """
    Work experience with evidence-based extraction.

    Each field that was extracted from the CV includes evidence spans
    to show where the information came from.
    """

    company_name: EvidenceString = Field(..., description="Company name with evidence")

    job_title: EvidenceString = Field(..., description="Job title with evidence")

    start_date: Optional[EvidenceDate] = Field(
        None,
        description="Start date with evidence"
    )

    end_date: Optional[EvidenceDate] = Field(
        None,
        description="End date with evidence (None if current)"
    )

    is_current: EvidenceBool = Field(..., description="Whether this is current role")

    location: Optional[EvidenceString] = Field(
        None,
        description="Job location with evidence"
    )

    responsibilities: List[EvidenceString] = Field(
        default_factory=list,
        description="Responsibilities with evidence"
    )

    achievements: List[EvidenceString] = Field(
        default_factory=list,
        description="Achievements with evidence"
    )

    technologies_used: List[EvidenceSkill] = Field(
        default_factory=list,
        description="Technologies with evidence"
    )

    duration_months: Optional[EvidenceFloat] = Field(
        None,
        description="Duration in months with evidence"
    )

    overall_quality_score: float = Field(
        default=0.0,
        description="Overall quality score for this work experience entry (0-1)",
        ge=0.0,
        le=1.0,
    )


class EvidenceEducation(BaseModel):
    """
    Education with evidence-based extraction.
    """

    institution_name: EvidenceString = Field(..., description="Institution name with evidence")

    degree: EvidenceString = Field(..., description="Degree with evidence")

    field_of_study: Optional[EvidenceString] = Field(
        None,
        description="Field of study with evidence"
    )

    start_date: Optional[EvidenceDate] = Field(
        None,
        description="Start date with evidence"
    )

    end_date: Optional[EvidenceDate] = Field(
        None,
        description="End date with evidence"
    )

    gpa: Optional[EvidenceFloat] = Field(
        None,
        description="GPA with evidence"
    )

    honors: List[EvidenceString] = Field(
        default_factory=list,
        description="Honors with evidence"
    )

    overall_quality_score: float = Field(
        default=0.0,
        description="Overall quality score for this education entry (0-1)",
        ge=0.0,
        le=1.0,
    )


class EvidenceCertification(BaseModel):
    """
    Certification with evidence-based extraction.
    """

    name: EvidenceString = Field(..., description="Certification name with evidence")

    issuing_organization: EvidenceString = Field(
        ...,
        description="Issuing organization with evidence"
    )

    issue_date: Optional[EvidenceDate] = Field(
        None,
        description="Issue date with evidence"
    )

    expiration_date: Optional[EvidenceDate] = Field(
        None,
        description="Expiration date with evidence"
    )

    credential_id: Optional[EvidenceString] = Field(
        None,
        description="Credential ID with evidence"
    )

    is_active: EvidenceBool = Field(
        ...,
        description="Whether certification is active"
    )

    overall_quality_score: float = Field(
        default=0.0,
        description="Overall quality score for this certification (0-1)",
        ge=0.0,
        le=1.0,
    )


# ============================================================================
# EVIDENCE-BASED CANDIDATE PROFILE
# ============================================================================

class EvidenceBasedCandidateProfile(BaseModel):
    """
    Complete candidate profile with evidence-based extraction.

    This version of CandidateProfile uses evidence fields throughout,
    providing full transparency and explainability for all extracted data.
    """

    # Personal Information
    full_name: EvidenceString = Field(..., description="Full name with evidence")

    email: Optional[EvidenceString] = Field(
        None,
        description="Email with evidence"
    )

    phone: Optional[EvidenceString] = Field(
        None,
        description="Phone with evidence"
    )

    location: Optional[EvidenceString] = Field(
        None,
        description="Location with evidence"
    )

    linkedin_url: Optional[EvidenceString] = Field(
        None,
        description="LinkedIn URL with evidence"
    )

    professional_summary: Optional[EvidenceString] = Field(
        None,
        description="Professional summary with evidence"
    )

    # Work Experience
    work_experience: List[EvidenceWorkExperience] = Field(
        default_factory=list,
        description="Work experience with evidence"
    )

    # Education
    education: List[EvidenceEducation] = Field(
        default_factory=list,
        description="Education with evidence"
    )

    # Skills
    skills: List[EvidenceSkill] = Field(
        default_factory=list,
        description="Skills with evidence and confidence"
    )

    # Certifications
    certifications: List[EvidenceCertification] = Field(
        default_factory=list,
        description="Certifications with evidence"
    )

    # Computed Fields
    total_years_experience: Optional[EvidenceFloat] = Field(
        None,
        description="Total years of experience with evidence"
    )

    career_level: Optional[EvidenceString] = Field(
        None,
        description="Career level with evidence"
    )

    primary_division: Optional[EvidenceString] = Field(
        None,
        description="Primary AIA division match with evidence"
    )

    # Overall Scores
    extraction_quality_score: float = Field(
        default=0.0,
        description="Overall extraction quality (0-1)",
        ge=0.0,
        le=1.0,
    )

    average_confidence: float = Field(
        default=0.0,
        description="Average confidence across all fields (0-1)",
        ge=0.0,
        le=1.0,
    )

    evidence_coverage: float = Field(
        default=0.0,
        description="Percentage of fields with evidence (0-1)",
        ge=0.0,
        le=1.0,
    )

    def get_high_confidence_skills(self, threshold: float = 0.8) -> List[EvidenceSkill]:
        """Get skills with confidence above threshold"""
        return [s for s in self.skills if s.confidence >= threshold]

    def get_verified_skills(self) -> List[EvidenceSkill]:
        """Get skills that are verified (high confidence + evidence)"""
        return [s for s in self.skills if s.is_verified()]

    def get_low_confidence_fields(self, threshold: float = 0.5) -> List[str]:
        """Get list of field names with confidence below threshold"""
        low_confidence_fields = []

        # Check personal info
        if self.email and self.email.confidence < threshold:
            low_confidence_fields.append("email")
        if self.phone and self.phone.confidence < threshold:
            low_confidence_fields.append("phone")
        if self.location and self.location.confidence < threshold:
            low_confidence_fields.append("location")

        # Check computed fields
        if self.total_years_experience and self.total_years_experience.confidence < threshold:
            low_confidence_fields.append("total_years_experience")
        if self.career_level and self.career_level.confidence < threshold:
            low_confidence_fields.append("career_level")

        return low_confidence_fields

    def calculate_overall_scores(self) -> None:
        """Calculate overall quality scores"""
        confidences = []

        # Collect all confidence scores
        if self.email:
            confidences.append(self.email.confidence)
        if self.phone:
            confidences.append(self.phone.confidence)
        if self.location:
            confidences.append(self.location.confidence)

        for exp in self.work_experience:
            confidences.append(exp.company_name.confidence)
            confidences.append(exp.job_title.confidence)

        for edu in self.education:
            confidences.append(edu.institution_name.confidence)
            confidences.append(edu.degree.confidence)

        for skill in self.skills:
            confidences.append(skill.confidence)

        # Calculate average confidence
        if confidences:
            self.average_confidence = sum(confidences) / len(confidences)

        # Calculate evidence coverage
        evidence_fields = []
        if self.email:
            evidence_fields.append(self.email.has_evidence())
        if self.phone:
            evidence_fields.append(self.phone.has_evidence())

        for skill in self.skills:
            evidence_fields.append(len(skill.evidence_spans) > 0)

        if evidence_fields:
            self.evidence_coverage = sum(evidence_fields) / len(evidence_fields)

        # Overall quality is weighted average
        self.extraction_quality_score = (
            0.6 * self.average_confidence + 0.4 * self.evidence_coverage
        )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_evidence_field(
    value: T,
    evidence: Union[str, List[str]],
    confidence: float = 1.0,
    inferred: bool = False,
    extraction_method: Optional[str] = None,
) -> EvidenceField[T]:
    """
    Utility function to create an evidence field.

    Args:
        value: The extracted value
        evidence: Evidence span(s) supporting the value
        confidence: Confidence score (0-1)
        inferred: Whether value was inferred
        extraction_method: Method used for extraction

    Returns:
        EvidenceField instance
    """
    evidence_spans = [evidence] if isinstance(evidence, str) else evidence

    return EvidenceField(
        value=value,
        confidence=confidence,
        evidence_spans=evidence_spans,
        inferred=inferred,
        extraction_method=extraction_method,
    )


def merge_evidence_fields(fields: List[EvidenceField[T]]) -> EvidenceField[T]:
    """
    Merge multiple evidence fields (e.g., from different extraction methods).

    Takes the value with highest confidence and combines all evidence.

    Args:
        fields: List of evidence fields to merge

    Returns:
        Merged evidence field
    """
    if not fields:
        raise ValueError("Cannot merge empty list of fields")

    # Sort by confidence (highest first)
    sorted_fields = sorted(fields, key=lambda f: f.confidence, reverse=True)

    # Take value from highest confidence field
    best_field = sorted_fields[0]

    # Combine all evidence
    all_evidence = []
    for field in fields:
        all_evidence.extend(field.evidence_spans)

    # Remove duplicates while preserving order
    unique_evidence = []
    seen = set()
    for span in all_evidence:
        if span not in seen:
            unique_evidence.append(span)
            seen.add(span)

    return EvidenceField(
        value=best_field.value,
        confidence=best_field.confidence,
        evidence_spans=unique_evidence,
        inferred=best_field.inferred,
        extraction_method=f"merged_{len(fields)}_sources",
    )


def validate_evidence_consistency(
    field: EvidenceField[T],
    min_confidence_for_evidence: float = 0.5,
) -> bool:
    """
    Validate that evidence is consistent with confidence score.

    High confidence should have evidence, low confidence may not.

    Args:
        field: Evidence field to validate
        min_confidence_for_evidence: Minimum confidence that requires evidence

    Returns:
        True if consistent, False otherwise
    """
    if field.confidence >= min_confidence_for_evidence:
        return field.has_evidence()
    return True  # Low confidence doesn't require evidence
