"""
JD Extraction Pipeline.

End-to-end pipeline for extracting structured data from Job Descriptions.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import date, datetime

from src.models import (
    JobDescription,
    RoleInfo,
    LocationInfo,
    SkillRequirement,
    ExperienceRequirement,
    EducationRequirement,
    CertificationRequirement,
    Responsibility,
    CompensationInfo,
    CultureInfo,
    ApplicationInfo,
    JDMetadata,
    RequirementPriority,
    SkillType,
    ExperienceLevel,
    WorkArrangement,
    EducationLevel,
)
from src.dspy_modules import ComprehensiveJDExtractor
from src.config import get_settings


logger = logging.getLogger(__name__)


class JDExtractionPipeline:
    """
    Complete pipeline for JD extraction.

    Pipeline steps:
    1. Preprocessing: Clean JD text
    2. Extraction: Extract structured data using DSPy
    3. Post-processing: Convert to Pydantic models, validate
    4. Analysis: Generate ideal candidate profile, matching weights
    5. Quality Assessment: Assess JD quality
    """

    def __init__(
        self,
        with_analysis: bool = True,
        strict_mode: bool = False,
        division: Optional[str] = None,
    ):
        """
        Initialize JD extraction pipeline.

        Args:
            with_analysis: Include analysis (ideal profile, weights, etc.)
            strict_mode: Use strict extraction (no inference)
            division: AIA division for division-specific extraction
        """
        self.settings = get_settings()
        self.with_analysis = with_analysis
        self.strict_mode = strict_mode
        self.division = division

        # Initialize DSPy extractor
        self.extractor = ComprehensiveJDExtractor(
            with_analysis=with_analysis,
            strict_mode=strict_mode,
        )

        logger.info(
            f"Initialized JDExtractionPipeline: "
            f"analysis={with_analysis}, strict_mode={strict_mode}, division={division}"
        )

    def extract(
        self,
        jd_text: str,
        jd_file_name: Optional[str] = None,
        available_divisions: Optional[str] = None,
    ) -> JobDescription:
        """
        Extract structured data from JD text.

        Args:
            jd_text: Full JD text
            jd_file_name: Original filename (for metadata)
            available_divisions: Comma-separated division options

        Returns:
            JobDescription with extracted data
        """
        logger.info(f"Starting JD extraction for {jd_file_name or 'unknown'}")

        # Set default divisions if not provided
        if available_divisions is None:
            available_divisions = "technology,insurance_operations,finance,hr,legal,sales,marketing,customer_service,investment_services,executive"

        try:
            # Step 1: Run DSPy extraction
            extraction_results = self.extractor(
                jd_text=jd_text,
                available_divisions=available_divisions,
            )

            # Step 2: Convert to Pydantic models
            job_description = self._convert_to_pydantic(
                extraction_results, jd_text, jd_file_name
            )

            # Step 3: Validate
            self._validate_jd(job_description)

            logger.info(f"Successfully extracted JD: {job_description.role_info.job_title}")

            return job_description

        except Exception as e:
            logger.error(f"Error during JD extraction: {str(e)}", exc_info=True)
            raise

    def _convert_to_pydantic(
        self,
        extraction_results: Dict[str, Any],
        jd_text: str,
        jd_file_name: Optional[str],
    ) -> JobDescription:
        """Convert DSPy extraction results to Pydantic JobDescription."""

        # Extract role info
        role_info_result = extraction_results.get("role_info", {})
        role_info = RoleInfo(
            job_title=getattr(role_info_result, "job_title", "Unknown"),
            department=self._clean_field(getattr(role_info_result, "department", None)),
            experience_level=self._parse_experience_level(
                getattr(role_info_result, "experience_level", None)
            ),
            reporting_to=self._clean_field(getattr(role_info_result, "reports_to", None)),
            team_size=self._parse_int(getattr(role_info_result, "team_size", None)),
        )

        # Extract location info
        location_info = self._extract_location_info(extraction_results)

        # Extract skills requirements
        skills_required = self._extract_skills_requirements(extraction_results)

        # Extract experience requirements
        experience_requirements = self._extract_experience_requirements(extraction_results)

        # Extract education requirements
        education_requirements = self._extract_education_requirements(extraction_results)

        # Extract certification requirements
        certifications_required = self._extract_certification_requirements(extraction_results)

        # Extract responsibilities
        responsibilities = self._extract_responsibilities(extraction_results)

        # Extract compensation
        compensation = self._extract_compensation(extraction_results)

        # Extract culture
        culture_info = self._extract_culture(extraction_results)

        # Extract application info
        application_info = self._extract_application_info(extraction_results)

        # Get division
        division_result = extraction_results.get("division", {})
        primary_division = self._clean_field(getattr(division_result, "primary_division", None))
        secondary_divisions = self._parse_list(getattr(division_result, "secondary_divisions", ""))

        # Create metadata
        metadata = JDMetadata(
            extraction_timestamp=datetime.now().isoformat(),
            jd_file_name=jd_file_name,
            language_detected="en",
        )

        # Create job description
        jd = JobDescription(
            role_info=role_info,
            location_info=location_info,
            skills_required=skills_required,
            experience_requirements=experience_requirements,
            education_requirements=education_requirements,
            certifications_required=certifications_required,
            responsibilities=responsibilities,
            compensation=compensation,
            culture_info=culture_info,
            application_info=application_info,
            primary_division=primary_division,
            secondary_divisions=secondary_divisions,
            metadata=metadata,
            raw_text=jd_text,
        )

        return jd

    def _extract_location_info(self, extraction_results: Dict[str, Any]) -> Optional[LocationInfo]:
        """Extract location info."""
        location_result = extraction_results.get("location_info", {})
        if not location_result:
            return None

        return LocationInfo(
            primary_location=self._clean_field(getattr(location_result, "primary_location", None)),
            work_arrangement=self._parse_work_arrangement(
                getattr(location_result, "work_arrangement", None)
            ),
            relocation_assistance=self._parse_bool(
                getattr(location_result, "relocation_assistance", "No")
            ),
            travel_required=self._clean_field(getattr(location_result, "travel_required", None)),
        )

    def _extract_skills_requirements(self, extraction_results: Dict[str, Any]) -> List[SkillRequirement]:
        """Extract skills requirements."""
        skills_requirements = []

        # Get required skills
        required_skills_result = extraction_results.get("required_skills", {})
        required_tech = self._parse_list(
            getattr(required_skills_result, "required_technical_skills", "")
        )
        preferred_tech = self._parse_list(
            getattr(required_skills_result, "preferred_technical_skills", "")
        )
        required_soft = self._parse_list(
            getattr(required_skills_result, "required_soft_skills", "")
        )

        # Add required technical skills
        for skill in required_tech:
            skills_requirements.append(
                SkillRequirement(
                    skill_name=skill,
                    skill_type=SkillType.TECHNICAL,
                    priority=RequirementPriority.REQUIRED,
                )
            )

        # Add preferred technical skills
        for skill in preferred_tech:
            skills_requirements.append(
                SkillRequirement(
                    skill_name=skill,
                    skill_type=SkillType.TECHNICAL,
                    priority=RequirementPriority.PREFERRED,
                )
            )

        # Add soft skills
        for skill in required_soft:
            skills_requirements.append(
                SkillRequirement(
                    skill_name=skill,
                    skill_type=SkillType.SOFT,
                    priority=RequirementPriority.REQUIRED,
                )
            )

        return skills_requirements

    def _extract_experience_requirements(
        self, extraction_results: Dict[str, Any]
    ) -> Optional[ExperienceRequirement]:
        """Extract experience requirements."""
        exp_result = extraction_results.get("experience_requirements", {})
        if not exp_result:
            return None

        return ExperienceRequirement(
            minimum_years=self._parse_float(getattr(exp_result, "minimum_years", None)),
            preferred_years=self._parse_float(getattr(exp_result, "preferred_years", None)),
            industry_experience_required=self._parse_list(
                getattr(exp_result, "industry_experience", "")
            ),
            role_specific_experience=self._parse_list(
                getattr(exp_result, "role_specific_experience", "")
            ),
            management_experience_required=self._parse_bool(
                getattr(exp_result, "management_required", "No")
            ),
            minimum_management_years=self._parse_float(
                getattr(exp_result, "management_years", None)
            ),
        )

    def _extract_education_requirements(
        self, extraction_results: Dict[str, Any]
    ) -> Optional[EducationRequirement]:
        """Extract education requirements."""
        edu_result = extraction_results.get("education_requirements", {})
        if not edu_result:
            return None

        return EducationRequirement(
            minimum_degree=self._parse_education_level(
                getattr(edu_result, "minimum_degree", None)
            ),
            preferred_degree=self._parse_education_level(
                getattr(edu_result, "preferred_degree", None)
            ),
            required_fields=self._parse_list(getattr(edu_result, "required_fields", "")),
            preferred_fields=self._parse_list(getattr(edu_result, "preferred_fields", "")),
            can_substitute_with_experience=self._parse_bool(
                getattr(edu_result, "can_substitute_with_experience", "No")
            ),
        )

    def _extract_certification_requirements(
        self, extraction_results: Dict[str, Any]
    ) -> List[CertificationRequirement]:
        """Extract certification requirements."""
        cert_result = extraction_results.get("certification_requirements", {})
        certifications = []

        required_certs = self._parse_list(getattr(cert_result, "required_certifications", ""))
        for cert in required_certs:
            certifications.append(
                CertificationRequirement(
                    certification_name=cert,
                    priority=RequirementPriority.REQUIRED,
                )
            )

        preferred_certs = self._parse_list(getattr(cert_result, "preferred_certifications", ""))
        for cert in preferred_certs:
            certifications.append(
                CertificationRequirement(
                    certification_name=cert,
                    priority=RequirementPriority.PREFERRED,
                )
            )

        return certifications

    def _extract_responsibilities(self, extraction_results: Dict[str, Any]) -> List[Responsibility]:
        """Extract responsibilities."""
        resp_result = extraction_results.get("responsibilities", {})
        responsibilities = []

        core_resp = self._parse_list(getattr(resp_result, "core_responsibilities", ""))
        for resp in core_resp:
            responsibilities.append(
                Responsibility(
                    description=resp,
                    category="Core",
                    priority=RequirementPriority.REQUIRED,
                )
            )

        return responsibilities

    def _extract_compensation(self, extraction_results: Dict[str, Any]) -> Optional[CompensationInfo]:
        """Extract compensation info."""
        comp_result = extraction_results.get("compensation", {})
        if not comp_result:
            return None

        salary_range = getattr(comp_result, "salary_range", None)
        salary_min = None
        salary_max = None

        if salary_range and salary_range != "Not Disclosed":
            # Parse salary range (e.g., "$100,000 - $150,000")
            try:
                parts = salary_range.replace("$", "").replace(",", "").split("-")
                if len(parts) == 2:
                    salary_min = float(parts[0].strip())
                    salary_max = float(parts[1].strip())
            except (ValueError, IndexError):
                pass

        return CompensationInfo(
            salary_min=salary_min,
            salary_max=salary_max,
            salary_currency=self._clean_field(getattr(comp_result, "salary_currency", None)),
            bonus_structure="Yes" if self._parse_bool(getattr(comp_result, "bonus_mentioned", "No")) else None,
            equity_offered=self._parse_bool(getattr(comp_result, "equity_offered", "No")),
            benefits_list=self._parse_list(getattr(comp_result, "key_benefits", "")),
        )

    def _extract_culture(self, extraction_results: Dict[str, Any]) -> Optional[CultureInfo]:
        """Extract culture info."""
        culture_result = extraction_results.get("culture", {})
        if not culture_result:
            return None

        return CultureInfo(
            company_values=self._parse_list(getattr(culture_result, "company_values", "")),
            team_culture=self._clean_field(getattr(culture_result, "team_culture", None)),
            work_environment=self._clean_field(getattr(culture_result, "work_environment", None)),
            growth_opportunities=self._parse_list(getattr(culture_result, "growth_opportunities", "")),
        )

    def _extract_application_info(self, extraction_results: Dict[str, Any]) -> Optional[ApplicationInfo]:
        """Extract application info."""
        app_result = extraction_results.get("application", {})
        if not app_result:
            return None

        return ApplicationInfo(
            application_deadline=self._parse_date(getattr(app_result, "application_deadline", None)),
            expected_start_date=self._parse_date(getattr(app_result, "expected_start_date", None)),
            visa_sponsorship_available=self._parse_bool(
                getattr(app_result, "visa_sponsorship", "Not Mentioned")
            ),
            required_documents=self._parse_list(getattr(app_result, "required_documents", "")),
        )

    def _validate_jd(self, jd: JobDescription) -> None:
        """Validate job description."""
        if not jd.role_info.job_title:
            logger.warning("JD missing job title")

        if not jd.skills_required:
            logger.warning("JD has no skills requirements")

    def _clean_field(self, value: Any) -> Optional[str]:
        """Clean a field value."""
        if value is None or value == "None" or value == "NOT_FOUND":
            return None
        return str(value).strip()

    def _parse_list(self, value: str, separator: str = " | ") -> List[str]:
        """Parse a delimited string into a list."""
        if not value or value == "None":
            return []

        items = value.split(separator)
        if len(items) == 1:
            items = value.split(",")

        return [item.strip() for item in items if item.strip() and item.strip() != "None"]

    def _parse_bool(self, value: str) -> bool:
        """Parse boolean value."""
        if not value:
            return False
        return value.lower() in ["yes", "true", "1"]

    def _parse_int(self, value: Any) -> Optional[int]:
        """Parse integer value."""
        if not value or value == "None":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def _parse_float(self, value: Any) -> Optional[float]:
        """Parse float value."""
        if not value or value == "None":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Parse date string to date object."""
        if not date_str or date_str == "None" or date_str == "NOT_FOUND":
            return None

        try:
            if "-" in date_str:
                parts = date_str.split("-")
                year = int(parts[0])
                month = int(parts[1]) if len(parts) > 1 else 1
                day = int(parts[2]) if len(parts) > 2 else 1
                return date(year, month, day)
            else:
                return date(int(date_str), 1, 1)
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse date '{date_str}': {e}")
            return None

    def _parse_experience_level(self, level_str: Optional[str]) -> Optional[ExperienceLevel]:
        """Parse experience level."""
        if not level_str or level_str == "None":
            return None

        level_map = {
            "Entry": ExperienceLevel.ENTRY,
            "Junior": ExperienceLevel.JUNIOR,
            "Mid": ExperienceLevel.MID,
            "Senior": ExperienceLevel.SENIOR,
            "Lead": ExperienceLevel.LEAD,
            "Principal": ExperienceLevel.PRINCIPAL,
            "Executive": ExperienceLevel.EXECUTIVE,
        }

        return level_map.get(level_str, ExperienceLevel.MID)

    def _parse_work_arrangement(self, arrangement_str: Optional[str]) -> Optional[WorkArrangement]:
        """Parse work arrangement."""
        if not arrangement_str or arrangement_str == "None":
            return None

        arrangement_map = {
            "On-Site": WorkArrangement.ON_SITE,
            "Remote": WorkArrangement.REMOTE,
            "Hybrid": WorkArrangement.HYBRID,
        }

        return arrangement_map.get(arrangement_str, WorkArrangement.ON_SITE)

    def _parse_education_level(self, level_str: Optional[str]) -> Optional[EducationLevel]:
        """Parse education level."""
        if not level_str or level_str == "None":
            return None

        level_map = {
            "High School": EducationLevel.HIGH_SCHOOL,
            "Associate": EducationLevel.ASSOCIATE,
            "Bachelor": EducationLevel.BACHELOR,
            "Master": EducationLevel.MASTER,
            "Doctorate": EducationLevel.DOCTORATE,
        }

        return level_map.get(level_str, None)
