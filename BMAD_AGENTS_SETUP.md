# 🎯 BMAD-Method Agents Integration Guide

## 🏆 Your BMAD Arsenal

Your n8n-cursor-integration project already includes the `bmad-method` package (v4.43.1) with access to:

### Core Agents
- **BMad Master** (`bmad-master`) - Universal task executor
- **BMad Orchestrator** (`bmad-orchestrator`) - Multi-agent coordinator

### Expansion Packs Available
- **Infrastructure/DevOps** - Server management, deployment automation
- **Game Development** (Godot, Unity, Phaser) - Complete game dev teams
- **Creative Writing** - Content creation and storytelling

### Estate Planning Specialization
- **BMAD-METHOD CRM** - Behavioral, Meeting, Asset, Decision analysis
- **Auto-monitoring** - Transcript processing automation
- **Baserow Integration** - Client data management

## 🚀 Quick Start: Using BMAD Agents

### 1. Activate BMad Orchestrator
```bash
# In your project directory
npx bmad-method bmad-orchestrator
```

### 2. Core Commands (all start with *)
```
*help          # Show all available commands
*agent         # List available agents
*agent {name}  # Transform into specific agent
*workflow      # List available workflows
*kb-mode       # Access BMAD knowledge base
*status        # Show current agent/context
```

### 3. Agent Transformation Examples
```
*agent pm           # Become Product Manager
*agent architect    # Become System Architect
*agent developer    # Become Developer
*agent game-dev     # Game development specialist
*agent qa           # Quality Assurance specialist
```

## 🔄 Integration with Your N8N Workflows

### Method 1: Direct Agent Commands in N8N
Create n8n nodes that execute bmad commands:

```javascript
// In an n8n Code node
const { exec } = require('child_process');

// Execute BMAD agent command
const command = 'npx bmad-method bmad-master "*task create-doc prd-tmpl"';
exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error}`);
    return;
  }
  console.log(`BMAD Output: ${stdout}`);
});
```

### Method 2: Node.js Integration
```javascript
// Create a new script: scripts/bmad-agent-runner.js
const { spawn } = require('child_process');

class BMADAgentRunner {
  constructor() {
    this.currentAgent = null;
  }

  async activateAgent(agentName) {
    return new Promise((resolve, reject) => {
      const bmad = spawn('npx', ['bmad-method', agentName]);

      bmad.stdout.on('data', (data) => {
        console.log(`BMAD: ${data}`);
        resolve(data.toString());
      });

      bmad.stderr.on('data', (data) => {
        console.error(`BMAD Error: ${data}`);
        reject(data.toString());
      });
    });
  }

  async executeTask(command) {
    // Execute BMAD command
    const result = await this.runCommand(`*${command}`);
    return result;
  }
}

module.exports = BMADAgentRunner;
```

### Method 3: Workflow Integration
Add to your `package.json` scripts:

```json
{
  "scripts": {
    "bmad:orchestrator": "npx bmad-method bmad-orchestrator",
    "bmad:master": "npx bmad-method bmad-master",
    "bmad:pm": "npx bmad-method bmad-orchestrator '*agent pm'",
    "bmad:architect": "npx bmad-method bmad-orchestrator '*agent architect'",
    "bmad:developer": "npx bmad-method bmad-orchestrator '*agent developer'"
  }
}
```

## 🎯 Recommended Workflow: Estate Planning + BMAD

### 1. Transcript Processing with BMAD Analysis
```bash
# Start the estate planning CRM
python3 deploy_bmad_crm.py

# In parallel, use BMAD agents for additional analysis
npm run bmad:orchestrator
# Then: *agent analyst
# Execute: *task create-deep-research-prompt
```

### 2. Document Generation Pipeline
```bash
# Use BMAD for document creation
npm run bmad:master
# Execute: *create-doc prd-tmpl
# Execute: *create-doc architecture-tmpl
```

### 3. Quality Assurance Workflow
```bash
# QA your generated content
npm run bmad:orchestrator
# Transform: *agent qa
# Execute: *checklist story-dod-checklist
```

## 🛠️ Custom Agent Integration Scripts

### Create BMAD-Enhanced N8N Nodes
1. **BMAD Document Generator Node**
2. **BMAD Quality Checker Node**
3. **BMAD Workflow Orchestrator Node**

### Integration with Existing Scripts
Your current scripts can be enhanced with BMAD:

- `sales-data-extractor.js` → Add BMAD analysis agent
- `email-recap-generator.js` → Use BMAD creative writing
- `batch-processor-helper.js` → Orchestrate with BMAD workflows

## 🎉 Next Steps

1. **Try the Orchestrator**: `npm run bmad:orchestrator`
2. **Explore Available Agents**: Type `*agent` to see all options
3. **Create Custom Workflows**: Combine BMAD with your estate planning CRM
4. **Scale Your Analysis**: Use BMAD for deeper transcript insights

## 🔗 Useful Commands Reference

```bash
# Start any agent
npx bmad-method {agent-name}

# Common workflows
*help                    # Show commands
*agent                   # List agents
*workflow               # List workflows
*task                   # List tasks
*kb-mode                # Knowledge base
*chat-mode              # Conversational assistance
*status                 # Current state
*exit                   # Return to orchestrator
```

## 💡 Pro Tips

- **Agent Switching**: Use orchestrator to seamlessly switch between specialists
- **Knowledge Base**: Access BMAD methodology with `*kb-mode`
- **Task Automation**: Chain BMAD tasks in your n8n workflows
- **Quality Gates**: Use BMAD checklists as workflow validation steps

🎯 **Your estate planning CRM + BMAD agents = Ultimate automation powerhouse!**