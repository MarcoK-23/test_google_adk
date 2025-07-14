# SupportSquadAI Integration for Chatwoot

This implementation modifies Chatwoot's AI Assist feature to send the entire conversation content to your SupportSquadAI server when users click "Summarize" or "Reply Suggestion" buttons.

## Architecture Overview

- **Chatwoot**: Hosted on your VPS
- **SupportSquadAI Server**: Hosted on Google Cloud
- **Communication**: HTTP requests between VPS and Google Cloud

## What This Does

1. **Modifies Chatwoot's AI Assist**: When users click "Summarize" or "Reply Suggestion" in the AI Assist panel, the system will:
   - Send the entire conversation content with simple instructions
   - Log the full payload completely
   - Always return "Hallo de request is gelukt gefeliciteerd" as the response

2. **Provides a Separate Server**: A Node.js server that can receive these requests and send back the specified message.

## Files Modified/Created

### Modified Files
- `lib/integrations/support_squad_ai/processor_service.rb` - Modified the summarize and reply suggestion methods

### New Files
- `support_squad_ai_server/support_squad_ai_server.js` - Node.js server to receive requests
- `support_squad_ai_server/package.json` - Dependencies for the server
- `SUPPORT_SQUAD_AI_README.md` - This documentation

## Setup Instructions

### 1. Deploy the SupportSquadAI Server to Google Cloud

#### Option A: Google Cloud Run (Recommended)

```bash
# Navigate to the server directory
cd support_squad_ai_server

# Create a Dockerfile
cat > Dockerfile << 'EOF'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 8080
CMD ["node", "support_squad_ai_server.js"]
EOF

# Update the server to use port 8080 (Cloud Run requirement)
# Edit support_squad_ai_server.js and change:
# const PORT = process.env.PORT || 8080;

# Build and deploy to Cloud Run
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/support-squad-ai
gcloud run deploy support-squad-ai \
  --image gcr.io/YOUR_PROJECT_ID/support-squad-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

#### Option B: Google Compute Engine

```bash
# Create a VM instance
gcloud compute instances create support-squad-ai \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --tags=http-server,https-server

# SSH into the instance
gcloud compute ssh support-squad-ai --zone=us-central1-a

# On the VM, install Node.js and deploy
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Clone or upload your server files
cd ~
mkdir support-squad-ai-server
cd support-squad-ai-server
# Upload your files here

npm install
npm start
```

#### Option C: Google App Engine

```bash
# Create app.yaml
cat > app.yaml << 'EOF'
runtime: nodejs18
service: support-squad-ai

env_variables:
  PORT: 8080

automatic_scaling:
  target_cpu_utilization: 0.6
  min_instances: 1
  max_instances: 10
EOF

# Deploy
gcloud app deploy
```

### 2. Configure Chatwoot on Your VPS

In your Chatwoot instance, when setting up the SupportSquadAI integration:

1. Go to **Settings > Integrations > SupportSquadAI**
2. Enter your API key (can be any value since we're not using it)
3. Set the **API Endpoint** to your Google Cloud server URL:
   - Cloud Run: `https://support-squad-ai-xxxxx-uc.a.run.app/v1/chat/completions`
   - Compute Engine: `http://YOUR_VM_IP:3000/v1/chat/completions`
   - App Engine: `https://YOUR_PROJECT_ID.uc.r.appspot.com/v1/chat/completions`
4. Save the configuration

### 3. Test the Integration

1. Open a conversation in Chatwoot
2. Click the AI Assist button (three dots in the message composer)
3. Select either "Summarize" or "Reply Suggestion"
4. Check the Google Cloud logs for the logged payload
5. The response should be "Hallo de request is gelukt gefeliciteerd"

## Google Cloud Specific Setup

### Cloud Run (Recommended)

**Advantages:**
- Serverless, auto-scaling
- Pay only for requests
- Built-in HTTPS
- Easy deployment

**Setup:**
```bash
# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Deploy
gcloud run deploy support-squad-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Compute Engine

**Advantages:**
- Full control over the server
- Persistent storage
- Custom configurations

**Setup:**
```bash
# Create firewall rule for port 3000
gcloud compute firewall-rules create allow-support-squad-ai \
  --allow tcp:3000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags http-server

# Use systemd for auto-start
sudo systemctl enable support-squad-ai
sudo systemctl start support-squad-ai
```

### App Engine

**Advantages:**
- Managed platform
- Auto-scaling
- Built-in monitoring

**Setup:**
```bash
# Deploy
gcloud app deploy

# View logs
gcloud app logs tail -s support-squad-ai
```

## Server Endpoints

### Main Endpoint
- **URL**: `POST /v1/chat/completions`
- **Purpose**: Receives AI Assist requests from Chatwoot
- **Response**: Always returns "Hallo de request is gelukt gefeliciteerd"

### Alternative Endpoint
- **URL**: `POST /ai/assist`
- **Purpose**: Alternative endpoint for different request formats
- **Response**: Same success message

### Health Check
- **URL**: `GET /health`
- **Purpose**: Check if server is running
- **Response**: Server status

## Logging and Monitoring

### Cloud Run Logs
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=support-squad-ai" --limit 50
```

### Compute Engine Logs
```bash
gcloud compute instances get-serial-port-output support-squad-ai --zone=us-central1-a
```

### App Engine Logs
```bash
gcloud app logs tail -s support-squad-ai
```

## Security Considerations

### For Production Use

1. **Authentication**: Add API key validation
```javascript
// In support_squad_ai_server.js
const API_KEY = process.env.API_KEY || 'your-secret-key';

app.use('/v1/chat/completions', (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (authHeader !== `Bearer ${API_KEY}`) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
});
```

2. **HTTPS**: Use Cloud Run or App Engine (built-in) or set up SSL for Compute Engine

3. **Rate Limiting**: Add rate limiting middleware
```bash
npm install express-rate-limit
```

4. **Environment Variables**: Use Google Cloud Secret Manager for sensitive data

## Cost Optimization

### Cloud Run
- Set minimum instances to 0 for cost savings
- Use appropriate memory allocation (128MB is usually sufficient)

### Compute Engine
- Use e2-micro for development
- Use e2-small or e2-medium for production
- Enable auto-shutdown for non-production instances

### App Engine
- Use automatic scaling with appropriate limits
- Monitor usage in Google Cloud Console

## Troubleshooting

### Connection Issues
- Check firewall rules
- Verify the API endpoint URL in Chatwoot
- Test with curl: `curl -X POST https://your-server-url/v1/chat/completions`

### Logs Not Appearing
- Check Google Cloud Logging
- Verify the service is running
- Check Chatwoot logs for errors

### Performance Issues
- Monitor CPU and memory usage
- Check network latency between VPS and Google Cloud
- Consider using a region closer to your VPS

## Production Checklist

- [ ] Deploy to Google Cloud
- [ ] Configure HTTPS
- [ ] Set up authentication
- [ ] Add rate limiting
- [ ] Configure monitoring and alerts
- [ ] Set up log retention
- [ ] Test failover scenarios
- [ ] Document deployment procedures 