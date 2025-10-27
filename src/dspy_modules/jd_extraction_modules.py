"""
DSPy modules for Job Description (JD) extraction.

Modules that use JD signatures to extract and structure job requirements.
"""

import dspy
from typing import List, Dict, Any, Optional
from datetime import datetime

from .jd_signatures import (
    RoleInfoExtraction,
    LocationInfoExtraction,
    RequiredSkillsExtraction,
    SkillRequirementWithPriority,
    ComprehensiveSkillsExtraction,
    ExperienceRequirementsExtraction,
    EducationRequirementsExtraction,
    CertificationRequirementsExtraction,
    ResponsibilitiesExtraction,
    ResponsibilityPrioritization,
    CompensationExtraction,
    CompanyCultureExtraction,
    ApplicationInfoExtraction,
    JDDivisionClassification,
    RequirementsPriorityScoring,
    DisqualifiersExtraction,
    IdealCandidateProfile,
    JDQualityAssessment,
    MatchingWeightRecommendation,
    StrictRequirementExtraction,
    JDKeywordExtraction,
)


# ============================================================================
# ROLE INFORMATION MODULE
# ============================================================================

class RoleInfoExtractor(dspy.Module):
    """Extract basic role information."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(RoleInfoExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract role information."""
        return self.extractor(jd_text=jd_text)


# ============================================================================
# LOCATION MODULE
# ============================================================================

class LocationInfoExtractor(dspy.Module):
    """Extract location and work arrangement."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(LocationInfoExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract location info."""
        return self.extractor(jd_text=jd_text)


# ============================================================================
# SKILLS REQUIREMENTS MODULES
# ============================================================================

class RequiredSkillsExtractor(dspy.Module):
    """Extract required and preferred skills."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(RequiredSkillsExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract required skills."""
        return self.extractor(jd_text=jd_text)


class ComprehensiveSkillsExtractor(dspy.Module):
    """Extract comprehensive skills breakdown."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(ComprehensiveSkillsExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract all skill categories."""
        return self.extractor(jd_text=jd_text)


class SkillRequirementClassifier(dspy.Module):
    """Classify individual skill requirement with priority."""

    def __init__(self):
        super().__init__()
        self.classifier = dspy.ChainOfThought(SkillRequirementWithPriority)

    def forward(self, jd_text: str, target_skill: str) -> dspy.Prediction:
        """Classify skill requirement priority."""
        return self.classifier(jd_text=jd_text, target_skill=target_skill)


class BatchSkillRequirementClassifier(dspy.Module):
    """Classify multiple skills at once."""

    def __init__(self):
        super().__init__()
        self.single_classifier = SkillRequirementClassifier()

    def forward(self, jd_text: str, target_skills: List[str]) -> Dict[str, dspy.Prediction]:
        """Classify multiple skills."""
        results = {}
        for skill in target_skills:
            results[skill] = self.single_classifier(jd_text=jd_text, target_skill=skill)
        return results


# ============================================================================
# REQUIREMENTS MODULES
# ============================================================================

class ExperienceRequirementsExtractor(dspy.Module):
    """Extract experience requirements."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(ExperienceRequirementsExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract experience requirements."""
        return self.extractor(jd_text=jd_text)


class EducationRequirementsExtractor(dspy.Module):
    """Extract education requirements."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(EducationRequirementsExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract education requirements."""
        return self.extractor(jd_text=jd_text)


class CertificationRequirementsExtractor(dspy.Module):
    """Extract certification requirements."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(CertificationRequirementsExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract certification requirements."""
        return self.extractor(jd_text=jd_text)


class DisqualifiersExtractor(dspy.Module):
    """Extract disqualifying factors."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(DisqualifiersExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract disqualifiers."""
        return self.extractor(jd_text=jd_text)


# ============================================================================
# RESPONSIBILITIES MODULE
# ============================================================================

class ResponsibilitiesExtractor(dspy.Module):
    """Extract responsibilities and duties."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(ResponsibilitiesExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract responsibilities."""
        return self.extractor(jd_text=jd_text)


class ResponsibilityPrioritizer(dspy.Module):
    """Prioritize responsibilities."""

    def __init__(self):
        super().__init__()
        self.prioritizer = dspy.ChainOfThought(ResponsibilityPrioritization)

    def forward(self, responsibilities_text: str) -> dspy.Prediction:
        """Prioritize responsibilities."""
        return self.prioritizer(responsibilities_text=responsibilities_text)


# ============================================================================
# COMPENSATION MODULE
# ============================================================================

class CompensationExtractor(dspy.Module):
    """Extract compensation and benefits."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(CompensationExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract compensation info."""
        return self.extractor(jd_text=jd_text)


# ============================================================================
# CULTURE MODULE
# ============================================================================

class CompanyCultureExtractor(dspy.Module):
    """Extract company culture information."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(CompanyCultureExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract culture info."""
        return self.extractor(jd_text=jd_text)


# ============================================================================
# APPLICATION MODULE
# ============================================================================

class ApplicationInfoExtractor(dspy.Module):
    """Extract application process information."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(ApplicationInfoExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract application info."""
        return self.extractor(jd_text=jd_text)


# ============================================================================
# DIVISION CLASSIFICATION MODULE
# ============================================================================

class JDDivisionClassifier(dspy.Module):
    """Classify JD to AIA business divisions."""

    def __init__(self):
        super().__init__()
        self.classifier = dspy.ChainOfThought(JDDivisionClassification)

    def forward(
        self,
        job_title: str,
        responsibilities_summary: str,
        required_skills: str,
        available_divisions: str,
    ) -> dspy.Prediction:
        """Classify JD to division."""
        return self.classifier(
            job_title=job_title,
            responsibilities_summary=responsibilities_summary,
            required_skills=required_skills,
            available_divisions=available_divisions,
        )


# ============================================================================
# ANALYSIS MODULES
# ============================================================================

class RequirementsPriorityScorer(dspy.Module):
    """Score importance of different requirement categories."""

    def __init__(self):
        super().__init__()
        self.scorer = dspy.ChainOfThought(RequirementsPriorityScoring)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Score requirement priorities."""
        return self.scorer(jd_text=jd_text)


class IdealCandidateProfileGenerator(dspy.Module):
    """Generate ideal candidate profile from JD."""

    def __init__(self):
        super().__init__()
        self.generator = dspy.ChainOfThought(IdealCandidateProfile)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Generate ideal candidate profile."""
        return self.generator(jd_text=jd_text)


class JDQualityAssessor(dspy.Module):
    """Assess JD quality and completeness."""

    def __init__(self):
        super().__init__()
        self.assessor = dspy.ChainOfThought(JDQualityAssessment)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Assess JD quality."""
        return self.assessor(jd_text=jd_text)


class MatchingWeightRecommender(dspy.Module):
    """Recommend matching weights for this JD."""

    def __init__(self):
        super().__init__()
        self.recommender = dspy.ChainOfThought(MatchingWeightRecommendation)

    def forward(
        self,
        jd_summary: str,
        experience_level: str,
        division: str,
    ) -> dspy.Prediction:
        """Recommend matching weights."""
        return self.recommender(
            jd_summary=jd_summary,
            experience_level=experience_level,
            division=division,
        )


# ============================================================================
# KEYWORD EXTRACTION MODULE
# ============================================================================

class JDKeywordExtractor(dspy.Module):
    """Extract critical keywords for matching."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(JDKeywordExtraction)

    def forward(self, jd_text: str) -> dspy.Prediction:
        """Extract keywords."""
        return self.extractor(jd_text=jd_text)


# ============================================================================
# STRICT MODE MODULE
# ============================================================================

class StrictRequirementExtractor(dspy.Module):
    """Extract requirements in strict mode (no inference)."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(StrictRequirementExtraction)

    def forward(
        self,
        jd_text: str,
        requirement_type: str,
    ) -> dspy.Prediction:
        """Extract requirements strictly."""
        # Instructions are now in the signature's docstring
        return self.extractor(
            jd_text=jd_text,
            requirement_type=requirement_type,
        )


# ============================================================================
# COMPOSITE MODULE
# ============================================================================

class ComprehensiveJDExtractor(dspy.Module):
    """
    Comprehensive JD extractor that orchestrates all extraction modules.

    This is a high-level module that coordinates extraction of all JD components.
    """

    def __init__(
        self,
        with_analysis: bool = True,
        strict_mode: bool = False,
    ):
        super().__init__()

        # Initialize core extractors
        self.role_extractor = RoleInfoExtractor()
        self.location_extractor = LocationInfoExtractor()
        self.skills_extractor = ComprehensiveSkillsExtractor()
        self.required_skills_extractor = RequiredSkillsExtractor()
        self.experience_extractor = ExperienceRequirementsExtractor()
        self.education_extractor = EducationRequirementsExtractor()
        self.certification_extractor = CertificationRequirementsExtractor()
        self.responsibilities_extractor = ResponsibilitiesExtractor()
        self.responsibility_prioritizer = ResponsibilityPrioritizer()
        self.compensation_extractor = CompensationExtractor()
        self.culture_extractor = CompanyCultureExtractor()
        self.application_extractor = ApplicationInfoExtractor()
        self.division_classifier = JDDivisionClassifier()
        self.disqualifiers_extractor = DisqualifiersExtractor()

        # Analysis modules (optional)
        self.with_analysis = with_analysis
        if with_analysis:
            self.priority_scorer = RequirementsPriorityScorer()
            self.ideal_profile_generator = IdealCandidateProfileGenerator()
            self.quality_assessor = JDQualityAssessor()
            self.weight_recommender = MatchingWeightRecommender()
            self.keyword_extractor = JDKeywordExtractor()

        # Strict mode
        self.strict_mode = strict_mode
        if strict_mode:
            self.strict_extractor = StrictRequirementExtractor()

    def forward(
        self,
        jd_text: str,
        available_divisions: str = "technology,insurance_operations,finance,hr,legal",
    ) -> Dict[str, Any]:
        """
        Extract all information from JD.

        Args:
            jd_text: Full job description text
            available_divisions: Comma-separated division options

        Returns:
            Dictionary with all extracted information
        """
        results = {}

        # Step 1: Extract role information
        role_info = self.role_extractor(jd_text=jd_text)
        results["role_info"] = role_info

        # Step 2: Extract location and arrangement
        location_info = self.location_extractor(jd_text=jd_text)
        results["location_info"] = location_info

        # Step 3: Extract skills
        skills = self.skills_extractor(jd_text=jd_text)
        results["skills"] = skills

        required_skills = self.required_skills_extractor(jd_text=jd_text)
        results["required_skills"] = required_skills

        # Step 4: Extract requirements
        experience_req = self.experience_extractor(jd_text=jd_text)
        results["experience_requirements"] = experience_req

        education_req = self.education_extractor(jd_text=jd_text)
        results["education_requirements"] = education_req

        certification_req = self.certification_extractor(jd_text=jd_text)
        results["certification_requirements"] = certification_req

        disqualifiers = self.disqualifiers_extractor(jd_text=jd_text)
        results["disqualifiers"] = disqualifiers

        # Step 5: Extract responsibilities
        responsibilities = self.responsibilities_extractor(jd_text=jd_text)
        results["responsibilities"] = responsibilities

        # Prioritize responsibilities
        resp_text = f"{responsibilities.core_responsibilities if hasattr(responsibilities, 'core_responsibilities') else ''}"
        if resp_text:
            resp_priority = self.responsibility_prioritizer(responsibilities_text=resp_text)
            results["responsibilities_priority"] = resp_priority

        # Step 6: Extract compensation
        compensation = self.compensation_extractor(jd_text=jd_text)
        results["compensation"] = compensation

        # Step 7: Extract culture
        culture = self.culture_extractor(jd_text=jd_text)
        results["culture"] = culture

        # Step 8: Extract application info
        application = self.application_extractor(jd_text=jd_text)
        results["application"] = application

        # Step 9: Division classification
        job_title = role_info.job_title if hasattr(role_info, 'job_title') else "Unknown"
        resp_summary = responsibilities.core_responsibilities if hasattr(responsibilities, 'core_responsibilities') else ""
        skills_summary = required_skills.required_technical_skills if hasattr(required_skills, 'required_technical_skills') else ""

        division = self.division_classifier(
            job_title=job_title,
            responsibilities_summary=resp_summary,
            required_skills=skills_summary,
            available_divisions=available_divisions,
        )
        results["division"] = division

        # Step 10: Analysis (if enabled)
        if self.with_analysis:
            # Priority scoring
            priority_scores = self.priority_scorer(jd_text=jd_text)
            results["priority_scores"] = priority_scores

            # Ideal candidate profile
            ideal_profile = self.ideal_profile_generator(jd_text=jd_text)
            results["ideal_profile"] = ideal_profile

            # Quality assessment
            quality = self.quality_assessor(jd_text=jd_text)
            results["quality_assessment"] = quality

            # Matching weights recommendation
            jd_summary = f"{job_title} | {resp_summary[:200]}"
            exp_level = role_info.experience_level if hasattr(role_info, 'experience_level') else "Mid"
            div = division.primary_division if hasattr(division, 'primary_division') else "general"

            weights = self.weight_recommender(
                jd_summary=jd_summary,
                experience_level=exp_level,
                division=div,
            )
            results["recommended_weights"] = weights

            # Keyword extraction
            keywords = self.keyword_extractor(jd_text=jd_text)
            results["keywords"] = keywords

        # Step 11: Strict extraction (if enabled)
        if self.strict_mode:
            strict_results = {}
            for req_type in ["skills", "education", "experience", "certifications"]:
                strict_result = self.strict_extractor(
                    jd_text=jd_text,
                    requirement_type=req_type,
                )
                strict_results[req_type] = strict_result
            results["strict_extraction"] = strict_results

        # Add metadata
        results["extraction_metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "with_analysis": self.with_analysis,
            "strict_mode": self.strict_mode,
        }

        return results


# ============================================================================
# SPECIALIZED MODULES
# ============================================================================

class DivisionSpecificJDExtractor(dspy.Module):
    """
    Division-specific JD extractor with customized extraction logic.

    Extends ComprehensiveJDExtractor with division-specific behaviors.
    """

    def __init__(
        self,
        division: str,
        division_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()

        self.division = division
        self.division_config = division_config or {}

        # Use comprehensive extractor as base
        self.base_extractor = ComprehensiveJDExtractor(
            with_analysis=True,
            strict_mode=self.division_config.get("strict_mode", False),
        )

    def forward(self, jd_text: str) -> Dict[str, Any]:
        """Extract with division-specific logic."""

        # Use base extractor
        results = self.base_extractor(jd_text=jd_text)

        # Add division-specific metadata
        results["division_specific"] = {
            "division": self.division,
            "config_applied": self.division_config,
        }

        return results
