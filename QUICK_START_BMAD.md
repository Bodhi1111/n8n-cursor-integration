# 🚀 Quick Start: BMAD Agents in Your N8N Workflow

## ⚡ Instant Commands

```bash
# Show help and available commands
npm run bmad:help

# Start the BMAD orchestrator (interactive)
npm run bmad:orchestrator

# Start BMAD master agent (direct task execution)
npm run bmad:master

# Check current agent status
npm run bmad:status

# Run specific BMAD commands
npm run bmad activate orchestrator
npm run bmad command help
npm run bmad generate prd-tmpl
npm run bmad qa story-dod-checklist
```

## 🎯 Integration with Your Estate Planning CRM

### 1. Enhanced Transcript Analysis
```bash
# Your existing flow: transcript → BMAD analysis → CRM
python3 deploy_bmad_crm.py     # Start estate planning CRM
npm run bmad:orchestrator      # Start BMAD in parallel

# In BMAD: *agent analyst
# Execute: *task create-deep-research-prompt
```

### 2. Document Generation Pipeline
```bash
# Generate follow-up emails with BMAD creative writing
npm run bmad activate orchestrator
# Then: *agent creative-writer
# Execute: *task create-next-story
```

### 3. Quality Assurance
```bash
# QA your estate planning workflows
npm run bmad qa story-dod-checklist
npm run bmad qa pm-checklist
```

## 🔄 Available Agents

Type `*agent` in orchestrator to see all:

- **bmad-master** - Universal task executor
- **bmad-orchestrator** - Multi-agent coordinator
- **architect** - System architecture design
- **pm** - Product management
- **analyst** - Data analysis and research
- **qa** - Quality assurance
- **creative-writer** - Content creation

## 🎛️ Agent Commands (all use * prefix)

```
*help          # Show available commands
*agent         # List all agents
*agent {name}  # Transform into specific agent
*workflow      # List available workflows
*task          # List available tasks
*kb-mode       # Access BMAD knowledge base
*chat-mode     # Conversational assistance
*status        # Show current state
*exit          # Return to orchestrator
```

## 💡 Estate Planning + BMAD Workflows

### Enhanced Client Analysis
1. **Transcript Processing**: Your existing BMAD-METHOD CRM
2. **Deep Analysis**: Use `*agent analyst` → `*task create-deep-research-prompt`
3. **Strategic Planning**: Use `*agent architect` → `*create-doc architecture-tmpl`
4. **Follow-up Content**: Use `*agent creative-writer` → generate personalized emails

### Document Generation
1. **PRD Creation**: `*create-doc prd-tmpl` for new service offerings
2. **Architecture Planning**: `*create-doc architecture-tmpl` for system design
3. **Story Creation**: `*create-doc story-tmpl` for client communication

### Quality Assurance
1. **Process Validation**: `*execute-checklist pm-checklist`
2. **Story Completeness**: `*execute-checklist story-dod-checklist`
3. **Change Management**: `*execute-checklist change-checklist`

## 🔗 Integration Points

### N8N Workflow Nodes
```javascript
// Example: Call BMAD from N8N Code node
const BMADRunner = require('./scripts/bmad-agent-runner.js');
const bmad = new BMADRunner();

// Generate document
const result = await bmad.generateDocument('prd-tmpl');

// Enhance transcript analysis
const enhanced = await bmad.enhanceTranscriptAnalysis(transcriptPath);

// Run quality check
const qaResult = await bmad.runQualityCheck('story-dod-checklist');
```

### Python Integration
```python
# Call BMAD from your existing Python scripts
import subprocess
import json

def run_bmad_command(command):
    result = subprocess.run(['npm', 'run', 'bmad', 'command', command],
                          capture_output=True, text=True)
    return result.stdout

# Example: enhance your estate planning analysis
analysis = run_bmad_command('create-deep-research-prompt')
```

## 🎉 Ready to Go!

Your BMAD-Method agents are now integrated and ready to enhance your estate planning automation:

1. **Start**: `npm run bmad:orchestrator`
2. **Explore**: Type `*help` to see all commands
3. **Transform**: Use `*agent {name}` to become any specialist
4. **Execute**: Run tasks, generate docs, perform QA
5. **Scale**: Integrate with your existing n8n workflows

🏆 **Combine your 352 transcript processing with BMAD intelligence for ultimate automation!**