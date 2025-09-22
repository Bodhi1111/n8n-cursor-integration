/**
 * N8N Code Node - Enhanced BMAD Estate Planning Analysis
 * Drop this code into your N8N "BMad Analyst - Batch Mode" Code node
 */

// For use in N8N Code node
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Get the transcript file path from previous node
const transcriptPath = $input.first().json.filepath || $input.first().json.path;
const transcriptContent = $input.first().json.content || $input.first().binary.data;

// Option 1: Execute our custom BMAD analyst directly
async function runBMADAnalysis() {
  try {
    // Save transcript content to temp file if needed
    const fs = require('fs');
    const tempFile = `/tmp/transcript_${Date.now()}.txt`;

    if (transcriptContent && !transcriptPath) {
      fs.writeFileSync(tempFile, transcriptContent);
    }

    const fileToAnalyze = transcriptPath || tempFile;

    // Run our enhanced estate planning analyst
    const command = `cd /Users/joshuavaughan/n8n-cursor-integration && node agents/estate-planning-analyst.js "${fileToAnalyze}"`;

    const { stdout, stderr } = await execPromise(command, {
      maxBuffer: 1024 * 1024 * 10 // 10MB buffer
    });

    // Parse the JSON output
    let analysisResult;
    try {
      // Extract JSON from output
      const jsonMatch = stdout.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        analysisResult = JSON.parse(jsonMatch[0]);
      } else {
        analysisResult = { error: 'No JSON found in output', raw: stdout };
      }
    } catch (parseError) {
      analysisResult = {
        error: 'Failed to parse analysis',
        parseError: parseError.message,
        raw: stdout.substring(0, 500)
      };
    }

    // Clean up temp file if created
    if (!transcriptPath && fs.existsSync(tempFile)) {
      fs.unlinkSync(tempFile);
    }

    // Add metadata
    analysisResult.processing = {
      agent: 'BMAD Estate Planning Analyst',
      timestamp: new Date().toISOString(),
      filename: transcriptPath ? transcriptPath.split('/').pop() : 'direct_content'
    };

    return analysisResult;

  } catch (error) {
    return {
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}

// Option 2: Use the full BMAD-N8N bridge for enhanced processing
async function runEnhancedBMADProcessing() {
  try {
    const command = `cd /Users/joshuavaughan/n8n-cursor-integration && node agents/bmad-n8n-bridge.js process "${transcriptPath}"`;

    const { stdout, stderr } = await execPromise(command, {
      maxBuffer: 1024 * 1024 * 10,
      timeout: 120000 // 2 minute timeout
    });

    // Parse the comprehensive result
    let result;
    try {
      const jsonMatch = stdout.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        result = JSON.parse(jsonMatch[0]);
      } else {
        result = { error: 'No JSON found', raw: stdout };
      }
    } catch (parseError) {
      result = {
        error: 'Parse failed',
        details: parseError.message,
        preview: stdout.substring(0, 500)
      };
    }

    return result;

  } catch (error) {
    return {
      error: error.message,
      type: 'enhanced_processing_error',
      timestamp: new Date().toISOString()
    };
  }
}

// Option 3: Simplified analysis with quality scoring
async function runQuickBMADValidation() {
  // This is for when you already have extracted data
  // and just want to validate quality

  const extractedData = $input.first().json.extractedData || $input.first().json;

  if (!extractedData) {
    return { error: 'No data to validate' };
  }

  try {
    // Save data to temp file
    const fs = require('fs');
    const tempDataFile = `/tmp/data_${Date.now()}.json`;
    fs.writeFileSync(tempDataFile, JSON.stringify(extractedData));

    // Run validator
    const command = `cd /Users/joshuavaughan/n8n-cursor-integration && node agents/document-validator.js "${tempDataFile}"`;

    const { stdout, stderr } = await execPromise(command);

    // Parse validation result
    let validationResult;
    try {
      const jsonMatch = stdout.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        validationResult = JSON.parse(jsonMatch[0]);
      }
    } catch (e) {
      validationResult = { error: 'Validation parse error' };
    }

    // Clean up
    if (fs.existsSync(tempDataFile)) {
      fs.unlinkSync(tempDataFile);
    }

    return validationResult;

  } catch (error) {
    return {
      error: error.message,
      type: 'validation_error'
    };
  }
}

// Main execution - choose your processing mode
const processingMode = $input.first().json.mode || 'enhanced'; // 'basic', 'enhanced', or 'validate'

let result;
switch(processingMode) {
  case 'enhanced':
    result = await runEnhancedBMADProcessing();
    break;
  case 'validate':
    result = await runQuickBMADValidation();
    break;
  case 'basic':
  default:
    result = await runBMADAnalysis();
    break;
}

// Return the result for the next node
return result;