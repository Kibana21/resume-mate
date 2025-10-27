"""
Pydantic models for Job Description (JD) structured data extraction.

These models define the complete schema for job descriptions extracted and structured
for matching with candidate profiles across all AIA business divisions.
"""

from datetime import date
from typing import List, Optional, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator


# ============================================================================
# ENUMS FOR CONTROLLED VOCABULARIES
# ============================================================================

class RequirementPriority(str, Enum):
    """Priority level for requirements"""
    REQUIRED = "required"  # Must-have
    PREFERRED = "preferred"  # Nice-to-have
    OPTIONAL = "optional"  # Bonus


class SkillType(str, Enum):
    """Types of skills required"""
    TECHNICAL = "technical"
    SOFT = "soft"
    DOMAIN = "domain"
    LANGUAGE = "language"
    TOOL = "tool"
    METHODOLOGY = "methodology"


class ExperienceLevel(str, Enum):
    """Experience level classification"""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"
    EXECUTIVE = "executive"


class EmploymentType(str, Enum):
    """Type of employment"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class WorkArrangement(str, Enum):
    """Work arrangement options"""
    ON_SITE = "on_site"
    REMOTE = "remote"
    HYBRID = "hybrid"


class EducationLevel(str, Enum):
    """Education level requirements"""
    HIGH_SCHOOL = "high_school"
    ASSOCIATE = "associate"
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORATE = "doctorate"
    PROFESSIONAL = "professional"


# ============================================================================
# ROLE INFORMATION MODELS
# ============================================================================

class RoleInfo(BaseModel):
    """Basic role information"""

    job_title: str = Field(..., description="Job title")

    job_code: Optional[str] = Field(
        None,
        description="Internal job code or requisition number"
    )

    department: Optional[str] = Field(
        None,
        description="Department or team"
    )

    division: Optional[str] = Field(
        None,
        description="AIA business division"
    )

    reporting_to: Optional[str] = Field(
        None,
        description="Role this position reports to"
    )

    team_size: Optional[int] = Field(
        None,
        description="Size of team this role will manage",
        ge=0
    )

    experience_level: Optional[ExperienceLevel] = Field(
        None,
        description="Experience level required"
    )

    seniority_level: Optional[str] = Field(
        None,
        description="Seniority level (e.g., 'IC3', 'Manager II')"
    )

    career_level: Optional[str] = Field(
        None,
        description="Career level classification"
    )


# ============================================================================
# LOCATION & WORK ARRANGEMENT
# ============================================================================

class LocationInfo(BaseModel):
    """Job location information"""

    primary_location: Optional[str] = Field(
        None,
        description="Primary work location (City, Country)"
    )

    additional_locations: List[str] = Field(
        default_factory=list,
        description="Additional possible locations"
    )

    work_arrangement: Optional[WorkArrangement] = Field(
        None,
        description="Work arrangement (on-site, remote, hybrid)"
    )

    relocation_assistance: bool = Field(
        default=False,
        description="Whether relocation assistance is provided"
    )

    travel_required: Optional[str] = Field(
        None,
        description="Travel requirements (e.g., '10%', 'Occasional', 'Frequent')"
    )

    timezone_requirements: Optional[str] = Field(
        None,
        description="Timezone requirements for remote work"
    )


# ============================================================================
# SKILLS REQUIREMENTS
# ============================================================================

class SkillRequirement(BaseModel):
    """Individual skill requirement"""

    skill_name: str = Field(..., description="Name of the skill")

    skill_type: SkillType = Field(
        default=SkillType.TECHNICAL,
        description="Type of skill"
    )

    priority: RequirementPriority = Field(
        default=RequirementPriority.REQUIRED,
        description="Priority level"
    )

    minimum_proficiency: Optional[str] = Field(
        None,
        description="Minimum proficiency level required"
    )

    years_required: Optional[float] = Field(
        None,
        description="Years of experience with this skill",
        ge=0
    )

    context: Optional[str] = Field(
        None,
        description="Context or specific application of skill"
    )

    alternatives: List[str] = Field(
        default_factory=list,
        description="Alternative skills that can substitute"
    )

    weight: float = Field(
        default=1.0,
        description="Weight in matching algorithm (0-1)",
        ge=0.0,
        le=1.0
    )

    related_skills: List[str] = Field(
        default_factory=list,
        description="Related or complementary skills"
    )


# ============================================================================
# EXPERIENCE REQUIREMENTS
# ============================================================================

class ExperienceRequirement(BaseModel):
    """Experience requirements for the role"""

    minimum_years: Optional[float] = Field(
        None,
        description="Minimum years of total experience",
        ge=0
    )

    maximum_years: Optional[float] = Field(
        None,
        description="Maximum years (if applicable)",
        ge=0
    )

    preferred_years: Optional[float] = Field(
        None,
        description="Preferred years of experience",
        ge=0
    )

    industry_experience_required: List[str] = Field(
        default_factory=list,
        description="Required industry experience"
    )

    industry_experience_preferred: List[str] = Field(
        default_factory=list,
        description="Preferred industry experience"
    )

    role_specific_experience: List[str] = Field(
        default_factory=list,
        description="Specific role or function experience required"
    )

    management_experience_required: bool = Field(
        default=False,
        description="Whether management experience is required"
    )

    minimum_management_years: Optional[float] = Field(
        None,
        description="Minimum years of management experience",
        ge=0
    )


# ============================================================================
# EDUCATION REQUIREMENTS
# ============================================================================

class EducationRequirement(BaseModel):
    """Education requirements"""

    minimum_degree: Optional[EducationLevel] = Field(
        None,
        description="Minimum degree level required"
    )

    preferred_degree: Optional[EducationLevel] = Field(
        None,
        description="Preferred degree level"
    )

    required_fields: List[str] = Field(
        default_factory=list,
        description="Required fields of study"
    )

    preferred_fields: List[str] = Field(
        default_factory=list,
        description="Preferred fields of study"
    )

    alternative_fields: List[str] = Field(
        default_factory=list,
        description="Alternative acceptable fields"
    )

    can_substitute_with_experience: bool = Field(
        default=False,
        description="Whether experience can substitute for education"
    )

    substitution_ratio: Optional[str] = Field(
        None,
        description="Substitution ratio (e.g., '2 years experience = 1 year education')"
    )

    advanced_degrees_valued: bool = Field(
        default=False,
        description="Whether advanced degrees add value"
    )


# ============================================================================
# CERTIFICATION REQUIREMENTS
# ============================================================================

class CertificationRequirement(BaseModel):
    """Certification requirements"""

    certification_name: str = Field(..., description="Name of certification")

    issuing_organization: Optional[str] = Field(
        None,
        description="Organization that issues certification"
    )

    priority: RequirementPriority = Field(
        default=RequirementPriority.REQUIRED,
        description="Priority level"
    )

    must_be_current: bool = Field(
        default=True,
        description="Whether certification must be current/active"
    )

    alternatives: List[str] = Field(
        default_factory=list,
        description="Alternative certifications that are acceptable"
    )

    time_to_obtain: Optional[str] = Field(
        None,
        description="Expected time to obtain if not already held"
    )

    employer_sponsored: bool = Field(
        default=False,
        description="Whether employer will sponsor obtaining this certification"
    )


# ============================================================================
# RESPONSIBILITIES & DUTIES
# ============================================================================

class Responsibility(BaseModel):
    """Individual responsibility or duty"""

    description: str = Field(..., description="Description of responsibility")

    category: Optional[str] = Field(
        None,
        description="Category (e.g., 'Technical', 'Leadership', 'Strategy')"
    )

    percentage_of_time: Optional[float] = Field(
        None,
        description="Percentage of time allocated to this responsibility",
        ge=0,
        le=100
    )

    priority: RequirementPriority = Field(
        default=RequirementPriority.REQUIRED,
        description="Priority level of this responsibility"
    )

    required_skills: List[str] = Field(
        default_factory=list,
        description="Skills required for this responsibility"
    )


# ============================================================================
# COMPENSATION & BENEFITS
# ============================================================================

class CompensationInfo(BaseModel):
    """Compensation and benefits information"""

    salary_min: Optional[float] = Field(
        None,
        description="Minimum salary",
        ge=0
    )

    salary_max: Optional[float] = Field(
        None,
        description="Maximum salary",
        ge=0
    )

    salary_currency: Optional[str] = Field(
        None,
        description="Currency code (e.g., 'USD', 'HKD')"
    )

    salary_period: Optional[str] = Field(
        None,
        description="Salary period (e.g., 'annual', 'monthly', 'hourly')"
    )

    bonus_structure: Optional[str] = Field(
        None,
        description="Bonus structure description"
    )

    equity_offered: bool = Field(
        default=False,
        description="Whether equity/stock options are offered"
    )

    benefits_summary: Optional[str] = Field(
        None,
        description="Summary of benefits package"
    )

    benefits_list: List[str] = Field(
        default_factory=list,
        description="Detailed list of benefits"
    )


# ============================================================================
# COMPANY CULTURE & VALUES
# ============================================================================

class CultureInfo(BaseModel):
    """Company culture and values information"""

    company_values: List[str] = Field(
        default_factory=list,
        description="Core company values"
    )

    team_culture: Optional[str] = Field(
        None,
        description="Description of team culture"
    )

    work_environment: Optional[str] = Field(
        None,
        description="Work environment description"
    )

    diversity_statement: Optional[str] = Field(
        None,
        description="Diversity and inclusion statement"
    )

    growth_opportunities: List[str] = Field(
        default_factory=list,
        description="Career growth and development opportunities"
    )

    work_life_balance: Optional[str] = Field(
        None,
        description="Work-life balance description"
    )


# ============================================================================
# APPLICATION PROCESS
# ============================================================================

class ApplicationInfo(BaseModel):
    """Application process information"""

    application_deadline: Optional[date] = Field(
        None,
        description="Application deadline"
    )

    expected_start_date: Optional[date] = Field(
        None,
        description="Expected start date"
    )

    hiring_timeline: Optional[str] = Field(
        None,
        description="Expected hiring timeline"
    )

    interview_process: Optional[str] = Field(
        None,
        description="Description of interview process"
    )

    number_of_positions: int = Field(
        default=1,
        description="Number of open positions",
        ge=1
    )

    contact_email: Optional[EmailStr] = Field(
        None,
        description="Contact email for applications"
    )

    application_url: Optional[HttpUrl] = Field(
        None,
        description="URL to apply"
    )

    visa_sponsorship_available: bool = Field(
        default=False,
        description="Whether visa sponsorship is available"
    )

    required_documents: List[str] = Field(
        default_factory=list,
        description="Required application documents"
    )


# ============================================================================
# COMPANY INFORMATION
# ============================================================================

class CompanyInfo(BaseModel):
    """Information about the hiring company"""

    company_name: Optional[str] = Field(
        None,
        description="Company name (may be confidential)"
    )

    industry: Optional[str] = Field(
        None,
        description="Industry sector"
    )

    company_size: Optional[str] = Field(
        None,
        description="Company size (e.g., '1000-5000 employees')"
    )

    headquarters_location: Optional[str] = Field(
        None,
        description="Headquarters location"
    )

    company_website: Optional[HttpUrl] = Field(
        None,
        description="Company website"
    )

    about_company: Optional[str] = Field(
        None,
        description="Company description",
        max_length=2000
    )

    company_mission: Optional[str] = Field(
        None,
        description="Company mission statement"
    )


# ============================================================================
# JD METADATA
# ============================================================================

class JDMetadata(BaseModel):
    """Metadata about the JD extraction"""

    extraction_timestamp: Optional[str] = Field(
        None,
        description="ISO timestamp of extraction"
    )

    jd_file_name: Optional[str] = Field(
        None,
        description="Original JD filename"
    )

    jd_source: Optional[str] = Field(
        None,
        description="Source of JD (e.g., 'career_site', 'internal_posting')"
    )

    language_detected: Optional[str] = Field(
        None,
        description="Primary language of JD"
    )

    extraction_quality_score: Optional[float] = Field(
        None,
        description="Quality score of extraction (0-100)",
        ge=0,
        le=100
    )

    completeness_score: Optional[float] = Field(
        None,
        description="Completeness score of extracted data (0-100)",
        ge=0,
        le=100
    )

    extraction_warnings: List[str] = Field(
        default_factory=list,
        description="Warnings during extraction"
    )

    extraction_errors: List[str] = Field(
        default_factory=list,
        description="Errors during extraction"
    )


# ============================================================================
# MAIN JOB DESCRIPTION MODEL
# ============================================================================

class JobDescription(BaseModel):
    """
    Complete job description structured data.

    This is the main output model for JD extraction pipeline,
    containing all structured information about a job posting.
    """

    # Core Role Information
    role_info: RoleInfo = Field(..., description="Basic role information")

    # Location & Arrangement
    location_info: Optional[LocationInfo] = Field(
        None,
        description="Location and work arrangement details"
    )

    # Requirements
    skills_required: List[SkillRequirement] = Field(
        default_factory=list,
        description="Required and preferred skills"
    )

    experience_requirements: Optional[ExperienceRequirement] = Field(
        None,
        description="Experience requirements"
    )

    education_requirements: Optional[EducationRequirement] = Field(
        None,
        description="Education requirements"
    )

    certifications_required: List[CertificationRequirement] = Field(
        default_factory=list,
        description="Required and preferred certifications"
    )

    # Responsibilities
    responsibilities: List[Responsibility] = Field(
        default_factory=list,
        description="Key responsibilities and duties"
    )

    # Compensation & Culture
    compensation: Optional[CompensationInfo] = Field(
        None,
        description="Compensation and benefits information"
    )

    culture_info: Optional[CultureInfo] = Field(
        None,
        description="Company culture and values"
    )

    # Company & Application
    company_info: Optional[CompanyInfo] = Field(
        None,
        description="Company information"
    )

    application_info: Optional[ApplicationInfo] = Field(
        None,
        description="Application process information"
    )

    # Additional Information
    additional_requirements: List[str] = Field(
        default_factory=list,
        description="Additional requirements not captured elsewhere"
    )

    nice_to_have: List[str] = Field(
        default_factory=list,
        description="Nice-to-have qualifications"
    )

    disqualifiers: List[str] = Field(
        default_factory=list,
        description="Automatic disqualifiers"
    )

    # Legal & Compliance
    equal_opportunity_statement: Optional[str] = Field(
        None,
        description="Equal opportunity employer statement"
    )

    legal_disclaimers: List[str] = Field(
        default_factory=list,
        description="Legal disclaimers and compliance statements"
    )

    # Division-Specific
    primary_division: Optional[str] = Field(
        None,
        description="Primary AIA division for this role"
    )

    secondary_divisions: List[str] = Field(
        default_factory=list,
        description="Secondary divisions where this role could fit"
    )

    division_specific_requirements: Dict[str, Any] = Field(
        default_factory=dict,
        description="Division-specific requirements and context"
    )

    # Metadata
    metadata: Optional[JDMetadata] = Field(
        None,
        description="Extraction metadata and quality indicators"
    )

    # Raw Data
    raw_text: Optional[str] = Field(
        None,
        description="Raw extracted text from JD",
        exclude=True
    )

    raw_html: Optional[str] = Field(
        None,
        description="Raw HTML if JD was from web",
        exclude=True
    )

    @field_validator("skills_required")
    @classmethod
    def sort_skills_by_priority(cls, v: List[SkillRequirement]) -> List[SkillRequirement]:
        """Sort skills by priority (required first)"""
        priority_order = {
            RequirementPriority.REQUIRED: 0,
            RequirementPriority.PREFERRED: 1,
            RequirementPriority.OPTIONAL: 2,
        }
        return sorted(v, key=lambda x: priority_order.get(x.priority, 999))

    def get_required_skills(self) -> List[SkillRequirement]:
        """Get only required skills"""
        return [s for s in self.skills_required if s.priority == RequirementPriority.REQUIRED]

    def get_preferred_skills(self) -> List[SkillRequirement]:
        """Get only preferred skills"""
        return [s for s in self.skills_required if s.priority == RequirementPriority.PREFERRED]

    def get_skills_by_type(self, skill_type: SkillType) -> List[SkillRequirement]:
        """Get skills of a specific type"""
        return [s for s in self.skills_required if s.skill_type == skill_type]

    def get_all_skill_names(self) -> List[str]:
        """Get all skill names as a flat list"""
        return [skill.skill_name for skill in self.skills_required]

    def get_required_certifications(self) -> List[CertificationRequirement]:
        """Get only required certifications"""
        return [
            c for c in self.certifications_required if c.priority == RequirementPriority.REQUIRED
        ]

    def get_years_experience_range(self) -> tuple[Optional[float], Optional[float]]:
        """Get min and max years of experience required"""
        if self.experience_requirements:
            return (
                self.experience_requirements.minimum_years,
                self.experience_requirements.maximum_years,
            )
        return (None, None)

    def model_dump_minimal(self) -> dict:
        """Return minimal representation without verbose fields"""
        return self.model_dump(
            exclude={
                "raw_text",
                "raw_html",
                "metadata",
                "extraction_warnings",
                "extraction_errors",
            }
        )

    def get_matching_weight_config(self) -> Dict[str, float]:
        """Get recommended matching weights for this JD"""
        # Default weights (can be overridden by division config)
        weights = {
            "experience": 0.30,
            "skills": 0.30,
            "education": 0.20,
            "certifications": 0.20,
        }

        # Adjust based on role characteristics
        if self.role_info.experience_level in [ExperienceLevel.SENIOR, ExperienceLevel.EXECUTIVE]:
            weights["experience"] = 0.40
            weights["skills"] = 0.25

        if self.certifications_required:
            required_certs = self.get_required_certifications()
            if len(required_certs) > 2:
                weights["certifications"] = 0.30
                weights["skills"] = 0.25

        return weights
