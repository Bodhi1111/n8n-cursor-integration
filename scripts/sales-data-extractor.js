/**
 * Sales Data Extractor - BMad Method Integration
 * Extracts structured sales data from meeting transcripts
 */

const fs = require('fs');
const path = require('path');

class SalesDataExtractor {
  constructor() {
    this.bmadAnalystPrompt = this.createAnalystPrompt();
  }

  /**
   * Create BMad Method Analyst prompt for sales data extraction
   */
  createAnalystPrompt() {
    return `
You are Mary, the BMad Method Business Analyst. Your role is to extract comprehensive sales intelligence from meeting transcripts with precision and strategic insight.

Core Principles:
- Curiosity-Driven Inquiry: Uncover underlying motivations and unstated needs
- Objective & Evidence-Based: Ground findings in verifiable transcript content
- Strategic Contextualization: Frame insights within broader business context
- Actionable Intelligence: Provide clear, implementable recommendations

Extract the following data structure from the transcript:

{
  "contactInfo": [
    {
      "name": "Contact name",
      "title": "Job title",
      "email": "email if mentioned",
      "phone": "phone if mentioned",
      "linkedin": "linkedin if mentioned",
      "role": "decision_maker|influencer|user|gatekeeper"
    }
  ],
  "companyDetails": {
    "size": "startup|small|medium|large|enterprise",
    "industry": "Industry category",
    "revenue": "Revenue range if mentioned",
    "employees": "Employee count if mentioned",
    "headquarters": "Location if mentioned",
    "subsidiaries": "Subsidiary companies if mentioned"
  },
  "salesStage": "lead_qualification|needs_assessment|solution_presentation|proposal|negotiation|closing|won|lost",
  "salesMetrics": {
    "dealSize": "Potential deal value",
    "probability": "Win probability percentage",
    "timeline": "Expected close timeline",
    "competitors": ["List of competitors mentioned"]
  },
  "painPoints": [
    {
      "description": "Specific pain point",
      "impact": "Business impact described",
      "urgency": "high|medium|low",
      "costOfInaction": "What happens if not solved"
    }
  ],
  "requirements": [
    {
      "requirement": "Specific requirement",
      "priority": "must_have|nice_to_have|future",
      "technicalSpecs": "Technical details if mentioned"
    }
  ],
  "budgetIndicators": {
    "range": "Budget range if mentioned",
    "timeframe": "Budget availability timeline",
    "approvalProcess": "Who needs to approve",
    "currentSpend": "What they currently spend on similar solutions"
  },
  "decisionCriteria": [
    {
      "criteria": "Decision factor",
      "weight": "high|medium|low",
      "details": "Specific requirements"
    }
  ],
  "nextSteps": [
    {
      "action": "Specific next step",
      "owner": "Who is responsible",
      "timeline": "When it should happen",
      "success_criteria": "How to measure completion"
    }
  ],
  "keyQuotes": [
    {
      "quote": "Exact quote from transcript",
      "speaker": "Who said it",
      "context": "Why this quote is significant",
      "socialMediaPotential": "high|medium|low"
    }
  ],
  "competitiveIntel": {
    "currentSolutions": ["What they currently use"],
    "previousVendors": ["Previous vendors they've tried"],
    "competitorMentions": ["Competitors they're considering"],
    "differentiationOpportunities": ["How we can differentiate"]
  },
  "riskFactors": [
    {
      "risk": "Potential deal risk",
      "likelihood": "high|medium|low",
      "mitigation": "How to address this risk"
    }
  ],
  "sentiment": {
    "overall": "positive|neutral|negative",
    "engagement": "high|medium|low",
    "buyingSignals": ["Positive buying signals detected"],
    "concerns": ["Concerns or objections raised"]
  }
}

Analyze this transcript with the depth and insight of an experienced sales analyst.
`;
  }

  /**
   * Extract sales data from transcript content
   * @param {Object} transcriptData - The transcript data object
   * @returns {Object} Structured sales data
   */
  extractSalesData(transcriptData) {
    try {
      const { transcriptContent, companyName, meetingDate, meetingType } = transcriptData;

      // Create analysis prompt with transcript content
      const fullPrompt = `
${this.bmadAnalystPrompt}

Meeting Context:
- Company: ${companyName}
- Date: ${meetingDate}
- Meeting Type: ${meetingType}

Transcript Content:
${transcriptContent}

Please analyze this transcript and return the structured JSON data as specified above.
`;

      return {
        ...transcriptData,
        analysisPrompt: fullPrompt,
        extractorVersion: '1.0.0',
        analysisRequested: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error in sales data extraction:', error);
      return {
        ...transcriptData,
        error: error.message,
        extractionStatus: 'failed'
      };
    }
  }

  /**
   * Parse LLM response and validate structure
   * @param {string} llmResponse - Raw LLM response
   * @returns {Object} Parsed and validated sales data
   */
  parseLLMResponse(llmResponse) {
    try {
      // Extract JSON from response
      const jsonMatch = llmResponse.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        throw new Error('No JSON found in LLM response');
      }

      const salesData = JSON.parse(jsonMatch[0]);

      // Validate required fields
      this.validateSalesData(salesData);

      return {
        ...salesData,
        extractionStatus: 'completed',
        parsedAt: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error parsing LLM response:', error);
      return {
        extractionStatus: 'failed',
        error: error.message,
        rawResponse: llmResponse
      };
    }
  }

  /**
   * Validate sales data structure
   * @param {Object} salesData - Sales data to validate
   */
  validateSalesData(salesData) {
    const requiredFields = [
      'contactInfo',
      'companyDetails',
      'salesStage',
      'painPoints',
      'nextSteps'
    ];

    for (const field of requiredFields) {
      if (!salesData.hasOwnProperty(field)) {
        throw new Error(`Missing required field: ${field}`);
      }
    }

    // Validate arrays
    if (!Array.isArray(salesData.contactInfo)) {
      throw new Error('contactInfo must be an array');
    }

    if (!Array.isArray(salesData.painPoints)) {
      throw new Error('painPoints must be an array');
    }

    if (!Array.isArray(salesData.nextSteps)) {
      throw new Error('nextSteps must be an array');
    }
  }

  /**
   * Generate summary statistics
   * @param {Object} salesData - Extracted sales data
   * @returns {Object} Summary statistics
   */
  generateSummary(salesData) {
    return {
      contactCount: salesData.contactInfo?.length || 0,
      painPointCount: salesData.painPoints?.length || 0,
      nextStepCount: salesData.nextSteps?.length || 0,
      keyQuoteCount: salesData.keyQuotes?.length || 0,
      riskFactorCount: salesData.riskFactors?.length || 0,
      hasbudgetInfo: !!salesData.budgetIndicators?.range,
      hasCompetitorIntel: (salesData.competitiveIntel?.currentSolutions?.length || 0) > 0,
      sentimentScore: salesData.sentiment?.overall || 'unknown'
    };
  }
}

// Export for use in n8n Function nodes
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SalesDataExtractor;
}

// For testing in n8n context
if (typeof items !== 'undefined') {
  const extractor = new SalesDataExtractor();
  const result = extractor.extractSalesData(items[0].json);
  return [{ json: result }];
}