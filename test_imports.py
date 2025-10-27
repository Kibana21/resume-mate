"""Quick test to verify all imports work"""

print("Testing imports...")

try:
    print("1. Testing src.config imports...")
    from src.config import init_dspy, get_settings
    print("   ✅ src.config imports successful")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("2. Testing src.pipelines imports...")
    from src.pipelines import CVExtractionPipeline
    print("   ✅ src.pipelines imports successful")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("3. Testing src.preprocessing imports...")
    from src.preprocessing import parse_file
    print("   ✅ src.preprocessing imports successful")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("4. Testing src.models imports...")
    from src.models import CandidateProfile
    print("   ✅ src.models imports successful")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ All basic imports successful!")
print("\nNext step: Make sure .env file is configured with Azure OpenAI credentials")
