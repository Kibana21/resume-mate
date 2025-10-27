# How to Run - Quick Reference

## 🎯 Where to Place Your Resume

Put your `resume.pdf` in this directory:
```
data/sample_cvs/resume.pdf
```

Or use it from any location on your computer.

---

## 🚀 Quick Commands

### 1. Install Dependencies (First Time Only)

```bash
pip install pydantic pydantic-settings dspy-ai openai pdfplumber python-docx loguru
```

### 2. Set Up Azure OpenAI Credentials

Create/edit `.env` file:

```bash
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 3. Run Extraction

**Basic (output to console):**
```bash
python scripts/extract_cv.py data/sample_cvs/resume.pdf
```

**Save to file:**
```bash
python scripts/extract_cv.py data/sample_cvs/resume.pdf --output data/outputs/result.json
```

---

## 📁 Directory Structure

```
resume-mate/
├── data/
│   ├── sample_cvs/          ← PUT YOUR RESUME HERE
│   │   └── resume.pdf
│   └── outputs/             ← RESULTS SAVED HERE
│       └── result.json
├── scripts/
│   └── extract_cv.py        ← RUN THIS SCRIPT
└── .env                     ← YOUR AZURE CREDENTIALS
```

---

## 💡 Common Commands

### Extract from different location:
```bash
python scripts/extract_cv.py /path/to/your/resume.pdf
```

### With industry context:
```bash
python scripts/extract_cv.py data/sample_cvs/resume.pdf --industry technology
```

### With evidence (shows quotes from CV):
```bash
python scripts/extract_cv.py data/sample_cvs/resume.pdf --evidence
```

### Fast mode (no HR insights):
```bash
python scripts/extract_cv.py data/sample_cvs/resume.pdf --no-hr-insights
```

### All options combined:
```bash
python scripts/extract_cv.py data/sample_cvs/resume.pdf \
    --output data/outputs/result.json \
    --industry technology \
    --evidence
```

---

## 📊 What You'll Get

The extraction provides:

✅ **Personal Info**: Name, email, phone, location, LinkedIn
✅ **Work Experience**: All jobs with dates, responsibilities, achievements
✅ **Education**: Degrees, institutions, GPA, honors
✅ **Skills**: Technical, soft, domain-specific (categorized)
✅ **Certifications**: Professional certifications and licenses
✅ **Career Summary**: Total experience, career level
✅ **Division Match**: Best matching AIA business division
✅ **HR Insights**: Career progression, quality scoring, red flags

---

## 🔧 Using in Python Code

```python
from src.config import init_dspy
from src.pipelines import CVExtractionPipeline

# Initialize
lm = init_dspy()
pipeline = CVExtractionPipeline(with_hr_insights=True)

# Extract
profile = pipeline.extract_from_file("data/sample_cvs/resume.pdf")

# Use the data
print(profile.personal_info.full_name)
print(profile.total_years_experience)
print([skill.name for skill in profile.skills])
```

---

## ❗ Troubleshooting

### Error: "AZURE_OPENAI_API_KEY not set"
- Create `.env` file in project root
- Add your Azure credentials
- Restart terminal/Python

### Error: "pdfplumber not installed"
```bash
pip install pdfplumber
```

### Error: "File not found"
```bash
# Check if file exists
ls data/sample_cvs/resume.pdf

# Use full path if needed
python scripts/extract_cv.py /full/path/to/resume.pdf
```

### Extraction is slow or fails
- Check Azure OpenAI quota in Azure Portal
- Ensure deployment name is correct
- Try with `--no-hr-insights` for faster processing

---

## 📚 Full Documentation

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Azure Setup**: [AZURE_SETUP.md](AZURE_SETUP.md)
- **All Changes**: [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)
- **Architecture**: [TECHNICAL_ARCHITECTURE_DSPY.md](TECHNICAL_ARCHITECTURE_DSPY.md)

---

## ✨ Example Output

```
================================================================================
📊 EXTRACTION RESULTS
================================================================================

👤 Personal Information:
   Name: John Doe
   Email: john.doe@email.com
   Location: San Francisco, CA

💼 Experience Summary:
   Total Experience: 8.5 years
   Career Level: Senior

📋 Work Experience:
   1. Senior Software Engineer at Tech Corp
      2020-05 - Present

🎓 Education:
   1. Bachelor of Science
      Stanford University

🔧 Skills (45 total):
   technical: Python, Java, AWS, Docker...

🏢 Division Classification:
   Primary Division: technology
```

---

## 🎯 That's It!

You're ready to extract structured data from any resume!
