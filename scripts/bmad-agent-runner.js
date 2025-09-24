#!/usr/bin/env node
/**
 * BMAD Agent Runner for N8N Workflows
 * Integrates BMAD-Method agents into your automation pipeline
 */

const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');

class BMADAgentRunner {
  constructor() {
    this.currentAgent = null;
    this.sessionId = Date.now();
    this.logFile = path.join(__dirname, '../logs', `bmad-session-${this.sessionId}.log`);
    this.ensureLogDirectory();
  }

  ensureLogDirectory() {
    const logDir = path.dirname(this.logFile);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
  }

  log(message) {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] ${message}\n`;
    fs.appendFileSync(this.logFile, logEntry);
    console.log(message);
  }

  /**
   * Activate a specific BMAD agent
   * @param {string} agentName - Name of the agent to activate
   * @returns {Promise<string>} Agent response
   */
  async activateAgent(agentName) {
    this.log(`🎯 Activating BMAD Agent: ${agentName}`);

    return new Promise((resolve, reject) => {
      const command = `npx bmad-method ${agentName}`;

      exec(command, { cwd: process.cwd() }, (error, stdout, stderr) => {
        if (error) {
          this.log(`❌ Error activating agent: ${error.message}`);
          reject(error);
          return;
        }

        if (stderr) {
          this.log(`⚠️ Agent warning: ${stderr}`);
        }

        this.currentAgent = agentName;
        this.log(`✅ Agent ${agentName} activated successfully`);
        resolve(stdout);
      });
    });
  }

  /**
   * Execute a BMAD command (automatically prefixes with *)
   * @param {string} command - Command to execute
   * @param {object} options - Additional options
   * @returns {Promise<string>} Command output
   */
  async executeCommand(command, options = {}) {
    if (!command.startsWith('*')) {
      command = '*' + command;
    }

    this.log(`🔄 Executing BMAD command: ${command}`);

    return new Promise((resolve, reject) => {
      const fullCommand = `echo "${command}" | npx bmad-method ${this.currentAgent || 'bmad-orchestrator'}`;

      exec(fullCommand, { cwd: process.cwd() }, (error, stdout, stderr) => {
        if (error) {
          this.log(`❌ Command failed: ${error.message}`);
          reject(error);
          return;
        }

        this.log(`✅ Command completed: ${command}`);
        resolve(stdout);
      });
    });
  }

  /**
   * Generate a document using BMAD
   * @param {string} templateType - Type of template (prd, architecture, story, etc.)
   * @param {object} context - Context data for the document
   * @returns {Promise<string>} Generated document
   */
  async generateDocument(templateType, context = {}) {
    this.log(`📄 Generating document: ${templateType}`);

    try {
      // Activate appropriate agent if not already active
      if (!this.currentAgent || this.currentAgent === 'bmad-orchestrator') {
        await this.activateAgent('bmad-master');
      }

      // Execute document creation
      const result = await this.executeCommand(`create-doc ${templateType}`);

      this.log(`✅ Document generated successfully`);
      return result;
    } catch (error) {
      this.log(`❌ Document generation failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Run a quality assurance checklist
   * @param {string} checklistType - Type of checklist to run
   * @returns {Promise<string>} QA results
   */
  async runQualityCheck(checklistType) {
    this.log(`🔍 Running quality check: ${checklistType}`);

    try {
      // Switch to QA agent if available
      await this.activateAgent('bmad-orchestrator');
      await this.executeCommand('agent qa');

      // Execute checklist
      const result = await this.executeCommand(`execute-checklist ${checklistType}`);

      this.log(`✅ Quality check completed`);
      return result;
    } catch (error) {
      this.log(`❌ Quality check failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Enhance estate planning transcript analysis with BMAD
   * @param {string} transcriptPath - Path to transcript file
   * @returns {Promise<object>} Enhanced analysis results
   */
  async enhanceTranscriptAnalysis(transcriptPath) {
    this.log(`🎯 Enhancing transcript analysis: ${transcriptPath}`);

    try {
      // Activate analyst agent
      await this.activateAgent('bmad-orchestrator');
      await this.executeCommand('agent analyst');

      // Create deep research prompt for transcript
      const analysisPrompt = await this.executeCommand('create-deep-research-prompt');

      // Process with existing estate planning analysis
      const enhancedAnalysis = {
        timestamp: new Date().toISOString(),
        transcriptPath,
        bmadAnalysis: analysisPrompt,
        recommendations: await this.generateFollowUpRecommendations()
      };

      this.log(`✅ Enhanced analysis completed`);
      return enhancedAnalysis;
    } catch (error) {
      this.log(`❌ Enhanced analysis failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Generate follow-up recommendations using creative writing agent
   * @returns {Promise<string>} Generated recommendations
   */
  async generateFollowUpRecommendations() {
    try {
      await this.activateAgent('bmad-orchestrator');
      await this.executeCommand('agent creative-writer');

      const recommendations = await this.executeCommand('task create-next-story');
      return recommendations;
    } catch (error) {
      this.log(`⚠️ Could not generate recommendations: ${error.message}`);
      return 'Standard follow-up recommended';
    }
  }

  /**
   * Orchestrate a complete workflow
   * @param {string} workflowType - Type of workflow to run
   * @param {object} params - Workflow parameters
   * @returns {Promise<object>} Workflow results
   */
  async orchestrateWorkflow(workflowType, params = {}) {
    this.log(`🎭 Orchestrating workflow: ${workflowType}`);

    try {
      await this.activateAgent('bmad-orchestrator');

      // Get workflow guidance
      const guidance = await this.executeCommand('workflow-guidance');

      // Execute specific workflow
      const workflowResult = await this.executeCommand(`workflow ${workflowType}`);

      const results = {
        workflowType,
        guidance,
        result: workflowResult,
        params,
        completedAt: new Date().toISOString()
      };

      this.log(`✅ Workflow orchestration completed`);
      return results;
    } catch (error) {
      this.log(`❌ Workflow orchestration failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Get current agent status and available commands
   * @returns {Promise<object>} Status information
   */
  async getStatus() {
    try {
      const status = await this.executeCommand('status');
      const help = await this.executeCommand('help');

      return {
        currentAgent: this.currentAgent,
        sessionId: this.sessionId,
        logFile: this.logFile,
        status,
        availableCommands: help
      };
    } catch (error) {
      this.log(`⚠️ Could not get status: ${error.message}`);
      return {
        currentAgent: this.currentAgent,
        sessionId: this.sessionId,
        error: error.message
      };
    }
  }
}

// Move function declaration to program root
async function runCLI(args, runner) {
  try {
    if (args.length === 0) {
      console.log('🎯 BMAD Agent Runner - Usage Examples:');
      console.log('');
      console.log('node bmad-agent-runner.js activate orchestrator');
      console.log('node bmad-agent-runner.js command help');
      console.log('node bmad-agent-runner.js generate prd-tmpl');
      console.log('node bmad-agent-runner.js qa story-dod-checklist');
      console.log('node bmad-agent-runner.js workflow greenfield-fullstack');
      console.log('node bmad-agent-runner.js status');
      return;
    }

    const [action, ...params] = args;

    switch (action) {
      case 'activate': {
        const result = await runner.activateAgent(params[0]);
        console.log(result);
        break;
      }

      case 'command': {
        const cmdResult = await runner.executeCommand(params[0]);
        console.log(cmdResult);
        break;
      }

      case 'generate': {
        const docResult = await runner.generateDocument(params[0]);
        console.log(docResult);
        break;
      }

      case 'qa': {
        const qaResult = await runner.runQualityCheck(params[0]);
        console.log(qaResult);
        break;
      }

      case 'workflow': {
        const workflowResult = await runner.orchestrateWorkflow(params[0]);
        console.log(JSON.stringify(workflowResult, null, 2));
        break;
      }

      case 'enhance': {
        const enhanceResult = await runner.enhanceTranscriptAnalysis(params[0]);
        console.log(JSON.stringify(enhanceResult, null, 2));
        break;
      }

      case 'status': {
        const status = await runner.getStatus();
        console.log(JSON.stringify(status, null, 2));
        break;
      }

      default:
        console.log(`❌ Unknown action: ${action}`);
    }
    } catch (error) {
      console.error(`❌ Error: ${error.message}`);
      process.exit(1);
    }
  }

  runCLI(args, runner);
}

module.exports = BMADAgentRunner;