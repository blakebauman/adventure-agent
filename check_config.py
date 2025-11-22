"""Quick script to validate API key configuration."""

from agent.config import Config

print("=" * 60)
print("Configuration Check")
print("=" * 60)

# Check OpenAI API Key
openai_key = Config.OPENAI_API_KEY
if openai_key:
    if openai_key.startswith("sk-"):
        print("✅ OPENAI_API_KEY: Set and valid format (starts with 'sk-')")
    elif openai_key.startswith("lsv2_pt_"):
        print("❌ OPENAI_API_KEY: ERROR - This is a LangSmith key, not OpenAI!")
        print("   You need to set OPENAI_API_KEY to an OpenAI key (starts with 'sk-')")
        print("   Get one at: https://platform.openai.com/account/api-keys")
    else:
        print(f"⚠️  OPENAI_API_KEY: Set but unexpected format: {openai_key[:10]}...")
else:
    print("❌ OPENAI_API_KEY: Not set!")
    print("   Add it to your .env file: OPENAI_API_KEY=sk-your-key-here")

# Check other config
print(f"\nOPENAI_MODEL: {Config.OPENAI_MODEL}")
print(f"OPENAI_TEMPERATURE: {Config.OPENAI_TEMPERATURE}")

# LangSmith (optional)
if Config.LANGCHAIN_API_KEY:
    print(f"✅ LANGCHAIN_API_KEY: Set (for tracing)")
else:
    print("ℹ️  LANGCHAIN_API_KEY: Not set (optional, for LangSmith tracing)")

# Validate
print("\n" + "=" * 60)
missing = Config.validate()
if missing:
    print(f"❌ Missing required configuration: {missing}")
    print("\nFix by adding to your .env file:")
    for key in missing:
        print(f"  {key}=your-value-here")
else:
    print("✅ All required configuration is present!")
print("=" * 60)

