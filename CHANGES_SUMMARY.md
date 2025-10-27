# Configuration Changes Summary - Azure OpenAI Only

## Overview
The project has been simplified to use **Azure OpenAI exclusively**, removing all other LLM provider dependencies (OpenAI, Anthropic).

## Files Modified

### 1. [src/config/settings.py](src/config/settings.py)
**Changes:**
- ✅ Removed `llm_provider` field (no longer needed)
- ✅ Removed `openai_api_key` field
- ✅ Removed `anthropic_api_key` field
- ✅ Removed `Literal` import for provider selection
- ✅ Added `azure_openai_endpoint` field
- ✅ Added `azure_openai_deployment_name` field
- ✅ Added `azure_openai_api_version` field
- ✅ Renamed section from "LLM Configuration" to "Azure OpenAI Configuration"

**New Configuration:**
```python
# Azure OpenAI Configuration
azure_openai_api_key: str = Field(default="", env="AZURE_OPENAI_API_KEY")
azure_openai_endpoint: str = Field(default="", env="AZURE_OPENAI_ENDPOINT")
azure_openai_deployment_name: str = Field(default="gpt-4", env="AZURE_OPENAI_DEPLOYMENT_NAME")
azure_openai_api_version: str = Field(default="2024-02-15-preview", env="AZURE_OPENAI_API_VERSION")

# LLM Parameters
llm_temperature: float = Field(default=0.0, env="LLM_TEMPERATURE")
llm_max_tokens: int = Field(default=4000, env="LLM_MAX_TOKENS")
```

---

### 2. [src/config/dspy_config.py](src/config/dspy_config.py)
**Changes:**
- ✅ Completely rewritten to use only Azure OpenAI
- ✅ Removed `model_provider` parameter
- ✅ Removed OpenAI and Anthropic initialization logic
- ✅ Removed all branching logic for different providers
- ✅ Added proper Azure OpenAI configuration validation
- ✅ Uses `dspy.LM()` with Azure-specific parameters

**New Implementation:**
```python
class DSPyConfig:
    """DSPy configuration and initialization for Azure OpenAI"""

    def __init__(
        self,
        deployment_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        settings = get_settings()

        # Azure OpenAI configuration
        self.api_key = settings.azure_openai_api_key
        self.endpoint = settings.azure_openai_endpoint
        self.deployment_name = deployment_name or settings.azure_openai_deployment_name
        self.api_version = settings.azure_openai_api_version

        # LLM parameters
        self.temperature = temperature if temperature is not None else settings.llm_temperature
        self.max_tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens

    def initialize_lm(self) -> dspy.LM:
        # Validation
        if not self.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY not set")
        if not self.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT not set")
        if not self.deployment_name:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME not set")
        if not self.api_version:
            raise ValueError("AZURE_OPENAI_API_VERSION not set")

        # Initialize Azure OpenAI LM
        self.lm = dspy.LM(
            self.deployment_name,
            api_key=self.api_key,
            api_base=self.endpoint,
            api_version=self.api_version
        )

        dspy.settings.configure(lm=self.lm)
        return self.lm
```

---

### 3. [.env.example](.env.example)
**Changes:**
- ✅ Removed `OPENAI_API_KEY`
- ✅ Removed `ANTHROPIC_API_KEY`
- ✅ Removed `LLM_PROVIDER`
- ✅ Removed `LLM_MODEL`
- ✅ Added `AZURE_OPENAI_ENDPOINT`
- ✅ Added `AZURE_OPENAI_DEPLOYMENT_NAME`
- ✅ Added `AZURE_OPENAI_API_VERSION`

**New Configuration:**
```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# LLM Parameters
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=4000
```

---

### 4. [requirements.txt](requirements.txt)
**Changes:**
- ✅ Updated `dspy` to `dspy-ai>=2.4.0` (official package name)
- ✅ Removed `anthropic>=0.18.0` dependency
- ✅ Kept `openai>=1.12.0` (required by Azure OpenAI SDK)
- ✅ Added `pydantic-settings>=2.0.0` (required for BaseSettings)

---

### 5. [AZURE_SETUP.md](AZURE_SETUP.md) ✨ NEW
**Purpose:** Complete setup guide for Azure OpenAI

**Contents:**
- Prerequisites and Azure resource creation
- Model deployment instructions
- Configuration details extraction
- Environment variable setup
- Verification steps
- Troubleshooting guide
- Cost optimization tips
- Security best practices

---

## Required Environment Variables

You **must** set these 4 environment variables in your `.env` file:

```bash
AZURE_OPENAI_API_KEY=your_actual_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## How to Get These Values

### 1. API Key
- Azure Portal → Your Azure OpenAI Resource → **Keys and Endpoint**
- Copy **KEY 1** or **KEY 2**

### 2. Endpoint
- Same location: **Keys and Endpoint** → **Endpoint**
- Format: `https://your-resource-name.openai.azure.com/`

### 3. Deployment Name
- Azure Portal → Your Azure OpenAI Resource → **Model deployments**
- The name you gave when deploying the model (e.g., `gpt-4`)

### 4. API Version
- Use latest: `2024-02-15-preview`
- Check [Azure docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation) for updates

## Quick Start

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your Azure OpenAI credentials
nano .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test configuration
python -c "from src.config import init_dspy; lm = init_dspy()"
```

## Usage Example

```python
from src.config import init_dspy
from src.pipelines import CVExtractionPipeline

# Initialize DSPy with Azure OpenAI
lm = init_dspy()

# Create extraction pipeline
cv_pipeline = CVExtractionPipeline(
    with_evidence=True,
    with_hr_insights=True
)

# Extract from CV
cv_text = """
John Doe
Software Engineer
john.doe@email.com
...
"""

candidate_profile = cv_pipeline.extract_from_text(cv_text)
print(f"Candidate: {candidate_profile.personal_info.full_name}")
print(f"Experience: {candidate_profile.total_years_experience} years")
print(f"Division: {candidate_profile.primary_division}")
```

## Benefits of Azure OpenAI

1. **Enterprise-Ready**: Data stays in your Azure subscription
2. **Compliance**: Meets enterprise security and compliance requirements
3. **Control**: You control the deployment and scaling
4. **Cost Management**: Predictable pricing with your Azure subscription
5. **Integration**: Seamless integration with other Azure services

## Migration Impact

### ✅ No Breaking Changes for Existing Code

The pipeline interfaces remain the same:
- `CVExtractionPipeline` - works as before
- `JDExtractionPipeline` - works as before
- All DSPy modules - work as before
- All Pydantic models - unchanged

### ⚠️ Configuration Changes Only

Only the configuration layer changed:
- Update `.env` file with Azure credentials
- Remove old OpenAI/Anthropic keys
- Set new Azure-specific variables

## Troubleshooting

### Error: "AZURE_OPENAI_API_KEY not set"
```bash
# Check your .env file exists
ls -la .env

# Verify the variable is set
cat .env | grep AZURE_OPENAI_API_KEY
```

### Error: "Deployment not found"
```bash
# Verify deployment name matches exactly
# Case-sensitive!
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4  # ✅ Correct
AZURE_OPENAI_DEPLOYMENT_NAME=GPT-4  # ❌ Wrong if you deployed as "gpt-4"
```

### Error: "Invalid endpoint"
```bash
# Ensure endpoint has trailing slash
AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com/  # ✅ Correct
AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com   # ❌ Missing /
```

## Next Steps

1. **Setup**: Follow [AZURE_SETUP.md](AZURE_SETUP.md) for detailed setup
2. **Architecture**: Review [TECHNICAL_ARCHITECTURE_DSPY.md](TECHNICAL_ARCHITECTURE_DSPY.md)
3. **Implementation**: Check [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)
4. **Start Coding**: Begin with CV/JD extraction pipelines

## Support

- **Azure OpenAI Docs**: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **Project Docs**: See README.md and documentation files
- **Code Examples**: See src/pipelines/ for usage examples
