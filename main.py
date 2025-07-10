from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Support Squad Backend",
    description="FastAPI backend for Chatwoot integration with Google ADK",
    version="1.0.0"
)

# Pydantic models for request/response validation
class ChatwootMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    sender_id: Optional[str] = None
    account_id: Optional[str] = None

class ADKResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None
    timestamp: str

# Mock Google ADK integration
class MockGoogleADK:
    def __init__(self):
        self.conversation_history = {}
    
    def process_message(self, message: str, conversation_id: str = None) -> str:
        """
        Mock implementation of Google ADK processing.
        In production, this would integrate with actual Google ADK APIs.
        """
        logger.info(f"Processing message: {message}")
        
        # Simple mock responses based on message content
        if "hello" in message.lower():
            response = "Hello! I'm your AI assistant. How can I help you today?"
        elif "help" in message.lower():
            response = "I'm here to help! You can ask me questions about our services, get support, or just chat with me."
        elif "support" in message.lower():
            response = "For technical support, please provide more details about your issue. I'll do my best to assist you."
        elif "bye" in message.lower() or "goodbye" in message.lower():
            response = "Goodbye! Feel free to reach out if you need help again."
        else:
            response = "I understand you said: " + message + ". How can I assist you further?"
        
        # Store conversation history (in production, this would be in a database)
        if conversation_id:
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
            self.conversation_history[conversation_id].append({
                "user_message": message,
                "ai_response": response,
                "timestamp": datetime.now().isoformat()
            })
        
        return response

# Initialize mock ADK
mock_adk = MockGoogleADK()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Support Squad Backend is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "support-squad-backend"
    }

@app.post("/chatwoot/webhook")
async def chatwoot_webhook(request: Request):
    """
    Webhook endpoint to receive messages from Chatwoot.
    This endpoint handles the integration between Chatwoot and Google ADK.
    """
    try:
        # Get the raw body
        body = await request.body()
        logger.info(f"Received webhook from Chatwoot: {body}")
        
        # Parse the JSON payload
        try:
            payload = await request.json()
        except:
            # If JSON parsing fails, try to parse as form data
            form_data = await request.form()
            payload = dict(form_data)
        
        logger.info(f"Parsed payload: {payload}")
        
        # Extract message from Chatwoot payload
        # Chatwoot webhook format may vary, so we handle different possible structures
        message = None
        conversation_id = None
        sender_id = None
        account_id = None
        
        # Try different possible payload structures
        if isinstance(payload, dict):
            # Direct message field
            if "message" in payload:
                message = payload["message"]
            
            # Nested message structure
            elif "content" in payload:
                message = payload["content"]
            
            # Chatwoot specific structure
            elif "conversation" in payload and "messages" in payload["conversation"]:
                messages = payload["conversation"]["messages"]
                if messages and len(messages) > 0:
                    message = messages[-1].get("content", "")
                    conversation_id = payload["conversation"].get("id")
                    sender_id = messages[-1].get("sender_id")
                    account_id = payload["conversation"].get("account_id")
            
            # Extract other fields
            conversation_id = conversation_id or payload.get("conversation_id")
            sender_id = sender_id or payload.get("sender_id")
            account_id = account_id or payload.get("account_id")
        
        if not message:
            raise HTTPException(status_code=400, detail="No message found in payload")
        
        logger.info(f"Processing message: {message} for conversation: {conversation_id}")
        
        # Process message through Google ADK (mock implementation)
        adk_response = mock_adk.process_message(message, conversation_id)
        
        # Prepare response for Chatwoot
        response_data = {
            "response": adk_response,
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        logger.info(f"Sending response: {response_data}")
        
        return JSONResponse(content=response_data, status_code=200)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/chat/message")
async def process_chat_message(chat_message: ChatwootMessage):
    """
    Direct message processing endpoint for testing.
    This endpoint can be used for direct API calls without webhook complexity.
    """
    try:
        logger.info(f"Processing direct message: {chat_message.message}")
        
        # Process message through Google ADK
        adk_response = mock_adk.process_message(
            chat_message.message, 
            chat_message.conversation_id
        )
        
        response = ADKResponse(
            response=adk_response,
            conversation_id=chat_message.conversation_id,
            timestamp=datetime.now().isoformat()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/conversations/{conversation_id}/history")
async def get_conversation_history(conversation_id: str):
    """
    Get conversation history for a specific conversation ID.
    Useful for debugging and testing.
    """
    if conversation_id in mock_adk.conversation_history:
        return {
            "conversation_id": conversation_id,
            "history": mock_adk.conversation_history[conversation_id]
        }
    else:
        return {
            "conversation_id": conversation_id,
            "history": [],
            "message": "No conversation history found"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 