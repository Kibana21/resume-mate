"""
DSPy modules for extracting and analyzing achievement metrics.

Uses LLM-based extraction instead of regex for better accuracy and flexibility.
"""

import dspy
from typing import List, Dict, Any
import json


# ============================================================================
# ACHIEVEMENT METRIC EXTRACTION SIGNATURES
# ============================================================================

class AchievementMetricExtraction(dspy.Signature):
    """Extract quantifiable metrics from an achievement statement.

    Identify numbers, percentages, dollar amounts, time periods, team sizes, etc.
    and classify the type of business impact."""

    achievement_text: str = dspy.InputField(
        desc="Achievement statement to analyze for quantifiable metrics"
    )

    has_metrics: str = dspy.OutputField(
        desc="'Yes' if contains quantifiable metrics (numbers, percentages, dollar amounts, etc.), 'No' if purely qualitative"
    )

    metric_value: str = dspy.OutputField(
        desc="Primary numeric value (e.g., '26', '200', '250000'). Use 'None' if no metrics."
    )

    metric_type: str = dspy.OutputField(
        desc="Type of metric: 'percentage', 'currency', 'time_duration', 'count', 'multiplier', or 'None'"
    )

    metric_unit: str = dspy.OutputField(
        desc="Unit of measurement (e.g., 'percent', 'USD', 'months', 'people', 'times'). Use 'None' if not applicable."
    )

    impact_category: str = dspy.OutputField(
        desc="""Category of business impact: 'cost_savings', 'revenue_generation', 'performance_improvement',
        'time_reduction', 'quality_improvement', 'team_growth', 'process_optimization',
        'customer_satisfaction', 'risk_mitigation', or 'None'"""
    )

    context: str = dspy.OutputField(
        desc="Brief context about what was achieved (1-2 sentences)"
    )

    confidence: str = dspy.OutputField(
        desc="Confidence level: 'high' (0.8-1.0), 'medium' (0.5-0.8), or 'low' (0-0.5)"
    )


class BatchAchievementExtraction(dspy.Signature):
    """Extract metrics from multiple achievements at once in JSON format.

    More efficient than processing one at a time."""

    achievements_list: str = dspy.InputField(
        desc="List of achievement statements separated by '|||'"
    )

    metrics_json: str = dspy.OutputField(
        desc="""JSON array of achievement metrics. Each object must have:
        {
          "raw_text": "original achievement text",
          "has_metrics": true/false,
          "metric_value": number or null,
          "metric_type": "percentage|currency|time_duration|count|multiplier" or null,
          "metric_unit": "percent|USD|months|people|times" or null,
          "impact_category": "cost_savings|revenue_generation|..." or null,
          "context": "brief description",
          "confidence": 0.0-1.0
        }
        Return empty array [] if no achievements provided."""
    )


# ============================================================================
# ACHIEVEMENT EXTRACTION MODULES
# ============================================================================

class AchievementMetricExtractor(dspy.Module):
    """Extract metrics from a single achievement statement"""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(AchievementMetricExtraction)

    def forward(self, achievement_text: str) -> dspy.Prediction:
        """Extract metrics from achievement text"""
        return self.extractor(achievement_text=achievement_text)


class BatchAchievementMetricExtractor(dspy.Module):
    """Extract metrics from multiple achievements efficiently"""

    def __init__(self):
        super().__init__()
        self.extractor = dspy.ChainOfThought(BatchAchievementExtraction)

    def forward(self, achievements: List[str]) -> List[Dict[str, Any]]:
        """
        Extract metrics from list of achievements.

        Args:
            achievements: List of achievement text strings

        Returns:
            List of dictionaries with extracted metrics
        """
        if not achievements:
            return []

        # Join achievements with delimiter
        achievements_list = " ||| ".join(achievements)

        # Extract using DSPy
        result = self.extractor(achievements_list=achievements_list)

        # Parse JSON output
        try:
            metrics = json.loads(result.metrics_json)
            if not isinstance(metrics, list):
                return []
            return metrics
        except json.JSONDecodeError:
            # Try to extract JSON from the text
            import re
            json_match = re.search(r'\[.*\]', result.metrics_json, re.DOTALL)
            if json_match:
                try:
                    metrics = json.loads(json_match.group())
                    if isinstance(metrics, list):
                        return metrics
                except json.JSONDecodeError:
                    pass
            return []


class ComprehensiveAchievementAnalyzer(dspy.Module):
    """
    Comprehensive achievement analysis including:
    - Metric extraction
    - Impact categorization
    - Confidence scoring
    - Context summarization
    """

    def __init__(self):
        super().__init__()
        self.batch_extractor = BatchAchievementMetricExtractor()

    def analyze_achievements(
        self,
        achievements: List[str],
        company_name: str = "",
        job_title: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Analyze list of achievements and extract structured metrics.

        Args:
            achievements: List of achievement statements
            company_name: Company where achievements occurred (for context)
            job_title: Job title (for context)

        Returns:
            List of achievement metrics dictionaries
        """
        if not achievements:
            return []

        # Extract metrics using batch extractor
        metrics = self.batch_extractor(achievements=achievements)

        # Add context
        for metric in metrics:
            if company_name:
                metric['company'] = company_name
            if job_title:
                metric['role'] = job_title

        return metrics

    def forward(self, achievements: List[str]) -> List[Dict[str, Any]]:
        """DSPy forward method"""
        return self.analyze_achievements(achievements)
