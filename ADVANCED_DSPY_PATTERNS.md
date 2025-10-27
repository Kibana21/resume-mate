# Advanced DSPy Patterns for Production-Grade CV/JD Extraction

## Overview

This document describes **advanced DSPy patterns** observed from production implementations that significantly improve extraction quality, explainability, and matching accuracy.

---

## 1. Evidence-Based Extraction Pattern ⭐⭐⭐

### Problem
Traditional extraction returns just the value, making it impossible to verify accuracy or explain where the data came from.

### Solution
Extract **value + confidence + evidence spans** together.

### Implementation

```python
# models/evidence_field.py
from pydantic import BaseModel, Field
from typing import List, Optional

class EvidenceField(BaseModel):
    """Field with extraction evidence"""
    value: str = Field(..., description="The extracted or inferred value")
    confidence: float = Field(..., description="Confidence score 0.0-1.0", ge=0.0, le=1.0)
    evidence_spans: List[str] = Field(
        default_factory=list,
        description="Direct quotes from CV that support this value"
    )

class EvidenceDateRange(BaseModel):
    """Date range with evidence"""
    start: Optional[str] = Field(None, description="Start date in YYYY-MM format")
    end: Optional[str] = Field(None, description="End date in YYYY-MM or 'Present'")
    evidence_spans: List[str] = Field(default_factory=list)

class EvidenceLocation(BaseModel):
    """Location with evidence"""
    city: Optional[str] = None
    country_code: Optional[str] = Field(None, description="ISO 3166-1 alpha-2")
    evidence_spans: List[str] = Field(default_factory=list)

class EvidenceSkill(BaseModel):
    """Skill with evidence and metadata"""
    name: str = Field(..., description="Canonical skill name")
    category: str = Field(..., description="technical, soft, language, domain, platform, tool, cloud, database, methodology")
    proficiency: Optional[str] = Field(None, description="beginner, intermediate, advanced, expert")
    years_experience: Optional[float] = Field(None, description="Decimal years, e.g., 3.5")
    last_used_year: Optional[str] = Field(None, description="Four-digit year if known")
    evidence_spans: List[str] = Field(default_factory=list)
```

### DSPy Signatures with Evidence

```python
# dspy_modules/evidence_signatures.py
import dspy
from typing import List

class PersonalInfoWithEvidence(dspy.Signature):
    """Extract personal information with evidence"""

    cv_text: str = dspy.InputField(desc="CV text section")
    strict_extract_only: bool = dspy.InputField(
        desc="If true, do not infer unknowns; return nulls/empties.",
        default=False
    )

    # Name
    name: str = dspy.OutputField(desc="Full name of candidate")
    name_confidence: float = dspy.OutputField(desc="Confidence 0.0-1.0")
    name_evidence: str = dspy.OutputField(desc="Direct quote supporting the name")

    # Email
    email: str = dspy.OutputField(desc="Email address or 'None'")
    email_confidence: float = dspy.OutputField(desc="Confidence 0.0-1.0")
    email_evidence: str = dspy.OutputField(desc="Direct quote with email")

    # Location
    location_city: str = dspy.OutputField(desc="City or 'None'")
    location_country_code: str = dspy.OutputField(desc="ISO 3166-1 alpha-2 code or 'None'")
    location_confidence: float = dspy.OutputField(desc="Confidence 0.0-1.0")
    location_evidence: str = dspy.OutputField(desc="Direct quote with location")

class SkillWithEvidence(dspy.Signature):
    """Extract a skill with supporting evidence"""

    cv_text: str = dspy.InputField(desc="Full CV text for context")
    skill_mention: str = dspy.InputField(desc="Specific skill mention to analyze")

    canonical_name: str = dspy.OutputField(desc="Standardized skill name")
    category: str = dspy.OutputField(desc="One of: technical, soft, language, domain, platform, tool, cloud, database, methodology")
    proficiency: str = dspy.OutputField(desc="One of: beginner, intermediate, advanced, expert, or 'inferred'")
    years_experience: str = dspy.OutputField(desc="Decimal years or '0.0' if unknown")
    last_used_year: str = dspy.OutputField(desc="Four-digit year or 'None'")
    evidence_spans: str = dspy.OutputField(desc="Pipe-separated quotes supporting this skill")
    confidence: float = dspy.OutputField(desc="Overall confidence 0.0-1.0")

class ExperienceWithEvidence(dspy.Signature):
    """Extract work experience with evidence"""

    experience_text: str = dspy.InputField(desc="Text for one job/role")
    strict_extract_only: bool = dspy.InputField(default=False)

    title: str = dspy.OutputField(desc="Job title")
    title_evidence: str = dspy.OutputField(desc="Quote with title")

    company: str = dspy.OutputField(desc="Company name")
    company_evidence: str = dspy.OutputField(desc="Quote with company")

    start_date: str = dspy.OutputField(desc="YYYY-MM format")
    end_date: str = dspy.OutputField(desc="YYYY-MM or 'Present'")
    dates_evidence: str = dspy.OutputField(desc="Quote with dates")

    responsibilities: str = dspy.OutputField(desc="Pipe-separated list of responsibilities")
    achievements: str = dspy.OutputField(desc="Pipe-separated quantified accomplishments")
    domain_tags: str = dspy.OutputField(desc="Comma-separated domain tags: insurance, banking, fintech, etc.")

    confidence: float = dspy.OutputField(desc="Overall confidence 0.0-1.0")
```

### Module with Evidence

```python
# dspy_modules/evidence_extractors.py
import dspy
from models.evidence_field import EvidenceField, EvidenceSkill, EvidenceDateRange

class PersonalInfoExtractorWithEvidence(dspy.Module):
    """Extract personal info with evidence"""

    def __init__(self):
        super().__init__()
        self.extract = dspy.ChainOfThought(PersonalInfoWithEvidence)

    def forward(self, cv_text: str, strict_mode: bool = False) -> dict:
        """Extract with evidence"""
        result = self.extract(cv_text=cv_text, strict_extract_only=strict_mode)

        return {
            "name": EvidenceField(
                value=result.name,
                confidence=result.name_confidence,
                evidence_spans=[result.name_evidence] if result.name_evidence != "None" else []
            ),
            "email": EvidenceField(
                value=result.email if result.email.lower() != "none" else None,
                confidence=result.email_confidence,
                evidence_spans=[result.email_evidence] if result.email_evidence != "None" else []
            ),
            "location": {
                "city": result.location_city if result.location_city.lower() != "none" else None,
                "country_code": result.location_country_code if result.location_country_code.lower() != "none" else None,
                "confidence": result.location_confidence,
                "evidence_spans": [result.location_evidence] if result.location_evidence != "None" else []
            }
        }
```

---

## 2. HR Insights Pattern ⭐⭐⭐

### Problem
Basic extraction doesn't provide recruiter-relevant insights about candidate quality, risks, or red flags.

### Solution
Add an **HR Insights layer** that analyzes the extracted data for recruiter-relevant signals.

### Implementation

```python
# models/hr_insights.py
from pydantic import BaseModel, Field
from typing import List, Optional

class HRInsights(BaseModel):
    """HR-relevant insights derived from CV analysis"""

    # Career Progression
    career_progression_summary: Optional[str] = Field(
        None,
        description="Concise narrative (≤60 words) summarizing career growth"
    )

    # Red Flags
    job_hopping_flag: bool = Field(
        False,
        description="True if ≥3 roles with tenure <12 months each in the last 5 years"
    )

    employment_gaps: List[dict] = Field(
        default_factory=list,
        description="List of gaps ≥3 months in employment history, with date ranges"
    )

    overqualification_flag: bool = Field(
        False,
        description="True if candidate exceeds JD requirements; False unless explicitly stated"
    )

    underqualification_flag: bool = Field(
        False,
        description="True if candidate lacks JD requirements; false unless explicitly stated"
    )

    # Quality Signals
    formatting_quality: str = Field(
        ...,
        description="Overall formatting quality: poor, fair, good, excellent"
    )

    formatting_issues: List[str] = Field(
        default_factory=list,
        description="List of formatting problems (e.g., inconsistent_dates, missing_contact)"
    )

    red_flags: List[str] = Field(
        default_factory=list,
        description="Evidence-backed concerns found in the CV"
    )

    # Strengths
    key_strengths: List[str] = Field(
        default_factory=list,
        description="Top 3-5 notable strengths (quantified achievements, rare skills, etc.)"
    )

    # Evidence
    evidence_spans: List[str] = Field(
        default_factory=list,
        description="Snippets from the CV supporting the insights or flags"
    )

class QualityScore(BaseModel):
    """Overall CV quality assessment"""

    completeness_score: float = Field(..., description="0-100, % of expected fields present")
    detail_score: float = Field(..., description="0-100, richness of descriptions")
    formatting_score: float = Field(..., description="0-100, formatting quality")
    evidence_score: float = Field(..., description="0-100, quantified achievements present")

    overall_score: float = Field(..., description="0-100, weighted average")
    grade: str = Field(..., description="A+ to F grade")
```

### DSPy Signature for HR Insights

```python
# dspy_modules/hr_insights_signature.py
import dspy

class HRInsightsExtraction(dspy.Signature):
    """Analyze CV for HR-relevant insights and red flags"""

    # Input: Structured CV data
    work_experiences_json: str = dspy.InputField(desc="JSON array of work experiences")
    education_json: str = dspy.InputField(desc="JSON array of education")
    skills_json: str = dspy.InputField(desc="JSON array of skills")
    full_cv_text: str = dspy.InputField(desc="Original CV text for context")

    # Career Analysis
    career_progression_summary: str = dspy.OutputField(
        desc="Concise narrative (≤60 words) summarizing career trajectory and growth"
    )

    # Red Flags
    job_hopping_flag: bool = dspy.OutputField(
        desc="True if ≥3 roles with tenure <12 months in last 5 years"
    )

    employment_gaps_json: str = dspy.OutputField(
        desc="JSON array of employment gaps ≥3 months with start/end dates"
    )

    overqualification_flag: bool = dspy.OutputField(
        desc="True if overqualified for typical roles at their level"
    )

    underqualification_flag: bool = dspy.OutputField(
        desc="True if lacks typical qualifications for stated roles"
    )

    # Quality
    formatting_quality: str = dspy.OutputField(
        desc="One of: poor, fair, good, excellent"
    )

    formatting_issues: str = dspy.OutputField(
        desc="Comma-separated list of issues or 'none'"
    )

    red_flags: str = dspy.OutputField(
        desc="Comma-separated evidence-backed concerns or 'none'"
    )

    # Strengths
    key_strengths: str = dspy.OutputField(
        desc="Comma-separated list of top 3-5 notable strengths"
    )

    # Evidence
    evidence_spans: str = dspy.OutputField(
        desc="Pipe-separated CV snippets supporting insights/flags"
    )

class HRInsightsModule(dspy.Module):
    """Extract HR insights from structured CV data"""

    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought(HRInsightsExtraction)

    def forward(
        self,
        work_experiences: List[dict],
        education: List[dict],
        skills: List[dict],
        full_cv_text: str
    ) -> HRInsights:
        """Generate HR insights"""

        import json

        result = self.analyze(
            work_experiences_json=json.dumps(work_experiences),
            education_json=json.dumps(education),
            skills_json=json.dumps(skills),
            full_cv_text=full_cv_text
        )

        # Parse employment gaps
        try:
            employment_gaps = json.loads(result.employment_gaps_json) if result.employment_gaps_json != "none" else []
        except:
            employment_gaps = []

        return HRInsights(
            career_progression_summary=result.career_progression_summary,
            job_hopping_flag=result.job_hopping_flag,
            employment_gaps=employment_gaps,
            overqualification_flag=result.overqualification_flag,
            underqualification_flag=result.underqualification_flag,
            formatting_quality=result.formatting_quality,
            formatting_issues=[i.strip() for i in result.formatting_issues.split(",") if i.strip() and i != "none"],
            red_flags=[f.strip() for f in result.red_flags.split(",") if f.strip() and f != "none"],
            key_strengths=[s.strip() for s in result.key_strengths.split(",") if s.strip()],
            evidence_spans=[e.strip() for e in result.evidence_spans.split("|") if e.strip()]
        )
```

---

## 3. Configurable Evaluation Framework ⭐⭐⭐

### Problem
Matching quality depends on configurable criteria (skills match, experience match, etc.) with different weights per role/division.

### Solution
Build a **criteria-based evaluation framework** with configurable weights.

### Implementation

```python
# models/evaluation_criteria.py
from pydantic import BaseModel, Field
from typing import List, Optional

class CriterionConfig(BaseModel):
    """Configuration for one evaluation criterion"""
    name: str = Field(..., description="Name of the criterion")
    weight: float = Field(..., description="Weight of the criterion (0 to 1)", ge=0.0, le=1.0)
    description: str = Field(..., description="Description of what this criterion evaluates")

class MatchEvidence(BaseModel):
    """Evidence supporting a match evaluation"""
    cv_span: Optional[str] = Field(None, description="Snippet from CV supporting the match")
    jd_span: Optional[str] = Field(None, description="Snippet from JD that corresponds")
    reason: Optional[str] = Field(None, description="Explanation of why CV and JD spans are similar")
    impact: float = Field(..., description="Impact on overall score, -1 to 1")
    confidence: Optional[float] = Field(None, description="Confidence in this evidence, 0-1")

class EvaluationCriterion(BaseModel):
    """Result of evaluating one criterion"""
    name: str = Field(..., description="Name of the criterion")
    weight: float = Field(..., description="Weight used in scoring")
    score: int = Field(..., description="Score for this criterion, 0 to 100")
    explanation: Optional[str] = Field(None, description="Brief explanation of the score")
    recommendation: Optional[str] = Field(None, description="Recommendation given to the candidate")
    questions: Optional[List[str]] = Field(None, description="Questions to ask in interview")
    evidence: Optional[List[MatchEvidence]] = Field(None, description="Supporting evidence")
    confidence: Optional[float] = Field(None, description="Confidence in this evaluation, 0-1")

class CVJDEvaluation(BaseModel):
    """Complete CV-JD evaluation result"""
    overall_score: float = Field(..., description="Weighted score 0-100")
    pass_fail: bool = Field(..., description="Whether candidate meets minimum threshold")
    criteria_scores: List[EvaluationCriterion] = Field(..., description="Individual criterion scores")

    # Summary
    match_summary: Optional[str] = Field(None, description="2-3 sentence summary of the match")
    strengths: List[str] = Field(default_factory=list, description="Candidate strengths for this role")
    gaps: List[str] = Field(default_factory=list, description="Missing requirements or skill gaps")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for hiring manager")

    # Confidence
    extraction_confidence: float = Field(default=1.0, description="Confidence in CV extraction quality")
    matching_confidence: float = Field(default=1.0, description="Confidence in matching accuracy")
```

### DSPy Signatures for Matching with Evidence

```python
# dspy_modules/matching_signatures.py
import dspy

class SkillsMatchEvaluation(dspy.Signature):
    """Evaluate skills match between CV and JD with evidence"""

    # Input
    candidate_skills_json: str = dspy.InputField(desc="JSON array of candidate skills")
    required_skills_json: str = dspy.InputField(desc="JSON array of required skills from JD")
    cv_text: str = dspy.InputField(desc="Full CV text for context")
    jd_text: str = dspy.InputField(desc="Full JD text for context")

    # Output
    score: int = dspy.OutputField(desc="Score 0-100 for skills match")

    explanation: str = dspy.OutputField(
        desc="Brief explanation (≤80 words) of the score, based on evidence"
    )

    matched_skills: str = dspy.OutputField(
        desc="Comma-separated list of skills that match"
    )

    missing_skills: str = dspy.OutputField(
        desc="Comma-separated list of required skills the candidate lacks"
    )

    evidence_json: str = dspy.OutputField(
        desc="JSON array of match evidence with fields: cv_span, jd_span, reason, impact"
    )

    confidence: float = dspy.OutputField(desc="Confidence 0.0-1.0")

class ExperienceMatchEvaluation(dspy.Signature):
    """Evaluate experience match between CV and JD with evidence"""

    # Input
    candidate_experience_json: str = dspy.InputField(desc="JSON array of work experiences")
    required_experience_json: str = dspy.InputField(desc="JSON of experience requirements from JD")
    cv_text: str = dspy.InputField(desc="Full CV text")
    jd_text: str = dspy.InputField(desc="Full JD text")

    # Output
    score: int = dspy.OutputField(desc="Score 0-100 for experience match")

    explanation: str = dspy.OutputField(
        desc="Brief explanation (≤80 words) based on evidence"
    )

    years_of_experience: str = dspy.OutputField(desc="Total years of relevant experience")

    relevant_roles: str = dspy.OutputField(
        desc="Comma-separated list of roles relevant to JD"
    )

    experience_gaps: str = dspy.OutputField(
        desc="Comma-separated list of missing experience areas"
    )

    evidence_json: str = dspy.OutputField(
        desc="JSON array of evidence"
    )

    confidence: float = dspy.OutputField(desc="Confidence 0.0-1.0")

class OverallMatchEvaluation(dspy.Signature):
    """Overall CV-JD match evaluation with configurable criteria"""

    # Input
    cv_extract_json: str = dspy.InputField(desc="Structured CV data as JSON")
    jd_extract_json: str = dspy.InputField(desc="Structured JD data as JSON")
    criteria_config_json: str = dspy.InputField(desc="JSON array of CriterionConfig objects")
    cv_text: str = dspy.InputField(desc="Full CV text")
    jd_text: str = dspy.InputField(desc="Full JD text")

    # Output
    overall_score: float = dspy.OutputField(desc="Weighted overall score 0-100")

    pass_fail: bool = dspy.OutputField(desc="True if meets minimum threshold")

    match_summary: str = dspy.OutputField(
        desc="2-3 sentence summary of the match quality"
    )

    strengths: str = dspy.OutputField(
        desc="Pipe-separated list of candidate strengths for this role"
    )

    gaps: str = dspy.OutputField(
        desc="Pipe-separated list of missing requirements or skill gaps"
    )

    recommendations: str = dspy.OutputField(
        desc="Pipe-separated recommendations for hiring manager"
    )

    criteria_scores_json: str = dspy.OutputField(
        desc="JSON array of EvaluationCriterion objects with scores for each criterion"
    )
```

### Matching Module with Evidence

```python
# pipelines/matching_pipeline.py
import dspy
import json
from typing import List
from models.evaluation_criteria import CriterionConfig, CVJDEvaluation, EvaluationCriterion, MatchEvidence

class CVJDMatchingPipeline(dspy.Module):
    """Complete matching pipeline with evidence and configurable criteria"""

    def __init__(self):
        super().__init__()
        self.skills_matcher = dspy.ChainOfThought(SkillsMatchEvaluation)
        self.experience_matcher = dspy.ChainOfThought(ExperienceMatchEvaluation)
        self.overall_matcher = dspy.ChainOfThought(OverallMatchEvaluation)

    def forward(
        self,
        cv_data: dict,
        jd_data: dict,
        criteria_config: List[CriterionConfig],
        cv_text: str,
        jd_text: str,
        threshold: float = 60.0
    ) -> CVJDEvaluation:
        """
        Match CV against JD with configurable criteria

        Args:
            cv_data: Structured CV data (dict)
            jd_data: Structured JD data (dict)
            criteria_config: List of evaluation criteria with weights
            cv_text: Original CV text
            jd_text: Original JD text
            threshold: Minimum score to pass (default 60.0)

        Returns:
            CVJDEvaluation with scores, evidence, and recommendations
        """

        # Serialize to JSON for DSPy
        cv_json = json.dumps(cv_data)
        jd_json = json.dumps(jd_data)
        criteria_json = json.dumps([c.dict() for c in criteria_config])

        # Run overall matching
        result = self.overall_matcher(
            cv_extract_json=cv_json,
            jd_extract_json=jd_json,
            criteria_config_json=criteria_json,
            cv_text=cv_text,
            jd_text=jd_text
        )

        # Parse criteria scores
        try:
            criteria_scores_data = json.loads(result.criteria_scores_json)
            criteria_scores = [EvaluationCriterion(**c) for c in criteria_scores_data]
        except:
            criteria_scores = []

        # Create evaluation result
        evaluation = CVJDEvaluation(
            overall_score=result.overall_score,
            pass_fail=result.pass_fail,
            criteria_scores=criteria_scores,
            match_summary=result.match_summary,
            strengths=[s.strip() for s in result.strengths.split("|") if s.strip()],
            gaps=[g.strip() for g in result.gaps.split("|") if g.strip()],
            recommendations=[r.strip() for r in result.recommendations.split("|") if r.strip()]
        )

        return evaluation
```

---

## 4. Strict Extract Mode Pattern ⭐⭐

### Problem
LLMs sometimes hallucinate or infer information not present in the CV.

### Solution
Add a **strict_extract_only** flag that prevents inference and returns nulls for missing data.

### Implementation

```python
# All signatures should include:
class AnyExtraction(dspy.Signature):
    """..."""
    cv_text: str = dspy.InputField(...)
    strict_extract_only: bool = dspy.InputField(
        desc="If true, do not infer unknowns; return nulls/empties.",
        default=False
    )
    # ... outputs

# Usage:
extractor = CVExtractor()

# Lenient mode (default): Allow inference
profile = extractor(cv_text=text, strict_extract_only=False)

# Strict mode: No inference, only explicit facts
profile = extractor(cv_text=text, strict_extract_only=True)
```

### Why This Matters
- **Lenient mode**: Good for incomplete CVs, helps fill gaps
- **Strict mode**: Good for compliance/regulatory roles where accuracy > completeness
- **Division-specific**: Legal/Finance might use strict, Tech might use lenient

---

## 5. Granular Type System Pattern ⭐⭐

### Problem
Monolithic extraction signatures are hard to optimize and debug.

### Solution
Create **fine-grained DSPy signatures** for each data type.

### Implementation

```python
# Instead of one big signature, break down into:

class DateRange(dspy.Signature):
    """Extract a date range"""
    text: str = dspy.InputField()
    start: str = dspy.OutputField(desc="YYYY-MM format")
    end: str = dspy.OutputField(desc="YYYY-MM or 'Present'")

class Location(dspy.Signature):
    """Extract location"""
    text: str = dspy.InputField()
    city: str = dspy.OutputField(default=None)
    country_code: str = dspy.OutputField(desc="ISO 3166-1 alpha-2", default=None)

class SkillItem(dspy.Signature):
    """Extract one skill with metadata"""
    text: str = dspy.InputField()
    name: str = dspy.OutputField()
    category: str = dspy.OutputField()
    proficiency: str = dspy.OutputField()
    years_experience: float = dspy.OutputField()

# Then compose them:
class Experience(dspy.Signature):
    """Extract one work experience"""
    text: str = dspy.InputField()

    title: str = dspy.OutputField()
    company: str = dspy.OutputField()
    dates: DateRange = dspy.OutputField()
    location: Location = dspy.OutputField()
    responsibilities: List[str] = dspy.OutputField()
```

### Benefits
- Each signature optimized independently
- Easier debugging (know exactly which part failed)
- Reusable components across CV and JD extraction
- Better teleprompter optimization

---

## 6. Integration: Complete Enhanced Pipeline

```python
# pipelines/enhanced_cv_extraction.py
import dspy
from typing import Optional, List
from models.cv_schema import CandidateProfile
from models.evidence_field import EvidenceField, EvidenceSkill
from models.hr_insights import HRInsights, QualityScore
from dspy_modules.evidence_extractors import PersonalInfoExtractorWithEvidence
from dspy_modules.hr_insights_signature import HRInsightsModule

class EnhancedCVExtractionPipeline(dspy.Module):
    """
    Production-grade CV extraction with:
    - Evidence-based extraction
    - HR insights
    - Quality scoring
    - Strict mode support
    """

    def __init__(self):
        super().__init__()

        # Evidence-based extractors
        self.personal_extractor = PersonalInfoExtractorWithEvidence()
        # ... other extractors

        # HR insights
        self.hr_analyzer = HRInsightsModule()

        # Quality scorer
        self.quality_scorer = CVQualityScorer()

    def forward(
        self,
        cv_text: str,
        strict_mode: bool = False,
        include_hr_insights: bool = True,
        include_quality_score: bool = True
    ) -> dict:
        """
        Extract CV with evidence and insights

        Args:
            cv_text: Raw CV text
            strict_mode: If True, no inference allowed
            include_hr_insights: Include HR analysis
            include_quality_score: Include quality assessment

        Returns:
            dict with:
                - candidate_profile: CandidateProfile
                - hr_insights: HRInsights (if requested)
                - quality_score: QualityScore (if requested)
                - extraction_metadata: timestamps, confidence, etc.
        """

        # Stage 1: Evidence-based extraction
        print("Stage 1: Extracting with evidence...")
        personal_info = self.personal_extractor(cv_text=cv_text, strict_mode=strict_mode)
        # ... extract other sections with evidence

        # Stage 2: HR Insights (optional)
        hr_insights = None
        if include_hr_insights:
            print("Stage 2: Generating HR insights...")
            hr_insights = self.hr_analyzer(
                work_experiences=work_experiences,
                education=educations,
                skills=skills,
                full_cv_text=cv_text
            )

        # Stage 3: Quality Scoring (optional)
        quality_score = None
        if include_quality_score:
            print("Stage 3: Calculating quality score...")
            quality_score = self.quality_scorer(
                candidate_profile=candidate_profile,
                cv_text=cv_text
            )

        # Return comprehensive result
        return {
            "candidate_profile": candidate_profile,
            "hr_insights": hr_insights,
            "quality_score": quality_score,
            "extraction_metadata": {
                "timestamp": datetime.now().isoformat(),
                "strict_mode": strict_mode,
                "processing_time_seconds": processing_time,
                "average_confidence": avg_confidence
            }
        }
```

---

## 7. Configuration Per Division

```python
# config/division_extraction_config.py
from typing import Dict

DIVISION_EXTRACTION_CONFIG: Dict[str, dict] = {
    "insurance_operations": {
        "strict_mode": True,  # High accuracy required
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["certifications", "regulatory_knowledge", "premium_volume"],
        "quality_threshold": 80.0
    },

    "technology": {
        "strict_mode": False,  # Allow inference for skills
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["technical_skills", "github_profile", "open_source"],
        "quality_threshold": 70.0
    },

    "legal": {
        "strict_mode": True,  # Critical accuracy
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["bar_admission", "practice_areas", "notable_cases"],
        "quality_threshold": 85.0
    },

    # ... other divisions
}

def get_extraction_config(division: str) -> dict:
    """Get extraction configuration for division"""
    return DIVISION_EXTRACTION_CONFIG.get(
        division,
        {  # Default config
            "strict_mode": False,
            "evidence_required": True,
            "hr_insights": True,
            "quality_threshold": 75.0
        }
    )
```

---

## 8. Usage Examples

### Example 1: Extract with Evidence

```python
from pipelines.enhanced_cv_extraction import EnhancedCVExtractionPipeline

# Initialize
pipeline = EnhancedCVExtractionPipeline()

# Extract with evidence
result = pipeline(
    cv_text=cv_text,
    strict_mode=False,
    include_hr_insights=True,
    include_quality_score=True
)

# Access evidence
personal_info = result["candidate_profile"].personal_info
print(f"Name: {personal_info.name.value}")
print(f"Confidence: {personal_info.name.confidence}")
print(f"Evidence: {personal_info.name.evidence_spans}")

# Access HR insights
insights = result["hr_insights"]
print(f"Career Summary: {insights.career_progression_summary}")
print(f"Red Flags: {insights.red_flags}")
print(f"Key Strengths: {insights.key_strengths}")

# Access quality score
quality = result["quality_score"]
print(f"Overall Quality: {quality.overall_score}/100 ({quality.grade})")
```

### Example 2: Division-Specific Extraction

```python
from config.division_extraction_config import get_extraction_config

# Get config for division
division = "legal"
config = get_extraction_config(division)

# Extract with division config
result = pipeline(
    cv_text=cv_text,
    strict_mode=config["strict_mode"],
    include_hr_insights=config["hr_insights"]
)

# Validate quality threshold
if result["quality_score"].overall_score < config["quality_threshold"]:
    print(f"⚠️  CV quality below threshold for {division} division")
```

### Example 3: Matching with Evidence

```python
from pipelines.matching_pipeline import CVJDMatchingPipeline
from models.evaluation_criteria import CriterionConfig

# Define criteria for this role
criteria = [
    CriterionConfig(name="Skills Match", weight=0.40, description="Technical skills alignment"),
    CriterionConfig(name="Experience Match", weight=0.30, description="Years and relevance"),
    CriterionConfig(name="Education Match", weight=0.15, description="Degree requirements"),
    CriterionConfig(name="Certifications", weight=0.15, description="Required certifications")
]

# Match with evidence
matcher = CVJDMatchingPipeline()
evaluation = matcher(
    cv_data=cv_data,
    jd_data=jd_data,
    criteria_config=criteria,
    cv_text=cv_text,
    jd_text=jd_text,
    threshold=60.0
)

# Review results
print(f"Overall Score: {evaluation.overall_score}/100")
print(f"Pass/Fail: {'PASS' if evaluation.pass_fail else 'FAIL'}")
print(f"\nMatch Summary:\n{evaluation.match_summary}")

print(f"\nStrengths:")
for strength in evaluation.strengths:
    print(f"  ✓ {strength}")

print(f"\nGaps:")
for gap in evaluation.gaps:
    print(f"  ✗ {gap}")

# Review evidence for each criterion
for criterion in evaluation.criteria_scores:
    print(f"\n{criterion.name}: {criterion.score}/100 (weight: {criterion.weight})")
    print(f"  {criterion.explanation}")
    if criterion.evidence:
        print(f"  Evidence:")
        for ev in criterion.evidence[:3]:  # Show top 3
            print(f"    CV: {ev.cv_span}")
            print(f"    JD: {ev.jd_span}")
            print(f"    Impact: {ev.impact:+.2f}")
```

---

## Summary: Key Improvements

| Pattern | Benefit | Priority |
|---------|---------|----------|
| **Evidence-Based Extraction** | Explainability, verification, debugging | ⭐⭐⭐ Critical |
| **HR Insights Layer** | Recruiter value-add, red flag detection | ⭐⭐⭐ Critical |
| **Configurable Evaluation** | Flexible matching, division-specific criteria | ⭐⭐⭐ Critical |
| **Strict Extract Mode** | Prevent hallucination, compliance-ready | ⭐⭐ Important |
| **Granular Type System** | Better optimization, easier debugging | ⭐⭐ Important |
| **Quality Scoring** | Filter low-quality CVs, improve UX | ⭐⭐ Important |

---

## Next Steps

1. ✅ Review these patterns
2. ⏳ Decide which patterns to integrate first (suggest: Evidence + HR Insights)
3. ⏳ Update existing signatures with evidence fields
4. ⏳ Implement HR Insights module
5. ⏳ Build evaluation framework with configurable criteria
6. ⏳ Test with sample CVs/JDs
7. ⏳ Optimize with teleprompters

**These patterns will make your extraction pipeline production-grade and enterprise-ready!** 🚀
