/**
 * Test Suite for Sales Transcript Processing Workflow
 * Tests all components independently and as an integrated system
 */

const fs = require('fs');
const path = require('path');

// Import our modules
const SalesDataExtractor = require('./sales-data-extractor');
const EmailRecapGenerator = require('./email-recap-generator');
const SocialContentGenerator = require('./social-content-generator');

class SalesWorkflowTester {
  constructor() {
    this.salesExtractor = new SalesDataExtractor();
    this.emailGenerator = new EmailRecapGenerator();
    this.socialGenerator = new SocialContentGenerator();

    this.mockTranscript = this.createMockTranscript();
    this.testResults = {
      passed: 0,
      failed: 0,
      errors: []
    };
  }

  /**
   * Create mock transcript data for testing
   */
  createMockTranscript() {
    return {
      fileName: '2024-01-15_TechCorp_Discovery.txt',
      filePath: '/test/transcripts/2024-01-15_TechCorp_Discovery.txt',
      meetingDate: '2024-01-15',
      companyName: 'TechCorp',
      meetingType: 'Discovery',
      wordCount: 2847,
      estimatedDuration: '45 min',
      processedAt: new Date().toISOString(),
      transcriptContent: `
Meeting: Discovery Call with TechCorp
Date: January 15, 2024
Attendees:
- Sarah Johnson, CEO (TechCorp)
- Mike Wilson, CTO (TechCorp)
- Alex Chen, Sales Rep (Our Company)
Duration: 45 minutes

Alex: Thanks for joining today, Sarah and Mike. I'd love to learn more about TechCorp and understand your current challenges.

Sarah: Absolutely. We're a 150-person SaaS company in the fintech space. We've been growing rapidly, but we're hitting some scaling issues with our current infrastructure.

Mike: Our biggest pain point right now is data synchronization across our microservices. We're spending about 20 hours a week manually reconciling data, and it's costing us roughly $50,000 per month in developer time.

Alex: That's significant. Tell me more about your current architecture.

Mike: We're running on AWS with about 12 microservices. Each service has its own database, but we need real-time data consistency across all of them. Our current solution is batch processing, but it's not scalable.

Sarah: We're looking at a 6-month timeline to solve this. Our board is pushing for a solution because it's affecting our product quality and customer satisfaction scores.

Alex: What's your budget range for addressing this?

Sarah: We're approved for up to $200,000 for the right solution. We've looked at building internally, but that would take 18 months and cost closer to $500,000.

Mike: We've also evaluated DataSync Pro and StreamLine Solutions. DataSync is cheaper at $80,000, but their real-time capabilities are limited. StreamLine is $250,000 but seems over-engineered for our needs.

Sarah: What I love about your approach is the focus on gradual migration. We can't afford downtime.

Alex: That's exactly what we specialize in. Our zero-downtime migration approach has helped companies like yours reduce implementation time by 60%.

Mike: The API-first architecture is also appealing. We need something that integrates with our existing tools.

Sarah: If we move forward, I'd need to get buy-in from our head of engineering, David Kumar, and our CFO, Lisa Park. They'll want to see a detailed technical proposal and ROI analysis.

Alex: Perfect. I can prepare a technical proposal showing exactly how we'd integrate with your current stack, plus a detailed ROI breakdown. When would be a good time to present this to your team?

Sarah: How about next Friday at 2 PM? That gives you a week to prepare, and it works with everyone's schedule.

Mike: I'll need to see performance benchmarks too. Latency is critical for our real-time trading features.

Alex: Absolutely. I'll include performance data from similar implementations. Our average latency improvement is 75%.

Sarah: This sounds promising. One concern is vendor lock-in. How flexible is your solution if we need to change direction?

Alex: Great question. Our platform is built on open standards, and we provide full data export capabilities. You own your data completely.

Mike: What about support during implementation?

Alex: We provide dedicated implementation support with weekly check-ins, plus 24/7 technical support for the first 90 days.

Sarah: Excellent. I'm excited to see the proposal. This could be exactly what we need to scale efficiently.

Action Items:
- Alex to prepare technical proposal and ROI analysis by January 22
- Sarah to schedule follow-up meeting with engineering team for January 26
- Mike to compile current performance metrics for baseline comparison
- Alex to send case studies from similar fintech implementations
      `
    };
  }

  /**
   * Run all tests
   */
  async runAllTests() {
    console.log('🧪 Starting Sales Workflow Test Suite\n');

    try {
      await this.testSalesDataExtraction();
      await this.testEmailGeneration();
      await this.testSocialContentGeneration();
      await this.testIntegratedWorkflow();

      this.printResults();
    } catch (error) {
      console.error('❌ Test suite failed:', error);
      this.testResults.errors.push(`Test suite error: ${error.message}`);
    }
  }

  /**
   * Test sales data extraction
   */
  async testSalesDataExtraction() {
    console.log('📊 Testing Sales Data Extraction...');

    try {
      // Test basic extraction
      const extractedData = this.salesExtractor.extractSalesData(this.mockTranscript);

      this.assert(extractedData.analysisPrompt, 'Analysis prompt should be generated');
      this.assert(extractedData.extractorVersion, 'Extractor version should be set');
      this.assert(extractedData.analysisRequested, 'Analysis timestamp should be set');

      // Test LLM response parsing
      const mockLLMResponse = `
Here's the extracted sales data:

{
  "contactInfo": [
    {
      "name": "Sarah Johnson",
      "title": "CEO",
      "role": "decision_maker"
    },
    {
      "name": "Mike Wilson",
      "title": "CTO",
      "role": "influencer"
    }
  ],
  "companyDetails": {
    "size": "medium",
    "industry": "fintech",
    "employees": "150"
  },
  "salesStage": "needs_assessment",
  "salesMetrics": {
    "dealSize": "$200,000",
    "timeline": "6 months"
  },
  "painPoints": [
    {
      "description": "Data synchronization across microservices",
      "impact": "Costing $50,000 per month in developer time",
      "urgency": "high"
    }
  ],
  "budgetIndicators": {
    "range": "$200,000",
    "timeframe": "6 months"
  },
  "nextSteps": [
    {
      "action": "Prepare technical proposal and ROI analysis",
      "owner": "Alex",
      "timeline": "January 22"
    }
  ],
  "keyQuotes": [
    {
      "quote": "What I love about your approach is the focus on gradual migration",
      "speaker": "Sarah Johnson",
      "socialMediaPotential": "high"
    }
  ]
}
      `;

      const parsedData = this.salesExtractor.parseLLMResponse(mockLLMResponse);

      this.assert(parsedData.extractionStatus === 'completed', 'Extraction should be completed');
      this.assert(parsedData.contactInfo.length === 2, 'Should extract 2 contacts');
      this.assert(parsedData.salesStage === 'needs_assessment', 'Sales stage should be correct');
      this.assert(parsedData.painPoints.length === 1, 'Should extract pain points');
      this.assert(parsedData.budgetIndicators.range === '$200,000', 'Budget should be extracted');

      // Test summary generation
      const summary = this.salesExtractor.generateSummary(parsedData);
      this.assert(summary.contactCount === 2, 'Summary should show correct contact count');
      this.assert(summary.hasbudgetInfo === true, 'Summary should indicate budget info present');

      console.log('✅ Sales Data Extraction tests passed\n');

    } catch (error) {
      console.log('❌ Sales Data Extraction tests failed:', error.message);
      this.testResults.errors.push(`Sales extraction error: ${error.message}`);
      this.testResults.failed++;
    }
  }

  /**
   * Test email generation
   */
  async testEmailGeneration() {
    console.log('📧 Testing Email Generation...');

    try {
      // Create mock sales data
      const mockSalesData = {
        ...this.mockTranscript,
        extractionStatus: 'completed',
        contactInfo: [
          {
            name: 'Sarah Johnson',
            title: 'CEO',
            email: 'sarah@techcorp.com',
            role: 'decision_maker'
          }
        ],
        companyDetails: {
          industry: 'fintech',
          size: 'medium'
        },
        salesStage: 'needs_assessment',
        painPoints: [
          {
            description: 'Data synchronization across microservices',
            impact: 'Costing $50,000 per month',
            urgency: 'high'
          }
        ],
        requirements: [
          {
            requirement: 'Zero-downtime migration',
            priority: 'must_have'
          }
        ],
        nextSteps: [
          {
            action: 'Prepare technical proposal',
            owner: 'Alex',
            timeline: 'January 22'
          }
        ],
        budgetIndicators: {
          range: '$200,000'
        },
        sentiment: {
          overall: 'positive',
          urgency: 'high'
        }
      };

      const emailData = this.emailGenerator.generateRecap(mockSalesData);

      this.assert(emailData.emailRecap, 'Email content should be generated');
      this.assert(emailData.emailSubject, 'Email subject should be generated');
      this.assert(emailData.emailType, 'Email type should be determined');
      this.assert(emailData.recipientEmail === 'sarah@techcorp.com', 'Primary email should be extracted');
      this.assert(emailData.priority, 'Priority should be set');

      // Test email content quality
      this.assert(emailData.emailRecap.includes('TechCorp'), 'Email should include company name');
      this.assert(emailData.emailRecap.includes('Data synchronization'), 'Email should include pain points');
      this.assert(emailData.emailRecap.includes('technical proposal'), 'Email should include next steps');

      console.log('✅ Email Generation tests passed\n');

    } catch (error) {
      console.log('❌ Email Generation tests failed:', error.message);
      this.testResults.errors.push(`Email generation error: ${error.message}`);
      this.testResults.failed++;
    }
  }

  /**
   * Test social content generation
   */
  async testSocialContentGeneration() {
    console.log('📱 Testing Social Content Generation...');

    try {
      const mockSalesData = {
        ...this.mockTranscript,
        contactInfo: [{ name: 'Sarah Johnson', title: 'CEO' }],
        companyDetails: { industry: 'fintech', size: 'medium' },
        painPoints: [
          {
            description: 'Data synchronization challenges',
            urgency: 'high'
          }
        ],
        keyQuotes: [
          {
            quote: 'What I love about your approach is the focus on gradual migration',
            speaker: 'Sarah Johnson',
            socialMediaPotential: 'high'
          }
        ],
        sentiment: {
          overall: 'positive',
          engagement: 'high'
        }
      };

      const socialData = this.socialGenerator.generateAllContent(mockSalesData);

      this.assert(socialData.socialContent, 'Social content should be generated');
      this.assert(socialData.socialContent.linkedin, 'LinkedIn content should be generated');
      this.assert(socialData.socialContent.twitter, 'Twitter content should be generated');
      this.assert(socialData.socialContent.instagram, 'Instagram content should be generated');
      this.assert(socialData.socialContent.facebook, 'Facebook content should be generated');

      // Test LinkedIn content quality
      const linkedinPosts = socialData.socialContent.linkedin;
      this.assert(linkedinPosts.length > 0, 'Should generate LinkedIn posts');
      this.assert(linkedinPosts[0].content.includes('gradual migration'), 'Should include key quotes');

      // Test Twitter content
      const tweets = socialData.socialContent.twitter;
      this.assert(tweets.length > 0, 'Should generate tweets');
      this.assert(tweets[0].content.length <= 280, 'Tweets should be within character limit');

      console.log('✅ Social Content Generation tests passed\n');

    } catch (error) {
      console.log('❌ Social Content Generation tests failed:', error.message);
      this.testResults.errors.push(`Social content error: ${error.message}`);
      this.testResults.failed++;
    }
  }

  /**
   * Test integrated workflow
   */
  async testIntegratedWorkflow() {
    console.log('🔄 Testing Integrated Workflow...');

    try {
      // Simulate the full workflow
      const data = { ...this.mockTranscript };

      // Step 1: Extract metadata (already done in mock)
      this.assert(data.companyName === 'TechCorp', 'Company name should be extracted');
      this.assert(data.meetingType === 'Discovery', 'Meeting type should be extracted');

      // Step 2: Sales data extraction
      const extractedData = this.salesExtractor.extractSalesData(data);
      this.assert(extractedData.analysisPrompt, 'Analysis prompt should be ready');

      // Step 3: Mock LLM response and parse
      const mockLLMResponse = '{"contactInfo": [{"name": "Sarah Johnson", "role": "decision_maker"}], "companyDetails": {"industry": "fintech", "size": "medium"}, "salesStage": "needs_assessment", "painPoints": [{"description": "Data sync issues"}], "nextSteps": [{"action": "Prepare proposal"}]}';
      const salesData = this.salesExtractor.parseLLMResponse(mockLLMResponse);

      const completeData = { ...extractedData, ...salesData };

      // Step 4: Generate email recap
      const emailData = this.emailGenerator.generateRecap(completeData);
      this.assert(emailData.emailRecap, 'Email should be generated');

      // Step 5: Generate social content
      const socialData = this.socialGenerator.generateAllContent(completeData);
      this.assert(socialData.socialContent, 'Social content should be generated');

      // Step 6: Validate complete workflow output
      const finalOutput = { ...emailData, ...socialData };

      this.assert(finalOutput.emailRecap, 'Final output should include email');
      this.assert(finalOutput.socialContent, 'Final output should include social content');
      this.assert(finalOutput.extractionStatus === 'completed', 'Extraction should be completed');

      console.log('✅ Integrated Workflow tests passed\n');

    } catch (error) {
      console.log('❌ Integrated Workflow tests failed:', error.message);
      this.testResults.errors.push(`Integrated workflow error: ${error.message}`);
      this.testResults.failed++;
    }
  }

  /**
   * Assert helper function
   */
  assert(condition, message) {
    if (condition) {
      this.testResults.passed++;
    } else {
      this.testResults.failed++;
      this.testResults.errors.push(message);
      throw new Error(message);
    }
  }

  /**
   * Print test results
   */
  printResults() {
    console.log('📋 Test Results Summary:');
    console.log('========================');
    console.log(`✅ Passed: ${this.testResults.passed}`);
    console.log(`❌ Failed: ${this.testResults.failed}`);
    console.log(`📊 Total: ${this.testResults.passed + this.testResults.failed}`);

    if (this.testResults.errors.length > 0) {
      console.log('\n🚨 Errors:');
      this.testResults.errors.forEach((error, index) => {
        console.log(`${index + 1}. ${error}`);
      });
    }

    if (this.testResults.failed === 0) {
      console.log('\n🎉 All tests passed! Your sales workflow is ready to go.');
    } else {
      console.log('\n⚠️  Some tests failed. Please review and fix the issues before deploying.');
    }
  }

  /**
   * Generate test transcript file
   */
  generateTestFile() {
    const testFile = path.join(__dirname, '..', 'test-transcript.txt');
    fs.writeFileSync(testFile, this.mockTranscript.transcriptContent);
    console.log(`📝 Test transcript written to: ${testFile}`);
    return testFile;
  }

  /**
   * Clean up test files
   */
  cleanup() {
    const testFile = path.join(__dirname, '..', 'test-transcript.txt');
    if (fs.existsSync(testFile)) {
      fs.unlinkSync(testFile);
      console.log('🧹 Test files cleaned up');
    }
  }
}

// Run tests if called directly
if (require.main === module) {
  const tester = new SalesWorkflowTester();

  tester.runAllTests()
    .then(() => {
      // Optionally generate test file for manual testing
      if (process.argv.includes('--generate-test-file')) {
        tester.generateTestFile();
      }

      if (process.argv.includes('--cleanup')) {
        tester.cleanup();
      }
    })
    .catch(error => {
      console.error('Test suite error:', error);
      process.exit(1);
    });
}

module.exports = SalesWorkflowTester;