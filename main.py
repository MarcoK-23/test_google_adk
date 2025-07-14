from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Health check endpoint (root)
@app.get("/")
async def root():
    # Simple root endpoint to verify the service is running
    return {"message": "De request is gelukt gefeliciteerd", "status": "healthy"}

# Health check endpoint for monitoring
@app.get("/health")
async def health_check():
    # Returns detailed health status and timestamp
    return {
        "message": "De request is gelukt gefeliciteerd",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "support-squad-backend"
    }

# Simple health check endpoint for container health checks
@app.get("/healthz")
async def health_check_simple():
    # Used by Docker/Cloud Run for quick health checks
    return {"message": "De request is gelukt gefeliciteerd", "status": "ok"}

# Main webhook endpoint for Chatwoot AI reply suggestions
@app.post("/chatwoot/webhook")
async def chatwoot_webhook(request: Request):
    try:
        # Log the raw request body for debugging
        body = await request.body()
        logger.info(f"Received webhook from Chatwoot: {body}")
        # Parse the incoming JSON or form payload
        try:
            payload = await request.json()
        except:
            form_data = await request.form()
            payload = dict(form_data)
        logger.info(f"Parsed payload: {payload}")
        # Extract the user message from various possible payload formats
        message = None
        conversation_id = None
        if isinstance(payload, dict):
            # Handle OpenAI/Chatwoot GPT-style payload
            if "messages" in payload and isinstance(payload["messages"], list):
                messages = payload["messages"]
                for msg in reversed(messages):
                    if msg.get("role") == "user":
                        message = msg.get("content", "")
                        break
                # Generate a fallback conversation ID if not present
                conversation_id = conversation_id or f"gpt-conv-{int(datetime.now().timestamp())}"
            # Handle simple message field
            elif "message" in payload:
                message = payload["message"]
            # Handle nested content field
            elif "content" in payload:
                message = payload["content"]
            # Handle Chatwoot's own conversation structure
            elif "conversation" in payload and "messages" in payload["conversation"]:
                messages = payload["conversation"]["messages"]
                if messages and len(messages) > 0:
                    message = messages[-1].get("content", "")
                    conversation_id = payload["conversation"].get("id")
            # Fallback: try to get conversation_id from top-level
            conversation_id = conversation_id or payload.get("conversation_id")
        # If no message is found, return a 400 error
        if not message:
            logger.error(f"No message found in payload. Payload structure: {payload}")
            raise HTTPException(status_code=400, detail="No message found in payload")
        logger.info(f"Extracted message: '{message}' from conversation: {conversation_id}")
        # Always return the static AI reply in the format Chatwoot expects
        response_data = {
            "choices": [
                {
                    "message": {
                        "content": "Hallo de request is gelukt gefeliciteerd"
                    }
                }
            ]
        }
        logger.info(f"Sending response: {response_data}")
        return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        # Log any errors and return a 500 error to Chatwoot
        logger.error(f"Error processing webhook: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# For local development/testing: run with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 