"""
Pydantic data models for Resume Mate platform.

This module exports all data models used throughout the application for
structured data extraction, validation, and matching.
"""

# CV Schema Models
from .cv_schema import (
    # Enums
    ProficiencyLevel,
    SkillCategory,
    EmploymentType,
    EducationLevel,
    CertificationStatus,
    # Models
    PersonalInfo,
    WorkExperience,
    Education,
    Skill,
    LanguageSkill,
    Certification,
    Project,
    Publication,
    Patent,
    Award,
    CVMetadata,
    CandidateProfile,
)

# JD Schema Models
from .jd_schema import (
    # Enums
    RequirementPriority,
    SkillType,
    ExperienceLevel,
    WorkArrangement,
    # Models
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
    CompanyInfo,
    JDMetadata,
    JobDescription,
)

# Evidence Field Models
from .evidence_field import (
    # Generic Models
    EvidenceField,
    EvidenceString,
    EvidenceFloat,
    EvidenceInt,
    EvidenceBool,
    EvidenceDate,
    EvidenceList,
    # Domain-Specific Models
    EvidenceSkill,
    EvidenceWorkExperience,
    EvidenceEducation,
    EvidenceCertification,
    EvidenceBasedCandidateProfile,
    # Utilities
    create_evidence_field,
    merge_evidence_fields,
    validate_evidence_consistency,
)

# HR Insights Models
from .hr_insights import (
    # Enums
    CareerTrajectory,
    RedFlagSeverity,
    QualityLevel,
    # Models
    RedFlag,
    EmploymentGap,
    CareerProgression,
    FormattingQuality,
    CompletenessScore,
    ContentQuality,
    QualityScore,
    KeyStrength,
    CandidateHighlight,
    HRInsights,
    # Utilities
    classify_quality_level,
    detect_job_hopping,
)

# Evaluation Criteria Models
from .evaluation_criteria import (
    # Enums
    MatchLevel,
    CriterionType,
    MatchImpact,
    # Models
    CriterionConfig,
    EvaluationConfig,
    MatchEvidence,
    CriterionEvaluation,
    CVJDEvaluation,
    BatchEvaluationResult,
    # Utilities
    classify_match_level,
    calculate_recommendation,
    create_default_evaluation_config,
)


__all__ = [
    # CV Schema
    "ProficiencyLevel",
    "SkillCategory",
    "EmploymentType",
    "EducationLevel",
    "CertificationStatus",
    "PersonalInfo",
    "WorkExperience",
    "Education",
    "Skill",
    "LanguageSkill",
    "Certification",
    "Project",
    "Publication",
    "Patent",
    "Award",
    "CVMetadata",
    "CandidateProfile",
    # JD Schema
    "RequirementPriority",
    "SkillType",
    "ExperienceLevel",
    "WorkArrangement",
    "RoleInfo",
    "LocationInfo",
    "SkillRequirement",
    "ExperienceRequirement",
    "EducationRequirement",
    "CertificationRequirement",
    "Responsibility",
    "CompensationInfo",
    "CultureInfo",
    "ApplicationInfo",
    "CompanyInfo",
    "JDMetadata",
    "JobDescription",
    # Evidence Fields
    "EvidenceField",
    "EvidenceString",
    "EvidenceFloat",
    "EvidenceInt",
    "EvidenceBool",
    "EvidenceDate",
    "EvidenceList",
    "EvidenceSkill",
    "EvidenceWorkExperience",
    "EvidenceEducation",
    "EvidenceCertification",
    "EvidenceBasedCandidateProfile",
    "create_evidence_field",
    "merge_evidence_fields",
    "validate_evidence_consistency",
    # HR Insights
    "CareerTrajectory",
    "RedFlagSeverity",
    "QualityLevel",
    "RedFlag",
    "EmploymentGap",
    "CareerProgression",
    "FormattingQuality",
    "CompletenessScore",
    "ContentQuality",
    "QualityScore",
    "KeyStrength",
    "CandidateHighlight",
    "HRInsights",
    "classify_quality_level",
    "detect_job_hopping",
    # Evaluation Criteria
    "MatchLevel",
    "CriterionType",
    "MatchImpact",
    "CriterionConfig",
    "EvaluationConfig",
    "MatchEvidence",
    "CriterionEvaluation",
    "CVJDEvaluation",
    "BatchEvaluationResult",
    "classify_match_level",
    "calculate_recommendation",
    "create_default_evaluation_config",
]
