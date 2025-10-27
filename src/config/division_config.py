"""Division-specific configurations for AIA business units"""

from typing import Dict, List, Optional


DIVISION_CONTEXTS = {
    "insurance_operations": {
        "keywords": [
            "underwriting",
            "actuarial",
            "claims",
            "risk assessment",
            "reinsurance",
            "mortality",
            "morbidity",
            "loss ratio",
            "premium",
        ],
        "skills": [
            "RMS",
            "Guidewire",
            "Duck Creek",
            "Prophet",
            "MoSes",
            "AXIS",
            "IFRS 17",
            "Solvency II",
        ],
        "certifications": ["CPCU", "ARe", "FCAS", "FSA", "CERA", "AINS", "AIC", "ARM", "FALU"],
        "example_titles": [
            "Underwriter",
            "Actuary",
            "Claims Adjuster",
            "Risk Manager",
            "Pricing Analyst",
        ],
    },
    "investment": {
        "keywords": [
            "portfolio",
            "investment",
            "asset management",
            "equity",
            "fixed income",
            "derivatives",
            "hedge fund",
            "private equity",
        ],
        "skills": [
            "Bloomberg Terminal",
            "FactSet",
            "Eikon",
            "Asset allocation",
            "Financial modeling",
            "Quantitative analysis",
            "Risk management",
        ],
        "certifications": ["CFA", "FRM", "CAIA", "CFP", "CMT", "CPA"],
        "example_titles": [
            "Portfolio Manager",
            "Investment Analyst",
            "Fund Manager",
            "Equity Analyst",
        ],
    },
    "technology": {
        "keywords": [
            "software",
            "engineering",
            "development",
            "cloud",
            "data",
            "devops",
            "agile",
            "api",
        ],
        "skills": [
            "Python",
            "Java",
            "JavaScript",
            "AWS",
            "Azure",
            "GCP",
            "Kubernetes",
            "Docker",
            "React",
            "Node.js",
        ],
        "certifications": [
            "AWS Certified",
            "Azure Certified",
            "GCP Certified",
            "PMP",
            "Scrum Master",
            "CISSP",
        ],
        "example_titles": [
            "Software Engineer",
            "Data Scientist",
            "DevOps Engineer",
            "Cloud Architect",
        ],
    },
    "legal": {
        "keywords": [
            "legal",
            "counsel",
            "attorney",
            "compliance",
            "contracts",
            "litigation",
            "regulatory",
            "governance",
        ],
        "skills": [
            "LexisNexis",
            "Westlaw",
            "Contract law",
            "Insurance law",
            "GDPR",
            "Corporate governance",
            "M&A",
        ],
        "certifications": [
            "Bar admission",
            "CIPP",
            "CIPM",
            "CAMS",
            "CFE",
            "LLM",
        ],
        "example_titles": [
            "Corporate Counsel",
            "Legal Counsel",
            "Compliance Officer",
            "General Counsel",
        ],
    },
    "hr": {
        "keywords": [
            "human resources",
            "talent",
            "recruitment",
            "compensation",
            "benefits",
            "employee relations",
            "performance management",
        ],
        "skills": [
            "Workday",
            "SuccessFactors",
            "Oracle HCM",
            "Talent acquisition",
            "Performance management",
            "Compensation analysis",
        ],
        "certifications": ["SHRM-CP", "SHRM-SCP", "PHR", "SPHR", "GPHR", "CIPD"],
        "example_titles": [
            "HR Business Partner",
            "Recruiter",
            "Compensation Analyst",
            "HR Manager",
        ],
    },
    "sales": {
        "keywords": [
            "sales",
            "business development",
            "account management",
            "revenue",
            "pipeline",
            "quota",
            "CRM",
        ],
        "skills": [
            "Salesforce",
            "HubSpot",
            "Sales enablement",
            "Consultative selling",
            "Relationship management",
        ],
        "certifications": ["LIMRA", "LUTC", "CLU", "ChFC", "Insurance licenses"],
        "example_titles": [
            "Sales Manager",
            "Account Executive",
            "Business Development Manager",
            "Regional Sales Director",
        ],
    },
    "finance": {
        "keywords": [
            "accounting",
            "finance",
            "financial reporting",
            "budgeting",
            "forecasting",
            "audit",
            "tax",
        ],
        "skills": [
            "SAP",
            "Oracle Financials",
            "IFRS",
            "US GAAP",
            "Financial reporting",
            "FP&A",
        ],
        "certifications": ["CPA", "CA", "ACCA", "CMA", "CIA", "CFA"],
        "example_titles": [
            "Accountant",
            "Financial Analyst",
            "Controller",
            "Finance Manager",
        ],
    },
    "customer_service": {
        "keywords": [
            "customer service",
            "support",
            "customer experience",
            "call center",
            "helpdesk",
            "satisfaction",
        ],
        "skills": [
            "Zendesk",
            "Salesforce Service Cloud",
            "Customer service",
            "Conflict resolution",
            "Communication",
        ],
        "certifications": ["HDI", "ITIL", "Customer Service Excellence"],
        "example_titles": [
            "Customer Service Representative",
            "Customer Success Manager",
            "Support Specialist",
        ],
    },
    "marketing": {
        "keywords": [
            "marketing",
            "digital marketing",
            "brand",
            "content",
            "social media",
            "SEO",
            "campaigns",
        ],
        "skills": [
            "Google Analytics",
            "SEO",
            "SEM",
            "Content marketing",
            "Social media",
            "Marketing automation",
        ],
        "certifications": ["Google Ads", "HubSpot", "Facebook Blueprint", "Hootsuite"],
        "example_titles": [
            "Marketing Manager",
            "Digital Marketing Specialist",
            "Content Manager",
            "Brand Manager",
        ],
    },
    "executive": {
        "keywords": ["executive", "leadership", "strategy", "vision", "c-suite", "board", "CEO"],
        "skills": [
            "Strategic planning",
            "Leadership",
            "P&L management",
            "Business transformation",
            "Change management",
        ],
        "certifications": ["MBA", "Executive education", "Board certification"],
        "example_titles": ["CEO", "CFO", "CTO", "COO", "VP", "Managing Director"],
    },
}


DIVISION_EXTRACTION_CONFIG: Dict[str, dict] = {
    "insurance_operations": {
        "strict_mode": True,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["certifications", "regulatory_knowledge", "underwriting_experience"],
        "quality_threshold": 80.0,
        "matching_weights": {
            "experience": 0.40,
            "certifications": 0.25,
            "education": 0.20,
            "skills": 0.15,
        },
    },
    "investment": {
        "strict_mode": True,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["cfa_designation", "investment_performance", "aum_managed"],
        "quality_threshold": 80.0,
        "matching_weights": {
            "experience": 0.35,
            "certifications": 0.30,
            "education": 0.20,
            "skills": 0.15,
        },
    },
    "technology": {
        "strict_mode": False,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["technical_skills", "github_profile", "projects"],
        "quality_threshold": 70.0,
        "matching_weights": {
            "skills": 0.50,
            "experience": 0.25,
            "education": 0.15,
            "certifications": 0.10,
        },
    },
    "legal": {
        "strict_mode": True,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["bar_admission", "practice_areas", "notable_cases"],
        "quality_threshold": 85.0,
        "matching_weights": {
            "experience": 0.35,
            "certifications": 0.30,
            "education": 0.20,
            "skills": 0.15,
        },
    },
    "hr": {
        "strict_mode": False,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["hr_certifications", "hris_experience", "talent_acquisition"],
        "quality_threshold": 75.0,
        "matching_weights": {
            "experience": 0.30,
            "skills": 0.30,
            "certifications": 0.20,
            "education": 0.20,
        },
    },
    "sales": {
        "strict_mode": False,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["sales_performance", "quota_attainment", "crm_skills"],
        "quality_threshold": 70.0,
        "matching_weights": {
            "experience": 0.40,
            "skills": 0.30,
            "certifications": 0.20,
            "education": 0.10,
        },
    },
    "finance": {
        "strict_mode": True,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["cpa_certification", "financial_reporting", "audit_experience"],
        "quality_threshold": 80.0,
        "matching_weights": {
            "certifications": 0.35,
            "experience": 0.30,
            "education": 0.20,
            "skills": 0.15,
        },
    },
    "customer_service": {
        "strict_mode": False,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["customer_service_experience", "satisfaction_scores", "languages"],
        "quality_threshold": 65.0,
        "matching_weights": {
            "experience": 0.35,
            "skills": 0.35,
            "education": 0.15,
            "certifications": 0.15,
        },
    },
    "marketing": {
        "strict_mode": False,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["digital_marketing_skills", "campaigns", "analytics"],
        "quality_threshold": 70.0,
        "matching_weights": {
            "skills": 0.40,
            "experience": 0.30,
            "education": 0.20,
            "certifications": 0.10,
        },
    },
    "executive": {
        "strict_mode": True,
        "evidence_required": True,
        "hr_insights": True,
        "priority_fields": ["leadership_experience", "p_and_l", "strategic_planning"],
        "quality_threshold": 85.0,
        "matching_weights": {
            "experience": 0.50,
            "education": 0.25,
            "skills": 0.15,
            "certifications": 0.10,
        },
    },
}


class DivisionContextProvider:
    """Provide division-specific context to DSPy modules"""

    @staticmethod
    def get_context(division: str) -> str:
        """
        Get context string for division

        Args:
            division: Division identifier

        Returns:
            Formatted context string with division information
        """
        config = DIVISION_CONTEXTS.get(division, {})

        if not config:
            return f"Division: {division} (no specific context available)"

        context = f"""
Division: {division}

Common Skills: {', '.join(config.get('skills', [])[:10])}
Key Certifications: {', '.join(config.get('certifications', [])[:8])}
Example Job Titles: {', '.join(config.get('example_titles', [])[:5])}
Domain Keywords: {', '.join(config.get('keywords', [])[:10])}
"""
        return context.strip()

    @staticmethod
    def enhance_extraction_prompt(base_prompt: str, division: str) -> str:
        """
        Enhance extraction prompt with division context

        Args:
            base_prompt: Base extraction prompt
            division: Division identifier

        Returns:
            Enhanced prompt with division context
        """
        context = DivisionContextProvider.get_context(division)
        return f"{base_prompt}\n\n--- DIVISION CONTEXT ---\n{context}"

    @staticmethod
    def get_division_skills(division: str) -> List[str]:
        """Get list of skills for a division"""
        return DIVISION_CONTEXTS.get(division, {}).get("skills", [])

    @staticmethod
    def get_division_certifications(division: str) -> List[str]:
        """Get list of certifications for a division"""
        return DIVISION_CONTEXTS.get(division, {}).get("certifications", [])


def get_extraction_config(division: str) -> dict:
    """
    Get extraction configuration for division

    Args:
        division: Division identifier

    Returns:
        Division-specific extraction configuration
    """
    return DIVISION_EXTRACTION_CONFIG.get(
        division,
        {
            "strict_mode": False,
            "evidence_required": True,
            "hr_insights": True,
            "quality_threshold": 75.0,
            "matching_weights": {
                "experience": 0.30,
                "skills": 0.30,
                "education": 0.20,
                "certifications": 0.20,
            },
        },
    )


def get_all_divisions() -> List[str]:
    """Get list of all supported divisions"""
    return list(DIVISION_CONTEXTS.keys())
