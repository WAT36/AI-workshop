import sys
print(f"Python version: {sys.version}")

try:
    import chromadb
    print(f"✓ chromadb: {chromadb.__version__}")
except ImportError as e:
    print(f"✗ chromadb: Not installed ({e})")

try:
    import openai
    print(f"✓ openai: {openai.__version__}")
except ImportError as e:
    print(f"✗ openai: Not installed ({e})")

try:
    import dotenv
    print(f"✓ python-dotenv: installed")
except ImportError as e:
    print(f"✗ python-dotenv: Not installed ({e})")

try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✓ OPENAI_API_KEY: Found (length: {len(api_key)})")
    else:
        print("✗ OPENAI_API_KEY: Not found in .env file")
except Exception as e:
    print(f"✗ Error loading .env: {e}")

print("\nSetup check complete!")