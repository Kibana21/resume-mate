"""
DSPy modules for CV extraction.

Modules are composable components that use signatures to perform extraction tasks.
They can be optimized using DSPy teleprompters for better performance.
"""

import logging
import dspy
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

from .cv_signatures import (
    PersonalInfoExtraction,
    ProfessionalSummaryExtraction,
    WorkExperienceExtraction,
    WorkExperienceWithEvidence,
    WorkExperienceListExtraction,
    EducationExtraction,
    EducationWithEvidence,
    EducationListExtraction,
    TechnicalSkillsExtraction,
    SkillsWithProficiency,
    DomainSkillsExtraction,
    SkillWithEvidenceExtraction,
    CertificationExtraction,
    CertificationListExtraction,
    DivisionClassification,
    CareerProgressionAnalysis,
    JobHoppingDetection,
    RedFlagDetection,
    QualityScoring,
    KeyStrengthsExtraction,
    TotalExperienceCalculation,
    CVSectionDetection,
    StrictPersonalInfoExtraction,
    StrictSkillExtraction,
)
from .achievement_extraction import ComprehensiveAchievementAnalyzer
from .skill_proficiency import ComprehensiveSkillProficiencyAnalyzer


# ============================================================================
# PERSONAL INFORMATION MODULE
# ============================================================================

class PersonalInfoExtractor(dspy.Module):
    """Extract personal and contact information from CV."""

    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self.strict_mode = strict_mode

        if strict_mode:
            self.extractor = dspy.ChainOfThought(StrictPersonalInfoExtraction)
        else:
            self.extractor = dspy.ChainOfThought(PersonalInfoExtraction)

    def forward(self, personal_section: str) -> dspy.Prediction:
        """
        Extract personal information.

        Args:
            personal_section: Text containing personal information

        Returns:
            Prediction with extracted personal info fields
        """
        # Instructions are now in the signature's docstring
        return self.extractor(personal_section=personal_section)


class ProfessionalSummaryExtractor(dspy.Module):
    """Extract and refine professional summary."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(ProfessionalSummaryExtraction)

    def forward(self, summary_section: str) -> dspy.Prediction:
        """Extract professional summary."""
        return self.extractor(summary_section=summary_section)


# ============================================================================
# WORK EXPERIENCE MODULE
# ============================================================================

class WorkExperienceExtractor(dspy.Module):
    """Extract work experience entries."""

    def __init__(self, with_evidence: bool = False):
        super().__init__()
        self.with_evidence = with_evidence

        if with_evidence:
            self.extractor = dspy.ChainOfThought(WorkExperienceWithEvidence)
        else:
            self.extractor = dspy.ChainOfThought(WorkExperienceExtraction)

    def forward(self, experience_text: str) -> dspy.Prediction:
        """
        Extract single work experience entry.

        Args:
            experience_text: Text of one work experience entry

        Returns:
            Prediction with extracted work experience fields
        """
        return self.extractor(experience_text=experience_text)


class BatchWorkExperienceExtractor(dspy.Module):
    """Extract multiple work experience entries."""

    def __init__(self, with_evidence: bool = False):
        super().__init__()
        self.single_extractor = WorkExperienceExtractor(with_evidence=with_evidence)

    def forward(self, experience_entries: List[str]) -> List[dspy.Prediction]:
        """
        Extract multiple work experiences.

        Args:
            experience_entries: List of work experience text blocks

        Returns:
            List of predictions for each entry
        """
        results = []
        for entry in experience_entries:
            result = self.single_extractor(experience_text=entry)
            results.append(result)
        return results


class WorkExperienceListExtractor(dspy.Module):
    """Extract ALL work experience entries from full CV text using Pydantic models."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(WorkExperienceListExtraction)

    def forward(self, cv_text: str) -> dspy.Prediction:
        """
        Extract all work experience from full CV text.

        Args:
            cv_text: Full CV text

        Returns:
            DSPy Prediction with work_experiences attribute (List[WorkExperience])
        """
        result = self.extractor(cv_text=cv_text)
        return result


# ============================================================================
# EDUCATION MODULE
# ============================================================================

class EducationExtractor(dspy.Module):
    """Extract education entries."""

    def __init__(self, with_evidence: bool = False):
        super().__init__()
        self.with_evidence = with_evidence

        if with_evidence:
            self.extractor = dspy.ChainOfThought(EducationWithEvidence)
        else:
            self.extractor = dspy.ChainOfThought(EducationExtraction)

    def forward(self, education_text: str) -> dspy.Prediction:
        """Extract single education entry."""
        return self.extractor(education_text=education_text)


class BatchEducationExtractor(dspy.Module):
    """Extract multiple education entries."""

    def __init__(self, with_evidence: bool = False):
        super().__init__()
        self.single_extractor = EducationExtractor(with_evidence=with_evidence)

    def forward(self, education_entries: List[str]) -> List[dspy.Prediction]:
        """Extract multiple education entries."""
        results = []
        for entry in education_entries:
            result = self.single_extractor(education_text=entry)
            results.append(result)
        return results


class EducationListExtractor(dspy.Module):
    """Extract ALL education entries from full CV text."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(EducationListExtraction)

    def forward(self, cv_text: str) -> List[Dict[str, Any]]:
        """
        Extract all education from full CV text.

        Args:
            cv_text: Full CV text

        Returns:
            List of education dictionaries
        """
        import json

        result = self.extractor(cv_text=cv_text)

        # Parse JSON output
        try:
            education_entries = json.loads(result.education_entries_json)
            if not isinstance(education_entries, list):
                return []
            return education_entries
        except json.JSONDecodeError:
            # Try to extract JSON from the text
            import re
            json_match = re.search(r'\[.*\]', result.education_entries_json, re.DOTALL)
            if json_match:
                try:
                    education_entries = json.loads(json_match.group())
                    if isinstance(education_entries, list):
                        return education_entries
                except json.JSONDecodeError:
                    pass
            return []


# ============================================================================
# SKILLS MODULE
# ============================================================================

class TechnicalSkillsExtractor(dspy.Module):
    """Extract technical skills."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(TechnicalSkillsExtraction)

    def forward(self, skills_section: str) -> dspy.Prediction:
        """Extract technical skills."""
        return self.extractor(skills_section=skills_section)


class SkillsWithProficiencyExtractor(dspy.Module):
    """Extract skills with proficiency levels."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(SkillsWithProficiency)

    def forward(self, skills_text: str) -> dspy.Prediction:
        """Extract skills categorized by proficiency."""
        return self.extractor(skills_text=skills_text)


class DomainSkillsExtractor(dspy.Module):
    """Extract domain-specific skills."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(DomainSkillsExtraction)

    def forward(self, cv_text: str, industry_domain: str) -> dspy.Prediction:
        """Extract domain-specific skills."""
        return self.extractor(cv_text=cv_text, industry_domain=industry_domain)


class SkillVerifier(dspy.Module):
    """Verify if candidate has a specific skill with evidence."""

    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self.strict_mode = strict_mode

        if strict_mode:
            self.verifier = dspy.ChainOfThought(StrictSkillExtraction)
        else:
            self.verifier = dspy.ChainOfThought(SkillWithEvidenceExtraction)

    def forward(self, cv_text: str, target_skill: str) -> dspy.Prediction:
        """Verify if candidate has specific skill."""
        # Instructions are now in the signature's docstring
        return self.verifier(cv_text=cv_text, target_skill=target_skill)


class BatchSkillVerifier(dspy.Module):
    """Verify multiple skills at once."""

    def __init__(self, strict_mode: bool = False):
        super().__init__()
        self.single_verifier = SkillVerifier(strict_mode=strict_mode)

    def forward(self, cv_text: str, target_skills: List[str]) -> Dict[str, dspy.Prediction]:
        """Verify multiple skills."""
        results = {}
        for skill in target_skills:
            results[skill] = self.single_verifier(cv_text=cv_text, target_skill=skill)
        return results


# ============================================================================
# CERTIFICATIONS MODULE
# ============================================================================

class CertificationExtractor(dspy.Module):
    """Extract individual certification."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(CertificationExtraction)

    def forward(self, certification_text: str) -> dspy.Prediction:
        """Extract single certification."""
        return self.extractor(certification_text=certification_text)


class CertificationListExtractor(dspy.Module):
    """Extract all certifications from CV."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(CertificationListExtraction)

    def forward(self, cv_text: str) -> dspy.Prediction:
        """Extract all certifications."""
        return self.extractor(cv_text=cv_text)


# ============================================================================
# DIVISION CLASSIFICATION MODULE
# ============================================================================

class DivisionClassifier(dspy.Module):
    """Classify candidate to AIA business divisions."""

    def __init__(self):
        super().__init__()
        self.classifier = dspy.ChainOfThought(DivisionClassification)

    def forward(
        self,
        cv_summary: str,
        available_divisions: str
    ) -> dspy.Prediction:
        """Classify to divisions."""
        return self.classifier(
            cv_summary=cv_summary,
            available_divisions=available_divisions
        )


# ============================================================================
# HR INSIGHTS MODULES
# ============================================================================

class CareerProgressionAnalyzer(dspy.Module):
    """Analyze career progression patterns."""

    def __init__(self):
        super().__init__()
        self.analyzer = dspy.ChainOfThought(CareerProgressionAnalysis)

    def forward(self, work_history: str) -> dspy.Prediction:
        """Analyze career progression."""
        return self.analyzer(work_history=work_history)


class JobHoppingDetector(dspy.Module):
    """Detect job hopping and employment gaps."""

    def __init__(self):
        super().__init__()
        self.detector = dspy.ChainOfThought(JobHoppingDetection)

    def forward(self, work_history: str) -> dspy.Prediction:
        """Detect job hopping patterns."""
        return self.detector(work_history=work_history)


class RedFlagDetector(dspy.Module):
    """Detect potential red flags in CV."""

    def __init__(self):
        super().__init__()
        self.detector = dspy.ChainOfThought(RedFlagDetection)

    def forward(
        self,
        cv_content: str,
        work_history_summary: str
    ) -> dspy.Prediction:
        """Detect red flags."""
        return self.detector(
            cv_content=cv_content,
            work_history_summary=work_history_summary
        )


class QualityScorer(dspy.Module):
    """Score CV quality and completeness."""

    def __init__(self):
        super().__init__()
        self.scorer = dspy.ChainOfThought(QualityScoring)

    def forward(self, cv_text: str) -> dspy.Prediction:
        """Score CV quality."""
        return self.scorer(cv_text=cv_text)


class KeyStrengthsExtractor(dspy.Module):
    """Extract key strengths and unique selling points."""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(KeyStrengthsExtraction)

    def forward(
        self,
        cv_text: str,
        target_role_context: str = "General"
    ) -> dspy.Prediction:
        """Extract key strengths."""
        return self.extractor(
            cv_text=cv_text,
            target_role_context=target_role_context
        )


# ============================================================================
# EXPERIENCE CALCULATION MODULE
# ============================================================================

class TotalExperienceCalculator(dspy.Module):
    """Calculate total years of experience."""

    def __init__(self):
        super().__init__()
        self.calculator = dspy.ChainOfThought(TotalExperienceCalculation)

    def forward(self, work_history: str) -> dspy.Prediction:
        """Calculate total experience."""
        return self.calculator(work_history=work_history)


# ============================================================================
# SECTION DETECTION MODULE
# ============================================================================

class CVSectionDetector(dspy.Module):
    """Detect sections in CV."""

    def __init__(self):
        super().__init__()
        self.detector = dspy.ChainOfThought(CVSectionDetection)

    def forward(self, cv_text: str) -> dspy.Prediction:
        """Detect CV sections."""
        return self.detector(cv_text=cv_text)


# ============================================================================
# COMPOSITE MODULES
# ============================================================================

class ComprehensiveCVExtractor(dspy.Module):
    """
    Comprehensive CV extractor that orchestrates all extraction modules.

    This is a high-level module that coordinates extraction of all CV components.
    """

    def __init__(
        self,
        with_evidence: bool = False,
        with_hr_insights: bool = True,
        strict_mode: bool = False,
        industry_domain: Optional[str] = None,
    ):
        super().__init__()

        # Initialize sub-modules
        self.section_detector = CVSectionDetector()
        self.personal_info_extractor = PersonalInfoExtractor(strict_mode=strict_mode)
        self.summary_extractor = ProfessionalSummaryExtractor()
        self.work_exp_extractor = BatchWorkExperienceExtractor(with_evidence=with_evidence)
        self.work_exp_list_extractor = WorkExperienceListExtractor()
        self.education_extractor = BatchEducationExtractor(with_evidence=with_evidence)
        self.education_list_extractor = EducationListExtractor()
        self.technical_skills_extractor = TechnicalSkillsExtractor()
        self.skills_proficiency_extractor = SkillsWithProficiencyExtractor()
        self.certification_extractor = CertificationListExtractor()
        self.division_classifier = DivisionClassifier()
        self.experience_calculator = TotalExperienceCalculator()

        # HR Insights modules (optional)
        self.with_hr_insights = with_hr_insights
        if with_hr_insights:
            self.career_analyzer = CareerProgressionAnalyzer()
            self.job_hopping_detector = JobHoppingDetector()
            self.red_flag_detector = RedFlagDetector()
            self.quality_scorer = QualityScorer()
            self.strengths_extractor = KeyStrengthsExtractor()

        # Domain skills extractor (optional)
        self.industry_domain = industry_domain
        if industry_domain:
            self.domain_skills_extractor = DomainSkillsExtractor()

        # Achievement metrics extractor
        self.achievement_analyzer = ComprehensiveAchievementAnalyzer()

        # Skill proficiency analyzer
        self.skill_proficiency_analyzer = ComprehensiveSkillProficiencyAnalyzer()

    def forward(
        self,
        cv_text: str,
        personal_section: Optional[str] = None,
        summary_section: Optional[str] = None,
        work_entries: Optional[List[str]] = None,
        education_entries: Optional[List[str]] = None,
        skills_section: Optional[str] = None,
        available_divisions: str = "technology,insurance_operations,finance,hr,legal",
    ) -> Dict[str, Any]:
        """
        Extract all information from CV.

        Args:
            cv_text: Full CV text
            personal_section: Personal info section (if pre-split)
            summary_section: Summary section (if pre-split)
            work_entries: Work experience entries (if pre-split)
            education_entries: Education entries (if pre-split)
            skills_section: Skills section (if pre-split)
            available_divisions: Comma-separated division options

        Returns:
            Dictionary with all extracted information
        """
        results = {}

        # Step 1: Detect sections if not provided
        if not all([personal_section, work_entries, education_entries]):
            section_info = self.section_detector(cv_text=cv_text)
            results["sections_detected"] = section_info

        # Step 2: Extract personal information
        if personal_section:
            personal_info = self.personal_info_extractor(personal_section=personal_section)
        else:
            # Pass first 4000 chars to capture contact info that may appear later in document
            # (some CVs have contact info in footer, after work history, or embedded in content)
            personal_info = self.personal_info_extractor(personal_section=cv_text[:4000])
        results["personal_info"] = personal_info

        # Step 3: Extract professional summary
        if summary_section:
            summary = self.summary_extractor(summary_section=summary_section)
        else:
            # Use first 1000 chars
            summary = self.summary_extractor(summary_section=cv_text[:1000])
        results["professional_summary"] = summary

        # Step 4: Extract work experience
        if work_entries:
            work_exp = self.work_exp_extractor(experience_entries=work_entries)
            results["work_experience"] = work_exp
        else:
            # Use list extractor to find work experience from full CV (returns List[WorkExperience] directly)
            work_exp_result = self.work_exp_list_extractor(cv_text=cv_text)
            work_exp_list = getattr(work_exp_result, "work_experiences", [])
            results["work_experience"] = work_exp_list
            results["work_experience_raw"] = work_exp_list  # Store raw extraction

        # Step 4.5: Analyze achievement metrics from work experience
        achievement_metrics_by_exp = {}
        for i, exp in enumerate(results["work_experience"]):
            # Get achievements for this experience
            if isinstance(exp, dict):
                achievements = exp.get('achievements', [])
                company = exp.get('company_name', '')
                title = exp.get('job_title', '')
            else:
                achievements = getattr(exp, 'achievements', [])
                company = getattr(exp, 'company_name', '')
                title = getattr(exp, 'job_title', '')

            # Analyze achievements if present
            if achievements:
                try:
                    metrics = self.achievement_analyzer.analyze_achievements(
                        achievements=achievements,
                        company_name=company,
                        job_title=title
                    )
                    achievement_metrics_by_exp[i] = metrics
                except Exception as e:
                    # Log but don't fail extraction
                    logger.warning(f"Failed to analyze achievements: {e}")
                    achievement_metrics_by_exp[i] = []

        results["achievement_metrics"] = achievement_metrics_by_exp

        # Step 5: Extract education
        if education_entries:
            education = self.education_extractor(education_entries=education_entries)
            results["education"] = education
        else:
            # Use list extractor to find education from full CV
            education_list = self.education_list_extractor(cv_text=cv_text)
            results["education"] = education_list
            results["education_raw"] = education_list  # Store raw extraction

        # Step 6: Extract skills
        technical_skills = self.technical_skills_extractor(
            skills_section=skills_section or cv_text
        )
        results["technical_skills"] = technical_skills

        # Skills with proficiency
        skills_proficiency = self.skills_proficiency_extractor(
            skills_text=cv_text
        )
        results["skills_proficiency"] = skills_proficiency

        # Domain skills (if industry specified)
        if self.industry_domain:
            domain_skills = self.domain_skills_extractor(
                cv_text=cv_text,
                industry_domain=self.industry_domain
            )
            results["domain_skills"] = domain_skills

        # Step 7: Extract certifications
        certifications = self.certification_extractor(cv_text=cv_text)
        results["certifications"] = certifications

        # Step 8: Calculate experience
        # Create work history summary for calculation (handle both dict and object formats)
        work_history_entries = []
        for exp in results["work_experience"]:
            if isinstance(exp, dict):
                # Dict format from list extractor
                job_title = exp.get('job_title', 'Unknown')
                company = exp.get('company_name', 'Unknown')
                start = exp.get('start_date', 'Unknown')
                end = exp.get('end_date', 'Present')
                work_history_entries.append(f"{job_title} @ {company} ({start} - {end})")
            elif hasattr(exp, 'job_title'):
                # Object format from batch extractor
                work_history_entries.append(f"{exp.job_title} @ {exp.company_name} ({exp.start_date} - {exp.end_date})")

        work_history_summary = " | ".join(work_history_entries) if work_history_entries else cv_text[:1000]

        total_exp = self.experience_calculator(work_history=work_history_summary)
        results["total_experience"] = total_exp

        # Step 8.5: Analyze skill proficiency (after total experience is calculated)
        # Collect all skills into a flat list
        all_skills = set()

        # From technical skills (use correct field names from TechnicalSkillsExtraction signature)
        if hasattr(technical_skills, 'programming_languages'):
            langs = getattr(technical_skills, 'programming_languages', '')
            if langs and langs.lower() != 'none':
                all_skills.update([s.strip() for s in langs.split(',') if s.strip()])

        if hasattr(technical_skills, 'frameworks_libraries'):
            frameworks = getattr(technical_skills, 'frameworks_libraries', '')
            if frameworks and frameworks.lower() != 'none':
                all_skills.update([s.strip() for s in frameworks.split(',') if s.strip()])

        if hasattr(technical_skills, 'tools_platforms'):
            tools = getattr(technical_skills, 'tools_platforms', '')
            if tools and tools.lower() != 'none':
                all_skills.update([s.strip() for s in tools.split(',') if s.strip()])

        if hasattr(technical_skills, 'databases'):
            dbs = getattr(technical_skills, 'databases', '')
            if dbs and dbs.lower() != 'none':
                all_skills.update([s.strip() for s in dbs.split(',') if s.strip()])

        if hasattr(technical_skills, 'cloud_services'):
            cloud = getattr(technical_skills, 'cloud_services', '')
            if cloud and cloud.lower() != 'none':
                all_skills.update([s.strip() for s in cloud.split(',') if s.strip()])

        # Extract total years from total_exp result
        total_years = None
        if hasattr(total_exp, 'total_years'):
            try:
                total_years = float(getattr(total_exp, 'total_years', 0))
            except (ValueError, TypeError):
                total_years = None

        # Analyze proficiency for each skill
        if all_skills and results["work_experience"]:
            try:
                # Convert work experiences to dicts if they're dspy.Prediction objects
                work_exp_dicts = []
                for exp in results["work_experience"]:
                    if isinstance(exp, dict):
                        work_exp_dicts.append(exp)
                    else:
                        # Convert dspy.Prediction to dict
                        exp_dict = {
                            'company_name': getattr(exp, 'company_name', ''),
                            'job_title': getattr(exp, 'job_title', ''),
                            'start_date': getattr(exp, 'start_date', None),
                            'end_date': getattr(exp, 'end_date', None),
                            'technologies_used': getattr(exp, 'technologies_used', []),
                            'responsibilities': getattr(exp, 'responsibilities', [])
                        }
                        work_exp_dicts.append(exp_dict)

                skill_proficiency_analysis = self.skill_proficiency_analyzer.analyze_skills(
                    skills=list(all_skills),
                    work_experiences=work_exp_dicts,
                    total_years_experience=total_years
                )
                results["skill_proficiency_analysis"] = skill_proficiency_analysis
            except Exception as e:
                logger.warning(f"Failed to analyze skill proficiency: {e}")
                results["skill_proficiency_analysis"] = []
        else:
            results["skill_proficiency_analysis"] = []

        # Step 9: Division classification
        cv_summary = f"{summary.professional_summary if hasattr(summary, 'professional_summary') else ''} | " \
                    f"Skills: {technical_skills.programming_languages if hasattr(technical_skills, 'programming_languages') else ''}"
        division = self.division_classifier(
            cv_summary=cv_summary,
            available_divisions=available_divisions
        )
        results["division"] = division

        # Step 10: HR Insights (if enabled)
        if self.with_hr_insights:
            # Career progression
            career_prog = self.career_analyzer(work_history=work_history_summary)
            results["career_progression"] = career_prog

            # Job hopping
            job_hopping = self.job_hopping_detector(work_history=work_history_summary)
            results["job_hopping"] = job_hopping

            # Red flags
            red_flags = self.red_flag_detector(
                cv_content=cv_text,
                work_history_summary=work_history_summary
            )
            results["red_flags"] = red_flags

            # Quality scoring
            quality = self.quality_scorer(cv_text=cv_text)
            results["quality_score"] = quality

            # Key strengths
            strengths = self.strengths_extractor(cv_text=cv_text)
            results["key_strengths"] = strengths

        # Add metadata
        results["extraction_metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "with_evidence": self.work_exp_extractor.single_extractor.with_evidence,
            "with_hr_insights": self.with_hr_insights,
            "industry_domain": self.industry_domain,
        }

        return results
