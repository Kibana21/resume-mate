"""
HR Insights models for advanced CV analysis.

These models implement an intelligent HR analysis layer that provides:
- Career progression patterns
- Red flag detection (job hopping, employment gaps, etc.)
- Quality scoring (formatting, completeness, presentation)
- Key strengths and weakness identification
- Evidence-based insights for explainability
"""

from datetime import date
from typing import List, Optional, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# ENUMS FOR HR INSIGHTS
# ============================================================================

class CareerTrajectory(str, Enum):
    """Career progression trajectory"""
    UPWARD = "upward"  # Consistent progression upward
    LATERAL = "lateral"  # Moves across similar levels
    MIXED = "mixed"  # Mix of upward and lateral
    DOWNWARD = "downward"  # Moving to lower levels
    STAGNANT = "stagnant"  # No clear progression
    EARLY_CAREER = "early_career"  # Too early to determine


class RedFlagSeverity(str, Enum):
    """Severity level for red flags"""
    CRITICAL = "critical"  # Major concern
    HIGH = "high"  # Significant concern
    MEDIUM = "medium"  # Moderate concern
    LOW = "low"  # Minor concern
    INFO = "info"  # Informational only


class QualityLevel(str, Enum):
    """Quality level classification"""
    EXCELLENT = "excellent"  # 90-100
    GOOD = "good"  # 75-89
    ACCEPTABLE = "acceptable"  # 60-74
    POOR = "poor"  # 40-59
    VERY_POOR = "very_poor"  # 0-39


# ============================================================================
# RED FLAG MODELS
# ============================================================================

class RedFlag(BaseModel):
    """Individual red flag detected in CV"""

    flag_type: str = Field(
        ...,
        description="Type of red flag (e.g., 'job_hopping', 'employment_gap')"
    )

    severity: RedFlagSeverity = Field(
        ...,
        description="Severity level of the red flag"
    )

    description: str = Field(
        ...,
        description="Description of the red flag"
    )

    evidence_spans: List[str] = Field(
        default_factory=list,
        description="Evidence supporting this red flag"
    )

    recommendation: Optional[str] = Field(
        None,
        description="Recommendation for recruiter (e.g., 'Ask about in interview')"
    )

    impact_score: float = Field(
        default=0.0,
        description="Impact on overall candidate assessment (0-1)",
        ge=0.0,
        le=1.0,
    )


class EmploymentGap(BaseModel):
    """Employment gap information"""

    start_date: Optional[date] = Field(
        None,
        description="Start of gap period"
    )

    end_date: Optional[date] = Field(
        None,
        description="End of gap period"
    )

    duration_months: float = Field(
        ...,
        description="Duration of gap in months",
        ge=0
    )

    explanation_found: bool = Field(
        default=False,
        description="Whether an explanation was found in CV"
    )

    explanation: Optional[str] = Field(
        None,
        description="Explanation for gap if provided"
    )

    severity: RedFlagSeverity = Field(
        default=RedFlagSeverity.MEDIUM,
        description="Severity assessment"
    )


# ============================================================================
# CAREER PROGRESSION MODELS
# ============================================================================

class CareerProgression(BaseModel):
    """Career progression analysis"""

    trajectory: CareerTrajectory = Field(
        ...,
        description="Overall career trajectory"
    )

    progression_rate: Optional[str] = Field(
        None,
        description="Rate of progression (e.g., 'Fast', 'Moderate', 'Slow')"
    )

    years_to_current_level: Optional[float] = Field(
        None,
        description="Years taken to reach current level",
        ge=0
    )

    number_of_promotions: int = Field(
        default=0,
        description="Number of promotions identified",
        ge=0
    )

    average_tenure_months: Optional[float] = Field(
        None,
        description="Average tenure per role in months",
        ge=0
    )

    longest_tenure_months: Optional[float] = Field(
        None,
        description="Longest tenure in a single role",
        ge=0
    )

    shortest_tenure_months: Optional[float] = Field(
        None,
        description="Shortest tenure in a single role",
        ge=0
    )

    industry_consistency: float = Field(
        default=0.0,
        description="Industry consistency score (0-1, 1=always same industry)",
        ge=0.0,
        le=1.0,
    )

    role_consistency: float = Field(
        default=0.0,
        description="Role consistency score (0-1, 1=always similar roles)",
        ge=0.0,
        le=1.0,
    )

    summary: Optional[str] = Field(
        None,
        description="Summary of career progression",
        max_length=500
    )

    evidence_spans: List[str] = Field(
        default_factory=list,
        description="Evidence supporting progression analysis"
    )


# ============================================================================
# QUALITY SCORING MODELS
# ============================================================================

class FormattingQuality(BaseModel):
    """CV formatting quality assessment"""

    overall_score: float = Field(
        ...,
        description="Overall formatting quality score (0-100)",
        ge=0,
        le=100,
    )

    quality_level: QualityLevel = Field(
        ...,
        description="Quality level classification"
    )

    has_clear_sections: bool = Field(
        default=True,
        description="Whether CV has clear section headers"
    )

    has_consistent_formatting: bool = Field(
        default=True,
        description="Whether formatting is consistent"
    )

    has_professional_appearance: bool = Field(
        default=True,
        description="Whether CV appears professional"
    )

    readability_score: Optional[float] = Field(
        None,
        description="Readability score (0-100)",
        ge=0,
        le=100,
    )

    issues: List[str] = Field(
        default_factory=list,
        description="List of formatting issues found"
    )

    strengths: List[str] = Field(
        default_factory=list,
        description="List of formatting strengths"
    )


class CompletenessScore(BaseModel):
    """CV completeness assessment"""

    overall_score: float = Field(
        ...,
        description="Overall completeness score (0-100)",
        ge=0,
        le=100,
    )

    quality_level: QualityLevel = Field(
        ...,
        description="Completeness level"
    )

    has_contact_info: bool = Field(default=False, description="Has contact information")
    has_work_experience: bool = Field(default=False, description="Has work experience")
    has_education: bool = Field(default=False, description="Has education")
    has_skills: bool = Field(default=False, description="Has skills listed")
    has_certifications: bool = Field(default=False, description="Has certifications")
    has_achievements: bool = Field(default=False, description="Has quantifiable achievements")
    has_professional_summary: bool = Field(
        default=False, description="Has professional summary"
    )

    missing_sections: List[str] = Field(
        default_factory=list,
        description="Sections that are missing or incomplete"
    )

    optional_sections_present: List[str] = Field(
        default_factory=list,
        description="Optional sections that are present (projects, publications, etc.)"
    )


class ContentQuality(BaseModel):
    """CV content quality assessment"""

    overall_score: float = Field(
        ...,
        description="Overall content quality score (0-100)",
        ge=0,
        le=100,
    )

    quality_level: QualityLevel = Field(
        ...,
        description="Content quality level"
    )

    has_quantifiable_achievements: bool = Field(
        default=False,
        description="Whether achievements are quantified"
    )

    achievement_count: int = Field(
        default=0,
        description="Number of quantifiable achievements",
        ge=0
    )

    has_action_verbs: bool = Field(
        default=True,
        description="Whether strong action verbs are used"
    )

    has_relevant_keywords: bool = Field(
        default=True,
        description="Whether relevant industry keywords are present"
    )

    detail_level: str = Field(
        default="moderate",
        description="Level of detail (e.g., 'minimal', 'moderate', 'comprehensive')"
    )

    specificity_score: float = Field(
        default=0.0,
        description="How specific and concrete the content is (0-1)",
        ge=0.0,
        le=1.0,
    )

    strengths: List[str] = Field(
        default_factory=list,
        description="Content strengths"
    )

    weaknesses: List[str] = Field(
        default_factory=list,
        description="Content weaknesses"
    )


class QualityScore(BaseModel):
    """Overall CV quality scoring"""

    overall_score: float = Field(
        ...,
        description="Overall quality score (0-100)",
        ge=0,
        le=100,
    )

    quality_level: QualityLevel = Field(
        ...,
        description="Overall quality level"
    )

    formatting_quality: FormattingQuality = Field(
        ...,
        description="Formatting quality assessment"
    )

    completeness_score: CompletenessScore = Field(
        ...,
        description="Completeness assessment"
    )

    content_quality: ContentQuality = Field(
        ...,
        description="Content quality assessment"
    )

    ats_compatibility_score: Optional[float] = Field(
        None,
        description="ATS (Applicant Tracking System) compatibility (0-100)",
        ge=0,
        le=100,
    )

    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improvement"
    )


# ============================================================================
# KEY STRENGTHS AND INSIGHTS
# ============================================================================

class KeyStrength(BaseModel):
    """Individual key strength of the candidate"""

    strength_type: str = Field(
        ...,
        description="Type of strength (e.g., 'technical_expertise', 'leadership')"
    )

    description: str = Field(
        ...,
        description="Description of the strength"
    )

    evidence_spans: List[str] = Field(
        default_factory=list,
        description="Evidence supporting this strength"
    )

    relevance_score: float = Field(
        default=1.0,
        description="Relevance to target roles (0-1)",
        ge=0.0,
        le=1.0,
    )

    uniqueness_score: float = Field(
        default=0.5,
        description="How unique/differentiating this strength is (0-1)",
        ge=0.0,
        le=1.0,
    )


class CandidateHighlight(BaseModel):
    """Notable highlights about the candidate"""

    category: str = Field(
        ...,
        description="Category (e.g., 'Education', 'Achievement', 'Experience')"
    )

    highlight: str = Field(
        ...,
        description="The highlight itself"
    )

    impact: str = Field(
        default="medium",
        description="Impact level (e.g., 'high', 'medium', 'low')"
    )


# ============================================================================
# MAIN HR INSIGHTS MODEL
# ============================================================================

class HRInsights(BaseModel):
    """
    Complete HR insights for a candidate profile.

    This model provides an intelligent analysis layer on top of raw extracted data,
    giving recruiters actionable insights about candidates.
    """

    # Career Progression
    career_progression: Optional[CareerProgression] = Field(
        None,
        description="Career progression analysis"
    )

    # Red Flags
    red_flags: List[RedFlag] = Field(
        default_factory=list,
        description="Red flags detected"
    )

    employment_gaps: List[EmploymentGap] = Field(
        default_factory=list,
        description="Employment gaps found"
    )

    job_hopping_flag: bool = Field(
        default=False,
        description="Whether candidate shows job hopping pattern"
    )

    job_hopping_details: Optional[str] = Field(
        None,
        description="Details about job hopping if flagged"
    )

    # Quality Scoring
    quality_score: Optional[QualityScore] = Field(
        None,
        description="Overall CV quality assessment"
    )

    # Strengths & Highlights
    key_strengths: List[KeyStrength] = Field(
        default_factory=list,
        description="Key strengths of the candidate"
    )

    candidate_highlights: List[CandidateHighlight] = Field(
        default_factory=list,
        description="Notable highlights"
    )

    unique_selling_points: List[str] = Field(
        default_factory=list,
        description="Unique selling points"
    )

    # Qualification Assessment
    overqualification_risk: bool = Field(
        default=False,
        description="Risk of overqualification for typical roles"
    )

    overqualification_details: Optional[str] = Field(
        None,
        description="Details about overqualification risk"
    )

    underqualification_risk: bool = Field(
        default=False,
        description="Risk of underqualification for typical roles"
    )

    underqualification_details: Optional[str] = Field(
        None,
        description="Details about underqualification risk"
    )

    # Fit Assessment
    culture_fit_indicators: List[str] = Field(
        default_factory=list,
        description="Indicators of potential culture fit"
    )

    potential_concerns: List[str] = Field(
        default_factory=list,
        description="Potential concerns for consideration"
    )

    interview_focus_areas: List[str] = Field(
        default_factory=list,
        description="Recommended areas to explore in interview"
    )

    # Summary Insights
    executive_summary: Optional[str] = Field(
        None,
        description="Executive summary of candidate (2-3 sentences)",
        max_length=500
    )

    recruiter_notes: Optional[str] = Field(
        None,
        description="Additional notes for recruiters",
        max_length=1000
    )

    # Scores
    overall_candidate_score: float = Field(
        default=0.0,
        description="Overall candidate quality score (0-100)",
        ge=0,
        le=100,
    )

    hirability_score: float = Field(
        default=0.0,
        description="Hirability score based on market standards (0-100)",
        ge=0,
        le=100,
    )

    # Evidence
    evidence_spans: List[str] = Field(
        default_factory=list,
        description="Key evidence spans supporting insights"
    )

    # Metadata
    analysis_timestamp: Optional[str] = Field(
        None,
        description="ISO timestamp of analysis"
    )

    confidence_score: float = Field(
        default=0.0,
        description="Confidence in the insights provided (0-1)",
        ge=0.0,
        le=1.0,
    )

    def get_critical_red_flags(self) -> List[RedFlag]:
        """Get only critical severity red flags"""
        return [rf for rf in self.red_flags if rf.severity == RedFlagSeverity.CRITICAL]

    def get_high_severity_red_flags(self) -> List[RedFlag]:
        """Get high and critical severity red flags"""
        return [
            rf
            for rf in self.red_flags
            if rf.severity in [RedFlagSeverity.CRITICAL, RedFlagSeverity.HIGH]
        ]

    def has_significant_gaps(self, threshold_months: int = 6) -> bool:
        """Check if candidate has significant employment gaps"""
        return any(gap.duration_months >= threshold_months for gap in self.employment_gaps)

    def get_top_strengths(self, n: int = 3) -> List[KeyStrength]:
        """Get top N strengths by relevance"""
        sorted_strengths = sorted(
            self.key_strengths, key=lambda s: s.relevance_score, reverse=True
        )
        return sorted_strengths[:n]

    def is_high_quality_candidate(
        self,
        min_score: float = 75.0,
        max_critical_flags: int = 0,
    ) -> bool:
        """
        Determine if candidate is high quality based on criteria.

        Args:
            min_score: Minimum overall candidate score
            max_critical_flags: Maximum number of critical red flags allowed

        Returns:
            True if candidate meets quality criteria
        """
        return (
            self.overall_candidate_score >= min_score
            and len(self.get_critical_red_flags()) <= max_critical_flags
        )

    def calculate_risk_score(self) -> float:
        """
        Calculate overall risk score based on red flags and concerns.

        Returns:
            Risk score from 0 (no risk) to 1 (high risk)
        """
        risk_score = 0.0

        # Weight red flags by severity
        severity_weights = {
            RedFlagSeverity.CRITICAL: 0.4,
            RedFlagSeverity.HIGH: 0.3,
            RedFlagSeverity.MEDIUM: 0.2,
            RedFlagSeverity.LOW: 0.1,
            RedFlagSeverity.INFO: 0.05,
        }

        for flag in self.red_flags:
            risk_score += severity_weights.get(flag.severity, 0.1)

        # Cap at 1.0
        return min(risk_score, 1.0)

    def generate_summary(self) -> str:
        """Generate a concise summary of insights"""
        parts = []

        # Career trajectory
        if self.career_progression:
            parts.append(f"Career trajectory: {self.career_progression.trajectory}")

        # Quality
        if self.quality_score:
            parts.append(f"CV quality: {self.quality_score.quality_level}")

        # Red flags
        critical_flags = self.get_critical_red_flags()
        if critical_flags:
            parts.append(f"{len(critical_flags)} critical red flags")

        # Strengths
        if self.key_strengths:
            parts.append(f"{len(self.key_strengths)} key strengths identified")

        return " | ".join(parts) if parts else "No significant insights"


# ============================================================================
# UTILITY FUNCTIONS FOR HR INSIGHTS
# ============================================================================

def classify_quality_level(score: float) -> QualityLevel:
    """Convert numeric score to quality level"""
    if score >= 90:
        return QualityLevel.EXCELLENT
    elif score >= 75:
        return QualityLevel.GOOD
    elif score >= 60:
        return QualityLevel.ACCEPTABLE
    elif score >= 40:
        return QualityLevel.POOR
    else:
        return QualityLevel.VERY_POOR


def detect_job_hopping(
    average_tenure_months: float,
    short_tenure_threshold: float = 12.0,
    min_roles: int = 3,
) -> tuple[bool, Optional[str]]:
    """
    Detect job hopping pattern.

    Args:
        average_tenure_months: Average tenure per role
        short_tenure_threshold: Threshold for short tenure in months
        min_roles: Minimum number of roles to consider

    Returns:
        Tuple of (is_job_hopping, details)
    """
    if average_tenure_months < short_tenure_threshold:
        details = (
            f"Average tenure of {average_tenure_months:.1f} months is below "
            f"typical threshold of {short_tenure_threshold} months"
        )
        return (True, details)

    return (False, None)
