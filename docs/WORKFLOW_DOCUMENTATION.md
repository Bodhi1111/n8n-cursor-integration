# 📋 Workflow Documentation

## Overview

This document provides comprehensive documentation of all workflows and CI/CD processes in the n8n-cursor-integration project.

## 🏗️ Infrastructure Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Actions CI/CD Pipeline              │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│    Lint     │    Test     │ Integration │      Deploy         │
│             │             │    Test     │                     │
│ - ESLint    │ - Unit      │ - Docker    │ - Staging           │
│ - Prettier  │ - Function  │ - Services  │ - Production        │
│ - Markdown  │ - Sales     │ - Vector    │ - Rollback          │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Docker Infrastructure                         │
├─────────────────────┬───────────────────────┬───────────────────┤
│        n8n          │       Baserow         │      Volumes      │
│                     │                       │                   │
│ - Port: 5679        │ - Port: 8080          │ - n8n_data        │
│ - Workflows         │ - CRM Database        │ - baserow_data    │
│ - Automation        │ - Client Management   │ - Persistent      │
└─────────────────────┴───────────────────────┴───────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 n8n Workflow Ecosystem                         │
├─────────────────────┬───────────────────────┬───────────────────┤
│    Estate Planning  │    Batch Processing   │  Sales Tracking   │
│                     │                       │                   │
│ - Client Analysis   │ - Bulk Transcripts    │ - Lead Capture    │
│ - Document Proc     │ - Automated Reports   │ - Pipeline Mgmt   │
│ - CRM Integration   │ - Error Handling      │ - Follow-up       │
└─────────────────────┴───────────────────────┴───────────────────┘
```

## 🔄 CI/CD Pipeline Workflows

### 1. Continuous Integration (`.github/workflows/ci.yml`)

**Trigger:** Push to main/develop, Pull Requests

**Jobs:**
- **lint**: Code quality checks (ESLint, Prettier, Markdown)
- **test**: Unit tests for n8n functions
- **integration-test**: Service integration with Ollama/Qdrant
- **docker-test**: Full Docker stack validation
- **security**: Security scanning and vulnerability checks

**Success Criteria:**
- All linting passes
- Unit tests achieve >90% success rate
- Docker services start and respond
- No critical security vulnerabilities

### 2. Deployment Pipeline (`.github/workflows/deploy.yml`)

**Trigger:** Push to main, Git tags, Manual dispatch

**Jobs:**
- **test**: Pre-deployment validation
- **security**: Security checks
- **deploy-staging**: Staging environment deployment
- **deploy-production**: Production deployment (tags only)
- **rollback**: Automatic rollback on failure

**Environments:**
- **Staging**: Automatic on main branch
- **Production**: Manual approval required, tags only

## 📊 n8n Workflow Definitions

### 1. Estate Planning Processor Enhanced

**File:** `workflows/estate-planning-processor-enhanced.json`

**Purpose:** Comprehensive estate planning transcript processing

**Flow:**
```
Manual Trigger → Get Files → Split List → Process Each → 
Read Content → BMAD Analysis → Extract Data → Save to CRM → 
Generate Reports → Send Notifications
```

**Key Features:**
- Processes `.txt` files from transcript directory
- Extracts client names from filenames
- Uses BMAD AI for content analysis
- Integrates with Baserow CRM
- Generates automated follow-up emails

**Trigger:** Manual batch processing
**Input:** Directory of transcript files
**Output:** CRM records, reports, email queue

### 2. Batch Transcript Processor

**File:** `workflows/batch-transcript-processor.json`

**Purpose:** Bulk processing of existing transcripts for sales dashboard

**Flow:**
```
Manual Trigger → Find Files → Split Batches → Read Content → 
Process Data → Format Output → Update Dashboard → Archive Files
```

**Key Features:**
- Supports multiple file formats (`.txt`, `.md`, `.docx`)
- Configurable batch sizes
- Error handling with continue-on-fail
- Automatic file archiving
- Progress tracking and reporting

**Trigger:** Manual bulk processing
**Input:** File system directory
**Output:** Sales dashboard data, archived files

### 3. Sales Transcript Processor

**File:** `workflows/sales-transcript-processor.json`

**Purpose:** Real-time sales lead processing and tracking

**Flow:**
```
Webhook Trigger → Validate Input → Extract Lead Data → 
Score Lead → Update CRM → Create Follow-up → Send Notifications
```

**Key Features:**
- Webhook-triggered processing
- Lead scoring algorithms
- CRM integration
- Automated follow-up creation
- Real-time notifications

**Trigger:** Webhook from sales system
**Input:** Lead data payload
**Output:** CRM updates, follow-up tasks

## 🐳 Docker Services

### n8n Service

**Configuration:**
```yaml
image: n8nio/n8n:latest
ports: ["5679:5678"]
environment:
  - N8N_HOST=localhost
  - N8N_PROTOCOL=http
  - N8N_BASIC_AUTH_ACTIVE=true
volumes:
  - workflows:/home/node/.n8n/workflows
  - credentials:/home/node/.n8n/credentials
```

**Health Check:** HTTP GET `http://localhost:5679/`

### Baserow Service

**Configuration:**
```yaml
image: baserow/baserow:latest
ports: ["8080:80"]
environment:
  - BASEROW_PUBLIC_URL=http://localhost:8080
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:80/signup"]
```

**Health Check:** HTTP GET `http://localhost:8080/signup`

## 🧪 Testing Strategy

### Unit Tests

**Location:** `scripts/test-runner.js`
**Coverage:** n8n Function node scripts
**Execution:** `npm test`

**Test Categories:**
- Data processing functions
- API payload builders
- Conditional routing logic
- File processing utilities

### Integration Tests

**Location:** `test-local-vector-pipeline.js`
**Dependencies:** Ollama, Qdrant services
**Execution:** `node test-local-vector-pipeline.js`

**Test Categories:**
- Ollama connection and model availability
- Vector embeddings generation
- Qdrant database operations
- End-to-end workflow validation

### Docker Integration Tests

**Execution:** CI pipeline `docker-test` job
**Validation:**
- Service startup and health
- Port accessibility
- Basic API responses
- Log analysis for errors

## 🔍 Monitoring and Observability

### Health Checks

**Services:**
- n8n: `curl -f http://localhost:5679/`
- Baserow: `curl -f http://localhost:8080/signup`
- Ollama: `curl -f http://localhost:11434/api/version`
- Qdrant: `curl -f http://localhost:6333/health`

### Logging

**Locations:**
- Docker logs: `docker-compose logs <service>`
- n8n execution logs: Web UI
- CI/CD logs: GitHub Actions

### Metrics

**Key Performance Indicators:**
- Workflow execution success rate
- Processing time per transcript
- Service uptime
- Error rates by component

## 🚨 Error Handling and Recovery

### Automatic Recovery

**Strategies:**
- Docker service restart policies
- n8n workflow retry mechanisms
- Graceful degradation for external services
- Rollback procedures for deployments

### Manual Intervention

**Procedures:**
1. Check service health endpoints
2. Review Docker and application logs
3. Restart failed services
4. Validate data integrity
5. Resume processing from checkpoint

## 🔐 Security Considerations

### Authentication

- n8n: Basic auth (admin/admin for development)
- Baserow: Built-in user management
- API endpoints: Token-based authentication

### Data Protection

- Sensitive data encrypted at rest
- Secure credential storage in n8n
- Network isolation via Docker networks
- Regular security scans in CI pipeline

### Compliance

- Regular dependency updates
- Vulnerability scanning
- Access logging and monitoring
- Data retention policies

## 📈 Performance Optimization

### Scaling Strategies

- Docker service scaling
- Batch processing optimization
- Database query optimization
- Caching strategies

### Resource Management

- Container resource limits
- Volume cleanup procedures
- Memory and CPU monitoring
- Disk space management

## 🔄 Maintenance Procedures

### Regular Tasks

- Dependency updates (weekly)
- Log rotation and cleanup
- Database maintenance
- Backup verification

### Incident Response

1. **Detection**: Monitoring alerts, health check failures
2. **Assessment**: Log analysis, service health evaluation
3. **Response**: Service restart, rollback, manual fixes
4. **Recovery**: Data validation, service restoration
5. **Post-mortem**: Root cause analysis, process improvement

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Baserow API Documentation](https://baserow.io/docs/apis)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Last Updated:** December 2024  
**Version:** 1.0  
**Maintainer:** Development Team