# Sample CVs Directory

## Quick Start

**Place your `resume.pdf` here and run:**

```bash
# From project root directory
python scripts/extract_cv.py data/sample_cvs/resume.pdf
```

## Supported Formats

- ✅ **PDF** (.pdf) - Recommended
- ✅ **DOCX** (.docx)
- ✅ **DOC** (.doc)
- ✅ **TXT** (.txt)

## Example Usage

```bash
# Basic extraction (prints to console)
python scripts/extract_cv.py data/sample_cvs/resume.pdf

# Save to JSON file
python scripts/extract_cv.py data/sample_cvs/resume.pdf --output data/outputs/john_doe.json

# With evidence spans
python scripts/extract_cv.py data/sample_cvs/resume.pdf --evidence

# Specify industry for better extraction
python scripts/extract_cv.py data/sample_cvs/resume.pdf --industry technology
```

## What Gets Extracted

The system extracts:

- ✅ Personal information (name, email, phone, location, LinkedIn, GitHub)
- ✅ Professional summary
- ✅ Work experience (company, title, dates, responsibilities, achievements)
- ✅ Education (degree, institution, GPA, honors)
- ✅ Skills (technical, soft, domain-specific)
- ✅ Certifications and licenses
- ✅ Projects, publications, patents
- ✅ Total years of experience
- ✅ Career level classification
- ✅ AIA division classification
- ✅ HR insights (career progression, red flags, quality scoring)

## Tips for Best Results

1. **Use PDF format** - Best text extraction quality
2. **Standard formatting** - Use common CV layouts
3. **Clear sections** - Label sections clearly (Experience, Education, Skills)
4. **Complete information** - Include dates, locations, details
5. **Readable text** - Avoid images of text, use actual text

## Example File Names

- `john_doe_resume.pdf`
- `jane_smith_cv.pdf`
- `software_engineer_resume.pdf`
- `senior_manager_cv.pdf`

## Processing Time

- Simple CV (1-2 pages): ~30 seconds
- Standard CV (2-3 pages): ~45 seconds
- Complex CV (4+ pages): ~60 seconds

## Output Location

Results are saved to `data/outputs/` directory (if you use `--output` flag)
