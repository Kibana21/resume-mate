"""
Simple script to extract structured data from a CV/Resume.

Usage:
    python scripts/extract_cv.py path/to/resume.pdf

    # Or place your resume in data/sample_cvs/ and run:
    python scripts/extract_cv.py data/sample_cvs/resume.pdf

    # With optional output file:
    python scripts/extract_cv.py path/to/resume.pdf --output data/outputs/result.json
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import init_dspy
from src.pipelines import CVExtractionPipeline
from src.preprocessing import get_file_info


def main():
    parser = argparse.ArgumentParser(description="Extract structured data from CV/Resume")
    parser.add_argument(
        "cv_file",
        help="Path to CV file (PDF, DOCX, or TXT)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file path (default: prints to console)",
        default=None
    )
    parser.add_argument(
        "--evidence",
        action="store_true",
        help="Include evidence spans in extraction"
    )
    parser.add_argument(
        "--no-hr-insights",
        action="store_true",
        help="Disable HR insights generation"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Use strict extraction mode (no inference)"
    )
    parser.add_argument(
        "--industry",
        help="Industry domain (e.g., 'technology', 'finance', 'insurance')",
        default=None
    )

    args = parser.parse_args()

    # Validate file exists
    cv_file = Path(args.cv_file)
    if not cv_file.exists():
        print(f"❌ Error: File not found: {cv_file}")
        sys.exit(1)

    print("=" * 80)
    print("🚀 Resume Mate - CV Extraction")
    print("=" * 80)
    print()

    # Show file info
    try:
        file_info = get_file_info(str(cv_file))
        print(f"📄 File: {file_info['file_name']}")
        print(f"📏 Size: {file_info['file_size_mb']:.2f} MB")
        print(f"📝 Format: {file_info['file_extension']}")
        print()
    except Exception as e:
        print(f"⚠️  Warning: Could not get file info: {e}")
        print()

    # Initialize DSPy
    print("🔧 Initializing Azure OpenAI...")
    try:
        lm = init_dspy()
        print("✅ DSPy initialized successfully")
        print()
    except Exception as e:
        print(f"❌ Error initializing DSPy: {e}")
        print()
        print("💡 Make sure you have set up your .env file with Azure OpenAI credentials:")
        print("   AZURE_OPENAI_API_KEY=...")
        print("   AZURE_OPENAI_ENDPOINT=...")
        print("   AZURE_OPENAI_DEPLOYMENT_NAME=...")
        print("   AZURE_OPENAI_API_VERSION=...")
        sys.exit(1)

    # Create extraction pipeline
    print("🔨 Creating extraction pipeline...")
    pipeline = CVExtractionPipeline(
        with_evidence=args.evidence,
        with_hr_insights=not args.no_hr_insights,
        strict_mode=args.strict,
        industry_domain=args.industry,
    )
    print(f"   • Evidence-based: {args.evidence}")
    print(f"   • HR Insights: {not args.no_hr_insights}")
    print(f"   • Strict mode: {args.strict}")
    if args.industry:
        print(f"   • Industry: {args.industry}")
    print()

    # Extract from CV
    print(f"⚙️  Extracting data from {cv_file.name}...")
    print("   (This may take 30-60 seconds depending on CV complexity)")
    print()

    try:
        candidate_profile = pipeline.extract_from_file(str(cv_file))
        print("✅ Extraction completed successfully!")
        print()
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Display results
    print("=" * 80)
    print("📊 EXTRACTION RESULTS")
    print("=" * 80)
    print()

    # Personal Info
    print("👤 Personal Information:")
    print(f"   Name: {candidate_profile.personal_info.full_name}")
    if candidate_profile.personal_info.email:
        print(f"   Email: {candidate_profile.personal_info.email}")
    if candidate_profile.personal_info.phone:
        print(f"   Phone: {candidate_profile.personal_info.phone}")
    if candidate_profile.personal_info.location:
        print(f"   Location: {candidate_profile.personal_info.location}")
    if candidate_profile.personal_info.linkedin_url:
        print(f"   LinkedIn: {candidate_profile.personal_info.linkedin_url}")
    print()

    # Experience Summary
    print("💼 Experience Summary:")
    print(f"   Total Experience: {candidate_profile.total_years_experience or 'N/A'} years")
    print(f"   Career Level: {candidate_profile.career_level or 'N/A'}")
    print(f"   Number of Positions: {len(candidate_profile.work_experience)}")
    print()

    # Work Experience
    if candidate_profile.work_experience:
        print("📋 Work Experience:")
        for i, exp in enumerate(candidate_profile.work_experience[:3], 1):  # Show top 3
            print(f"   {i}. {exp.job_title} at {exp.company_name}")
            date_range = f"{exp.start_date or 'N/A'} - {exp.end_date or 'Present'}"
            print(f"      {date_range}")
        if len(candidate_profile.work_experience) > 3:
            print(f"   ... and {len(candidate_profile.work_experience) - 3} more positions")
        print()

    # Education
    if candidate_profile.education:
        print("🎓 Education:")
        for i, edu in enumerate(candidate_profile.education, 1):
            print(f"   {i}. {edu.degree}")
            print(f"      {edu.institution_name}")
            if edu.field_of_study:
                print(f"      Field: {edu.field_of_study}")
        print()

    # Skills
    if candidate_profile.skills:
        print(f"🔧 Skills ({len(candidate_profile.skills)} total):")
        # Group by category
        skills_by_category = candidate_profile.get_skill_categories()
        for category, skills in list(skills_by_category.items())[:3]:  # Show top 3 categories
            print(f"   {category.value}: {', '.join(skills[:10])}")
            if len(skills) > 10:
                print(f"      ... and {len(skills) - 10} more")
        print()

    # Certifications
    if candidate_profile.certifications:
        print(f"📜 Certifications ({len(candidate_profile.certifications)}):")
        for i, cert in enumerate(candidate_profile.certifications[:5], 1):
            print(f"   {i}. {cert.name}")
        if len(candidate_profile.certifications) > 5:
            print(f"   ... and {len(candidate_profile.certifications) - 5} more")
        print()

    # Division Classification
    print("🏢 Division Classification:")
    print(f"   Primary Division: {candidate_profile.primary_division or 'N/A'}")
    if candidate_profile.secondary_divisions:
        print(f"   Secondary Divisions: {', '.join(candidate_profile.secondary_divisions)}")
    print()

    # HR Insights
    if candidate_profile.career_progression_analysis or candidate_profile.key_strengths or \
       candidate_profile.job_hopping_assessment or candidate_profile.red_flags or \
       candidate_profile.quality_score is not None:
        print("🎯 HR INSIGHTS")
        print("=" * 80)
        print()

        if candidate_profile.quality_score is not None:
            print(f"📊 Quality Score: {candidate_profile.quality_score:.1f}/100")
            print()

        if candidate_profile.career_progression_analysis:
            print("📈 Career Progression:")
            print(f"   {candidate_profile.career_progression_analysis}")
            print()

        if candidate_profile.job_hopping_assessment:
            print("⏱️  Job Stability:")
            print(f"   {candidate_profile.job_hopping_assessment}")
            print()

        if candidate_profile.key_strengths:
            print("💪 Key Strengths:")
            print(f"   {candidate_profile.key_strengths}")
            print()

        if candidate_profile.red_flags:
            print("⚠️  Red Flags:")
            # Wrap long text
            import textwrap
            wrapped = textwrap.fill(candidate_profile.red_flags, width=76,
                                   initial_indent="   ", subsequent_indent="   ")
            print(wrapped)
            print()

        print("=" * 80)
        print()

    # Save to file if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict
        result_dict = candidate_profile.model_dump(mode='json')

        # Add extraction metadata
        result_dict['extraction_info'] = {
            'timestamp': datetime.now().isoformat(),
            'input_file': str(cv_file.absolute()),
            'pipeline_config': {
                'with_evidence': args.evidence,
                'with_hr_insights': not args.no_hr_insights,
                'strict_mode': args.strict,
                'industry_domain': args.industry,
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, default=str)

        print(f"💾 Results saved to: {output_path}")
        print()

    print("=" * 80)
    print("✨ Extraction complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
