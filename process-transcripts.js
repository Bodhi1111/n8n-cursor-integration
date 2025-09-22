#!/usr/bin/env node
/**
 * Production-Ready Transcript Processor
 * Processes estate planning transcripts with BMAD agents
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

class TranscriptProcessor {
  constructor(config = {}) {
    this.baserowToken = config.baserowToken || process.env.BASEROW_TOKEN || 'h9JNHcGxmXZRIICUjpbHvVcKc5geaASA';
    this.baserowUrl = config.baserowUrl || process.env.BASEROW_URL || 'http://localhost';
    this.tableId = config.tableId || process.env.BASEROW_TABLE_ID || '698';
    this.ollamaUrl = config.ollamaUrl || process.env.OLLAMA_URL || 'http://localhost:11434';
    this.ollamaModel = config.ollamaModel || process.env.OLLAMA_MODEL || 'gpt-oss:20b';
    this.stats = {
      processed: 0,
      successful: 0,
      failed: 0,
      startTime: Date.now()
    };
  }

  async processTranscript(transcriptPath) {
    console.log(`\n📄 Processing: ${path.basename(transcriptPath)}`);

    try {
      // Read transcript
      const content = fs.readFileSync(transcriptPath, 'utf8');

      // Extract basic metadata
      const clientName = path.basename(transcriptPath).replace(/[:\-].*/, '').trim();

      // Call Ollama for analysis
      console.log('   🧠 Running AI analysis...');
      const analysis = await this.analyzeWithOllama(content, clientName);

      // Save to Baserow if valid
      if (analysis && !analysis.error) {
        console.log('   💾 Saving to CRM...');
        await this.saveToBaserow(analysis);
        this.stats.successful++;
        console.log(`   ✅ Successfully processed: ${clientName}`);
        return { success: true, data: analysis };
      } else {
        this.stats.failed++;
        console.log(`   ❌ Failed to analyze: ${analysis?.error || 'Unknown error'}`);
        return { success: false, error: analysis?.error };
      }

    } catch (error) {
      this.stats.failed++;
      console.log(`   ❌ Error: ${error.message}`);
      return { success: false, error: error.message };
    } finally {
      this.stats.processed++;
    }
  }

  async analyzeWithOllama(transcript, clientName) {
    const prompt = `You are analyzing an estate planning meeting transcript. Extract the following information and return ONLY a JSON object.

CLIENT NAME: ${clientName}

MEETING CONTENT (first 5000 characters):
${transcript.substring(0, 5000)}

Return this exact JSON structure with your analysis:
{
  "client_name": "${clientName}",
  "meeting_stage": "Follow Up",
  "marital_status": "Single",
  "urgency_score": 5,
  "key_pain_points": "needs estate planning",
  "follow_up_required": true
}

Important: Return ONLY the JSON object, no other text.`;

    try {
      const response = await axios.post(`${this.ollamaUrl}/api/generate`, {
        model: this.ollamaModel,
        prompt: prompt,
        stream: false,
        temperature: 0.1,
        options: {
          num_predict: 500
        }
      }, {
        timeout: 30000 // 30 second timeout
      });

      // Extract JSON from response - check both response and thinking fields
      const responseText = response.data.response || response.data.thinking || '';

      // Try to find JSON in the response
      let jsonMatch = responseText.match(/\{[\s\S]*\}/);

      if (!jsonMatch) {
        // Fallback: try to find JSON-like structure
        const startIdx = responseText.indexOf('{');
        const endIdx = responseText.lastIndexOf('}');
        if (startIdx >= 0 && endIdx > startIdx) {
          jsonMatch = [responseText.substring(startIdx, endIdx + 1)];
        }
      }

      if (jsonMatch) {
        try {
          const data = JSON.parse(jsonMatch[0]);
          // Add metadata
          data.Name = clientName;
          data.processed_date = new Date().toISOString();
          data.transcript_file = path.basename(transcript);

          // Ensure proper data types
          if (data.urgency_score) {
            data.urgency_score = parseInt(data.urgency_score) || 5;
          }
          if (typeof data.follow_up_required === 'string') {
            data.follow_up_required = data.follow_up_required === 'true';
          }

          return data;
        } catch (parseError) {
          console.error('   ⚠️ JSON parse error:', parseError.message);
          console.error('   📄 Attempted to parse:', jsonMatch[0].substring(0, 200));
          console.error('   📄 Full response text:', responseText.substring(0, 500));
        }
      }

      // If all else fails, return basic data
      return {
        client_name: clientName,
        Name: clientName,
        meeting_stage: 'Follow Up',
        urgency_score: 5,
        follow_up_required: true,
        key_pain_points: 'Unable to extract details from transcript',
        error: 'AI analysis incomplete'
      };

    } catch (error) {
      console.error('   ⚠️ Ollama error:', error.message);

      // Check specific error types for better debugging
      if (error.code === 'ECONNREFUSED') {
        console.error('   🔌 Connection refused - is Ollama running on', this.ollamaUrl, '?');
      } else if (error.response) {
        console.error('   📡 HTTP error:', error.response.status, error.response.statusText);
        console.error('   📄 Response data:', error.response.data);
      } else if (error.request) {
        console.error('   ⏰ Request timeout or network error');
      }

      // Fallback to basic extraction
      return {
        Name: clientName,
        client_name: clientName,
        meeting_stage: 'Follow Up',
        processed_date: new Date().toISOString(),
        error: `AI analysis failed: ${error.message}`
      };
    }
  }

  async saveToBaserow(data) {
    try {
      // Map our data to Baserow field IDs with proper validation
      // Validate meeting_stage and use only valid options
      const validMeetingStages = ['Follow Up', 'Consultation', 'Closed Won', 'Closed Lost'];
      const meetingStage = (data.meeting_stage && validMeetingStages.includes(data.meeting_stage))
        ? data.meeting_stage
        : 'Follow Up';

      const baserowData = {
        field_6755: String(data.client_name || data.Name || 'Unknown'),  // lead_name (text)
        field_6756: meetingStage,                                        // meeting_stage (single select)
        field_6764: Math.min(10, Math.max(1, parseInt(data.urgency_score) || 5)), // urgency_score (rating 1-10)
        field_6765: Boolean(data.follow_up_required),                    // follow_up_required (boolean)
        field_6767: new Date().toISOString().split('T')[0]               // processed_date (date)
      };

      // Add optional fields only if they have valid values
      if (data.marital_status && ['Single', 'Married', 'Divorced', 'Widowed'].includes(data.marital_status)) {
        baserowData.field_6757 = data.marital_status;
      }

      if (data.children_count && !isNaN(data.children_count)) {
        baserowData.field_6758 = parseInt(data.children_count);
      }

      if (data.estate_value) {
        const estateNum = parseInt(String(data.estate_value).replace(/[^0-9]/g, ''));
        if (!isNaN(estateNum) && estateNum > 0) {
          baserowData.field_6759 = estateNum;
        }
      }

      if (data.key_pain_points) {
        baserowData.field_6762 = String(data.key_pain_points).substring(0, 1000); // Limit length
      }

      if (data.objections) {
        baserowData.field_6763 = String(data.objections).substring(0, 1000);
      }

      if (data.state && data.state.length === 2) {
        baserowData.field_6768 = data.state.toUpperCase();
      }

      // Remove undefined/null values
      Object.keys(baserowData).forEach(key => {
        if (baserowData[key] === undefined || baserowData[key] === null) {
          delete baserowData[key];
        }
      });

      console.log('   📝 Saving data with field IDs...');

      const response = await axios.post(
        `${this.baserowUrl}/api/database/rows/table/${this.tableId}/`,
        baserowData,
        {
          headers: {
            'Authorization': `Token ${this.baserowToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return response.data;

    } catch (error) {
      console.error('   ⚠️ Baserow error:', error.response?.data || error.message);
      throw error;
    }
  }

  async processBatch(directory, limit = null) {
    console.log(`\n📁 Processing transcripts from: ${directory}`);

    const files = fs.readdirSync(directory)
      .filter(f => f.endsWith('.txt'))
      .slice(0, limit);

    console.log(`📊 Found ${files.length} transcripts to process\n`);

    const results = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const filePath = path.join(directory, file);

      console.log(`[${i+1}/${files.length}] Processing...`);
      const result = await this.processTranscript(filePath);
      results.push({ file, ...result });

      // Brief pause between files
      if (i < files.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    // Print summary
    const duration = Math.round((Date.now() - this.stats.startTime) / 1000);
    console.log(`\n${'='.repeat(50)}`);
    console.log(`📊 PROCESSING COMPLETE`);
    console.log(`${'='.repeat(50)}`);
    console.log(`✅ Successful: ${this.stats.successful}`);
    console.log(`❌ Failed: ${this.stats.failed}`);
    console.log(`📈 Total: ${this.stats.processed}`);
    console.log(`⏱️ Duration: ${duration} seconds`);
    console.log(`🚀 Rate: ${(this.stats.processed / duration).toFixed(2)} files/second`);

    // Save report
    const reportPath = path.join(__dirname, 'processing-report.json');
    fs.writeFileSync(reportPath, JSON.stringify({
      summary: this.stats,
      duration,
      results
    }, null, 2));

    console.log(`\n📄 Detailed report saved to: ${reportPath}`);

    return results;
  }
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  const processor = new TranscriptProcessor();

  if (command === 'test') {
    // Test single file
    const testFile = args[1] || '/Users/joshuavaughan/Documents/McAdams Transcripts/Abbot Ware: Estate Planning Advisor Meeting.txt';
    processor.processTranscript(testFile)
      .then(result => console.log('\nResult:', result))
      .catch(console.error);

  } else if (command === 'batch') {
    // Batch processing
    const directory = args[1] || '/Users/joshuavaughan/Documents/McAdams Transcripts';
    const limit = args[2] ? parseInt(args[2]) : null;

    processor.processBatch(directory, limit)
      .catch(console.error);

  } else {
    console.log('Usage:');
    console.log('  node process-transcripts.js test [file]     - Test single file');
    console.log('  node process-transcripts.js batch [dir] [limit] - Batch process');
  }
}

module.exports = TranscriptProcessor;