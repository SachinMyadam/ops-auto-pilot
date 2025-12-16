
import os
import json
import google.generativeai as genai

config = {
    "name": "AIAnalyzer",
    "type": "event",
    "subscribes": ["analyze-error"], 
    "emits": [],
    "description": "Analyzes logs using Google Gemini 1.5 Flash",
    "flows": ["ops-flow"]
}

async def handler(event, context):
    # 1. Get the input data
    data = event.get("data", {})
    job = data.get("job_name", "unknown_job")
    error_log = data.get("error_log", "No error log provided.")
    
    # 2. Configure Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        context.logger.error("❌ Missing GEMINI_API_KEY environment variable")
        return {"error": "Missing API Key"}

    genai.configure(api_key=api_key)
    
    context.logger.info(f"🤖 GEMINI AGENT: Analyzing logs for {job}...")

    # 3. Define the prompt
    prompt = f"""
    You are a Senior DevOps Engineer. Analyze this error log:
    Job: {job}
    Log: {error_log}
    
    Return a JSON object with these keys:
    - root_cause (string)
    - action (string, e.g. scale_up, restart, rollback)
    - confidence (float between 0-1)
    """

    try:
        # Use the "flash" model which is fast and free
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Call the API with JSON enforcement
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        # 4. Parse the response
        decision = json.loads(response.text)
        
        context.logger.info(f"✅ GEMINI DECISION: {decision}")
        return decision

    except Exception as e:
        context.logger.error(f"❌ Gemini Failed: {str(e)}")
        return {"error": str(e)}
