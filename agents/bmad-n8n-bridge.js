#!/usr/bin/env node
/**
 * BMAD-N8N Integration Bridge
 * Connects BMAD agents with N8N workflows for enhanced transcript processing
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { spawn, exec } = require('child_process');

const EstatePlanningAnalyst = require('./estate-planning-analyst');
const DocumentValidator = require('./document-validator');

class BMADN8NBridge {
  constructor(config = {}) {
    this.config = {
      n8n_url: config.n8n_url || 'http://localhost:5678',
      baserow_url: config.baserow_url || 'http://localhost',
      ollama_url: config.ollama_url || 'http://localhost:11434',
      webhook_path: config.webhook_path || '/webhook/bmad-enhanced',
      processing_mode: config.processing_mode || 'enhanced', // 'basic' | 'enhanced' | 'parallel'
      quality_threshold: config.quality_threshold || 75
    };

    this.agents = {
      analyst: new EstatePlanningAnalyst({
        ollamaUrl: this.config.ollama_url,
        model: 'gpt-oss:20b'
      }),
      validator: new DocumentValidator({
        minimumScore: this.config.quality_threshold
      })
    };

    this.processingStats = {
      total_processed: 0,
      successful: 0,
      failed: 0,
      quality_scores: [],
      average_processing_time: 0,
      start_time: Date.now()
    };

    console.log(`🌉 BMAD-N8N Bridge initialized`);
    console.log(`🔗 N8N: ${this.config.n8n_url} | Mode: ${this.config.processing_mode}`);
  }

  // Main processing pipeline
  async processTranscript(transcriptPath, options = {}) {
    const startTime = Date.now();
    const processingId = this.generateProcessingId();

    console.log(`🚀 [${processingId}] Processing: ${path.basename(transcriptPath)}`);

    try {
      let result;

      switch (this.config.processing_mode) {
        case 'enhanced':
          result = await this.enhancedProcessing(transcriptPath, processingId);
          break;
        case 'parallel':
          result = await this.parallelProcessing(transcriptPath, processingId);
          break;
        case 'basic':
        default:
          result = await this.basicProcessing(transcriptPath, processingId);
          break;
      }

      // Add processing metadata
      result.processing_metadata = {
        processing_id: processingId,
        processing_time_ms: Date.now() - startTime,
        mode: this.config.processing_mode,
        timestamp: new Date().toISOString()
      };

      this.updateStats(true, Date.now() - startTime, result.validation?.overall_score);

      console.log(`✅ [${processingId}] Completed in ${Date.now() - startTime}ms`);
      return result;

    } catch (error) {
      console.error(`❌ [${processingId}] Failed:`, error.message);
      this.updateStats(false, Date.now() - startTime);

      return {
        error: error.message,
        processing_id: processingId,
        transcript_file: path.basename(transcriptPath),
        processing_time_ms: Date.now() - startTime
      };
    }
  }

  // Enhanced processing with BMAD agents
  async enhancedProcessing(transcriptPath, processingId) {
    console.log(`🧠 [${processingId}] Enhanced processing with BMAD agents`);

    // Step 1: BMAD Estate Planning Analyst
    console.log(`📊 [${processingId}] Running estate planning analysis...`);
    const analysisResult = await this.agents.analyst.analyzeTranscript(transcriptPath);

    if (analysisResult.error) {
      throw new Error(`Analysis failed: ${analysisResult.error}`);
    }

    // Step 2: Document Validation
    console.log(`🛡️ [${processingId}] Validating extracted data...`);
    const validation = await this.agents.validator.validateDocument(analysisResult);

    // Step 3: Quality gate check
    if (validation.overall_score < this.config.quality_threshold) {
      console.log(`⚠️ [${processingId}] Quality score ${validation.overall_score}% below threshold`);

      if (validation.recommendation === 'reject_and_reprocess') {
        throw new Error(`Data quality too low: ${validation.overall_score}%`);
      }
    }

    // Step 4: Apply auto-corrections
    let finalData = analysisResult;
    if (validation.auto_corrections && Object.keys(validation.auto_corrections).length > 0) {
      finalData = this.agents.validator.applyCorrections(analysisResult, validation.auto_corrections);
      console.log(`🔧 [${processingId}] Applied ${Object.keys(validation.auto_corrections).length} auto-corrections`);
    }

    // Step 5: Trigger N8N workflow (optional)
    if (this.config.trigger_n8n) {
      await this.triggerN8NWorkflow(finalData, processingId);
    }

    return {
      extracted_data: finalData,
      validation: validation,
      agent_analysis: analysisResult.agent_analysis,
      recommendation: validation.recommendation,
      quality_score: validation.overall_score
    };
  }

  // Parallel processing with multiple agents
  async parallelProcessing(transcriptPath, processingId) {
    console.log(`⚡ [${processingId}] Parallel processing with multiple agents`);

    const transcript = fs.readFileSync(transcriptPath, 'utf8');

    // Run multiple analyses in parallel
    const [
      bmadAnalysis,
      basicAnalysis
    ] = await Promise.all([
      this.agents.analyst.analyzeTranscript(transcriptPath),
      this.runBasicOllamaAnalysis(transcript)
    ]);

    // Merge results with BMAD taking priority
    const mergedData = this.mergeAnalysisResults(bmadAnalysis, basicAnalysis);

    // Validate merged result
    const validation = await this.agents.validator.validateDocument(mergedData);

    return {
      extracted_data: mergedData,
      validation: validation,
      bmad_analysis: bmadAnalysis.agent_analysis,
      basic_analysis: basicAnalysis,
      quality_score: validation.overall_score,
      processing_strategy: 'parallel'
    };
  }

  // Basic processing (fallback)
  async basicProcessing(transcriptPath, processingId) {
    console.log(`📄 [${processingId}] Basic processing mode`);

    const transcript = fs.readFileSync(transcriptPath, 'utf8');
    const basicResult = await this.runBasicOllamaAnalysis(transcript);

    // Still validate even basic results
    const validation = await this.agents.validator.validateDocument(basicResult);

    return {
      extracted_data: basicResult,
      validation: validation,
      quality_score: validation.overall_score,
      processing_strategy: 'basic'
    };
  }

  // Run basic Ollama analysis (similar to current n8n workflow)
  async runBasicOllamaAnalysis(transcript) {
    const prompt = this.generateBasicPrompt(transcript);

    const response = await axios.post(`${this.config.ollama_url}/api/generate`, {
      model: 'gpt-oss:20b',
      prompt: prompt,
      stream: false,
      temperature: 0.1
    });

    // Parse JSON from response
    const responseText = response.data.response.trim();
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);

    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    } else {
      throw new Error('Failed to extract JSON from basic analysis');
    }
  }

  generateBasicPrompt(transcript) {
    // Use existing enhanced prompt from the project
    const enhancedPromptPath = path.join(__dirname, '../enhanced-estate-planning-prompt.json');

    try {
      const promptConfig = JSON.parse(fs.readFileSync(enhancedPromptPath, 'utf8'));
      return promptConfig.prompt.replace('{{ $binary.data.toString() }}', transcript);
    } catch (error) {
      // Fallback basic prompt
      return `Analyze this estate planning transcript and extract client information as JSON:

${transcript}

Return only valid JSON with fields: client_name, meeting_stage, estate_value, marital_status, etc.`;
    }
  }

  // Merge analysis results with intelligent priority
  mergeAnalysisResults(bmadResult, basicResult) {
    const merged = { ...basicResult };

    // BMAD analysis takes priority for enhanced fields
    if (bmadResult.agent_analysis) {
      merged.agent_analysis = bmadResult.agent_analysis;

      // Override with BMAD insights where available
      if (bmadResult.estate_value) merged.estate_value = bmadResult.estate_value;
      if (bmadResult.family_structure) merged.family_structure = bmadResult.family_structure;
      if (bmadResult.business_entities) merged.business_entities = bmadResult.business_entities;
    }

    // Merge other fields, preferring non-null values
    Object.keys(bmadResult).forEach(key => {
      if (bmadResult[key] && (!merged[key] || merged[key] === '')) {
        merged[key] = bmadResult[key];
      }
    });

    return merged;
  }

  // Trigger N8N workflow with processed data
  async triggerN8NWorkflow(data, processingId) {
    try {
      const webhookUrl = `${this.config.n8n_url}${this.config.webhook_path}`;

      const payload = {
        processing_id: processingId,
        source: 'bmad-enhanced',
        data: data,
        timestamp: new Date().toISOString()
      };

      const response = await axios.post(webhookUrl, payload, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 30000
      });

      console.log(`🔗 [${processingId}] N8N workflow triggered successfully`);
      return response.data;

    } catch (error) {
      console.error(`❌ [${processingId}] N8N trigger failed:`, error.message);
      throw error;
    }
  }

  // Send data directly to Baserow
  async sendToBaserow(data, processingId) {
    try {
      const baserowConfig = this.loadBaserowConfig();
      const tableId = baserowConfig.tables.CRM.id;

      const response = await axios.post(
        `${this.config.baserow_url}/api/database/rows/table/${tableId}/`,
        data,
        {
          headers: {
            'Authorization': `Token ${baserowConfig.token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log(`💾 [${processingId}] Data saved to Baserow`);
      return response.data;

    } catch (error) {
      console.error(`❌ [${processingId}] Baserow save failed:`, error.message);
      throw error;
    }
  }

  loadBaserowConfig() {
    try {
      const configPath = path.join(__dirname, '../baserow_config.json');
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return config.baserow;
    } catch (error) {
      throw new Error('Baserow configuration not found');
    }
  }

  // Batch processing for multiple transcripts
  async batchProcess(transcriptDirectory, options = {}) {
    console.log(`📁 Starting batch processing: ${transcriptDirectory}`);

    const files = fs.readdirSync(transcriptDirectory)
      .filter(file => file.endsWith('.txt'))
      .map(file => path.join(transcriptDirectory, file));

    console.log(`📋 Found ${files.length} transcript files`);

    const results = [];
    const batchSize = options.batchSize || 5;
    const saveToBaserow = options.saveToBaserow || false;

    for (let i = 0; i < files.length; i += batchSize) {
      const batch = files.slice(i, i + batchSize);
      console.log(`🔄 Processing batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(files.length / batchSize)}`);

      const batchPromises = batch.map(async (filePath) => {
        try {
          const result = await this.processTranscript(filePath);

          if (saveToBaserow && result.extracted_data && result.quality_score >= this.config.quality_threshold) {
            await this.sendToBaserow(result.extracted_data, result.processing_metadata.processing_id);
          }

          return result;
        } catch (error) {
          return { error: error.message, file: filePath };
        }
      });

      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);

      // Brief pause between batches
      if (i + batchSize < files.length) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    this.generateBatchReport(results);
    return results;
  }

  generateBatchReport(results) {
    const report = {
      total_files: results.length,
      successful: results.filter(r => !r.error).length,
      failed: results.filter(r => r.error).length,
      average_quality: 0,
      processing_stats: this.processingStats
    };

    const qualityScores = results
      .filter(r => r.quality_score)
      .map(r => r.quality_score);

    if (qualityScores.length > 0) {
      report.average_quality = Math.round(
        qualityScores.reduce((a, b) => a + b, 0) / qualityScores.length
      );
    }

    console.log(`📊 Batch Processing Report:`);
    console.log(`   Total Files: ${report.total_files}`);
    console.log(`   Successful: ${report.successful}`);
    console.log(`   Failed: ${report.failed}`);
    console.log(`   Average Quality: ${report.average_quality}%`);

    // Save detailed report
    const reportPath = path.join(__dirname, '../batch-processing-report.json');
    fs.writeFileSync(reportPath, JSON.stringify({ report, results }, null, 2));
    console.log(`📄 Detailed report saved: ${reportPath}`);
  }

  updateStats(success, processingTime, qualityScore = null) {
    this.processingStats.total_processed++;

    if (success) {
      this.processingStats.successful++;
      if (qualityScore) {
        this.processingStats.quality_scores.push(qualityScore);
      }
    } else {
      this.processingStats.failed++;
    }

    // Update average processing time
    const totalTime = (this.processingStats.average_processing_time * (this.processingStats.total_processed - 1)) + processingTime;
    this.processingStats.average_processing_time = Math.round(totalTime / this.processingStats.total_processed);
  }

  generateProcessingId() {
    return `bmad_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Health check for all services
  async healthCheck() {
    console.log(`🏥 Running health check...`);

    const services = {
      ollama: { url: `${this.config.ollama_url}/api/tags`, status: 'unknown' },
      n8n: { url: this.config.n8n_url, status: 'unknown' },
      baserow: { url: this.config.baserow_url, status: 'unknown' }
    };

    for (const [name, service] of Object.entries(services)) {
      try {
        await axios.get(service.url, { timeout: 5000 });
        service.status = 'healthy';
        console.log(`✅ ${name}: healthy`);
      } catch (error) {
        service.status = 'unhealthy';
        console.log(`❌ ${name}: unhealthy - ${error.message}`);
      }
    }

    return services;
  }

  // CLI interface
  async processFromCLI() {
    const args = process.argv.slice(2);
    const command = args[0];

    switch (command) {
      case 'process':
        const filePath = args[1];
        if (!filePath) {
          console.log('Usage: node bmad-n8n-bridge.js process <transcript-file>');
          return;
        }
        const result = await this.processTranscript(filePath);
        console.log(JSON.stringify(result, null, 2));
        break;

      case 'batch':
        const directory = args[1];
        if (!directory) {
          console.log('Usage: node bmad-n8n-bridge.js batch <transcript-directory>');
          return;
        }
        await this.batchProcess(directory, { saveToBaserow: true });
        break;

      case 'health':
        await this.healthCheck();
        break;

      default:
        console.log('Available commands:');
        console.log('  process <file>      - Process single transcript');
        console.log('  batch <directory>   - Process all transcripts in directory');
        console.log('  health              - Check service health');
        break;
    }
  }
}

// CLI execution
if (require.main === module) {
  const bridge = new BMADN8NBridge({
    processing_mode: 'enhanced',
    quality_threshold: 75
  });

  bridge.processFromCLI().catch(console.error);
}

module.exports = BMADN8NBridge;