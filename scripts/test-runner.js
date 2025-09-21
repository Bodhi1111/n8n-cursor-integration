#!/usr/bin/env node

/**
 * Test runner for n8n Function node scripts
 * This allows you to test your n8n scripts locally before copying them to n8n
 */

const fs = require('fs');
const path = require('path');

// Mock n8n context for testing
const mockContext = {
  items: [
    {
      json: {
        message: "Hello from n8n!",
        timestamp: new Date().toISOString(),
        user: "test-user"
      }
    }
  ],
  workflow: {
    id: "test-workflow",
    name: "Test Workflow"
  }
};

// Load and test scripts
function testScripts() {
  const scriptsDir = path.join(__dirname);
  const scriptFiles = fs.readdirSync(scriptsDir)
    .filter(file => file.endsWith('.js') && file !== 'test-runner.js');

  console.log('🧪 Testing n8n Function Node Scripts\n');

  scriptFiles.forEach(file => {
    console.log(`📄 Testing ${file}:`);
    
    try {
      // Load the script
      const scriptPath = path.join(scriptsDir, file);
      const scriptContent = fs.readFileSync(scriptPath, 'utf8');
      
      // Create a function from the script content
      const scriptFunction = new Function('items', 'context', 'return ' + scriptContent);
      
      // Execute the script with mock data
      const result = scriptFunction(mockContext.items, mockContext);
      
      console.log(`✅ Success:`, JSON.stringify(result, null, 2));
    } catch (error) {
      console.log(`❌ Error:`, error.message);
    }
    
    console.log('---\n');
  });
}

// Run tests if this file is executed directly
if (require.main === module) {
  testScripts();
}

module.exports = { testScripts, mockContext };
