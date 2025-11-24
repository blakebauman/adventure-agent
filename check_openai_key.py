#!/usr/bin/env python3
"""Quick script to check OPENAI_API_KEY format and value."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Load .env manually first to see raw value
from dotenv import load_dotenv
load_dotenv()

raw_key = os.getenv("OPENAI_API_KEY")

print("=" * 60)
print("OPENAI_API_KEY Diagnostic")
print("=" * 60)

if not raw_key:
    print("❌ OPENAI_API_KEY: Not set in environment!")
    print("\nTo fix:")
    print("1. Create a .env file in the project root")
    print("2. Add: OPENAI_API_KEY=sk-your-actual-key-here")
    print("3. Make sure there are NO quotes around the key")
    print("4. Make sure there are NO spaces around the = sign")
    sys.exit(1)

# Check for common issues
print(f"✅ OPENAI_API_KEY is set")
print(f"   Length: {len(raw_key)} characters")
print(f"   First 20 chars: {raw_key[:20]}...")

issues = []

# Check format
if not raw_key.startswith("sk-"):
    if raw_key.startswith("k-proj-"):
        issues.append("⚠️  Key starts with 'k-proj-' - should start with 'sk-proj-'")
        print("   ⚠️  This looks like a truncated or malformed key!")
        print("   OpenAI keys should start with 'sk-' or 'sk-proj-'")
    elif raw_key.startswith("lsv2_pt_"):
        issues.append("❌ This is a LangSmith key, not an OpenAI key!")
        print("   ❌ ERROR: This is a LangSmith API key, not OpenAI!")
        print("   Get an OpenAI key from: https://platform.openai.com/account/api-keys")
    else:
        issues.append(f"⚠️  Unexpected format - starts with '{raw_key[:5]}'")
        print(f"   ⚠️  Unexpected format: starts with '{raw_key[:5]}'")
        print("   OpenAI keys should start with 'sk-' or 'sk-proj-'")
else:
    print("   ✅ Format looks correct (starts with 'sk-')")

# Check for quotes
if raw_key.startswith('"') or raw_key.startswith("'"):
    issues.append("❌ Key has quotes around it - remove them!")
    print("   ❌ Key has quotes - remove quotes from .env file")

if raw_key.endswith('"') or raw_key.endswith("'"):
    issues.append("❌ Key has quotes around it - remove them!")
    print("   ❌ Key has quotes - remove quotes from .env file")

# Check length (OpenAI keys are typically 51+ characters)
if len(raw_key) < 40:
    issues.append("⚠️  Key seems too short (OpenAI keys are typically 51+ chars)")
    print("   ⚠️  Key seems too short")

# Check for whitespace
if raw_key != raw_key.strip():
    issues.append("⚠️  Key has leading/trailing whitespace")
    print("   ⚠️  Key has whitespace - trim it in .env file")

print("\n" + "=" * 60)
if issues:
    print("Issues found:")
    for issue in issues:
        print(f"  {issue}")
    print("\nTo fix:")
    print("1. Open your .env file")
    print("2. Make sure the line looks like:")
    print("   OPENAI_API_KEY=sk-proj-...your-full-key...")
    print("3. NO quotes, NO spaces around =")
    print("4. Get a valid key from: https://platform.openai.com/account/api-keys")
else:
    print("✅ Key format looks good!")
    print("\nIf you're still getting 401 errors:")
    print("1. Verify the key is active at: https://platform.openai.com/account/api-keys")
    print("2. Check if you have billing set up")
    print("3. Try regenerating the key")
print("=" * 60)

