"""
DSPy signatures for CV extraction.

Signatures define the input-output interface for LLM-based extraction tasks.
Each signature specifies what inputs the LLM receives and what outputs it should produce.
"""

import dspy
from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.cv_schema import RedFlag


# ============================================================================
# SIMPLIFIED OUTPUT MODELS (for DSPy with string dates)
# ============================================================================

class WorkExperienceOutput(BaseModel):
    """Simplified work experience for DSPy output with string dates."""
    company_name: str = Field(..., description="Company name")
    job_title: str = Field(..., description="Job title")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM or YYYY)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM, YYYY, or Present)")
    location: Optional[str] = Field(None, description="Location")
    responsibilities: List[str] = Field(default_factory=list, description="Responsibilities")
    achievements: List[str] = Field(default_factory=list, description="Achievements")
    technologies_used: List[str] = Field(default_factory=list, description="Technologies")


class EducationOutput(BaseModel):
    """Simplified education for DSPy output with string dates."""
    institution_name: str = Field(..., description="University/school name")
    degree: str = Field(..., description="Degree type (e.g., Bachelor of Science, MBA)")
    field_of_study: Optional[str] = Field(None, description="Major/specialization")
    start_date: Optional[str] = Field(None, description="Start date (YYYY or YYYY-MM)")
    end_date: Optional[str] = Field(None, description="End date (YYYY or YYYY-MM, or Present)")
    gpa: Optional[str] = Field(None, description="GPA (e.g., 3.8/4.0)")
    honors: List[str] = Field(default_factory=list, description="Honors and awards")


# ============================================================================
# PERSONAL INFORMATION EXTRACTION
# ============================================================================

class PersonalInfoExtraction(dspy.Signature):
    """Extract personal and contact information from CV. Search the entire text carefully - contact info may appear anywhere (header, footer, middle of document, or embedded in content)."""

    personal_section: str = dspy.InputField(
        desc="Text from CV containing personal information. Search thoroughly as email/phone may appear in footer, after work history, or anywhere in the document."
    )

    full_name: str = dspy.OutputField(
        desc="Full name of the candidate"
    )

    email: str = dspy.OutputField(
        desc="Email address (or 'None' if not found)"
    )

    phone: str = dspy.OutputField(
        desc="Primary phone number in standard format. If multiple numbers separated by '/' or ',', return ONLY the first one. Example: '+91-8368423820' not '+91-8368423820/+91-8554828962' (or 'None' if not found)"
    )

    location: str = dspy.OutputField(
        desc="Current location - City, Country (or 'None' if not found)"
    )

    linkedin_url: str = dspy.OutputField(
        desc="LinkedIn profile URL (or 'None' if not found)"
    )

    github_url: str = dspy.OutputField(
        desc="GitHub profile URL (or 'None' if not found)"
    )

    visa_status: str = dspy.OutputField(
        desc="Visa or work authorization status if mentioned (e.g., 'Permanent Residence', 'PR', 'Work Permit', 'Citizen', 'Green Card', etc.) (or 'None' if not found)"
    )


class ProfessionalSummaryExtraction(dspy.Signature):
    """Extract and refine professional summary from CV."""

    summary_section: str = dspy.InputField(
        desc="Professional summary or objective section from CV"
    )

    professional_summary: str = dspy.OutputField(
        desc="Refined professional summary (2-3 sentences, max 200 words)"
    )

    career_level: str = dspy.OutputField(
        desc="Career level: 'Entry', 'Junior', 'Mid', 'Senior', 'Lead', or 'Executive'"
    )

    key_specializations: str = dspy.OutputField(
        desc="Comma-separated list of key specializations/expertise areas"
    )


# ============================================================================
# WORK EXPERIENCE EXTRACTION
# ============================================================================

class WorkExperienceExtraction(dspy.Signature):
    """Extract structured information from a single work experience entry."""

    experience_text: str = dspy.InputField(
        desc="Text of a single work experience entry from CV"
    )

    company_name: str = dspy.OutputField(
        desc="Name of the company"
    )

    job_title: str = dspy.OutputField(
        desc="Job title or position held"
    )

    start_date: str = dspy.OutputField(
        desc="Start date in YYYY-MM format (or 'None' if not found)"
    )

    end_date: str = dspy.OutputField(
        desc="End date in YYYY-MM format, or 'Present' if current, or 'None' if not found"
    )

    location: str = dspy.OutputField(
        desc="Job location - City, Country (or 'None' if not found)"
    )

    responsibilities: str = dspy.OutputField(
        desc="Key responsibilities as bullet points separated by ' | '"
    )

    achievements: str = dspy.OutputField(
        desc="Quantifiable achievements separated by ' | ' (or 'None' if not found)"
    )

    technologies: str = dspy.OutputField(
        desc="Technologies, tools, platforms used - comma-separated (or 'None' if not found)"
    )


class WorkExperienceWithEvidence(dspy.Signature):
    """Extract work experience with evidence spans for explainability."""

    experience_text: str = dspy.InputField(
        desc="Text of a single work experience entry from CV"
    )

    company_name: str = dspy.OutputField(
        desc="Name of the company"
    )

    company_evidence: str = dspy.OutputField(
        desc="Direct quote from CV supporting the company name"
    )

    job_title: str = dspy.OutputField(
        desc="Job title or position held"
    )

    title_evidence: str = dspy.OutputField(
        desc="Direct quote from CV supporting the job title"
    )

    start_date: str = dspy.OutputField(
        desc="Start date in YYYY-MM format"
    )

    end_date: str = dspy.OutputField(
        desc="End date in YYYY-MM format or 'Present' if current"
    )

    date_evidence: str = dspy.OutputField(
        desc="Direct quote from CV showing the dates"
    )

    key_achievements: str = dspy.OutputField(
        desc="Top 3 quantifiable achievements separated by ' | '"
    )


class WorkExperienceListExtraction(dspy.Signature):
    """Extract ALL work experience entries from full CV text."""

    cv_text: str = dspy.InputField(
        desc="Full CV text containing work experience section"
    )

    work_experiences: List[WorkExperienceOutput] = dspy.OutputField(
        desc="""List of work experience objects with company_name, job_title, dates (YYYY-MM format, normalize seasons: Summer→06, Fall→09, Winter→12, Spring→03), location, responsibilities (list), achievements (list), and technologies_used (list).
        Return empty list if no work experience found."""
    )


# ============================================================================
# EDUCATION EXTRACTION
# ============================================================================

class EducationExtraction(dspy.Signature):
    """Extract structured information from a single education entry."""

    education_text: str = dspy.InputField(
        desc="Text of a single education entry from CV"
    )

    institution_name: str = dspy.OutputField(
        desc="Name of educational institution"
    )

    degree: str = dspy.OutputField(
        desc="Degree obtained or in progress (e.g., 'Bachelor of Science', 'MBA')"
    )

    field_of_study: str = dspy.OutputField(
        desc="Major or field of study (or 'None' if not found)"
    )

    start_date: str = dspy.OutputField(
        desc="Start date in YYYY-MM or YYYY format (normalize: Summer→06, Fall→09, Winter→12, Spring→03, or 'None' if not found)"
    )

    end_date: str = dspy.OutputField(
        desc="End date in YYYY-MM or YYYY format (normalize: Summer→06, Fall→09, Winter→12, Spring→03), or 'Present' if current, or 'None' if not found"
    )

    gpa: str = dspy.OutputField(
        desc="GPA if mentioned (or 'None' if not found)"
    )

    honors: str = dspy.OutputField(
        desc="Academic honors/awards - comma-separated (or 'None' if not found)"
    )


class EducationWithEvidence(dspy.Signature):
    """Extract education with evidence spans for explainability."""

    education_text: str = dspy.InputField(
        desc="Text of a single education entry from CV"
    )

    institution_name: str = dspy.OutputField(
        desc="Name of educational institution"
    )

    institution_evidence: str = dspy.OutputField(
        desc="Direct quote from CV supporting the institution name"
    )

    degree: str = dspy.OutputField(
        desc="Degree obtained or in progress"
    )

    degree_evidence: str = dspy.OutputField(
        desc="Direct quote from CV supporting the degree"
    )

    field_of_study: str = dspy.OutputField(
        desc="Major or field of study"
    )

    gpa: str = dspy.OutputField(
        desc="GPA if mentioned, format as 'X.X/Y.Y' or 'None'"
    )


class EducationListExtraction(dspy.Signature):
    """Extract ALL education entries from full CV text."""

    cv_text: str = dspy.InputField(
        desc="Full CV text containing education section"
    )

    education_entries: List[EducationOutput] = dspy.OutputField(
        desc="""List of education objects with institution_name, degree, field_of_study, dates (YYYY or YYYY-MM format, normalize seasons: Summer→06, Fall→09, Winter→12, Spring→03), gpa, and honors (list).
        Return empty list if no education found."""
    )


# ============================================================================
# SKILLS EXTRACTION
# ============================================================================

class TechnicalSkillsExtraction(dspy.Signature):
    """Extract technical skills from CV section."""

    skills_section: str = dspy.InputField(
        desc="Skills section or full CV text"
    )

    programming_languages: str = dspy.OutputField(
        desc="Programming languages - comma-separated (or 'None' if not found)"
    )

    frameworks_libraries: str = dspy.OutputField(
        desc="Frameworks and libraries - comma-separated (or 'None' if not found)"
    )

    tools_platforms: str = dspy.OutputField(
        desc="Tools and platforms - comma-separated (or 'None' if not found)"
    )

    databases: str = dspy.OutputField(
        desc="Database technologies - comma-separated (or 'None' if not found)"
    )

    cloud_services: str = dspy.OutputField(
        desc="Cloud services (AWS, Azure, GCP, etc.) - comma-separated (or 'None' if not found)"
    )

    other_technical: str = dspy.OutputField(
        desc="Other technical skills not in above categories - comma-separated (or 'None' if not found)"
    )


class SkillsWithProficiency(dspy.Signature):
    """Extract skills with proficiency levels inferred from context."""

    skills_text: str = dspy.InputField(
        desc="Skills section and work experience text combined"
    )

    expert_skills: str = dspy.OutputField(
        desc="Skills at expert level (5+ years or explicitly stated) - comma-separated"
    )

    advanced_skills: str = dspy.OutputField(
        desc="Skills at advanced level (3-5 years) - comma-separated"
    )

    intermediate_skills: str = dspy.OutputField(
        desc="Skills at intermediate level (1-3 years) - comma-separated"
    )

    beginner_skills: str = dspy.OutputField(
        desc="Skills at beginner level (<1 year) - comma-separated"
    )


class DomainSkillsExtraction(dspy.Signature):
    """Extract domain-specific skills based on industry context."""

    cv_text: str = dspy.InputField(
        desc="Full CV text or relevant sections"
    )

    industry_domain: str = dspy.InputField(
        desc="Industry domain context (e.g., 'Insurance', 'Technology', 'Finance')"
    )

    domain_expertise: str = dspy.OutputField(
        desc="Domain-specific expertise areas - comma-separated"
    )

    industry_certifications: str = dspy.OutputField(
        desc="Industry-specific certifications mentioned - comma-separated"
    )

    domain_knowledge: str = dspy.OutputField(
        desc="Specialized domain knowledge (regulations, methodologies, standards) - comma-separated"
    )

    business_skills: str = dspy.OutputField(
        desc="Business and soft skills demonstrated - comma-separated"
    )


class SkillWithEvidenceExtraction(dspy.Signature):
    """Extract individual skill with evidence and confidence."""

    cv_text: str = dspy.InputField(
        desc="Full CV text or relevant sections"
    )

    target_skill: str = dspy.InputField(
        desc="Specific skill to search for and validate"
    )

    has_skill: str = dspy.OutputField(
        desc="'Yes' if candidate has this skill, 'No' otherwise"
    )

    confidence: str = dspy.OutputField(
        desc="Confidence level: 'High' (explicitly stated), 'Medium' (implied), or 'Low' (uncertain)"
    )

    evidence: str = dspy.OutputField(
        desc="Direct quote from CV showing this skill (or 'None' if skill not found)"
    )

    proficiency_level: str = dspy.OutputField(
        desc="Inferred proficiency: 'Expert', 'Advanced', 'Intermediate', 'Beginner', or 'Unknown'"
    )

    years_of_experience: str = dspy.OutputField(
        desc="Years of experience with this skill if mentioned (or 'Unknown')"
    )


# ============================================================================
# CERTIFICATIONS EXTRACTION
# ============================================================================

class CertificationExtraction(dspy.Signature):
    """Extract professional certifications and licenses."""

    certification_text: str = dspy.InputField(
        desc="Certifications section or full CV text"
    )

    certification_name: str = dspy.OutputField(
        desc="Name of the certification"
    )

    issuing_organization: str = dspy.OutputField(
        desc="Organization that issued the certification"
    )

    issue_date: str = dspy.OutputField(
        desc="Issue date in YYYY-MM format (or 'None' if not found)"
    )

    expiration_date: str = dspy.OutputField(
        desc="Expiration date in YYYY-MM format, or 'No Expiration', or 'None' if not found"
    )

    credential_id: str = dspy.OutputField(
        desc="Credential ID or license number (or 'None' if not found)"
    )


class CertificationListExtraction(dspy.Signature):
    """Extract all certifications from CV."""

    cv_text: str = dspy.InputField(
        desc="Full CV text or certifications section"
    )

    certifications: str = dspy.OutputField(
        desc="All certifications found, formatted as 'Cert Name (Issuing Org, Year)' separated by ' | '"
    )

    active_certifications: str = dspy.OutputField(
        desc="Currently active/valid certifications - comma-separated"
    )

    expired_certifications: str = dspy.OutputField(
        desc="Expired certifications - comma-separated (or 'None')"
    )


# ============================================================================
# DIVISION CLASSIFICATION
# ============================================================================

class DivisionClassification(dspy.Signature):
    """Classify candidate profile to AIA business divisions."""

    cv_summary: str = dspy.InputField(
        desc="Summary of candidate's background including job titles, skills, and experience"
    )

    available_divisions: str = dspy.InputField(
        desc="Comma-separated list of available divisions to classify into"
    )

    primary_division: str = dspy.OutputField(
        desc="Most suitable primary division from the available divisions"
    )

    secondary_divisions: str = dspy.OutputField(
        desc="Other suitable divisions - comma-separated (or 'None' if only one division fits)"
    )

    confidence: str = dspy.OutputField(
        desc="Confidence in primary division: 'High', 'Medium', or 'Low'"
    )

    reasoning: str = dspy.OutputField(
        desc="Brief explanation (1-2 sentences) of why this division assignment"
    )


# ============================================================================
# HR INSIGHTS EXTRACTION
# ============================================================================

class CareerProgressionAnalysis(dspy.Signature):
    """Analyze career progression pattern from work history."""

    work_history: str = dspy.InputField(
        desc="Work history with job titles and dates formatted as: 'Title @ Company (Start - End)' separated by ' | '"
    )

    trajectory: str = dspy.OutputField(
        desc="Career trajectory: 'Upward', 'Lateral', 'Mixed', 'Downward', 'Stagnant', or 'Early Career'"
    )

    progression_rate: str = dspy.OutputField(
        desc="Progression rate: 'Fast', 'Moderate', 'Slow', or 'None'"
    )

    number_of_promotions: str = dspy.OutputField(
        desc="Number of clear promotions identified (as integer)"
    )

    average_tenure_months: str = dspy.OutputField(
        desc="Average tenure per role in months (as integer)"
    )

    summary: str = dspy.OutputField(
        desc="2-3 sentence summary of career progression pattern"
    )


class JobHoppingDetection(dspy.Signature):
    """Detect job hopping patterns and employment gaps."""

    work_history: str = dspy.InputField(
        desc="Work history with dates formatted as: 'Title @ Company (Start - End)' separated by ' | '"
    )

    is_job_hopping: str = dspy.OutputField(
        desc="'Yes' if pattern of job hopping detected, 'No' otherwise"
    )

    job_hopping_details: str = dspy.OutputField(
        desc="Explanation of job hopping pattern if detected (or 'None')"
    )

    employment_gaps_json: str = dspy.OutputField(
        desc="""JSON array of employment gaps formatted as strings like '2006-01 to 2006-02 (1 month)'.
        Return empty array [] if no gaps. Example: ["2006-01 to 2006-02 (1 month)", "2010-06 to 2010-09 (3 months)"]"""
    )


class RedFlagDetection(dspy.Signature):
    """Detect potential red flags in candidate profile."""

    cv_content: str = dspy.InputField(
        desc="Full CV text or key sections for analysis"
    )

    work_history_summary: str = dspy.InputField(
        desc="Summary of work history with key dates and transitions"
    )

    red_flags: List[RedFlag] = dspy.OutputField(
        desc="""List of red flag objects with category, description, and severity (high/medium/low).
        Categories: 'Employment Gap', 'Frequent Job Changes', 'Lack of Progression', etc.
        Return empty list if no red flags found."""
    )


class QualityScoring(dspy.Signature):
    """Assess overall CV quality and completeness."""

    cv_text: str = dspy.InputField(
        desc="Full CV text"
    )

    formatting_score: str = dspy.OutputField(
        desc="Formatting quality score (0-100)"
    )

    completeness_score: str = dspy.OutputField(
        desc="Completeness score (0-100)"
    )

    content_quality_score: str = dspy.OutputField(
        desc="Content quality score (0-100)"
    )

    formatting_issues: str = dspy.OutputField(
        desc="Formatting issues found - comma-separated (or 'None')"
    )

    missing_sections: str = dspy.OutputField(
        desc="Important missing sections - comma-separated (or 'None')"
    )

    key_strengths: str = dspy.OutputField(
        desc="Top 3 CV strengths - separated by ' | '"
    )

    improvement_suggestions: str = dspy.OutputField(
        desc="Top 3 improvement suggestions - separated by ' | '"
    )


class KeyStrengthsExtraction(dspy.Signature):
    """Extract key strengths and unique selling points of candidate."""

    cv_text: str = dspy.InputField(
        desc="Full CV text with work experience and achievements"
    )

    target_role_context: str = dspy.InputField(
        desc="Target role or industry context (optional, use 'General' if not specified)"
    )

    technical_strengths: str = dspy.OutputField(
        desc="Top 3 technical strengths with evidence - formatted as 'Strength: Evidence' separated by ' | '"
    )

    leadership_strengths: str = dspy.OutputField(
        desc="Leadership/management strengths if applicable - comma-separated (or 'None')"
    )

    unique_selling_points: str = dspy.OutputField(
        desc="Top 3 unique selling points that differentiate this candidate - separated by ' | '"
    )

    career_highlights: str = dspy.OutputField(
        desc="Top 3 career highlights or achievements - separated by ' | '"
    )


# ============================================================================
# EXPERIENCE CALCULATION
# ============================================================================

class TotalExperienceCalculation(dspy.Signature):
    """Calculate total years of professional experience."""

    work_history: str = dspy.InputField(
        desc="Work history with dates formatted as: 'Title @ Company (Start - End)' separated by ' | '"
    )

    total_years: str = dspy.OutputField(
        desc="Total years of professional experience (as decimal, e.g., '5.5')"
    )

    relevant_years: str = dspy.OutputField(
        desc="Years in relevant/similar roles if identifiable (as decimal)"
    )

    calculation_notes: str = dspy.OutputField(
        desc="Notes on calculation (e.g., overlaps excluded, gaps excluded, etc.)"
    )


# ============================================================================
# SECTION DETECTION
# ============================================================================

class CVSectionDetection(dspy.Signature):
    """Detect and classify sections in a CV."""

    cv_text: str = dspy.InputField(
        desc="Full CV text"
    )

    has_work_experience: str = dspy.OutputField(
        desc="'Yes' if work experience section found, 'No' otherwise"
    )

    has_education: str = dspy.OutputField(
        desc="'Yes' if education section found, 'No' otherwise"
    )

    has_skills: str = dspy.OutputField(
        desc="'Yes' if skills section found, 'No' otherwise"
    )

    has_certifications: str = dspy.OutputField(
        desc="'Yes' if certifications section found, 'No' otherwise"
    )

    has_projects: str = dspy.OutputField(
        desc="'Yes' if projects section found, 'No' otherwise"
    )

    has_publications: str = dspy.OutputField(
        desc="'Yes' if publications section found, 'No' otherwise"
    )

    section_structure: str = dspy.OutputField(
        desc="Overall structure quality: 'Excellent', 'Good', 'Acceptable', or 'Poor'"
    )


# ============================================================================
# STRICT EXTRACTION MODE (NO INFERENCE)
# ============================================================================

class StrictPersonalInfoExtraction(dspy.Signature):
    """Extract personal information in strict mode - only explicitly stated information. Extract ONLY information that is EXPLICITLY stated. Do NOT infer or guess. Use 'NOT_FOUND' if information is not clearly present."""

    personal_section: str = dspy.InputField(
        desc="Personal information section text from CV"
    )

    full_name: str = dspy.OutputField(
        desc="Full name EXACTLY as written in CV (or 'NOT_FOUND')"
    )

    email: str = dspy.OutputField(
        desc="Email address EXACTLY as written (or 'NOT_FOUND')"
    )

    phone: str = dspy.OutputField(
        desc="Primary phone number. If multiple numbers are present, return ONLY the first one (or 'NOT_FOUND')"
    )

    location: str = dspy.OutputField(
        desc="Location EXACTLY as written (or 'NOT_FOUND')"
    )


class StrictSkillExtraction(dspy.Signature):
    """Extract skills in strict mode - only explicitly mentioned skills. STRICT MODE: Only return 'Yes' if the EXACT skill name or clear synonym is EXPLICITLY mentioned. Do NOT infer from related skills."""

    cv_text: str = dspy.InputField(
        desc="Full CV text or skills section"
    )

    target_skill: str = dspy.InputField(
        desc="Specific skill to verify"
    )

    skill_found: str = dspy.OutputField(
        desc="'Yes' ONLY if skill is explicitly mentioned, 'No' otherwise"
    )

    exact_mention: str = dspy.OutputField(
        desc="EXACT quote where skill is mentioned (or 'NOT_FOUND')"
    )
