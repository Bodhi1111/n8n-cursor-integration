/**
 * Batch Processor Helper
 * Utilities for managing bulk transcript processing
 */

const fs = require('fs');
const path = require('path');

class BatchProcessorHelper {
  constructor() {
    this.hostTranscriptPath = '/Users/joshuavaughan/Documents/McAdams Transcripts';
    this.containerPath = '/files/transcripts/incoming';
    this.processedPath = '/files/transcripts/processed';
    this.archivePath = '/files/transcripts/archive';
  }

  /**
   * Scan for existing transcript files
   */
  scanForTranscripts() {
    try {
      if (!fs.existsSync(this.hostTranscriptPath)) {
        console.log(`❌ Transcript folder not found: ${this.hostTranscriptPath}`);
        return [];
      }

      const files = fs.readdirSync(this.hostTranscriptPath);
      const transcriptFiles = files.filter(file => {
        const ext = path.extname(file).toLowerCase();
        return ['.txt', '.md', '.docx'].includes(ext);
      });

      console.log(`📁 Found ${transcriptFiles.length} transcript files:`);
      transcriptFiles.forEach((file, index) => {
        console.log(`   ${index + 1}. ${file}`);
      });

      return transcriptFiles;
    } catch (error) {
      console.error('Error scanning for transcripts:', error.message);
      return [];
    }
  }

  /**
   * Analyze transcript files for metadata
   */
  analyzeTranscripts() {
    const files = this.scanForTranscripts();

    if (files.length === 0) {
      console.log('No transcript files found to analyze.');
      return [];
    }

    const analysis = files.map(file => {
      const filePath = path.join(this.hostTranscriptPath, file);
      let stats = null;
      let content = '';

      try {
        stats = fs.statSync(filePath);
        content = fs.readFileSync(filePath, 'utf8');
      } catch (error) {
        console.warn(`⚠️ Could not read ${file}: ${error.message}`);
        return null;
      }

      // Extract metadata from filename
      const fileNameParts = file.split('_');
      const dateMatch = file.match(/\d{4}-\d{2}-\d{2}/);

      // Extract metadata from content
      const wordCount = content.split(/\s+/).length;
      const lineCount = content.split('\n').length;
      const companyMatch = content.match(/(?:Company|Client|Organization):\s*([^\n]+)/i);
      const attendeeMatches = content.match(/Attendees?:\s*([^\n]+(?:\n-[^\n]+)*)/i);

      return {
        fileName: file,
        fileSize: stats.size,
        lastModified: stats.mtime,
        extractedMetadata: {
          meetingDate: dateMatch ? dateMatch[0] : 'Unknown',
          companyName: fileNameParts[1] || (companyMatch ? companyMatch[1].trim() : 'Unknown'),
          meetingType: fileNameParts[2]?.replace(/\.[^.]+$/, '') || 'Meeting',
          wordCount,
          lineCount,
          attendeeCount: attendeeMatches ? attendeeMatches[1].split(/\n-|\n/).length : 0
        },
        contentPreview: content.substring(0, 200) + '...'
      };
    }).filter(item => item !== null);

    console.log('\n📊 Transcript Analysis Summary:');
    console.log(`   Total Files: ${analysis.length}`);
    console.log(`   Total Words: ${analysis.reduce((sum, a) => sum + a.extractedMetadata.wordCount, 0).toLocaleString()}`);
    console.log(`   Date Range: ${this.getDateRange(analysis)}`);
    console.log(`   Companies: ${this.getUniqueCompanies(analysis).length}`);

    return analysis;
  }

  /**
   * Get date range from analyzed transcripts
   */
  getDateRange(analysis) {
    const dates = analysis
      .map(a => a.extractedMetadata.meetingDate)
      .filter(date => date !== 'Unknown')
      .sort();

    if (dates.length === 0) return 'No dates found';
    if (dates.length === 1) return dates[0];

    return `${dates[0]} to ${dates[dates.length - 1]}`;
  }

  /**
   * Get unique companies from analyzed transcripts
   */
  getUniqueCompanies(analysis) {
    const companies = analysis
      .map(a => a.extractedMetadata.companyName)
      .filter(company => company !== 'Unknown');

    return [...new Set(companies)];
  }

  /**
   * Prepare files for batch processing
   */
  prepareBatchProcessing() {
    const analysis = this.analyzeTranscripts();

    if (analysis.length === 0) {
      console.log('No files to prepare for batch processing.');
      return false;
    }

    console.log('\n🚀 Batch Processing Preparation:');
    console.log(`   ${analysis.length} files ready for processing`);
    console.log(`   Estimated processing time: ${Math.ceil(analysis.length * 0.5)} minutes`);

    const estimatedTokens = analysis.reduce((sum, a) => sum + Math.ceil(a.extractedMetadata.wordCount * 1.3), 0);
    console.log(`   Estimated OpenAI tokens: ${estimatedTokens.toLocaleString()}`);
    console.log(`   Estimated cost: $${(estimatedTokens * 0.03 / 1000).toFixed(2)}`);

    // Group by company for organized processing
    const byCompany = this.groupByCompany(analysis);
    console.log(`\n🏢 Processing will organize ${Object.keys(byCompany).length} companies:`);
    Object.entries(byCompany).forEach(([company, files]) => {
      console.log(`   ${company}: ${files.length} files`);
    });

    return true;
  }

  /**
   * Group transcripts by company
   */
  groupByCompany(analysis) {
    return analysis.reduce((groups, transcript) => {
      const company = transcript.extractedMetadata.companyName;
      if (!groups[company]) groups[company] = [];
      groups[company].push(transcript);
      return groups;
    }, {});
  }

  /**
   * Generate batch processing report
   */
  generateBatchReport() {
    const analysis = this.analyzeTranscripts();

    const report = {
      scanDate: new Date().toISOString(),
      totalFiles: analysis.length,
      readyForProcessing: analysis.filter(a => a.extractedMetadata.companyName !== 'Unknown').length,
      needsAttention: analysis.filter(a => a.extractedMetadata.companyName === 'Unknown').length,
      byCompany: this.groupByCompany(analysis),
      byMeetingType: this.groupByMeetingType(analysis),
      dateRange: this.getDateRange(analysis),
      estimatedProcessingTime: Math.ceil(analysis.length * 0.5),
      files: analysis
    };

    // Save report to file
    const reportPath = path.join(__dirname, '..', 'data', 'batch-processing-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

    console.log(`\n📄 Batch processing report saved to: ${reportPath}`);

    return report;
  }

  /**
   * Group transcripts by meeting type
   */
  groupByMeetingType(analysis) {
    return analysis.reduce((groups, transcript) => {
      const type = transcript.extractedMetadata.meetingType;
      if (!groups[type]) groups[type] = [];
      groups[type].push(transcript);
      return groups;
    }, {});
  }

  /**
   * Create Notion database structure for batch processing
   */
  generateNotionStructure() {
    const structure = {
      title: 'Sales Transcript Dashboard',
      description: 'Comprehensive sales intelligence from processed meeting transcripts',
      properties: {
        'Company': { type: 'title' },
        'Meeting Date': { type: 'date' },
        'Meeting Type': {
          type: 'select',
          options: ['Discovery', 'Demo', 'Proposal', 'Negotiation', 'Closing', 'Follow-up', 'Check-in']
        },
        'Sales Stage': {
          type: 'select',
          options: ['Lead Qualification', 'Needs Assessment', 'Solution Presentation', 'Proposal', 'Negotiation', 'Closing', 'Won', 'Lost']
        },
        'Primary Contact': { type: 'rich_text' },
        'Email': { type: 'email' },
        'Industry': {
          type: 'select',
          options: ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Other']
        },
        'Company Size': {
          type: 'select',
          options: ['Startup', 'Small', 'Medium', 'Large', 'Enterprise']
        },
        'Urgency': {
          type: 'select',
          options: ['High', 'Medium', 'Low']
        },
        'Deal Value': { type: 'rich_text' },
        'Close Timeline': { type: 'rich_text' },
        'Next Steps': { type: 'rich_text' },
        'Pain Points': { type: 'rich_text' },
        'Key Quotes': { type: 'rich_text' },
        'Source File': { type: 'rich_text' },
        'Processing Date': { type: 'date' },
        'Batch Processing': { type: 'checkbox' }
      }
    };

    console.log('\n🗄️ Recommended Notion Database Structure:');
    console.log(JSON.stringify(structure, null, 2));

    return structure;
  }

  /**
   * Validate environment for batch processing
   */
  validateEnvironment() {
    console.log('🔍 Validating Environment for Batch Processing...\n');

    const checks = {
      transcriptFolder: fs.existsSync(this.hostTranscriptPath),
      hasTranscripts: false,
      dockerRunning: false,
      n8nAccessible: false
    };

    // Check transcript folder
    if (checks.transcriptFolder) {
      console.log('✅ Transcript folder exists');
      const files = this.scanForTranscripts();
      checks.hasTranscripts = files.length > 0;
      console.log(checks.hasTranscripts ? `✅ Found ${files.length} transcript files` : '❌ No transcript files found');
    } else {
      console.log('❌ Transcript folder not found');
    }

    // Check environment variables
    const requiredEnvVars = ['OPENAI_API_KEY', 'NOTION_API_KEY', 'NOTION_CRM_DATABASE_ID'];
    const missingEnvVars = requiredEnvVars.filter(varName => !process.env[varName]);

    if (missingEnvVars.length === 0) {
      console.log('✅ Required environment variables are set');
    } else {
      console.log(`❌ Missing environment variables: ${missingEnvVars.join(', ')}`);
    }

    console.log('\n📋 Pre-flight Checklist:');
    console.log(`   ${checks.transcriptFolder ? '✅' : '❌'} Transcript folder accessible`);
    console.log(`   ${checks.hasTranscripts ? '✅' : '❌'} Transcript files found`);
    console.log(`   ${missingEnvVars.length === 0 ? '✅' : '❌'} Environment variables configured`);
    console.log('   ⏳ Docker container running (check with: docker ps)');
    console.log('   ⏳ n8n accessible (check: http://localhost:5679)');

    return checks;
  }
}

// CLI interface
if (require.main === module) {
  const helper = new BatchProcessorHelper();
  const command = process.argv[2];

  switch (command) {
    case 'scan':
      helper.scanForTranscripts();
      break;
    case 'analyze':
      helper.analyzeTranscripts();
      break;
    case 'prepare':
      helper.prepareBatchProcessing();
      break;
    case 'report':
      helper.generateBatchReport();
      break;
    case 'notion':
      helper.generateNotionStructure();
      break;
    case 'validate':
      helper.validateEnvironment();
      break;
    default:
      console.log('📝 Batch Processor Helper - Usage:');
      console.log('   node scripts/batch-processor-helper.js scan     - Scan for transcript files');
      console.log('   node scripts/batch-processor-helper.js analyze  - Analyze transcript metadata');
      console.log('   node scripts/batch-processor-helper.js prepare  - Prepare for batch processing');
      console.log('   node scripts/batch-processor-helper.js report   - Generate detailed report');
      console.log('   node scripts/batch-processor-helper.js notion   - Show Notion database structure');
      console.log('   node scripts/batch-processor-helper.js validate - Validate environment setup');
  }
}

module.exports = BatchProcessorHelper;