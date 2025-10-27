"""Debug script to check skill proficiency analysis"""
import json
from src.config.dspy_config import DSPyConfig
from src.dspy_modules.cv_extraction_modules import ComprehensiveCVExtractor
from src.preprocessing.pdf_parser import parse_file

# Initialize
config = DSPyConfig()
config.initialize_lm()

# Parse CV
cv_text = parse_file("data/sample_cvs/Resume.pdf")

# Create extractor
extractor = ComprehensiveCVExtractor(with_hr_insights=True)

# Extract
print("Running extraction...")
results = extractor(cv_text=cv_text)

# Check if skill_proficiency_analysis is in results
print(f"\nKeys in results: {list(results.keys())}")

if "skill_proficiency_analysis" in results:
    skill_prof = results["skill_proficiency_analysis"]
    print(f"\nSkill proficiency analysis found! Type: {type(skill_prof)}")
    print(f"Number of skills: {len(skill_prof) if isinstance(skill_prof, list) else 'N/A'}")

    if isinstance(skill_prof, list) and len(skill_prof) > 0:
        print(f"\nFirst skill analysis:")
        print(json.dumps(skill_prof[0], indent=2, default=str))
else:
    print("\nNO skill_proficiency_analysis in results!")

# Check work experience
if "work_experience" in results:
    work_exp = results["work_experience"]
    if len(work_exp) > 0:
        exp = work_exp[0]
        print(f"\nFirst work experience:")
        if isinstance(exp, dict):
            print(f"  Company: {exp.get('company_name')}")
            print(f"  Technologies: {exp.get('technologies', [])}")
            print(f"  Technologies Used: {exp.get('technologies_used', [])}")
        else:
            print(f"  Company: {getattr(exp, 'company_name', 'N/A')}")
            print(f"  Technologies: {getattr(exp, 'technologies', [])}")

# Check technical skills
if "technical_skills" in results:
    tech_skills = results["technical_skills"]
    print(f"\nTechnical skills type: {type(tech_skills)}")
    if hasattr(tech_skills, 'programming_languages'):
        print(f"Programming languages: {getattr(tech_skills, 'programming_languages', '')[:100]}")
