"""
Evaluation criteria models for CV-JD matching and assessment.

These models implement a configurable, evidence-based evaluation framework
for matching candidates to job descriptions with explainable scoring.
"""

from typing import List, Optional, Dict, Any, Literal
from enum import Enum

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# ENUMS FOR EVALUATION
# ============================================================================

class MatchLevel(str, Enum):
    """Match level classification"""
    EXCELLENT = "excellent"  # 90-100%
    GOOD = "good"  # 75-89%
    MODERATE = "moderate"  # 60-74%
    WEAK = "weak"  # 40-59%
    POOR = "poor"  # 0-39%


class CriterionType(str, Enum):
    """Type of evaluation criterion"""
    SKILLS = "skills"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    CERTIFICATIONS = "certifications"
    SOFT_SKILLS = "soft_skills"
    CULTURE_FIT = "culture_fit"
    LOCATION = "location"
    SALARY = "salary"
    CUSTOM = "custom"


class MatchImpact(str, Enum):
    """Impact of a match on overall score"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


# ============================================================================
# CRITERION CONFIGURATION
# ============================================================================

class CriterionConfig(BaseModel):
    """
    Configuration for a single evaluation criterion.

    Allows customization of matching weights and thresholds per role or division.
    """

    name: str = Field(..., description="Criterion name")

    criterion_type: CriterionType = Field(
        ...,
        description="Type of criterion"
    )

    weight: float = Field(
        ...,
        description="Weight in overall score (0-1)",
        ge=0.0,
        le=1.0,
    )

    is_required: bool = Field(
        default=False,
        description="Whether this is a required criterion (disqualifying if not met)"
    )

    minimum_score: float = Field(
        default=0.0,
        description="Minimum score required for this criterion (0-100)",
        ge=0.0,
        le=100.0,
    )

    description: Optional[str] = Field(
        None,
        description="Description of what this criterion evaluates"
    )

    evaluation_method: Optional[str] = Field(
        None,
        description="Method used for evaluation (e.g., 'keyword_match', 'semantic_similarity')"
    )

    custom_parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Custom parameters for this criterion"
    )


class EvaluationConfig(BaseModel):
    """
    Complete evaluation configuration for a role or division.

    Defines all criteria and their weights for candidate-job matching.
    """

    config_id: str = Field(..., description="Configuration identifier")

    config_name: str = Field(..., description="Human-readable config name")

    division: Optional[str] = Field(
        None,
        description="AIA division this config applies to"
    )

    criteria: List[CriterionConfig] = Field(
        ...,
        description="List of evaluation criteria"
    )

    overall_pass_threshold: float = Field(
        default=60.0,
        description="Overall score threshold for 'pass' (0-100)",
        ge=0.0,
        le=100.0,
    )

    strict_mode: bool = Field(
        default=False,
        description="Whether to apply strict matching (all required criteria must pass)"
    )

    description: Optional[str] = Field(
        None,
        description="Description of this configuration"
    )

    @field_validator("criteria")
    @classmethod
    def validate_weights_sum(cls, v: List[CriterionConfig]) -> List[CriterionConfig]:
        """Validate that weights sum to approximately 1.0"""
        total_weight = sum(criterion.weight for criterion in v)
        if not (0.95 <= total_weight <= 1.05):  # Allow 5% tolerance
            raise ValueError(
                f"Criterion weights must sum to ~1.0, got {total_weight:.2f}"
            )
        return v

    def get_required_criteria(self) -> List[CriterionConfig]:
        """Get only required criteria"""
        return [c for c in self.criteria if c.is_required]

    def get_criterion_by_type(self, criterion_type: CriterionType) -> List[CriterionConfig]:
        """Get criteria of a specific type"""
        return [c for c in self.criteria if c.criterion_type == criterion_type]


# ============================================================================
# MATCH EVIDENCE
# ============================================================================

class MatchEvidence(BaseModel):
    """
    Evidence for a specific match between CV and JD.

    Provides explainability by showing what in the CV matched what in the JD.
    """

    cv_span: Optional[str] = Field(
        None,
        description="Quote from CV supporting this match"
    )

    jd_span: Optional[str] = Field(
        None,
        description="Quote from JD that this matches"
    )

    match_type: str = Field(
        default="exact",
        description="Type of match (e.g., 'exact', 'semantic', 'inferred')"
    )

    confidence: float = Field(
        default=1.0,
        description="Confidence in this match (0-1)",
        ge=0.0,
        le=1.0,
    )

    reason: Optional[str] = Field(
        None,
        description="Explanation of why/how these match"
    )

    impact: float = Field(
        default=0.0,
        description="Impact on score (-1 to 1, negative = penalty)",
        ge=-1.0,
        le=1.0,
    )

    impact_category: MatchImpact = Field(
        default=MatchImpact.POSITIVE,
        description="Category of impact"
    )


# ============================================================================
# CRITERION EVALUATION RESULT
# ============================================================================

class CriterionEvaluation(BaseModel):
    """
    Result of evaluating a single criterion.

    Contains score, evidence, and explanation for one evaluation criterion.
    """

    criterion_name: str = Field(..., description="Name of criterion evaluated")

    criterion_type: CriterionType = Field(..., description="Type of criterion")

    score: float = Field(
        ...,
        description="Score for this criterion (0-100)",
        ge=0.0,
        le=100.0,
    )

    weight: float = Field(
        ...,
        description="Weight of this criterion (0-1)",
        ge=0.0,
        le=1.0,
    )

    weighted_score: float = Field(
        ...,
        description="Score * weight contribution to overall",
        ge=0.0,
        le=100.0,
    )

    passed: bool = Field(
        ...,
        description="Whether criterion passed minimum threshold"
    )

    is_required: bool = Field(
        default=False,
        description="Whether this criterion was required"
    )

    match_level: MatchLevel = Field(
        ...,
        description="Match level classification"
    )

    # Evidence and Explanation
    matches: List[MatchEvidence] = Field(
        default_factory=list,
        description="Evidence of matches found"
    )

    gaps: List[str] = Field(
        default_factory=list,
        description="Requirements from JD not found in CV"
    )

    strengths: List[str] = Field(
        default_factory=list,
        description="Areas where CV exceeds JD requirements"
    )

    explanation: Optional[str] = Field(
        None,
        description="Human-readable explanation of evaluation"
    )

    detailed_breakdown: Dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed breakdown of scoring (criterion-specific)"
    )

    def get_positive_matches(self) -> List[MatchEvidence]:
        """Get matches with positive impact"""
        return [m for m in self.matches if m.impact > 0]

    def get_negative_matches(self) -> List[MatchEvidence]:
        """Get matches with negative impact"""
        return [m for m in self.matches if m.impact < 0]


# ============================================================================
# OVERALL EVALUATION RESULT
# ============================================================================

class CVJDEvaluation(BaseModel):
    """
    Complete evaluation result for CV-JD matching.

    This is the main output of the matching pipeline, containing overall scores,
    criterion-by-criterion breakdown, and evidence-based explanations.
    """

    # Identifiers
    evaluation_id: Optional[str] = Field(
        None,
        description="Unique evaluation identifier"
    )

    candidate_id: Optional[str] = Field(
        None,
        description="Candidate identifier"
    )

    job_id: Optional[str] = Field(
        None,
        description="Job identifier"
    )

    # Overall Scores
    overall_score: float = Field(
        ...,
        description="Overall match score (0-100)",
        ge=0.0,
        le=100.0,
    )

    match_level: MatchLevel = Field(
        ...,
        description="Overall match level"
    )

    passed: bool = Field(
        ...,
        description="Whether candidate passed overall threshold"
    )

    # Criterion Results
    criterion_evaluations: List[CriterionEvaluation] = Field(
        default_factory=list,
        description="Results for each criterion"
    )

    # Summary
    summary: Optional[str] = Field(
        None,
        description="Executive summary of evaluation",
        max_length=1000
    )

    key_strengths: List[str] = Field(
        default_factory=list,
        description="Key strengths of candidate for this role"
    )

    key_gaps: List[str] = Field(
        default_factory=list,
        description="Key gaps in candidate profile vs requirements"
    )

    areas_to_probe: List[str] = Field(
        default_factory=list,
        description="Areas to explore further in interview"
    )

    # Disqualification
    is_disqualified: bool = Field(
        default=False,
        description="Whether candidate is disqualified"
    )

    disqualification_reasons: List[str] = Field(
        default_factory=list,
        description="Reasons for disqualification if applicable"
    )

    # Recommendations
    recommendation: Literal["strong_yes", "yes", "maybe", "no", "strong_no"] = Field(
        ...,
        description="Hiring recommendation"
    )

    recommendation_reason: Optional[str] = Field(
        None,
        description="Reason for recommendation"
    )

    interview_priority: Literal["high", "medium", "low"] = Field(
        default="medium",
        description="Priority for scheduling interview"
    )

    # Evidence
    all_match_evidence: List[MatchEvidence] = Field(
        default_factory=list,
        description="All match evidence across criteria"
    )

    confidence_score: float = Field(
        default=0.0,
        description="Confidence in evaluation (0-1)",
        ge=0.0,
        le=1.0,
    )

    # Metadata
    evaluation_timestamp: Optional[str] = Field(
        None,
        description="ISO timestamp of evaluation"
    )

    config_used: Optional[str] = Field(
        None,
        description="Evaluation config ID used"
    )

    model_version: Optional[str] = Field(
        None,
        description="Model version used for evaluation"
    )

    division: Optional[str] = Field(
        None,
        description="AIA division for this evaluation"
    )

    @field_validator("criterion_evaluations")
    @classmethod
    def calculate_overall_score_validator(
        cls, v: List[CriterionEvaluation]
    ) -> List[CriterionEvaluation]:
        """Validate criterion evaluations are present"""
        if not v:
            raise ValueError("At least one criterion evaluation required")
        return v

    def get_failed_required_criteria(self) -> List[CriterionEvaluation]:
        """Get required criteria that failed"""
        return [c for c in self.criterion_evaluations if c.is_required and not c.passed]

    def get_top_scoring_criteria(self, n: int = 3) -> List[CriterionEvaluation]:
        """Get top N scoring criteria"""
        return sorted(self.criterion_evaluations, key=lambda c: c.score, reverse=True)[:n]

    def get_lowest_scoring_criteria(self, n: int = 3) -> List[CriterionEvaluation]:
        """Get bottom N scoring criteria"""
        return sorted(self.criterion_evaluations, key=lambda c: c.score)[:n]

    def get_criterion_by_type(self, criterion_type: CriterionType) -> List[CriterionEvaluation]:
        """Get evaluations for specific criterion type"""
        return [c for c in self.criterion_evaluations if c.criterion_type == criterion_type]

    def calculate_component_scores(self) -> Dict[str, float]:
        """Calculate average scores by criterion type"""
        scores_by_type: Dict[str, List[float]] = {}

        for criterion in self.criterion_evaluations:
            ctype = criterion.criterion_type
            if ctype not in scores_by_type:
                scores_by_type[ctype] = []
            scores_by_type[ctype].append(criterion.score)

        return {
            ctype: sum(scores) / len(scores) for ctype, scores in scores_by_type.items()
        }

    def get_all_gaps(self) -> List[str]:
        """Get all gaps across all criteria"""
        all_gaps = []
        for criterion in self.criterion_evaluations:
            all_gaps.extend(criterion.gaps)
        return all_gaps

    def get_all_strengths(self) -> List[str]:
        """Get all strengths across all criteria"""
        all_strengths = []
        for criterion in self.criterion_evaluations:
            all_strengths.extend(criterion.strengths)
        return all_strengths

    def generate_summary(self) -> str:
        """Generate evaluation summary"""
        parts = []

        # Overall
        parts.append(f"Overall: {self.match_level.value} ({self.overall_score:.1f}%)")

        # Top criterion
        top_criterion = self.get_top_scoring_criteria(1)
        if top_criterion:
            parts.append(f"Strongest: {top_criterion[0].criterion_name}")

        # Gaps
        if self.key_gaps:
            parts.append(f"{len(self.key_gaps)} key gaps")

        # Recommendation
        parts.append(f"Recommendation: {self.recommendation}")

        return " | ".join(parts)


# ============================================================================
# BATCH EVALUATION RESULT
# ============================================================================

class BatchEvaluationResult(BaseModel):
    """
    Result of evaluating multiple candidates against a single JD.

    Used for ranking candidates for a position.
    """

    job_id: str = Field(..., description="Job identifier")

    evaluations: List[CVJDEvaluation] = Field(
        default_factory=list,
        description="Individual candidate evaluations"
    )

    evaluation_timestamp: Optional[str] = Field(
        None,
        description="ISO timestamp of batch evaluation"
    )

    config_used: Optional[str] = Field(
        None,
        description="Evaluation config ID used"
    )

    def get_ranked_candidates(self) -> List[CVJDEvaluation]:
        """Get candidates ranked by overall score"""
        return sorted(self.evaluations, key=lambda e: e.overall_score, reverse=True)

    def get_qualified_candidates(self) -> List[CVJDEvaluation]:
        """Get only candidates who passed"""
        return [e for e in self.evaluations if e.passed and not e.is_disqualified]

    def get_strong_yes_candidates(self) -> List[CVJDEvaluation]:
        """Get candidates with 'strong_yes' recommendation"""
        return [e for e in self.evaluations if e.recommendation == "strong_yes"]

    def get_top_n_candidates(self, n: int = 10) -> List[CVJDEvaluation]:
        """Get top N candidates by score"""
        return self.get_ranked_candidates()[:n]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def classify_match_level(score: float) -> MatchLevel:
    """Convert numeric score to match level"""
    if score >= 90:
        return MatchLevel.EXCELLENT
    elif score >= 75:
        return MatchLevel.GOOD
    elif score >= 60:
        return MatchLevel.MODERATE
    elif score >= 40:
        return MatchLevel.WEAK
    else:
        return MatchLevel.POOR


def calculate_recommendation(
    overall_score: float,
    failed_required: List[CriterionEvaluation],
    is_disqualified: bool,
) -> Literal["strong_yes", "yes", "maybe", "no", "strong_no"]:
    """
    Calculate hiring recommendation based on evaluation results.

    Args:
        overall_score: Overall match score (0-100)
        failed_required: List of failed required criteria
        is_disqualified: Whether candidate is disqualified

    Returns:
        Recommendation level
    """
    if is_disqualified or failed_required:
        return "strong_no"

    if overall_score >= 90:
        return "strong_yes"
    elif overall_score >= 75:
        return "yes"
    elif overall_score >= 60:
        return "maybe"
    elif overall_score >= 40:
        return "no"
    else:
        return "strong_no"


def create_default_evaluation_config(division: Optional[str] = None) -> EvaluationConfig:
    """
    Create default evaluation configuration.

    Args:
        division: Optional division to customize for

    Returns:
        Default evaluation configuration
    """
    # Base configuration
    criteria = [
        CriterionConfig(
            name="Technical Skills",
            criterion_type=CriterionType.SKILLS,
            weight=0.30,
            is_required=True,
            minimum_score=60.0,
            description="Match on required technical skills",
        ),
        CriterionConfig(
            name="Experience",
            criterion_type=CriterionType.EXPERIENCE,
            weight=0.30,
            is_required=True,
            minimum_score=50.0,
            description="Relevant work experience",
        ),
        CriterionConfig(
            name="Education",
            criterion_type=CriterionType.EDUCATION,
            weight=0.20,
            is_required=False,
            minimum_score=40.0,
            description="Educational background",
        ),
        CriterionConfig(
            name="Certifications",
            criterion_type=CriterionType.CERTIFICATIONS,
            weight=0.20,
            is_required=False,
            minimum_score=0.0,
            description="Professional certifications",
        ),
    ]

    return EvaluationConfig(
        config_id=f"default_{division or 'general'}",
        config_name=f"Default Configuration - {division or 'General'}",
        division=division,
        criteria=criteria,
        overall_pass_threshold=60.0,
        strict_mode=False,
    )
