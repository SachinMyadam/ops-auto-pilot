import google.generativeai as genai
import os

# Configure the API key
genai.configure(api_key="AIzaSyCXstP5dsEZ_Srb2h5CmBut4g4FJ1qeSYY")

print("🔍 Checking available models for your API Key...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ AVAILABLE: {m.name}")
except Exception as e:
    print(f"❌ ERROR: {e}")
