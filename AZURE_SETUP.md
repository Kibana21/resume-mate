# Azure OpenAI Setup Guide

This project is configured to use **Azure OpenAI** exclusively. Follow these steps to set up your environment.

## Prerequisites

1. **Azure Subscription**: You need an active Azure subscription
2. **Azure OpenAI Access**: Request access to Azure OpenAI Service if you haven't already
3. **Resource Created**: Create an Azure OpenAI resource in your Azure portal

## Step 1: Create Azure OpenAI Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Create a resource** → **AI + Machine Learning** → **Azure OpenAI**
3. Fill in the required details:
   - **Subscription**: Select your subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose your preferred region
   - **Name**: Choose a unique name for your resource
   - **Pricing Tier**: Select appropriate tier

4. Click **Review + Create** → **Create**

## Step 2: Deploy a Model

1. Go to your Azure OpenAI resource
2. Navigate to **Model deployments** → **Manage Deployments**
3. Click **Create new deployment**
4. Select:
   - **Model**: GPT-4, GPT-4 Turbo, or GPT-3.5 Turbo
   - **Deployment name**: Choose a name (e.g., `gpt-4`)
   - **Model version**: Select latest available
5. Click **Create**

## Step 3: Get Configuration Details

### API Key
1. In your Azure OpenAI resource, go to **Keys and Endpoint**
2. Copy **KEY 1** or **KEY 2**

### Endpoint
1. In **Keys and Endpoint**, copy the **Endpoint** URL
   - Format: `https://your-resource-name.openai.azure.com/`

### Deployment Name
1. The name you gave to your deployment in Step 2 (e.g., `gpt-4`)

### API Version
1. Use the latest API version: `2024-02-15-preview`
   - Check [Azure OpenAI API versions](https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation) for the most recent

## Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your Azure OpenAI details:
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

## Step 5: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 6: Verify Setup

Test your configuration:

```python
from src.config import init_dspy

# Initialize DSPy with Azure OpenAI
lm = init_dspy()

# Should see success message:
# ✓ DSPy initialized with Azure OpenAI - Deployment: gpt-4, Endpoint: https://...
```

## Step 7: Run Extraction Pipeline

```python
from src.pipelines import CVExtractionPipeline

# Create pipeline
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
print(candidate_profile.personal_info.full_name)
```

## Configuration Options

### Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | `abc123...` | ✅ |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL | `https://my-resource.openai.azure.com/` | ✅ |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Name of your model deployment | `gpt-4` | ✅ |
| `AZURE_OPENAI_API_VERSION` | Azure OpenAI API version | `2024-02-15-preview` | ✅ |
| `LLM_TEMPERATURE` | Temperature for LLM responses (0.0-2.0) | `0.0` | ❌ |
| `LLM_MAX_TOKENS` | Maximum tokens per response | `4000` | ❌ |

### Recommended Models

| Use Case | Recommended Model | Deployment Name |
|----------|-------------------|-----------------|
| Production (Best Quality) | GPT-4 Turbo | `gpt-4` |
| Production (Cost-Effective) | GPT-3.5 Turbo | `gpt-35-turbo` |
| Development/Testing | GPT-3.5 Turbo | `gpt-35-turbo` |

### Temperature Settings

| Temperature | Behavior | Use Case |
|-------------|----------|----------|
| `0.0` | Deterministic, consistent | Structured extraction (recommended) |
| `0.3` | Slightly varied | Creative extraction |
| `0.7` | More varied | Exploratory analysis |

## Troubleshooting

### Error: "AZURE_OPENAI_API_KEY not set"
- Ensure `.env` file exists in project root
- Check that `AZURE_OPENAI_API_KEY` is set in `.env`
- Restart your Python interpreter after updating `.env`

### Error: "AZURE_OPENAI_ENDPOINT not set"
- Verify endpoint URL format: `https://your-resource-name.openai.azure.com/`
- Ensure there's a trailing slash `/`

### Error: "Deployment not found"
- Check that `AZURE_OPENAI_DEPLOYMENT_NAME` matches your actual deployment name
- Verify deployment exists in Azure portal
- Deployment names are case-sensitive

### Error: "API version not supported"
- Update `AZURE_OPENAI_API_VERSION` to latest version
- Check [Azure OpenAI versions](https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation)

### Rate Limiting
- Azure OpenAI has quota limits per deployment
- Check your quota in Azure portal: **Resource → Quotas**
- Consider requesting quota increase if needed

## Cost Optimization

1. **Use GPT-3.5 Turbo for Development**: Much cheaper than GPT-4
2. **Set Appropriate Max Tokens**: Don't request more tokens than needed
3. **Enable Caching**: Set `ENABLE_CACHING=true` to cache results
4. **Batch Processing**: Process multiple CVs in batches
5. **Monitor Usage**: Check Azure portal for usage metrics

## Security Best Practices

1. **Never commit `.env` file**: Already in `.gitignore`
2. **Rotate keys regularly**: Generate new API keys periodically
3. **Use separate deployments**: Development vs Production
4. **Restrict access**: Use Azure RBAC to limit access
5. **Enable monitoring**: Set up alerts in Azure Monitor

## Next Steps

- See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for implementation progress
- See [TECHNICAL_ARCHITECTURE_DSPY.md](TECHNICAL_ARCHITECTURE_DSPY.md) for architecture details
- See [ADVANCED_DSPY_PATTERNS.md](ADVANCED_DSPY_PATTERNS.md) for advanced patterns

## Support

For Azure OpenAI specific issues:
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure OpenAI Quickstart](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart)
- [API Reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)

For project-specific issues:
- Check [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)
- Review code in [src/](src/) directory
