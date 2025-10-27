# Quick Start Guide - Resume Extraction

This guide will help you extract structured data from your resume.pdf file in just a few minutes!

## Prerequisites

1. **Azure OpenAI Account** with a deployed model
2. **Python 3.10+** installed
3. **Your resume.pdf** file ready

## Step 1: Install Dependencies

```bash
# Navigate to project directory
cd /Users/kartik/Documents/Work/Projects/resume-mate/resume-mate

# Install required packages
pip install pydantic pydantic-settings dspy-ai openai pdfplumber python-docx loguru
```

## Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your Azure OpenAI credentials
nano .env
```

Add your Azure OpenAI credentials:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# LLM Parameters
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=4000
```

## Step 3: Place Your Resume

Put your `resume.pdf` in the `data/sample_cvs/` directory:

```bash
# Option 1: Copy your resume there
cp /path/to/your/resume.pdf data/sample_cvs/resume.pdf

# Option 2: Or use it from any location
# You can reference it directly in the command
```

## Step 4: Run Extraction

### Simple Extraction (Console Output)

```bash
python scripts/extract_cv.py data/sample_cvs/resume.pdf
```

### Save Results to JSON

```bash
python scripts/extract_cv.py data/sample_cvs/resume.pdf --output data/outputs/result.json
```

### Advanced Options

```bash
# With evidence spans (shows where data was extracted from)
python scripts/extract_cv.py data/sample_cvs/resume.pdf --evidence

# Specify industry for better domain-specific extraction
python scripts/extract_cv.py data/sample_cvs/resume.pdf --industry technology

# Disable HR insights (faster)
python scripts/extract_cv.py data/sample_cvs/resume.pdf --no-hr-insights

# Strict mode (no inference, only explicit data)
python scripts/extract_cv.py data/sample_cvs/resume.pdf --strict
```

## What You'll See

The script will show:

```
================================================================================
🚀 Resume Mate - CV Extraction
================================================================================

📄 File: resume.pdf
📏 Size: 0.15 MB
📝 Format: .pdf

🔧 Initializing Azure OpenAI...
✅ DSPy initialized successfully

🔨 Creating extraction pipeline...
   • Evidence-based: False
   • HR Insights: True
   • Strict mode: False

⚙️  Extracting data from resume.pdf...
   (This may take 30-60 seconds depending on CV complexity)

✅ Extraction completed successfully!

================================================================================
📊 EXTRACTION RESULTS
================================================================================

👤 Personal Information:
   Name: John Doe
   Email: john.doe@email.com
   Phone: +1-555-0123
   Location: San Francisco, CA
   LinkedIn: https://linkedin.com/in/johndoe

💼 Experience Summary:
   Total Experience: 8.5 years
   Career Level: Senior
   Number of Positions: 4

📋 Work Experience:
   1. Senior Software Engineer at Tech Corp
      2020-05 - Present
   2. Software Engineer at StartupXYZ
      2018-03 - 2020-04
   ... and 2 more positions

🎓 Education:
   1. Bachelor of Science
      Stanford University
      Field: Computer Science

🔧 Skills (45 total):
   technical: Python, Java, JavaScript, React, Node.js, AWS, Docker, Kubernetes...
   soft: Leadership, Communication, Team Management, Problem Solving...

📜 Certifications (3):
   1. AWS Certified Solutions Architect
   2. Certified Scrum Master
   3. Google Cloud Professional

🏢 Division Classification:
   Primary Division: technology
   Secondary Divisions: insurance_operations, finance

💾 Results saved to: data/outputs/result.json

================================================================================
✨ Extraction complete!
================================================================================
```

## Output JSON Structure

The `result.json` file contains:

```json
{
  "personal_info": {
    "full_name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "+1-555-0123",
    "location": "San Francisco, CA",
    ...
  },
  "work_experience": [
    {
      "company_name": "Tech Corp",
      "job_title": "Senior Software Engineer",
      "start_date": "2020-05-01",
      "end_date": null,
      "is_current": true,
      "responsibilities": [...],
      "achievements": [...],
      "technologies_used": [...]
    }
  ],
  "education": [...],
  "skills": [...],
  "certifications": [...],
  "total_years_experience": 8.5,
  "career_level": "Senior",
  "primary_division": "technology",
  ...
}
```

## Using in Python Code

You can also use the pipeline directly in Python:

```python
from src.config import init_dspy
from src.pipelines import CVExtractionPipeline

# Initialize DSPy
lm = init_dspy()

# Create pipeline
pipeline = CVExtractionPipeline(
    with_evidence=True,
    with_hr_insights=True
)

# Extract from file
candidate_profile = pipeline.extract_from_file("data/sample_cvs/resume.pdf")

# Access the data
print(f"Name: {candidate_profile.personal_info.full_name}")
print(f"Experience: {candidate_profile.total_years_experience} years")
print(f"Skills: {len(candidate_profile.skills)}")

# Get specific information
technical_skills = [
    skill.name for skill in candidate_profile.skills
    if skill.category == "technical"
]
print(f"Technical Skills: {', '.join(technical_skills[:10])}")

# Save to JSON
import json
with open("output.json", "w") as f:
    json.dump(candidate_profile.model_dump(mode='json'), f, indent=2, default=str)
```

## Troubleshooting

### "pdfplumber not installed"
```bash
pip install pdfplumber
```

### "AZURE_OPENAI_API_KEY not set"
- Make sure `.env` file exists in project root
- Check that credentials are correctly set
- Restart Python if you just created `.env`

### "File not found"
```bash
# Check file path
ls -la data/sample_cvs/resume.pdf

# Or use absolute path
python scripts/extract_cv.py /full/path/to/resume.pdf
```

### Extraction is slow
- First run is slower (initializing models)
- Complex/long resumes take longer
- Use `--no-hr-insights` for faster extraction
- Check your Azure OpenAI quota/rate limits

### Poor extraction quality
- Try adding `--industry your_industry` for domain-specific extraction
- Use `--evidence` to see what text was extracted from
- Ensure resume is in a standard format (PDF works best)
- Check if text is properly extracted: `python -c "from src.preprocessing import parse_pdf; print(parse_pdf('data/sample_cvs/resume.pdf')[:500])"`

## Next Steps

1. **Extract Multiple CVs**: Create a batch script to process multiple resumes
2. **Job Description Matching**: Extract JD and match with CV
3. **Custom Analysis**: Modify the pipeline for specific requirements
4. **API Integration**: Build a REST API for production use

## Additional Resources

- [AZURE_SETUP.md](AZURE_SETUP.md) - Detailed Azure OpenAI setup
- [TECHNICAL_ARCHITECTURE_DSPY.md](TECHNICAL_ARCHITECTURE_DSPY.md) - Architecture details
- [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) - What's implemented
- [ADVANCED_DSPY_PATTERNS.md](ADVANCED_DSPY_PATTERNS.md) - Advanced patterns

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the documentation files
- Ensure Azure OpenAI is properly configured
