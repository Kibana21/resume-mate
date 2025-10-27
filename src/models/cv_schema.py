"""
Pydantic models for CV/Resume structured data extraction.

These models define the complete schema for candidate profiles extracted from CVs,
supporting all AIA business divisions with comprehensive field definitions.
"""

from datetime import date
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator


# ============================================================================
# ENUMS FOR CONTROLLED VOCABULARIES
# ============================================================================

class ProficiencyLevel(str, Enum):
    """Skill proficiency levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class SkillCategory(str, Enum):
    """Skill categorization"""
    TECHNICAL = "technical"
    SOFT = "soft"
    LANGUAGE = "language"
    DOMAIN = "domain"
    TOOL = "tool"
    METHODOLOGY = "methodology"


class EmploymentType(str, Enum):
    """Employment type classification"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"


class EducationLevel(str, Enum):
    """Education degree levels"""
    HIGH_SCHOOL = "high_school"
    ASSOCIATE = "associate"
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORATE = "doctorate"
    PROFESSIONAL = "professional"
    CERTIFICATE = "certificate"


class CertificationStatus(str, Enum):
    """Certification status"""
    ACTIVE = "active"
    EXPIRED = "expired"
    IN_PROGRESS = "in_progress"


class MetricType(str, Enum):
    """Types of quantifiable metrics in achievements"""
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    TIME_DURATION = "time_duration"
    COUNT = "count"
    RATIO = "ratio"
    MULTIPLIER = "multiplier"


class ImpactCategory(str, Enum):
    """Categories of business impact"""
    COST_SAVINGS = "cost_savings"
    REVENUE_GENERATION = "revenue_generation"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"
    TIME_REDUCTION = "time_reduction"
    QUALITY_IMPROVEMENT = "quality_improvement"
    TEAM_GROWTH = "team_growth"
    PROCESS_OPTIMIZATION = "process_optimization"
    CUSTOMER_SATISFACTION = "customer_satisfaction"
    RISK_MITIGATION = "risk_mitigation"


# ============================================================================
# PERSONAL INFORMATION MODELS
# ============================================================================

class PersonalInfo(BaseModel):
    """Personal and contact information"""

    full_name: str = Field(..., description="Full name of the candidate")

    email: Optional[EmailStr] = Field(
        None,
        description="Primary email address"
    )

    phone: Optional[str] = Field(
        None,
        description="Primary phone number (LLM-normalized, may contain +, digits, spaces, hyphens, parentheses)",
        min_length=7,
        max_length=30
    )

    location: Optional[str] = Field(
        None,
        description="Current location (City, Country)"
    )

    linkedin_url: Optional[HttpUrl] = Field(
        None,
        description="LinkedIn profile URL"
    )

    github_url: Optional[HttpUrl] = Field(
        None,
        description="GitHub profile URL"
    )

    portfolio_url: Optional[HttpUrl] = Field(
        None,
        description="Personal website or portfolio URL"
    )

    professional_summary: Optional[str] = Field(
        None,
        description="Professional summary or objective statement",
        max_length=1000
    )

    preferred_job_titles: List[str] = Field(
        default_factory=list,
        description="Job titles candidate is seeking"
    )

    willing_to_relocate: Optional[bool] = Field(
        None,
        description="Whether candidate is open to relocation"
    )

    visa_sponsorship_required: Optional[bool] = Field(
        None,
        description="Whether candidate requires visa sponsorship"
    )


# ============================================================================
# WORK EXPERIENCE MODELS
# ============================================================================

class AchievementMetric(BaseModel):
    """Quantifiable metric extracted from an achievement"""

    raw_text: str = Field(..., description="Original achievement text")

    metric_value: Optional[float] = Field(
        None,
        description="Numeric value of the metric (e.g., 26, 200, 250000)"
    )

    metric_type: Optional[MetricType] = Field(
        None,
        description="Type of metric (percentage, currency, time, count, etc.)"
    )

    metric_unit: Optional[str] = Field(
        None,
        description="Unit of measurement (e.g., 'percent', 'USD', 'months', 'developers')"
    )

    impact_category: Optional[ImpactCategory] = Field(
        None,
        description="Category of business impact"
    )

    confidence: float = Field(
        default=0.0,
        description="Confidence score for this metric extraction (0-1)",
        ge=0.0,
        le=1.0
    )

    context: Optional[str] = Field(
        None,
        description="Additional context about the achievement"
    )

    is_quantifiable: bool = Field(
        default=False,
        description="Whether this achievement contains quantifiable metrics"
    )


class WorkExperience(BaseModel):
    """Single work experience entry"""

    company_name: str = Field(..., description="Name of the company")

    job_title: str = Field(..., description="Job title/position held")

    start_date: Optional[date] = Field(
        None,
        description="Start date of employment"
    )

    end_date: Optional[date] = Field(
        None,
        description="End date of employment (None if current)"
    )

    is_current: bool = Field(
        default=False,
        description="Whether this is the current position"
    )

    location: Optional[str] = Field(
        None,
        description="Job location (City, Country)"
    )

    employment_type: Optional[EmploymentType] = Field(
        None,
        description="Type of employment"
    )

    duration_months: Optional[float] = Field(
        None,
        description="Duration in months (calculated)",
        ge=0
    )

    responsibilities: List[str] = Field(
        default_factory=list,
        description="List of key responsibilities and duties"
    )

    achievements: List[str] = Field(
        default_factory=list,
        description="Quantifiable achievements and accomplishments (raw text)"
    )

    achievement_metrics: List[AchievementMetric] = Field(
        default_factory=list,
        description="Structured achievement metrics with quantified impact"
    )

    technologies_used: List[str] = Field(
        default_factory=list,
        description="Technologies, tools, and platforms used"
    )

    skills_demonstrated: List[str] = Field(
        default_factory=list,
        description="Skills demonstrated in this role"
    )

    team_size: Optional[int] = Field(
        None,
        description="Size of team managed (if applicable)",
        ge=0
    )

    reports_to: Optional[str] = Field(
        None,
        description="Reporting structure (e.g., 'CTO', 'VP Engineering')"
    )

    industry: Optional[str] = Field(
        None,
        description="Industry sector of the company"
    )

    company_size: Optional[str] = Field(
        None,
        description="Size of company (e.g., 'Startup', 'Enterprise')"
    )


# ============================================================================
# EDUCATION MODELS
# ============================================================================

class Education(BaseModel):
    """Education entry"""

    institution_name: str = Field(..., description="Name of educational institution")

    degree: str = Field(..., description="Degree obtained or in progress")

    degree_level: Optional[EducationLevel] = Field(
        None,
        description="Standardized degree level"
    )

    field_of_study: Optional[str] = Field(
        None,
        description="Major/field of study"
    )

    start_date: Optional[date] = Field(
        None,
        description="Start date of study"
    )

    end_date: Optional[date] = Field(
        None,
        description="End date or expected graduation date"
    )

    is_current: bool = Field(
        default=False,
        description="Whether currently enrolled"
    )

    gpa: Optional[float] = Field(
        None,
        description="Grade Point Average",
        ge=0.0,
        le=4.0
    )

    gpa_scale: Optional[float] = Field(
        None,
        description="GPA scale (e.g., 4.0, 5.0)",
        ge=0.0
    )

    honors: List[str] = Field(
        default_factory=list,
        description="Academic honors and awards"
    )

    relevant_coursework: List[str] = Field(
        default_factory=list,
        description="Relevant courses completed"
    )

    thesis_title: Optional[str] = Field(
        None,
        description="Title of thesis or dissertation"
    )

    location: Optional[str] = Field(
        None,
        description="Location of institution"
    )


# ============================================================================
# SKILLS MODELS
# ============================================================================

class Skill(BaseModel):
    """Individual skill with proficiency"""

    name: str = Field(..., description="Skill name")

    category: SkillCategory = Field(
        default=SkillCategory.TECHNICAL,
        description="Skill category"
    )

    proficiency_level: Optional[ProficiencyLevel] = Field(
        None,
        description="Proficiency level"
    )

    years_of_experience: Optional[float] = Field(
        None,
        description="Years of experience with this skill",
        ge=0
    )

    last_used: Optional[date] = Field(
        None,
        description="Last time this skill was used professionally"
    )

    endorsed: bool = Field(
        default=False,
        description="Whether skill is endorsed (e.g., on LinkedIn)"
    )

    parent_skill: Optional[str] = Field(
        None,
        description="Parent skill in taxonomy (e.g., 'Python' -> 'Programming')"
    )

    related_skills: List[str] = Field(
        default_factory=list,
        description="Related or complementary skills"
    )

    mentioned_count: int = Field(
        default=0,
        description="Number of times skill appears in CV",
        ge=0
    )

    usage_context: List[str] = Field(
        default_factory=list,
        description="Companies/projects where this skill was used"
    )

    first_used_date: Optional[date] = Field(
        None,
        description="First professional use of this skill (from work history)"
    )

    proficiency_confidence: float = Field(
        default=0.0,
        description="Confidence in proficiency level assessment (0-1)",
        ge=0.0,
        le=1.0
    )


class LanguageSkill(BaseModel):
    """Language proficiency"""

    language: str = Field(..., description="Language name")

    proficiency_level: str = Field(
        ...,
        description="Proficiency level (e.g., 'Native', 'Fluent', 'Professional', 'Basic')"
    )

    can_read: bool = Field(default=True, description="Reading ability")
    can_write: bool = Field(default=True, description="Writing ability")
    can_speak: bool = Field(default=True, description="Speaking ability")

    certification: Optional[str] = Field(
        None,
        description="Language certification (e.g., 'TOEFL 110', 'IELTS 8.0')"
    )


# ============================================================================
# CERTIFICATIONS & LICENSES
# ============================================================================

class Certification(BaseModel):
    """Professional certification or license"""

    name: str = Field(..., description="Certification name")

    issuing_organization: str = Field(..., description="Organization that issued certification")

    issue_date: Optional[date] = Field(
        None,
        description="Date certification was issued"
    )

    expiration_date: Optional[date] = Field(
        None,
        description="Expiration date (None if no expiration)"
    )

    status: CertificationStatus = Field(
        default=CertificationStatus.ACTIVE,
        description="Current status of certification"
    )

    credential_id: Optional[str] = Field(
        None,
        description="Credential ID or license number"
    )

    credential_url: Optional[HttpUrl] = Field(
        None,
        description="URL to verify credential"
    )

    does_not_expire: bool = Field(
        default=False,
        description="Whether certification has no expiration"
    )

    division_relevance: List[str] = Field(
        default_factory=list,
        description="AIA divisions where this certification is relevant"
    )


# ============================================================================
# PROJECTS, PUBLICATIONS, PATENTS
# ============================================================================

class Project(BaseModel):
    """Professional or academic project"""

    title: str = Field(..., description="Project title")

    description: str = Field(..., description="Project description")

    role: Optional[str] = Field(
        None,
        description="Role in the project"
    )

    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")

    technologies_used: List[str] = Field(
        default_factory=list,
        description="Technologies used in project"
    )

    url: Optional[HttpUrl] = Field(
        None,
        description="Project URL or repository"
    )

    outcomes: List[str] = Field(
        default_factory=list,
        description="Key outcomes and results"
    )


class Publication(BaseModel):
    """Academic or professional publication"""

    title: str = Field(..., description="Publication title")

    authors: List[str] = Field(
        default_factory=list,
        description="List of authors"
    )

    publication_date: Optional[date] = Field(
        None,
        description="Date of publication"
    )

    publisher: Optional[str] = Field(
        None,
        description="Publisher or journal name"
    )

    url: Optional[HttpUrl] = Field(
        None,
        description="URL to publication"
    )

    doi: Optional[str] = Field(
        None,
        description="Digital Object Identifier"
    )

    citation_count: Optional[int] = Field(
        None,
        description="Number of citations",
        ge=0
    )


class Patent(BaseModel):
    """Patent information"""

    title: str = Field(..., description="Patent title")

    patent_number: str = Field(..., description="Patent number")

    status: str = Field(
        ...,
        description="Patent status (e.g., 'Granted', 'Pending', 'Filed')"
    )

    issue_date: Optional[date] = Field(
        None,
        description="Date patent was issued"
    )

    inventors: List[str] = Field(
        default_factory=list,
        description="List of inventors"
    )

    description: Optional[str] = Field(
        None,
        description="Patent description"
    )

    url: Optional[HttpUrl] = Field(
        None,
        description="URL to patent record"
    )


class Award(BaseModel):
    """Professional award or recognition"""

    title: str = Field(..., description="Award title")

    issuer: str = Field(..., description="Organization that issued award")

    award_date: Optional[date] = Field(
        None,
        description="Date award was received"
    )

    description: Optional[str] = Field(
        None,
        description="Award description"
    )


# ============================================================================
# METADATA & QUALITY INDICATORS
# ============================================================================

class CVMetadata(BaseModel):
    """Metadata about the CV extraction"""

    extraction_timestamp: Optional[str] = Field(
        None,
        description="ISO timestamp of extraction"
    )

    cv_file_name: Optional[str] = Field(
        None,
        description="Original CV filename"
    )

    cv_format: Optional[str] = Field(
        None,
        description="CV file format (PDF, DOCX, etc.)"
    )

    total_pages: Optional[int] = Field(
        None,
        description="Total number of pages in CV",
        ge=0
    )

    language_detected: Optional[str] = Field(
        None,
        description="Primary language of CV"
    )

    parsing_quality_score: Optional[float] = Field(
        None,
        description="Quality score of parsing (0-100)",
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
# MAIN CANDIDATE PROFILE MODEL
# ============================================================================

class CandidateProfile(BaseModel):
    """
    Complete candidate profile extracted from CV.

    This is the main output model for CV extraction pipeline,
    containing all structured information about a candidate.
    """

    # Core Information
    personal_info: PersonalInfo = Field(..., description="Personal and contact information")

    # Experience & Education
    work_experience: List[WorkExperience] = Field(
        default_factory=list,
        description="Work experience history (reverse chronological)"
    )

    education: List[Education] = Field(
        default_factory=list,
        description="Education history (reverse chronological)"
    )

    # Skills
    skills: List[Skill] = Field(
        default_factory=list,
        description="Technical and soft skills"
    )

    languages: List[LanguageSkill] = Field(
        default_factory=list,
        description="Language proficiencies"
    )

    # Certifications & Credentials
    certifications: List[Certification] = Field(
        default_factory=list,
        description="Professional certifications and licenses"
    )

    # Additional Sections
    projects: List[Project] = Field(
        default_factory=list,
        description="Notable projects"
    )

    publications: List[Publication] = Field(
        default_factory=list,
        description="Academic or professional publications"
    )

    patents: List[Patent] = Field(
        default_factory=list,
        description="Patents held"
    )

    awards: List[Award] = Field(
        default_factory=list,
        description="Professional awards and recognition"
    )

    # Computed Fields
    total_years_experience: Optional[float] = Field(
        None,
        description="Total years of professional experience",
        ge=0
    )

    years_in_current_role: Optional[float] = Field(
        None,
        description="Years in current position",
        ge=0
    )

    career_level: Optional[str] = Field(
        None,
        description="Career level (e.g., 'Entry', 'Mid', 'Senior', 'Executive')"
    )

    primary_division: Optional[str] = Field(
        None,
        description="Primary AIA division match"
    )

    secondary_divisions: List[str] = Field(
        default_factory=list,
        description="Secondary AIA divisions where candidate could fit"
    )

    # HR Insights
    career_progression_analysis: Optional[str] = Field(
        None,
        description="Analysis of career progression and growth trajectory"
    )

    job_hopping_assessment: Optional[str] = Field(
        None,
        description="Assessment of job stability and tenure patterns"
    )

    red_flags: Optional[str] = Field(
        None,
        description="Potential concerns or red flags identified in CV"
    )

    quality_score: Optional[float] = Field(
        None,
        description="Overall CV quality score (0-100)",
        ge=0,
        le=100
    )

    key_strengths: Optional[str] = Field(
        None,
        description="Key strengths and unique selling points of the candidate"
    )

    # Metadata
    metadata: Optional[CVMetadata] = Field(
        None,
        description="Extraction metadata and quality indicators"
    )

    # Raw Data (optional)
    raw_text: Optional[str] = Field(
        None,
        description="Raw extracted text from CV",
        exclude=True  # Exclude from API responses by default
    )

    @field_validator("work_experience")
    @classmethod
    def sort_work_experience(cls, v: List[WorkExperience]) -> List[WorkExperience]:
        """Sort work experience by start date (most recent first)"""
        return sorted(
            v,
            key=lambda x: x.start_date if x.start_date else date.min,
            reverse=True
        )

    @field_validator("education")
    @classmethod
    def sort_education(cls, v: List[Education]) -> List[Education]:
        """Sort education by end date (most recent first)"""
        return sorted(
            v,
            key=lambda x: x.end_date if x.end_date else date.min,
            reverse=True
        )

    def model_dump_minimal(self) -> dict:
        """Return minimal representation without verbose fields"""
        return self.model_dump(
            exclude={"raw_text", "metadata", "extraction_warnings", "extraction_errors"}
        )

    def get_all_skills(self) -> List[str]:
        """Get all skill names as a flat list"""
        return [skill.name for skill in self.skills]

    def get_skill_categories(self) -> dict[str, List[str]]:
        """Get skills grouped by category"""
        categories: dict[str, List[str]] = {}
        for skill in self.skills:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill.name)
        return categories

    def get_active_certifications(self) -> List[Certification]:
        """Get only active certifications"""
        return [cert for cert in self.certifications if cert.status == CertificationStatus.ACTIVE]

    def calculate_total_experience(self) -> float:
        """Calculate total years of experience from work history"""
        total_months = sum(
            exp.duration_months for exp in self.work_experience if exp.duration_months
        )
        return round(total_months / 12, 1)
