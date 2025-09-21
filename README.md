# n8n + Cursor IDE Integration

This project provides a complete setup for developing n8n workflows locally using Docker, with Cursor IDE integration for rapid script development and testing.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js (for local script testing)
- Cursor IDE

### Setup

1. **Clone and navigate to the project:**

   ```bash
   cd ~/n8n-cursor-integration
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start n8n:**

   ```bash
   npm run start
   # or
   docker-compose up -d
   ```

4. **Access n8n:**

   - Open <http://localhost:5679> in your browser
   - Login with: `admin` / `admin`

5. **Test scripts locally:**

   ```bash
   npm run test
   ```

## 📁 Project Structure

```text
n8n-cursor-integration/
├── docker-compose.yml          # n8n Docker setup
├── package.json               # Node.js dependencies
├── tsconfig.json             # TypeScript configuration
├── scripts/                  # n8n Function node scripts
│   ├── test-runner.js        # Local testing utility
│   ├── data-processor.js     # Data transformation script
│   ├── api-payload-builder.js # API payload builder
│   ├── conditional-router.js  # Conditional routing logic
│   └── file-processor.js     # File processing utilities
├── examples/                 # Workflow templates and examples
│   ├── sample-workflows.json # Example workflow definitions
│   └── http-request-templates.json # HTTP request templates
├── workflows/               # n8n workflow exports (auto-created)
├── credentials/            # n8n credentials (auto-created)
└── data/                   # Shared data directory
```

## 🔧 Development Workflow

### 1. Script Development in Cursor IDE

1. **Open the project in Cursor IDE**
2. **Edit scripts in the `scripts/` directory**
3. **Test locally:**

   ```bash
   npm run test
   ```
4. **Copy tested code to n8n Function nodes**

### 2. n8n Workflow Development

1. **Access n8n UI:** <http://localhost:5679>
2. **Create new workflow**
3. **Add Function nodes and paste scripts from Cursor**
4. **Test and iterate**

### 3. Integration Examples

#### Data Processing Pipeline

```javascript
// In Cursor IDE: scripts/data-processor.js
// Copy this to n8n Function node

return items.map(item => {
  const data = item.json;
  return {
    json: {
      ...data,
      processed_at: new Date().toISOString(),
      status: data.message?.length > 10 ? 'valid' : 'needs_review'
    }
  };
});
```

#### API Integration

```javascript
// In Cursor IDE: scripts/api-payload-builder.js
// Use with HTTP Request nodes

const payload = {
  id: data.id || `generated_${Date.now()}`,
  timestamp: new Date().toISOString(),
  source: 'n8n-workflow',
  data: data
};

return [{ json: payload }];
```

## 🛠 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `data-processor.js` | Transform and validate data | Copy to Function node for data processing |
| `api-payload-builder.js` | Build API request payloads | Use before HTTP Request nodes |
| `conditional-router.js` | Route items based on conditions | Connect multiple outputs for branching |
| `file-processor.js` | Process file metadata | Handle file uploads and processing |

## 🔗 HTTP Request Templates

Pre-built templates for common API integrations:

- **POST JSON Data** - Send structured data via POST
- **GET with Query Parameters** - Dynamic GET requests
- **Webhook Receiver** - Send data to external webhooks
- **File Upload** - Upload files with metadata

## 🐳 Docker Commands

```bash
# Start n8n
npm run start
# or
docker-compose up -d

# Stop n8n
npm run stop
# or
docker-compose down

# View logs
npm run logs
# or
docker-compose logs -f n8n

# Restart
npm run restart
```

## 🧪 Local Testing

The `test-runner.js` script allows you to test your n8n Function node scripts locally:

```bash
# Test all scripts
npm run test

# Test specific script
node scripts/test-runner.js
```

### Mock Data Structure
```javascript
const mockContext = {
  items: [{
    json: {
      message: "Hello from n8n!",
      timestamp: new Date().toISOString(),
      user: "test-user"
    }
  }]
};
```

## 📝 Best Practices

### 1. Script Development
- Write and test scripts in Cursor IDE first
- Use the local test runner to validate logic
- Copy working scripts to n8n Function nodes
- Keep scripts modular and reusable

### 2. Workflow Design
- Use descriptive node names
- Add comments in Function nodes
- Test with sample data before production
- Export workflows for version control

### 3. Error Handling
- Always validate input data
- Use try-catch blocks in complex scripts
- Add meaningful error messages
- Test error scenarios

## 🔒 Security Notes

- Change default n8n credentials in production
- Update the encryption key in `docker-compose.yml`
- Use environment variables for sensitive data
- Regularly update Docker images

## 🚀 Advanced Features

### Custom Node Development
- Extend n8n with custom nodes
- Share nodes across workflows
- Create reusable components

### Webhook Integration
- Local webhook endpoints for testing
- Integration with external services
- Real-time data processing

### File System Access
- Read/write local files
- Process uploaded files
- Generate reports and exports

## 📚 Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Function Node Guide](https://docs.n8n.io/code-examples/methods-variables-examples/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Cursor IDE Documentation](https://cursor.sh/docs)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new scripts
4. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.
