const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
// Use port 8080 for Google Cloud Run, fallback to 3000 for local development
const PORT = process.env.PORT || 8080;

// Middleware
app.use(cors());
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ extended: true, limit: '50mb' }));

// Enhanced logging middleware for cloud environments
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.path}`);
  console.log(`[${timestamp}] Request Headers:`, JSON.stringify(req.headers, null, 2));
  console.log(`[${timestamp}] Request Body:`, JSON.stringify(req.body, null, 2));
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  const healthInfo = {
    status: 'ok',
    message: 'SupportSquadAI Server is running',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
    port: PORT,
    version: '1.0.0'
  };
  console.log(`[${new Date().toISOString()}] Health check requested`);
  res.json(healthInfo);
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'SupportSquadAI Server',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      chat: '/v1/chat/completions',
      assist: '/ai/assist'
    }
  });
});

// Main AI Assist endpoint
app.post('/v1/chat/completions', (req, res) => {
  const requestId = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  try {
    // Log the full incoming payload
    console.log(`[${new Date().toISOString()}] [${requestId}] === SUPPORT SQUAD AI REQUEST RECEIVED ===`);
    console.log(`[${new Date().toISOString()}] [${requestId}] Full Payload:`, JSON.stringify(req.body, null, 2));
    console.log(`[${new Date().toISOString()}] [${requestId}] === END REQUEST ===`);

    // Extract information from the request
    const { messages, model } = req.body;
    
    // Log the conversation content
    if (messages && messages.length > 0) {
      console.log(`[${new Date().toISOString()}] [${requestId}] Conversation Messages:`);
      messages.forEach((msg, index) => {
        console.log(`[${new Date().toISOString()}] [${requestId}] Message ${index + 1} (${msg.role}): ${msg.content}`);
      });
    }

    // Always return the success message
    const response = {
      id: `chatcmpl-${Date.now()}`,
      object: 'chat.completion',
      created: Math.floor(Date.now() / 1000),
      model: model || 'gpt-4o-mini',
      choices: [
        {
          index: 0,
          message: {
            role: 'assistant',
            content: 'Hallo de request is gelukt gefeliciteerd'
          },
          finish_reason: 'stop'
        }
      ],
      usage: {
        prompt_tokens: 0,
        completion_tokens: 0,
        total_tokens: 0
      }
    };

    console.log(`[${new Date().toISOString()}] [${requestId}] === SENDING RESPONSE ===`);
    console.log(`[${new Date().toISOString()}] [${requestId}] Response:`, JSON.stringify(response, null, 2));
    console.log(`[${new Date().toISOString()}] [${requestId}] === END RESPONSE ===`);

    res.json(response);
  } catch (error) {
    console.error(`[${new Date().toISOString()}] [${requestId}] Error processing request:`, error);
    res.status(500).json({
      error: {
        message: 'Internal server error',
        type: 'server_error',
        code: 500,
        request_id: requestId
      }
    });
  }
});

// Alternative endpoint for different request formats
app.post('/ai/assist', (req, res) => {
  const requestId = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  try {
    console.log(`[${new Date().toISOString()}] [${requestId}] === AI ASSIST REQUEST RECEIVED ===`);
    console.log(`[${new Date().toISOString()}] [${requestId}] Full Payload:`, JSON.stringify(req.body, null, 2));
    console.log(`[${new Date().toISOString()}] [${requestId}] === END REQUEST ===`);

    const response = {
      success: true,
      message: 'Hallo de request is gelukt gefeliciteerd',
      timestamp: new Date().toISOString(),
      request_id: requestId
    };

    console.log(`[${new Date().toISOString()}] [${requestId}] === SENDING RESPONSE ===`);
    console.log(`[${new Date().toISOString()}] [${requestId}] Response:`, JSON.stringify(response, null, 2));
    console.log(`[${new Date().toISOString()}] [${requestId}] === END RESPONSE ===`);

    res.json(response);
  } catch (error) {
    console.error(`[${new Date().toISOString()}] [${requestId}] Error processing AI assist request:`, error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      request_id: requestId
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(`[${new Date().toISOString()}] Unhandled error:`, err);
  res.status(500).json({
    error: {
      message: 'Internal server error',
      type: 'unhandled_error',
      code: 500
    }
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: {
      message: 'Endpoint not found',
      type: 'not_found',
      code: 404,
      available_endpoints: ['/health', '/v1/chat/completions', '/ai/assist']
    }
  });
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`[${new Date().toISOString()}] SupportSquadAI Server running on port ${PORT}`);
  console.log(`[${new Date().toISOString()}] Health check: http://localhost:${PORT}/health`);
  console.log(`[${new Date().toISOString()}] Main endpoint: http://localhost:${PORT}/v1/chat/completions`);
  console.log(`[${new Date().toISOString()}] Alternative endpoint: http://localhost:${PORT}/ai/assist`);
  console.log(`[${new Date().toISOString()}] Environment: ${process.env.NODE_ENV || 'development'}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log(`[${new Date().toISOString()}] SIGTERM received, shutting down gracefully`);
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log(`[${new Date().toISOString()}] SIGINT received, shutting down gracefully`);
  process.exit(0);
});

module.exports = app; 