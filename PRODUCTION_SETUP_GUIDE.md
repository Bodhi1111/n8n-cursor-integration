# 🚀 Production BMAD Estate Planning Workflow Setup Guide

## Overview

This guide provides step-by-step instructions for setting up the production-ready BMAD Estate Planning Processor workflow in n8n. This workflow processes 352 estate planning transcripts using the BMAD methodology with advanced features including:

- ✅ **Webhook automation** for triggered processing
- ✅ **5 specialized BMAD agents** for enhanced analysis
- ✅ **Parallel batch processing** for optimal performance
- ✅ **Comprehensive error handling** with retry logic
- ✅ **Quality-based routing** and human review queues
- ✅ **Personalized email generation** based on meeting stages
- ✅ **Advanced knowledge extraction** and competitive intelligence
- ✅ **Real-time monitoring** and performance reporting

## Prerequisites

Before setting up the workflow, ensure you have:

1. **n8n Instance** (v1.0+ recommended)
2. **OpenAI API Key** for GPT-4 access
3. **Baserow Instance** with CRM database configured
4. **Access to transcript files** (352 estate planning transcripts)
5. **BMAD agents** deployed (optional but recommended for enhanced features)

## 1. n8n Workflow Import

### Step 1: Import the Workflow

1. Open your n8n instance
2. Click **"Import"** in the workflows section
3. Upload the file: `/Users/joshuavaughan/n8n-cursor-integration/production-bmad-estate-workflow.json`
4. The workflow will be imported as "Production BMAD Estate Planning Processor"

### Step 2: Configure Credentials

The workflow requires these credentials to be set up in n8n:

#### OpenAI Credentials
1. Go to **Settings > Credentials**
2. Create new **OpenAI** credential
3. Add your OpenAI API key
4. Test the connection
5. Link to the "LLM Analysis - GPT-4" node

#### Baserow HTTP Request Credentials
1. Create new **Header Auth** credential
2. Set header name: `Authorization`
3. Set header value: `Token h9JNHcGxmXZRIICUjpbHvVcKc5geaASA`
4. Link to the "Save to Baserow CRM" node

## 2. Baserow CRM Configuration

### Step 1: Database Setup

Your Baserow database should have these fields configured:

```json
{
  "table_id": "698",
  "required_fields": {
    "field_6755": "Client Name (Text)",
    "field_6756": "Meeting Stage (Single Select)",
    "field_6764": "Urgency Score (Number)",
    "field_6765": "Follow Up Required (Checkbox)"
  },
  "recommended_fields": {
    "estate_value": "Estate Value (Text)",
    "estate_complexity": "Estate Complexity (Single Select)",
    "beneficiaries_count": "Number of Beneficiaries (Number)",
    "real_estate": "Has Real Estate (Checkbox)",
    "business_owner": "Owns Business (Checkbox)",
    "quality_score": "Data Quality Score (Number)",
    "urgency_level": "Urgency Level (Single Select)",
    "notes": "Comprehensive Notes (Long Text)"
  }
}
```

### Step 2: Update Baserow Configuration

1. Edit the **baserow_config.json** file:
```json
{
  "baserow": {
    "base_url": "YOUR_BASEROW_URL",
    "database_id": "YOUR_DATABASE_ID",
    "token": "YOUR_BASEROW_TOKEN",
    "tables": {
      "CRM": {
        "id": "YOUR_TABLE_ID",
        "fields": {
          "Name": "YOUR_NAME_FIELD_ID"
        }
      }
    }
  }
}
```

2. Update the workflow's "Save to Baserow CRM" node with your field IDs

## 3. Webhook Configuration

### Step 1: Enable Webhook Trigger

The workflow includes a webhook trigger at: `/bmad-estate-processor`

**Webhook URL**: `https://your-n8n-instance.com/webhook/bmad-estate-processor`

### Step 2: Webhook Payload Structure

Send POST requests with this payload structure:

```json
{
  "transcript_path": "/path/to/your/transcripts",
  "batch_size": 5,
  "parallel": true,
  "bmad_mode": "enhanced"
}
```

**Parameters:**
- `transcript_path`: Path to directory containing transcript files
- `batch_size`: Number of files to process in each batch (default: 5)
- `parallel`: Enable parallel processing (default: true)
- `bmad_mode`: Processing mode - "basic", "enhanced", or "validate"

### Step 3: Test Webhook

```bash
curl -X POST "https://your-n8n-instance.com/webhook/bmad-estate-processor" \
  -H "Content-Type: application/json" \
  -d '{
    "transcript_path": "/Users/joshuavaughan/Documents/McAdams Transcripts",
    "batch_size": 3,
    "bmad_mode": "enhanced"
  }'
```

## 4. File System Configuration

### Step 1: Transcript File Organization

Ensure your transcript files are organized as:
```
/Users/joshuavaughan/Documents/McAdams Transcripts/
├── Client1_Meeting_Date.txt
├── Client2_Meeting_Date.txt
└── ...
```

### Step 2: File Naming Convention

The workflow extracts client names from filenames using these patterns:
- `ClientName: Meeting Notes.txt`
- `ClientName - Meeting Date.txt`
- `ClientName_Meeting_Info.txt`
- `ClientName Meeting YYYY.txt`

### Step 3: File Permissions

Ensure n8n has read access to the transcript directory:
```bash
chmod -R 755 "/Users/joshuavaughan/Documents/McAdams Transcripts"
```

## 5. BMAD Agents Integration (Optional Enhanced Features)

### Step 1: Deploy BMAD Agents

If you want to use the full BMAD methodology, deploy these agents:

1. **Estate Planning Analyst**: Enhanced domain expertise
2. **Document Validator**: Quality assurance and validation
3. **Email Orchestrator**: Personalized follow-up generation
4. **Knowledge Extractor**: Advanced insights and competitive intelligence
5. **Pipeline Manager**: Performance monitoring and optimization

### Step 2: Configure Agent Endpoints

Update the workflow's function nodes to call your deployed agents:

```javascript
// Example agent configuration
const agentEndpoints = {
  estate_analyst: 'http://localhost:3001/analyze',
  validator: 'http://localhost:3002/validate',
  email_orchestrator: 'http://localhost:3003/generate-email',
  knowledge_extractor: 'http://localhost:3004/extract-insights',
  pipeline_manager: 'http://localhost:3005/monitor'
};
```

## 6. Environment Variables

Set these environment variables in your n8n instance:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export BASEROW_URL="http://localhost"
export BASEROW_TOKEN="your-baserow-token"
export TRANSCRIPT_PATH="/Users/joshuavaughan/Documents/McAdams Transcripts"
export BMAD_MODE="enhanced"
```

## 7. Performance Optimization

### Step 1: Batch Size Tuning

Optimize batch size based on your system resources:

- **Small systems**: batch_size = 3-5
- **Medium systems**: batch_size = 5-10
- **Large systems**: batch_size = 10-15

### Step 2: Parallel Processing

Enable parallel processing for better throughput:
- Set `parallel: true` in webhook payload
- Monitor system resources during processing
- Adjust batch size if memory usage is high

### Step 3: Timeout Configuration

Configure timeouts based on your LLM response times:
```javascript
const timeoutConfig = {
  llm_timeout: 300000,      // 5 minutes for LLM analysis
  file_read_timeout: 30000, // 30 seconds for file operations
  api_timeout: 60000        // 1 minute for API calls
};
```

## 8. Monitoring and Alerts

### Step 1: Enable Execution Logging

In n8n settings:
1. Enable "Save Execution Progress"
2. Enable "Save Manual Executions"
3. Set log level to "info" for production monitoring

### Step 2: Quality Monitoring

The workflow provides quality metrics:
- **Overall Quality Score**: Average across all processed files
- **Success Rate**: Percentage of successful extractions
- **Review Queue Size**: Number of files requiring human review
- **Processing Time**: Average time per transcript

### Step 3: Alert Configuration

Set up alerts for:
- Quality scores below 75%
- Processing failures exceeding 5%
- High-urgency clients (score >= 8)
- Processing time exceeding 10 minutes per batch

## 9. Manual Processing

### Step 1: Use Manual Trigger

For one-time batch processing:
1. Click the "Manual Trigger - Batch Process" node
2. The workflow will process all files in the configured directory
3. Monitor progress in the execution log

### Step 2: Processing Modes

Choose the appropriate processing mode:

- **basic**: Standard GPT-4 analysis only
- **enhanced**: Full BMAD methodology with all 5 agents
- **validate**: Quality validation of existing extractions

## 10. Troubleshooting

### Common Issues

**Issue**: "No transcript files found"
**Solution**: Check transcript path and file permissions

**Issue**: "OpenAI API rate limiting"
**Solution**: Implement exponential backoff or reduce batch size

**Issue**: "Baserow connection failed"
**Solution**: Verify API token and database permissions

**Issue**: "Quality scores consistently low"
**Solution**: Review and enhance extraction prompts

### Debug Mode

Enable debug logging in function nodes:
```javascript
console.log(`🔍 Debug: Processing ${clientName}`);
console.log(`   File: ${fileName}`);
console.log(`   Content Length: ${content.length}`);
```

### Performance Monitoring

Monitor these metrics:
- **Processing Rate**: Files per hour
- **Error Rate**: Percentage of failed extractions
- **Quality Distribution**: Breakdown by quality score ranges
- **Resource Usage**: CPU and memory consumption

## 11. Production Deployment Checklist

- [ ] n8n workflow imported and tested
- [ ] OpenAI credentials configured and tested
- [ ] Baserow database structure matches requirements
- [ ] Webhook endpoint accessible and tested
- [ ] Transcript files accessible with proper permissions
- [ ] Environment variables set correctly
- [ ] Batch size optimized for your system
- [ ] Monitoring and alerting configured
- [ ] Error handling tested with sample failures
- [ ] Documentation and runbooks prepared

## 12. Expected Results

After successful setup, you should see:

### Processing Metrics
- **Throughput**: 10-20 transcripts per hour (depending on system)
- **Quality**: 80%+ average quality score
- **Success Rate**: 95%+ successful extractions
- **Automation**: 100% automated processing with human review only for edge cases

### Business Outcomes
- **Comprehensive client profiles** with 40+ data points
- **Personalized follow-up emails** generated automatically
- **Quality-scored extractions** with validation
- **Advanced insights** including competitive intelligence
- **Real-time monitoring** of processing pipeline

## Support and Maintenance

For ongoing support:
1. Monitor execution logs daily
2. Review quality metrics weekly
3. Update prompts based on new transcript patterns
4. Scale batch sizes based on volume changes
5. Maintain BMAD agent endpoints if using enhanced mode

This production workflow represents a significant advancement over basic transcript processing, providing enterprise-grade automation with the specialized expertise of the BMAD methodology.