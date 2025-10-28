"""
CV Extraction Pipeline.

End-to-end pipeline for extracting structured data from CVs/resumes.
Integrates preprocessing, DSPy extraction modules, and post-processing.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import date, datetime
from pathlib import Path

from src.models import (
    CandidateProfile,
    PersonalInfo,
    WorkExperience,
    Education,
    Skill,
    LanguageSkill,
    Certification,
    CVMetadata,
    HRInsights,
    EvidenceBasedCandidateProfile,
    SkillCategory,
    ProficiencyLevel,
    EducationLevel,
    CertificationStatus,
)
from src.dspy_modules import (
    ComprehensiveCVExtractor,
)
from src.config import get_settings


logger = logging.getLogger(__name__)


class CVExtractionPipeline:
    """
    Complete pipeline for CV extraction.

    Pipeline steps:
    1. Preprocessing: Parse PDF/DOCX, clean text
    2. Section Detection: Identify CV sections
    3. Extraction: Extract structured data using DSPy
    4. Post-processing: Convert to Pydantic models, validate
    5. HR Insights: Generate HR analysis (optional)
    6. Quality Scoring: Assess extraction quality
    """

    def __init__(
        self,
        with_evidence: bool = False,
        with_hr_insights: bool = True,
        strict_mode: bool = False,
        industry_domain: Optional[str] = None,
        division: Optional[str] = None,
    ):
        """
        Initialize CV extraction pipeline.

        Args:
            with_evidence: Include evidence spans for explainability
            with_hr_insights: Generate HR insights
            strict_mode: Use strict extraction (no inference)
            industry_domain: Industry domain for context
            division: AIA division for division-specific extraction
        """
        self.settings = get_settings()
        self.with_evidence = with_evidence
        self.with_hr_insights = with_hr_insights
        self.strict_mode = strict_mode
        self.industry_domain = industry_domain
        self.division = division

        # Initialize DSPy extractor
        self.extractor = ComprehensiveCVExtractor(
            with_evidence=with_evidence,
            with_hr_insights=with_hr_insights,
            strict_mode=strict_mode,
            industry_domain=industry_domain,
        )

        logger.info(
            f"Initialized CVExtractionPipeline: "
            f"evidence={with_evidence}, hr_insights={with_hr_insights}, "
            f"strict_mode={strict_mode}, domain={industry_domain}"
        )

    def extract_from_text(
        self,
        cv_text: str,
        cv_file_name: Optional[str] = None,
        available_divisions: Optional[str] = None,
    ) -> CandidateProfile:
        """
        Extract structured data from CV text.

        Args:
            cv_text: Full CV text
            cv_file_name: Original filename (for metadata)
            available_divisions: Comma-separated division options

        Returns:
            CandidateProfile with extracted data
        """
        logger.info(f"Starting CV extraction for {cv_file_name or 'unknown'}")

        # Set default divisions if not provided
        if available_divisions is None:
            available_divisions = "technology,insurance_operations,finance,hr,legal,sales,marketing,customer_service,investment_services,executive"

        try:
            # Step 1: Run DSPy extraction
            extraction_results = self.extractor(
                cv_text=cv_text,
                available_divisions=available_divisions,
            )

            # Step 2: Convert to Pydantic models
            candidate_profile = self._convert_to_pydantic(
                extraction_results, cv_text, cv_file_name
            )

            # Step 3: Calculate derived fields
            self._calculate_derived_fields(candidate_profile)

            # Step 4: Validate
            self._validate_profile(candidate_profile)

            logger.info(f"Successfully extracted CV for {candidate_profile.personal_info.full_name}")

            return candidate_profile

        except Exception as e:
            logger.error(f"Error during CV extraction: {str(e)}", exc_info=True)
            raise

    def extract_from_file(
        self,
        cv_file_path: str,
        available_divisions: Optional[str] = None,
    ) -> CandidateProfile:
        """
        Extract structured data from CV file (PDF, DOCX, etc.).

        Args:
            cv_file_path: Path to CV file
            available_divisions: Comma-separated division options

        Returns:
            CandidateProfile with extracted data
        """
        logger.info(f"Extracting from file: {cv_file_path}")

        # Parse file to text (placeholder - implement with actual parser)
        cv_text = self._parse_file(cv_file_path)

        # Extract from text
        file_name = Path(cv_file_path).name
        return self.extract_from_text(
            cv_text=cv_text,
            cv_file_name=file_name,
            available_divisions=available_divisions,
        )

    def _parse_file(self, file_path: str) -> str:
        """
        Parse CV file to text.

        Uses Azure Document Intelligence if available (better structure preservation),
        otherwise falls back to basic PDF/DOCX parsing.

        Args:
            file_path: Path to file

        Returns:
            Extracted text (markdown format if using Document Intelligence)
        """
        from src.preprocessing import (
            parse_file,
            is_azure_document_intelligence_available,
            parse_pdf_via_images,
        )

        # Try Azure Document Intelligence with image-based approach (extracts all pages)
        if is_azure_document_intelligence_available() and file_path.endswith('.pdf'):
            try:
                logger.info("Using Azure Document Intelligence (image-based) for PDF parsing...")
                markdown_content = parse_pdf_via_images(file_path)
                logger.info(f"Successfully parsed PDF to markdown ({len(markdown_content)} chars)")
                return markdown_content
            except Exception as e:
                logger.warning(
                    f"Azure Document Intelligence parsing failed: {e}. "
                    f"Falling back to basic PDF parsing."
                )
                # Fall through to basic parsing

        # Fallback to basic PDF/DOCX parsing
        logger.info("Using pdfplumber for PDF/DOCX parsing...")
        full_text = parse_file(file_path)
        logger.info(f"Extracted {len(full_text)} characters")
        return full_text

    def _convert_to_pydantic(
        self,
        extraction_results: Dict[str, Any],
        cv_text: str,
        cv_file_name: Optional[str],
    ) -> CandidateProfile:
        """
        Convert DSPy extraction results to Pydantic CandidateProfile.

        Args:
            extraction_results: Results from DSPy extraction
            cv_text: Original CV text
            cv_file_name: Filename

        Returns:
            CandidateProfile instance
        """
        # Extract personal info
        personal_info_result = extraction_results.get("personal_info", {})
        personal_info = PersonalInfo(
            full_name=getattr(personal_info_result, "full_name", "Unknown"),
            email=self._clean_field(getattr(personal_info_result, "email", None)),
            phone=self._clean_field(getattr(personal_info_result, "phone", None)),
            location=self._clean_field(getattr(personal_info_result, "location", None)),
            linkedin_url=self._clean_field(getattr(personal_info_result, "linkedin_url", None)),
            github_url=self._clean_field(getattr(personal_info_result, "github_url", None)),
            visa_status=self._clean_field(getattr(personal_info_result, "visa_status", None)),
            professional_summary=self._get_professional_summary(extraction_results),
        )

        # Extract work experience
        work_experience = self._extract_work_experience(extraction_results)

        # Extract education
        education = self._extract_education(extraction_results)

        # Extract skills
        skills = self._extract_skills(extraction_results)

        # Extract certifications
        certifications = self._extract_certifications(extraction_results)

        # Get division
        division_result = extraction_results.get("division", {})
        primary_division = self._clean_field(getattr(division_result, "primary_division", None))
        secondary_divisions = self._parse_list(getattr(division_result, "secondary_divisions", ""))

        # Get career level
        summary_result = extraction_results.get("professional_summary", {})
        career_level = getattr(summary_result, "career_level", None)

        # Extract HR insights if available (structured objects)
        from src.models.cv_schema import (
            CareerProgressionAnalysis, JobHoppingAssessment, RedFlag,
            CareerTrajectory, ProgressionRate, RedFlagSeverity
        )

        career_progression = None
        job_hopping = None
        red_flags_list = []
        quality_score_value = None
        key_strengths_text = None

        if self.with_hr_insights:
            # Career progression - create structured object
            career_prog_result = extraction_results.get("career_progression", {})
            if career_prog_result:
                trajectory_str = getattr(career_prog_result, "trajectory", "").lower()
                rate_str = getattr(career_prog_result, "progression_rate", "").lower()
                promotions_str = getattr(career_prog_result, "number_of_promotions", "0")
                tenure_str = getattr(career_prog_result, "average_tenure_months", "0")
                summary = getattr(career_prog_result, "summary", "")

                # Map strings to enums
                trajectory_map = {
                    'upward': CareerTrajectory.UPWARD,
                    'stagnant': CareerTrajectory.STAGNANT,
                    'mixed': CareerTrajectory.MIXED,
                    'early career': CareerTrajectory.EARLY_CAREER,
                    'downward': CareerTrajectory.DOWNWARD
                }
                rate_map = {
                    'rapid': ProgressionRate.RAPID,
                    'fast': ProgressionRate.RAPID,
                    'moderate': ProgressionRate.MODERATE,
                    'slow': ProgressionRate.SLOW,
                    'none': ProgressionRate.NONE
                }

                try:
                    career_progression = CareerProgressionAnalysis(
                        trajectory=trajectory_map.get(trajectory_str),
                        progression_rate=rate_map.get(rate_str),
                        number_of_promotions=int(promotions_str) if promotions_str.isdigit() else 0,
                        average_tenure_months=int(tenure_str) if tenure_str.isdigit() else None,
                        summary=summary
                    )
                except Exception as e:
                    logger.warning(f"Failed to create CareerProgressionAnalysis: {e}")
                    career_progression = None

            # Job hopping - create structured object
            job_hopping_result = extraction_results.get("job_hopping", {})
            if job_hopping_result:
                is_hopping_str = getattr(job_hopping_result, "is_job_hopping", "No")
                details = getattr(job_hopping_result, "job_hopping_details", "")
                gaps_json_str = getattr(job_hopping_result, "employment_gaps_json", "[]")

                # Parse employment gaps JSON
                try:
                    import json
                    gaps_list = json.loads(gaps_json_str) if gaps_json_str else []
                except json.JSONDecodeError:
                    # Fallback to old format if JSON parsing fails
                    gaps_old = getattr(job_hopping_result, "employment_gaps", "None")
                    gaps_list = [g.strip() for g in gaps_old.split('|') if g.strip() and g.strip().lower() != 'none']

                try:
                    job_hopping = JobHoppingAssessment(
                        is_job_hopper=is_hopping_str.lower() in ['yes', 'true'],
                        details=details if details and details.lower() != 'none' else None,
                        employment_gaps=gaps_list
                    )
                except Exception as e:
                    logger.warning(f"Failed to create JobHoppingAssessment: {e}")
                    job_hopping = None

            # Red flags - DSPy now returns List[RedFlag] directly
            red_flags_result = extraction_results.get("red_flags", {})
            logger.info(f"Red flags result type: {type(red_flags_result)}")
            if red_flags_result:
                # Get the red_flags attribute (List[RedFlag] from DSPy)
                red_flags_from_dspy = getattr(red_flags_result, "red_flags", [])

                if isinstance(red_flags_from_dspy, list):
                    # DSPy returns RedFlag objects directly
                    red_flags_list = red_flags_from_dspy
                    logger.info(f"Received {len(red_flags_list)} red flags from DSPy")
                else:
                    logger.warning(f"Unexpected type for red_flags: {type(red_flags_from_dspy)}")
                    red_flags_list = []

            # Quality score - calculate average from multiple scores
            quality_result = extraction_results.get("quality_score", {})
            if quality_result:
                formatting = getattr(quality_result, "formatting_score", "0")
                completeness = getattr(quality_result, "completeness_score", "0")
                content = getattr(quality_result, "content_quality_score", "0")

                try:
                    scores = [float(s) for s in [formatting, completeness, content] if s and s != "0"]
                    if scores:
                        quality_score_value = sum(scores) / len(scores)
                    else:
                        quality_score_value = None
                except (ValueError, TypeError):
                    quality_score_value = None
            else:
                quality_score_value = None

            # Key strengths - combine all strength categories
            strengths_result = extraction_results.get("key_strengths", {})
            if strengths_result:
                technical = getattr(strengths_result, "technical_strengths", "")
                leadership = getattr(strengths_result, "leadership_strengths", "")
                usp = getattr(strengths_result, "unique_selling_points", "")

                parts = []
                if technical:
                    parts.append(f"Technical: {technical}")
                if leadership:
                    parts.append(f"Leadership: {leadership}")
                if usp:
                    parts.append(f"USP: {usp}")

                key_strengths_text = " | ".join(parts) if parts else None
            else:
                key_strengths_text = None

        # Create metadata
        metadata = CVMetadata(
            extraction_timestamp=datetime.now().isoformat(),
            cv_file_name=cv_file_name,
            language_detected="en",  # TODO: Implement language detection
        )

        # Create profile
        profile = CandidateProfile(
            personal_info=personal_info,
            work_experience=work_experience,
            education=education,
            skills=skills,
            certifications=certifications,
            primary_division=primary_division,
            secondary_divisions=secondary_divisions,
            career_level=career_level,
            career_progression_analysis=career_progression,  # Now CareerProgressionAnalysis object
            job_hopping_assessment=job_hopping,  # Now JobHoppingAssessment object
            red_flags=red_flags_list,  # Now List[RedFlag] objects
            quality_score=quality_score_value,
            key_strengths=key_strengths_text,
            metadata=metadata,
            raw_text=cv_text,
        )

        return profile

    def _get_professional_summary(self, extraction_results: Dict[str, Any]) -> Optional[str]:
        """Extract professional summary from results."""
        summary_result = extraction_results.get("professional_summary", {})
        return getattr(summary_result, "professional_summary", None)

    def _extract_work_experience(self, extraction_results: Dict[str, Any]) -> List[WorkExperience]:
        """Extract work experience list with achievement metrics."""
        from src.models.cv_schema import AchievementMetric, MetricType, ImpactCategory

        work_exp_results = extraction_results.get("work_experience", [])
        achievement_metrics_by_exp = extraction_results.get("achievement_metrics", {})
        work_experiences = []

        for idx, exp in enumerate(work_exp_results):
            try:
                # Get achievement metrics for this experience
                exp_metrics = achievement_metrics_by_exp.get(idx, [])
                achievement_metric_objects = []

                # Convert metrics to Pydantic models
                for metric in exp_metrics:
                    try:
                        # Map confidence string to float
                        confidence_map = {'high': 0.9, 'medium': 0.7, 'low': 0.4}
                        confidence_str = metric.get('confidence', 'medium')
                        if isinstance(confidence_str, str):
                            confidence = confidence_map.get(confidence_str.lower(), 0.5)
                        else:
                            confidence = float(confidence_str)

                        achievement_metric = AchievementMetric(
                            raw_text=metric.get('raw_text', ''),
                            metric_value=metric.get('metric_value'),
                            metric_type=MetricType(metric['metric_type']) if metric.get('metric_type') else None,
                            metric_unit=metric.get('metric_unit'),
                            impact_category=ImpactCategory(metric['impact_category']) if metric.get('impact_category') else None,
                            confidence=confidence,
                            context=metric.get('context'),
                            is_quantifiable=metric.get('has_metrics', False)
                        )
                        achievement_metric_objects.append(achievement_metric)
                    except Exception as e:
                        logger.warning(f"Failed to parse achievement metric: {e}")

                # Handle both dict (from list extractor) and object (from batch extractor)
                if isinstance(exp, dict):
                    work_exp = WorkExperience(
                        company_name=exp.get("company_name", "Unknown"),
                        job_title=exp.get("job_title", "Unknown"),
                        start_date=self._parse_date(exp.get("start_date")),
                        end_date=self._parse_date(exp.get("end_date")),
                        is_current=self._is_current(exp.get("end_date")),
                        location=self._clean_field(exp.get("location")),
                        responsibilities=self._parse_list(exp.get("responsibilities", "")),
                        achievements=self._parse_list(exp.get("achievements", "")),
                        achievement_metrics=achievement_metric_objects,
                        technologies_used=self._parse_list(exp.get("technologies", "")),
                    )
                else:
                    # Handle object format (from Pydantic models)
                    work_exp = WorkExperience(
                        company_name=getattr(exp, "company_name", "Unknown"),
                        job_title=getattr(exp, "job_title", "Unknown"),
                        start_date=self._parse_date(getattr(exp, "start_date", None)),
                        end_date=self._parse_date(getattr(exp, "end_date", None)),
                        is_current=self._is_current(getattr(exp, "end_date", None)),
                        location=self._clean_field(getattr(exp, "location", None)),
                        responsibilities=self._parse_list(getattr(exp, "responsibilities", [])),
                        achievements=self._parse_list(getattr(exp, "achievements", [])),
                        achievement_metrics=achievement_metric_objects,
                        technologies_used=self._parse_list(getattr(exp, "technologies_used", [])),
                    )
                work_experiences.append(work_exp)
            except Exception as e:
                logger.warning(f"Failed to parse work experience: {e}")

        return work_experiences

    def _extract_education(self, extraction_results: Dict[str, Any]) -> List[Education]:
        """Extract education list."""
        edu_results = extraction_results.get("education", [])
        educations = []

        for edu in edu_results:
            try:
                # Handle both dict (from list extractor) and object (from batch extractor)
                if isinstance(edu, dict):
                    education = Education(
                        institution_name=edu.get("institution_name", "Unknown"),
                        degree=edu.get("degree", "Unknown"),
                        field_of_study=self._clean_field(edu.get("field_of_study")),
                        start_date=self._parse_date(edu.get("start_date")),
                        end_date=self._parse_date(edu.get("end_date")),
                        is_current=self._is_current(edu.get("end_date")),
                        gpa=self._parse_gpa(edu.get("gpa")),
                        honors=self._parse_list(edu.get("honors", "")),
                    )
                else:
                    # Handle object format
                    education = Education(
                        institution_name=getattr(edu, "institution_name", "Unknown"),
                        degree=getattr(edu, "degree", "Unknown"),
                        field_of_study=self._clean_field(getattr(edu, "field_of_study", None)),
                        start_date=self._parse_date(getattr(edu, "start_date", None)),
                        end_date=self._parse_date(getattr(edu, "end_date", None)),
                        is_current=self._is_current(getattr(edu, "end_date", None)),
                        gpa=self._parse_gpa(getattr(edu, "gpa", None)),
                        honors=self._parse_list(getattr(edu, "honors", "")),
                    )
                educations.append(education)
            except Exception as e:
                logger.warning(f"Failed to parse education: {e}")

        return educations

    def _extract_skills(self, extraction_results: Dict[str, Any]) -> List[Skill]:
        """Extract skills list with proficiency analysis."""
        from src.models.cv_schema import ProficiencyLevel

        skills = []

        # Get technical skills
        tech_skills = extraction_results.get("technical_skills", {})
        skills.extend(self._parse_skills_from_field(tech_skills, "programming_languages", SkillCategory.TECHNICAL))
        skills.extend(self._parse_skills_from_field(tech_skills, "frameworks_libraries", SkillCategory.TECHNICAL))
        skills.extend(self._parse_skills_from_field(tech_skills, "tools_platforms", SkillCategory.TOOL))
        skills.extend(self._parse_skills_from_field(tech_skills, "databases", SkillCategory.TECHNICAL))
        skills.extend(self._parse_skills_from_field(tech_skills, "cloud_services", SkillCategory.TECHNICAL))

        # Get skills with proficiency
        proficiency_skills = extraction_results.get("skills_proficiency", {})
        skills.extend(self._parse_proficiency_skills(proficiency_skills, "expert_skills", ProficiencyLevel.EXPERT))
        skills.extend(self._parse_proficiency_skills(proficiency_skills, "advanced_skills", ProficiencyLevel.ADVANCED))
        skills.extend(self._parse_proficiency_skills(proficiency_skills, "intermediate_skills", ProficiencyLevel.INTERMEDIATE))
        skills.extend(self._parse_proficiency_skills(proficiency_skills, "beginner_skills", ProficiencyLevel.BEGINNER))

        # Get domain skills
        if "domain_skills" in extraction_results:
            domain_skills = extraction_results["domain_skills"]
            skills.extend(self._parse_skills_from_field(domain_skills, "domain_expertise", SkillCategory.DOMAIN))
            skills.extend(self._parse_skills_from_field(domain_skills, "business_skills", SkillCategory.SOFT))

        # Deduplicate by name and merge proficiency analysis
        unique_skills = {}
        for skill in skills:
            if skill.name not in unique_skills:
                unique_skills[skill.name] = skill

        # Enrich with proficiency analysis data
        proficiency_analysis = extraction_results.get("skill_proficiency_analysis", [])
        for analysis in proficiency_analysis:
            skill_name = analysis.get('skill_name', '')
            if skill_name in unique_skills:
                skill = unique_skills[skill_name]

                # Map proficiency level string to enum
                prof_level_str = analysis.get('proficiency_level', '').lower()
                prof_level_map = {
                    'beginner': ProficiencyLevel.BEGINNER,
                    'intermediate': ProficiencyLevel.INTERMEDIATE,
                    'advanced': ProficiencyLevel.ADVANCED,
                    'expert': ProficiencyLevel.EXPERT
                }
                if prof_level_str in prof_level_map:
                    skill.proficiency_level = prof_level_map[prof_level_str]

                # Add calculated fields
                skill.years_of_experience = analysis.get('years_of_experience', 0.0)
                skill.first_used_date = analysis.get('first_used')
                skill.last_used = analysis.get('last_used')
                skill.usage_context = analysis.get('usage_context', [])
                skill.mentioned_count = analysis.get('mentioned_count', 1)
                skill.proficiency_confidence = analysis.get('proficiency_confidence', 0.0)

        return list(unique_skills.values())

    def _parse_skills_from_field(
        self,
        result: Any,
        field_name: str,
        category: SkillCategory,
    ) -> List[Skill]:
        """Parse skills from a result field."""
        field_value = getattr(result, field_name, None)
        if not field_value or field_value == "None":
            return []

        skill_names = self._parse_list(field_value)
        return [
            Skill(name=name.strip(), category=category)
            for name in skill_names
            if name.strip()
        ]

    def _parse_proficiency_skills(
        self,
        result: Any,
        field_name: str,
        proficiency: ProficiencyLevel,
    ) -> List[Skill]:
        """Parse skills with proficiency level."""
        field_value = getattr(result, field_name, None)
        if not field_value or field_value == "None":
            return []

        skill_names = self._parse_list(field_value)
        return [
            Skill(
                name=name.strip(),
                category=SkillCategory.TECHNICAL,
                proficiency_level=proficiency
            )
            for name in skill_names
            if name.strip()
        ]

    def _extract_certifications(self, extraction_results: Dict[str, Any]) -> List[Certification]:
        """Extract certifications list."""
        cert_result = extraction_results.get("certifications", {})
        cert_text = getattr(cert_result, "certifications", "")

        if not cert_text or cert_text == "None":
            return []

        # Parse certification entries
        cert_entries = cert_text.split(" | ")
        certifications = []

        for entry in cert_entries:
            if not entry.strip():
                continue

            try:
                # Simple parsing (can be enhanced)
                parts = entry.split("(")
                name = parts[0].strip()

                certification = Certification(
                    name=name,
                    issuing_organization="Unknown",  # TODO: Parse from entry
                    status=CertificationStatus.ACTIVE,
                )
                certifications.append(certification)
            except Exception as e:
                logger.warning(f"Failed to parse certification: {e}")

        return certifications

    def _calculate_derived_fields(self, profile: CandidateProfile) -> None:
        """Calculate derived fields like total experience."""
        # Calculate total years of experience
        if profile.work_experience:
            total_months = 0
            for exp in profile.work_experience:
                if exp.start_date and exp.end_date:
                    months = (exp.end_date.year - exp.start_date.year) * 12
                    months += exp.end_date.month - exp.start_date.month
                    total_months += max(months, 0)
                elif exp.start_date:
                    # Current role
                    months = (date.today().year - exp.start_date.year) * 12
                    months += date.today().month - exp.start_date.month
                    total_months += max(months, 0)

            profile.total_years_experience = round(total_months / 12, 1)

            # Calculate years in current role
            if profile.work_experience[0].is_current:
                current_exp = profile.work_experience[0]
                if current_exp.start_date:
                    months = (date.today().year - current_exp.start_date.year) * 12
                    months += date.today().month - current_exp.start_date.month
                    profile.years_in_current_role = round(months / 12, 1)

    def _validate_profile(self, profile: CandidateProfile) -> None:
        """Validate candidate profile."""
        # Pydantic already validates, but we can add custom validation
        if not profile.personal_info.full_name:
            logger.warning("Candidate profile missing name")

        if not profile.work_experience:
            logger.warning("Candidate profile has no work experience")

        if not profile.skills:
            logger.warning("Candidate profile has no skills")

    def _clean_field(self, value: Any) -> Optional[str]:
        """Clean a field value."""
        if value is None or value == "None" or value == "NOT_FOUND":
            return None
        return str(value).strip()

    def _parse_list(self, value, separator: str = " | ") -> List[str]:
        """Parse a delimited string or list into a list."""
        # Handle case where value is already a list (from Pydantic models)
        if isinstance(value, list):
            return [str(item).strip() for item in value if item and str(item).strip() != "None"]

        # Handle string values
        if not value or value == "None":
            return []

        # Try primary separator
        items = value.split(separator)
        if len(items) == 1:
            # Try comma separator
            items = value.split(",")

        return [item.strip() for item in items if item.strip() and item.strip() != "None"]

    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Parse date string to date object with flexible format handling."""
        if not date_str or date_str == "None" or date_str == "NOT_FOUND":
            return None

        if date_str == "Present":
            return None

        try:
            # Handle YYYY-MM-DD format first
            if date_str.count("-") == 2:
                parts = date_str.split("-")
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])
                return date(year, month, day)
            # Handle YYYY-MM or YYYY-Season format
            elif "-" in date_str:
                parts = date_str.split("-")
                year = int(parts[0])

                # Try to parse month as integer
                try:
                    month = int(parts[1])
                    return date(year, month, 1)
                except ValueError:
                    # Handle season names (Summer, Fall, Winter, Spring) or text
                    season_month_map = {
                        'spring': 3,
                        'summer': 6,
                        'fall': 9,
                        'autumn': 9,
                        'winter': 12
                    }
                    month_name = parts[1].lower().strip()
                    month = season_month_map.get(month_name, 1)
                    return date(year, month, 1)
            # Try YYYY format
            else:
                return date(int(date_str), 1, 1)
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse date '{date_str}': {e}")
            return None

    def _parse_gpa(self, gpa_str: Optional[str]) -> Optional[float]:
        """Parse GPA string to float."""
        if not gpa_str or gpa_str == "None":
            return None

        try:
            # Extract numeric part (e.g., "3.8/4.0" -> 3.8)
            numeric_part = gpa_str.split("/")[0].strip()
            return float(numeric_part)
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse GPA '{gpa_str}': {e}")
            return None

    def _is_current(self, end_date_str: Optional[str]) -> bool:
        """Check if position is current."""
        if not end_date_str:
            return False
        return end_date_str == "Present"
