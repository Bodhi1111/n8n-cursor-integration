# Baserow Integration Guide

## Quick Start

1. **Start the containers:**
   ```bash
   ./start-baserow.sh
   ```

2. **Access the services:**
   - Baserow: http://localhost
   - n8n: http://localhost:5679 (admin/admin)

## Setup Baserow

1. Open http://localhost in your browser
2. Create your first account
3. Create a workspace and database
4. Go to Settings → API tokens → Create token
5. Copy your API token for n8n integration

## Integration Methods

### Method 1: HTTP Request Node (Recommended)

Use n8n's HTTP Request node to interact with Baserow's REST API.

**Important:** Use `http://host.docker.internal` instead of `localhost` when connecting from n8n container to Baserow.

Example endpoints:
- List rows: `GET http://host.docker.internal/api/database/rows/table/{table_id}/`
- Create row: `POST http://host.docker.internal/api/database/rows/table/{table_id}/`
- Update row: `PATCH http://host.docker.internal/api/database/rows/table/{table_id}/{row_id}/`
- Delete row: `DELETE http://host.docker.internal/api/database/rows/table/{table_id}/{row_id}/`

### Method 2: Webhook Triggers

Set up webhooks in n8n to receive data from external sources and write to Baserow:

1. Create a Webhook node in n8n
2. Copy the webhook URL
3. Send data to the webhook
4. Use HTTP Request node to write to Baserow

### Method 3: Scheduled Sync

Create workflows that sync data between Baserow and other systems on a schedule:

1. Use Schedule Trigger node
2. Fetch data from source
3. Transform data as needed
4. Write to Baserow using HTTP Request

## Common Use Cases

### 1. Form Submission to Database
- Webhook receives form data
- Validate and transform data
- Create new row in Baserow

### 2. Data Synchronization
- Schedule trigger every hour
- Fetch data from external API
- Update or create rows in Baserow

### 3. Report Generation
- Read data from Baserow
- Process and aggregate data
- Send reports via email or Slack

### 4. CRM Integration
- Sync contacts between systems
- Update customer information
- Track interactions in Baserow

## API Authentication

Always include the Authorization header:
```
Authorization: Token YOUR_API_TOKEN
```

## Troubleshooting

### Connection Issues
- Use `http://host.docker.internal` from n8n to connect to Baserow
- Ensure both containers are on the same network
- Check container logs: `docker logs baserow` or `docker logs n8n-cursor-integration`

### API Errors
- Verify your API token is correct
- Check table and field IDs in Baserow
- Review API documentation at https://baserow.io/api-docs

### Performance Tips
- Use pagination for large datasets
- Implement rate limiting in your workflows
- Cache frequently accessed data

## Example Workflow

Import the example workflow from `examples/baserow-n8n-integration.json`:

1. Open n8n (http://localhost:5679)
2. Go to Workflows → Import from File
3. Select the example file
4. Update the API token and table IDs
5. Test the workflow

## Docker Commands

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker logs -f baserow
docker logs -f n8n-cursor-integration

# Restart a container
docker restart baserow

# Check container status
docker ps

# Access container shell
docker exec -it baserow bash
```

## Security Notes

1. **Change default passwords** in production
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** for production deployments
4. **Restrict API token permissions** in Baserow
5. **Use secrets management** for credentials

## Resources

- [Baserow API Documentation](https://baserow.io/api-docs)
- [n8n Documentation](https://docs.n8n.io)
- [Docker Networking](https://docs.docker.com/network/)
- [Baserow Templates](https://baserow.io/templates)