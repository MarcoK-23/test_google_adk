# Support Squad Backend

A FastAPI application that integrates Chatwoot with Google ADK (Agent Development Kit) for AI-powered customer support.

## Features

- **Chatwoot Webhook Integration**: Receives messages from Chatwoot and processes them through Google ADK
- **Google ADK Integration**: Processes messages using Google's Agent Development Kit (currently using mock responses for local testing)
- **Conversation Management**: Tracks conversation history and context
- **RESTful API**: Clean API endpoints for testing and integration
- **Health Monitoring**: Built-in health check endpoints

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the FastAPI server:
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. The application will be available at:
   - **API**: http://localhost:8000
   - **Interactive Documentation**: http://localhost:8000/docs
   - **Alternative Documentation**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint with basic status
- `GET /health` - Detailed health check

### Chatwoot Integration
- `POST /chatwoot/webhook` - Webhook endpoint for Chatwoot messages
- `POST /chat/message` - Direct message processing endpoint

### Conversation Management
- `GET /conversations/{conversation_id}/history` - Get conversation history

## Testing the Application

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Direct Message Processing
```bash
curl -X POST "http://localhost:8000/chat/message" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Hello, I need help with my order",
       "conversation_id": "test-conv-123"
     }'
```

### 3. Chatwoot Webhook Simulation
```bash
curl -X POST "http://localhost:8000/chatwoot/webhook" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "I have a technical issue",
       "conversation_id": "chatwoot-conv-456",
       "sender_id": "user-123",
       "account_id": "account-789"
     }'
```

### 4. Get Conversation History
```bash
curl http://localhost:8000/conversations/test-conv-123/history
```

## Chatwoot Integration

### Webhook Configuration

To integrate with Chatwoot, configure a webhook in your Chatwoot instance:

1. Go to your Chatwoot dashboard
2. Navigate to Settings > Integrations > Webhooks
3. Add a new webhook with the URL: `http://your-domain:8000/chatwoot/webhook`
4. Configure the webhook to trigger on message events

### Webhook Payload Format

The application expects webhook payloads in one of these formats:

**Simple format:**
```json
{
  "message": "User message content",
  "conversation_id": "conv-123",
  "sender_id": "user-456",
  "account_id": "account-789"
}
```

**Chatwoot format:**
```json
{
  "conversation": {
    "id": "conv-123",
    "account_id": "account-789",
    "messages": [
      {
        "content": "User message content",
        "sender_id": "user-456"
      }
    ]
  }
}
```

## Google ADK Integration

### Current Implementation

The application currently uses a mock implementation of Google ADK for local testing. The mock provides realistic responses based on message content.

### Production Setup

When ready for production with actual Google ADK:

1. **Set up Google Cloud Project**:
   - Create a Google Cloud project
   - Enable the necessary APIs (Vertex AI, etc.)
   - Set up authentication credentials

2. **Update Configuration**:
   - Replace mock implementations in `google_adk_client.py`
   - Add your Google Cloud project ID and credentials
   - Configure the appropriate ADK endpoints

3. **Environment Variables**:
   ```bash
   export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
   ```

### Mock Responses

The current mock implementation responds to these keywords:
- "hello", "hi" - Greeting responses
- "help" - General help information
- "support" - Technical support assistance
- "bye", "goodbye" - Farewell messages
- "weather" - Weather-related queries
- "order", "purchase" - Order-related assistance

## Project Structure

```
supportsquad-backend-v2/
├── main.py                 # FastAPI application with routes
├── google_adk_client.py    # Google ADK integration client
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Development

### Adding New Features

1. **New Endpoints**: Add routes to `main.py`
2. **ADK Integration**: Extend `GoogleADKClient` in `google_adk_client.py`
3. **Data Models**: Add Pydantic models for request/response validation

### Testing

The application includes built-in logging for debugging:
- All API requests are logged
- ADK interactions are tracked
- Conversation history is maintained in memory

### Deployment

For production deployment:

1. **Environment Setup**:
   - Use a production WSGI server (Gunicorn)
   - Set up proper logging
   - Configure environment variables

2. **Google Cloud Deployment**:
   - Deploy to Google Cloud Run or App Engine
   - Set up proper authentication
   - Configure domain and SSL

3. **Monitoring**:
   - Set up health checks
   - Monitor API performance
   - Track conversation metrics

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Change port in main.py or use different port
   uvicorn main:app --port 8001
   ```

2. **Import Errors**:
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

3. **Webhook Not Receiving Data**:
   - Check Chatwoot webhook configuration
   - Verify the webhook URL is accessible
   - Check application logs for errors

### Logs

The application logs all activities. Check the console output for:
- Incoming webhook requests
- ADK processing results
- Error messages and stack traces

## Next Steps

1. **Real Google ADK Integration**: Replace mock implementations with actual API calls
2. **Database Integration**: Add persistent storage for conversations
3. **Authentication**: Implement proper authentication and authorization
4. **Advanced Features**: Add conversation analytics, sentiment analysis, etc.
5. **Deployment**: Deploy to Google Cloud with proper infrastructure

## Support

For issues and questions:
1. Check the application logs
2. Review the API documentation at `/docs`
3. Test individual endpoints
4. Verify Chatwoot webhook configuration 