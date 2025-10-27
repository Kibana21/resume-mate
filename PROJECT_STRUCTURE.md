# Resume Mate - Project Structure

## 📁 Directory Structure

```
resume-mate/
├── README.md                          # Main project documentation
├── TECHNICAL_ARCHITECTURE_DSPY.md    # DSPy technical architecture
├── ADVANCED_DSPY_PATTERNS.md         # Advanced patterns guide
├── PROJECT_STRUCTURE.md              # This file
├── requirements.txt                   # Python dependencies
├── pyproject.toml                    # Poetry configuration
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
│
├── src/                              # Source code
│   ├── __init__.py
│   ├── config/                       # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py              # Application settings (Pydantic)
│   │   ├── dspy_config.py           # DSPy initialization
│   │   └── division_config.py       # Division-specific configs
│   │
│   ├── models/                       # Pydantic data models
│   │   ├── __init__.py
│   │   ├── cv_schema.py             # CV data models
│   │   ├── jd_schema.py             # JD data models
│   │   ├── evidence_field.py        # Evidence-based extraction models
│   │   ├── hr_insights.py           # HR insights models
│   │   ├── evaluation_criteria.py   # Matching criteria models
│   │   └── database.py              # SQLAlchemy models
│   │
│   ├── dspy_modules/                 # DSPy signatures and modules
│   │   ├── __init__.py
│   │   ├── cv_signatures.py         # CV extraction signatures
│   │   ├── jd_signatures.py         # JD extraction signatures
│   │   ├── cv_extraction_modules.py # CV extraction modules
│   │   ├── jd_extraction_modules.py # JD extraction modules
│   │   ├── evidence_extractors.py   # Evidence-based extractors
│   │   ├── hr_insights_signature.py # HR insights extraction
│   │   └── matching_signatures.py   # Matching/evaluation signatures
│   │
│   ├── pipelines/                    # End-to-end pipelines
│   │   ├── __init__.py
│   │   ├── cv_extraction_pipeline.py    # CV extraction pipeline
│   │   ├── jd_extraction_pipeline.py    # JD extraction pipeline
│   │   ├── enhanced_cv_extraction.py    # With evidence & insights
│   │   ├── matching_pipeline.py         # CV-JD matching
│   │   └── division_aware_extraction.py # Division-specific extraction
│   │
│   ├── preprocessing/                # Document preprocessing
│   │   ├── __init__.py
│   │   ├── document_parser.py       # PDF, DOCX, image parsing
│   │   ├── text_cleaner.py          # Text normalization
│   │   ├── ocr_processor.py         # OCR for images
│   │   └── skill_normalizer.py      # Skill/title normalization
│   │
│   ├── evaluation/                   # Evaluation & optimization
│   │   ├── __init__.py
│   │   ├── metrics.py               # Evaluation metrics
│   │   ├── teleprompter_optimization.py # DSPy optimization
│   │   └── training_data_creation.py    # Training data utilities
│   │
│   ├── utils/                        # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py                # Logging configuration
│   │   ├── cache.py                 # Caching utilities
│   │   ├── validators.py            # Data validation
│   │   └── helpers.py               # Helper functions
│   │
│   └── api/                          # FastAPI application
│       ├── __init__.py
│       ├── main.py                  # FastAPI app entry
│       ├── routes/                  # API routes
│       │   ├── __init__.py
│       │   ├── cv_extraction.py     # CV extraction endpoints
│       │   ├── jd_extraction.py     # JD extraction endpoints
│       │   ├── matching.py          # Matching endpoints
│       │   └── health.py            # Health check endpoints
│       ├── dependencies.py          # FastAPI dependencies
│       ├── middleware.py            # API middleware
│       └── schemas.py               # API request/response schemas
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── unit/                        # Unit tests
│   │   ├── test_cv_extraction.py
│   │   ├── test_jd_extraction.py
│   │   ├── test_matching.py
│   │   └── test_evidence_extraction.py
│   ├── integration/                 # Integration tests
│   │   ├── test_pipelines.py
│   │   ├── test_api.py
│   │   └── test_division_aware.py
│   └── fixtures/                    # Test fixtures
│       ├── sample_cv.txt
│       ├── sample_jd.txt
│       └── expected_outputs.json
│
├── data/                             # Data directory
│   ├── sample_cvs/                  # Sample CVs for testing
│   │   ├── .gitkeep
│   │   ├── technology_cv_1.pdf
│   │   ├── insurance_cv_1.pdf
│   │   └── legal_cv_1.pdf
│   ├── sample_jds/                  # Sample JDs for testing
│   │   ├── .gitkeep
│   │   ├── technology_jd_1.txt
│   │   └── insurance_jd_1.txt
│   ├── training_data/               # Training data for optimization
│   │   ├── .gitkeep
│   │   ├── cv_training.json
│   │   └── jd_training.json
│   └── uploads/                     # Runtime uploads (gitignored)
│
├── scripts/                          # Utility scripts
│   ├── init_db.py                   # Initialize database
│   ├── run_extraction.py            # Run extraction on samples
│   ├── optimize_models.py           # Run DSPy optimization
│   ├── generate_training_data.py    # Generate training examples
│   └── benchmark.py                 # Performance benchmarking
│
├── docs/                             # Documentation
│   ├── index.md                     # Documentation home
│   ├── getting_started.md           # Quick start guide
│   ├── api_reference.md             # API documentation
│   ├── division_guide.md            # Division-specific guide
│   └── deployment.md                # Deployment guide
│
├── notebooks/                        # Jupyter notebooks
│   ├── 01_cv_extraction_demo.ipynb
│   ├── 02_jd_extraction_demo.ipynb
│   ├── 03_matching_demo.ipynb
│   ├── 04_optimization_demo.ipynb
│   └── 05_evaluation_demo.ipynb
│
├── logs/                             # Application logs (gitignored)
│   └── .gitkeep
│
└── .github/                          # GitHub configuration
    └── workflows/
        ├── tests.yml                # CI/CD tests
        ├── lint.yml                 # Linting
        └── deploy.yml               # Deployment
```

## 📦 Module Descriptions

### `src/config/`
Configuration management with environment variables, DSPy setup, and division-specific configurations.

**Key Files:**
- `settings.py`: Pydantic settings with env var support
- `dspy_config.py`: DSPy LM initialization
- `division_config.py`: Division contexts and extraction configs

### `src/models/`
Pydantic data models for type-safe data structures.

**Key Files:**
- `cv_schema.py`: CandidateProfile, WorkExperience, Education, Skill models
- `jd_schema.py`: JobDescription, SkillRequirement, ExperienceRequirement models
- `evidence_field.py`: EvidenceField, EvidenceSkill with confidence scores
- `hr_insights.py`: HRInsights, QualityScore models
- `evaluation_criteria.py`: CriterionConfig, MatchEvidence, CVJDEvaluation models

### `src/dspy_modules/`
DSPy signatures and modules for extraction.

**Key Files:**
- `cv_signatures.py`: DSPy signatures for CV extraction
- `cv_extraction_modules.py`: DSPy modules wrapping signatures
- `evidence_extractors.py`: Evidence-based extraction modules
- `hr_insights_signature.py`: HR insights extraction
- `matching_signatures.py`: CV-JD matching signatures

### `src/pipelines/`
End-to-end extraction and matching pipelines.

**Key Files:**
- `cv_extraction_pipeline.py`: Complete CV extraction pipeline
- `jd_extraction_pipeline.py`: Complete JD extraction pipeline
- `enhanced_cv_extraction.py`: With evidence, HR insights, quality scoring
- `matching_pipeline.py`: CV-JD matching with evidence
- `division_aware_extraction.py`: Division-specific extraction

### `src/preprocessing/`
Document parsing and text preprocessing.

**Key Files:**
- `document_parser.py`: Parse PDF, DOCX, images to text
- `text_cleaner.py`: Text normalization and cleaning
- `ocr_processor.py`: OCR for image-based CVs
- `skill_normalizer.py`: Normalize skills, titles, degrees

### `src/evaluation/`
Model evaluation and optimization.

**Key Files:**
- `metrics.py`: Extraction accuracy, F1, precision/recall metrics
- `teleprompter_optimization.py`: DSPy BootstrapFewShot, MIPRO optimization
- `training_data_creation.py`: Create training examples

### `src/api/`
FastAPI REST API.

**Key Files:**
- `main.py`: FastAPI app initialization
- `routes/cv_extraction.py`: POST /api/cv/extract endpoint
- `routes/jd_extraction.py`: POST /api/jd/extract endpoint
- `routes/matching.py`: POST /api/match endpoint

### `tests/`
Comprehensive test suite.

**Directories:**
- `unit/`: Unit tests for individual modules
- `integration/`: End-to-end integration tests
- `fixtures/`: Sample data and expected outputs

### `scripts/`
Utility scripts for common tasks.

**Key Scripts:**
- `run_extraction.py`: Test extraction on sample CVs/JDs
- `optimize_models.py`: Run DSPy optimization
- `generate_training_data.py`: Create training examples
- `benchmark.py`: Performance benchmarking

### `notebooks/`
Jupyter notebooks for exploration and demos.

**Notebooks:**
- `01_cv_extraction_demo.ipynb`: CV extraction walkthrough
- `02_jd_extraction_demo.ipynb`: JD extraction walkthrough
- `03_matching_demo.ipynb`: CV-JD matching demo
- `04_optimization_demo.ipynb`: DSPy optimization tutorial
- `05_evaluation_demo.ipynb`: Evaluation metrics demo

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or using poetry
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 2. Initialize DSPy

```bash
# Run a test extraction
python scripts/run_extraction.py data/sample_cvs/technology_cv_1.pdf
```

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_cv_extraction.py -v
```

### 4. Start API Server

```bash
# Development mode
uvicorn src.api.main:app --reload --port 8000

# Production mode
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Explore with Notebooks

```bash
jupyter notebook notebooks/
```

## 📊 Development Workflow

### Phase 1: Basic Extraction (Week 1)
1. Implement `cv_extraction_pipeline.py`
2. Test with sample CVs
3. Achieve 70%+ accuracy

### Phase 2: Evidence & Insights (Week 2)
1. Add evidence-based extraction
2. Implement HR insights
3. Add quality scoring

### Phase 3: JD & Matching (Week 3)
1. Implement JD extraction
2. Build matching pipeline
3. Add configurable criteria

### Phase 4: Optimization (Week 4)
1. Collect training data
2. Run DSPy optimization
3. Achieve 85%+ accuracy

### Phase 5: API & Integration (Week 5-6)
1. Build FastAPI endpoints
2. Add async processing
3. Deploy to production

## 🔧 Configuration

### Environment Variables
See `.env.example` for all configuration options.

### Division-Specific Configs
Edit `src/config/division_config.py` to customize:
- Matching weights per division
- Quality thresholds
- Priority fields
- Strict mode settings

## 📝 Coding Standards

### Code Style
- **Formatter**: Black (line length 100)
- **Import sorting**: isort
- **Linting**: Flake8, Pylint
- **Type checking**: mypy

### Run Code Quality Checks
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
pylint src/
```

## 🧪 Testing

### Test Coverage Goals
- Unit tests: 80%+ coverage
- Integration tests: Critical paths covered
- E2E tests: Main user flows tested

### Run Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_cv_extraction.py

# With verbose output
pytest -v

# With coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## 📚 Documentation

### Generate Docs
```bash
mkdocs build
mkdocs serve  # View at http://localhost:8000
```

## 🚢 Deployment

See `docs/deployment.md` for production deployment guide.

### Quick Deploy (Docker)
```bash
docker build -t resume-mate:latest .
docker run -p 8000:8000 --env-file .env resume-mate:latest
```

## 🤝 Contributing

1. Create feature branch
2. Write tests
3. Implement feature
4. Run code quality checks
5. Submit PR

## 📞 Support

For questions or issues, contact the AIA Team or open an issue on GitHub.

---

**Last Updated**: 2025-01-27
**Version**: 0.1.0
