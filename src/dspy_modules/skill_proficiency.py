"""
DSPy modules for skill proficiency analysis and classification.

Analyzes skills from CV and determines:
- Years of experience per skill
- Proficiency level (Beginner, Intermediate, Advanced, Expert)
- Usage context and timeline
"""

import dspy
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import json
import re
from loguru import logger


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_flexible_date(date_str: Any) -> Optional[date]:
    """
    Parse date string with flexible format handling.

    Supports:
    - ISO format: YYYY-MM-DD
    - Year-Month: YYYY-MM
    - Year-Season: YYYY-Summer, YYYY-Fall, etc.
    - Year only: YYYY
    - Date objects (returned as-is)
    """
    if not date_str:
        return None

    # Already a date object
    if isinstance(date_str, date):
        return date_str

    # Convert to string
    date_str = str(date_str).strip()

    if not date_str or date_str.lower() in ['none', 'present', 'current', 'not_found']:
        return None

    try:
        # Handle YYYY-MM-DD format
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
                # Handle season names or text
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
    except (ValueError, IndexError, AttributeError) as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")
        return None


# ============================================================================
# SKILL PROFICIENCY SIGNATURES
# ============================================================================

class SkillProficiencyClassification(dspy.Signature):
    """Classify proficiency level for a skill based on context and duration.

    Proficiency Levels:
    - Beginner: <1 year or mentioned briefly
    - Intermediate: 1-3 years, some projects
    - Advanced: 3-5 years, multiple projects, depth
    - Expert: 5+ years, extensive use, leadership/mentoring
    """

    skill_name: str = dspy.InputField(
        desc="Name of the skill to classify"
    )

    years_of_experience: str = dspy.InputField(
        desc="Calculated years using this skill professionally"
    )

    usage_context: str = dspy.InputField(
        desc="Where and how the skill was used (companies, projects, achievements)"
    )

    proficiency_level: str = dspy.OutputField(
        desc="Proficiency level: 'beginner', 'intermediate', 'advanced', or 'expert'"
    )

    reasoning: str = dspy.OutputField(
        desc="Brief explanation for the proficiency classification (1-2 sentences)"
    )

    confidence: str = dspy.OutputField(
        desc="Confidence: 'high' (0.8-1.0), 'medium' (0.5-0.8), or 'low' (0-0.5)"
    )


class BatchSkillProficiencyAnalysis(dspy.Signature):
    """Analyze proficiency for multiple skills at once in JSON format."""

    skills_data: str = dspy.InputField(
        desc="JSON array of skills with usage data"
    )

    proficiency_analysis_json: str = dspy.OutputField(
        desc="""JSON array of skill proficiency analysis. Each object must have:
        {
          "skill_name": "skill name",
          "proficiency_level": "beginner|intermediate|advanced|expert",
          "reasoning": "explanation",
          "confidence": 0.0-1.0,
          "key_indicators": ["indicator1", "indicator2"]
        }
        Return empty array [] if no skills provided."""
    )


# ============================================================================
# SKILL PROFICIENCY MODULES
# ============================================================================

class SkillProficiencyClassifier(dspy.Module):
    """Classify skill proficiency level"""

    def __init__(self):
        super().__init__()
        self.classifier = dspy.ChainOfThought(SkillProficiencyClassification)

    def forward(
        self,
        skill_name: str,
        years_of_experience: float,
        usage_context: str
    ) -> dspy.Prediction:
        """Classify skill proficiency"""
        return self.classifier(
            skill_name=skill_name,
            years_of_experience=str(years_of_experience),
            usage_context=usage_context
        )


class SkillTimelineCalculator:
    """Calculate years of experience for skills based on work history timeline"""

    @staticmethod
    def calculate_years_for_skill(
        skill_name: str,
        work_experiences: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate years of experience for a skill across work history.

        Args:
            skill_name: Name of the skill
            work_experiences: List of work experience dictionaries with dates and technologies

        Returns:
            Dictionary with:
                - years: Total years of experience
                - first_used: First use date
                - last_used: Last use date
                - companies: List of companies where used
        """
        skill_lower = skill_name.lower()
        total_months = 0
        companies_used = []
        first_date = None
        last_date = None

        for exp in work_experiences:
            # Check if skill appears in technologies, responsibilities, or achievements
            skill_mentioned = False

            # Check technologies (try both 'technologies_used' and 'technologies')
            tech_list = exp.get('technologies_used', exp.get('technologies', []))
            if isinstance(tech_list, str):
                # If it's a string, split by comma or pipe (but skip if it's "None" or "N/A")
                if tech_list.lower() not in ['none', 'n/a', 'null', '']:
                    tech_list = [t.strip() for t in tech_list.replace('|', ',').split(',') if t.strip()]
                else:
                    tech_list = []
            elif not tech_list or tech_list is None:
                tech_list = []

            for tech in tech_list:
                if skill_lower in str(tech).lower():
                    skill_mentioned = True
                    break

            # Check responsibilities
            if not skill_mentioned:
                responsibilities = exp.get('responsibilities', [])
                if isinstance(responsibilities, str):
                    # If it's a string, split by pipe or newline
                    responsibilities = [r.strip() for r in responsibilities.replace('\n', '|').split('|') if r.strip()]
                elif not responsibilities:
                    responsibilities = []

                for resp in responsibilities:
                    if skill_lower in str(resp).lower():
                        skill_mentioned = True
                        break

            # If skill mentioned, count the duration
            if skill_mentioned:
                start_date = exp.get('start_date')
                end_date = exp.get('end_date')

                if start_date:
                    try:
                        # Use flexible date parsing
                        start = parse_flexible_date(start_date)
                        end = parse_flexible_date(end_date) if end_date else date.today()

                        if start and end:
                            # Calculate months
                            months = (end.year - start.year) * 12 + (end.month - start.month)
                            total_months += max(months, 0)

                            # Track companies
                            company = exp.get('company_name', '')
                            if company:
                                companies_used.append(company)

                            # Track dates
                            if first_date is None or start < first_date:
                                first_date = start
                            if last_date is None or end > last_date:
                                last_date = end

                    except (ValueError, AttributeError) as e:
                        logger.debug(f"Failed to parse dates for skill {skill_name}: {e}")
                        pass

        years = round(total_months / 12.0, 1) if total_months > 0 else 0.0

        return {
            'years': years,
            'first_used': first_date,
            'last_used': last_date,
            'companies': list(set(companies_used)),
            'mentioned_count': len(companies_used)
        }


class ComprehensiveSkillProficiencyAnalyzer(dspy.Module):
    """
    Comprehensive skill proficiency analysis including:
    - Timeline calculation from work history
    - Proficiency level classification
    - Usage context extraction
    """

    def __init__(self):
        super().__init__()
        self.classifier = SkillProficiencyClassifier()
        self.timeline_calculator = SkillTimelineCalculator()

    def analyze_skills(
        self,
        skills: List[str],
        work_experiences: List[Dict[str, Any]],
        total_years_experience: float = None
    ) -> List[Dict[str, Any]]:
        """
        Analyze proficiency for all skills.

        Args:
            skills: List of skill names
            work_experiences: Work history with dates and technologies
            total_years_experience: Total years of professional experience

        Returns:
            List of skill analysis dictionaries
        """
        skill_analyses = []

        for skill_name in skills:
            # Calculate timeline from work history
            timeline = self.timeline_calculator.calculate_years_for_skill(
                skill_name, work_experiences
            )

            # Build usage context
            companies = timeline.get('companies', [])
            years = timeline.get('years', 0)

            if years == 0 and total_years_experience and total_years_experience > 0:
                # Skill mentioned but no timeline in work history
                # This is common when resumes have a global skills section
                # Estimate based on total experience and use LLM for classification
                usage_context = f"Listed in technical skills | Total experience: {total_years_experience} years"

                try:
                    result = self.classifier(
                        skill_name=skill_name,
                        years_of_experience=total_years_experience,
                        usage_context=usage_context
                    )

                    proficiency_level = result.proficiency_level
                    reasoning = result.reasoning

                    # Map confidence
                    confidence_map = {'high': 0.9, 'medium': 0.7, 'low': 0.5}
                    confidence_str = result.confidence
                    confidence = confidence_map.get(confidence_str.lower(), 0.6) if isinstance(confidence_str, str) else float(confidence_str)

                except Exception as e:
                    # Fallback - estimate proficiency based on total experience
                    if total_years_experience < 2:
                        proficiency_level = 'beginner'
                    elif total_years_experience < 5:
                        proficiency_level = 'intermediate'
                    elif total_years_experience < 10:
                        proficiency_level = 'advanced'
                    else:
                        proficiency_level = 'expert'

                    confidence = 0.6
                    reasoning = f"Estimated based on {total_years_experience} years total experience"

                # Use total experience as proxy
                years = total_years_experience

            elif years == 0:
                # No timeline and no total experience - treat as beginner
                proficiency_level = 'beginner'
                confidence = 0.5
                reasoning = f"{skill_name} is mentioned in CV but experience unclear"
            else:
                # Use DSPy to classify proficiency based on calculated years
                usage_context = f"Used at: {', '.join(companies[:3])} | Duration: {years} years"

                try:
                    result = self.classifier(
                        skill_name=skill_name,
                        years_of_experience=years,
                        usage_context=usage_context
                    )

                    proficiency_level = result.proficiency_level
                    reasoning = result.reasoning

                    # Map confidence
                    confidence_map = {'high': 0.9, 'medium': 0.7, 'low': 0.5}
                    confidence_str = result.confidence
                    confidence = confidence_map.get(confidence_str.lower(), 0.7) if isinstance(confidence_str, str) else float(confidence_str)

                except Exception as e:
                    # Fallback classification based on years
                    if years < 1:
                        proficiency_level = 'beginner'
                    elif years < 3:
                        proficiency_level = 'intermediate'
                    elif years < 5:
                        proficiency_level = 'advanced'
                    else:
                        proficiency_level = 'expert'

                    confidence = 0.6
                    reasoning = f"Based on {years} years of experience"

            skill_analyses.append({
                'skill_name': skill_name,
                'years_of_experience': years,
                'proficiency_level': proficiency_level,
                'first_used': timeline.get('first_used'),
                'last_used': timeline.get('last_used'),
                'usage_context': companies,
                'mentioned_count': timeline.get('mentioned_count', 1),
                'proficiency_confidence': confidence,
                'reasoning': reasoning
            })

        return skill_analyses

    def forward(
        self,
        skills: List[str],
        work_experiences: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """DSPy forward method"""
        return self.analyze_skills(skills, work_experiences)
