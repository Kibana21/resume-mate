"""
DSPy signatures for Job Description (JD) extraction.

Signatures define the input-output interface for extracting structured data from job postings.
"""

import dspy
from typing import List, Optional


# ============================================================================
# ROLE INFORMATION EXTRACTION
# ============================================================================

class RoleInfoExtraction(dspy.Signature):
    """Extract basic role information from job description."""

    jd_text: str = dspy.InputField(
        desc="Job description text or header section"
    )

    job_title: str = dspy.OutputField(
        desc="Job title or position name"
    )

    department: str = dspy.OutputField(
        desc="Department or team (or 'None' if not mentioned)"
    )

    experience_level: str = dspy.OutputField(
        desc="Experience level: 'Entry', 'Junior', 'Mid', 'Senior', 'Lead', 'Principal', or 'Executive'"
    )

    reports_to: str = dspy.OutputField(
        desc="Reporting structure - who this role reports to (or 'None' if not mentioned)"
    )

    team_size: str = dspy.OutputField(
        desc="Team size this role will manage, as integer (or 'None' if not mentioned)"
    )


# ============================================================================
# LOCATION & WORK ARRANGEMENT
# ============================================================================

class LocationInfoExtraction(dspy.Signature):
    """Extract location and work arrangement details."""

    jd_text: str = dspy.InputField(
        desc="Job description text"
    )

    primary_location: str = dspy.OutputField(
        desc="Primary work location - City, Country (or 'None' if not specified)"
    )

    work_arrangement: str = dspy.OutputField(
        desc="Work arrangement: 'On-Site', 'Remote', or 'Hybrid'"
    )

    relocation_assistance: str = dspy.OutputField(
        desc="'Yes' if relocation assistance offered, 'No' otherwise"
    )

    travel_required: str = dspy.OutputField(
        desc="Travel requirements if mentioned (e.g., '10%', 'Occasional') or 'None'"
    )


# ============================================================================
# SKILLS REQUIREMENTS EXTRACTION
# ============================================================================

class RequiredSkillsExtraction(dspy.Signature):
    """Extract required skills from job description."""

    jd_text: str = dspy.InputField(
        desc="Job description text, especially requirements and qualifications sections"
    )

    required_technical_skills: str = dspy.OutputField(
        desc="Required technical skills - comma-separated"
    )

    preferred_technical_skills: str = dspy.OutputField(
        desc="Preferred/nice-to-have technical skills - comma-separated (or 'None')"
    )

    required_soft_skills: str = dspy.OutputField(
        desc="Required soft skills - comma-separated"
    )

    required_domain_knowledge: str = dspy.OutputField(
        desc="Required domain/industry knowledge - comma-separated (or 'None')"
    )


class SkillRequirementWithPriority(dspy.Signature):
    """Extract individual skill requirement with priority classification."""

    jd_text: str = dspy.InputField(
        desc="Job description requirements section"
    )

    target_skill: str = dspy.InputField(
        desc="Specific skill to classify"
    )

    priority: str = dspy.OutputField(
        desc="Priority level: 'Required' (must-have), 'Preferred' (nice-to-have), or 'Optional' (bonus)"
    )

    years_required: str = dspy.OutputField(
        desc="Years of experience required for this skill (or 'None' if not specified)"
    )

    context: str = dspy.OutputField(
        desc="Context or specific application of this skill mentioned in JD (or 'None')"
    )

    evidence: str = dspy.OutputField(
        desc="Direct quote from JD mentioning this skill requirement"
    )


class ComprehensiveSkillsExtraction(dspy.Signature):
    """Extract comprehensive skills breakdown with categorization."""

    jd_text: str = dspy.InputField(
        desc="Complete job description text"
    )

    programming_languages: str = dspy.OutputField(
        desc="Programming languages required/preferred - comma-separated (or 'None')"
    )

    frameworks_libraries: str = dspy.OutputField(
        desc="Frameworks and libraries - comma-separated (or 'None')"
    )

    tools_platforms: str = dspy.OutputField(
        desc="Tools and platforms - comma-separated (or 'None')"
    )

    cloud_technologies: str = dspy.OutputField(
        desc="Cloud technologies (AWS, Azure, GCP, etc.) - comma-separated (or 'None')"
    )

    databases: str = dspy.OutputField(
        desc="Database technologies - comma-separated (or 'None')"
    )

    methodologies: str = dspy.OutputField(
        desc="Methodologies (Agile, DevOps, etc.) - comma-separated (or 'None')"
    )

    soft_skills: str = dspy.OutputField(
        desc="Soft skills (communication, leadership, etc.) - comma-separated"
    )


# ============================================================================
# EXPERIENCE REQUIREMENTS EXTRACTION
# ============================================================================

class ExperienceRequirementsExtraction(dspy.Signature):
    """Extract experience requirements from job description."""

    jd_text: str = dspy.InputField(
        desc="Job description requirements section"
    )

    minimum_years: str = dspy.OutputField(
        desc="Minimum years of total experience required (or 'None' if not specified)"
    )

    preferred_years: str = dspy.OutputField(
        desc="Preferred years of experience (or 'None' if not specified)"
    )

    industry_experience: str = dspy.OutputField(
        desc="Required industry experience - comma-separated (or 'None')"
    )

    role_specific_experience: str = dspy.OutputField(
        desc="Specific role or function experience required - comma-separated (or 'None')"
    )

    management_required: str = dspy.OutputField(
        desc="'Yes' if management experience required, 'No' otherwise"
    )

    management_years: str = dspy.OutputField(
        desc="Years of management experience required if applicable (or 'None')"
    )


# ============================================================================
# EDUCATION REQUIREMENTS EXTRACTION
# ============================================================================

class EducationRequirementsExtraction(dspy.Signature):
    """Extract education requirements from job description."""

    jd_text: str = dspy.InputField(
        desc="Job description requirements section"
    )

    minimum_degree: str = dspy.OutputField(
        desc="Minimum degree required: 'High School', 'Associate', 'Bachelor', 'Master', 'Doctorate', or 'None' if not specified"
    )

    preferred_degree: str = dspy.OutputField(
        desc="Preferred degree level (or 'None' if not specified)"
    )

    required_fields: str = dspy.OutputField(
        desc="Required fields of study - comma-separated (or 'None')"
    )

    preferred_fields: str = dspy.OutputField(
        desc="Preferred fields of study - comma-separated (or 'None')"
    )

    can_substitute_with_experience: str = dspy.OutputField(
        desc="'Yes' if experience can substitute for education, 'No' or 'Not Mentioned' otherwise"
    )


# ============================================================================
# CERTIFICATION REQUIREMENTS EXTRACTION
# ============================================================================

class CertificationRequirementsExtraction(dspy.Signature):
    """Extract certification requirements from job description."""

    jd_text: str = dspy.InputField(
        desc="Job description requirements section"
    )

    required_certifications: str = dspy.OutputField(
        desc="Required certifications - comma-separated (or 'None')"
    )

    preferred_certifications: str = dspy.OutputField(
        desc="Preferred/nice-to-have certifications - comma-separated (or 'None')"
    )

    license_requirements: str = dspy.OutputField(
        desc="Required licenses (e.g., driver's license, professional license) - comma-separated (or 'None')"
    )


# ============================================================================
# RESPONSIBILITIES EXTRACTION
# ============================================================================

class ResponsibilitiesExtraction(dspy.Signature):
    """Extract key responsibilities and duties from job description."""

    jd_text: str = dspy.InputField(
        desc="Job description text, especially responsibilities section"
    )

    core_responsibilities: str = dspy.OutputField(
        desc="Core/primary responsibilities - separated by ' | '"
    )

    technical_responsibilities: str = dspy.OutputField(
        desc="Technical responsibilities - separated by ' | ' (or 'None')"
    )

    leadership_responsibilities: str = dspy.OutputField(
        desc="Leadership/management responsibilities - separated by ' | ' (or 'None')"
    )

    strategic_responsibilities: str = dspy.OutputField(
        desc="Strategic/planning responsibilities - separated by ' | ' (or 'None')"
    )


class ResponsibilityPrioritization(dspy.Signature):
    """Categorize and prioritize responsibilities."""

    responsibilities_text: str = dspy.InputField(
        desc="Responsibilities section from job description"
    )

    critical_duties: str = dspy.OutputField(
        desc="Critical/essential duties that are must-haves - separated by ' | '"
    )

    important_duties: str = dspy.OutputField(
        desc="Important but not critical duties - separated by ' | '"
    )

    additional_duties: str = dspy.OutputField(
        desc="Additional/nice-to-have duties - separated by ' | ' (or 'None')"
    )


# ============================================================================
# COMPENSATION EXTRACTION
# ============================================================================

class CompensationExtraction(dspy.Signature):
    """Extract compensation and benefits information."""

    jd_text: str = dspy.InputField(
        desc="Job description text"
    )

    salary_range: str = dspy.OutputField(
        desc="Salary range if mentioned (e.g., '$100,000 - $150,000') or 'Not Disclosed'"
    )

    salary_currency: str = dspy.OutputField(
        desc="Currency (e.g., 'USD', 'HKD', 'SGD') or 'None' if not mentioned"
    )

    bonus_mentioned: str = dspy.OutputField(
        desc="'Yes' if bonus/incentive mentioned, 'No' otherwise"
    )

    equity_offered: str = dspy.OutputField(
        desc="'Yes' if equity/stock options mentioned, 'No' otherwise"
    )

    key_benefits: str = dspy.OutputField(
        desc="Key benefits mentioned - comma-separated (or 'None')"
    )


# ============================================================================
# COMPANY & CULTURE EXTRACTION
# ============================================================================

class CompanyCultureExtraction(dspy.Signature):
    """Extract company culture and values information."""

    jd_text: str = dspy.InputField(
        desc="Job description text, especially company/culture sections"
    )

    company_values: str = dspy.OutputField(
        desc="Company values mentioned - comma-separated (or 'None')"
    )

    team_culture: str = dspy.OutputField(
        desc="Description of team culture (1-2 sentences, or 'None')"
    )

    work_environment: str = dspy.OutputField(
        desc="Work environment characteristics - comma-separated (or 'None')"
    )

    growth_opportunities: str = dspy.OutputField(
        desc="Career growth opportunities mentioned - comma-separated (or 'None')"
    )


# ============================================================================
# APPLICATION PROCESS EXTRACTION
# ============================================================================

class ApplicationInfoExtraction(dspy.Signature):
    """Extract application process information."""

    jd_text: str = dspy.InputField(
        desc="Job description text"
    )

    application_deadline: str = dspy.OutputField(
        desc="Application deadline in YYYY-MM-DD format (or 'None' if not mentioned)"
    )

    expected_start_date: str = dspy.OutputField(
        desc="Expected start date in YYYY-MM-DD format (or 'ASAP' or 'None')"
    )

    visa_sponsorship: str = dspy.OutputField(
        desc="'Yes' if visa sponsorship available, 'No' if explicitly not available, 'Not Mentioned' otherwise"
    )

    required_documents: str = dspy.OutputField(
        desc="Required application documents - comma-separated (or 'Standard' if not specified)"
    )


# ============================================================================
# DIVISION CLASSIFICATION
# ============================================================================

class JDDivisionClassification(dspy.Signature):
    """Classify job description to AIA business divisions."""

    job_title: str = dspy.InputField(
        desc="Job title from the JD"
    )

    responsibilities_summary: str = dspy.InputField(
        desc="Summary of key responsibilities"
    )

    required_skills: str = dspy.InputField(
        desc="List of required skills"
    )

    available_divisions: str = dspy.InputField(
        desc="Comma-separated list of available divisions"
    )

    primary_division: str = dspy.OutputField(
        desc="Most suitable primary division from available divisions"
    )

    secondary_divisions: str = dspy.OutputField(
        desc="Other suitable divisions - comma-separated (or 'None')"
    )

    confidence: str = dspy.OutputField(
        desc="Confidence in classification: 'High', 'Medium', or 'Low'"
    )

    reasoning: str = dspy.OutputField(
        desc="Brief explanation of division assignment (1-2 sentences)"
    )


# ============================================================================
# REQUIREMENTS PRIORITY SCORING
# ============================================================================

class RequirementsPriorityScoring(dspy.Signature):
    """Score and prioritize different requirement categories for matching weights."""

    jd_text: str = dspy.InputField(
        desc="Complete job description text"
    )

    skills_importance: str = dspy.OutputField(
        desc="Importance of skills matching (0-100 score)"
    )

    experience_importance: str = dspy.OutputField(
        desc="Importance of experience matching (0-100 score)"
    )

    education_importance: str = dspy.OutputField(
        desc="Importance of education matching (0-100 score)"
    )

    certifications_importance: str = dspy.OutputField(
        desc="Importance of certifications matching (0-100 score)"
    )

    reasoning: str = dspy.OutputField(
        desc="Brief explanation of why these weights (2-3 sentences)"
    )


# ============================================================================
# DISQUALIFIERS DETECTION
# ============================================================================

class DisqualifiersExtraction(dspy.Signature):
    """Extract automatic disqualifiers or must-have requirements."""

    jd_text: str = dspy.InputField(
        desc="Job description requirements section"
    )

    absolute_requirements: str = dspy.OutputField(
        desc="Absolute must-have requirements that cannot be substituted - separated by ' | '"
    )

    disqualifying_factors: str = dspy.OutputField(
        desc="Factors that would disqualify a candidate - separated by ' | ' (or 'None')"
    )

    legal_requirements: str = dspy.OutputField(
        desc="Legal requirements (work authorization, background check, etc.) - comma-separated (or 'None')"
    )


# ============================================================================
# IDEAL CANDIDATE PROFILE
# ============================================================================

class IdealCandidateProfile(dspy.Signature):
    """Generate ideal candidate profile from job description."""

    jd_text: str = dspy.InputField(
        desc="Complete job description text"
    )

    ideal_background: str = dspy.OutputField(
        desc="Ideal professional background (2-3 sentences)"
    )

    must_have_skills: str = dspy.OutputField(
        desc="Top 5 must-have skills - comma-separated"
    )

    ideal_experience: str = dspy.OutputField(
        desc="Ideal experience profile (years, industry, roles)"
    )

    ideal_education: str = dspy.OutputField(
        desc="Ideal education background"
    )

    success_indicators: str = dspy.OutputField(
        desc="Key indicators of success in this role - separated by ' | '"
    )


# ============================================================================
# JD QUALITY ASSESSMENT
# ============================================================================

class JDQualityAssessment(dspy.Signature):
    """Assess quality and completeness of job description."""

    jd_text: str = dspy.InputField(
        desc="Complete job description text"
    )

    completeness_score: str = dspy.OutputField(
        desc="Completeness score (0-100)"
    )

    clarity_score: str = dspy.OutputField(
        desc="Clarity score - how clear are requirements (0-100)"
    )

    missing_information: str = dspy.OutputField(
        desc="Important missing information - comma-separated (or 'None')"
    )

    ambiguous_requirements: str = dspy.OutputField(
        desc="Ambiguous or unclear requirements - separated by ' | ' (or 'None')"
    )

    quality_level: str = dspy.OutputField(
        desc="Overall quality: 'Excellent', 'Good', 'Acceptable', or 'Poor'"
    )


# ============================================================================
# MATCHING WEIGHT RECOMMENDATION
# ============================================================================

class MatchingWeightRecommendation(dspy.Signature):
    """Recommend matching weights based on job requirements emphasis."""

    jd_summary: str = dspy.InputField(
        desc="Summary of job requirements and role characteristics"
    )

    experience_level: str = dspy.InputField(
        desc="Experience level of the role"
    )

    division: str = dspy.InputField(
        desc="AIA division for this role"
    )

    experience_weight: str = dspy.OutputField(
        desc="Recommended weight for experience matching (0.0-1.0)"
    )

    skills_weight: str = dspy.OutputField(
        desc="Recommended weight for skills matching (0.0-1.0)"
    )

    education_weight: str = dspy.OutputField(
        desc="Recommended weight for education matching (0.0-1.0)"
    )

    certifications_weight: str = dspy.OutputField(
        desc="Recommended weight for certifications matching (0.0-1.0)"
    )

    reasoning: str = dspy.OutputField(
        desc="Explanation for recommended weights (2-3 sentences)"
    )


# ============================================================================
# STRICT EXTRACTION (NO INFERENCE)
# ============================================================================

class StrictRequirementExtraction(dspy.Signature):
    """Extract requirements in strict mode - only explicitly stated. STRICT MODE: Extract ONLY requirements that are EXPLICITLY and CLEARLY stated. Do NOT infer, interpret, or expand. Use 'NOT_FOUND' if not explicitly mentioned."""

    jd_text: str = dspy.InputField(
        desc="Job description requirements section"
    )

    requirement_type: str = dspy.InputField(
        desc="Type of requirement to extract: 'skills', 'education', 'experience', or 'certifications'"
    )

    required_items: str = dspy.OutputField(
        desc="Items explicitly marked as required - comma-separated (or 'NOT_FOUND')"
    )

    preferred_items: str = dspy.OutputField(
        desc="Items explicitly marked as preferred/nice-to-have - comma-separated (or 'NOT_FOUND')"
    )

    evidence: str = dspy.OutputField(
        desc="Direct quotes from JD for each requirement - separated by ' | '"
    )


# ============================================================================
# KEYWORD EXTRACTION FOR MATCHING
# ============================================================================

class JDKeywordExtraction(dspy.Signature):
    """Extract critical keywords for CV matching."""

    jd_text: str = dspy.InputField(
        desc="Complete job description text"
    )

    critical_keywords: str = dspy.OutputField(
        desc="Top 20 critical keywords that should appear in matching CVs - comma-separated"
    )

    technical_terms: str = dspy.OutputField(
        desc="Important technical terms and jargon - comma-separated"
    )

    action_verbs: str = dspy.OutputField(
        desc="Key action verbs indicating required capabilities - comma-separated"
    )

    domain_terms: str = dspy.OutputField(
        desc="Domain-specific terminology - comma-separated"
    )
