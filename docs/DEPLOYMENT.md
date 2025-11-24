# Deployment Guide

This guide covers deployment options for the Arizona Adventure Agent, including both the LangGraph backend API and the React frontend.

## Architecture Overview

The application consists of two main components:

1. **Backend API**: LangGraph-based agent system exposed via LangGraph CLI
2. **Frontend**: React/TypeScript application built with Vite

## Backend Deployment Options

### 1. LangSmith Cloud (Recommended for Production)

**Best for**: Production deployments, managed infrastructure, automatic scaling

LangSmith provides managed hosting for LangGraph applications with built-in observability, monitoring, and scaling.

#### Prerequisites
- LangSmith account with API key
- All environment variables configured

#### Deployment Steps

1. **Install LangGraph CLI**:
   ```bash
   uv pip install -U "langgraph-cli[cloud]"
   ```

2. **Login to LangSmith**:
   ```bash
   langgraph login
   ```

3. **Deploy to LangSmith**:
   ```bash
   langgraph deploy
   ```

4. **Configure environment variables** in LangSmith dashboard:
   - Navigate to your project settings
   - Add all required API keys (OpenAI, Anthropic, etc.)

#### Benefits
- ✅ Managed infrastructure
- ✅ Automatic scaling
- ✅ Built-in monitoring and observability
- ✅ No server management
- ✅ Global CDN
- ✅ Automatic SSL certificates

#### Pricing
- Free tier available for development
- Pay-as-you-go for production usage

---

### 2. Self-Hosted with Docker

**Best for**: Full control, custom infrastructure, cost optimization

#### Prerequisites
- Docker and Docker Compose installed
- PostgreSQL database (for persistent checkpointing)
- Server with sufficient resources (2+ GB RAM recommended)

#### Deployment Steps

1. **Build Docker image**:
   ```bash
   langgraph build
   ```

2. **Create `docker-compose.yml`**:
   ```yaml
   version: '3.8'
   
   services:
     api:
       image: langgraph-adventure-agent:latest
       ports:
         - "2024:2024"
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
         - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
         - LANGCHAIN_PROJECT=${LANGCHAIN_PROJECT}
         - CHECKPOINTER_TYPE=postgres
         - CHECKPOINTER_DB_URL=postgresql://postgres:password@postgres:5432/langgraph
         # Add other environment variables as needed
       depends_on:
         - postgres
       restart: unless-stopped
   
     postgres:
       image: postgres:15-alpine
       environment:
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=password
         - POSTGRES_DB=langgraph
       volumes:
         - postgres_data:/var/lib/postgresql/data
       restart: unless-stopped
   
   volumes:
     postgres_data:
   ```

3. **Create `.env` file** with all required variables

4. **Start services**:
   ```bash
   docker-compose up -d
   ```

#### Benefits
- ✅ Full control over infrastructure
- ✅ Cost-effective for high traffic
- ✅ Customizable configuration
- ✅ Can deploy to any cloud provider

#### Hosting Options
- **AWS**: EC2, ECS, EKS, or App Runner
- **Google Cloud**: Cloud Run, GKE, or Compute Engine
- **Azure**: Container Instances, AKS, or App Service
- **DigitalOcean**: App Platform or Droplets
- **Linode**: Kubernetes or Compute Instances
- **Railway**: Simple container deployment
- **Render**: Container service
- **Fly.io**: Global edge deployment

---

### 3. Cloud Platform Deployments

#### Railway

**Best for**: Quick deployment, automatic HTTPS, PostgreSQL included

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Initialize project**:
   ```bash
   railway init
   ```

3. **Add PostgreSQL service** (for checkpointing)

4. **Set environment variables** in Railway dashboard

5. **Deploy**:
   ```bash
   railway up
   ```

#### Render

**Best for**: Simple deployments, free tier available

1. **Connect GitHub repository** to Render

2. **Create new Web Service**:
   - Build command: `langgraph build`
   - Start command: `langgraph up`
   - Add PostgreSQL database

3. **Set environment variables**

4. **Deploy**

#### Fly.io

**Best for**: Global edge deployment, low latency

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create `fly.toml`**:
   ```toml
   app = "adventure-agent"
   primary_region = "phx"
   
   [build]
     dockerfile = "Dockerfile"
   
   [env]
     PORT = "2024"
   
   [[services]]
     internal_port = 2024
     protocol = "tcp"
   
     [[services.ports]]
       handlers = ["http"]
       port = 80
   
     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   ```

3. **Deploy**:
   ```bash
   fly launch
   fly secrets set OPENAI_API_KEY=...
   fly secrets set ANTHROPIC_API_KEY=...
   # ... other secrets
   ```

#### Google Cloud Run

**Best for**: Serverless, auto-scaling, pay-per-use

1. **Build and push image**:
   ```bash
   langgraph build
   gcloud builds submit --tag gcr.io/PROJECT_ID/adventure-agent
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy adventure-agent \
     --image gcr.io/PROJECT_ID/adventure-agent \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=...,ANTHROPIC_API_KEY=...
   ```

#### AWS App Runner

**Best for**: Simple container deployment on AWS

1. **Push image to ECR**:
   ```bash
   aws ecr create-repository --repository-name adventure-agent
   # Build and push image
   ```

2. **Create App Runner service** via AWS Console or CLI

3. **Configure environment variables**

---

### 4. Kubernetes Deployment

**Best for**: Enterprise deployments, high availability, auto-scaling

#### Prerequisites
- Kubernetes cluster (EKS, GKE, AKS, or self-hosted)
- kubectl configured

#### Deployment Steps

1. **Create `k8s/deployment.yaml`**:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: adventure-agent
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: adventure-agent
     template:
       metadata:
         labels:
           app: adventure-agent
       spec:
         containers:
         - name: api
           image: langgraph-adventure-agent:latest
           ports:
           - containerPort: 2024
           env:
           - name: OPENAI_API_KEY
             valueFrom:
               secretKeyRef:
                 name: adventure-agent-secrets
                 key: openai-api-key
           # Add other environment variables
           resources:
             requests:
               memory: "512Mi"
               cpu: "250m"
             limits:
               memory: "2Gi"
               cpu: "1000m"
   ```

2. **Create `k8s/service.yaml`**:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: adventure-agent
   spec:
     selector:
       app: adventure-agent
     ports:
     - port: 80
       targetPort: 2024
     type: LoadBalancer
   ```

3. **Create secrets**:
   ```bash
   kubectl create secret generic adventure-agent-secrets \
     --from-literal=openai-api-key=... \
     --from-literal=anthropic-api-key=...
   ```

4. **Deploy**:
   ```bash
   kubectl apply -f k8s/
   ```

---

## Frontend Deployment Options

### 1. Vercel (Recommended)

**Best for**: React apps, automatic deployments, global CDN

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Configure `vercel.json`**:
   ```json
   {
     "buildCommand": "cd frontend && npm install && npm run build",
     "outputDirectory": "frontend/dist",
     "devCommand": "cd frontend && npm run dev",
     "rewrites": [
       {
         "source": "/api/:path*",
         "destination": "https://your-api-url.com/:path*"
       }
     ],
     "env": {
       "VITE_API_URL": "https://your-api-url.com"
     }
   }
   ```

3. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

#### Benefits
- ✅ Automatic deployments from Git
- ✅ Preview deployments for PRs
- ✅ Global CDN
- ✅ Free tier available
- ✅ Automatic SSL

---

### 2. Netlify

**Best for**: JAMstack apps, form handling, serverless functions

1. **Install Netlify CLI**:
   ```bash
   npm i -g netlify-cli
   ```

2. **Create `netlify.toml`**:
   ```toml
   [build]
     command = "cd frontend && npm install && npm run build"
     publish = "frontend/dist"
   
   [[redirects]]
     from = "/api/*"
     to = "https://your-api-url.com/:splat"
     status = 200
   
   [build.environment]
     VITE_API_URL = "https://your-api-url.com"
   ```

3. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

---

### 3. Cloudflare Pages

**Best for**: Fast global CDN, edge computing, free tier

1. **Connect repository** to Cloudflare Pages

2. **Configure build settings**:
   - Build command: `cd frontend && npm install && npm run build`
   - Build output directory: `frontend/dist`

3. **Set environment variables**:
   - `VITE_API_URL`: Your backend API URL

4. **Deploy** (automatic on Git push)

---

### 4. AWS S3 + CloudFront

**Best for**: Enterprise, custom domain, full control

1. **Build frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Upload to S3**:
   ```bash
   aws s3 sync frontend/dist s3://your-bucket-name --delete
   ```

3. **Configure CloudFront** distribution pointing to S3 bucket

4. **Set up custom domain** and SSL certificate

---

### 5. GitHub Pages

**Best for**: Free hosting, simple static sites

1. **Update `vite.config.ts`**:
   ```typescript
   export default defineConfig({
     base: '/adventure-agent/', // if using project pages
     // ... other config
   })
   ```

2. **Add GitHub Actions workflow** (`.github/workflows/deploy.yml`):
   ```yaml
   name: Deploy to GitHub Pages
   
   on:
     push:
       branches: [ main ]
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-node@v3
           with:
             node-version: '18'
         - run: cd frontend && npm install && npm run build
         - uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./frontend/dist
   ```

---

## Full-Stack Deployment Options

### Option 1: Separate Deployments (Recommended)

- **Backend**: LangSmith Cloud or self-hosted Docker
- **Frontend**: Vercel, Netlify, or Cloudflare Pages
- **Database**: Managed PostgreSQL (AWS RDS, Google Cloud SQL, etc.)

**Benefits**:
- ✅ Independent scaling
- ✅ Best-in-class hosting for each component
- ✅ Easier to maintain
- ✅ Better performance (CDN for frontend)

### Option 2: Monolithic Deployment

Deploy both frontend and backend together:

1. **Serve frontend from backend**:
   - Build frontend: `cd frontend && npm run build`
   - Serve static files from FastAPI/LangGraph server
   - Add custom route in `webapp.py`:

   ```python
   from fastapi.staticfiles import StaticFiles
   from fastapi.responses import FileResponse
   
   app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")
   
   @app.get("/{full_path:path}")
   async def serve_frontend(full_path: str):
       if full_path.startswith("api") or full_path.startswith("threads"):
           return {"error": "Not found"}
       return FileResponse("frontend/dist/index.html")
   ```

2. **Deploy as single Docker container**

---

## Environment Variables

### Backend Required Variables

```bash
# LLM Providers (at least one required)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# LangSmith (optional but recommended)
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_PROJECT=adventure-agent
LANGCHAIN_TRACING_V2=true

# Optional APIs
TAVILY_API_KEY=your_key_here
OPENCAGE_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
GOOGLE_PLACES_API_KEY=your_key_here
RECREATION_GOV_API_KEY=your_key_here

# Checkpointing (for production)
CHECKPOINTER_TYPE=postgres
CHECKPOINTER_DB_URL=postgresql://user:pass@host:5432/dbname
```

### Frontend Required Variables

```bash
VITE_API_URL=https://your-backend-api-url.com
```

---

## Production Checklist

### Backend
- [ ] All API keys configured
- [ ] PostgreSQL database set up for checkpointing
- [ ] LangSmith tracing enabled
- [ ] Rate limiting configured
- [ ] Error monitoring set up (Sentry, etc.)
- [ ] Health check endpoint configured
- [ ] SSL/TLS certificates configured
- [ ] CORS configured for frontend domain
- [ ] Environment variables secured (secrets management)

### Frontend
- [ ] API URL configured
- [ ] Build optimized (`npm run build`)
- [ ] Environment variables set in hosting platform
- [ ] Custom domain configured
- [ ] SSL certificate active
- [ ] Analytics configured (optional)
- [ ] Error tracking configured (Sentry, etc.)

### Infrastructure
- [ ] Database backups configured
- [ ] Monitoring and alerting set up
- [ ] Log aggregation configured
- [ ] Auto-scaling configured (if needed)
- [ ] CDN configured for static assets
- [ ] DNS records configured

---

## Monitoring and Observability

### LangSmith Integration

The backend automatically integrates with LangSmith for:
- Request tracing
- Performance monitoring
- Error tracking
- Cost analysis

Ensure `LANGCHAIN_API_KEY` and `LANGCHAIN_TRACING_V2=true` are set.

### Additional Monitoring

Consider adding:
- **Sentry**: Error tracking for both frontend and backend
- **Datadog/New Relic**: Application performance monitoring
- **Uptime monitoring**: Pingdom, UptimeRobot, etc.
- **Log aggregation**: CloudWatch, Datadog Logs, etc.

---

## Cost Estimation

### Backend (LangSmith Cloud)
- Free tier: Development/testing
- Production: Pay-per-use based on API calls and compute

### Self-Hosted Backend
- Server: $5-50/month (depending on provider and size)
- Database: $0-25/month (managed PostgreSQL)
- Bandwidth: Usually included

### Frontend
- Vercel/Netlify: Free tier available, $20/month for pro
- Cloudflare Pages: Free tier
- AWS S3 + CloudFront: ~$1-10/month for low traffic

### LLM API Costs
- OpenAI GPT-4o-mini: ~$0.15-0.60 per 1M tokens
- Anthropic Claude Haiku: ~$0.25 per 1M tokens
- Anthropic Claude Sonnet: ~$3 per 1M tokens

**Estimated monthly cost for moderate usage**:
- Infrastructure: $20-100/month
- LLM API calls: $50-500/month (highly variable)

---

## Security Considerations

1. **API Keys**: Never commit API keys to Git
2. **CORS**: Configure CORS to only allow your frontend domain
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Authentication**: Add API authentication for production
5. **HTTPS**: Always use HTTPS in production
6. **Secrets Management**: Use platform secrets management (not environment files)
7. **Database**: Use connection pooling and secure connections
8. **Input Validation**: Validate all user inputs

---

## Troubleshooting

### Backend Issues

**Server won't start**:
- Check environment variables are set
- Verify PostgreSQL connection (if using)
- Check LangGraph CLI version: `langgraph --version`

**High latency**:
- Enable caching: `ENABLE_CACHING=true`
- Check LLM API response times
- Consider using faster models for simple tasks

**Memory issues**:
- Reduce `MAX_CONCURRENCY` in config
- Use streaming for long responses
- Monitor container memory limits

### Frontend Issues

**API connection errors**:
- Verify `VITE_API_URL` is correct
- Check CORS configuration on backend
- Verify backend is running and accessible

**Build failures**:
- Clear `node_modules` and reinstall
- Check Node.js version (18+ required)
- Verify all environment variables are set

---

## Additional Resources

- [LangGraph CLI Documentation](https://docs.langchain.com/langsmith/cli)
- [LangSmith Deployment Guide](https://docs.langchain.com/langsmith/deploy)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

---

## Quick Start: Deploy to LangSmith + Vercel

The fastest path to production:

1. **Backend**:
   ```bash
   langgraph login
   langgraph deploy
   # Configure environment variables in LangSmith dashboard
   ```

2. **Frontend**:
   ```bash
   cd frontend
   vercel
   # Set VITE_API_URL to your LangSmith API URL
   ```

That's it! Your application is now live.

