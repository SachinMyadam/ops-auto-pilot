
import os

config = {
    "name": "GitHubWebhook",
    "type": "api",
    "path": "/webhook",
    "method": "POST",
    "description": "Receives GitHub webhook events",
    "emits": ["analyze-error"],
    "flows": ["ops-flow"]
}

async def handler(req, context):
    # Get data safely (handle both object and dict access if needed)
    data = req.body if hasattr(req, "body") else {}
    
    # Log the event
    context.logger.info("🚨 Webhook Received!")
    
    # Emit an event to trigger the next step (The AI)
    await context.emit({
        "topic": "analyze-error",
        "data": {
            "job_name": "build-deploy",
            "error_log": "FATAL ERROR: Out of Memory (Exit Code 137)"
        }
    })

    return {
        "status": 200,
        "body": {"message": "Alert received. AI Agents dispatched."}
    }
